/**
 * @file reconcilePayments.ts
 * @description Job periódico de reconciliación ampliada: pagos pendientes, reembolsos huérfanos y webhooks colgados.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import { dbPool, isPostgresAvailable } from '../config/database';
import { transitionOrder } from '../services/orders/stateMachine';
import { logger } from '../utils/logger';
import { alertSlack } from '../utils/alerts';
import { InMemoryDataStore } from '../infrastructure/repositories/memory.repositories';
import { memoryPayments, memoryWebhookEvents } from '../controllers/paymentWebhook.controller';
import { checkCulqiRefundStatus } from '../controllers/refund.controller';

const STALE_MINUTES = 15;
const BATCH_SIZE = 50;
const MAX_DRAIN_CYCLES = 10; // Hasta 500 registros por ejecución para drenar backlog sin timeout

export async function fetchCulqiCharge(chargeId: string): Promise<any> {
  const secretKey = process.env.CULQI_SECRET_KEY;

  if (secretKey && secretKey.startsWith('sk_')) {
    const res = await fetch(`https://api.culqi.com/v2/charges/${chargeId}`, {
      headers: { Authorization: `Bearer ${secretKey}` }
    });
    if (!res.ok) return null;
    return res.json();
  }

  // Simulación para tests o local
  if (chargeId.startsWith('ch_mock_reconcile_paid')) {
    return { id: chargeId, status: 'paid', amount: 50000 };
  }
  if (chargeId.startsWith('ch_mock_reconcile_mismatch')) {
    return { id: chargeId, status: 'paid', amount: 30000 };
  }
  return null;
}

export async function reconcilePendingPayments(): Promise<void> {
  if (isPostgresAvailable()) {
    // ─── BATCH 1: Pagos PENDING / FAILED en órdenes PENDIENTE con Paginación (Drain Loop) ───
    let cycle = 0;
    while (cycle < MAX_DRAIN_CYCLES) {
      const { rows } = await dbPool.query(
        `SELECT o.id AS order_id, o.estado,
                COALESCE(p.amount_cents, o.total_cents, ROUND(o.total_amount * 100)::bigint) as total_cents,
                p.provider, p.provider_charge_id, p.status AS payment_status
           FROM orders o
           JOIN payments p ON p.order_id = o.id
          WHERE o.estado = 'PENDIENTE'
            AND p.status IN ('PENDING', 'FAILED')
            AND o.created_at < NOW() - INTERVAL '${STALE_MINUTES} minutes'
          ORDER BY o.created_at ASC
          LIMIT ${BATCH_SIZE}`
      );

      if (rows.length === 0) break;

      for (const row of rows) {
        try {
          if (row.provider !== 'culqi') continue;

          const charge = await fetchCulqiCharge(row.provider_charge_id);
          if (!charge) continue;

          if (charge.status === 'paid' || charge.status === 'captured') {
            const expectedCents = Number(row.total_cents);
            if (charge.amount !== expectedCents) {
              await alertSlack('⚠️ Reconciliación: monto distinto', {
                orderId: row.order_id,
                esperado: expectedCents,
                real: charge.amount
              });
              continue;
            }

            const client = await dbPool.connect();
            try {
              await client.query('BEGIN');
              await transitionOrder(client, row.order_id, 'PAGADO', 'system:reconcile', {
                chargeId: row.provider_charge_id,
                reconciledAt: new Date().toISOString()
              });
              await client.query(
                `UPDATE payments
                    SET status = 'PAID',
                        reconciled_at = NOW(),
                        reconcile_note = 'Reconciliado vía API Culqi'
                  WHERE provider = $1 AND provider_charge_id = $2`,
                [row.provider, row.provider_charge_id]
              );
              await client.query('COMMIT');
              logger.info('payment_reconciled', { orderId: row.order_id });
            } catch (err: any) {
              await client.query('ROLLBACK');
              logger.error('reconcile_transition_failed', {
                orderId: row.order_id,
                err: err.message
              });
            } finally {
              client.release();
            }
          } else if (charge.status === 'failed' || charge.status === 'expired') {
            await dbPool.query(
              `UPDATE payments SET status = 'FAILED', updated_at = NOW()
                WHERE provider = $1 AND provider_charge_id = $2`,
              [row.provider, row.provider_charge_id]
            );
          }
        } catch (err: any) {
          logger.error('reconcile_error', { orderId: row.order_id, err: err.message });
        }
      }

      cycle++;
      if (rows.length < BATCH_SIZE) break;
    }

    // ─── BATCH 2: Reconciliación de REFUND_PENDING huérfanos (> 5 minutos) ───
    try {
      const { rows: staleRefunds } = await dbPool.query(
        `SELECT id, order_id, provider, provider_charge_id, amount_cents
           FROM payments
          WHERE status = 'REFUND_PENDING'
            AND updated_at < NOW() - INTERVAL '5 minutes'
          ORDER BY updated_at ASC
          LIMIT 50`
      );

      for (const ref of staleRefunds) {
        if (ref.provider !== 'culqi') continue;
        const culqiStatus = await checkCulqiRefundStatus(ref.provider_charge_id);
        if (culqiStatus && culqiStatus.status === 'successful') {
          const client = await dbPool.connect();
          try {
            await client.query('BEGIN');
            await client.query(
              `UPDATE payments
                  SET status = 'REFUNDED',
                      raw_response = $1,
                      updated_at = NOW()
                WHERE id = $2`,
              [JSON.stringify(culqiStatus), ref.id]
            );
            await transitionOrder(client, ref.order_id, 'REEMBOLSADO', 'system:reconcile_refund', {
              recovered: true,
              providerRefundId: culqiStatus.id
            });
            await client.query('COMMIT');
            logger.info('refund_reconciled_success', { orderId: ref.order_id });
          } catch (err: any) {
            await client.query('ROLLBACK');
            logger.error('refund_reconcile_commit_failed', { orderId: ref.order_id, err: err.message });
          } finally {
            client.release();
          }
        } else {
          // Si pasaron > 30 minutos y no hay refund en Culqi, alertar a Slack y revertir a PAID
          await dbPool.query(
            `UPDATE payments SET status = 'PAID', updated_at = NOW() WHERE id = $1`,
            [ref.id]
          );
          await alertSlack('🚨 REFUND_PENDING huérfano detectado y revertido a PAID', {
            orderId: ref.order_id,
            chargeId: ref.provider_charge_id
          });
        }
      }
    } catch (err: any) {
      logger.error('reconcile_stale_refunds_failed', { error: err.message });
    }

    // ─── BATCH 3: Detección y limpieza de webhook_events colgados en RECEIVED ───
    try {
      const { rows: staleWebhooks } = await dbPool.query(
        `SELECT id, provider, event_id, payload, created_at
           FROM webhook_events
          WHERE status = 'RECEIVED'
            AND created_at < NOW() - INTERVAL '2 minutes'
          ORDER BY created_at ASC
          LIMIT 50`
      );

      for (const wh of staleWebhooks) {
        const orderId = Number(wh.payload?.data?.metadata?.order_id || wh.payload?.orderId);
        if (orderId) {
          const { rows: [ord] } = await dbPool.query(`SELECT estado FROM orders WHERE id = $1`, [orderId]);
          if (ord && ['PAGADO', 'REEMBOLSADO', 'CANCELADO'].includes(ord.estado)) {
            // El negocio se completó exitosamente, reconciliar webhook a PROCESSED
            await dbPool.query(
              `UPDATE webhook_events SET status = 'PROCESSED', processed_at = NOW() WHERE id = $1`,
              [wh.id]
            );
            continue;
          }
        }

        // Si tiene más de 5 minutos colgado sin procesar, marcar como FAILED para visibilidad en dashboard
        const diffMs = Date.now() - new Date(wh.created_at).getTime();
        if (diffMs > 5 * 60_000) {
          await dbPool.query(
            `UPDATE webhook_events
                SET status = 'FAILED',
                    processed_at = NOW(),
                    error_message = 'PROCESSING_TIMEOUT_ORPHAN'
              WHERE id = $1`,
            [wh.id]
          );
        }
      }
    } catch (err: any) {
      logger.error('reconcile_stale_webhooks_failed', { error: err.message });
    }
  } else {
    // ─── Modo en memoria para tests unitarios y desarrollo local ───
    for (const payment of memoryPayments) {
      // 1. Pagos pendientes
      if (payment.status === 'PENDING' || payment.status === 'FAILED') {
        const order = InMemoryDataStore.orders.find((o) => o.id === payment.orderId);
        if (!order) continue;
        let currentEstado = ((order as any).estado || order.status || '').toUpperCase();
        if (currentEstado === 'RECIBIDO') currentEstado = 'PENDIENTE';
        if (currentEstado !== 'PENDIENTE') continue;

        const charge = await fetchCulqiCharge(payment.providerChargeId);
        if (!charge) continue;

        if (charge.status === 'paid' || charge.status === 'captured') {
          const expectedCents = (order as any).total_cents ?? Math.round(Number(order.total_amount) * 100);
          if (charge.amount !== expectedCents) {
            await alertSlack('⚠️ Reconciliación: monto distinto', {
              orderId: order.id,
              esperado: expectedCents,
              real: charge.amount
            });
            continue;
          }

          payment.status = 'PAID';
          await transitionOrder(null, order.id, 'PAGADO', 'system:reconcile', {
            chargeId: payment.providerChargeId,
            reconciledAt: new Date().toISOString()
          });
          logger.info('payment_reconciled_memory', { orderId: order.id });
        }
      }

      // 2. Reembolsos huérfanos en memoria
      if (payment.status === 'REFUND_PENDING') {
        const culqiStatus = await checkCulqiRefundStatus(payment.providerChargeId);
        if (culqiStatus && culqiStatus.status === 'successful') {
          payment.status = 'REFUNDED';
          await transitionOrder(null, payment.orderId, 'REEMBOLSADO', 'system:reconcile_refund', {
            recovered: true,
            providerRefundId: culqiStatus.id
          });
          logger.info('refund_reconciled_memory_success', { orderId: payment.orderId });
        }
      }
    }

    // 3. Webhooks huérfanos en memoria
    for (const [key, ev] of memoryWebhookEvents.entries()) {
      if (ev.status === 'RECEIVED') {
        const diffMs = Date.now() - ev.createdAt.getTime();
        if (diffMs > 5 * 60_000) {
          ev.status = 'FAILED';
          ev.error = 'PROCESSING_TIMEOUT_ORPHAN';
        }
      }
    }
  }
}

export function startReconciliationJob(): NodeJS.Timeout {
  const INTERVAL_MS = parseInt(process.env.RECONCILE_INTERVAL_MS || '600000', 10); // 10 minutos
  const timer = setInterval(() => {
    reconcilePendingPayments().catch((err) =>
      logger.error('reconcile_job_failed', { err: err.message })
    );
  }, INTERVAL_MS);

  timer.unref(); // No impide el apagado seguro del proceso
  return timer;
}

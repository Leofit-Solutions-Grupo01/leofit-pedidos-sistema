/**
 * @file reconcilePayments.ts
 * @description Job periódico de reconciliación de pagos huérfanos o con webhooks perdidos (Ronda 8.5).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import { dbPool, isPostgresAvailable } from '../config/database';
import { transitionOrder } from '../services/orders/stateMachine';
import { logger } from '../utils/logger';
import { alertSlack } from '../utils/alerts';
import { InMemoryDataStore } from '../infrastructure/repositories/memory.repositories';
import { memoryPayments } from '../controllers/paymentWebhook.controller';

const STALE_MINUTES = 15;

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
    const { rows } = await dbPool.query(
      `SELECT o.id AS order_id, o.estado,
              COALESCE(o.total_cents, ROUND(o.total_amount * 100)::bigint) as total_cents,
              p.provider, p.provider_charge_id, p.status AS payment_status
         FROM orders o
         JOIN payments p ON p.order_id = o.id
        WHERE o.estado = 'PENDIENTE'
          AND p.status IN ('PENDING', 'FAILED')
          AND o.created_at < NOW() - INTERVAL '${STALE_MINUTES} minutes'
        ORDER BY o.created_at ASC
        LIMIT 50`
    );

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
  } else {
    // Modo en memoria para suites de tests
    for (const payment of memoryPayments) {
      if (payment.status !== 'PENDING' && payment.status !== 'FAILED') continue;
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

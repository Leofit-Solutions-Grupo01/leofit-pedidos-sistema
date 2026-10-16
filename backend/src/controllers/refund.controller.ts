/**
 * @file refund.controller.ts
 * @description Controlador de reembolsos de pedidos (Admin-only) con Idempotencia en Culqi y protección de concurrencia.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import { Response, NextFunction } from 'express';
import { z } from 'zod';
import { dbPool, isPostgresAvailable } from '../config/database';
import { transitionOrder } from '../services/orders/stateMachine';
import { logger } from '../utils/logger';
import { alertSlack } from '../utils/alerts';
import { AuthenticatedRequest } from '../middlewares/auth.middleware';
import { InMemoryDataStore } from '../infrastructure/repositories/memory.repositories';
import { memoryPayments } from './paymentWebhook.controller';

export const RefundRequestSchema = z.object({
  amountCents: z.number().int().positive().optional(),
  reason: z.enum(['solicitud_cliente', 'producto_defectuoso', 'error_sistema', 'fraude']).default('solicitud_cliente')
});

export async function culqiRefund(
  chargeId: string,
  amountCents: number,
  reason: string,
  idempotencyKey?: string
): Promise<any> {
  const secret = process.env.CULQI_SECRET_KEY;

  if (secret && secret.startsWith('sk_')) {
    const headers: Record<string, string> = {
      Authorization: `Bearer ${secret}`,
      'Content-Type': 'application/json'
    };
    if (idempotencyKey) {
      headers['Idempotency-Key'] = idempotencyKey;
    }

    const res = await fetch('https://api.culqi.com/v2/refunds', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        charge_id: chargeId,
        amount: amountCents,
        reason
      })
    });

    const body = (await res.json()) as any;
    if (!res.ok) {
      throw Object.assign(new Error('REFUND_PROVIDER_ERROR'), {
        status: 409,
        provider: body
      });
    }
    return body;
  }

  // Fallback seguro de simulación para tests y desarrollo local
  if (chargeId === 'ch_fail_refund') {
    throw Object.assign(new Error('REFUND_PROVIDER_ERROR'), {
      status: 409,
      provider: { message: 'Culqi card refund rejected by issuing bank' }
    });
  }

  return {
    id: `ref_mock_${Date.now()}`,
    object: 'refund',
    charge_id: chargeId,
    amount: amountCents,
    status: 'successful',
    idempotency_key: idempotencyKey,
    created_at: Date.now()
  };
}

export async function checkCulqiRefundStatus(chargeId: string): Promise<any | null> {
  const secret = process.env.CULQI_SECRET_KEY;
  if (secret && secret.startsWith('sk_')) {
    const res = await fetch(`https://api.culqi.com/v2/charges/${chargeId}`, {
      headers: { Authorization: `Bearer ${secret}` }
    });
    if (!res.ok) return null;
    const body = (await res.json()) as any;
    return body.refunds && body.refunds.length > 0 ? body.refunds[0] : null;
  }

  if (chargeId.startsWith('ch_mock_reconcile_refunded')) {
    return { id: `ref_mock_${Date.now()}`, status: 'successful', amount: 50000 };
  }
  return null;
}

export async function refundOrder(req: AuthenticatedRequest, res: Response, next: NextFunction): Promise<void> {
  const orderId = Number(req.params.id);
  const parseResult = RefundRequestSchema.safeParse(req.body || {});
  if (!parseResult.success) {
    res.status(400).json({
      error: { code: 'INVALID_REFUND_PAYLOAD', message: parseResult.error.message }
    });
    return;
  }

  const { reason, amountCents } = parseResult.data;
  const adminId = req.user?.userId || req.user?.id || 1;

  if (isPostgresAvailable()) {
    const client = await dbPool.connect();
    try {
      await client.query('BEGIN');

      // 1. Lock pesimista sobre el pedido
      const { rows: [order] } = await client.query(
        `SELECT id, estado, total_cents, total_amount FROM orders WHERE id = $1 FOR UPDATE`,
        [orderId]
      );

      if (!order) {
        await client.query('ROLLBACK');
        res.status(404).json({ error: { code: 'ORDER_NOT_FOUND', message: 'Pedido no encontrado' } });
        return;
      }

      const estado = (order.estado || '').toUpperCase();
      if (!['PAGADO', 'ENTREGADO'].includes(estado)) {
        await client.query('ROLLBACK');
        res.status(409).json({
          error: { code: 'NOT_REFUNDABLE', estado, message: `El pedido está en estado ${estado} y no puede reembolsarse.` }
        });
        return;
      }

      // 2. Lock pesimista sobre el pago (evita carreras de dos administradores concurrentes)
      const { rows: [payment] } = await client.query(
        `SELECT id, provider, provider_charge_id, amount_cents, status, updated_at,
                COALESCE(refunded_amount_cents, 0) as refunded_amount_cents
           FROM payments
          WHERE order_id = $1 AND status IN ('PAID', 'REFUND_PENDING')
          ORDER BY created_at DESC LIMIT 1 FOR UPDATE`,
        [orderId]
      );

      if (!payment) {
        await client.query('ROLLBACK');
        res.status(409).json({
          error: { code: 'NO_PAID_PAYMENT', message: 'No existe un pago confirmado para este pedido.' }
        });
        return;
      }

      const paymentAmountCents = Number(payment.amount_cents);
      const targetAmountCents = amountCents || paymentAmountCents;

      if (targetAmountCents > paymentAmountCents) {
        await client.query('ROLLBACK');
        res.status(409).json({
          error: { code: 'AMOUNT_EXCEEDS_PAYMENT', message: `El monto a reembolsar (${targetAmountCents}) excede el total pagado (${paymentAmountCents}).` }
        });
        return;
      }

      // 3. Control de REFUND_PENDING existente
      if (payment.status === 'REFUND_PENDING') {
        const diffMs = Date.now() - new Date(payment.updated_at).getTime();
        if (diffMs < 2 * 60_000) {
          // Reembolso en ejecución por otra solicitud concurrente
          await client.query('ROLLBACK');
          res.status(409).json({
            error: { code: 'REFUND_IN_PROGRESS', message: 'Un reembolso para este pedido se encuentra en proceso de ejecución. Por favor espere.' }
          });
          return;
        }

        // Si es mayor a 2 min (huérfano tras caída), verificar primero en Culqi
        const existingCulqiRefund = await checkCulqiRefundStatus(payment.provider_charge_id);
        if (existingCulqiRefund) {
          await client.query(
            `UPDATE payments SET status = 'REFUNDED', raw_response = $1, updated_at = NOW() WHERE id = $2`,
            [JSON.stringify(existingCulqiRefund), payment.id]
          );
          await transitionOrder(client, orderId, 'REEMBOLSADO', `admin:${adminId}`, {
            reason,
            providerRefundId: existingCulqiRefund.id,
            reconciled: true
          });
          await client.query('COMMIT');
          res.status(200).json({ ok: true, refund: existingCulqiRefund, recovered: true });
          return;
        }
      }

      // 4. Clave de idempotencia única para el reembolso
      const idempotencyKey = `refund-${orderId}-${payment.id || payment.provider_charge_id}-${targetAmountCents}`;

      // Marcar intención antes de llamar al proveedor externo
      await client.query(
        `UPDATE payments
            SET status = 'REFUND_PENDING',
                refund_idempotency_key = $1,
                updated_at = NOW()
          WHERE id = $2`,
        [idempotencyKey, payment.id]
      );
      await client.query('COMMIT');

      // 5. Llamada externa FUERA de la transacción con Idempotency-Key
      let refundResult: any;
      try {
        if (payment.provider === 'culqi') {
          refundResult = await culqiRefund(payment.provider_charge_id, targetAmountCents, reason, idempotencyKey);
        } else {
          throw Object.assign(new Error('PROVIDER_NOT_SUPPORTED'), { status: 500 });
        }
      } catch (err: any) {
        // Revertir a PAID en caso de rechazo del proveedor
        await dbPool.query(
          `UPDATE payments SET status = 'PAID', updated_at = NOW() WHERE id = $1`,
          [payment.id]
        );
        await alertSlack('❌ Reembolso rechazado por proveedor', {
          orderId,
          provider: payment.provider,
          error: err.message
        });
        res.status(err.status ?? 500).json({
          error: { code: err.message, provider: err.provider }
        });
        return;
      }

      // 6. Confirmar: actualizar pago a REFUNDED y transicionar orden a REEMBOLSADO
      const c2 = await dbPool.connect();
      try {
        await c2.query('BEGIN');
        await c2.query(
          `UPDATE payments
              SET status = 'REFUNDED',
                  refunded_amount_cents = $1,
                  raw_response = $2,
                  updated_at = NOW()
            WHERE id = $3`,
          [targetAmountCents, JSON.stringify(refundResult), payment.id]
        );

        await transitionOrder(c2, orderId, 'REEMBOLSADO', `admin:${adminId}`, {
          reason,
          amountCents: targetAmountCents,
          isPartial: targetAmountCents < paymentAmountCents,
          providerRefundId: refundResult?.id
        });
        await c2.query('COMMIT');
      } catch (err: any) {
        await c2.query('ROLLBACK');
        logger.error('refund_finalize_failed', { orderId, err: err.message });
        await alertSlack('🚨 Reembolso aceptado por proveedor pero falló al confirmar en DB', {
          orderId,
          providerRefundId: refundResult?.id
        });
        res.status(500).json({ error: { code: 'REFUND_FINALIZE_FAILED' } });
        return;
      } finally {
        c2.release();
      }

      logger.audit('refund_completed', {
        orderId,
        adminId,
        amountCents: targetAmountCents
      });

      res.status(200).json({ ok: true, refund: refundResult });
    } catch (err) {
      await client.query('ROLLBACK').catch(() => {});
      next(err);
    } finally {
      client.release();
    }
  } else {
    // ─── Modo en memoria para suites de tests y desarrollo local ───
    const order = InMemoryDataStore.orders.find((o) => o.id === orderId);
    if (!order) {
      res.status(404).json({ error: { code: 'ORDER_NOT_FOUND', message: 'Pedido no encontrado' } });
      return;
    }

    const estado = ((order as any).estado || order.status || '').toUpperCase();
    if (!['PAGADO', 'ENTREGADO'].includes(estado)) {
      res.status(409).json({
        error: { code: 'NOT_REFUNDABLE', estado, message: `El pedido está en estado ${estado} y no puede reembolsarse.` }
      });
      return;
    }

    const payment = memoryPayments.find((p) => p.orderId === orderId && ['PAID', 'REFUND_PENDING'].includes(p.status));
    if (!payment) {
      res.status(409).json({
        error: { code: 'NO_PAID_PAYMENT', message: 'No existe un pago confirmado para este pedido.' }
      });
      return;
    }

    if (payment.status === 'REFUND_PENDING') {
      res.status(409).json({
        error: { code: 'REFUND_IN_PROGRESS', message: 'Un reembolso para este pedido se encuentra en proceso de ejecución.' }
      });
      return;
    }

    const targetAmountCents = amountCents || payment.amountCents;
    if (targetAmountCents > payment.amountCents) {
      res.status(409).json({
        error: { code: 'AMOUNT_EXCEEDS_PAYMENT', message: 'El monto a reembolsar excede el total pagado.' }
      });
      return;
    }

    payment.status = 'REFUND_PENDING';
    payment.updatedAt = new Date();

    const idempotencyKey = `refund-${orderId}-${payment.providerChargeId}-${targetAmountCents}`;
    let refundResult: any;
    try {
      refundResult = await culqiRefund(payment.providerChargeId, targetAmountCents, reason, idempotencyKey);
    } catch (err: any) {
      payment.status = 'PAID';
      res.status(err.status ?? 500).json({
        error: { code: err.message, provider: err.provider }
      });
      return;
    }

    payment.status = 'REFUNDED';
    await transitionOrder(null, orderId, 'REEMBOLSADO', `admin:${adminId}`, {
      reason,
      amountCents: targetAmountCents,
      isPartial: targetAmountCents < payment.amountCents,
      providerRefundId: refundResult?.id
    });

    res.status(200).json({ ok: true, refund: refundResult });
  }
}

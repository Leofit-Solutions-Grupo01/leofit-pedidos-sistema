/**
 * @file refund.controller.ts
 * @description Controlador de reembolsos de pedidos (Admin-only) con pasarela Culqi y máquina de estados.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import { Response, NextFunction } from 'express';
import { dbPool, isPostgresAvailable } from '../config/database';
import { transitionOrder } from '../services/orders/stateMachine';
import { logger } from '../utils/logger';
import { alertSlack } from '../utils/alerts';
import { AuthenticatedRequest } from '../middlewares/auth.middleware';
import { InMemoryDataStore } from '../infrastructure/repositories/memory.repositories';
import { memoryPayments } from './paymentWebhook.controller';

export async function culqiRefund(chargeId: string, amountCents: number, reason: string): Promise<any> {
  const secret = process.env.CULQI_SECRET_KEY;

  if (secret && secret.startsWith('sk_')) {
    const res = await fetch('https://api.culqi.com/v2/refunds', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${secret}`,
        'Content-Type': 'application/json'
      },
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

  // Fallback seguro de simulación para entornos de test y desarrollo local
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
    created_at: Date.now()
  };
}

export async function refundOrder(req: AuthenticatedRequest, res: Response, next: NextFunction): Promise<void> {
  const orderId = Number(req.params.id);
  const { reason = 'solicitud_cliente' } = req.body || {};
  const adminId = req.user?.userId || req.user?.id || 1;

  if (isPostgresAvailable()) {
    const client = await dbPool.connect();
    try {
      await client.query('BEGIN');

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

      const { rows: [payment] } = await client.query(
        `SELECT provider, provider_charge_id, amount_cents
           FROM payments
          WHERE order_id = $1 AND status = 'PAID'
          ORDER BY created_at DESC LIMIT 1`,
        [orderId]
      );

      if (!payment) {
        await client.query('ROLLBACK');
        res.status(409).json({
          error: { code: 'NO_PAID_PAYMENT', message: 'No existe un pago confirmado para este pedido.' }
        });
        return;
      }

      // Marcar intención antes de llamar al proveedor externo (evita carreras concurrentes)
      await client.query(
        `UPDATE payments SET status = 'REFUND_PENDING'
          WHERE provider = $1 AND provider_charge_id = $2`,
        [payment.provider, payment.provider_charge_id]
      );
      await client.query('COMMIT');

      // Llamada externa FUERA de la transacción para no bloquear la fila
      let refundResult: any;
      try {
        if (payment.provider === 'culqi') {
          refundResult = await culqiRefund(payment.provider_charge_id, payment.amount_cents, reason);
        } else {
          throw Object.assign(new Error('PROVIDER_NOT_SUPPORTED'), { status: 500 });
        }
      } catch (err: any) {
        // Revertir el estado a PAID en caso de rechazo del proveedor
        await dbPool.query(
          `UPDATE payments SET status = 'PAID'
            WHERE provider = $1 AND provider_charge_id = $2`,
          [payment.provider, payment.provider_charge_id]
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

      // Confirmar: transición a REEMBOLSADO y pago marcado como REFUNDED
      const c2 = await dbPool.connect();
      try {
        await c2.query('BEGIN');
        await c2.query(
          `UPDATE payments SET status = 'REFUNDED', raw_response = $1, updated_at = NOW()
            WHERE provider = $2 AND provider_charge_id = $3`,
          [JSON.stringify(refundResult), payment.provider, payment.provider_charge_id]
        );
        await transitionOrder(c2, orderId, 'REEMBOLSADO', `admin:${adminId}`, {
          reason,
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
        amountCents: payment.amount_cents
      });

      res.status(200).json({ ok: true, refund: refundResult });
    } catch (err) {
      await client.query('ROLLBACK').catch(() => {});
      next(err);
    } finally {
      client.release();
    }
  } else {
    // ─── Modo en memoria para tests y desarrollo local ───
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

    const payment = memoryPayments.find((p) => p.orderId === orderId && p.status === 'PAID');
    if (!payment) {
      res.status(409).json({
        error: { code: 'NO_PAID_PAYMENT', message: 'No existe un pago confirmado para este pedido.' }
      });
      return;
    }

    payment.status = 'REFUND_PENDING';

    let refundResult: any;
    try {
      refundResult = await culqiRefund(payment.providerChargeId, payment.amountCents, reason);
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
      providerRefundId: refundResult?.id
    });

    res.status(200).json({ ok: true, refund: refundResult });
  }
}

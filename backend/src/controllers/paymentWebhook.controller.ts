/**
 * @file paymentWebhook.controller.ts
 * @description Controlador de Webhooks de Pasarelas de Pago con Hardening Crítico (Ronda 8.5).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * 
 * Controles de Resiliencia y Seguridad:
 * 1. Validación estricta de monto (event.amountCents === order.total_cents) y divisa (PEN).
 * 2. Persistencia de webhook_events aislada fuera de la transacción de negocio (evita loop infinito).
 * 3. Manejo de pedidos terminales (CANCELADO, REEMBOLSADO) -> HTTP 200 IGNORED + PAID_ORPHAN + alerta.
 * 4. Verificación anti-replay con timestamp header de Culqi/Niubiz (ventana de 5 minutos).
 * 5. Notificación post-pago asíncrona a operaciones y clientes.
 */

import crypto from 'node:crypto';
import { Request, Response } from 'express';
import { dbPool, isPostgresAvailable } from '../config/database';
import { logger } from '../utils/logger';
import { transitionOrder } from '../services/orders/stateMachine';
import { alertSlack } from '../utils/alerts';
import { InMemoryDataStore } from '../infrastructure/repositories/memory.repositories';

export type Provider = 'culqi' | 'niubiz' | 'mercadopago';

export interface NormalizedEvent {
  provider: Provider;
  eventId: string;
  chargeId: string;
  orderId: number;
  amountCents: number;
  currency: string;
  status: 'PAID' | 'FAILED' | 'REFUNDED';
  timestampMs?: number;
  raw: any;
}

// Almacenes en memoria para tests y entorno local sin PostgreSQL
const memoryWebhookEvents = new Map<string, { status: string; attempts: number; error?: string }>();
export const memoryPayments: Array<{
  orderId: number;
  provider: Provider;
  providerChargeId: string;
  amountCents: number;
  currency: string;
  status: string;
  rawResponse: any;
}> = [];

const MAX_SIGNATURE_AGE_MS = 5 * 60_000; // Ventana anti-replay de 5 minutos

export function verifySignature(
  provider: Provider,
  rawBody: Buffer,
  headers: Record<string, any>
): void {
  const envVar = `${provider.toUpperCase()}_WEBHOOK_SECRET`;
  const secret = process.env[envVar] || process.env.PAYMENT_WEBHOOK_SECRET || process.env.WEBHOOK_SECRET;

  if (!secret) {
    throw new Error(`MISSING_SECRET_${provider}`);
  }

  const signature =
    headers['x-signature'] ||
    headers['x-culqi-signature'] ||
    headers['x-niubiz-signature'] ||
    '';

  const timestamp =
    headers['x-culqi-timestamp'] ||
    headers['x-timestamp'] ||
    headers['x-niubiz-timestamp'];

  // Anti-replay: rechazar si el timestamp está fuera de la ventana de 5 minutos
  if (timestamp) {
    const tsMs = Number(timestamp) * (String(timestamp).length <= 10 ? 1000 : 1);
    if (!Number.isFinite(tsMs) || Math.abs(Date.now() - tsMs) > MAX_SIGNATURE_AGE_MS) {
      throw Object.assign(new Error('SIGNATURE_EXPIRED'), { status: 401 });
    }
  }

  // Culqi y proveedores modernos firman `timestamp.body`; si no hay timestamp, solo body
  const signedPayload = timestamp
    ? Buffer.concat([Buffer.from(`${timestamp}.`), rawBody])
    : rawBody;

  const expected = crypto
    .createHmac('sha256', secret)
    .update(signedPayload)
    .digest('hex');

  const a = Buffer.from(String(signature), 'hex');
  const b = Buffer.from(expected, 'hex');

  if (a.length === 0 || a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
    throw Object.assign(new Error('INVALID_SIGNATURE'), { status: 401 });
  }
}

export function normalize(provider: Provider, body: any): NormalizedEvent {
  if (provider === 'culqi') {
    return {
      provider,
      eventId: body.id || `evt_${Date.now()}`,
      chargeId: body.data?.id || body.id,
      orderId: Number(body.data?.metadata?.order_id || body.metadata?.order_id),
      amountCents: Number(body.data?.amount || body.amount || 0),
      currency: body.data?.currency_code || body.currency_code || 'PEN',
      status:
        body.type === 'charge.succeeded'
          ? 'PAID'
          : body.type === 'charge.refunded'
          ? 'REFUNDED'
          : 'FAILED',
      raw: body
    };
  }

  if (provider === 'niubiz') {
    return {
      provider,
      eventId: String(body.transactionId || body.id),
      chargeId: String(body.transactionId || body.id),
      orderId: Number(body.orderId || body.metadata?.order_id),
      amountCents: Math.round(Number(body.amount || 0) * 100),
      currency: 'PEN',
      status:
        body.status === 'Authorized'
          ? 'PAID'
          : body.status === 'Refunded'
          ? 'REFUNDED'
          : 'FAILED',
      raw: body
    };
  }

  throw Object.assign(new Error(`UNSUPPORTED_PROVIDER_${provider}`), { status: 400 });
}

// ─── Paso 1: Registrar el evento (transacción aislada, commit inmediato) ───
async function registerEvent(provider: Provider, eventId: string, payload: any): Promise<number | null> {
  if (!isPostgresAvailable()) {
    const key = `${provider}:${eventId}`;
    if (memoryWebhookEvents.has(key)) {
      return null; // Duplicado
    }
    memoryWebhookEvents.set(key, { status: 'RECEIVED', attempts: 1 });
    return 1;
  }

  const { rows } = await dbPool.query(
    `INSERT INTO webhook_events (provider, event_id, payload, status)
     VALUES ($1, $2, $3, 'RECEIVED')
     ON CONFLICT (provider, event_id) DO NOTHING
     RETURNING id`,
    [provider, eventId, JSON.stringify(payload)]
  );
  return rows[0]?.id ?? null; // null = duplicado
}

async function markEvent(
  eventId: string,
  provider: Provider,
  status: 'PROCESSED' | 'IGNORED' | 'FAILED',
  errorMessage?: string
): Promise<void> {
  if (!isPostgresAvailable()) {
    const key = `${provider}:${eventId}`;
    const cur = memoryWebhookEvents.get(key) || { attempts: 0, status };
    memoryWebhookEvents.set(key, {
      status,
      attempts: cur.attempts + 1,
      error: errorMessage
    });
    return;
  }

  await dbPool.query(
    `UPDATE webhook_events
        SET status = $1,
            processed_at = NOW(),
            attempts = attempts + 1,
            error_message = $2
      WHERE provider = $3 AND event_id = $4`,
    [status, errorMessage ?? null, provider, eventId]
  ).catch((err: any) => logger.error('mark_event_failed', { err: err.message }));
}

// ─── Notificación post-pago (fuera de la transacción de negocio) ───
export async function notifyOrderPaid(orderId: number): Promise<void> {
  try {
    let order: any = null;
    if (isPostgresAvailable()) {
      const { rows } = await dbPool.query(
        `SELECT o.id, o.cliente_email, o.cliente_nombre,
                COALESCE(o.total_cents, ROUND(o.total_amount * 100)::bigint) as total_cents
           FROM orders o WHERE o.id = $1`,
        [orderId]
      );
      order = rows[0];
    } else {
      order = InMemoryDataStore.orders.find((o) => o.id === orderId);
    }

    if (!order) return;

    const totalCents = Number(order.total_cents ?? Math.round(Number(order.total_amount || 0) * 100));
    const cliente = order.cliente_nombre || order.client?.name || 'Cliente';

    // Notificación a operaciones en Slack
    await alertSlack('✅ Nuevo pedido PAGADO', {
      orderId: order.id,
      cliente,
      totalSoles: (totalCents / 100).toFixed(2)
    });
  } catch (err: any) {
    logger.error('notify_order_paid_failed', { orderId, error: err.message });
  }
}

export async function handleWebhook(req: Request, res: Response): Promise<void> {
  const provider = (req.params.provider || '').toLowerCase() as Provider;
  const rawBody = (req as any).rawBody || Buffer.from(JSON.stringify(req.body || {}));

  // 1) Verificar firma y anti-replay
  try {
    verifySignature(provider, rawBody, req.headers);
  } catch (err: any) {
    logger.audit('webhook_signature_invalid', {
      provider,
      ip: req.ip,
      reason: err.message
    });
    const statusCode = err.status || 401;
    res.status(statusCode).json({ error: { code: err.message || 'INVALID_SIGNATURE' } });
    return;
  }

  // 2) Normalizar payload
  let event: NormalizedEvent;
  try {
    event = normalize(provider, req.body);
  } catch (err: any) {
    const statusCode = err.status || 400;
    res.status(statusCode).json({ error: { code: 'INVALID_PAYLOAD', message: err.message } });
    return;
  }

  if (!Number.isFinite(event.orderId) || event.orderId <= 0) {
    res.status(400).json({ error: { code: 'MISSING_ORDER_ID' } });
    return;
  }

  // 3) Registrar evento en transacción aislada (sobrevive al rollback de negocio)
  const webhookRowId = await registerEvent(provider, event.eventId, event.raw);
  if (!webhookRowId) {
    logger.info('webhook_duplicated', { provider, eventId: event.eventId });
    res.status(200).json({ ok: true, deduped: true });
    return;
  }

  // 4) Procesar la lógica de negocio
  if (isPostgresAvailable()) {
    const client = await dbPool.connect();
    try {
      await client.query('BEGIN');

      const { rows: [order] } = await client.query(
        `SELECT id, estado,
                COALESCE(total_cents, ROUND(total_amount * 100)::bigint) as total_cents,
                COALESCE(currency, 'PEN') as currency
           FROM orders WHERE id = $1 FOR UPDATE`,
        [event.orderId]
      );

      if (!order) {
        await client.query('ROLLBACK');
        await markEvent(event.eventId, provider, 'FAILED', 'ORDER_NOT_FOUND');
        res.status(404).json({ error: { code: 'ORDER_NOT_FOUND' } });
        return;
      }

      const orderTotalCents = Number(order.total_cents);
      const orderCurrency = String(order.currency).trim().toUpperCase();

      // 4a) Validación estricta de monto y moneda (CRÍTICO - P0)
      if (event.status === 'PAID' || event.status === 'REFUNDED') {
        if (orderTotalCents !== event.amountCents) {
          await client.query('ROLLBACK');
          await markEvent(event.eventId, provider, 'FAILED', 'AMOUNT_MISMATCH');
          await alertSlack('🚨 Monto de pago NO coincide con el pedido', {
            orderId: order.id,
            esperadoCents: orderTotalCents,
            recibidoCents: event.amountCents,
            provider,
            eventId: event.eventId
          });
          res.status(409).json({ error: { code: 'AMOUNT_MISMATCH' } });
          return;
        }

        if (orderCurrency !== event.currency.toUpperCase()) {
          await client.query('ROLLBACK');
          await markEvent(event.eventId, provider, 'FAILED', 'CURRENCY_MISMATCH');
          await alertSlack('🚨 Moneda de pago NO coincide', {
            orderId: order.id,
            esperada: orderCurrency,
            recibida: event.currency
          });
          res.status(409).json({ error: { code: 'CURRENCY_MISMATCH' } });
          return;
        }
      }

      // 4b) Upsert del pago (idempotente por provider_charge_id)
      await client.query(
        `INSERT INTO payments
           (order_id, provider, provider_charge_id, amount_cents, currency, status, raw_response)
         VALUES ($1, $2, $3, $4, $5, $6, $7)
         ON CONFLICT (provider, provider_charge_id)
         DO UPDATE SET status = EXCLUDED.status,
                       raw_response = EXCLUDED.raw_response,
                       updated_at = NOW()`,
        [
          event.orderId,
          event.provider,
          event.chargeId,
          event.amountCents,
          event.currency,
          event.status,
          JSON.stringify(event.raw)
        ]
      );

      // 4c) Transición según el resultado y gestión de estados terminales
      const TERMINAL_STATES = ['CANCELADO', 'REEMBOLSADO'];
      const currentEstado = (order.estado || '').toUpperCase();

      if (event.status === 'PAID') {
        if (TERMINAL_STATES.includes(currentEstado)) {
          // Pedido cancelado/reembolsado pero llegó un pago -> PAID_ORPHAN
          await client.query(
            `UPDATE payments SET status = 'PAID_ORPHAN'
              WHERE provider = $1 AND provider_charge_id = $2`,
            [event.provider, event.chargeId]
          );
          await client.query('COMMIT');
          await markEvent(event.eventId, provider, 'IGNORED', 'ORDER_IN_TERMINAL_STATE');
          await alertSlack('💸 Pago recibido sobre pedido cancelado — REEMBOLSAR', {
            orderId: order.id,
            estado: order.estado,
            chargeId: event.chargeId,
            amountCents: event.amountCents
          });
          // 200 IGNORED: evitar loop infinito de reintentos
          res.status(200).json({ ok: true, ignored: true, reason: 'ORDER_TERMINAL' });
          return;
        }

        await transitionOrder(client, event.orderId, 'PAGADO', `webhook:${provider}`, {
          chargeId: event.chargeId,
          amountCents: event.amountCents
        });
      } else if (event.status === 'REFUNDED') {
        await transitionOrder(client, event.orderId, 'REEMBOLSADO', `webhook:${provider}`, {
          chargeId: event.chargeId
        });
      }

      await client.query('COMMIT');
      await markEvent(event.eventId, provider, 'PROCESSED');

      logger.info('webhook_processed', {
        provider,
        eventId: event.eventId,
        orderId: event.orderId,
        status: event.status
      });

      if (event.status === 'PAID') {
        notifyOrderPaid(event.orderId).catch((err) =>
          logger.error('notify_order_paid_failed', { err: err.message })
        );
      }

      res.status(200).json({ ok: true });
    } catch (err: any) {
      await client.query('ROLLBACK').catch(() => {});

      if (err.code === 'INVALID_TRANSITION') {
        await markEvent(event.eventId, provider, 'FAILED', err.message);
        logger.warn('webhook_invalid_transition', {
          orderId: event.orderId,
          from: err.from,
          to: err.to
        });
        res.status(409).json({ error: { code: 'INVALID_TRANSITION' } });
        return;
      }

      await markEvent(event.eventId, provider, 'FAILED', err.message);
      logger.error('webhook_failed', {
        provider,
        eventId: event.eventId,
        err: err.message
      });
      await alertSlack('Webhook de pago falló (transitorio)', {
        provider,
        eventId: event.eventId,
        err: err.message
      });

      res.status(500).json({ error: { code: 'WEBHOOK_PROCESSING_FAILED' } });
    } finally {
      client.release();
    }
  } else {
    // ─── Modo en memoria (suites de tests unitarios y desarrollo local) ───
    const order = InMemoryDataStore.orders.find((o) => o.id === event.orderId);
    if (!order) {
      await markEvent(event.eventId, provider, 'FAILED', 'ORDER_NOT_FOUND');
      res.status(404).json({ error: { code: 'ORDER_NOT_FOUND' } });
      return;
    }

    const orderTotalCents = (order as any).total_cents ?? Math.round(Number(order.total_amount) * 100);
    const orderCurrency = ((order as any).currency || 'PEN').toUpperCase();

    // Validación estricta de monto y moneda en memoria
    if (event.status === 'PAID' || event.status === 'REFUNDED') {
      if (orderTotalCents !== event.amountCents) {
        await markEvent(event.eventId, provider, 'FAILED', 'AMOUNT_MISMATCH');
        await alertSlack('🚨 Monto de pago NO coincide con el pedido', {
          orderId: order.id,
          esperadoCents: orderTotalCents,
          recibidoCents: event.amountCents
        });
        res.status(409).json({ error: { code: 'AMOUNT_MISMATCH' } });
        return;
      }

      if (orderCurrency !== event.currency.toUpperCase()) {
        await markEvent(event.eventId, provider, 'FAILED', 'CURRENCY_MISMATCH');
        res.status(409).json({ error: { code: 'CURRENCY_MISMATCH' } });
        return;
      }
    }

    // Upsert en pagos en memoria
    const existingPaymentIdx = memoryPayments.findIndex(
      (p) => p.provider === provider && p.providerChargeId === event.chargeId
    );
    const paymentRecord: {
      orderId: number;
      provider: Provider;
      providerChargeId: string;
      amountCents: number;
      currency: string;
      status: string;
      rawResponse: any;
    } = {
      orderId: event.orderId,
      provider,
      providerChargeId: event.chargeId,
      amountCents: event.amountCents,
      currency: event.currency,
      status: event.status,
      rawResponse: event.raw
    };
    if (existingPaymentIdx >= 0) {
      memoryPayments[existingPaymentIdx] = paymentRecord;
    } else {
      memoryPayments.push(paymentRecord);
    }

    // Estados terminales en memoria
    const currentEstado = ((order as any).estado || order.status || '').toUpperCase();
    const TERMINAL_STATES = ['CANCELADO', 'REEMBOLSADO'];

    if (event.status === 'PAID') {
      if (TERMINAL_STATES.includes(currentEstado)) {
        paymentRecord.status = 'PAID_ORPHAN';
        await markEvent(event.eventId, provider, 'IGNORED', 'ORDER_IN_TERMINAL_STATE');
        await alertSlack('💸 Pago recibido sobre pedido cancelado — REEMBOLSAR', {
          orderId: order.id,
          chargeId: event.chargeId
        });
        res.status(200).json({ ok: true, ignored: true, reason: 'ORDER_TERMINAL' });
        return;
      }

      await transitionOrder(null, event.orderId, 'PAGADO', `webhook:${provider}`, {
        chargeId: event.chargeId,
        amountCents: event.amountCents
      });
    } else if (event.status === 'REFUNDED') {
      await transitionOrder(null, event.orderId, 'REEMBOLSADO', `webhook:${provider}`, {
        chargeId: event.chargeId
      });
    }

    await markEvent(event.eventId, provider, 'PROCESSED');

    if (event.status === 'PAID') {
      notifyOrderPaid(event.orderId).catch(() => {});
    }

    res.status(200).json({ ok: true });
  }
}

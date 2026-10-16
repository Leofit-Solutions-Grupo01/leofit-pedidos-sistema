/**
 * @file paymentWebhook.controller.ts
 * @description Controlador genérico para webhooks de pasarelas de pago (Culqi, Niubiz, Mercado Pago).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import crypto from 'node:crypto';
import { Request, Response } from 'express';
import { dbPool, isPostgresAvailable } from '../config/database';
import { logger } from '../utils/logger';
import { transitionOrder } from '../services/orders/stateMachine';
import { alertSlack } from '../utils/alerts';

type Provider = 'culqi' | 'niubiz' | 'mercadopago';

interface NormalizedEvent {
  provider: Provider;
  eventId: string;
  chargeId: string;
  orderId: number;
  amountCents: number;
  currency: string;
  status: 'PAID' | 'FAILED' | 'REFUNDED';
  raw: any;
}

// Registro en memoria de eventos para suites de tests o sin Postgres
const memoryWebhookEvents = new Set<string>();

export function verifySignature(provider: Provider, rawBody: Buffer, headers: Record<string, any>): void {
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

  const expected = crypto
    .createHmac('sha256', secret)
    .update(rawBody)
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

  throw new Error(`UNSUPPORTED_PROVIDER_${provider}`);
}

export async function handleWebhook(req: Request, res: Response): Promise<void> {
  const provider = (req.params.provider || '').toLowerCase() as Provider;

  const rawBody = (req as any).rawBody || Buffer.from(JSON.stringify(req.body || {}));

  try {
    verifySignature(provider, rawBody, req.headers);
  } catch (err: any) {
    logger.audit('webhook_signature_invalid', { provider, ip: req.ip, error: err.message });
    res.status(401).json({ error: { code: 'INVALID_SIGNATURE' } });
    return;
  }

  let event: NormalizedEvent;
  try {
    event = normalize(provider, req.body);
  } catch (err: any) {
    res.status(400).json({ error: { code: 'INVALID_PAYLOAD', message: err.message } });
    return;
  }

  if (!event.orderId || isNaN(event.orderId)) {
    res.status(400).json({ error: { code: 'MISSING_ORDER_ID' } });
    return;
  }

  if (isPostgresAvailable()) {
    const client = await dbPool.connect();
    try {
      await client.query('BEGIN');

      // 1) Deduplicación atómica por (provider, event_id)
      const ins = await client.query(
        `INSERT INTO webhook_events (provider, event_id, payload)
         VALUES ($1, $2, $3)
         ON CONFLICT (provider, event_id) DO NOTHING
         RETURNING id`,
        [provider, event.eventId, JSON.stringify(event.raw)]
      );

      if (ins.rowCount === 0) {
        await client.query('COMMIT');
        logger.info('webhook_duplicated', { provider, eventId: event.eventId });
        res.status(200).json({ ok: true, deduped: true });
        return;
      }

      // 2) Upsert del pago (idempotente por provider_charge_id)
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

      // 3) Transición formal del pedido según el resultado del pago
      if (event.status === 'PAID') {
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

      logger.info('webhook_processed', {
        provider,
        eventId: event.eventId,
        orderId: event.orderId,
        status: event.status
      });

      res.status(200).json({ ok: true });
    } catch (err: any) {
      await client.query('ROLLBACK').catch(() => {});
      logger.error('webhook_failed', {
        provider,
        eventId: event?.eventId,
        err: err.message
      });

      await alertSlack('Webhook de pago falló', {
        provider,
        eventId: event?.eventId,
        err: err.message
      }).catch(() => {});

      // 500 hace que el proveedor reintente la entrega del webhook
      res.status(500).json({ error: { code: 'WEBHOOK_PROCESSING_FAILED' } });
    } finally {
      client.release();
    }
  } else {
    // Almacén en memoria (para pruebas unitarias y desarrollo sin Postgres)
    const eventKey = `${provider}:${event.eventId}`;
    if (memoryWebhookEvents.has(eventKey)) {
      res.status(200).json({ ok: true, deduped: true });
      return;
    }
    memoryWebhookEvents.add(eventKey);

    try {
      if (event.status === 'PAID') {
        await transitionOrder(null, event.orderId, 'PAGADO', `webhook:${provider}`, {
          chargeId: event.chargeId,
          amountCents: event.amountCents
        });
      } else if (event.status === 'REFUNDED') {
        await transitionOrder(null, event.orderId, 'REEMBOLSADO', `webhook:${provider}`, {
          chargeId: event.chargeId
        });
      }

      res.status(200).json({ ok: true });
    } catch (err: any) {
      res.status(500).json({ error: { code: 'WEBHOOK_PROCESSING_FAILED', message: err.message } });
    }
  }
}

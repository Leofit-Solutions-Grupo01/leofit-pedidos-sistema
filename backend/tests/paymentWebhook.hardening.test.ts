/**
 * @file paymentWebhook.hardening.test.ts
 * @description Suite completa de pruebas de hardening de pagos, snapshots, idempotencia y reconciliación (Ronda 8.5+).
 */

import crypto from 'node:crypto';
import request from 'supertest';
import { createApp } from '../src/app';
import { JWTService } from '../src/infrastructure/security/jwt.utils';
import { reconcilePendingPayments } from '../src/jobs/reconcilePayments';
import {
  memoryPayments,
  memoryWebhookEvents,
  sentOrderEmails
} from '../src/controllers/paymentWebhook.controller';
import { InMemoryDataStore } from '../src/infrastructure/repositories/memory.repositories';

const SECRET = 'test_culqi_hardening_secret_98765';
process.env.CULQI_WEBHOOK_SECRET = SECRET;

function sign(payload: any, opts: { timestamp?: number; badSig?: string } = {}) {
  const rawString = JSON.stringify(payload);
  const raw = Buffer.from(rawString, 'utf8');
  const ts = opts.timestamp ?? Math.floor(Date.now() / 1000);
  const signedPayload = Buffer.concat([Buffer.from(`${ts}.`), raw]);
  const sig = opts.badSig !== undefined
    ? opts.badSig
    : crypto.createHmac('sha256', SECRET).update(signedPayload).digest('hex');
  return { rawString, sig, ts };
}

describe('Ronda 8.5 — Hardening Crítico de Pagos y Máquina de Estados', () => {
  const app = createApp();
  let adminToken: string;
  let orderId: number;
  const orderTotalCents = 6000; // S/ 50 (item) + S/ 10 (envío) = S/ 60.00 -> 6000 céntimos

  beforeAll(async () => {
    adminToken = JWTService.generateToken({
      userId: 1,
      email: 'admin@leofit.pe',
      name: 'Admin Hardening',
      role: 'ADMIN'
    });

    // 1. Crear un pedido PENDIENTE vía API
    const orderRes = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        clientId: 1,
        paymentMethod: 'CULQI',
        shippingCost: 10,
        items: [{ variantId: 1, quantity: 1, unitPrice: 50 }]
      });

    expect([200, 201]).toContain(orderRes.status);
    orderId = orderRes.body.data.id;
  });

  it('1. Firma con caracteres no-hex o longitud inválida -> 401 INVALID_SIGNATURE (nunca 500 DoS)', async () => {
    const payload = { test: true };
    const { rawString, ts } = sign(payload);

    // Envío de caracteres 'zzzz' que no son hex
    const r1 = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    expect(r1.status).toBe(401);
    expect(r1.body.error.code).toBe('INVALID_SIGNATURE');

    // Envío de firma hex truncada (menos de 64 caracteres)
    const r2 = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', 'deadbeef')
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    expect(r2.status).toBe(401);
    expect(r2.body.error.code).toBe('INVALID_SIGNATURE');
  });

  it('2. Webhook con amount distinto al total -> 409 AMOUNT_MISMATCH y NO transiciona', async () => {
    const payload = {
      id: `evt_mismatch_${Date.now()}`,
      type: 'charge.succeeded',
      data: {
        id: `ch_mismatch_${Date.now()}`,
        amount: orderTotalCents - 1000, // S/ 50 en vez de S/ 60
        currency_code: 'PEN',
        metadata: { order_id: String(orderId) }
      }
    };

    const { rawString, sig, ts } = sign(payload);
    const r = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    expect(r.status).toBe(409);
    expect(r.body.error.code).toBe('AMOUNT_MISMATCH');

    // Comprobar que el pedido sigue en PENDIENTE
    const checkRes = await request(app)
      .get(`/api/orders/${orderId}`)
      .set('Authorization', `Bearer ${adminToken}`);
    let estado = ((checkRes.body.data as any).estado || checkRes.body.data.status).toUpperCase();
    if (estado === 'RECIBIDO') estado = 'PENDIENTE';
    expect(estado).toBe('PENDIENTE');
  });

  it('3. Webhook con currency distinta -> 409 CURRENCY_MISMATCH', async () => {
    const payload = {
      id: `evt_currency_${Date.now()}`,
      type: 'charge.succeeded',
      data: {
        id: `ch_curr_${Date.now()}`,
        amount: orderTotalCents,
        currency_code: 'USD', // Diferente de PEN
        metadata: { order_id: String(orderId) }
      }
    };

    const { rawString, sig, ts } = sign(payload);
    const r = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    expect(r.status).toBe(409);
    expect(r.body.error.code).toBe('CURRENCY_MISMATCH');
  });

  it('4. Replay con timestamp viejo (>5min) -> 401 SIGNATURE_EXPIRED', async () => {
    const payload = {
      id: `evt_old_${Date.now()}`,
      type: 'charge.succeeded',
      data: { id: `ch_old_${Date.now()}`, amount: orderTotalCents, metadata: { order_id: String(orderId) } }
    };

    // 10 minutos en el pasado
    const expiredTs = Math.floor(Date.now() / 1000) - 600;
    const { rawString, sig, ts } = sign(payload, { timestamp: expiredTs });

    const r = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    expect(r.status).toBe(401);
    expect(r.body.error.code).toBe('SIGNATURE_EXPIRED');
  });

  it('5. Webhook con monto correcto y firma válida -> 200 y transiciona a PAGADO + envía email exactamente 1 vez', async () => {
    const okEventId = `evt_ok_${Date.now()}`;
    const payload = {
      id: okEventId,
      type: 'charge.succeeded',
      data: {
        id: `ch_ok_${Date.now()}`,
        amount: orderTotalCents,
        currency_code: 'PEN',
        metadata: { order_id: String(orderId) }
      }
    };

    const initialEmailsCount = sentOrderEmails.filter(e => e.orderId === orderId).length;

    const { rawString, sig, ts } = sign(payload);
    const r = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    expect(r.status).toBe(200);
    expect(r.body.ok).toBe(true);

    const checkRes = await request(app)
      .get(`/api/orders/${orderId}`)
      .set('Authorization', `Bearer ${adminToken}`);
    const estado = ((checkRes.body.data as any).estado || checkRes.body.data.status).toUpperCase();
    expect(estado).toBe('PAGADO');

    // Verificar que se emitió el email de confirmación
    const afterFirstSendCount = sentOrderEmails.filter(e => e.orderId === orderId).length;
    expect(afterFirstSendCount).toBe(initialEmailsCount + 1);

    // 5b. Webhook duplicado -> 200 deduped y NO re-envía email (idempotencia estricta)
    const dupRes = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    expect(dupRes.status).toBe(200);
    expect(dupRes.body.deduped).toBe(true);

    const afterDupCount = sentOrderEmails.filter(e => e.orderId === orderId).length;
    expect(afterDupCount).toBe(afterFirstSendCount);
  });

  it('6. Webhook sobre pedido CANCELADO -> 200 IGNORED + payment PAID_ORPHAN', async () => {
    // Crear pedido cancelado
    const orderRes = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        clientId: 1,
        paymentMethod: 'CULQI',
        shippingCost: 0,
        items: [{ variantId: 1, quantity: 1, unitPrice: 30 }]
      });

    const cancelledOrderId = orderRes.body.data.id;
    await request(app)
      .post(`/api/orders/${cancelledOrderId}/cancel`)
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ reason: 'cancelado por usuario' });

    const orphanChargeId = `ch_orphan_${Date.now()}`;
    const payload = {
      id: `evt_orphan_${Date.now()}`,
      type: 'charge.succeeded',
      data: {
        id: orphanChargeId,
        amount: 3000,
        currency_code: 'PEN',
        metadata: { order_id: String(cancelledOrderId) }
      }
    };

    const { rawString, sig, ts } = sign(payload);
    const r = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    expect(r.status).toBe(200);
    expect(r.body.ignored).toBe(true);
    expect(r.body.reason).toBe('ORDER_TERMINAL');

    const payment = memoryPayments.find((p) => p.providerChargeId === orphanChargeId);
    expect(payment?.status).toBe('PAID_ORPHAN');
  });

  it('7. Snapshot de checkout: Si el pedido cambia después del checkout, el webhook valida contra el snapshot congelado -> 200 OK', async () => {
    // 1. Crear pedido inicial por S/ 40
    const orderRes = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        clientId: 1,
        paymentMethod: 'CULQI',
        shippingCost: 0,
        items: [{ variantId: 1, quantity: 1, unitPrice: 40 }]
      });

    const snapOrderId = orderRes.body.data.id;

    // 2. Generar checkout inicial congelando payments.amount_cents = 4000
    const linkRes = await request(app)
      .post(`/api/orders/${snapOrderId}/payment-link`)
      .set('Authorization', `Bearer ${adminToken}`);
    expect(linkRes.status).toBe(200);
    const snapChargeId = linkRes.body.data.providerOrderId;

    // 3. Simular que el total del pedido en BD cambió a S/ 50 después del checkout
    const orderInMemory = InMemoryDataStore.orders.find(o => o.id === snapOrderId);
    if (orderInMemory) {
      orderInMemory.total_amount = 50;
      (orderInMemory as any).total_cents = 5000;
    }

    // 4. Webhook llega por los S/ 40 originales del checkout
    const payload = {
      id: `evt_snap_${Date.now()}`,
      type: 'charge.succeeded',
      data: {
        id: snapChargeId,
        amount: 4000, // 4000 coincide con el snapshot congelado de payment
        currency_code: 'PEN',
        metadata: { order_id: String(snapOrderId) }
      }
    };

    const { rawString, sig, ts } = sign(payload);
    const r = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    expect(r.status).toBe(200);
    expect(r.body.ok).toBe(true);
  });

  it('8. /payment-link reusado -> devuelve la misma checkout_url y reused: true', async () => {
    const orderRes = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        clientId: 1,
        paymentMethod: 'CULQI',
        shippingCost: 5,
        items: [{ variantId: 1, quantity: 2, unitPrice: 20 }]
      });

    const newOrderId = orderRes.body.data.id;

    const r1 = await request(app)
      .post(`/api/orders/${newOrderId}/payment-link`)
      .set('Authorization', `Bearer ${adminToken}`);

    expect(r1.status).toBe(200);
    const firstUrl = r1.body.data.checkoutUrl;
    expect(firstUrl).toBeDefined();

    const r2 = await request(app)
      .post(`/api/orders/${newOrderId}/payment-link`)
      .set('Authorization', `Bearer ${adminToken}`);

    expect(r2.status).toBe(200);
    expect(r2.body.data.checkoutUrl).toBe(firstUrl);
    expect(r2.body.data.reused).toBe(true);
  });

  it('9. /payment-link sobre pedido PAGADO -> 409 ORDER_NOT_PAYABLE', async () => {
    const r = await request(app)
      .post(`/api/orders/${orderId}/payment-link`)
      .set('Authorization', `Bearer ${adminToken}`);

    expect(r.status).toBe(409);
    expect(r.body.error.code).toBe('ORDER_NOT_PAYABLE');
  });

  it('10. Reembolso con razón inválida -> 400 INVALID_REFUND_PAYLOAD', async () => {
    const res = await request(app)
      .post(`/api/orders/${orderId}/refund`)
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ reason: 'razon_inventada_no_valida' });

    expect(res.status).toBe(400);
    expect(res.body.error.code).toBe('INVALID_REFUND_PAYLOAD');
  });

  it('11. Reembolso parcial válido y protección contra doble reembolso (REFUND_IN_PROGRESS)', async () => {
    // 1. Crear nuevo pedido pagado de S/ 100 (10000 céntimos)
    const orderRes = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        clientId: 1,
        paymentMethod: 'CULQI',
        shippingCost: 0,
        items: [{ variantId: 1, quantity: 2, unitPrice: 50 }]
      });
    const pOrderId = orderRes.body.data.id;

    const pChargeId = `ch_partial_${Date.now()}`;
    const payload = {
      id: `evt_partial_${Date.now()}`,
      type: 'charge.succeeded',
      data: {
        id: pChargeId,
        amount: 10000,
        currency_code: 'PEN',
        metadata: { order_id: String(pOrderId) }
      }
    };
    const { rawString, sig, ts } = sign(payload);
    await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    // 2. Simular que el pago quedó en REFUND_PENDING reciente (concurrencia de 2 admins)
    const paymentInMem = memoryPayments.find(p => p.orderId === pOrderId && p.status === 'PAID');
    if (paymentInMem) {
      paymentInMem.status = 'REFUND_PENDING';
      paymentInMem.updatedAt = new Date();
    }

    // Segundo intento simultáneo -> debe ser rechazado con 409 REFUND_IN_PROGRESS
    const concurrentRes = await request(app)
      .post(`/api/orders/${pOrderId}/refund`)
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ reason: 'solicitud_cliente' });

    expect(concurrentRes.status).toBe(409);
    expect(concurrentRes.body.error.code).toBe('REFUND_IN_PROGRESS');

    // Restaurar a PAID y probar reembolso parcial de S/ 40
    if (paymentInMem) paymentInMem.status = 'PAID';

    const partialRes = await request(app)
      .post(`/api/orders/${pOrderId}/refund`)
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        reason: 'producto_defectuoso',
        amountCents: 4000 // Reembolso parcial
      });

    expect(partialRes.status).toBe(200);
    expect(partialRes.body.ok).toBe(true);
    expect(partialRes.body.refund.amount).toBe(4000);
  });

  it('12. Reembolso con proveedor rechazado -> 409 REFUND_PROVIDER_ERROR', async () => {
    const orderRes = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        clientId: 1,
        paymentMethod: 'CULQI',
        shippingCost: 0,
        items: [{ variantId: 1, quantity: 1, unitPrice: 100 }]
      });

    const badRefundOrderId = orderRes.body.data.id;
    const badChargeId = 'ch_fail_refund';

    const payload = {
      id: `evt_bad_refund_${Date.now()}`,
      type: 'charge.succeeded',
      data: {
        id: badChargeId,
        amount: 10000,
        currency_code: 'PEN',
        metadata: { order_id: String(badRefundOrderId) }
      }
    };

    const { rawString, sig, ts } = sign(payload);
    await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    const res = await request(app)
      .post(`/api/orders/${badRefundOrderId}/refund`)
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ reason: 'error_sistema' });

    expect(res.status).toBe(409);
    expect(res.body.error.code).toBe('REFUND_PROVIDER_ERROR');
  });

  it('13. Reconciliación: Pedido PENDIENTE con pago Culqi capturado -> transiciona a PAGADO', async () => {
    const orderRes = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        clientId: 1,
        paymentMethod: 'CULQI',
        shippingCost: 0,
        items: [{ variantId: 1, quantity: 1, unitPrice: 500 }]
      });

    const recOrderId = orderRes.body.data.id;
    memoryPayments.push({
      orderId: recOrderId,
      provider: 'culqi',
      providerChargeId: `ch_mock_reconcile_paid_${Date.now()}`,
      amountCents: 50000,
      currency: 'PEN',
      status: 'PENDING',
      rawResponse: {}
    });

    await reconcilePendingPayments();

    const checkOrder = InMemoryDataStore.orders.find((o) => o.id === recOrderId);
    const estado = ((checkOrder as any).estado || checkOrder?.status || '').toUpperCase();
    expect(estado).toBe('PAGADO');
  });

  it('14. Reconciliación: REFUND_PENDING huérfano con Culqi exitoso -> recupera y transiciona a REEMBOLSADO', async () => {
    const orderRes = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        clientId: 1,
        paymentMethod: 'CULQI',
        shippingCost: 0,
        items: [{ variantId: 1, quantity: 1, unitPrice: 500 }]
      });

    const orphanRefundOrderId = orderRes.body.data.id;
    const orderInMem = InMemoryDataStore.orders.find(o => o.id === orphanRefundOrderId);
    if (orderInMem) {
      (orderInMem as any).estado = 'PAGADO';
      orderInMem.status = 'PAGADO' as any;
    }

    // Pago que quedó en REFUND_PENDING tras un crash del worker
    memoryPayments.push({
      orderId: orphanRefundOrderId,
      provider: 'culqi',
      providerChargeId: `ch_mock_reconcile_refunded_${Date.now()}`,
      amountCents: 50000,
      currency: 'PEN',
      status: 'REFUND_PENDING',
      rawResponse: {},
      updatedAt: new Date(Date.now() - 10 * 60_000) // 10 minutos atrás
    });

    await reconcilePendingPayments();

    const payment = memoryPayments.find(p => p.orderId === orphanRefundOrderId);
    expect(payment?.status).toBe('REFUNDED');

    const checkOrder = InMemoryDataStore.orders.find(o => o.id === orphanRefundOrderId);
    const estado = ((checkOrder as any).estado || checkOrder?.status || '').toUpperCase();
    expect(estado).toBe('REEMBOLSADO');
  });

  it('15. Reconciliación: webhook_events huérfanos RECEIVED > 5 min -> marcados FAILED', async () => {
    const staleEventId = `evt_stale_${Date.now()}`;
    memoryWebhookEvents.set(`culqi:${staleEventId}`, {
      status: 'RECEIVED',
      attempts: 1,
      createdAt: new Date(Date.now() - 10 * 60_000) // 10 minutos atrás
    });

    await reconcilePendingPayments();

    const eventRecord = memoryWebhookEvents.get(`culqi:${staleEventId}`);
    expect(eventRecord?.status).toBe('FAILED');
    expect(eventRecord?.error).toBe('PROCESSING_TIMEOUT_ORPHAN');
  });
});

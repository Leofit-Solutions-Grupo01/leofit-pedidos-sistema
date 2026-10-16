/**
 * @file paymentWebhook.hardening.test.ts
 * @description Suite de pruebas de resiliencia, validación de montos, anti-replay, idempotencia y reembolsos (Ronda 8.5).
 */

import crypto from 'node:crypto';
import request from 'supertest';
import { createApp } from '../src/app';
import { JWTService } from '../src/infrastructure/security/jwt.utils';
import { reconcilePendingPayments } from '../src/jobs/reconcilePayments';
import { memoryPayments } from '../src/controllers/paymentWebhook.controller';
import { InMemoryDataStore } from '../src/infrastructure/repositories/memory.repositories';

const SECRET = 'test_culqi_hardening_secret_98765';
process.env.CULQI_WEBHOOK_SECRET = SECRET;

function sign(payload: any, opts: { timestamp?: number; badSig?: boolean } = {}) {
  const rawString = JSON.stringify(payload);
  const raw = Buffer.from(rawString, 'utf8');
  const ts = opts.timestamp ?? Math.floor(Date.now() / 1000);
  const signedPayload = Buffer.concat([Buffer.from(`${ts}.`), raw]);
  const sig = opts.badSig
    ? 'deadbeefcafebabe'
    : crypto.createHmac('sha256', SECRET).update(signedPayload).digest('hex');
  return { rawString, sig, ts };
}

describe('Ronda 8.5 — Hardening de Pagos y Máquina de Estados', () => {
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

  it('1. Webhook con amount distinto al total -> 409 AMOUNT_MISMATCH y NO transiciona', async () => {
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

  it('2. Webhook con currency distinta -> 409 CURRENCY_MISMATCH', async () => {
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

  it('3. Replay con timestamp viejo (>5min) -> 401 SIGNATURE_EXPIRED', async () => {
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

  it('4. Webhook con monto correcto y firma válida -> 200 y transiciona a PAGADO', async () => {
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

    // 4b. Webhook duplicado exitoso -> 200 deduped, 1 sola transición
    const dupRes = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .set('x-culqi-timestamp', String(ts))
      .send(rawString);

    expect(dupRes.status).toBe(200);
    expect(dupRes.body.deduped).toBe(true);
  });

  it('5. Webhook sobre pedido CANCELADO -> 200 IGNORED + payment PAID_ORPHAN', async () => {
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

  it('6. /payment-link reusado -> devuelve la misma checkout_url y reused: true', async () => {
    // Crear un nuevo pedido PENDIENTE
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

    // Primer llamado a payment-link
    const r1 = await request(app)
      .post(`/api/orders/${newOrderId}/payment-link`)
      .set('Authorization', `Bearer ${adminToken}`);

    expect(r1.status).toBe(200);
    const firstUrl = r1.body.data.checkoutUrl;
    expect(firstUrl).toBeDefined();

    // Segundo llamado a payment-link
    const r2 = await request(app)
      .post(`/api/orders/${newOrderId}/payment-link`)
      .set('Authorization', `Bearer ${adminToken}`);

    expect(r2.status).toBe(200);
    expect(r2.body.data.checkoutUrl).toBe(firstUrl);
    expect(r2.body.data.reused).toBe(true);
  });

  it('7. /payment-link sobre pedido PAGADO -> 409 ORDER_NOT_PAYABLE', async () => {
    const r = await request(app)
      .post(`/api/orders/${orderId}/payment-link`)
      .set('Authorization', `Bearer ${adminToken}`);

    expect(r.status).toBe(409);
    expect(r.body.error.code).toBe('ORDER_NOT_PAYABLE');
  });

  it('8. Reembolso exitoso -> transición a REEMBOLSADO', async () => {
    // Pedido pagado orderId
    const res = await request(app)
      .post(`/api/orders/${orderId}/refund`)
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ reason: 'cliente desistió de la compra' });

    expect(res.status).toBe(200);
    expect(res.body.ok).toBe(true);
    expect(res.body.refund.status).toBe('successful');

    const checkRes = await request(app)
      .get(`/api/orders/${orderId}`)
      .set('Authorization', `Bearer ${adminToken}`);
    const estado = ((checkRes.body.data as any).estado || checkRes.body.data.status).toUpperCase();
    expect(estado).toBe('REEMBOLSADO');
  });

  it('9. Reembolso con proveedor rechazado -> 409 REFUND_PROVIDER_ERROR', async () => {
    // Crear pedido, pagarlo con un chargeId que simule fallo de Culqi
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

    // Intentar reembolso que fallará en Culqi
    const res = await request(app)
      .post(`/api/orders/${badRefundOrderId}/refund`)
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ reason: 'falla bancaria simulada' });

    expect(res.status).toBe(409);
    expect(res.body.error.code).toBe('REFUND_PROVIDER_ERROR');
  });

  it('10. Reconciliación: Pedido PENDIENTE con pago Culqi capturado -> transiciona a PAGADO', async () => {
    // Crear pedido pendiente
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
    // Simular un pago PENDING en memoria con chargeId reconciliable
    memoryPayments.push({
      orderId: recOrderId,
      provider: 'culqi',
      providerChargeId: `ch_mock_reconcile_paid_${Date.now()}`,
      amountCents: 50000,
      currency: 'PEN',
      status: 'PENDING',
      rawResponse: {}
    });

    // Ejecutar el job de reconciliación
    await reconcilePendingPayments();

    const checkOrder = InMemoryDataStore.orders.find((o) => o.id === recOrderId);
    const estado = ((checkOrder as any).estado || checkOrder?.status || '').toUpperCase();
    expect(estado).toBe('PAGADO');
  });
});

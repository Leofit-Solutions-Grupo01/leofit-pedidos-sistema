import crypto from 'node:crypto';
import request from 'supertest';
import { createApp } from '../src/app';
import { JWTService } from '../src/infrastructure/security/jwt.utils';
import { transitionOrder } from '../src/services/orders/stateMachine';

const CULQI_SECRET = 'test_culqi_webhook_secret_key_12345';
process.env.CULQI_WEBHOOK_SECRET = CULQI_SECRET;

function sign(payload: object) {
  const rawString = JSON.stringify(payload);
  const sig = crypto.createHmac('sha256', CULQI_SECRET).update(Buffer.from(rawString, 'utf8')).digest('hex');
  return { rawString, sig };
}

describe('Ronda 8: Webhook de Pagos, Deduplicación y Máquina de Estados', () => {
  const app = createApp();
  let adminToken: string;
  let orderId: number;

  beforeAll(async () => {
    adminToken = JWTService.generateToken({
      userId: 1,
      email: 'admin@leofit.pe',
      name: 'Admin Test',
      role: 'ADMIN'
    });

    // 1. Crear un pedido PENDIENTE vía API
    const orderRes = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        clientId: 1,
        paymentMethod: 'TRANSFERENCIA',
        shippingCost: 10,
        items: [{ variantId: 1, quantity: 1, unitPrice: 50 }]
      });

    expect([200, 201]).toContain(orderRes.status);
    orderId = orderRes.body.data.id;
  });

  it('1. Rechaza firma HMAC inválida (401)', async () => {
    const res = await request(app)
      .post('/api/webhooks/culqi')
      .set('x-signature', 'deadbeefcafebabe')
      .send({ test: true });

    expect(res.status).toBe(401);
    expect(res.body.error.code).toBe('INVALID_SIGNATURE');
  });

  it('2. GET payment-link devuelve checkoutUrl para un pedido pendiente', async () => {
    const res = await request(app)
      .post(`/api/orders/${orderId}/payment-link`)
      .set('Authorization', `Bearer ${adminToken}`);

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.checkoutUrl).toBeDefined();
    expect(res.body.data.checkoutUrl).toContain('culqi.com');
  });

  it('3. Procesa pago válido y transiciona pedido a PAGADO', async () => {
    const eventId = `evt_test_${Date.now()}_1`;
    const payload = {
      id: eventId,
      type: 'charge.succeeded',
      data: {
        id: `ch_test_${Date.now()}`,
        amount: 6000,
        currency_code: 'PEN',
        metadata: { order_id: String(orderId) }
      }
    };

    const { rawString, sig } = sign(payload);

    const res = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .send(rawString);

    expect(res.status).toBe(200);
    expect(res.body.ok).toBe(true);

    // Consultar pedido y verificar estado PAGADO
    const getRes = await request(app)
      .get(`/api/orders/${orderId}`)
      .set('Authorization', `Bearer ${adminToken}`);

    expect(getRes.status).toBe(200);
    const estado = ((getRes.body.data as any).estado || getRes.body.data.status).toUpperCase();
    expect(estado).toBe('PAGADO');
  });

  it('4. Es idempotente: el mismo event_id no duplica y devuelve deduped: true', async () => {
    const eventId = `evt_test_dedup_${Date.now()}`;
    const payload = {
      id: eventId,
      type: 'charge.succeeded',
      data: {
        id: `ch_dedup_${Date.now()}`,
        amount: 6000,
        currency_code: 'PEN',
        metadata: { order_id: String(orderId) }
      }
    };

    const { rawString, sig } = sign(payload);

    // Primer envío: procesa
    const r1 = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .send(rawString);

    expect(r1.status).toBe(200);
    expect(r1.body.ok).toBe(true);

    // Segundo envío idéntico: detecta deduplicación
    const r2 = await request(app)
      .post('/api/webhooks/culqi')
      .set('Content-Type', 'application/json')
      .set('x-signature', sig)
      .send(rawString);

    expect(r2.status).toBe(200);
    expect(r2.body.deduped).toBe(true);
  });

  it('5. Rechaza payment-link si el pedido ya está PAGADO (409)', async () => {
    const res = await request(app)
      .post(`/api/orders/${orderId}/payment-link`)
      .set('Authorization', `Bearer ${adminToken}`);

    expect(res.status).toBe(409);
    expect(res.body.error.code).toBe('ORDER_NOT_PAYABLE');
  });

  it('6. Máquina de Estados: Transición no permitida arroja 409 INVALID_TRANSITION', async () => {
    // Intentar mover de PAGADO directamente a ENTREGADO sin pasar por EN_CAMINO
    await expect(
      transitionOrder(null, orderId, 'ENTREGADO', 'test_actor')
    ).rejects.toMatchObject({
      status: 409,
      code: 'INVALID_TRANSITION'
    });
  });
});

import request from 'supertest';
import { createApp } from '../src/app';
import crypto from 'crypto';

describe('SEC-05 Webhook HMAC Validation', () => {
  const app = createApp();
  const webhookUrl = '/api/external/payments/webhook';

  const payload = {
    provider: 'YAPE',
    transactionId: '123456',
    orderCode: 'ORD-123',
    amount: 150.00,
    status: 'APPROVED'
  };

  const payloadString = JSON.stringify(payload);

  it('Debe arrojar un error si WEBHOOK_SECRET no está configurado (Fail-Fast al arranque)', () => {
    delete process.env.WEBHOOK_SECRET;
    expect(() => {
      jest.resetModules();
      require('../src/controllers/external.controller');
    }).toThrow('FATAL ERROR: WEBHOOK_SECRET must be defined in the environment.');
    process.env.WEBHOOK_SECRET = 'test_secret_123'; // Restore
  });

  it('Debe rechazar la petición con firma inválida de longitud incorrecta sin arrojar 500 (401)', async () => {
    const response = await request(app)
      .post(webhookUrl)
      .set('Content-Type', 'application/json')
      .set('x-signature', 'abcd') // short length
      .send(payloadString);
    
    expect(response.status).toBe(401);
    expect(response.body.error).toBe('INVALID_SIGNATURE');
  });

  it('Debe rechazar la petición si no tiene firma HMAC (401)', async () => {
    const response = await request(app)
      .post(webhookUrl)
      .send(payload);
    
    expect(response.status).toBe(401);
    expect(response.body.error).toBe('Missing webhook signature');
  });

  it('Debe rechazar la petición con firma inválida (401)', async () => {
    const response = await request(app)
      .post(webhookUrl)
      .set('x-signature', 'firma_invalida_totalmente')
      .send(payload);
    
    expect(response.status).toBe(401);
    expect(response.body.error).toBe('INVALID_SIGNATURE');
  });

  it('Debe aceptar la petición si la firma es válida (200)', async () => {
    const secret = 'test_global_secret_123';
    const expectedSignature = crypto.createHmac('sha256', secret).update(payloadString).digest('hex');

    const response = await request(app)
      .post(webhookUrl)
      .set('Content-Type', 'application/json')
      .set('x-signature', expectedSignature)
      .send(payloadString);
    
    expect(response.status).toBe(200);
    expect(response.body.success).toBe(true);
  });
});

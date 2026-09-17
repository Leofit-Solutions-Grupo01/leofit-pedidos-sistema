// =============================================================================
// ORDERS & TRANSACTION TESTS - ACID TRANSACTIONS & STOCK CONSISTENCY
// =============================================================================

import request from 'supertest';
import { createApp } from '../src/app';
import { JWTService } from '../src/infrastructure/security/jwt.utils';

const app = createApp();
const testToken = JWTService.generateToken({
  userId: 1,
  email: 'admin@leofit.pe',
  name: 'Lady Loayza',
  role: 'ADMIN'
});

describe('Módulo de Gestión de Pedidos (/api/orders)', () => {
  it('Debe consultar un pedido por su código público de tracking', async () => {
    const res = await request(app).get('/api/orders/track/LEO-20260302-001');
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.order_number).toBe('LEO-20260302-001');
  });

  it('Debe crear un pedido nuevo con validación atómica y cálculo de totales', async () => {
    const res = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${testToken}`)
      .send({
        clientData: {
          fullName: 'Juan Pérez Test',
          phone: '987000111',
          address: 'Av. Arequipa 1234',
          district: 'Lince',
          reference: 'Piso 4'
        },
        paymentMethod: 'YAPE',
        shippingCost: 10.00,
        notes: 'Prueba unitaria automatizada',
        items: [
          {
            variantId: 1, // Polo Gym Beast S
            quantity: 1,
            unitPrice: 49.90
          }
        ]
      });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.order_number).toBeDefined();
    expect(res.body.data.status).toBe('RECIBIDO');
    expect(res.body.data.total_amount).toBe(59.90);
  });

  it('Debe rechazar la creación de pedidos si la cantidad excede el stock disponible', async () => {
    const res = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${testToken}`)
      .send({
        clientData: {
          fullName: 'Stock Overflow User',
          phone: '987999888',
          address: 'Jr. Junín 500',
          district: 'Lima'
        },
        paymentMethod: 'PLIN',
        shippingCost: 10.00,
        items: [
          {
            variantId: 1,
            quantity: 99999, // Exceeds available stock
            unitPrice: 49.90
          }
        ]
      });

    expect(res.status).toBe(409);
    expect(res.body.success).toBe(false);
    expect(res.body.error.code).toBe('INSUFFICIENT_STOCK');
  });

  it('Debe permitir la actualización de estados del pedido', async () => {
    const res = await request(app)
      .patch('/api/orders/1/status')
      .set('Authorization', `Bearer ${testToken}`)
      .send({
        status: 'EN_CAMINO',
        comments: 'Despacho verificado por testing'
      });

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.status).toBe('EN_CAMINO');
  });
});

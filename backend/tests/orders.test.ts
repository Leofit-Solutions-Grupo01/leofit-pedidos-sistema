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

  describe('Paginación y X-Total-Count', () => {
    it('X-Total-Count reporta el total real, no el tamaño de la página', async () => {
      // Creamos un par de pedidos extra para asegurar que el total sea > 1
      for(let i=0; i<2; i++) {
        await request(app)
          .post('/api/orders')
          .set('Authorization', `Bearer ${testToken}`)
          .send({
            clientData: { fullName: `Test User ${i}`, phone: '987000111', address: 'A', district: 'L' },
            paymentMethod: 'YAPE', shippingCost: 10,
            items: [{ variantId: 1, quantity: 1, unitPrice: 49.90 }]
          });
      }

      // Solicitamos limit=1
      const res = await request(app)
        .get('/api/orders?limit=1')
        .set('Authorization', `Bearer ${testToken}`);
      
      expect(res.status).toBe(200);
      expect(res.header['x-total-count']).toBeDefined();
      const total = parseInt(res.header['x-total-count'], 10);
      
      expect(total).toBeGreaterThanOrEqual(2);      // total real en toda la tabla
      expect(res.body.data.length).toBe(1);         // página respeta el limit
      expect(total).not.toBe(res.body.data.length); // Falla si el código buggeado (min(N, limit)) siguiera activo
      
      expect(res.body.limit).toBe(1);
      expect(res.body.page).toBe(1);
      expect(res.body.total).toBe(total);
    });

    it('Debe rechazar paginación con limit fuera de rango (limit=0)', async () => {
      const res = await request(app)
        .get('/api/orders?limit=0')
        .set('Authorization', `Bearer ${testToken}`);
      
      expect(res.status).toBe(400); // Error de Zod: min(1)
      expect(res.body.success).toBe(false);
      expect(JSON.stringify(res.body.error)).toContain('Number must be greater than or equal to 1');
    });

    it('Debe rechazar paginación con limit exagerado (limit=999999)', async () => {
      const res = await request(app)
        .get('/api/orders?limit=999999')
        .set('Authorization', `Bearer ${testToken}`);
      
      expect(res.status).toBe(400); // Error de Zod: max(100)
      expect(res.body.success).toBe(false);
      expect(JSON.stringify(res.body.error)).toContain('Number must be less than or equal to 100');
    });

    it('Debe rechazar paginación con offset negativo (page=0 o negativo)', async () => {
      const res = await request(app)
        .get('/api/orders?page=0')
        .set('Authorization', `Bearer ${testToken}`);
      
      expect(res.status).toBe(400); // Error de Zod: min(1)
      expect(res.body.success).toBe(false);
      expect(JSON.stringify(res.body.error)).toContain('Number must be greater than or equal to 1');
    });
  describe('Extensión Logística (Shipping Fields)', () => {
    it('T1: Debe rechazar pedido PROVINCIA si no tiene destinationCity o shippingAgency', async () => {
      const res = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          clientData: { fullName: 'Pedro', phone: '999888777', address: 'Calle 1', district: 'Lima' },
          paymentMethod: 'YAPE',
          shippingCost: 15,
          shippingType: 'PROVINCIA',
          items: [{ variantId: 1, quantity: 1, unitPrice: 50 }]
        });
      
      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(JSON.stringify(res.body.error)).toContain('Para envíos a PROVINCIA, la ciudad de destino y agencia son obligatorias');
    });

    it('T2: Debe crear pedido PROVINCIA con datos completos y retornar campos', async () => {
      const res = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          clientData: { fullName: 'Pedro P', phone: '999888771', address: 'Calle 1', district: 'Lima' },
          paymentMethod: 'YAPE',
          shippingCost: 15,
          shippingType: 'PROVINCIA',
          destinationCity: 'Arequipa',
          shippingAgency: 'Shalom',
          trackingNumber: 'TRK12345',
          items: [{ variantId: 1, quantity: 1, unitPrice: 50 }]
        });
      
      expect(res.status).toBe(201);
      expect(res.body.success).toBe(true);
      expect(res.body.data.shippingType).toBe('PROVINCIA');
      expect(res.body.data.destinationCity).toBe('Arequipa');
      expect(res.body.data.shippingAgency).toBe('Shalom');
      expect(res.body.data.trackingNumber).toBe('TRK12345');
    });

    it('T3: Debe crear pedido LIMA sin datos logísticos adicionales', async () => {
      const res = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          clientData: { fullName: 'Maria M', phone: '999888772', address: 'Calle 2', district: 'Lima' },
          paymentMethod: 'TRANSFERENCIA',
          shippingCost: 10,
          shippingType: 'LIMA',
          items: [{ variantId: 1, quantity: 1, unitPrice: 50 }]
        });
      
      expect(res.status).toBe(201);
      expect(res.body.success).toBe(true);
      expect(res.body.data.shippingType).toBe('LIMA');
      expect(res.body.data.destinationCity).toBeUndefined();
    });

    it('T4: Debe rechazar trackingNumber inválido (muy corto)', async () => {
      const res = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          clientData: { fullName: 'Luis', phone: '999888773', address: 'Calle 3', district: 'Lima' },
          paymentMethod: 'YAPE',
          shippingCost: 15,
          shippingType: 'PROVINCIA',
          destinationCity: 'Cusco',
          shippingAgency: 'Marvisur',
          trackingNumber: 'A', // Muy corto
          items: [{ variantId: 1, quantity: 1, unitPrice: 50 }]
        });
      
      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(JSON.stringify(res.body.error)).toContain('String must contain at least 5 character(s)');
    });

    it('T5: GET /api/orders/:id debe retornar todos los campos logísticos (Round-Trip)', async () => {
      // 1. Crear
      const postRes = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          clientData: { fullName: 'Ana', phone: '999888774', address: 'Calle 4', district: 'Lima' },
          paymentMethod: 'PLIN',
          shippingCost: 20,
          shippingType: 'PROVINCIA',
          destinationCity: 'Trujillo',
          shippingAgency: 'Civa',
          items: [{ variantId: 1, quantity: 2, unitPrice: 50 }]
        });
      
      expect(postRes.status).toBe(201);
      const orderId = postRes.body.data.id;

      // 2. Leer
      const getRes = await request(app)
        .get(`/api/orders/${orderId}`)
        .set('Authorization', `Bearer ${testToken}`);
      
      expect(getRes.status).toBe(200);
      expect(getRes.body.success).toBe(true);
      expect(getRes.body.data.shippingType).toBe('PROVINCIA');
      expect(getRes.body.data.destinationCity).toBe('Trujillo');
      expect(getRes.body.data.shippingAgency).toBe('Civa');
      expect(getRes.body.data.payment_method).toBe('PLIN'); // Se verifica que el método de pago se lee bien
    });
  });
});
});

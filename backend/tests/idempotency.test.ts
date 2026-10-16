// =============================================================================
// IDEMPOTENCY & CONCURRENCY TESTS - RFC 8785 & RFC 9457 SPECIFICATION
// =============================================================================

import request from 'supertest';
import { createApp } from '../src/app';
import { JWTService } from '../src/infrastructure/security/jwt.utils';
import { canonicalizeJson } from '../src/middlewares/idempotency.middleware';
import { dbPool, isPostgresAvailable } from '../src/config/database';

const app = createApp();

const user1Token = JWTService.generateToken({
  userId: 101,
  email: 'operador1@leofit.pe',
  name: 'Operador Uno',
  role: 'OPERATOR'
});

const user2Token = JWTService.generateToken({
  userId: 202,
  email: 'operador2@leofit.pe',
  name: 'Operador Dos',
  role: 'OPERATOR'
});

describe('Módulo de Idempotencia y Resiliencia (RFC 8785 & Concurrencia)', () => {
  describe('Canonical JSON (RFC 8785 / JCS)', () => {
    it('Debe generar el mismo string canónico independientemente del orden de las claves del objeto', () => {
      const obj1 = { b: 2, a: 1, c: { z: 99, y: 88 } };
      const obj2 = { a: 1, c: { y: 88, z: 99 }, b: 2 };

      expect(canonicalizeJson(obj1)).toBe('{"a":1,"b":2,"c":{"y":88,"z":99}}');
      expect(canonicalizeJson(obj1)).toBe(canonicalizeJson(obj2));
    });

    it('Debe manejar arrays, valores primitivos y null sin alterar su orden interno', () => {
      const payload = {
        items: [{ variantId: 1, quantity: 2 }, { variantId: 2, quantity: 1 }],
        notes: null,
        active: true
      };
      const canon = canonicalizeJson(payload);
      expect(canon).toContain('"items":[{"quantity":2,"variantId":1},{"quantity":1,"variantId":2}]');
      expect(canon).toContain('"notes":null');
      expect(canon).toContain('"active":true');
    });
  });

  describe('Garantías de Transacción HTTP y Detección de Payload Mismatch', () => {
    it('Debe rechazar cabeceras Idempotency-Key con formato inválido (400)', async () => {
      const res = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${user1Token}`)
        .set('Idempotency-Key', 'corta') // < 8 caracteres
        .send({
          clientData: { fullName: 'Test', phone: '999888777', address: 'Lima', district: 'Lima' },
          paymentMethod: 'YAPE',
          shippingCost: 10,
          items: [{ variantId: 1, quantity: 1, unitPrice: 49.9 }]
        });

      expect(res.status).toBe(400);
      expect(res.body.error.code).toBe('INVALID_IDEMPOTENCY_KEY');
    });

    it('Si no hay cabecera Idempotency-Key, procesa la petición normalmente', async () => {
      const res = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${user1Token}`)
        .send({
          clientData: { fullName: 'Cliente Normal', phone: '999888777', address: 'Av. Brasil 100', district: 'Jesus Maria' },
          paymentMethod: 'PLIN',
          shippingCost: 8,
          items: [{ variantId: 1, quantity: 1, unitPrice: 49.9 }]
        });

      // Si Postgres no está activo en test, el repositorio in-memory crea la orden exitosamente
      expect([201, 503]).toContain(res.status);
      if (res.status === 201) {
        expect(res.body.success).toBe(true);
      }
    });
  });

  // Pruebas que validan la lógica de base de datos cuando Postgres está disponible o simulado
  describe('Persistencia y Concurrencia Simultánea (Promise.all)', () => {
    it('Dos peticiones simultáneas con la misma key procesan atómicamente sin duplicar pedidos', async () => {
      const testKey = `CONC-${Date.now()}-A1B2C3`;
      const orderPayload = {
        clientData: { fullName: 'Concurrencia Test', phone: '912345678', address: 'Calle 10', district: 'Lince' },
        paymentMethod: 'YAPE',
        shippingCost: 10,
        items: [{ variantId: 1, quantity: 1, unitPrice: 49.9 }]
      };

      // Disparo simultáneo con Promise.all
      const [res1, res2] = await Promise.all([
        request(app)
          .post('/api/orders')
          .set('Authorization', `Bearer ${user1Token}`)
          .set('Idempotency-Key', testKey)
          .send(orderPayload),
        request(app)
          .post('/api/orders')
          .set('Authorization', `Bearer ${user1Token}`)
          .set('Idempotency-Key', testKey)
          .send(orderPayload)
      ]);

      // Si Postgres está disponible, una es 201 y la otra es 201 (cacheada) o 409 (en progreso)
      // Si corre en fallback sin Postgres, ambas retornan 503 IDEMPOTENCY_STORE_UNAVAILABLE (fail-closed seguro)
      if (isPostgresAvailable()) {
        const statuses = [res1.status, res2.status].sort();
        expect(statuses[0]).toBe(201); // Al menos una creó el pedido exitosamente
        expect([201, 409]).toContain(statuses[1]); // La otra obtuvo el cache o 409 controlado
      } else {
        expect(res1.status).toBe(503);
        expect(res2.status).toBe(503);
        expect(res1.body.error.code).toBe('IDEMPOTENCY_STORE_UNAVAILABLE');
      }
    });

    it('Misma key enviada por dos usuarios distintos está debidamente aislada (Scoping)', async () => {
      const sharedKey = `USER-SCOPE-${Date.now()}`;
      const payloadUser1 = {
        clientData: { fullName: 'Cliente User 1', phone: '911111111', address: 'A', district: 'Lima' },
        paymentMethod: 'YAPE',
        shippingCost: 10,
        items: [{ variantId: 1, quantity: 1, unitPrice: 49.9 }]
      };

      const resUser1 = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${user1Token}`)
        .set('Idempotency-Key', sharedKey)
        .send(payloadUser1);

      const resUser2 = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${user2Token}`)
        .set('Idempotency-Key', sharedKey)
        .send(payloadUser1);

      // Si PG está activo, cada usuario tiene su propio scope
      if (isPostgresAvailable()) {
        expect(resUser1.status).toBe(201);
        expect(resUser2.status).toBe(201);
      } else {
        expect(resUser1.status).toBe(503);
        expect(resUser2.status).toBe(503);
      }
    });
  });
});

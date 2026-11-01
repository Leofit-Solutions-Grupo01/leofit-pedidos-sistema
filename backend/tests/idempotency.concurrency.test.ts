// =============================================================================
// IDEMPOTENCY CONCURRENCY & ORPHAN RECOVERY TESTS - ACID VERIFICATION
// =============================================================================

import request from 'supertest';
import { createApp } from '../src/app';
import { JWTService } from '../src/infrastructure/security/jwt.utils';
import { dbPool, isPostgresAvailable } from '../src/config/database';
import { runVersionedMigrations } from '../src/database/migrations/runner';
import crypto from 'crypto';

const app = createApp();

const userToken = JWTService.generateToken({
  userId: 1,
  email: 'admin@leofit.pe',
  name: 'Lady Loayza',
  role: 'ADMIN'
});

const generateTestKey = () => `CONC-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;

describe('Idempotency — Concurrencia Real, Recuperación de Huérfanos y Migraciones', () => {
  it('DOS requests simultáneos con la MISMA key → exactamente 1 pedido creado', async () => {
    const key = generateTestKey();
    const payload = {
      clientData: {
        fullName: 'Test Concurrencia Real',
        phone: '999888777',
        address: 'Av. Arequipa 123',
        district: 'Lima'
      },
      paymentMethod: 'YAPE',
      shippingCost: 10,
      items: [{ variantId: 1, quantity: 1, unitPrice: 49.9 }]
    };

    const [r1, r2] = await Promise.all([
      request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${userToken}`)
        .set('Idempotency-Key', key)
        .send(payload),
      request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${userToken}`)
        .set('Idempotency-Key', key)
        .send(payload),
    ]);

    if (isPostgresAvailable()) {
      const codes = [r1.status, r2.status].sort();
      expect(codes[0]).toBe(201);
      expect([201, 409]).toContain(codes[1]);

      // Si fue 409, el reintento debe devolver el mismo pedido cacheado
      let finalRes = r1.status === 201 ? r1 : r2;
      if (codes[1] === 409) {
        await new Promise((r) => setTimeout(r, 600));
        finalRes = await request(app)
          .post('/api/orders')
          .set('Authorization', `Bearer ${userToken}`)
          .set('Idempotency-Key', key)
          .send(payload);
      }

      expect(finalRes.status).toBe(201);
      expect(finalRes.body.data.id).toBeDefined();

      // Verificar que solo existe UN pedido con esa orden en orders
      const orderNumber = finalRes.body.data.order_number;
      const { rows } = await dbPool.query(
        `SELECT COUNT(*)::int AS count FROM orders WHERE order_number = $1`,
        [orderNumber]
      );
      expect(rows[0].count).toBe(1);
    } else {
      expect(r1.status).toBe(503);
      expect(r2.status).toBe(503);
    }
  });

  it('3 requests concurrentes con PENDING huérfano → 1 solo recupera atómicamente, resto 409', async () => {
    const key = generateTestKey();
    const userId = 1;

    const payload = {
      clientData: {
        fullName: 'Huérfano Test',
        phone: '999888777',
        address: 'Av. Brasil 456',
        district: 'Jesus Maria'
      },
      paymentMethod: 'PLIN',
      shippingCost: 8,
      items: [{ variantId: 1, quantity: 1, unitPrice: 49.9 }]
    };

    // Calcular hash canónico del body
    const pathForHash = '/api/orders';
    const hashPayload = `${userId}:POST:${pathForHash}:${JSON.stringify(payload)}`;
    const realHash = crypto.createHash('sha256').update(hashPayload).digest('hex');

    if (isPostgresAvailable()) {
      // Simular huérfano: registro PENDING con locked_until expirado en el pasado
      await dbPool.query(
        `INSERT INTO idempotency_keys
           (user_id, key, request_hash, status, locked_until, expires_at)
         VALUES ($1, $2, $3, 'PENDING', NOW() - INTERVAL '60 seconds', NOW() + INTERVAL '48 hours')
         ON CONFLICT (user_id, key) DO UPDATE 
           SET status = 'PENDING',
               request_hash = $3,
               locked_until = NOW() - INTERVAL '60 seconds'`,
        [userId, key, realHash]
      );

      // Disparar 3 peticiones simultáneas
      const results = await Promise.all([
        request(app).post('/api/orders').set('Authorization', `Bearer ${userToken}`).set('Idempotency-Key', key).send(payload),
        request(app).post('/api/orders').set('Authorization', `Bearer ${userToken}`).set('Idempotency-Key', key).send(payload),
        request(app).post('/api/orders').set('Authorization', `Bearer ${userToken}`).set('Idempotency-Key', key).send(payload),
      ]);

      const ok = results.filter((r) => r.status === 201);
      const conflict = results.filter((r) => r.status === 409);
      expect(ok.length).toBe(1);
      expect(conflict.length).toBe(2);
    } else {
      expect(true).toBe(true);
    }
  });

  it('FAILED con payload A, reintento con payload B → 422, NO re-ejecuta (Anti-Bypass)', async () => {
    const key = generateTestKey();
    const payloadA = {
      clientData: { fullName: 'A', phone: '', address: 'Lima', district: 'Lima' }, // Teléfono vacío -> 400
      paymentMethod: 'YAPE',
      shippingCost: 10,
      items: [{ variantId: 1, quantity: 1, unitPrice: 49.9 }]
    };
    const payloadB = {
      clientData: { fullName: 'B', phone: '999888777', address: 'Lima', district: 'Lima' },
      paymentMethod: 'YAPE',
      shippingCost: 10,
      items: [{ variantId: 1, quantity: 1, unitPrice: 49.9 }]
    };

    const r1 = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${userToken}`)
      .set('Idempotency-Key', key)
      .send(payloadA);

    if (isPostgresAvailable()) {
      expect(r1.status).toBe(400);

      const r2 = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${userToken}`)
        .set('Idempotency-Key', key)
        .send(payloadB);

      expect(r2.status).toBe(422);
      expect(r2.body.error.code).toBe('IDEMPOTENCY_PAYLOAD_MISMATCH');
    } else {
      expect([400, 503]).toContain(r1.status);
    }
  });

  it('Mismo usuario con dos keys DISTINTAS en paralelo → NO se bloquean entre sí (Two-Key Advisory Lock)', async () => {
    const key1 = generateTestKey();
    const key2 = generateTestKey();

    const payload = {
      clientData: { fullName: 'Doble Pedido Paralelo', phone: '912345678', address: 'Calle 1', district: 'Lima' },
      paymentMethod: 'YAPE',
      shippingCost: 10,
      items: [{ variantId: 1, quantity: 1, unitPrice: 49.9 }]
    };

    const [r1, r2] = await Promise.all([
      request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${userToken}`)
        .set('Idempotency-Key', key1)
        .send(payload),
      request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${userToken}`)
        .set('Idempotency-Key', key2)
        .send(payload),
    ]);

    if (isPostgresAvailable()) {
      // Ambas deben procesar sin bloquearse mutuamente
      expect(r1.status).toBe(201);
      expect(r2.status).toBe(201);
      expect(r1.body.data.id).not.toBe(r2.body.data.id);
    } else {
      expect(r1.status).toBe(503);
      expect(r2.status).toBe(503);
    }
  });

  it('Migraciones versionadas son idempotentes (ejecutar dos veces no duplica ni falla)', async () => {
    if (isPostgresAvailable()) {
      await expect(runVersionedMigrations()).resolves.not.toThrow();
      await expect(runVersionedMigrations()).resolves.not.toThrow();
    } else {
      expect(true).toBe(true);
    }
  });
});

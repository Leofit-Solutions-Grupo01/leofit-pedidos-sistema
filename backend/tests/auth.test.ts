// =============================================================================
// AUTHENTICATION & RBAC TESTS - LEOFIT SECURITY
// =============================================================================

import request from 'supertest';
import { createApp } from '../src/app';
import { JWTService } from '../src/infrastructure/security/jwt.utils';

const app = createApp();

describe('Módulo de Autenticación & Seguridad RBAC (/api/auth)', () => {
  
  let adminToken = '';
  let operatorToken = '';

  beforeAll(() => {
    adminToken = JWTService.generateToken({ userId: 1, email: 'admin@leofit.pe', name: 'Admin Test', role: 'ADMIN' });
    operatorToken = JWTService.generateToken({ userId: 2, email: 'operador@leofit.pe', name: 'Operador Test', role: 'OPERATOR' });
  });

  it('SEC: /register sin token debe rechazarse (401) — no se permite auto-registro como ADMIN', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send({ name: 'Intruso', email: 'intruso@evil.test', password: 'Intruso2026!', role: 'ADMIN' });
    expect(res.status).toBe(401);
  });

  it('SEC: /register con un OPERATOR debe rechazarse (403)', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .set('Authorization', `Bearer ${operatorToken}`)
      .send({ name: 'Otro Operador', email: 'otro.op@leofit.pe', password: 'Password2026!' });
    expect(res.status).toBe(403);
  });
  
  it('Debe registrar un nuevo usuario y generar un token JWT', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        name: 'Lady Luz Loayza (Scrum Master)',
        email: 'scrum.master@leofit.pe',
        password: 'Password2026!',
        role: 'ADMIN'
      });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.token).toBeDefined();
    expect(res.body.data.user.email).toBe('scrum.master@leofit.pe');
  });

  it('Debe prevenir la enumeración de usuarios en el registro (400) si el correo ya existe', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        name: 'Otro Usuario',
        email: 'scrum.master@leofit.pe',
        password: 'Password2026!'
      });

    expect(res.status).toBe(400);
    expect(res.body.success).toBe(false);
    expect(res.body.error.code).toBe('REGISTRATION_FAILED');
  });

  it('Debe iniciar sesión exitosamente con credenciales válidas y retornar JWT', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'scrum.master@leofit.pe',
        password: 'Password2026!'
      });

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.token).toBeDefined();
    expect(res.body.data.user.role).toBe('ADMIN');
  });

  it('Debe rechazar el acceso con contraseña errónea (401)', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'scrum.master@leofit.pe',
        password: 'wrong_password_xyz'
      });

    expect(res.status).toBe(401);
    expect(res.body.success).toBe(false);
    expect(res.body.error.code).toBe('INVALID_CREDENTIALS');
  });

  it('Debe obtener el perfil del usuario autenticado con el token Bearer', async () => {
    // 1. Obtener token
    const loginRes = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'scrum.master@leofit.pe',
        password: 'Password2026!'
      });

    const token = loginRes.body.data.token;

    // 2. Consultar perfil
    const profileRes = await request(app)
      .get('/api/auth/profile')
      .set('Authorization', `Bearer ${token}`);

    expect(profileRes.status).toBe(200);
    expect(profileRes.body.success).toBe(true);
    expect(profileRes.body.data.email).toBe('scrum.master@leofit.pe');
  });

  it('Debe proteger rutas privadas cuando no se envía Token (401)', async () => {
    const res = await request(app).get('/api/orders');
    expect(res.status).toBe(401);
    expect(res.body.success).toBe(false);
    expect(res.body.error.code).toBe('UNAUTHORIZED');
  });

  describe('Matriz RBAC: Restricciones para rol OPERATOR (Principio de Mínimo Privilegio)', () => {
    it('OPERATOR debe tener prohibido crear nuevos productos en catálogo (403)', async () => {
      const res = await request(app)
        .post('/api/products')
        .set('Authorization', `Bearer ${operatorToken}`)
        .send({
          categoryId: 1,
          name: 'Polo Hackeado',
          basePrice: 10,
          variants: [{ size: 'M', color: 'Negro', sku: 'HACK-01', stock: 10 }]
        });
      expect(res.status).toBe(403);
      expect(res.body.error.code).toBe('INSUFFICIENT_PERMISSIONS');
    });

    it('OPERATOR debe tener prohibido modificar productos existentes (403)', async () => {
      const res = await request(app)
        .put('/api/products/1')
        .set('Authorization', `Bearer ${operatorToken}`)
        .send({ name: 'Nombre Modificado por Operador' });
      expect(res.status).toBe(403);
      expect(res.body.error.code).toBe('INSUFFICIENT_PERMISSIONS');
    });

    it('OPERATOR debe tener prohibido alterar stock base directamente (403)', async () => {
      const res = await request(app)
        .patch('/api/products/variant/1/stock')
        .set('Authorization', `Bearer ${operatorToken}`)
        .send({ stock: 50 });
      expect(res.status).toBe(403);
      expect(res.body.error.code).toBe('INSUFFICIENT_PERMISSIONS');
    });

    it('OPERATOR debe tener prohibido eliminar prendas del catálogo (403)', async () => {
      const res = await request(app)
        .delete('/api/products/1')
        .set('Authorization', `Bearer ${operatorToken}`);
      expect(res.status).toBe(403);
      expect(res.body.error.code).toBe('INSUFFICIENT_PERMISSIONS');
    });

    it('OPERATOR debe tener prohibido cancelar pedidos mediante endpoint /cancel (403)', async () => {
      const res = await request(app)
        .post('/api/orders/1/cancel')
        .set('Authorization', `Bearer ${operatorToken}`)
        .send({ reason: 'Intento de anulación por operador' });
      expect(res.status).toBe(403);
      expect(res.body.error.code).toBe('INSUFFICIENT_PERMISSIONS');
    });

    it('OPERATOR debe tener prohibido cancelar pedidos mediante status CANCELADO (403)', async () => {
      const res = await request(app)
        .patch('/api/orders/1/status')
        .set('Authorization', `Bearer ${operatorToken}`)
        .send({ status: 'CANCELADO', comments: 'Operador cancelando orden' });
      expect(res.status).toBe(403);
      expect(res.body.error.code).toBe('INSUFFICIENT_PERMISSIONS');
    });

    it('OPERATOR debe tener prohibido emitir reembolsos (403)', async () => {
      const res = await request(app)
        .post('/api/orders/1/refund')
        .set('Authorization', `Bearer ${operatorToken}`)
        .send({ reason: 'Reembolso no autorizado' });
      expect(res.status).toBe(403);
      expect(res.body.error.code).toBe('INSUFFICIENT_PERMISSIONS');
    });

    it('OPERATOR debe tener prohibido emitir notas de crédito (403)', async () => {
      const res = await request(app)
        .post('/api/orders/1/credit-note')
        .set('Authorization', `Bearer ${operatorToken}`)
        .send({ motivoCodigo: '01' });
      expect(res.status).toBe(403);
      expect(res.body.error.code).toBe('INSUFFICIENT_PERMISSIONS');
    });

    it('OPERATOR SÍ puede consultar catálogo de productos (200)', async () => {
      const res = await request(app)
        .get('/api/products')
        .set('Authorization', `Bearer ${operatorToken}`);
      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
    });

    it('OPERATOR SÍ puede consultar pedidos y métricas de dashboard (200)', async () => {
      const resOrders = await request(app)
        .get('/api/orders')
        .set('Authorization', `Bearer ${operatorToken}`);
      expect(resOrders.status).toBe(200);

      const resMetrics = await request(app)
        .get('/api/dashboard/stats')
        .set('Authorization', `Bearer ${operatorToken}`);
      expect(resMetrics.status).toBe(200);
    });

    it('OPERATOR SÍ puede registrar nuevos pedidos (201)', async () => {
      const res = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${operatorToken}`)
        .send({
          clientData: {
            fullName: 'Cliente de Operador',
            phone: '999888777',
            address: 'Av. Gamarra 500',
            district: 'La Victoria'
          },
          paymentMethod: 'YAPE',
          shippingCost: 8,
          items: [{ variantId: 1, quantity: 1, unitPrice: 49.90 }]
        });
      expect(res.status).toBe(201);
      expect(res.body.success).toBe(true);
    });

    it('OPERATOR SÍ puede actualizar estado operativo de pedidos (200)', async () => {
      const res = await request(app)
        .patch('/api/orders/1/status')
        .set('Authorization', `Bearer ${operatorToken}`)
        .send({ status: 'EN_CAMINO', comments: 'Operador despachó el pedido' });
      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
    });
  });
});

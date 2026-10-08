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
});

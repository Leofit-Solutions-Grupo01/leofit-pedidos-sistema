import request from 'supertest';
import { createApp } from '../src/app';
import { JWTService } from '../src/infrastructure/security/jwt.utils';
import { REFRESH_COOKIE_NAME } from '../src/services/auth.tokens';

describe('Ronda 7: Refresh Token Flow, Detección de Reuso y Rotación', () => {
  const app = createApp();
  let cookie: string;
  let accessToken: string;

  beforeAll(async () => {
    const bootstrapToken = JWTService.generateToken({
      userId: 1,
      email: 'admin@leofit.pe',
      name: 'Admin Bootstrap',
      role: 'ADMIN'
    });

    // Registrar usuario de prueba con contraseña conocida para la suite
    await request(app)
      .post('/api/auth/register')
      .set('Authorization', `Bearer ${bootstrapToken}`)
      .send({
        name: 'Test Refresh User',
        email: 'test.refresh@leofit.pe',
        password: 'Password2026!',
        role: 'ADMIN'
      });

    // Login inicial
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test.refresh@leofit.pe', password: 'Password2026!' });

    expect(res.status).toBe(200);
    accessToken = res.body.data.token || res.body.data.accessToken;

    const setCookieHeader = res.headers['set-cookie'];
    expect(setCookieHeader).toBeDefined();
    cookie = setCookieHeader[0].split(';')[0];
    expect(cookie).toContain(REFRESH_COOKIE_NAME);
  });

  it('GET /api/auth/me debe retornar los datos del usuario autenticado', async () => {
    const res = await request(app)
      .get('/api/auth/me')
      .set('Authorization', `Bearer ${accessToken}`);

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.email).toBe('test.refresh@leofit.pe');
    expect(res.body.data.role).toBe('ADMIN');
  });

  it('POST /api/auth/refresh rota el token y emite nuevo accessToken y nueva cookie', async () => {
    const r1 = await request(app)
      .post('/api/auth/refresh')
      .set('Cookie', cookie);

    expect(r1.status).toBe(200);
    expect(r1.body.data.accessToken).toBeDefined();

    const newSetCookie = r1.headers['set-cookie'];
    expect(newSetCookie).toBeDefined();
    const newCookie = newSetCookie[0].split(';')[0];
    expect(newCookie).not.toBe(cookie);

    // Detección de Reuso: Intentar reusar el token anterior (ya revocado)
    const r2 = await request(app)
      .post('/api/auth/refresh')
      .set('Cookie', cookie);

    expect(r2.status).toBe(401);
    expect(r2.body.error.code).toBe('REFRESH_REUSE_DETECTED');

    // Dado que se detectó reuso, toda la familia fue revocada, por lo que el nuevo token tampoco debe funcionar
    const r3 = await request(app)
      .post('/api/auth/refresh')
      .set('Cookie', newCookie);

    expect(r3.status).toBe(401);
  });

  it('POST /api/auth/logout revoca el token y limpia la cookie', async () => {
    // 1. Login nuevo
    const loginRes = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test.refresh@leofit.pe', password: 'Password2026!' });

    expect(loginRes.status).toBe(200);
    const c = loginRes.headers['set-cookie'][0].split(';')[0];

    // 2. Logout
    const logoutRes = await request(app)
      .post('/api/auth/logout')
      .set('Cookie', c);

    expect([200, 204]).toContain(logoutRes.status);

    // 3. Intento de refresh con token cerrado debe dar 401
    const refreshRes = await request(app)
      .post('/api/auth/refresh')
      .set('Cookie', c);

    expect(refreshRes.status).toBe(401);
  });

  it('Soft Delete: DELETE /api/products/:id marca deleted_at y GET retorna 410 GONE', async () => {
    // 1. Obtener listado de productos
    const listRes = await request(app).get('/api/products');
    expect(listRes.status).toBe(200);
    expect(listRes.body.data.length).toBeGreaterThan(0);
    const targetProduct = listRes.body.data[0];

    // 2. Login como admin para tener token
    const loginRes = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test.refresh@leofit.pe', password: 'Password2026!' });

    expect(loginRes.status).toBe(200);
    const adminToken = loginRes.body.data.token || loginRes.body.data.accessToken;

    // 3. Eliminar producto (soft delete)
    const deleteRes = await request(app)
      .delete(`/api/products/${targetProduct.id}`)
      .set('Authorization', `Bearer ${adminToken}`);

    expect(deleteRes.status).toBe(200);

    // 4. Consultar producto por ID debe retornar 410 GONE
    const getRes = await request(app).get(`/api/products/${targetProduct.id}`);
    expect(getRes.status).toBe(410);
    expect(getRes.body.error.code).toBe('GONE');

    // 5. El producto ya no debe figurar en el listado activo
    const updatedList = await request(app).get('/api/products');
    const ids = updatedList.body.data.map((p: any) => p.id);
    expect(ids).not.toContain(targetProduct.id);
  });
});

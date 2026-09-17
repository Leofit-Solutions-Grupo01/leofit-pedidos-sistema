// =============================================================================
// CLIENTS & DASHBOARD TESTS
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

describe('Módulo de Clientes y Métricas Dashboard (/api/clients, /api/dashboard)', () => {
  it('Debe listar los clientes registrados', async () => {
    const res = await request(app)
      .get('/api/clients')
      .set('Authorization', `Bearer ${testToken}`);

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(Array.isArray(res.body.data)).toBe(true);
    expect(res.body.data.length).toBeGreaterThan(0);
  });

  it('Debe registrar un nuevo cliente', async () => {
    const res = await request(app)
      .post('/api/clients')
      .set('Authorization', `Bearer ${testToken}`)
      .send({
        fullName: 'Rodrigo Santillán',
        phone: '955443322',
        address: 'Calle Los Cedros 321',
        district: 'Surquillo',
        reference: 'Frente al mercado'
      });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.id).toBeDefined();
    expect(res.body.data.phone).toBe('955443322');
  });

  it('Debe calcular y retornar las métricas del Dashboard (KPIs)', async () => {
    const res = await request(app)
      .get('/api/dashboard/stats')
      .set('Authorization', `Bearer ${testToken}`);

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data).toHaveProperty('totalOrders');
    expect(res.body.data).toHaveProperty('ordersByStatus');
    expect(res.body.data).toHaveProperty('totalRevenue');
    expect(res.body.data).toHaveProperty('lowStockCount');
  });
});

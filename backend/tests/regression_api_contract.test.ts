import request from 'supertest';
import { createApp } from '../src/app';
import { JWTService } from '../src/infrastructure/security/jwt.utils';

const app = createApp();
const adminToken = JWTService.generateToken({ userId: 1, email: 'admin@leofit.pe', name: 'Admin', role: 'ADMIN' });

describe('Contrato de la API: productos y clientes', () => {
  it('POST /api/products crea un producto con variantes (categoryId/basePrice en camelCase)', async () => {
    const res = await request(app)
      .post('/api/products')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({
        categoryId: 1,
        name: 'Camiseta Regresión Test',
        basePrice: 59.9,
        variants: [{ size: 'M', color: 'Negro', sku: 'LF-REG-TEST-M', stock: 7, alertThreshold: 2 }]
      });
    expect(res.status).toBe(201);
    expect(res.body.data.category_id).toBe(1);
    expect(Number(res.body.data.base_price)).toBeCloseTo(59.9);
    expect(res.body.data.variants[0].sku).toBe('LF-REG-TEST-M');
  });

  it('PUT /api/products/:id actualiza nombre y precio', async () => {
    const created = await request(app)
      .post('/api/products')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ categoryId: 2, name: 'Short Regresión', basePrice: 40, variants: [{ size: 'L', color: 'Gris', sku: 'LF-REG-SHORT-L', stock: 3 }] });
    const id = created.body.data.id;
    const res = await request(app)
      .put(`/api/products/${id}`)
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ name: 'Short Regresión Editado', basePrice: 45.5 });
    expect(res.status).toBe(200);
    expect(res.body.data.name).toBe('Short Regresión Editado');
    expect(Number(res.body.data.base_price)).toBeCloseTo(45.5);
  });

  it('POST /api/clients crea un cliente (fullName en camelCase)', async () => {
    const res = await request(app)
      .post('/api/clients')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ fullName: 'Cliente Regresión', phone: '944555666', address: 'Calle Falsa 123', district: 'Miraflores' });
    expect(res.status).toBe(201);
    expect(res.body.data.full_name).toBe('Cliente Regresión');
  });
});
// =============================================================================
// PRODUCTS & INVENTORY TESTS
// =============================================================================

import request from 'supertest';
import { createApp } from '../src/app';

const app = createApp();

describe('Módulo de Productos e Inventario (/api/products)', () => {
  it('Debe listar el catálogo público de productos con sus variantes', async () => {
    const res = await request(app).get('/api/products');
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(Array.isArray(res.body.data)).toBe(true);
    expect(res.body.data.length).toBeGreaterThan(0);
    expect(res.body.data[0]).toHaveProperty('variants');
  });

  it('Debe obtener el detalle de un producto por su ID', async () => {
    const res = await request(app).get('/api/products/1');
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.id).toBe(1);
    expect(res.body.data.name).toBeDefined();
  });

  it('Debe retornar 404 para un ID de producto inexistente', async () => {
    const res = await request(app).get('/api/products/99999');
    expect(res.status).toBe(404);
    expect(res.body.success).toBe(false);
  });
});

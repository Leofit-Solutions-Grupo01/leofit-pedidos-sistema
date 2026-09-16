// =============================================================================
// SECURITY & OWASP AUDIT TESTS - LEOFIT SECURITY
// =============================================================================

import request from 'supertest';
import { createApp } from '../src/app';

const app = createApp();

describe('Auditoría de Seguridad Web & OWASP Top 10 (/api)', () => {
  it('Debe incluir cabeceras de seguridad HTTP (Helmet)', async () => {
    const res = await request(app).get('/api/health');
    expect(res.status).toBe(200);
    expect(res.headers['x-dns-prefetch-control']).toBeDefined();
    expect(res.headers['x-content-type-options']).toBe('nosniff');
    expect(res.headers['x-frame-options']).toBe('SAMEORIGIN');
  });

  it('Debe neutralizar intentos de inyección SQL en consultas de búsqueda', async () => {
    const maliciousPayload = "' OR '1'='1; DROP TABLE users; --";
    const res = await request(app).get(`/api/products?search=${encodeURIComponent(maliciousPayload)}`);
    // Should return 200 with 0 results instead of crashing or leaking data
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(Array.isArray(res.body.data)).toBe(true);
  });

  it('Debe rechazar payloads malformados con XSS o tipos incorrectos en validación Zod', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: '<script>alert("xss")</script>',
        password: 12345 // type error
      });

    expect(res.status).toBe(400);
    expect(res.body.success).toBe(false);
    expect(res.body.error.code).toBe('VALIDATION_ERROR');
  });
});

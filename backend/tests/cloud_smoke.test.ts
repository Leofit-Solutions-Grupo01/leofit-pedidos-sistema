/**
 * @file cloud_smoke.test.ts
 * @description APF3 - Validación y verificación EN LA PLATAFORMA CLOUD (funcional + integración).
 *              Se ejecuta contra la API desplegada (Render). Se omite si CLOUD_API_URL no está definida.
 *   Uso:  CLOUD_API_URL=https://leofit-backend-api.onrender.com \
 *         CLOUD_ADMIN_EMAIL=admin@leofit.pe CLOUD_ADMIN_PASSWORD=*** npm run test:cloud
 */
const BASE = (process.env.CLOUD_API_URL || '').replace(/\/+$/, '');
const EMAIL = process.env.CLOUD_ADMIN_EMAIL;
const PASS = process.env.CLOUD_ADMIN_PASSWORD;
const d = BASE ? describe : describe.skip;

jest.setTimeout(60000); // Render free tier puede tardar en despertar (cold start)

async function call(path: string, init: RequestInit = {}) {
  const t0 = Date.now();
  const res = await fetch(`${BASE}${path}`, { ...init, headers: { 'Content-Type': 'application/json', ...(init.headers || {}) } });
  let json: any = null;
  try { json = await res.json(); } catch { /* sin JSON */ }
  return { status: res.status, json, ms: Date.now() - t0 };
}

d('APF3 Cloud: validación funcional e integración en producción', () => {
  let token = '';

  it('CL-01 /api/health responde UP y expone versión 2.x', async () => {
    const r = await call('/api/health');
    expect(r.status).toBe(200);
    expect(r.json.status).toBe('UP');
    expect(String(r.json.version)).toMatch(/^2\./);
    console.log(`[cloud] health ${r.ms} ms, db=${r.json?.database?.engine}/${r.json?.database?.status}`);
  });

  it('CL-02 la base de datos de producción es PostgreSQL (no el fallback en memoria)', async () => {
    const r = await call('/api/health');
    expect(JSON.stringify(r.json.database)).not.toMatch(/In-Memory/i);
  });

  (EMAIL && PASS ? it : it.skip)('CL-03 login real devuelve token JWT', async () => {
    const r = await call('/api/auth/login', { method: 'POST', body: JSON.stringify({ email: EMAIL, password: PASS }) });
    expect(r.status).toBe(200);
    token = r.json.data.accessToken || r.json.data.token;
    expect(token).toBeTruthy();
  });

  it('CL-04 una ruta protegida sin token es rechazada (401/403)', async () => {
    const r = await call('/api/orders');
    expect([401, 403]).toContain(r.status);
  });

  (EMAIL && PASS ? it : it.skip)('CL-05 con token se listan pedidos en < 2 s (SLO)', async () => {
    const r = await call('/api/orders', { headers: { Authorization: `Bearer ${token}` } });
    expect(r.status).toBe(200);
    expect(r.ms).toBeLessThan(2000);
  });

  it('CL-06 integración WhatsApp: valida formato de teléfono en producción', async () => {
    const bad = await call('/api/external/whatsapp/notify', { method: 'POST', body: JSON.stringify({ phone: '12345', orderCode: 'X', customerName: 'T', total: 1, status: 'Recibido' }) });
    expect(bad.status).toBe(400);
    const ok = await call('/api/external/whatsapp/notify', { method: 'POST', body: JSON.stringify({ phone: '51987654321', orderCode: 'PED-CLOUD-1', customerName: 'Prueba', total: 10, status: 'Recibido' }) });
    expect(ok.status).toBe(200);
    expect(ok.json.data.directUrl).toContain('api.whatsapp.com');
  });

  it('CL-07 webhook de pago sin firma HMAC es rechazado en producción', async () => {
    const r = await call('/api/webhooks/payments', { method: 'POST', body: JSON.stringify({ any: 'payload' }) });
    expect([400, 401, 403, 404]).toContain(r.status);
  });
});

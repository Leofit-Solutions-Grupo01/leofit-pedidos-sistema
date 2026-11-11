/**
 * @file integration_culqi_contract.test.ts
 * @description APF3 - Artefacto 2: prueba de integración REAL por HTTP contra el sistema externo Culqi.
 *              Un servidor HTTP stub (puerto efímero) reemplaza a api.culqi.com mediante CULQI_API_URL,
 *              de modo que se verifica el contrato real: método, ruta, cabecera Authorization, cuerpo JSON,
 *              manejo de errores 5xx y fallback sandbox. Herramientas: Jest + http nativo de Node.
 */
import http from 'http';
import { AddressInfo } from 'net';
import { createOrReuseCulqiCheckout } from '../src/services/payments/culqi';

interface Recibida { method?: string; url?: string; auth?: string; body: any }

let server: http.Server;
let recibidas: Recibida[] = [];
let modo: 'ok' | 'error500' = 'ok';

beforeAll(async () => {
  server = http.createServer((req, res) => {
    let raw = '';
    req.on('data', (c) => (raw += c));
    req.on('end', () => {
      recibidas.push({ method: req.method, url: req.url, auth: req.headers.authorization, body: raw ? JSON.parse(raw) : null });
      res.setHeader('Content-Type', 'application/json');
      if (modo === 'error500') { res.statusCode = 500; return res.end('{"error":"boom"}'); }
      res.end(JSON.stringify({ id: 'ord_test_123', checkout_url: 'https://checkout.culqi.com/#/order/ord_test_123' }));
    });
  });
  await new Promise<void>((r) => server.listen(0, '127.0.0.1', r));
  process.env.CULQI_API_URL = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});

afterAll(async () => {
  delete process.env.CULQI_API_URL;
  delete process.env.CULQI_SECRET_KEY;
  await new Promise<void>((r) => server.close(() => r()));
});

beforeEach(() => { recibidas = []; modo = 'ok'; });

describe('APF3 Interoperabilidad: LeoFit <-> Culqi (contrato HTTP)', () => {
  it('IC-01 envía POST /v2/orders con Bearer, moneda PEN y monto en céntimos', async () => {
    process.env.CULQI_SECRET_KEY = 'sk_test_abc';
    const r = await createOrReuseCulqiCheckout({ id: 9001, totalCents: 18990, email: 'cliente@test.pe' });
    expect(recibidas).toHaveLength(1);
    expect(recibidas[0].method).toBe('POST');
    expect(recibidas[0].url).toBe('/v2/orders');
    expect(recibidas[0].auth).toBe('Bearer sk_test_abc');
    expect(recibidas[0].body).toMatchObject({ amount: 18990, currency_code: 'PEN', order_number: 'LEO-9001' });
    expect(r.providerOrderId).toBe('ord_test_123');
    expect(r.checkoutUrl).toContain('checkout.culqi.com');
  });

  it('IC-02 propaga el fallo cuando Culqi responde 5xx (CULQI_ERROR_500)', async () => {
    process.env.CULQI_SECRET_KEY = 'sk_test_abc';
    modo = 'error500';
    await expect(createOrReuseCulqiCheckout({ id: 9002, totalCents: 5000, email: 'a@b.pe' })).rejects.toThrow('CULQI_ERROR_500');
  });

  it('IC-03 sin clave sk_ usa el fallback sandbox y NO contacta al sistema externo', async () => {
    delete process.env.CULQI_SECRET_KEY;
    const r = await createOrReuseCulqiCheckout({ id: 9003, totalCents: 5000, email: 'a@b.pe' });
    expect(recibidas).toHaveLength(0);
    expect(r.checkoutUrl).toContain('/sandbox/');
  });
});

// =============================================================================
// SUNAT & NUBEFACT INVOICING TESTS - ROUND 9 (CRITICAL HARDENING)
// CPE: Boletas (03), Facturas (01), Notas de Crédito (07), RUC Módulo 11 & Cola
// Correlativos sin gaps, Decimal.js IGV, Resumen Diario RC, Catálogo 09
// =============================================================================

import request from 'supertest';
import { createApp } from '../src/app';
import { JWTService } from '../src/infrastructure/security/jwt.utils';
import { validateRuc, NubefactService, reserveInvoiceNumber } from '../src/services/sunat/nubefact.service';
import {
  enqueueInvoice,
  processInvoiceQueue,
  memoryInvoiceQueue,
  memoryInvoices
} from '../src/jobs/emitInvoiceWorker';
import { sendDailySummary } from '../src/jobs/dailySummaryWorker';
import { splitIgv } from '../src/utils/igv';
import { transitionOrder } from '../src/services/orders/stateMachine';
import { InMemoryDataStore } from '../src/infrastructure/repositories/memory.repositories';

const app = createApp();
const adminToken = JWTService.generateToken({
  userId: 1,
  email: 'admin@leofit.pe',
  name: 'Lady Loayza',
  role: 'ADMIN'
});
const operatorToken = JWTService.generateToken({
  userId: 2,
  email: 'operador@leofit.pe',
  name: 'Carlos Operador',
  role: 'OPERATOR'
});

describe('Ronda 9 — Facturación Electrónica SUNAT (PSE Nubefact)', () => {
  beforeEach(() => {
    // Limpiar estado en memoria antes de cada prueba
    memoryInvoiceQueue.length = 0;
    memoryInvoices.length = 0;
  });

  // ───────────────────────────────────────────────────────────────────────────
  // 1. Validación de RUC (Algoritmo Módulo 11 de SUNAT)
  // ───────────────────────────────────────────────────────────────────────────
  describe('Validación de RUC Módulo 11 (SUNAT)', () => {
    it('Debe validar exitosamente un RUC oficial con Módulo 11 correcto (ej. 20100070970)', () => {
      const res = validateRuc('20100070970');
      expect(res.valid).toBe(true);
      expect(res.ruc).toBe('20100070970');
      expect(res.estado).toBe('ACTIVO');
      expect(res.condicion).toBe('HABIDO');
      expect(res.razonSocial).toContain('20100070970');
    });

    it('Debe rechazar un RUC con longitud incorrecta', () => {
      const res = validateRuc('201000709');
      expect(res.valid).toBe(false);
      expect(res.error).toMatch(/11 dígitos/i);
    });

    it('Debe rechazar un RUC con prefijo no autorizado por SUNAT', () => {
      const res = validateRuc('30100070970');
      expect(res.valid).toBe(false);
      expect(res.error).toMatch(/Prefijo.*no válido/i);
    });

    it('Debe rechazar un RUC cuyo dígito verificador no coincida con el Módulo 11', () => {
      // 20100070970 es el correcto; cambiamos el último dígito a 5
      const res = validateRuc('20100070975');
      expect(res.valid).toBe(false);
      expect(res.error).toMatch(/dígito verificador/i);
    });

    it('GET /api/sunat/ruc/:numero debe responder 200 con datos para RUC válido', async () => {
      const res = await request(app).get('/api/sunat/ruc/20100070970');
      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.valid).toBe(true);
      expect(res.body.data.estado).toBe('ACTIVO');
    });

    it('GET /api/sunat/ruc/:numero debe responder 400 con INVALID_RUC para RUC erróneo', async () => {
      const res = await request(app).get('/api/sunat/ruc/12345678901');
      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('INVALID_RUC');
    });
  });

  // ───────────────────────────────────────────────────────────────────────────
  // 2. Desglose Fiscal IGV 18% con Decimal.js (Tolerancia Cero)
  // ───────────────────────────────────────────────────────────────────────────
  describe('Cálculo de IGV con Decimal.js (Tolerancia Cero y Cuadre al Centavo)', () => {
    it('Debe cuadrar exactamente subtotal + igv === total en 20 montos aleatorios', () => {
      // 20 montos aleatorios entre S/ 5.00 y S/ 1500.00
      const testCents = [
        10000, 5990, 4999, 11800, 23600, 35400, 1500, 7555, 9999, 12345,
        8765, 54321, 98765, 1000, 50, 99, 101, 1050, 45000, 150000
      ];

      for (const cents of testCents) {
        const result = splitIgv(cents);
        const sum = Math.round((result.subtotal + result.igv) * 100);
        expect(sum).toBe(cents);
        expect(result.subtotalCents + result.igvCents).toBe(cents);
        expect(Number((result.subtotal + result.igv).toFixed(2))).toBe(result.total);
      }
    });

    it('Debe emitir una Boleta (tipo 03) con cálculo exacto de subtotal e IGV 18%', async () => {
      const cpe = await NubefactService.emitInvoice({
        orderId: 101,
        tipoComprobante: '03',
        clienteDenominacion: 'Juan Pérez',
        totalAmount: 118.00,
        items: [{ name: 'Short Deportivo LeoFit Pro', quantity: 1, unitPrice: 118.00 }]
      });

      expect(cpe.success).toBe(true);
      expect(cpe.tipo).toBe('03');
      expect(cpe.serie).toBe('BBB1');
      expect(cpe.numero).toBeGreaterThan(0);
      expect(cpe.enlace_del_pdf).toMatch(/^https:\/\/nubefact\.com\/cpe\//);
      expect(cpe.enlace_del_xml).toMatch(/\.xml$/);
      expect(cpe.codigo_hash).toBeDefined();
      expect(cpe.aceptada_por_sunat).toBe(true);
    });

    it('Debe emitir una Factura (tipo 01) con serie FFF1 para empresas con RUC', async () => {
      const cpe = await NubefactService.emitInvoice({
        orderId: 102,
        tipoComprobante: '01',
        clienteDocTipo: '6',
        clienteDocNumero: '20100070970',
        clienteDenominacion: 'CORPORACION TEXTIL S.A.C.',
        totalAmount: 236.00,
        items: [{ name: 'Lote Camisetas LeoFit', quantity: 2, unitPrice: 118.00 }]
      });

      expect(cpe.success).toBe(true);
      expect(cpe.tipo).toBe('01');
      expect(cpe.serie).toBe('FFF1');
      expect(cpe.numero).toBeGreaterThan(0);
    });
  });

  // ───────────────────────────────────────────────────────────────────────────
  // 3. Correlativos y Resumen Diario de Boletas (RC)
  // ───────────────────────────────────────────────────────────────────────────
  describe('Correlativos sin gaps y Resumen Diario (RC)', () => {
    it('reserveInvoiceNumber reserva correlativos secuenciales sin repeticiones', async () => {
      const n1 = await reserveInvoiceNumber(null, '03', 'BBB1');
      const n2 = await reserveInvoiceNumber(null, '03', 'BBB1');
      expect(n2).toBe(n1 + 1);
    });

    it('sendDailySummary no arroja errores y maneja envíos consolidados', async () => {
      const result = await sendDailySummary();
      expect(result).toBeDefined();
      expect(result.count).toBeGreaterThanOrEqual(0);
    });
  });

  // ───────────────────────────────────────────────────────────────────────────
  // 4. Flujo Asíncrono: Transición a PAGADO -> Cola -> Worker
  // ───────────────────────────────────────────────────────────────────────────
  describe('Cola Asíncrona de Emisión (invoice_queue & Worker)', () => {
    it('Al transicionar una orden a PAGADO, se encola automáticamente un trabajo de facturación', async () => {
      const testOrder = InMemoryDataStore.orders[0];
      expect(testOrder).toBeDefined();
      testOrder.status = 'RECIBIDO' as any;
      (testOrder as any).estado = 'PENDIENTE';

      const transitionResult = await transitionOrder(null, testOrder.id, 'PAGADO', 'webhook:culqi', {
        tipoComprobante: '03'
      });

      expect(transitionResult.to).toBe('PAGADO');

      const enqueued = memoryInvoiceQueue.find((q) => q.orderId === testOrder.id);
      expect(enqueued).toBeDefined();
      expect(enqueued?.estado).toBe('PENDING');
      expect(enqueued?.tipo).toBe('03');
    });

    it('El worker processInvoiceQueue() procesa la cola y emite el comprobante en memoria', async () => {
      const testOrder = InMemoryDataStore.orders[0];
      testOrder.status = 'PAGADO' as any;
      (testOrder as any).estado = 'PAGADO';

      await enqueueInvoice(testOrder.id, '03', { clienteNombre: 'Cliente Test' });

      expect(memoryInvoiceQueue.length).toBeGreaterThan(0);

      const processedCount = await processInvoiceQueue();
      expect(processedCount).toBeGreaterThanOrEqual(1);

      const job = memoryInvoiceQueue.find((q) => q.orderId === testOrder.id);
      expect(job?.estado).toBe('COMPLETED');

      const invoice = memoryInvoices.find((i) => i.orderId === testOrder.id);
      expect(invoice).toBeDefined();
      expect(invoice?.estado).toBe('ACEPTADO');
      expect(invoice?.serie).toBe('BBB1');
      expect(invoice?.pdfUrl).toBeDefined();
      expect(invoice?.hashSunat).toBeDefined();
    });

    it('Si un pedido fue cancelado antes de emitir, la tarea en cola queda en SKIPPED y no emite', async () => {
      const testOrder = InMemoryDataStore.orders[1] || InMemoryDataStore.orders[0];
      (testOrder as any).estado = 'CANCELADO';
      testOrder.status = 'CANCELADO' as any;

      await enqueueInvoice(testOrder.id, '03');

      const processedCount = await processInvoiceQueue();
      const job = memoryInvoiceQueue.find((q) => q.orderId === testOrder.id);
      expect(job?.estado).toBe('SKIPPED');
      expect(job?.lastError).toBe('ORDER_CANCELLED_BEFORE_EMISSION');

      // No debe haberse emitido en memoria
      const invoice = memoryInvoices.find((i) => i.orderId === testOrder.id && i.estado === 'ACEPTADO');
      expect(invoice).toBeUndefined();
    });
  });

  // ───────────────────────────────────────────────────────────────────────────
  // 5. Endpoints de Consulta, Descarga y Nota de Crédito (Catálogo 09)
  // ───────────────────────────────────────────────────────────────────────────
  describe('Endpoints /api/invoices y /api/orders/:id/credit-note', () => {
    let emittedOrderId: number;
    let emittedInvoiceId: number;

    beforeEach(async () => {
      const testOrder = InMemoryDataStore.orders[0];
      (testOrder as any).estado = 'PAGADO';
      testOrder.status = 'PAGADO' as any;
      emittedOrderId = testOrder.id;

      await enqueueInvoice(emittedOrderId, '03');
      await processInvoiceQueue();

      const inv = memoryInvoices.find((i) => i.orderId === emittedOrderId);
      if (inv) {
        emittedInvoiceId = inv.id;
      }
    });

    it('GET /api/invoices/order/:orderId retorna el comprobante electrónico emitido', async () => {
      const res = await request(app).get(`/api/invoices/order/${emittedOrderId}`);
      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.orderId).toBe(emittedOrderId);
      expect(res.body.data.estado).toBe('ACEPTADO');
      expect(res.body.data.hashSunat).toBeDefined();
    });

    it('GET /api/invoices/order/999999 responde 404 con INVOICE_NOT_FOUND', async () => {
      const res = await request(app).get('/api/invoices/order/999999');
      expect(res.status).toBe(404);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('INVOICE_NOT_FOUND');
    });

    it('GET /api/invoices/:id/pdf redirige a la URL oficial del PDF', async () => {
      const res = await request(app).get(`/api/invoices/${emittedInvoiceId}/pdf`);
      expect(res.status).toBe(302);
      expect(res.headers.location).toMatch(/^https:\/\/nubefact\.com\/cpe\//);
    });

    it('GET /api/invoices/:id/xml redirige a la URL oficial del XML', async () => {
      const res = await request(app).get(`/api/invoices/${emittedInvoiceId}/xml`);
      expect(res.status).toBe(302);
      expect(res.headers.location).toMatch(/\.xml$/);
    });

    it('POST /api/orders/:id/credit-note rechaza llamadas sin token de autenticación (401)', async () => {
      const res = await request(app).post(`/api/orders/${emittedOrderId}/credit-note`).send({});
      expect(res.status).toBe(401);
    });

    it('POST /api/orders/:id/credit-note rechaza llamadas de usuarios con rol OPERATOR (403)', async () => {
      const res = await request(app)
        .post(`/api/orders/${emittedOrderId}/credit-note`)
        .set('Authorization', `Bearer ${operatorToken}`)
        .send({ reasonCode: '01', reasonDescription: 'Anulación de la operación' });
      expect(res.status).toBe(403);
    });

    it('POST /api/orders/:id/credit-note rechaza motivos inválidos fuera del Catálogo 09 de SUNAT (400)', async () => {
      const res = await request(app)
        .post(`/api/orders/${emittedOrderId}/credit-note`)
        .set('Authorization', `Bearer ${adminToken}`)
        .send({
          reasonCode: '99', // Código inválido
          reasonDescription: 'Motivo inventado'
        });

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('INVALID_MOTIVO');
    });

    it('POST /api/orders/:id/credit-note emite Nota de Crédito (tipo 07) si el motivo es válido (Catálogo 09)', async () => {
      const res = await request(app)
        .post(`/api/orders/${emittedOrderId}/credit-note`)
        .set('Authorization', `Bearer ${adminToken}`)
        .send({
          reasonCode: '01',
          reasonDescription: 'Reembolso total y anulación del pedido'
        });

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.tipo).toBe('07');
      expect(res.body.data.serie).toBe('BC01'); // Nota de crédito para boleta BBB1
      expect(res.body.data.aceptada_por_sunat).toBe(true);

      const nc = memoryInvoices.find((i) => i.orderId === emittedOrderId && i.tipo === '07');
      expect(nc).toBeDefined();
      expect(nc?.estado).toBe('ACEPTADO');
    });

    it('POST /api/orders/:id/credit-note responde 404 si la orden no tiene factura/boleta previa aceptada', async () => {
      const res = await request(app)
        .post('/api/orders/999999/credit-note')
        .set('Authorization', `Bearer ${adminToken}`)
        .send({ reasonCode: '01' });

      expect(res.status).toBe(404);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('ORIGINAL_INVOICE_NOT_FOUND');
    });
  });
});

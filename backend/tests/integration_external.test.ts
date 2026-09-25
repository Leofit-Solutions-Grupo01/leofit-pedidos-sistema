/**
 * @file integration_external.test.ts
 * @description Suite de Pruebas de Integración y Servicios Externos (APF3 Criterio 2)
 * @rubric APF3 Criterio 2: Automatización de Pruebas de Integración (6 artefactos)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 */

import request from 'supertest';
import { createApp } from '../src/app';

const app = createApp();

describe('APF3: Pruebas de Integración e Interoperabilidad con Servicios Externos', () => {

  describe('Sistema Externo 1: WhatsApp Cloud API & Notificaciones de Tracking', () => {
    it('debe interoperar con WhatsApp Gateway enviando notificación de pedido y enlace de tracking', async () => {
      const payload = {
        phone: '51987654321',
        orderCode: 'PED-2026-089',
        customerName: 'Víctor Cárdenas',
        total: 189.90,
        status: 'En Preparación'
      };

      const res = await request(app)
        .post('/api/external/whatsapp/notify')
        .send(payload);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.delivered).toBe(true);
      expect(res.body.data.directUrl).toContain('https://api.whatsapp.com/send');
      expect(res.body.data.messagePreview).toContain('PED-2026-089');
    });

    it('debe rechazar números telefónicos que no cumplan el formato internacional peruano (519XXXXXXXX)', async () => {
      const invalidPayload = {
        phone: '12345',
        orderCode: 'PED-2026-089',
        customerName: 'Víctor Cárdenas',
        total: 189.90,
        status: 'En Preparación'
      };

      const res = await request(app)
        .post('/api/external/whatsapp/notify')
        .send(invalidPayload);

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
    });
  });

  describe('Sistema Externo 2: Pasarela de Pagos (Yape / Plin / Mercado Pago)', () => {
    it('debe recibir y conciliar el webhook de pago aprobado generando código de conciliación fiscal', async () => {
      const webhookPayload = {
        provider: 'YAPE',
        transactionId: 'TX-YAPE-9823412',
        orderCode: 'PED-2026-089',
        amount: 189.90,
        status: 'APPROVED'
      };

      const res = await request(app)
        .post('/api/external/payments/webhook')
        .send(webhookPayload);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.reconciliationId).toMatch(/^REC-/);
      expect(res.body.data.status).toBe('APPROVED');
      expect(res.body.data.fiscalReceiptReady).toBe(true);
    });

    it('debe rechazar el procesamiento si el proveedor de pagos no está homologado', async () => {
      const invalidWebhook = {
        provider: 'CRYPTO_UNSUPPORTED',
        transactionId: 'TX-000',
        orderCode: 'PED-2026-089',
        amount: 189.90,
        status: 'APPROVED'
      };

      const res = await request(app)
        .post('/api/external/payments/webhook')
        .send(invalidWebhook);

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
    });
  });

  describe('Sistema Externo 3: Padrón de Identidad SUNAT & RENIEC', () => {
    it('debe validar un DNI de 8 dígitos ante el servicio mock de RENIEC y retornar datos del titular', async () => {
      const res = await request(app)
        .post('/api/external/identity/lookup')
        .send({ type: 'DNI', number: '72345678' });

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.entity).toBe('RENIEC');
      expect(res.body.data.isValid).toBe(true);
      expect(res.body.data.fullName).toBeDefined();
    });

    it('debe validar un RUC comercial de 11 dígitos ante el servicio mock de SUNAT y verificar condición HABIDO', async () => {
      const res = await request(app)
        .post('/api/external/identity/lookup')
        .send({ type: 'RUC', number: '20601234567' });

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.entity).toBe('SUNAT');
      expect(res.body.data.condition).toBe('HABIDO');
      expect(res.body.data.status).toBe('ACTIVO');
    });

    it('debe rechazar consultas con documentos malformados', async () => {
      const res = await request(app)
        .post('/api/external/identity/lookup')
        .send({ type: 'DNI', number: 'ABC' });

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
    });
  });

});

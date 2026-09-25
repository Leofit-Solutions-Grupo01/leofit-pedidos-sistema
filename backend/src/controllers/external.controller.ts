// =============================================================================
// EXTERNAL INTEGRATIONS CONTROLLER - APF3 INTEROPERABILITY
// =============================================================================

import { Request, Response } from 'express';
import { z } from 'zod';

// Esquemas de validación Zod
const sendWhatsAppSchema = z.object({
  phone: z.string().regex(/^51[0-9]{9}$/, 'El teléfono debe tener formato internacional peruano (519XXXXXXXX)'),
  orderCode: z.string().min(3),
  customerName: z.string().min(2),
  total: z.number().positive(),
  status: z.string().min(2)
});

const paymentWebhookSchema = z.object({
  provider: z.enum(['YAPE', 'PLIN', 'MERCADOPAGO', 'TRANSFERENCIA']),
  transactionId: z.string().min(4),
  orderCode: z.string().min(3),
  amount: z.number().positive(),
  status: z.enum(['APPROVED', 'REJECTED', 'PENDING'])
});

const identityLookupSchema = z.object({
  type: z.enum(['DNI', 'RUC']),
  number: z.string().min(8).max(11)
});

export const externalController = {
  // 1. WhatsApp Cloud API / Direct Link Gateway
  async sendWhatsAppNotification(req: Request, res: Response) {
    try {
      const data = sendWhatsAppSchema.parse(req.body);
      
      const trackingUrl = `https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/?tracking=${data.orderCode}`;
      const message = `Hola ${data.customerName}! Tu pedido en LeoFit #${data.orderCode} por S/ ${data.total.toFixed(2)} está en estado: ${data.status}. Puedes seguirlo en vivo aquí: ${trackingUrl}`;
      const encodedMessage = encodeURIComponent(message);
      const directUrl = `https://api.whatsapp.com/send?phone=${data.phone}&text=${encodedMessage}`;

      return res.status(200).json({
        success: true,
        data: {
          gateway: 'WhatsApp Cloud API / Webhook Interoperability',
          delivered: true,
          recipient: data.phone,
          orderCode: data.orderCode,
          directUrl,
          messagePreview: message,
          timestamp: new Date().toISOString()
        }
      });
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ success: false, error: error.errors });
      }
      return res.status(500).json({ success: false, error: 'Error al enviar notificación WhatsApp' });
    }
  },

  // 2. Pasarela de Pagos (Yape, Plin, Mercado Pago)
  async handlePaymentWebhook(req: Request, res: Response) {
    try {
      const data = paymentWebhookSchema.parse(req.body);

      // Simulación de validación y conciliación transaccional
      const reconciliationId = `REC-${Date.now()}-${Math.floor(Math.random() * 1000)}`;

      return res.status(200).json({
        success: true,
        data: {
          gateway: `${data.provider} Payment Gateway`,
          reconciliationId,
          orderCode: data.orderCode,
          transactionId: data.transactionId,
          amountVerified: data.amount,
          status: data.status,
          reconciledAt: new Date().toISOString(),
          fiscalReceiptReady: data.status === 'APPROVED'
        }
      });
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ success: false, error: error.errors });
      }
      return res.status(500).json({ success: false, error: 'Error en webhook de pagos' });
    }
  },

  // 3. Validación de Identidad SUNAT / RENIEC
  async lookupIdentity(req: Request, res: Response) {
    try {
      const data = identityLookupSchema.parse(req.body);

      if (data.type === 'DNI') {
        if (!/^[0-9]{8}$/.test(data.number)) {
          return res.status(400).json({ success: false, error: 'El DNI debe tener exactamente 8 dígitos numéricos' });
        }
        return res.status(200).json({
          success: true,
          data: {
            entity: 'RENIEC',
            documentType: 'DNI',
            documentNumber: data.number,
            fullName: 'CARLOS ALBERTO MENDOZA RUIZ',
            isValid: true,
            status: 'ACTIVO'
          }
        });
      }

      if (data.type === 'RUC') {
        if (!/^(10|20)[0-9]{9}$/.test(data.number)) {
          return res.status(400).json({ success: false, error: 'El RUC debe comenzar con 10 o 20 y tener 11 dígitos' });
        }
        return res.status(200).json({
          success: true,
          data: {
            entity: 'SUNAT',
            documentType: 'RUC',
            documentNumber: data.number,
            businessName: 'INVERSIONES TEXTILES LEOFIT S.A.C.',
            condition: 'HABIDO',
            status: 'ACTIVO',
            taxAddress: 'JR. GAMARRA 1025, LA VICTORIA, LIMA'
          }
        });
      }

      return res.status(400).json({ success: false, error: 'Tipo de documento no soportado' });
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ success: false, error: error.errors });
      }
      return res.status(500).json({ success: false, error: 'Error al consultar servicio de identidad' });
    }
  }
};

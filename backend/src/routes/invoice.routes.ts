/**
 * @file invoice.routes.ts
 * @description Rutas para consulta de Comprobantes de Pago Electrónicos (Boletas, Facturas, Notas de Crédito).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import { Router } from 'express';
import { InvoiceController } from '../controllers/invoice.controller';
import { authenticateToken } from '../middlewares/auth.middleware';
import { requireRole } from '../middlewares/role.middleware';
import { audit } from '../middlewares/audit.middleware';

const router = Router();

// Consulta pública / cliente de comprobante por ID de orden
router.get('/order/:orderId', InvoiceController.getByOrderId);

// Descarga o redirección de archivos oficiales
router.get('/:id/pdf', InvoiceController.getPdf);
router.get('/:id/xml', InvoiceController.getXml);

// Emisión administrativa de Nota de Crédito
router.post(
  '/order/:id/credit-note',
  authenticateToken,
  requireRole('ADMIN'),
  audit('CREDIT_NOTE', 'order'),
  InvoiceController.emitCreditNote
);

export default router;

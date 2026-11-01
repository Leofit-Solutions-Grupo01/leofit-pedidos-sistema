/**
 * @file webhook.routes.ts
 * @description Rutas para recepción de Webhooks de proveedores de pagos sin autenticación JWT (validación por HMAC).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import { Router } from 'express';
import { handleWebhook } from '../controllers/paymentWebhook.controller';

const router = Router();

// POST /api/webhooks/:provider (ej: /api/webhooks/culqi)
router.post('/:provider', handleWebhook);

export default router;

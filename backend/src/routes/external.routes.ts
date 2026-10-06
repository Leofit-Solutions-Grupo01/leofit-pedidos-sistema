// =============================================================================
// EXTERNAL INTEGRATION ROUTES - APF3
// =============================================================================

import { Router } from 'express';
import express from 'express';
import { externalController } from '../controllers/external.controller';

const router = Router();

// Endpoint 1: Notificación WhatsApp
router.post('/whatsapp/notify', externalController.sendWhatsAppNotification);

// Endpoint 2: Conciliación Pasarela de Pagos
// (Webhook montado en app.ts para capturar rawBody correctamente)

// Endpoint 3: Verificación RENIEC / SUNAT
router.post('/identity/lookup', externalController.lookupIdentity);

export default router;

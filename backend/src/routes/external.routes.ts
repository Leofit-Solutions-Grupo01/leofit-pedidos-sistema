// =============================================================================
// EXTERNAL INTEGRATION ROUTES - APF3
// =============================================================================

import { Router } from 'express';
import { externalController } from '../controllers/external.controller';

const router = Router();

// Endpoint 1: Notificación WhatsApp
router.post('/whatsapp/notify', externalController.sendWhatsAppNotification);

// Endpoint 2: Conciliación Pasarela de Pagos
router.post('/payments/webhook', externalController.handlePaymentWebhook);

// Endpoint 3: Verificación RENIEC / SUNAT
router.post('/identity/lookup', externalController.lookupIdentity);

export default router;

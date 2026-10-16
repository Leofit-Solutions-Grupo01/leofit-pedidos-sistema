// =============================================================================
// ORDER MANAGEMENT ROUTES - /api/orders
// =============================================================================

import { Router } from 'express';
import { OrderController } from '../controllers/order.controller';
import { refundOrder } from '../controllers/refund.controller';
import { authenticateToken } from '../middlewares/auth.middleware';
import { idempotencyMiddleware } from '../middlewares/idempotency.middleware';
import { validateBody } from '../middlewares/validate.middleware';
import { paymentLinkLimiter } from '../middlewares/rateLimit.middleware';
import { requireRole } from '../middlewares/role.middleware';
import { audit } from '../middlewares/audit.middleware';
import { CreateOrderSchema, UpdateOrderStatusSchema } from '../infrastructure/validators/schemas';

const router = Router();

// Order tracking by public order number (Customer self-service tracking)
router.get('/track/:orderNumber', OrderController.getOrderByNumber);

// Protected order processing (ADMIN / OPERATOR)
router.get('/', authenticateToken, OrderController.listOrders);
router.get('/:id', authenticateToken, OrderController.getOrderById);
router.post('/', authenticateToken, idempotencyMiddleware, validateBody(CreateOrderSchema), OrderController.createOrder);
router.patch('/:id/status', authenticateToken, validateBody(UpdateOrderStatusSchema), OrderController.updateOrderStatus);
router.post('/:id/cancel', authenticateToken, OrderController.cancelOrder);
router.post('/:id/payment-link', authenticateToken, paymentLinkLimiter, OrderController.getPaymentLink);
router.post('/:id/refund', authenticateToken, requireRole('ADMIN'), audit('REFUND', 'order'), refundOrder);

export default router;


// =============================================================================
// ORDER MANAGEMENT ROUTES - /api/orders
// =============================================================================

import { Router } from 'express';
import { OrderController } from '../controllers/order.controller';
import { authenticateToken } from '../middlewares/auth.middleware';
import { validateBody } from '../middlewares/validate.middleware';
import { CreateOrderSchema, UpdateOrderStatusSchema } from '../infrastructure/validators/schemas';

const router = Router();

// Order tracking by public order number (Customer self-service tracking)
router.get('/track/:orderNumber', OrderController.getOrderByNumber);

// Protected order processing (ADMIN / OPERATOR)
router.get('/', authenticateToken, OrderController.listOrders);
router.get('/:id', authenticateToken, OrderController.getOrderById);
router.post('/', authenticateToken, validateBody(CreateOrderSchema), OrderController.createOrder);
router.patch('/:id/status', authenticateToken, validateBody(UpdateOrderStatusSchema), OrderController.updateOrderStatus);
router.post('/:id/cancel', authenticateToken, OrderController.cancelOrder);

export default router;

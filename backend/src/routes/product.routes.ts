// =============================================================================
// PRODUCT & INVENTORY ROUTES - /api/products
// =============================================================================

import { Router } from 'express';
import { ProductController } from '../controllers/product.controller';
import { authenticateToken } from '../middlewares/auth.middleware';
import { requireRole } from '../middlewares/role.middleware';
import { validateBody } from '../middlewares/validate.middleware';
import { CreateProductSchema, UpdateProductSchema, StockUpdateSchema } from '../infrastructure/validators/schemas';

const router = Router();

// Public catalog retrieval con Cache-Control explícito (Edge & Browser Caching)
router.get('/', (req, res, next) => {
  res.setHeader('Cache-Control', 'public, max-age=60, stale-while-revalidate=120');
  next();
}, ProductController.listProducts);

router.get('/alerts/low-stock', authenticateToken, ProductController.getLowStockAlerts);

router.get('/:id', (req, res, next) => {
  res.setHeader('Cache-Control', 'public, max-age=60, stale-while-revalidate=120');
  next();
}, ProductController.getProductById);

// Protected inventory management (ADMIN / OPERATOR)
router.post('/', authenticateToken, requireRole('ADMIN'), validateBody(CreateProductSchema), ProductController.createProduct);
router.put('/:id', authenticateToken, requireRole('ADMIN'), validateBody(UpdateProductSchema), ProductController.updateProduct);
router.patch('/variant/:variantId/stock', authenticateToken, validateBody(StockUpdateSchema), ProductController.updateStock);
router.delete('/:id', authenticateToken, requireRole('ADMIN'), ProductController.deleteProduct);

export default router;

// =============================================================================
// MAIN ROUTE AGGREGATOR - API VERSION 1 & 2
// =============================================================================

import { Router } from 'express';
import authRoutes from './auth.routes';
import productRoutes from './product.routes';
import orderRoutes from './order.routes';
import clientRoutes from './client.routes';
import { dashboardRouter, healthRouter } from './dashboard.routes';

const router = Router();

router.use('/health', healthRouter);
router.use('/auth', authRoutes);
router.use('/products', productRoutes);
router.use('/orders', orderRoutes);
router.use('/clients', clientRoutes);
router.use('/dashboard', dashboardRouter);

export default router;

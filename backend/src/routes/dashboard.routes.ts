// =============================================================================
// DASHBOARD & HEALTH ROUTES
// =============================================================================

import { Router } from 'express';
import { DashboardController } from '../controllers/dashboard.controller';
import { HealthController } from '../controllers/health.controller';
import { authenticateToken } from '../middlewares/auth.middleware';

export const dashboardRouter = Router();
dashboardRouter.get('/stats', authenticateToken, DashboardController.getMetrics);
dashboardRouter.get('/activity', authenticateToken, DashboardController.getRecentActivity);

export const healthRouter = Router();
healthRouter.get('/', HealthController.check);

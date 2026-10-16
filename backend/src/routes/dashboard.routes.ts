// =============================================================================
// DASHBOARD & HEALTH ROUTES
// =============================================================================

import { Router } from 'express';
import { DashboardController } from '../controllers/dashboard.controller';
import { HealthController } from '../controllers/health.controller';
import { authenticateToken } from '../middlewares/auth.middleware';
import { readyHealthRateLimiter } from '../middlewares/rateLimit.middleware';
import { cleanupExpiredIdempotencyKeys } from '../middlewares/idempotency.middleware';

export const dashboardRouter = Router();
dashboardRouter.get('/stats', authenticateToken, DashboardController.getMetrics);
dashboardRouter.get('/activity', authenticateToken, DashboardController.getRecentActivity);

export const healthRouter = Router();
healthRouter.get('/', HealthController.check);
healthRouter.get('/live', HealthController.liveness);
healthRouter.get('/ready', readyHealthRateLimiter, HealthController.readiness);

/**
 * Endpoint de mantenimiento invocado por cron jobs externos (Render Cron / GitHub Actions / cron-job.org).
 * Protegido por secreto administrativo (ADMIN_CLEANUP_SECRET) o Bearer token de admin.
 */
healthRouter.post('/cleanup-idempotency', async (req, res) => {
  const secret = process.env.ADMIN_CLEANUP_SECRET || 'leofit_internal_cleanup_secret';
  const provided = req.headers['x-admin-secret'] || req.query.secret;

  if (provided !== secret) {
    res.status(403).json({ success: false, error: 'Acceso no autorizado al endpoint de mantenimiento.' });
    return;
  }

  const deleted = await cleanupExpiredIdempotencyKeys();
  res.status(200).json({
    success: true,
    deletedKeys: deleted,
    timestamp: new Date().toISOString()
  });
});

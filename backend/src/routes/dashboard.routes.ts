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
 * Protegido estrictamente por cabeceras (Authorization: Bearer <CRON_SECRET> o X-Admin-Secret).
 * Nunca admite secretos en query parameters (?secret=...) para evitar filtraciones en logs y proxys.
 */
healthRouter.post('/cleanup-idempotency', async (req, res) => {
  const secret = process.env.ADMIN_CLEANUP_SECRET || 'leofit_internal_cleanup_secret';
  
  const authHeader = req.headers.authorization;
  const bearerToken = authHeader && authHeader.startsWith('Bearer ') ? authHeader.split(' ')[1] : null;
  const adminSecretHeader = req.headers['x-admin-secret'];

  const providedSecret = bearerToken || adminSecretHeader;

  if (!providedSecret || providedSecret !== secret) {
    res.status(401).json({
      success: false,
      error: {
        code: 'UNAUTHORIZED_MAINTENANCE',
        message: 'Acceso no autorizado. Se requiere cabecera Authorization: Bearer <CRON_SECRET> o X-Admin-Secret.'
      }
    });
    return;
  }

  const deleted = await cleanupExpiredIdempotencyKeys();
  res.status(200).json({
    success: true,
    deletedKeys: deleted,
    timestamp: new Date().toISOString()
  });
});

/**
 * @file audit.middleware.ts
 * @description Middleware para registro de auditoría de administradores (OWASP A09).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import { Request, Response, NextFunction } from 'express';
import { dbPool, isPostgresAvailable } from '../config/database';
import { logger } from '../utils/logger';

export function audit(action: string, resourceType: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const originalJson = res.json.bind(res);

    res.json = (body: any) => {
      if (res.statusCode >= 200 && res.statusCode < 300) {
        const userId = (req as any).user?.userId || (req as any).user?.id || null;
        const resourceId = body?.data?.id || req.params.id || null;
        const correlationId = (req as any).correlationId || req.headers['x-correlation-id'] || null;
        const ip = req.ip || req.socket.remoteAddress || null;
        const userAgent = req.headers['user-agent'] || null;

        if (isPostgresAvailable()) {
          dbPool.query(
            `INSERT INTO audit_log
               (user_id, action, resource_type, resource_id, after_state, ip, user_agent, correlation_id)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
            [
              userId,
              action,
              resourceType,
              resourceId ? String(resourceId) : null,
              JSON.stringify(body?.data || {}),
              ip,
              userAgent,
              correlationId
            ]
          ).catch((err) => {
            logger.error('[Audit Log Error] Falló el registro de auditoría:', { error: err.message });
          });
        }
      }
      return originalJson(body);
    };

    next();
  };
}

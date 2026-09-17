/**
 * @file role.middleware.ts
 * @description Middleware de Control de Acceso Basado en Roles (RBAC - Role-Based Access Control).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Función:
 * - Implementa el principio de privilegio mínimo (Principle of Least Privilege).
 * - Restringe el acceso a endpoints críticos a los roles autorizados (ej: 'ADMIN').
 * - Previene vulnerabilidades OWASP A01 (Broken Access Control).
 */

import { Response, NextFunction } from 'express';
import { AuthenticatedRequest } from './auth.middleware';
import { UserRole } from '../domain/entities/models';

/**
 * Genera un middleware que verifica si el usuario autenticado posee alguno de los roles permitidos.
 * @param allowedRoles Lista de roles con permiso de ejecución
 */
export function requireRole(...allowedRoles: UserRole[]) {
  return (req: AuthenticatedRequest, res: Response, next: NextFunction): void => {
    if (!req.user) {
      res.status(401).json({
        success: false,
        error: { code: 'UNAUTHORIZED', message: 'Usuario no autenticado en el sistema.' }
      });
      return;
    }

    if (!allowedRoles.includes(req.user.role)) {
      res.status(403).json({
        success: false,
        error: {
          code: 'INSUFFICIENT_PERMISSIONS',
          message: `Acceso restringido. Se requiere uno de los siguientes roles: [${allowedRoles.join(', ')}]. Su rol actual es: ${req.user.role}`
        }
      });
      return;
    }

    next();
  };
}

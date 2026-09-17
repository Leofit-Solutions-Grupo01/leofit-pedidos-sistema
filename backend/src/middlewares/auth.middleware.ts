/**
 * @file auth.middleware.ts
 * @description Middleware de Autenticación Basado en Tokens JWT (JSON Web Tokens).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Función:
 * - Extrae el token Bearer del header `Authorization`.
 * - Valida la firma criptográfica HMAC-SHA256 y la fecha de expiración.
 * - Inyecta el payload del usuario autenticado en el objeto `req.user`.
 * - Retorna HTTP 401 (Unauthorized) si no se provee token o HTTP 403 (Forbidden) si el token es inválido o expiró.
 */

import { Request, Response, NextFunction } from 'express';
import { JWTService, JWTPayload } from '../infrastructure/security/jwt.utils';

/**
 * Extensión de la interfaz de Request de Express para contener los datos del usuario verificado.
 */
export interface AuthenticatedRequest extends Request {
  user?: JWTPayload;
}

/**
 * Middleware para validar la autenticidad y vigencia del token de sesión.
 */
export function authenticateToken(req: AuthenticatedRequest, res: Response, next: NextFunction): void {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.startsWith('Bearer ') ? authHeader.split(' ')[1] : null;

  if (!token) {
    res.status(401).json({
      success: false,
      error: {
        code: 'UNAUTHORIZED',
        message: 'Acceso no autorizado. Se requiere la cabecera Authorization: Bearer <token>'
      }
    });
    return;
  }

  const payload = JWTService.verifyToken(token);
  if (!payload) {
    res.status(403).json({
      success: false,
      error: {
        code: 'FORBIDDEN',
        message: 'Token de sesión inválido o expirado. Inicie sesión nuevamente.'
      }
    });
    return;
  }

  req.user = payload;
  next();
}

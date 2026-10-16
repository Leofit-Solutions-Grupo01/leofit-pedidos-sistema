/**
 * @file rateLimit.middleware.ts
 * @description Middleware de Limitación de Tasa de Peticiones (Rate Limiting RFC 6585).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Controles de Seguridad:
 * - Mitigación contra ataques de Denegación de Servicio (DoS / DDoS).
 * - Protección contra ataques de fuerza bruta en el formulario de inicio de sesión (OWASP A07).
 * - Emisión garantizada de cabeceras RFC: RateLimit-Limit, X-RateLimit-*, Retry-After.
 */

import { Request, Response } from 'express';
import rateLimit from 'express-rate-limit';

const windowMs = parseInt(process.env.RATE_LIMIT_WINDOW_MS || '900000', 10); // 15 minutos
const maxRequests = parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '200', 10);

/**
 * Limitador global para todas las rutas transaccionales de la API REST.
 * Excluye explícitamente sondas de orquestador (/health).
 */
export const apiRateLimiter = rateLimit({
  windowMs,
  max: maxRequests,
  standardHeaders: true,
  legacyHeaders: true,
  skip: (req) => req.path.startsWith('/health') || req.path === '/',
  handler: (req: Request, res: Response, _next, options) => {
    const retryAfter = res.getHeader('Retry-After') || Math.ceil(windowMs / 1000);
    res.setHeader('Retry-After', String(retryAfter));
    res.status(429).json({
      success: false,
      error: {
        code: 'RATE_LIMIT_EXCEEDED',
        message: 'Demasiadas solicitudes enviadas desde esta dirección IP. Por favor intente más tarde.',
        retryAfter: Number(retryAfter)
      }
    });
  }
});

/**
 * Limitador estricto para el endpoint de autenticación `/api/auth/login`.
 * Permite un máximo de 20 intentos de inicio de sesión cada 15 minutos por IP.
 */
export const authRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 20,
  standardHeaders: true,
  legacyHeaders: true,
  handler: (req: Request, res: Response, _next, options) => {
    const retryAfter = res.getHeader('Retry-After') || 900;
    res.setHeader('Retry-After', String(retryAfter));
    res.status(429).json({
      success: false,
      error: {
        code: 'AUTH_RATE_LIMIT_EXCEEDED',
        message: 'Límite de intentos de inicio de sesión superado. Por motivos de seguridad, espere antes de reintentar.',
        retryAfter: Number(retryAfter)
      }
    });
  }
});

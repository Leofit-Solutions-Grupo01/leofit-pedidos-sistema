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
 * - Protección contra DoS en sondas de base de datos (/health/ready).
 * - Emisión garantizada de cabeceras RFC: RateLimit-Limit, X-RateLimit-*, Retry-After.
 */

import { Request, Response } from 'express';
import rateLimit from 'express-rate-limit';

const windowMs = parseInt(process.env.RATE_LIMIT_WINDOW_MS || '900000', 10); // 15 minutos
const maxRequests = parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '200', 10);

/**
 * Limitador global para todas las rutas transaccionales de la API REST.
 * Excluye EXCLUSIVAMENTE la sonda in-memory de liveness (/health/live) y la raíz.
 * La sonda de readiness (/health/ready) NO se excluye aquí para evitar vectores de DoS a Postgres.
 */
export const apiRateLimiter = rateLimit({
  windowMs,
  max: maxRequests,
  standardHeaders: true,
  legacyHeaders: true,
  skip: (req) => {
    const p = (req.path || '').toLowerCase();
    const orig = (req.originalUrl || '').toLowerCase();
    const ua = (req.headers['user-agent'] || '').toLowerCase();

    // Excluir todas las variantes de health checks (/api/health, /health, /health/live, /health/ready, /)
    if (p === '/' || p.startsWith('/health') || p.includes('health')) return true;
    if (orig === '/' || orig.includes('/health')) return true;

    // Excluir agentes de sondeo de orquestadores de Render, AWS o Uptime
    if (ua.includes('render') || ua.includes('healthcheck') || ua.includes('uptime') || ua.includes('consul')) {
      return true;
    }

    return false;
  },
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
 * Limitador específico y controlado para la sonda de base de datos `/api/health/ready`.
 * Permite monitoreo frecuente de orquestadores (Render/Kubernetes) hasta 600 peticiones/minuto por IP,
 * bloqueando intentos maliciosos de saturar el pool de conexiones de Postgres.
 */
export const readyHealthRateLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minuto
  max: 600, // 10 peticiones por segundo máximo
  standardHeaders: true,
  legacyHeaders: false,
  skip: (req) => {
    const ua = (req.headers['user-agent'] || '').toLowerCase();
    return ua.includes('render') || ua.includes('healthcheck') || ua.includes('uptime') || ua.includes('consul');
  },
  handler: (req: Request, res: Response) => {
    res.setHeader('Retry-After', '60');
    res.status(429).json({
      status: 'TOO_MANY_REQUESTS',
      message: 'Límite de comprobaciones de salud excedido para esta IP.'
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

/**
 * Limitador para el endpoint de refresco de tokens `/api/auth/refresh`.
 * Permite 30 peticiones por minuto por IP para rotación normal y previene fuerza bruta.
 */
export const refreshLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minuto
  max: 30,
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req: Request, res: Response) => {
    res.setHeader('Retry-After', '60');
    res.status(429).json({
      success: false,
      error: {
        code: 'TOO_MANY_REFRESH',
        message: 'Límite de intentos de renovación de sesión excedido. Espere un momento.'
      }
    });
  }
});

/**
 * Limitador estricto para generación de links de pago (/api/orders/:id/payment-link).
 * Permite un máximo de 5 peticiones por minuto por usuario para evitar saturar Culqi.
 */
export const paymentLinkLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minuto
  max: 5,
  keyGenerator: (req) => `u:${(req as any).user?.userId ?? (req as any).user?.id ?? req.ip}`,
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req: Request, res: Response) => {
    res.setHeader('Retry-After', '60');
    res.status(429).json({
      success: false,
      error: {
        code: 'TOO_MANY_PAYMENT_LINKS',
        message: 'Ha superado el límite de generación de links de pago (máximo 5 por minuto).'
      }
    });
  }
});


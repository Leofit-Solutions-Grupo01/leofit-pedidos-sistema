/**
 * @file error.middleware.ts
 * @description Middleware Centralizado de Manejo de Excepciones y Respuestas de Error Uniformes.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Función:
 * - Captura errores no controlados en la cadena de middleware de Express.
 * - Evita la fuga de trazas de stack trace sensibles en entornos de producción (OWASP A05).
 * - Formatea todas las respuestas de error bajo una estructura JSON predecible:
 *   {
 *     "success": false,
 *     "error": { "code": string, "message": string }
 *   }
 */

import { Request, Response, NextFunction } from 'express';

export function errorHandler(err: any, req: Request, res: Response, next: NextFunction): void {
  const correlationId = (req.headers['x-correlation-id'] as string) || 'unknown';

  // Registro en log para observabilidad del servidor con correlationId
  console.error(`❌ [Server Error] [CID: ${correlationId}]:`, err);

  if (err && err.name === 'ZodError') {
    res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Los datos proporcionados no cumplen con el esquema de validación',
        details: err.errors || err.message,
        correlationId
      }
    });
    return;
  }

  const statusCode = err.statusCode || 500;
  const errorCode = err.code || 'INTERNAL_SERVER_ERROR';
  const errorMessage = process.env.NODE_ENV === 'production' && statusCode === 500
    ? 'Ha ocurrido un error interno en el servidor.'
    : (err.message || 'Ha ocurrido un error inesperado en el servidor.');

  res.status(statusCode).json({
    success: false,
    error: {
      code: errorCode,
      message: errorMessage,
      correlationId,
      ...(process.env.NODE_ENV !== 'production' && { stack: err.stack })
    }
  });
}

/**
 * @file validate.middleware.ts
 * @description Middleware de Validación y Sanitización de Cargas Útiles (Zod Schema Validation).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Función:
 * - Valida la estructura, tipos de datos y restricciones de negocio en el cuerpo de la petición HTTP (`req.body`).
 * - Sanitiza y previene inyecciones maliciosas (XSS, SQLi, Prototype Pollution).
 * - Retorna un desglose amigable y detallado de errores en caso de fallo (HTTP 400 Bad Request).
 */

import { Request, Response, NextFunction } from 'express';
import { ZodSchema, ZodError } from 'zod';

/**
 * Validador genérico basado en esquemas Zod.
 * @param schema Esquema de validación Zod
 */
export function validateBody(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction): void => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        res.status(400).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Los datos enviados en la petición no cumplen con el esquema de validación requerido.',
            details: error.errors.map(err => ({
              field: err.path.join('.'),
              message: err.message
            }))
          }
        });
        return;
      }
      next(error);
    }
  };
}

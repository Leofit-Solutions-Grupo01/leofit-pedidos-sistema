/**
 * @file idempotency.middleware.ts
 * @description Middleware de Idempotencia estricto (RFC 9457 & IETF Idempotency-Key Draft).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Garantías Arquitectónicas:
 * 1. Scope Estricto por Usuario: La unicidad está ligada a (user_id, idempotency_key).
 *    Previene colisiones accidentales y ataques de cross-user replay.
 * 2. Canonical JSON (RFC 8785 / JCS): Hash determinista insensible al orden de propiedades.
 * 3. Protección de Concurrencia Simultánea (Promise.all): Reserva atómica en DB
 *    que previene pedidos duplicados y descuento múltiple de inventario.
 * 4. Fail-Closed: Requiere almacenamiento centralizado para consistencia en clúster multi-nodo.
 * 5. TTL & Limpieza Automática: Registros expiran a las 48 horas.
 */

import { Request, Response, NextFunction } from 'express';
import crypto from 'crypto';
import { dbPool, isPostgresAvailable } from '../config/database';
import { logger } from '../utils/logger';

const CLEANUP_INTERVAL_MS = 60 * 60 * 1000; // Limpieza in-process cada 1 hora

/**
 * Normaliza un objeto a formato JSON Canónico según RFC 8785 (JCS).
 * Las claves se ordenan lexicográficamente por código Unicode UTF-16 de forma recursiva.
 */
export function canonicalizeJson(value: any): string {
  if (value === null || typeof value !== 'object') {
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return '[' + value.map(canonicalizeJson).join(',') + ']';
  }
  const keys = Object.keys(value).sort();
  const pairs = keys.map((key) => JSON.stringify(key) + ':' + canonicalizeJson(value[key]));
  return '{' + pairs.join(',') + '}';
}

/**
 * Ejecuta la purga de registros expirados en PostgreSQL.
 * Puede ser invocada por el temporizador interno o por un cron externo vía endpoint.
 */
export async function cleanupExpiredIdempotencyKeys(): Promise<number> {
  if (!isPostgresAvailable()) return 0;
  try {
    const result = await dbPool.query('DELETE FROM idempotency_keys WHERE expires_at < CURRENT_TIMESTAMP');
    const deleted = result.rowCount || 0;
    if (deleted > 0) {
      logger.info(`[Idempotency Cleanup] ${deleted} claves expiradas eliminadas exitosamente.`);
    }
    return deleted;
  } catch (err: any) {
    logger.warn('[Idempotency Cleanup Warning] Error durante purga:', { error: err.message });
    return 0;
  }
}

// Limpieza periódica in-process
setInterval(() => {
  cleanupExpiredIdempotencyKeys().catch(() => {});
}, CLEANUP_INTERVAL_MS).unref();

export async function idempotencyMiddleware(req: Request, res: Response, next: NextFunction): Promise<void> {
  const rawKey = req.headers['idempotency-key'] || req.headers['x-idempotency-key'];
  if (!rawKey || typeof rawKey !== 'string') {
    return next();
  }

  const idempotencyKey = rawKey.trim();
  // Validación estricta de formato seguro
  if (!/^[a-zA-Z0-9_\-:]{8,128}$/.test(idempotencyKey)) {
    res.status(400).json({
      success: false,
      error: {
        code: 'INVALID_IDEMPOTENCY_KEY',
        message: 'La cabecera Idempotency-Key debe contener entre 8 y 128 caracteres alfanuméricos válidos.'
      }
    });
    return;
  }

  // 1. Fail-Closed: La persistencia centralizada es requerida
  if (!isPostgresAvailable()) {
    res.setHeader('Retry-After', '5');
    res.status(503).json({
      success: false,
      error: {
        code: 'IDEMPOTENCY_STORE_UNAVAILABLE',
        message: 'El almacén transaccional de idempotencia no está disponible temporalmente. Intente en unos segundos.'
      }
    });
    return;
  }

  // 2. Extraer usuario autenticado para scopear la llave (anti cross-user replay)
  const userId = (req as any).user?.userId || (req as any).user?.id || 0;

  // 3. Hash determinista canónico (RFC 8785)
  const canonicalBody = canonicalizeJson(req.body || {});
  const pathForHash = (req.baseUrl || '') + (req.path || '');
  const hashPayload = `${userId}:${req.method}:${pathForHash}:${canonicalBody}`;
  const currentRequestHash = crypto.createHash('sha256').update(hashPayload).digest('hex');

  // 4. Verificación de existencia previa en PostgreSQL
  try {
    const existing = await dbPool.query(
      `SELECT status_code, response_body, request_hash, expires_at 
       FROM idempotency_keys 
       WHERE user_id = $1 AND key = $2 AND expires_at > CURRENT_TIMESTAMP`,
      [userId, idempotencyKey]
    );

    if (existing.rows.length > 0) {
      const cached = existing.rows[0];

      // Verificación de Payload Mismatch (RFC Section 2.3)
      if (cached.request_hash && cached.request_hash !== currentRequestHash) {
        res.status(422).json({
          success: false,
          error: {
            code: 'IDEMPOTENCY_PAYLOAD_MISMATCH',
            message: 'La Idempotency-Key proporcionada ya fue utilizada con un cuerpo o usuario diferente.'
          }
        });
        return;
      }

      // Si status_code === 0, hay una petición en curso en este momento (concurrencia paralela)
      if (cached.status_code === 0) {
        // Breve espera activa para esperar la finalización del request en curso
        for (let attempt = 0; attempt < 15; attempt++) {
          await new Promise((resolve) => setTimeout(resolve, 100));
          const check = await dbPool.query(
            `SELECT status_code, response_body FROM idempotency_keys WHERE user_id = $1 AND key = $2`,
            [userId, idempotencyKey]
          );
          if (check.rows.length > 0 && check.rows[0].status_code > 0) {
            res.setHeader('X-Cache-Lookup', 'IDEMPOTENT_HIT');
            res.setHeader('Idempotency-Key', idempotencyKey);
            res.status(check.rows[0].status_code).json(check.rows[0].response_body);
            return;
          }
        }

        // Si expiró el tiempo de espera del request en curso
        res.status(409).json({
          success: false,
          error: {
            code: 'IDEMPOTENCY_IN_PROGRESS',
            message: 'Una solicitud con esta Idempotency-Key está siendo procesada en este momento. Intente en unos segundos.'
          }
        });
        return;
      }

      // Solicitud previa completada: retornar respuesta cacheada
      res.setHeader('X-Cache-Lookup', 'IDEMPOTENT_HIT');
      res.setHeader('Idempotency-Key', idempotencyKey);
      res.status(cached.status_code).json(cached.response_body);
      return;
    }

    // 5. Reserva atómica: registrar la clave con status_code = 0 (en progreso)
    const reservation = await dbPool.query(
      `INSERT INTO idempotency_keys (user_id, key, request_hash, status_code, response_body, expires_at)
       VALUES ($1, $2, $3, 0, '{}'::jsonb, CURRENT_TIMESTAMP + INTERVAL '48 hours')
       ON CONFLICT (user_id, key) DO NOTHING
       RETURNING id`,
      [userId, idempotencyKey, currentRequestHash]
    );

    // Si hubo conflicto (otra petición ganó la carrera de inserción milisegundos antes)
    if (reservation.rowCount === 0) {
      // Reintentar lectura para servir la respuesta de la otra petición
      for (let attempt = 0; attempt < 15; attempt++) {
        await new Promise((resolve) => setTimeout(resolve, 100));
        const check = await dbPool.query(
          `SELECT status_code, response_body FROM idempotency_keys WHERE user_id = $1 AND key = $2`,
          [userId, idempotencyKey]
        );
        if (check.rows.length > 0 && check.rows[0].status_code > 0) {
          res.setHeader('X-Cache-Lookup', 'IDEMPOTENT_HIT');
          res.setHeader('Idempotency-Key', idempotencyKey);
          res.status(check.rows[0].status_code).json(check.rows[0].response_body);
          return;
        }
      }

      res.status(409).json({
        success: false,
        error: {
          code: 'IDEMPOTENCY_IN_PROGRESS',
          message: 'Una solicitud con esta Idempotency-Key está siendo procesada en este momento.'
        }
      });
      return;
    }
  } catch (err: any) {
    logger.error('Error al procesar reserva de idempotencia:', { error: err.message });
    res.setHeader('Retry-After', '5');
    res.status(503).json({
      success: false,
      error: {
        code: 'IDEMPOTENCY_CHECK_FAILED',
        message: 'No se pudo verificar la llave de idempotencia. Intente nuevamente.'
      }
    });
    return;
  }

  // 6. Interceptar res.json para persistir el resultado final de la operación
  const originalJson = res.json.bind(res);
  res.json = (body: any): Response => {
    res.json = originalJson;

    if (res.statusCode >= 200 && res.statusCode < 300) {
      // Éxito: persistir respuesta final para futuros reintentos
      dbPool.query(
        `UPDATE idempotency_keys 
         SET status_code = $1, response_body = $2 
         WHERE user_id = $3 AND key = $4`,
        [res.statusCode, JSON.stringify(body), userId, idempotencyKey]
      ).catch((err) => {
        logger.error('Error persistiendo respuesta de idempotencia:', { error: err.message });
      });
    } else {
      // Fallo de cliente/servidor: liberar la reserva para permitir reintentos corregidos
      dbPool.query(
        `DELETE FROM idempotency_keys WHERE user_id = $1 AND key = $2 AND status_code = 0`,
        [userId, idempotencyKey]
      ).catch(() => {});
    }

    res.setHeader('Idempotency-Key', idempotencyKey);
    return originalJson(body);
  };

  next();
}

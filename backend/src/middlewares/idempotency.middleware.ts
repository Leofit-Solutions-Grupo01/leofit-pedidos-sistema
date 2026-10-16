/**
 * @file idempotency.middleware.ts
 * @description Middleware de Idempotencia estricto (RFC 8785 Canonical JSON & IETF Idempotency-Key Draft).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Garantías Arquitectónicas (Ronda 4):
 * 1. Scope Estricto por Usuario: La unicidad está ligada a (user_id, idempotency_key).
 * 2. Canonical JSON Estricto (RFC 8785 / JCS): Mediante la librería oficial `canonicalize`.
 * 3. Máquina de Estados Explícita (PENDING -> COMPLETED / FAILED):
 *    - CERO "rollback delete": Los fallos se marcan como FAILED para evitar race conditions.
 *    - Reintentos sobre transacciones fallidas son permitidos y rastreados.
 * 4. Serialización Atómica con PostgreSQL Advisory Locks:
 *    - Previene condiciones de carrera con requests simultáneos (Promise.all).
 * 5. Fail-Closed: Requiere almacenamiento centralizado para consistencia en clúster.
 */

import { Request, Response, NextFunction } from 'express';
import crypto from 'crypto';
import canonicalize from '../utils/canonicalize';
import { dbPool, isPostgresAvailable } from '../config/database';
import { logger } from '../utils/logger';

const CLEANUP_INTERVAL_MS = 60 * 60 * 1000; // Limpieza in-process cada 1 hora

/**
 * Normaliza un objeto a formato JSON Canónico según RFC 8785 (JCS) usando la librería oficial.
 */
export function canonicalizeJson(value: any): string {
  try {
    const result = canonicalize(value);
    return typeof result === 'string' ? result : JSON.stringify(value);
  } catch {
    return JSON.stringify(value);
  }
}

/**
 * Ejecuta la purga de registros expirados en PostgreSQL.
 * Puede ser invocada por el temporizador interno o por un cron externo vía endpoint administrativo.
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
  // Validación estricta de formato seguro (anti injection y longitud estándar)
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

  // 2. Extraer usuario autenticado para scopear la llave
  const userId = (req as any).user?.userId || (req as any).user?.id || 0;

  // 3. Hash determinista canónico estricto (RFC 8785)
  const canonicalBody = canonicalizeJson(req.body || {});
  const pathForHash = (req.baseUrl || '') + (req.path || '');
  const hashPayload = `${userId}:${req.method}:${pathForHash}:${canonicalBody}`;
  const currentRequestHash = crypto.createHash('sha256').update(hashPayload).digest('hex');

  const lockKey = `${userId}:${idempotencyKey}`;
  let lockAcquired = false;

  try {
    // 4. Intentar adquirir PostgreSQL Advisory Lock para serializar peticiones simultáneas sobre la misma clave
    const lockResult = await dbPool.query('SELECT pg_try_advisory_lock(hashtext($1)) as acquired', [lockKey]);
    lockAcquired = lockResult.rows[0]?.acquired === true;

    if (!lockAcquired) {
      // Conflicto de carrera concurrente detectado: otra petición está procesando activamente esta key
      res.setHeader('Retry-After', '2');
      res.status(409).json({
        success: false,
        error: {
          code: 'IDEMPOTENCY_IN_PROGRESS',
          message: 'Una solicitud con esta Idempotency-Key está siendo procesada concurrentemente. Por favor espere y reintente.',
          retryAfter: 2
        }
      });
      return;
    }

    // 5. Consultar estado en la base de datos
    const existing = await dbPool.query(
      `SELECT status, status_code, response_body, request_hash, locked_until, expires_at 
       FROM idempotency_keys 
       WHERE user_id = $1 AND key = $2 AND expires_at > CURRENT_TIMESTAMP`,
      [userId, idempotencyKey]
    );

    if (existing.rows.length > 0) {
      const record = existing.rows[0];

      // Verificación de Payload Mismatch (RFC Section 2.3)
      if (record.request_hash && record.request_hash !== currentRequestHash) {
        await dbPool.query('SELECT pg_advisory_unlock(hashtext($1))', [lockKey]);
        res.status(422).json({
          success: false,
          error: {
            code: 'IDEMPOTENCY_PAYLOAD_MISMATCH',
            message: 'La Idempotency-Key proporcionada ya fue utilizada con un cuerpo o solicitud diferente.'
          }
        });
        return;
      }

      // Máquina de Estados:
      // A) COMPLETED: Retornar respuesta cacheada
      if (record.status === 'COMPLETED') {
        await dbPool.query('SELECT pg_advisory_unlock(hashtext($1))', [lockKey]);
        res.setHeader('X-Cache-Lookup', 'IDEMPOTENT_HIT');
        res.setHeader('Idempotency-Key', idempotencyKey);
        res.status(record.status_code).json(record.response_body);
        return;
      }

      // B) PENDING: Verificar si aún está dentro de su ventana de lock
      const now = new Date();
      const lockExpiry = record.locked_until ? new Date(record.locked_until) : new Date(0);
      if (record.status === 'PENDING' && lockExpiry > now) {
        await dbPool.query('SELECT pg_advisory_unlock(hashtext($1))', [lockKey]);
        res.setHeader('Retry-After', '2');
        res.status(409).json({
          success: false,
          error: {
            code: 'IDEMPOTENCY_IN_PROGRESS',
            message: 'Una solicitud con esta Idempotency-Key está en proceso de ejecución.',
            retryAfter: 2
          }
        });
        return;
      }

      // C) FAILED o PENDING expirado (el proceso anterior crasheó o falló):
      // Permitir re-ejecución actualizando a PENDING con nueva ventana de lock
      await dbPool.query(
        `UPDATE idempotency_keys 
         SET status = 'PENDING', 
             request_hash = $1, 
             updated_at = CURRENT_TIMESTAMP, 
             locked_until = CURRENT_TIMESTAMP + INTERVAL '30 seconds' 
         WHERE user_id = $2 AND key = $3`,
        [currentRequestHash, userId, idempotencyKey]
      );
    } else {
      // 6. Inserción inicial con estado PENDING y ventana de lock de 30s
      await dbPool.query(
        `INSERT INTO idempotency_keys (user_id, key, request_hash, status, status_code, response_body, locked_until, expires_at)
         VALUES ($1, $2, $3, 'PENDING', 0, '{}'::jsonb, CURRENT_TIMESTAMP + INTERVAL '30 seconds', CURRENT_TIMESTAMP + INTERVAL '48 hours')
         ON CONFLICT (user_id, key) DO UPDATE 
           SET status = 'PENDING',
               request_hash = EXCLUDED.request_hash,
               updated_at = CURRENT_TIMESTAMP,
               locked_until = CURRENT_TIMESTAMP + INTERVAL '30 seconds'`,
        [userId, idempotencyKey, currentRequestHash]
      );
    }
  } catch (err: any) {
    if (lockAcquired) {
      await dbPool.query('SELECT pg_advisory_unlock(hashtext($1))', [lockKey]).catch(() => {});
    }
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

  // 7. Interceptar res.json para persistir el resultado y liberar el advisory lock
  const originalJson = res.json.bind(res);
  res.json = (body: any): Response => {
    res.json = originalJson;

    const statusCode = res.statusCode;
    const isSuccess = statusCode >= 200 && statusCode < 300;
    const newStatus = isSuccess ? 'COMPLETED' : 'FAILED';

    // Actualización atómica del estado (CERO DELETE, previniendo la race condition señalada)
    dbPool.query(
      `UPDATE idempotency_keys 
       SET status = $1, 
           status_code = $2, 
           response_body = $3, 
           updated_at = CURRENT_TIMESTAMP 
       WHERE user_id = $4 AND key = $5`,
      [newStatus, statusCode, JSON.stringify(body), userId, idempotencyKey]
    ).catch((err) => {
      logger.error('Error actualizando estado de idempotencia:', { error: err.message });
    }).finally(() => {
      // Liberar el advisory lock una vez persistido el estado final
      dbPool.query('SELECT pg_advisory_unlock(hashtext($1))', [lockKey]).catch(() => {});
    });

    res.setHeader('Idempotency-Key', idempotencyKey);
    return originalJson(body);
  };

  next();
}

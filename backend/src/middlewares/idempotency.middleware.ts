/**
 * @file idempotency.middleware.ts
 * @description Middleware de Idempotencia estricto (RFC 8785 Canonical JSON & IETF Idempotency-Key Draft).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Garantías de Producción (Ronda 5):
 * 1. Cero Lock Leaks: Se utiliza `pg_try_advisory_xact_lock` con dos enteros `(user_id, hashtext(key))`
 *    dentro de un bloque transaccional explícito (`BEGIN ... COMMIT / ROLLBACK`).
 *    El lock se libera automáticamente al cerrar la transacción, incluso ante caídas o excepciones no capturadas.
 * 2. Cero Colisiones Cross-User: Al usar `(user_id, hashtext(key))` en dos argumentos de 32 bits,
 *    el `user_id` actúa como espacio de nombres unívoco, eliminando colisiones por paradoja del cumpleaños.
 * 3. Máquina de Estados Inmutable (PENDING -> COMPLETED / FAILED):
 *    - Cero "rollback delete".
 *    - Revalidación estricta de hash: Si un registro está en `FAILED` pero el reintento envía un payload
 *      diferente, responde HTTP 422 IDEMPOTENCY_PAYLOAD_MISMATCH (previene bypass de payloads).
 * 4. PENDING Huérfano: Si un proceso previo crasheó y `locked_until < NOW()`, transiciona explícitamente
 *    a `FAILED` y permite re-ejecución solo si el hash coincide.
 */

import { Request, Response, NextFunction } from 'express';
import crypto from 'crypto';
import { canonicalize } from '../utils/canonicalize';
import { dbPool, isPostgresAvailable } from '../config/database';
import { logger } from '../utils/logger';

const CLEANUP_INTERVAL_MS = 60 * 60 * 1000; // Limpieza in-process cada 1 hora

/**
 * Normaliza un objeto a formato JSON Canónico según RFC 8785 (JCS) usando canonicalize puro.
 */
export function canonicalizeJson(value: any): string {
  try {
    return canonicalize(value);
  } catch {
    return JSON.stringify(value);
  }
}

/**
 * Ejecuta la purga de registros expirados en PostgreSQL.
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

  // 1. Fail-Closed: La persistencia centralizada es obligatoria
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

  // Conexión cliente dedicada para manejar la transacción de lock sin fugas en el pool
  let client: any = null;

  try {
    client = await dbPool.connect();
    await client.query('BEGIN');

    // 4. pg_try_advisory_xact_lock(int, int): Se libera AUTOMÁTICAMENTE al hacer COMMIT o ROLLBACK.
    // Argumento 1: userId (evita colisiones cross-user).
    // Argumento 2: hashtext(idempotencyKey) (entero de 32 bits de la clave).
    const lockResult = await client.query(
      'SELECT pg_try_advisory_xact_lock($1, hashtext($2)) as acquired',
      [userId, idempotencyKey]
    );

    const acquired = lockResult.rows[0]?.acquired === true;
    if (!acquired) {
      await client.query('ROLLBACK');
      client.release();
      client = null;

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

    // 5. Consultar estado en la tabla idempotency_keys
    const existing = await client.query(
      `SELECT status, status_code, response_body, request_hash, locked_until, expires_at 
       FROM idempotency_keys 
       WHERE user_id = $1 AND key = $2 AND expires_at > CURRENT_TIMESTAMP`,
      [userId, idempotencyKey]
    );

    if (existing.rows.length > 0) {
      const record = existing.rows[0];

      // A) Verificación de Payload Mismatch (RFC Section 2.3)
      // Si la clave ya fue usada previamente (en COMPLETED, FAILED o PENDING) con un body distinto -> 422
      if (record.request_hash && record.request_hash !== currentRequestHash) {
        await client.query('ROLLBACK');
        client.release();
        client = null;

        res.status(422).json({
          success: false,
          error: {
            code: 'IDEMPOTENCY_PAYLOAD_MISMATCH',
            message: 'La Idempotency-Key proporcionada ya fue utilizada previamente con un payload diferente.'
          }
        });
        return;
      }

      // B) COMPLETED: Retornar respuesta cacheada directamente
      if (record.status === 'COMPLETED') {
        await client.query('ROLLBACK');
        client.release();
        client = null;

        res.setHeader('X-Cache-Lookup', 'IDEMPOTENT_HIT');
        res.setHeader('Idempotency-Key', idempotencyKey);
        res.status(record.status_code).json(record.response_body);
        return;
      }

      // C) PENDING: Verificar si aún está dentro de su ventana de lock
      const now = new Date();
      const lockExpiry = record.locked_until ? new Date(record.locked_until) : new Date(0);
      if (record.status === 'PENDING' && lockExpiry > now) {
        await client.query('ROLLBACK');
        client.release();
        client = null;

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

      // D) FAILED o PENDING Huérfano (timeout de 30s expirado):
      // Como el hash coincide (comprobado en paso A), se permite la re-ejecución pasando a PENDING
      await client.query(
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
      await client.query(
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

    // Commit de la reserva: el xact_lock se libera aquí de forma limpia y la fila queda en PENDING
    await client.query('COMMIT');
    client.release();
    client = null;
  } catch (err: any) {
    if (client) {
      await client.query('ROLLBACK').catch(() => {});
      client.release(true); // Destruir conexión si hubo fallo crítico para no contaminar el pool
      client = null;
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

  // 7. Interceptar res.json para persistir el resultado final
  const originalJson = res.json.bind(res);
  res.json = (body: any): Response => {
    res.json = originalJson;

    const statusCode = res.statusCode;
    const isSuccess = statusCode >= 200 && statusCode < 300;
    const newStatus = isSuccess ? 'COMPLETED' : 'FAILED';

    // Actualización atómica en base de datos (CERO DELETE)
    dbPool.query(
      `UPDATE idempotency_keys 
       SET status = $1, 
           status_code = $2, 
           response_body = $3, 
           updated_at = CURRENT_TIMESTAMP 
       WHERE user_id = $4 AND key = $5`,
      [newStatus, statusCode, JSON.stringify(body), userId, idempotencyKey]
    ).catch((err) => {
      logger.error('Error actualizando estado final de idempotencia:', { error: err.message });
    });

    res.setHeader('Idempotency-Key', idempotencyKey);
    return originalJson(body);
  };

  next();
}

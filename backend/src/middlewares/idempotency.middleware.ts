/**
 * @file idempotency.middleware.ts
 * @description Middleware de Idempotencia estricto (RFC 8785 Canonical JSON & IETF Idempotency-Key Draft).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Garantías Arquitectónicas (Ronda 6 - Producción Real):
 * 1. Transacción Unificada (CERO Lock Leaks & Cero Teatro):
 *    - La transacción `BEGIN`, el `pg_try_advisory_xact_lock`, la creación del pedido (`INSERT INTO orders`)
 *      y la actualización a `COMPLETED` se ejecutan sobre la MISMA conexión (`res.locals.dbClient`).
 *    - El `COMMIT` final persiste atómicamente el pedido, el stock y la llave de idempotencia,
 *      liberando el advisory xact lock en un único instante indivisible.
 * 2. Timeouts Transaccionales Duros:
 *    - `SET LOCAL statement_timeout = '10s'`
 *    - `SET LOCAL idle_in_transaction_session_timeout = '15s'`
 * 3. Recuperación Atómica de PENDING Huérfano:
 *    - `UPDATE ... WHERE locked_until < NOW() RETURNING id` en una sola sentencia SQL atómica.
 * 4. Cero Colisiones Cross-User:
 *    - Par de 2 enteros nativo `pg_try_advisory_xact_lock(user_id, hashtext(key))`.
 * 5. Revalidación Estricta de Hash en `FAILED`:
 *    - Rechazo inmediato (HTTP 422) si se reintenta una clave con payload alterado.
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

  let client: any = null;

  try {
    client = await dbPool.connect();
    await client.query('BEGIN');

    // Timeouts de seguridad estrictos DENTRO de la transacción
    await client.query("SET LOCAL statement_timeout = '10s'");
    await client.query("SET LOCAL idle_in_transaction_session_timeout = '15s'");

    // 4. Intento 1: Recuperación atómica de PENDING huérfano (solo UNO gana)
    const recoverResult = await client.query(
      `UPDATE idempotency_keys
       SET locked_until = NOW() + INTERVAL '30 seconds',
           updated_at   = NOW()
       WHERE user_id = $1 
         AND key = $2
         AND status = 'PENDING' 
         AND locked_until < NOW()
         AND request_hash = $3
       RETURNING id`,
      [userId, idempotencyKey, currentRequestHash]
    );

    // 5. Intento 2: Reserva nueva si la clave no existía
    const insertResult = await client.query(
      `INSERT INTO idempotency_keys
         (user_id, key, request_hash, status, locked_until, expires_at)
       VALUES ($1, $2, $3, 'PENDING', NOW() + INTERVAL '30 seconds', NOW() + INTERVAL '48 hours')
       ON CONFLICT (user_id, key) DO NOTHING
       RETURNING id`,
      [userId, idempotencyKey, currentRequestHash]
    );

    // 6. Si no recuperó huérfano ni insertó nuevo, la clave ya existe con estado activo
    if (recoverResult.rowCount === 0 && insertResult.rowCount === 0) {
      const existing = await client.query(
        `SELECT status, status_code, response_body, request_hash, locked_until 
         FROM idempotency_keys 
         WHERE user_id = $1 AND key = $2`,
        [userId, idempotencyKey]
      );

      const row = existing.rows[0];

      // A) Verificación de Payload Mismatch (RFC Section 2.3)
      if (row.request_hash && row.request_hash !== currentRequestHash) {
        await client.query('ROLLBACK');
        client.release();
        res.status(422).json({
          success: false,
          error: {
            code: 'IDEMPOTENCY_PAYLOAD_MISMATCH',
            message: 'La Idempotency-Key proporcionada ya fue utilizada previamente con un payload diferente.'
          }
        });
        return;
      }

      // B) COMPLETED: Retornar respuesta cacheada
      if (row.status === 'COMPLETED') {
        await client.query('ROLLBACK');
        client.release();
        res.setHeader('X-Cache-Lookup', 'IDEMPOTENT_HIT');
        res.setHeader('Idempotency-Key', idempotencyKey);
        res.status(row.status_code).json(row.response_body);
        return;
      }

      // C) FAILED con mismo payload: Permitir re-ejecución
      if (row.status === 'FAILED') {
        await client.query(
          `UPDATE idempotency_keys 
           SET status = 'PENDING', 
               locked_until = NOW() + INTERVAL '30 seconds', 
               updated_at = NOW() 
           WHERE user_id = $1 AND key = $2`,
          [userId, idempotencyKey]
        );
      } else {
        // PENDING activo no expirado: Conflicto de procesamiento en curso
        await client.query('ROLLBACK');
        client.release();
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
    }

    // 7. Adquirir Advisory xact lock transaccional (par de 2 enteros = sin colisiones cross-user)
    const lock = await client.query(
      `SELECT pg_try_advisory_xact_lock($1, hashtext($2)) AS acquired`,
      [userId, idempotencyKey]
    );

    if (!lock.rows[0].acquired) {
      await client.query('ROLLBACK');
      client.release();
      res.setHeader('Retry-After', '2');
      res.status(409).json({
        success: false,
        error: {
          code: 'IDEMPOTENCY_IN_PROGRESS',
          message: 'Una solicitud con esta Idempotency-Key está siendo procesada en este momento.',
          retryAfter: 2
        }
      });
      return;
    }

    // 8. Exponer la conexión transaccional al controlador para que el INSERT use LA MISMA transacción
    res.locals.dbClient = client;
    res.locals.idempotencyKey = idempotencyKey;
    res.locals.requestHash = currentRequestHash;
  } catch (err: any) {
    if (client) {
      await client.query('ROLLBACK').catch(() => {});
      client.release(true);
    }
    logger.error('Error al inicializar transacción de idempotencia:', { error: err.message });
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

  // 9. Interceptar res.json para finalizar la transacción en la MISMA conexión
  const originalJson = res.json.bind(res);
  res.json = (body: any): Response => {
    res.json = originalJson;

    const statusCode = res.statusCode;
    const isSuccess = statusCode >= 200 && statusCode < 300;
    const newStatus = isSuccess ? 'COMPLETED' : 'FAILED';

    client.query(
      `UPDATE idempotency_keys 
       SET status = $1, 
           status_code = $2, 
           response_body = $3, 
           updated_at = NOW() 
       WHERE user_id = $4 AND key = $5`,
      [newStatus, statusCode, JSON.stringify(body), userId, idempotencyKey]
    )
    .then(async () => {
      // COMMIT atómico que consolida el pedido, el stock y la clave de idempotencia
      await client.query('COMMIT');
    })
    .catch(async (err: any) => {
      logger.error('Error persistiendo confirmación de idempotencia:', { error: err.message });
      await client.query('ROLLBACK').catch(() => {});
    })
    .finally(() => {
      client.release();
    });

    res.setHeader('Idempotency-Key', idempotencyKey);
    return originalJson(body);
  };

  next();
}

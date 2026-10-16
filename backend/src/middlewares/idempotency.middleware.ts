/**
 * @file idempotency.middleware.ts
 * @description Middleware de Idempotencia estricto (RFC 9457 & IETF Idempotency-Key Draft).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Garantías Arquitectónicas:
 * 1. Fail-Closed: Si PostgreSQL no está disponible para garantizar unicidad distribuida,
 *    retorna 503 (evita falsos duplicados en clúster multi-instancia de Render).
 * 2. Payload Mismatch (RFC Section 2.3): Si se reutiliza la misma clave con un payload distinto,
 *    retorna HTTP 422 Unprocessable Entity.
 * 3. TTL & Cleanup Automático: Registros expiran a las 48 horas con limpieza periódica.
 */

import { Request, Response, NextFunction } from 'express';
import crypto from 'crypto';
import { dbPool, isPostgresAvailable } from '../config/database';

const CLEANUP_INTERVAL_MS = 60 * 60 * 1000; // Limpieza cada 1 hora

// Limpieza periódica en PostgreSQL de claves con TTL expirado
setInterval(async () => {
  if (isPostgresAvailable()) {
    try {
      await dbPool.query('DELETE FROM idempotency_keys WHERE expires_at < CURRENT_TIMESTAMP');
    } catch {
      // Ignorar errores transitorios de limpieza en segundo plano
    }
  }
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

  // 1. Fail-Closed: La persistencia centralizada es requerida para evitar bifurcaciones
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

  // Cálculo del hash SHA-256 del cuerpo de la petición
  const requestPayloadString = JSON.stringify(req.body || {});
  const currentRequestHash = crypto.createHash('sha256').update(requestPayloadString).digest('hex');

  // 2. Consulta de respuesta previa en PostgreSQL
  try {
    const result = await dbPool.query(
      `SELECT status_code, response_body, request_hash, expires_at 
       FROM idempotency_keys 
       WHERE key = $1 AND expires_at > CURRENT_TIMESTAMP`,
      [idempotencyKey]
    );

    if (result.rows.length > 0) {
      const cached = result.rows[0];

      // Verificación de Payload Mismatch (RFC Section 2.3)
      if (cached.request_hash && cached.request_hash !== currentRequestHash) {
        res.status(422).json({
          success: false,
          error: {
            code: 'IDEMPOTENCY_PAYLOAD_MISMATCH',
            message: 'La Idempotency-Key proporcionada ya fue utilizada con un cuerpo de solicitud diferente.'
          }
        });
        return;
      }

      res.setHeader('X-Cache-Lookup', 'IDEMPOTENT_HIT');
      res.setHeader('Idempotency-Key', idempotencyKey);
      res.status(cached.status_code).json(cached.response_body);
      return;
    }
  } catch (err: any) {
    console.error('❌ Error consultando idempotency_keys:', err);
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

  // 3. Interceptar res.json para persistir la respuesta original con TTL de 48h
  const originalJson = res.json.bind(res);
  res.json = (body: any): Response => {
    res.json = originalJson;

    // Solo persistir respuestas exitosas (2xx)
    if (res.statusCode >= 200 && res.statusCode < 300) {
      dbPool.query(
        `INSERT INTO idempotency_keys (key, request_hash, status_code, response_body, expires_at)
         VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP + INTERVAL '48 hours')
         ON CONFLICT (key) DO UPDATE 
           SET response_body = EXCLUDED.response_body,
               status_code = EXCLUDED.status_code`,
        [idempotencyKey, currentRequestHash, res.statusCode, JSON.stringify(body)]
      ).catch((err) => {
        console.error('⚠️ Error persistiendo idempotency_key:', err);
      });
    }

    res.setHeader('Idempotency-Key', idempotencyKey);
    return originalJson(body);
  };

  next();
}

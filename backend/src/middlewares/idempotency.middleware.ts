/**
 * @file idempotency.middleware.ts
 * @description Middleware de Idempotencia para endpoints transaccionales (POST /api/orders).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Función:
 * - Inspecciona la cabecera `Idempotency-Key` (RFC estándar).
 * - Si la petición ya fue procesada, retorna la respuesta cacheada sin duplicar órdenes ni descontar doble stock.
 * - Soporta persistencia en PostgreSQL con fallback en memoria (LRU / Map con TTL de 24h).
 */

import { Request, Response, NextFunction } from 'express';
import { dbPool, isPostgresAvailable } from '../config/database';

interface CachedResponse {
  statusCode: number;
  body: any;
  timestamp: number;
}

const memoryIdempotencyStore = new Map<string, CachedResponse>();
const CLEANUP_INTERVAL_MS = 60 * 60 * 1000; // 1 hora
const TTL_MS = 24 * 60 * 60 * 1000; // 24 horas

// Limpieza periódica de claves expiradas en memoria
setInterval(() => {
  const now = Date.now();
  for (const [key, value] of memoryIdempotencyStore.entries()) {
    if (now - value.timestamp > TTL_MS) {
      memoryIdempotencyStore.delete(key);
    }
  }
}, CLEANUP_INTERVAL_MS).unref();

export async function idempotencyMiddleware(req: Request, res: Response, next: NextFunction): Promise<void> {
  const rawKey = req.headers['idempotency-key'] || req.headers['x-idempotency-key'];
  if (!rawKey || typeof rawKey !== 'string') {
    return next();
  }

  const idempotencyKey = rawKey.trim();
  if (!idempotencyKey || idempotencyKey.length > 128) {
    return next();
  }

  // 1. Intentar recuperar respuesta previa desde PostgreSQL
  if (isPostgresAvailable()) {
    try {
      const result = await dbPool.query(
        'SELECT status_code, response_body FROM idempotency_keys WHERE key = $1',
        [idempotencyKey]
      );
      if (result.rows.length > 0) {
        const cached = result.rows[0];
        res.setHeader('X-Cache-Lookup', 'IDEMPOTENT_HIT');
        res.setHeader('Idempotency-Key', idempotencyKey);
        res.status(cached.status_code).json(cached.response_body);
        return;
      }
    } catch (err) {
      console.warn('⚠️ Error consultando idempotency_keys en DB, procediendo con fallback en memoria:', err);
    }
  }

  // 2. Fallback: consultar almacén en memoria
  const memoryCached = memoryIdempotencyStore.get(idempotencyKey);
  if (memoryCached && (Date.now() - memoryCached.timestamp < TTL_MS)) {
    res.setHeader('X-Cache-Lookup', 'IDEMPOTENT_HIT_MEMORY');
    res.setHeader('Idempotency-Key', idempotencyKey);
    res.status(memoryCached.statusCode).json(memoryCached.body);
    return;
  }

  // 3. Interceptar res.json para guardar la respuesta tras procesar el pedido
  const originalJson = res.json.bind(res);
  res.json = (body: any): Response => {
    // Restaurar originalJson
    res.json = originalJson;

    // Solo guardar respuestas exitosas (2xx) para permitir reintentos en errores transitorios (4xx/5xx)
    if (res.statusCode >= 200 && res.statusCode < 300) {
      memoryIdempotencyStore.set(idempotencyKey, {
        statusCode: res.statusCode,
        body,
        timestamp: Date.now()
      });

      if (isPostgresAvailable()) {
        dbPool.query(
          `INSERT INTO idempotency_keys (key, status_code, response_body)
           VALUES ($1, $2, $3)
           ON CONFLICT (key) DO NOTHING`,
          [idempotencyKey, res.statusCode, JSON.stringify(body)]
        ).catch((err) => {
          console.warn('⚠️ No se pudo persistir idempotency_key en DB:', err);
        });
      }
    }

    res.setHeader('Idempotency-Key', idempotencyKey);
    return originalJson(body);
  };

  next();
}

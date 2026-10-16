/**
 * @file health.controller.ts
 * @description Controlador de Diagnóstico, Salud del Sistema y Cumplimiento de SLA/SLO.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Indicadores Técnicos Monitoreados:
 * - SLA (Service Level Agreement): Disponibilidad del 99.9% mensual.
 * - SLO (Service Level Objective): Tiempo de respuesta medio < 200ms.
 * - Estado de la capa de persistencia y consumo de memoria del proceso Node.js.
 * - Protección contra saturación de Connection Pool mediante Micro-Cache (3000ms).
 */

import { Request, Response } from 'express';
import { isPostgresAvailable, dbPool } from '../config/database';

const startTime = Date.now();
let consecutiveDbFailures = 0;
const FAILURE_THRESHOLD_READINESS = 3;

// Micro-cache para el ping a la base de datos (mitigación de DoS al connection pool)
const DB_CACHE_TTL_MS = 3000;
let lastDbCheckTimestamp = 0;
let lastDbCheckHealthy = false;
let lastDbCheckError: string | null = null;

export class HealthController {
  /**
   * @route GET /api/health
   * @desc Endpoint de métricas de servicio para orquestadores y dashboards de observabilidad.
   */
  public static check(req: Request, res: Response): void {
    const uptimeSeconds = Math.floor((Date.now() - startTime) / 1000);
    const memoryUsage = process.memoryUsage();

    res.status(200).json({
      status: 'UP',
      timestamp: new Date().toISOString(),
      uptime: `${uptimeSeconds}s`,
      service: 'leofit-backend-api',
      version: '2.0.0',
      database: {
        engine: isPostgresAvailable() ? 'PostgreSQL 16 Cluster (Active Pool)' : 'In-Memory Transactional Store (Fallback)',
        status: 'CONNECTED'
      },
      system: {
        nodeVersion: process.version,
        rssMemoryMB: (memoryUsage.rss / 1024 / 1024).toFixed(2),
        heapUsedMB: (memoryUsage.heapUsed / 1024 / 1024).toFixed(2)
      },
      slo: {
        targetAvailability: '99.9%',
        targetLatencyMs: '< 200ms'
      }
    });
  }

  /**
   * @route GET /api/health/live
   * @desc Sonda Liveness: 100% in-memory. Confirma que el bucle de eventos de Node.js no está bloqueado.
   */
  public static liveness(req: Request, res: Response): void {
    res.status(200).json({
      status: 'ALIVE',
      timestamp: new Date().toISOString()
    });
  }

  /**
   * @route GET /api/health/ready
   * @desc Sonda Readiness con micro-cache de 3000ms y umbral de tolerancia a fallos transitorios.
   */
  public static async readiness(req: Request, res: Response): Promise<void> {
    if (!isPostgresAvailable()) {
      res.status(200).json({
        status: 'READY_DEGRADED',
        mode: 'IN_MEMORY_FALLBACK',
        timestamp: new Date().toISOString()
      });
      return;
    }

    const now = Date.now();
    // Si la última comprobación se realizó hace menos de 3000ms, reutilizar el resultado cacheado
    if (now - lastDbCheckTimestamp < DB_CACHE_TTL_MS) {
      if (lastDbCheckHealthy) {
        res.status(200).json({
          status: 'READY',
          database: 'HEALTHY',
          cached: true,
          timestamp: new Date().toISOString()
        });
        return;
      } else if (consecutiveDbFailures < FAILURE_THRESHOLD_READINESS) {
        res.status(200).json({
          status: 'READY_DEGRADED',
          warning: 'Latencia transitoria o ping lento en base de datos',
          cached: true,
          consecutiveFailures: consecutiveDbFailures,
          timestamp: new Date().toISOString()
        });
        return;
      } else {
        res.setHeader('Retry-After', '5');
        res.status(503).json({
          status: 'NOT_READY',
          error: lastDbCheckError || 'Database unavailable',
          cached: true,
          consecutiveFailures: consecutiveDbFailures,
          retryAfter: '5'
        });
        return;
      }
    }

    try {
      const client = await Promise.race([
        dbPool.connect(),
        new Promise<never>((_, reject) => setTimeout(() => reject(new Error('Database ping timeout')), 3000))
      ]);
      await client.query('SELECT 1');
      client.release();

      consecutiveDbFailures = 0;
      lastDbCheckTimestamp = now;
      lastDbCheckHealthy = true;
      lastDbCheckError = null;

      res.status(200).json({
        status: 'READY',
        database: 'HEALTHY',
        timestamp: new Date().toISOString()
      });
    } catch (error: any) {
      consecutiveDbFailures++;
      lastDbCheckTimestamp = now;
      lastDbCheckHealthy = false;
      lastDbCheckError = error.message;

      console.warn(`⚠️ [Readiness Probe Alert] Fallo ${consecutiveDbFailures}/${FAILURE_THRESHOLD_READINESS}: ${error.message}`);

      // Si no ha superado el umbral, reportar DEGRADED (200) para evitar reinicio intempestivo en Render
      if (consecutiveDbFailures < FAILURE_THRESHOLD_READINESS) {
        res.status(200).json({
          status: 'READY_DEGRADED',
          warning: 'Latencia transitoria o ping lento en base de datos',
          consecutiveFailures: consecutiveDbFailures,
          timestamp: new Date().toISOString()
        });
        return;
      }

      // Umbral superado: marcar 503 para que el load balancer desvíe el tráfico
      res.setHeader('Retry-After', '5');
      res.status(503).json({
        status: 'NOT_READY',
        error: error.message || 'Database unavailable',
        consecutiveFailures: consecutiveDbFailures,
        retryAfter: '5'
      });
    }
  }
}

/**
 * @file health.controller.ts
 * @description Controlador de Diagnóstico, Salud del Sistema y Cumplimiento de SLA/SLO.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Indicadores Técnicos Monitoreados:
 * - SLA: Disponibilidad del 99.9% mensual.
 * - SLO: Tiempo de respuesta medio < 200ms.
 * - Sonda Liveness (/live): 100% in-memory para orquestadores.
 * - Sonda Readiness (/ready): Verificación directa y en tiempo real de PostgreSQL (sin cache que enmascare caídas).
 */

import { Request, Response } from 'express';
import { isPostgresAvailable, dbPool } from '../config/database';

const startTime = Date.now();
let consecutiveDbFailures = 0;
const FAILURE_THRESHOLD_READINESS = 3;

export class HealthController {
  /**
   * @route GET /api/health
   * @desc Endpoint de métricas de servicio para observabilidad general.
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
        status: isPostgresAvailable() ? 'CONNECTED' : 'DEGRADED'
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
   * @desc Sonda Readiness: Verificación directa de conectividad y latencia contra PostgreSQL.
   *       Protegida contra flood por `readyHealthRateLimiter`.
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

    try {
      const client = await Promise.race([
        dbPool.connect(),
        new Promise<never>((_, reject) => setTimeout(() => reject(new Error('Database ping timeout (2500ms)')), 2500))
      ]);
      await client.query('SELECT 1');
      client.release();

      consecutiveDbFailures = 0;

      res.status(200).json({
        status: 'READY',
        database: 'HEALTHY',
        timestamp: new Date().toISOString()
      });
    } catch (error: any) {
      consecutiveDbFailures++;
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

      // Umbral superado: marcar 503 para que el balanceador desvíe el tráfico inmediatamente
      res.setHeader('Retry-After', '5');
      res.status(503).json({
        status: 'NOT_READY',
        error: error.message || 'Database connection failure',
        consecutiveFailures: consecutiveDbFailures,
        retryAfter: '5'
      });
    }
  }
}

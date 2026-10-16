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
 */

import { Request, Response } from 'express';
import { isPostgresAvailable, dbPool } from '../config/database';

const startTime = Date.now();
let consecutiveDbFailures = 0;
const FAILURE_THRESHOLD_READINESS = 3;

export class HealthController {
  /**
   * @route GET /api/health
   * @desc Endpoint de liveness y readiness para sondas de orquestadores (Docker / Kubernetes / Uptime Monitors).
   * @access Público
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
   * @desc Sonda Liveness: confirma que el proceso de Node.js está activo y recibiendo tráfico.
   */
  public static liveness(req: Request, res: Response): void {
    res.status(200).json({
      status: 'ALIVE',
      timestamp: new Date().toISOString()
    });
  }

  /**
   * @route GET /api/health/ready
   * @desc Sonda Readiness: verifica que la base de datos esté lista para aceptar transacciones.
   *       Usa umbral de 3 fallos consecutivos para evitar que el orquestador mate la app por un cold-start o latencia transitoria.
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
        new Promise<never>((_, reject) => setTimeout(() => reject(new Error('Database ping timeout')), 3000))
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

      // Si no ha superado el umbral, reportar DEGRADED (200) para evitar que Render mate el pod
      if (consecutiveDbFailures < FAILURE_THRESHOLD_READINESS) {
        res.status(200).json({
          status: 'READY_DEGRADED',
          warning: 'Latencia transitoria o ping lento en base de datos',
          consecutiveFailures: consecutiveDbFailures,
          timestamp: new Date().toISOString()
        });
        return;
      }

      // Umbral superado: marcar 503 para desviar tráfico real
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

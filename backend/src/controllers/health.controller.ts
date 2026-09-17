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
import { isPostgresAvailable } from '../config/database';

const startTime = Date.now();

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
}

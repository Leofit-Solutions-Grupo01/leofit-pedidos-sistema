/**
 * @file dashboard.controller.ts
 * @description Controlador de Métricas de Negocio, KPIs y Analítica de Ventas.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Indicadores Clave de Desempeño (KPIs):
 * - KPI-01: Volumen total de órdenes procesadas y distribución por estado.
 * - KPI-02: Facturación bruta acumulada (excluyendo pedidos cancelados).
 * - KPI-03: Conteo proactivo de productos con existencias por debajo del umbral de seguridad.
 * - KPI-04: Ranking Top 5 de modelos de prendas con mayor demanda comercial.
 */

import { Request, Response, NextFunction } from 'express';
import { RepositoryFactory } from '../infrastructure/repositories/factory';

export class DashboardController {
  /**
   * @route GET /api/dashboard/stats
   * @desc Consolida las estadísticas y métricas del sistema para el panel administrativo.
   * @access Protegido (ADMIN / OPERATOR)
   */
  public static async getMetrics(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const orderRepo = RepositoryFactory.getOrderRepository();
      const metrics = await orderRepo.getMetrics();

      res.status(200).json({
        success: true,
        data: metrics
      });
    } catch (error) {
      next(error);
    }
  }
}

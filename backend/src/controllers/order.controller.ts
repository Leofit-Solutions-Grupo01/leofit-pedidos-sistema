/**
 * @file order.controller.ts
 * @description Controlador de Ciclo de Vida de Pedidos y Transacciones ACID de Inventario.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Reglas de Negocio y Transaccionalidad:
 * 1. Atomicidad en Inventario: La creación de un pedido bloquea y descuenta el stock de forma atómica.
 * 2. Validación de Transición de Estados: RECIBIDO -> PREPARACION -> EN_CAMINO -> ENTREGADO.
 * 3. Cancelación Segura: Al cancelar un pedido, todas las prendas reservadas se devuelven al almacén.
 * 4. Pista de Auditoría: Cada cambio de estado genera un registro inmutable en `order_status_history`.
 */

import { Request, Response, NextFunction } from 'express';
import { RepositoryFactory } from '../infrastructure/repositories/factory';
import { AuthenticatedRequest } from '../middlewares/auth.middleware';
import { OrderStatus } from '../domain/entities/models';

export class OrderController {
  /**
   * @route GET /api/orders
   * @desc Lista órdenes de compra con opciones de filtrado por estado y término de búsqueda.
   * @access Protegido (ADMIN / OPERATOR)
   * @query { status?: OrderStatus, search?: string }
   */
  public static async listOrders(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const status = req.query.status as OrderStatus | undefined;
      const search = req.query.search as string | undefined;

      const orderRepo = RepositoryFactory.getOrderRepository();
      const orders = await orderRepo.listAll({ status, search });

      res.status(200).json({
        success: true,
        count: orders.length,
        data: orders
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route GET /api/orders/:id
   * @desc Obtiene la ficha completa de un pedido (Items, Datos del Cliente e Historial de Auditoría).
   * @access Protegido (ADMIN / OPERATOR)
   * @param id Identificador numérico del pedido
   */
  public static async getOrderById(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const id = parseInt(req.params.id, 10);
      const orderRepo = RepositoryFactory.getOrderRepository();
      const order = await orderRepo.findById(id);

      if (!order) {
        res.status(404).json({
          success: false,
          error: { code: 'ORDER_NOT_FOUND', message: `Pedido con ID ${id} no encontrado en el sistema.` }
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: order
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route GET /api/orders/track/:orderNumber
   * @desc Consulta pública del estado de un pedido mediante su código único de tracking.
   *       Permite al cliente final rastrear su compra de forma autónoma.
   * @access Público
   * @param orderNumber Código de seguimiento (ej: 'LEO-20260302-001')
   */
  public static async getOrderByNumber(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const orderNumber = req.params.orderNumber;
      const orderRepo = RepositoryFactory.getOrderRepository();
      const order = await orderRepo.findByOrderNumber(orderNumber);

      if (!order) {
        res.status(404).json({
          success: false,
          error: { code: 'ORDER_NOT_FOUND', message: `No se encontró ningún pedido asociado al código: ${orderNumber}` }
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: order
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route POST /api/orders
   * @desc Registra un nuevo pedido, descuenta stock atómicamente y calcula totales.
   * @access Protegido (ADMIN / OPERATOR)
   * @body CreateOrderDTO { clientId/clientData, paymentMethod, shippingCost, items: [{ variantId, quantity, unitPrice }] }
   */
  public static async createOrder(req: AuthenticatedRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      const orderRepo = RepositoryFactory.getOrderRepository();
      
      // Ejecución de la transacción ACID a través de la capa de persistencia
      const order = await orderRepo.create({
        ...req.body,
        userId: req.user?.userId
      });

      res.status(201).json({
        success: true,
        message: `Pedido ${order.order_number} registrado y procesado exitosamente.`,
        data: order
      });
    } catch (error: any) {
      // Manejo específico de conflicto por falta de stock
      if (error.message?.includes('Stock insuficiente')) {
        res.status(409).json({
          success: false,
          error: { code: 'INSUFFICIENT_STOCK', message: error.message }
        });
        return;
      }
      next(error);
    }
  }

  /**
   * @route PATCH /api/orders/:id/status
   * @desc Actualiza el estado del pedido y anota el cambio en la bitácora de auditoría.
   * @access Protegido (ADMIN / OPERATOR)
   * @param id ID del pedido
   * @body { status: OrderStatus, comments?: string }
   */
  public static async updateOrderStatus(req: AuthenticatedRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      const id = parseInt(req.params.id, 10);
      const { status, comments } = req.body;
      const orderRepo = RepositoryFactory.getOrderRepository();

      const updated = status === 'CANCELADO'
        ? await orderRepo.cancelOrder(id, req.user?.userId, comments)
        : await orderRepo.updateStatus(id, status, req.user?.userId, comments);
      if (!updated) {
        res.status(404).json({
          success: false,
          error: { code: 'ORDER_NOT_FOUND', message: `Pedido con ID ${id} no encontrado.` }
        });
        return;
      }

      res.status(200).json({
        success: true,
        message: `El pedido fue actualizado satisfactoriamente al estado: ${status}`,
        data: updated
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route POST /api/orders/:id/cancel
   * @desc Anula el pedido y reincorpora automáticamente las existencias de stock a las variantes de producto.
   * @access Protegido (ADMIN / OPERATOR)
   * @param id ID del pedido
   * @body { reason?: string }
   */
  public static async cancelOrder(req: AuthenticatedRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      const id = parseInt(req.params.id, 10);
      const { reason } = req.body;
      const orderRepo = RepositoryFactory.getOrderRepository();

      const cancelled = await orderRepo.cancelOrder(id, req.user?.userId, reason);
      if (!cancelled) {
        res.status(404).json({
          success: false,
          error: { code: 'ORDER_NOT_FOUND', message: `Pedido con ID ${id} no encontrado.` }
        });
        return;
      }

      res.status(200).json({
        success: true,
        message: 'Pedido cancelado satisfactoriamente y existencias reincorporadas al inventario.',
        data: cancelled
      });
    } catch (error) {
      next(error);
    }
  }
}

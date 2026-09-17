/**
 * @file product.controller.ts
 * @description Controlador de Catálogo de Productos y Control de Existencias de Stock.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Funcionalidades:
 * - Consulta de catálogo con filtrado multicriterio y búsqueda por coincidencia textual.
 * - Registro y actualización de fichas técnicas de indumentaria textil.
 * - Modificación de stock por variante de talla y color.
 * - Alertas tempranas de quiebre de stock (`stock <= alert_threshold`).
 * - Borrado lógico para preservar integridad referencial de pedidos históricos.
 */

import { Request, Response, NextFunction } from 'express';
import { RepositoryFactory } from '../infrastructure/repositories/factory';

export class ProductController {
  /**
   * @route GET /api/products
   * @desc Lista productos del catálogo con soporte para filtros por categoría, estado activo y búsqueda.
   * @access Público
   * @query { categoryId?: number, isActive?: boolean, search?: string }
   */
  public static async listProducts(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const categoryId = req.query.categoryId ? parseInt(req.query.categoryId as string, 10) : undefined;
      const isActive = req.query.isActive !== undefined ? req.query.isActive === 'true' : undefined;
      const search = req.query.search as string | undefined;

      const productRepo = RepositoryFactory.getProductRepository();
      const products = await productRepo.listAll({ categoryId, isActive, search });

      res.status(200).json({
        success: true,
        count: products.length,
        data: products
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route GET /api/products/:id
   * @desc Obtiene el detalle técnico y variantes de un producto por su identificador.
   * @access Público
   * @param id Identificador numérico del producto
   */
  public static async getProductById(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const id = parseInt(req.params.id, 10);
      const productRepo = RepositoryFactory.getProductRepository();
      const product = await productRepo.findById(id);

      if (!product) {
        res.status(404).json({
          success: false,
          error: { code: 'PRODUCT_NOT_FOUND', message: `Producto con ID ${id} no encontrado en el catálogo.` }
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: product
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route POST /api/products
   * @desc Registra un nuevo producto con su conjunto inicial de variantes de talla/color.
   * @access Protegido (Solo Administradores - RBAC: ADMIN)
   * @body CreateProductSchema
   */
  public static async createProduct(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const productRepo = RepositoryFactory.getProductRepository();
      const product = await productRepo.create(req.body);

      res.status(201).json({
        success: true,
        message: 'Producto y variantes registrados exitosamente en el catálogo.',
        data: product
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route PUT /api/products/:id
   * @desc Actualiza la ficha técnica, precio base o metadatos de un producto.
   * @access Protegido (Solo Administradores - RBAC: ADMIN)
   * @param id Identificador del producto
   */
  public static async updateProduct(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const id = parseInt(req.params.id, 10);
      const productRepo = RepositoryFactory.getProductRepository();
      const updated = await productRepo.update(id, req.body);

      if (!updated) {
        res.status(404).json({
          success: false,
          error: { code: 'PRODUCT_NOT_FOUND', message: `Producto con ID ${id} no encontrado.` }
        });
        return;
      }

      res.status(200).json({
        success: true,
        message: 'Producto actualizado exitosamente.',
        data: updated
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route PATCH /api/products/variant/:variantId/stock
   * @desc Ajusta las unidades disponibles de una variante (ingreso de lote de confección o merma).
   * @access Protegido (ADMIN / OPERATOR)
   * @param variantId Identificador de la variante
   * @body { quantityDelta: number }
   */
  public static async updateStock(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const variantId = parseInt(req.params.variantId, 10);
      const { quantityDelta } = req.body;
      const productRepo = RepositoryFactory.getProductRepository();

      const variant = await productRepo.updateVariantStock(variantId, quantityDelta);

      res.status(200).json({
        success: true,
        message: 'Stock de la variante actualizado correctamente.',
        data: variant
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route DELETE /api/products/:id
   * @desc Deshabilita un producto del catálogo (borrado lógico para preservar integridad histórica).
   * @access Protegido (Solo Administradores - RBAC: ADMIN)
   * @param id Identificador del producto
   */
  public static async deleteProduct(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const id = parseInt(req.params.id, 10);
      const productRepo = RepositoryFactory.getProductRepository();
      const success = await productRepo.delete(id);

      if (!success) {
        res.status(404).json({
          success: false,
          error: { code: 'PRODUCT_NOT_FOUND', message: `Producto con ID ${id} no encontrado.` }
        });
        return;
      }

      res.status(200).json({
        success: true,
        message: 'Producto deshabilitado del catálogo exitosamente.'
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route GET /api/products/alerts/low-stock
   * @desc Retorna la lista de todas las variantes que han alcanzado o cruzado su umbral de alerta de existencias.
   * @access Protegido (ADMIN / OPERATOR)
   */
  public static async getLowStockAlerts(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const productRepo = RepositoryFactory.getProductRepository();
      const alerts = await productRepo.getLowStockVariants();

      res.status(200).json({
        success: true,
        count: alerts.length,
        data: alerts
      });
    } catch (error) {
      next(error);
    }
  }
}

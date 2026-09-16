/**
 * @file client.controller.ts
 * @description Controlador de Directorio de Clientes (CRM de Despacho y Envíos).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Funcionalidades:
 * - Autocompletado y búsqueda rápida de clientes recurrentes en la toma de pedidos.
 * - Registro y actualización de direcciones de despacho y referencias para delivery en Lima.
 */

import { Request, Response, NextFunction } from 'express';
import { RepositoryFactory } from '../infrastructure/repositories/factory';

export class ClientController {
  /**
   * @route GET /api/clients
   * @desc Lista clientes con soporte para búsqueda rápida por nombre, teléfono o distrito.
   * @access Protegido (ADMIN / OPERATOR)
   * @query { search?: string }
   */
  public static async listClients(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const search = req.query.search as string | undefined;
      const clientRepo = RepositoryFactory.getClientRepository();
      const clients = await clientRepo.listAll(search);

      res.status(200).json({
        success: true,
        count: clients.length,
        data: clients
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route GET /api/clients/:id
   * @desc Obtiene la ficha de un cliente por su ID.
   * @access Protegido (ADMIN / OPERATOR)
   * @param id Identificador del cliente
   */
  public static async getClientById(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const id = parseInt(req.params.id, 10);
      const clientRepo = RepositoryFactory.getClientRepository();
      const client = await clientRepo.findById(id);

      if (!client) {
        res.status(404).json({
          success: false,
          error: { code: 'CLIENT_NOT_FOUND', message: `Cliente con ID ${id} no encontrado.` }
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: client
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route POST /api/clients
   * @desc Registra un nuevo cliente con sus datos de contacto y entrega.
   * @access Protegido (ADMIN / OPERATOR)
   * @body CreateClientSchema
   */
  public static async createClient(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const clientRepo = RepositoryFactory.getClientRepository();
      const client = await clientRepo.create(req.body);

      res.status(201).json({
        success: true,
        message: 'Cliente registrado exitosamente en el directorio.',
        data: client
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route PUT /api/clients/:id
   * @desc Actualiza la dirección o teléfono de contacto de un cliente.
   * @access Protegido (ADMIN / OPERATOR)
   * @param id Identificador del cliente
   */
  public static async updateClient(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const id = parseInt(req.params.id, 10);
      const clientRepo = RepositoryFactory.getClientRepository();
      const updated = await clientRepo.update(id, req.body);

      if (!updated) {
        res.status(404).json({
          success: false,
          error: { code: 'CLIENT_NOT_FOUND', message: `Cliente con ID ${id} no encontrado.` }
        });
        return;
      }

      res.status(200).json({
        success: true,
        message: 'Datos del cliente actualizados exitosamente.',
        data: updated
      });
    } catch (error) {
      next(error);
    }
  }
}

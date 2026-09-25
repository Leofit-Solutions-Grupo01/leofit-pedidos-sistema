/**
 * @file factory.ts
 * @description Fábrica de Repositorios (Factory Pattern & Dependency Injection).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Propósito Arquitectónico:
 * 1. Desacoplamiento (Clean Architecture): Los controladores dependen de interfaces de dominio (IOrderRepository, etc.)
 *    y nunca de implementaciones concretas de base de datos.
 * 2. Fallback Transparente y Alta Disponibilidad: Si PostgreSQL está en línea, despacha repositorios `pg` con transacciones ACID.
 *    Si la base de datos no está disponible (ej. suites de pruebas en CI/CD sin Postgres o cortes transitorios),
 *    despacha instancias `MemoryRepository` precargadas sin quebrar la API REST.
 * 3. Cache de Instancias Singleton: Evita la instanciación redundante en cada petición HTTP, reutilizando conexiones.
 */

import { isPostgresAvailable } from '../../config/database';
import {
  IUserRepository,
  ICategoryRepository,
  IProductRepository,
  IClientRepository,
  IOrderRepository
} from '../../domain/repositories/interfaces';
import {
  MemoryUserRepository,
  MemoryCategoryRepository,
  MemoryProductRepository,
  MemoryClientRepository,
  MemoryOrderRepository
} from './memory.repositories';
import {
  PgUserRepository,
  PgCategoryRepository,
  PgProductRepository,
  PgClientRepository,
  PgOrderRepository
} from './pg.repositories';

// Instancias Singleton en memoria (para pruebas, CI y fallback)
const memoryUserRepo = new MemoryUserRepository();
const memoryCategoryRepo = new MemoryCategoryRepository();
const memoryProductRepo = new MemoryProductRepository();
const memoryClientRepo = new MemoryClientRepository();
const memoryOrderRepo = new MemoryOrderRepository();

// Instancias Singleton de producción (PostgreSQL 16)
const pgUserRepo = new PgUserRepository();
const pgCategoryRepo = new PgCategoryRepository();
const pgProductRepo = new PgProductRepository();
const pgClientRepo = new PgClientRepository();
const pgOrderRepo = new PgOrderRepository();

export class RepositoryFactory {
  /**
   * Obtiene la instancia activa del repositorio de Usuarios.
   * @returns {IUserRepository} Implementación PostgreSQL o memoria.
   */
  public static getUserRepository(): IUserRepository {
    return isPostgresAvailable() ? pgUserRepo : memoryUserRepo;
  }

  /**
   * Obtiene la instancia activa del repositorio de Categorías.
   * @returns {ICategoryRepository} Implementación PostgreSQL o memoria.
   */
  public static getCategoryRepository(): ICategoryRepository {
    return isPostgresAvailable() ? pgCategoryRepo : memoryCategoryRepo;
  }

  /**
   * Obtiene la instancia activa del repositorio de Productos e Inventario.
   * @returns {IProductRepository} Implementación PostgreSQL o memoria.
   */
  public static getProductRepository(): IProductRepository {
    return isPostgresAvailable() ? pgProductRepo : memoryProductRepo;
  }

  /**
   * Obtiene la instancia activa del repositorio de Clientes.
   * @returns {IClientRepository} Implementación PostgreSQL o memoria.
   */
  public static getClientRepository(): IClientRepository {
    return isPostgresAvailable() ? pgClientRepo : memoryClientRepo;
  }

  /**
   * Obtiene la instancia activa del repositorio de Pedidos y Trazabilidad.
   * @returns {IOrderRepository} Implementación PostgreSQL o memoria.
   */
  public static getOrderRepository(): IOrderRepository {
    return isPostgresAvailable() ? pgOrderRepo : memoryOrderRepo;
  }
}


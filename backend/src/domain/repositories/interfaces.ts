/**
 * @file interfaces.ts
 * @description Contratos de Interfaces para la Capa de Acceso a Datos (Repository Pattern / DAO).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos y Control de Inventario Multicanal
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Principios de Diseño Aplicados:
 * - Dependency Inversion Principle (DIP): Los módulos de alto nivel (Casos de Uso / Controladores)
 *   no dependen de implementaciones concretas de base de datos (PostgreSQL, MySQL, SQLite),
 *   sino de estas abstracciones de repositorio.
 * - Interface Segregation Principle (ISP): Contratos granulares y específicos por contexto delimitado.
 */

import {
  User,
  Product,
  ProductVariant,
  Category,
  Client,
  Order,
  OrderStatus,
  DashboardMetrics
} from '../entities/models';

/**
 * Contrato de persistencia para la gestión de usuarios y credenciales administrativas.
 */
export interface IUserRepository {
  /** Busca un usuario por su dirección de correo electrónico institucional */
  findByEmail(email: string): Promise<User | null>;
  /** Busca un usuario por su identificador primario */
  findById(id: number): Promise<User | null>;
  /** Registra un nuevo operador en el sistema con su contraseña previamente hasheada */
  create(user: Omit<User, 'id' | 'created_at' | 'updated_at'>): Promise<User>;
  /** Retorna el catálogo completo de usuarios registrados (omitiendo hashes sensibles) */
  listAll(): Promise<User[]>;
}

/**
 * Contrato de persistencia para el catálogo de categorías de indumentaria.
 */
export interface ICategoryRepository {
  /** Obtiene la totalidad de categorías activas */
  listAll(): Promise<Category[]>;
  /** Obtiene una categoría por su ID */
  findById(id: number): Promise<Category | null>;
  /** Registra una nueva categoría de prendas */
  create(category: Omit<Category, 'id' | 'created_at'>): Promise<Category>;
}

/**
 * Contrato de persistencia para la gestión del catálogo de productos y control de stock.
 */
export interface IProductRepository {
  /**
   * Consulta productos con soporte para filtros combinados y búsqueda por texto libre.
   */
  listAll(filters?: { categoryId?: number; isActive?: boolean; search?: string }): Promise<Product[]>;
  /** Obtiene la ficha técnica completa de un producto y todas sus variantes */
  findById(id: number): Promise<Product | null>;
  /** Busca una variante específica mediante su código SKU universal */
  findBySku(sku: string): Promise<ProductVariant | null>;
  /** Inserta un nuevo producto con sus variantes en una sola operación transaccional */
  create(product: Omit<Product, 'id' | 'created_at' | 'updated_at'>): Promise<Product>;
  /** Actualiza los metadatos o estado de un producto existente */
  update(id: number, product: Partial<Product>): Promise<Product | null>;
  /**
   * Ajusta el stock de una variante de forma atómica.
   * @param variantId Identificador de la variante
   * @param quantityDelta Cantidad a sumar (positivo) o restar (negativo)
   */
  updateVariantStock(variantId: number, quantityDelta: number): Promise<ProductVariant | null>;
  /** Realiza el borrado lógico (`is_active = false`) de un producto */
  delete(id: number): Promise<boolean>;
  /** Retorna todas las variantes cuyo stock actual es menor o igual a su umbral de alerta */
  getLowStockVariants(): Promise<Array<ProductVariant & { productName: string }>>;
}

/**
 * Contrato de persistencia para el directorio de clientes (CRM de despacho).
 */
export interface IClientRepository {
  /** Lista clientes con filtro opcional de búsqueda por nombre, teléfono o distrito */
  listAll(search?: string): Promise<Client[]>;
  /** Busca un cliente por su ID */
  findById(id: number): Promise<Client | null>;
  /** Busca un cliente por su número de teléfono celular / WhatsApp */
  findByPhone(phone: string): Promise<Client | null>;
  /** Registra un nuevo cliente para envíos */
  create(client: Omit<Client, 'id' | 'created_at' | 'updated_at'>): Promise<Client>;
  /** Actualiza la información de contacto o dirección del cliente */
  update(id: number, client: Partial<Client>): Promise<Client | null>;
}

/**
 * Objeto de Transferencia de Datos (DTO) para la creación integral de pedidos.
 */
export interface CreateOrderDTO {
  /** ID del cliente existente (si ya está registrado) */
  clientId?: number;
  /** Datos del cliente para auto-registro (si es un comprador nuevo) */
  clientData?: {
    fullName: string;
    phone: string;
    address: string;
    district: string;
    reference?: string;
  };
  /** ID del operador que registra la venta */
  userId?: number;
  /** Medio de pago acordado */
  paymentMethod: Order['payment_method'];
  /** Tarifa de delivery calculada en PEN */
  shippingCost: number;
  /** Notas u observaciones de entrega */
  notes?: string;
  /** Líneas de productos solicitadas con sus variantes y precios acordados */
  items: Array<{
    variantId: number;
    quantity: number;
    unitPrice: number;
  }>;
}

/**
 * Contrato de persistencia para la gestión transaccional de órdenes de compra.
 */
export interface IOrderRepository {
  /** Consulta pedidos aplicando filtros por estado, rangos de fecha y texto libre */
  listAll(filters?: { status?: OrderStatus; dateFrom?: string; dateTo?: string; search?: string }): Promise<Order[]>;
  /** Obtiene el pedido completo con sus items, datos del cliente e historial de auditoría */
  findById(id: number): Promise<Order | null>;
  /** Consulta un pedido mediante su código único de tracking público (ej: LEO-20260302-001) */
  findByOrderNumber(orderNumber: string): Promise<Order | null>;
  /**
   * Crea un nuevo pedido ejecutando una transacción ACID:
   * 1. Verifica y reserva stock de cada variante con bloqueo de fila.
   * 2. Registra cabecera de orden y detalle de items.
   * 3. Inserta registro inicial en la pista de auditoría.
   */
  create(dto: CreateOrderDTO): Promise<Order>;
  /**
   * Ejecuta una transición controlada de estado en la máquina de estados del pedido.
   */
  updateStatus(orderId: number, newStatus: OrderStatus, userId?: number, comments?: string): Promise<Order | null>;
  /**
   * Anula un pedido y revierte el stock de todas las prendas asociadas al inventario.
   */
  cancelOrder(orderId: number, userId?: number, reason?: string): Promise<Order | null>;
  /**
   * Calcula y consolida las métricas agregadas de negocio para el Dashboard.
   */
  getMetrics(): Promise<DashboardMetrics>;
}

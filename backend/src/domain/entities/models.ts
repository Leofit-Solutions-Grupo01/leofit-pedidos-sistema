/**
 * @file models.ts
 * @description Entidades de Dominio Centrales del Negocio (Domain Layer - Clean Architecture).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos y Control de Inventario Multicanal
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Principios de Arquitectura Aplicados:
 * - Capa de Dominio Pura: Entidades agnósticas de frameworks, ORMs y librerías externas.
 * - Single Responsibility Principle (SRP): Cada modelo representa una entidad única del negocio textil.
 * - Tipado Estricto (Strict TypeScript): Enums, tipos literales e interfaces inmutables.
 */

/**
 * Roles de usuario admitidos en el sistema administrativo de Leofit.
 * - ADMIN: Acceso irrestricto (configuración, usuarios, catálogo, anulación y reportes).
 * - OPERATOR: Acceso operativo (toma de pedidos, actualización de estados y clientes).
 */
export type UserRole = 'ADMIN' | 'OPERATOR';

/**
 * Entidad de Usuario Administrativo.
 * Representa a los operadores del taller en Gamarra y administradores del negocio.
 */
export interface User {
  /** Identificador único autoincremental */
  id: number;
  /** Nombre completo del operador */
  name: string;
  /** Correo electrónico institucional (único en el sistema) */
  email: string;
  /** Hash criptográfico de la contraseña (generado con bcrypt, 10 rondas de salt) */
  password_hash: string;
  /** Rol asignado para control de acceso RBAC */
  role: UserRole;
  /** Marca temporal de creación del registro */
  created_at?: Date | string;
  /** Marca temporal de última modificación */
  updated_at?: Date | string;
}

/**
 * Entidad de Categoría de Indumentaria Deportiva.
 * Agrupa las prendas según su tipología (Polos Dry-Fit, Shorts 2 en 1, Joggers, etc.).
 */
export interface Category {
  /** Identificador único autoincremental */
  id: number;
  /** Nombre comercial de la categoría (ej: 'Polos Oversize Dry-Fit') */
  name: string;
  /** Descripción técnica y comercial del tipo de prenda */
  description?: string | null;
  /** Marca temporal de creación */
  created_at?: Date | string;
}

/**
 * Tallas estándar disponibles en el catálogo de prendas LeoFit.
 */
export type VariantSize = 'S' | 'M' | 'L' | 'XL' | 'XXL' | 'UNICA';

/**
 * Entidad de Variante de Producto (Stock por Talla y Color).
 * Representa la unidad de mantenimiento de existencias (SKU) real en almacén.
 */
export interface ProductVariant {
  /** Identificador único autoincremental de la variante */
  id: number;
  /** Llave foránea del producto padre en el catálogo */
  product_id: number;
  /** Talla de la prenda deportiva */
  size: VariantSize;
  /** Color de confección (ej: 'Negro', 'Crema', 'Gris Plomo') */
  color: string;
  /** Código único de inventario SKU (ej: 'POL-GYM-NEG-M') */
  sku: string;
  /** Unidades físicas disponibles en el taller */
  stock: number;
  /** Umbral para disparo automático de alerta de stock bajo (default: 3) */
  alert_threshold: number;
  /** Marca temporal de creación */
  created_at?: Date | string;
  /** Marca temporal de última modificación */
  updated_at?: Date | string;
}

/**
 * Entidad de Producto Base (Catálogo).
 * Agrupa una o múltiples variantes de tallas/colores con su ficha técnica y precio base.
 */
export interface Product {
  /** Identificador único autoincremental */
  id: number;
  /** Llave foránea de la categoría a la que pertenece */
  category_id: number;
  /** Nombre de la categoría asociada (unión en consultas) */
  category_name?: string;
  /** Nombre comercial del producto */
  name: string;
  /** Ficha técnica, composición textil (ej: Algodón peinado 24/1) y características */
  description?: string | null;
  /** Precio de venta base en Soles (PEN) */
  base_price: number;
  /** URL de la fotografía de alta resolución de la prenda */
  image_url?: string | null;
  /** Bandera de visibilidad (borrado lógico) */
  is_active: boolean;
  /** Colección de variantes de inventario asociadas al producto */
  variants?: ProductVariant[];
  /** Marca temporal de creación */
  created_at?: Date | string;
  /** Marca temporal de última modificación */
  updated_at?: Date | string;
}

/**
 * Entidad de Cliente (CRM).
 * Almacena los datos de contacto y despacho para el ruteo de entregas en Lima Metropolitana.
 */
export interface Client {
  /** Identificador único autoincremental */
  id: number;
  /** Nombre y apellidos del comprador */
  full_name: string;
  /** Número de teléfono / WhatsApp para tracking y confirmaciones */
  phone: string;
  /** Dirección completa de entrega (Calle, Avenida, Número, Dpto) */
  address: string;
  /** Distrito de Lima Metropolitana (ej: 'Miraflores', 'San Isidro', 'Surquillo') */
  district: string;
  /** Referencia geográfica para el motorizado de delivery */
  reference?: string | null;
  /** Marca temporal de creación */
  created_at?: Date | string;
  /** Marca temporal de última modificación */
  updated_at?: Date | string;
}

/**
 * Estados permitidos en la máquina de estados del pedido:
 * 1. RECIBIDO: Pedido registrado por el canal de venta (WhatsApp/Web).
 * 2. PREPARACION: Prendas seleccionadas y empaquetadas en el taller de Gamarra.
 * 3. EN_CAMINO: Pedido entregado al courier/motorizado para despacho.
 * 4. ENTREGADO: Pedido recibido satisfactoriamente por el cliente final.
 * 5. CANCELADO: Anulación con reincorporación automática del stock al inventario.
 */
export type OrderStatus = 'RECIBIDO' | 'PREPARACION' | 'EN_CAMINO' | 'ENTREGADO' | 'CANCELADO';

/**
 * Métodos de pago admitidos en el flujo comercial.
 */
export type PaymentMethod = 'YAPE' | 'PLIN' | 'TRANSFERENCIA' | 'CONTRAENTREGA' | 'EFECTIVO';

/**
 * Entidad de Detalle de Item del Pedido (Order Item).
 * Representa una línea de compra con su precio unitario congelado al momento de la orden.
 */
export interface OrderItem {
  /** Identificador autoincremental de la línea */
  id?: number;
  /** Identificador del pedido al que pertenece */
  order_id?: number;
  /** Identificador de la variante de producto comprada */
  variant_id: number;
  /** Nombre comercial del producto (desnormalizado para auditoría) */
  product_name?: string;
  /** Talla solicitada */
  size?: VariantSize;
  /** Color solicitado */
  color?: string;
  /** Código SKU de la variante */
  sku?: string;
  /** Cantidad de prendas solicitadas */
  quantity: number;
  /** Precio unitario pactado al momento de la venta en PEN */
  unit_price: number;
  /** Subtotal de la línea (unit_price * quantity) en PEN */
  subtotal: number;
}

/**
 * Entidad de Auditoría y Trazabilidad de Estados (Order Status History).
 * Registra cada cambio de estado, el usuario responsable y los comentarios del operador.
 */
export interface OrderStatusHistory {
  /** Identificador único del evento de auditoría */
  id: number;
  /** Identificador del pedido auditado */
  order_id: number;
  /** Identificador del usuario/operador que realizó la transición */
  user_id?: number | null;
  /** Nombre del operador que ejecutó el cambio */
  user_name?: string | null;
  /** Estado anterior (null si es creación) */
  previous_status?: OrderStatus | null;
  /** Nuevo estado establecido */
  new_status: OrderStatus;
  /** Fecha y hora exacta del cambio de estado */
  changed_at: Date | string;
  /** Observaciones u anotaciones de la transición (ej: Guía de courier) */
  comments?: string | null;
}

/**
 * Entidad de Cabecera de Pedido (Order Aggregate Root).
 * Agrega el cliente, los items comprados y la pista de auditoría.
 */
export interface Order {
  /** Identificador único autoincremental */
  id: number;
  /** Código de seguimiento público único (ej: 'LEO-20260302-001') */
  order_number: string;
  /** Identificador del cliente */
  client_id: number;
  /** Entidad del cliente asociada */
  client?: Client;
  /** Identificador del usuario que tomó la orden */
  user_id?: number | null;
  /** Nombre del usuario creador */
  user_name?: string | null;
  /** Estado actual del pedido */
  status: OrderStatus;
  /** Subtotal sumado de los items en PEN */
  subtotal: number;
  /** Costo de envío según distrito en PEN */
  shipping_cost: number;
  /** Importe total a liquidar (subtotal + shipping_cost) en PEN */
  total_amount: number;
  /** Medio de pago acordado */
  payment_method: PaymentMethod;
  /** Notas e instrucciones especiales para el empaque o delivery */
  notes?: string | null;
  /** Líneas de productos asociadas al pedido */
  items?: OrderItem[];
  /** Historial cronológico de cambios de estado */
  history?: OrderStatusHistory[];
  /** Fecha y hora de creación de la orden */
  created_at?: Date | string;
  /** Fecha y hora de última actualización */
  updated_at?: Date | string;
}

/**
 * Métricas Agregadas para el Dashboard Ejecutivo y Panel Operativo.
 */
export interface DashboardMetrics {
  /** Conteo total de pedidos procesados */
  totalOrders: number;
  /** Distribución de pedidos por cada estado del flujo */
  ordersByStatus: Record<OrderStatus, number>;
  /** Facturación bruta acumulada (excluyendo cancelados) en PEN */
  totalRevenue: number;
  /** Cantidad de variantes en nivel crítico de inventario */
  lowStockCount: number;
  /** Listado de los pedidos más recientes */
  recentOrders: Order[];
  /** Ranking de los 5 productos más vendidos */
  topSellingProducts: Array<{
    productId: number;
    name: string;
    totalQuantity: number;
    totalRevenue: number;
  }>;
}

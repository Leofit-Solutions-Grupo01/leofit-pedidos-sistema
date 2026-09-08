/**
 * @file mockData.ts
 * @description Modelos de datos TypeScript, datasets sintéticos y lógica de negocio para LeoFit
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

export interface Producto {
  id: string;
  nombre: string;
  categoria: "Deportiva" | "Casual" | "Accesorios";
  talla: string;
  color: string;
  precio: number;
  stock: number;
}

export interface ItemPedido {
  productoId: string;
  nombre: string;
  cantidad: number;
  precio: number;
}

export type EstadoPedido = "Recibido" | "Preparación" | "Camino" | "Entregado" | "Cancelado";
export type TipoEnvio = "Local" | "Nacional";
export type AgenciaEncomienda = "Shalom" | "Olva Courier" | "Marvisur" | "Flores Hermanos" | "Otra";
export type MetodoPago = "Yape" | "Plin" | "Transferencia BCP" | "Transferencia BBVA" | "Contra Entrega" | "Tarjeta/Link";

export interface CuponPromocional {
  codigo: string;
  descuento: number;
  descripcion: string;
  minimoCompra?: number;
}

export const CUPONES_VALIDOS: CuponPromocional[] = [
  { codigo: "LEOFIT10", descuento: 10, descripcion: "Descuento de bienvenida S/ 10.00" },
  { codigo: "PROMOVERANO", descuento: 15, descripcion: "Campaña Verano S/ 15.00", minimoCompra: 80 },
  { codigo: "ENVIOGRATIS", descuento: 8, descripcion: "Cupón Delivery Gratis S/ 8.00" },
  { codigo: "VICTORVIP", descuento: 20, descripcion: "Descuento VIP Clientes Frecuentes S/ 20.00", minimoCompra: 120 },
];

export interface Cliente {
  nombre: string;
  telefono: string;
  direccion: string;
  dniRuc?: string;
  distrito?: string;
  referencia?: string;
}

export interface Pedido {
  id: string;
  numero: string; // formato LFT-NNN
  canal: "WhatsApp" | "Llamada" | "Sistema";
  cliente: Cliente;
  tipoEnvio?: TipoEnvio;
  ciudadDestino?: string;
  agenciaEncomienda?: AgenciaEncomienda;
  numeroGuia?: string;
  items: ItemPedido[];
  total: number;
  costoDelivery: number;
  descuento: number;
  cuponAplicado?: string;
  metodoPago: MetodoPago;
  numeroOperacion?: string;
  estado: EstadoPedido;
  fecha: string;       // fecha de creación (YYYY-MM-DD)
  fechaEntrega?: string; // fecha y hora real de entrega
  notas?: string;
}

export const productosIniciales: Producto[] = [
  { id: "p1", nombre: "Camiseta Deportiva Pro", categoria: "Deportiva", talla: "M", color: "Rojo", precio: 49.9, stock: 20 },
  { id: "p2", nombre: "Pantalón Jogger Tech", categoria: "Casual", talla: "L", color: "Negro", precio: 79.9, stock: 15 },
  { id: "p3", nombre: "Zapatillas Running X", categoria: "Deportiva", talla: "42", color: "Blanco", precio: 199.9, stock: 10 },
  { id: "p4", nombre: "Gorra Deportiva Aerofit", categoria: "Accesorios", talla: "Único", color: "Azul", precio: 29.9, stock: 4 }, // Urgencia stock
  { id: "p5", nombre: "Mochila Gym Impermeable", categoria: "Accesorios", talla: "Único", color: "Negro", precio: 89.9, stock: 3 }, // Urgencia stock
];

export const pedidosIniciales: Pedido[] = [
  {
    id: "o1", numero: "LFT-001", canal: "WhatsApp",
    cliente: {
      nombre: "Carlos Mendoza",
      telefono: "987654321",
      dniRuc: "72458910",
      distrito: "Miraflores",
      direccion: "Av. Arequipa 1234, Dpto 402",
      referencia: "Frente al Parque Kennedy, timbre blanco",
    },
    tipoEnvio: "Local", ciudadDestino: "Lima Capital",
    items: [{ productoId: "p1", nombre: "Camiseta Deportiva Pro", cantidad: 2, precio: 49.9 }],
    total: 99.8, costoDelivery: 8, descuento: 0,
    metodoPago: "Yape", numeroOperacion: "OP-982143",
    estado: "Recibido", fecha: "2026-08-24",  // 3 días atrás → EN RIESGO
    notas: "Cliente prefiere entrega por la mañana",
  },
  {
    id: "o2", numero: "LFT-002", canal: "WhatsApp",
    cliente: {
      nombre: "María García",
      telefono: "912345678",
      dniRuc: "45891234",
      distrito: "Lima Centro",
      direccion: "Jr. Tacna 567",
      referencia: "A media cuadra de la Iglesia Las Nazarenas",
    },
    tipoEnvio: "Local", ciudadDestino: "Lima Capital",
    items: [{ productoId: "p2", nombre: "Pantalón Jogger Tech", cantidad: 1, precio: 79.9 }],
    total: 79.9, costoDelivery: 5, descuento: 0,
    metodoPago: "Contra Entrega",
    estado: "Recibido", fecha: "2026-08-27",
  },
  {
    id: "o3", numero: "LFT-003", canal: "Llamada",
    cliente: {
      nombre: "Luis Torres",
      telefono: "956789012",
      dniRuc: "10745892",
      distrito: "San Isidro",
      direccion: "Calle Las Flores 89",
      referencia: "Cerca al Hotel Cars, portón negro",
    },
    tipoEnvio: "Local", ciudadDestino: "Lima Capital",
    items: [{ productoId: "p3", nombre: "Zapatillas Running X", cantidad: 1, precio: 199.9 }],
    total: 199.9, costoDelivery: 10, descuento: 0,
    metodoPago: "Transferencia BCP", numeroOperacion: "BCP-8834120",
    estado: "Camino", fecha: "2026-08-26",
    notas: "Dejar con el portero si no hay nadie",
  },
  {
    id: "o4", numero: "LFT-004", canal: "WhatsApp",
    cliente: {
      nombre: "Ana Rodríguez",
      telefono: "934567890",
      dniRuc: "71239084",
      distrito: "Trujillo",
      direccion: "Agencia Shalom - Av. España 1020, Trujillo",
      referencia: "Recojo en agencia Shalom España con DNI",
    },
    tipoEnvio: "Nacional", ciudadDestino: "Trujillo, La Libertad", agenciaEncomienda: "Shalom", numeroGuia: "SH-789412",
    items: [
      { productoId: "p4", nombre: "Gorra Deportiva Aerofit", cantidad: 2, precio: 29.9 },
      { productoId: "p1", nombre: "Camiseta Deportiva Pro", cantidad: 1, precio: 49.9 },
    ],
    total: 109.7, costoDelivery: 15, descuento: 5, cuponAplicado: "LEOFIT10",
    metodoPago: "Yape", numeroOperacion: "YP-443912",
    estado: "Camino", fecha: "2026-08-27",
    notas: "Envío interprovincial vía encomienda Shalom",
  },
  {
    id: "o5", numero: "LFT-005", canal: "Sistema",
    cliente: {
      nombre: "Pedro Quispe",
      telefono: "978901234",
      dniRuc: "09458123",
      distrito: "Breña",
      direccion: "Jr. Independencia 234",
      referencia: "Alt. cuadra 12 de Av. Brasil",
    },
    tipoEnvio: "Local", ciudadDestino: "Lima Capital",
    items: [{ productoId: "p5", nombre: "Mochila Gym Impermeable", cantidad: 1, precio: 89.9 }],
    total: 89.9, costoDelivery: 8, descuento: 0,
    metodoPago: "Plin", numeroOperacion: "PL-009182",
    estado: "Entregado", fecha: "2026-08-25",
    fechaEntrega: "2026-08-25T15:30:00",
  },
  {
    id: "o6", numero: "LFT-006", canal: "WhatsApp",
    cliente: {
      nombre: "Rosa Huanca",
      telefono: "901234567",
      dniRuc: "41982345",
      distrito: "Arequipa",
      direccion: "Agencia Olva - Calle Mercaderes 402, Arequipa",
      referencia: "Recojo presencial Olva Courier",
    },
    tipoEnvio: "Nacional", ciudadDestino: "Arequipa", agenciaEncomienda: "Olva Courier", numeroGuia: "OLV-993210",
    items: [{ productoId: "p2", nombre: "Pantalón Jogger Tech", cantidad: 2, precio: 79.9 }],
    total: 159.8, costoDelivery: 18, descuento: 0,
    metodoPago: "Transferencia BBVA", numeroOperacion: "BBVA-394819",
    estado: "Entregado", fecha: "2026-08-24",
    fechaEntrega: "2026-08-24T11:15:00",
  },
  {
    id: "o7", numero: "LFT-007", canal: "Llamada",
    cliente: {
      nombre: "Jorge Sánchez",
      telefono: "923456789",
      dniRuc: "48291044",
      distrito: "Callao",
      direccion: "Av. Colonial 890",
      referencia: "Frente al Mall Aventura Plaza Callao",
    },
    tipoEnvio: "Local", ciudadDestino: "Callao",
    items: [{ productoId: "p3", nombre: "Zapatillas Running X", cantidad: 1, precio: 199.9 }],
    total: 199.9, costoDelivery: 12, descuento: 0,
    metodoPago: "Contra Entrega",
    estado: "Entregado", fecha: "2026-08-23",
    fechaEntrega: "2026-08-23T14:00:00",
  },
  {
    id: "o8", numero: "LFT-008", canal: "WhatsApp",
    cliente: {
      nombre: "Carmen Flores",
      telefono: "967890123",
      dniRuc: "70981234",
      distrito: "Jesús María",
      direccion: "Jr. Piura 345",
      referencia: "A espaldas de MiBanco, casa rejas verdes",
    },
    tipoEnvio: "Local", ciudadDestino: "Lima Capital",
    items: [
      { productoId: "p4", nombre: "Gorra Deportiva Aerofit", cantidad: 1, precio: 29.9 },
      { productoId: "p5", nombre: "Mochila Gym Impermeable", cantidad: 1, precio: 89.9 },
    ],
    total: 119.8, costoDelivery: 8, descuento: 0,
    metodoPago: "Contra Entrega",
    estado: "Recibido", fecha: "2026-08-27",
    notas: "Paga contra entrega en efectivo (llevar sencillo de 50)",
  },
  {
    id: "o9", numero: "LFT-009", canal: "WhatsApp",
    cliente: {
      nombre: "Miguel Palacios",
      telefono: "945678901",
      dniRuc: "23891044",
      distrito: "Cusco",
      direccion: "Agencia Marvisur - Av. Sol 500, Cusco",
      referencia: "Recojo agencia Marvisur Wanchaq",
    },
    tipoEnvio: "Nacional", ciudadDestino: "Cusco", agenciaEncomienda: "Marvisur", numeroGuia: "MVS-441209",
    items: [{ productoId: "p1", nombre: "Camiseta Deportiva Pro", cantidad: 3, precio: 49.9 }],
    total: 149.7, costoDelivery: 20, descuento: 0,
    metodoPago: "Yape", numeroOperacion: "YP-778210",
    estado: "Preparación", fecha: "2026-08-25", // 2 días atrás → EN RIESGO
    notas: "Llamar antes de enviar a agencia",
  },
  {
    id: "o10", numero: "LFT-010", canal: "Sistema",
    cliente: {
      nombre: "Sofía Villanueva",
      telefono: "989012345",
      dniRuc: "75641209",
      distrito: "Surquillo",
      direccion: "Calle Lima 456",
      referencia: "Alt. Mercado de Surquillo #1",
    },
    tipoEnvio: "Local", ciudadDestino: "Lima Capital",
    items: [{ productoId: "p2", nombre: "Pantalón Jogger Tech", cantidad: 1, precio: 79.9 }],
    total: 79.9, costoDelivery: 8, descuento: 0,
    metodoPago: "Tarjeta/Link", numeroOperacion: "CULQI-88129",
    estado: "Cancelado", fecha: "2026-08-22",
    notas: "Cliente canceló porque encontró talla diferente en tienda física",
  },
];

// Helper: un pedido está "en riesgo" si es Recibido/Preparación y tiene más de 24h sin atender
export function estaEnRiesgo(pedido: Pedido): boolean {
  const HOY = new Date().toISOString().split("T")[0];
  return (pedido.estado === "Recibido" || pedido.estado === "Preparación") && pedido.fecha < HOY;
}

// Helper: total de ingresos reales (solo Entregados)
export function calcularIngresos(pedidos: Pedido[]): number {
  return pedidos
    .filter((p) => p.estado === "Entregado")
    .reduce((acc, p) => acc + p.total, 0);
}

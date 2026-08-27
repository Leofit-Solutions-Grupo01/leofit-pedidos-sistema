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

// "En Riesgo" es un estado CALCULADO (no almacenado):
// un pedido está en riesgo si su estado es Recibido/Preparación y su fecha es anterior a hoy.
export type EstadoPedido = "Recibido" | "Preparación" | "Camino" | "Entregado" | "Cancelado";

export interface Pedido {
  id: string;
  numero: string; // formato LFT-NNN
  canal: "WhatsApp" | "Llamada" | "Sistema";
  cliente: {
    nombre: string;
    telefono: string;
    direccion: string;
  };
  items: ItemPedido[];
  total: number;
  costoDelivery: number;
  descuento: number;
  estado: EstadoPedido;
  fecha: string;       // fecha de creación (YYYY-MM-DD)
  fechaEntrega?: string; // fecha y hora real de entrega
  notas?: string;
}

export const productosIniciales: Producto[] = [
  { id: "p1", nombre: "Camiseta Deportiva", categoria: "Deportiva", talla: "M", color: "Rojo", precio: 49.9, stock: 20 },
  { id: "p2", nombre: "Pantalón Jogger", categoria: "Casual", talla: "L", color: "Negro", precio: 79.9, stock: 15 },
  { id: "p3", nombre: "Zapatillas Running", categoria: "Deportiva", talla: "42", color: "Blanco", precio: 199.9, stock: 10 },
  { id: "p4", nombre: "Gorra Deportiva", categoria: "Accesorios", talla: "Único", color: "Azul", precio: 29.9, stock: 4 },
  { id: "p5", nombre: "Mochila Gym", categoria: "Accesorios", talla: "Único", color: "Negro", precio: 89.9, stock: 3 },
];

// Pedidos con fechas variadas para demo:
// - Los marcados Recibido con fecha ANTERIOR a hoy → aparecerán como "En Riesgo"
// - Hoy es 2026-08-27
export const pedidosIniciales: Pedido[] = [
  {
    id: "o1", numero: "LFT-001", canal: "WhatsApp",
    cliente: { nombre: "Carlos Mendoza", telefono: "987654321", direccion: "Av. Arequipa 1234, Miraflores" },
    items: [{ productoId: "p1", nombre: "Camiseta Deportiva", cantidad: 2, precio: 49.9 }],
    total: 99.8, costoDelivery: 8, descuento: 0,
    estado: "Recibido", fecha: "2026-08-24",  // 3 días atrás → EN RIESGO
    notas: "Cliente prefiere entrega por la mañana",
  },
  {
    id: "o2", numero: "LFT-002", canal: "WhatsApp",
    cliente: { nombre: "María García", telefono: "912345678", direccion: "Jr. Tacna 567, Lima Centro" },
    items: [{ productoId: "p2", nombre: "Pantalón Jogger", cantidad: 1, precio: 79.9 }],
    total: 79.9, costoDelivery: 5, descuento: 0,
    estado: "Recibido", fecha: "2026-08-27",
  },
  {
    id: "o3", numero: "LFT-003", canal: "Llamada",
    cliente: { nombre: "Luis Torres", telefono: "956789012", direccion: "Calle Las Flores 89, San Isidro" },
    items: [{ productoId: "p3", nombre: "Zapatillas Running", cantidad: 1, precio: 199.9 }],
    total: 199.9, costoDelivery: 10, descuento: 0,
    estado: "Camino", fecha: "2026-08-26",
    notas: "Dejar con el portero si no hay nadie",
  },
  {
    id: "o4", numero: "LFT-004", canal: "WhatsApp",
    cliente: { nombre: "Ana Rodríguez", telefono: "934567890", direccion: "Av. Brasil 456, Pueblo Libre" },
    items: [
      { productoId: "p4", nombre: "Gorra Deportiva", cantidad: 2, precio: 29.9 },
      { productoId: "p1", nombre: "Camiseta Deportiva", cantidad: 1, precio: 49.9 },
    ],
    total: 109.7, costoDelivery: 8, descuento: 5,
    estado: "Preparación", fecha: "2026-08-27",
  },
  {
    id: "o5", numero: "LFT-005", canal: "Sistema",
    cliente: { nombre: "Pedro Quispe", telefono: "978901234", direccion: "Jr. Independencia 234, Breña" },
    items: [{ productoId: "p5", nombre: "Mochila Gym", cantidad: 1, precio: 89.9 }],
    total: 89.9, costoDelivery: 8, descuento: 0,
    estado: "Entregado", fecha: "2026-08-25",
    fechaEntrega: "2026-08-25T15:30:00",
  },
  {
    id: "o6", numero: "LFT-006", canal: "WhatsApp",
    cliente: { nombre: "Rosa Huanca", telefono: "901234567", direccion: "Calle Cusco 78, La Victoria" },
    items: [{ productoId: "p2", nombre: "Pantalón Jogger", cantidad: 2, precio: 79.9 }],
    total: 159.8, costoDelivery: 8, descuento: 0,
    estado: "Entregado", fecha: "2026-08-24",
    fechaEntrega: "2026-08-24T11:15:00",
  },
  {
    id: "o7", numero: "LFT-007", canal: "Llamada",
    cliente: { nombre: "Jorge Sánchez", telefono: "923456789", direccion: "Av. Colonial 890, Callao" },
    items: [{ productoId: "p3", nombre: "Zapatillas Running", cantidad: 1, precio: 199.9 }],
    total: 199.9, costoDelivery: 12, descuento: 0,
    estado: "Entregado", fecha: "2026-08-23",
    fechaEntrega: "2026-08-23T14:00:00",
  },
  {
    id: "o8", numero: "LFT-008", canal: "WhatsApp",
    cliente: { nombre: "Carmen Flores", telefono: "967890123", direccion: "Jr. Piura 345, Jesús María" },
    items: [
      { productoId: "p4", nombre: "Gorra Deportiva", cantidad: 1, precio: 29.9 },
      { productoId: "p5", nombre: "Mochila Gym", cantidad: 1, precio: 89.9 },
    ],
    total: 119.8, costoDelivery: 8, descuento: 0,
    estado: "Recibido", fecha: "2026-08-27",
    notas: "Paga contra entrega",
  },
  {
    id: "o9", numero: "LFT-009", canal: "WhatsApp",
    cliente: { nombre: "Miguel Palacios", telefono: "945678901", direccion: "Av. Universitaria 1567, San Miguel" },
    items: [{ productoId: "p1", nombre: "Camiseta Deportiva", cantidad: 3, precio: 49.9 }],
    total: 149.7, costoDelivery: 8, descuento: 0,
    estado: "Recibido", fecha: "2026-08-25", // 2 días atrás → EN RIESGO
    notas: "Llamar antes de enviar, trabaja en turno noche",
  },
  {
    id: "o10", numero: "LFT-010", canal: "Sistema",
    cliente: { nombre: "Sofía Villanueva", telefono: "989012345", direccion: "Calle Lima 456, Surquillo" },
    items: [{ productoId: "p2", nombre: "Pantalón Jogger", cantidad: 1, precio: 79.9 }],
    total: 79.9, costoDelivery: 8, descuento: 0,
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

import { Pedido } from "../data/mockData";

export interface CreateOrderDTO {
  clientData: {
    fullName: string;
    phone: string;
    address: string;
    district?: string;
    reference?: string;
  };
  paymentMethod: 'YAPE' | 'PLIN' | 'TRANSFERENCIA' | 'CONTRAENTREGA' | 'EFECTIVO';
  shippingCost: number;
  shippingType?: 'LIMA' | 'PROVINCIA';
  destinationCity?: string;
  shippingAgency?: string;
  trackingNumber?: string;
  notes?: string;
  items: Array<{
    variantId: number;
    quantity: number;
    unitPrice: number;
  }>;
}

export function toCreateOrderDTO(pedido: Pedido): CreateOrderDTO {
  if (!pedido.cliente.nombre || !pedido.cliente.nombre.trim()) {
    throw new Error("El nombre del cliente es obligatorio.");
  }
  if (!pedido.cliente.telefono || !pedido.cliente.telefono.trim()) {
    throw new Error("El teléfono del cliente es obligatorio.");
  }
  if (!pedido.cliente.direccion || !pedido.cliente.direccion.trim()) {
    throw new Error("La dirección de entrega es obligatoria.");
  }
  
  const tipoEnvioMapped = pedido.tipoEnvio === "Nacional" ? "PROVINCIA" : "LIMA";

  if (tipoEnvioMapped === "PROVINCIA") {
    if (!pedido.cliente.dniRuc || !pedido.cliente.dniRuc.trim()) {
      throw new Error("El DNI o RUC es obligatorio para envíos Nacionales.");
    }
    if (!pedido.ciudadDestino || !pedido.ciudadDestino.trim()) {
      throw new Error("La ciudad de destino es obligatoria para envíos Nacionales.");
    }
  }

  let paymentMapped: CreateOrderDTO['paymentMethod'];
  switch (pedido.metodoPago) {
    case "Yape": paymentMapped = "YAPE"; break;
    case "Plin": paymentMapped = "PLIN"; break;
    case "Transferencia BCP":
    case "Transferencia BBVA": paymentMapped = "TRANSFERENCIA"; break;
    case "Contra Entrega": paymentMapped = "CONTRAENTREGA"; break;
    default: throw new Error(`Método de pago no soportado: ${pedido.metodoPago}`);
  }

  const items = pedido.items.map(item => {
    const variantId = Number(item.productoId.replace(/\D/g, ''));
    if (!Number.isInteger(variantId) || variantId <= 0) {
      throw new Error(`variantId inválido: ${item.productoId}`);
    }
    return {
      variantId,
      quantity: item.cantidad,
      unitPrice: item.precio
    };
  });

  return {
    clientData: {
      fullName: pedido.cliente.nombre,
      phone: pedido.cliente.telefono,
      address: pedido.cliente.direccion,
      district: pedido.cliente.distrito,
      reference: pedido.cliente.referencia,
    },
    paymentMethod: paymentMapped,
    shippingCost: pedido.costoDelivery,
    shippingType: tipoEnvioMapped,
    destinationCity: pedido.ciudadDestino,
    shippingAgency: pedido.agenciaEncomienda,
    trackingNumber: pedido.numeroGuia,
    notes: pedido.notas,
    items
  };
}

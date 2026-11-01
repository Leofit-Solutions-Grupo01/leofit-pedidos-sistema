import { Pedido, Producto } from "../data/mockData";

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

export function mapCategoryName(catName?: string): Producto["categoria"] {
  if (!catName) return "Deportiva";
  const lower = catName.toLowerCase();
  if (lower.includes("accesorio") || lower.includes("strap") || lower.includes("gorra") || lower.includes("mochila")) {
    return "Accesorios";
  }
  if (lower.includes("jogger") || lower.includes("casual")) {
    return "Casual";
  }
  return "Deportiva";
}

/**
 * Normaliza y mapea productos desde el backend o catálogo local a la estructura que espera la interfaz de usuario.
 * Transforma estructuras relacionales con variantes (PostgreSQL) o estructuras planas (mock) de forma transparente.
 */
export function normalizeProductCatalog(rawProducts: unknown): Producto[] {
  if (!Array.isArray(rawProducts)) return [];

  const resultado: Producto[] = [];

  for (const p of rawProducts) {
    if (!p || typeof p !== "object") continue;

    const prod = p as Record<string, any>;
    const basePrice = Number(prod.precio ?? parseFloat(prod.base_price || "0")) || 0;
    const cat = prod.categoria || mapCategoryName(prod.category_name);

    // Si viene del backend con variantes (PostgreSQL DDL)
    if (Array.isArray(prod.variants) && prod.variants.length > 0) {
      for (const v of prod.variants) {
        if (!v) continue;
        const variantId = String(v.id);
        const talla = v.size || prod.talla || "M";
        const color = v.color || prod.color || "Negro";
        const stock = typeof v.stock === "number" ? Math.max(0, v.stock) : 0;
        const nombreBase = prod.name || prod.nombre || "Prenda LeoFit";

        resultado.push({
          id: variantId,
          nombre: `${nombreBase} - ${color} (${talla})`,
          categoria: cat,
          talla,
          color,
          precio: basePrice,
          stock,
        });
      }
    } else {
      // Si es un producto plano (mock o creado en frontend)
      resultado.push({
        id: String(prod.id ?? `p${resultado.length + 1}`),
        nombre: prod.nombre || prod.name || "Prenda LeoFit",
        categoria: cat,
        talla: prod.talla || "M",
        color: prod.color || "Negro",
        precio: basePrice,
        stock: typeof prod.stock === "number" ? Math.max(0, prod.stock) : 0,
      });
    }
  }

  return resultado;
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
    case "Tarjeta/Link": paymentMapped = "TRANSFERENCIA"; break;
    default: paymentMapped = "EFECTIVO";
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
      district: (pedido.cliente.distrito && pedido.cliente.distrito.trim()) ? pedido.cliente.distrito.trim() : 'Lima',
      reference: pedido.cliente.referencia,
    },
    paymentMethod: paymentMapped,
    shippingCost: pedido.costoDelivery,
    shippingType: tipoEnvioMapped,
    destinationCity: tipoEnvioMapped === "PROVINCIA" ? (pedido.ciudadDestino || 'Provincia') : undefined,
    shippingAgency: tipoEnvioMapped === "PROVINCIA" ? (pedido.agenciaEncomienda || 'Shalom') : undefined,
    trackingNumber: pedido.numeroGuia,
    notes: pedido.notas,
    items
  };
}

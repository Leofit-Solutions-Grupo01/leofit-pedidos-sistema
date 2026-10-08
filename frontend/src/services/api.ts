/**
 * @description Cliente HTTP del backend LeoFit + mapeadores entre el modelo de pantalla
 *              (Pedido / Producto, en español) y el modelo de la API (Order / Product, snake_case).
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 *
 * Decisiones de diseño:
 *  - Un `Producto` de pantalla equivale a UNA VARIANTE de la API (producto + talla + color),
 *    por eso su id es el id de la variante. Es lo que el backend necesita para crear pedidos.
 *  - La API no guarda algunos datos propios de la operación peruana (canal, DNI/RUC, agencia,
 *    guía, cupón, número de operación). Se serializan de forma compacta al final de `notes`
 *    (bloque [[LFT-META]]) y se recuperan al leer. Mejora futura: columnas propias en `orders`.
 */
import type {
  Pedido,
  Producto,
  EstadoPedido,
  MetodoPago,
  TipoEnvio,
  AgenciaEncomienda,
} from "../data/mockData";

/* ------------------------------------------------------------------ */
/* Configuración y sesión                                              */
/* ------------------------------------------------------------------ */

export const SESSION_KEY = "leofit_session";

/** URL base del backend, sin "/" final y sin "/api" (ej.: https://leofit-api.onrender.com). */
export const API_URL: string =
  ((import.meta as any).env?.VITE_API_URL as string | undefined)?.replace(/\/+$/, "") || "";

export const getToken = (): string | null => {
  try {
    return sessionStorage.getItem(SESSION_KEY);
  } catch {
    return null;
  }
};
export const setToken = (token: string): void => {
  try {
    sessionStorage.setItem(SESSION_KEY, token);
  } catch {
    /* sandbox / navegación privada */
  }
};
export const clearToken = (): void => {
  try {
    sessionStorage.removeItem(SESSION_KEY);
  } catch {
    /* noop */
  }
};

export class ApiError extends Error {
  status: number;
  code?: string;
  constructor(message: string, status: number, code?: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

async function request<T>(
  path: string,
  opts: { method?: string; body?: unknown; auth?: boolean } = {}
): Promise<{ json: any; data: T }> {
  const { method = "GET", body, auth = true } = opts;
  const headers: Record<string, string> = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  let res: Response;
  try {
    res = await fetch(`${API_URL}/api${path}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError("No se pudo conectar con el servidor. Verifique su conexión.", 0, "NETWORK");
  }

  let json: any = null;
  try {
    json = await res.json();
  } catch {
    /* respuesta sin cuerpo JSON */
  }

  if (!res.ok) {
    const detalles = Array.isArray(json?.error?.details)
      ? " (" + json.error.details.map((d: any) => `${d.field}: ${d.message}`).join("; ") + ")"
      : "";
    const msg = (json?.error?.message || `Error ${res.status}`) + detalles;
    if (res.status === 401 && auth) {
      clearToken();
      if (typeof window !== "undefined") window.dispatchEvent(new Event("leofit:unauthorized"));
    }
    throw new ApiError(msg, res.status, json?.error?.code);
  }
  return { json, data: json?.data as T };
}

/* ------------------------------------------------------------------ */
/* Tipos de la API (solo lo que usa el frontend)                       */
/* ------------------------------------------------------------------ */

interface ApiVariant {
  id: number;
  product_id: number;
  size: string;
  color: string;
  sku: string;
  stock: number;
}
interface ApiProduct {
  id: number;
  category_id: number;
  category_name?: string;
  name: string;
  base_price: number | string;
  is_active: boolean;
  variants?: ApiVariant[];
}
interface ApiOrderItem {
  variant_id: number;
  product_name?: string;
  quantity: number;
  unit_price: number | string;
}
interface ApiOrder {
  id: number;
  order_number: string;
  status: string;
  subtotal: number | string;
  shipping_cost: number | string;
  payment_method: string;
  notes?: string | null;
  created_at?: string;
  client?: { full_name: string; phone: string; address: string; district?: string; reference?: string | null };
  items?: ApiOrderItem[];
  history?: Array<{ new_status: string; changed_at: string }>;
}

/* ------------------------------------------------------------------ */
/* Catálogos de conversión                                             */
/* ------------------------------------------------------------------ */

const ESTADO_DESDE_API: Record<string, EstadoPedido> = {
  RECIBIDO: "Recibido",
  PREPARACION: "Preparación",
  EN_CAMINO: "Camino",
  ENTREGADO: "Entregado",
  CANCELADO: "Cancelado",
};
const ESTADO_HACIA_API: Record<EstadoPedido, string> = {
  Recibido: "RECIBIDO",
  Preparación: "PREPARACION",
  Camino: "EN_CAMINO",
  Entregado: "ENTREGADO",
  Cancelado: "CANCELADO",
};

const PAGO_HACIA_API: Record<MetodoPago, string> = {
  Yape: "YAPE",
  Plin: "PLIN",
  "Transferencia BCP": "TRANSFERENCIA",
  "Transferencia BBVA": "TRANSFERENCIA",
  "Tarjeta/Link": "TRANSFERENCIA",
  "Contra Entrega": "CONTRAENTREGA",
};
const PAGO_DESDE_API: Record<string, MetodoPago> = {
  YAPE: "Yape",
  PLIN: "Plin",
  TRANSFERENCIA: "Transferencia BCP",
  CONTRAENTREGA: "Contra Entrega",
  EFECTIVO: "Contra Entrega",
};

type Categoria = Producto["categoria"];
const CATEGORIA_DESDE_API: Record<string, Categoria> = {
  Camisetas: "Deportiva",
  Shorts: "Deportiva",
  "Tirantes / Bividis": "Deportiva",
  Joggers: "Casual",
  Accesorios: "Accesorios",
};
/** ids de categoría del seed (database/seeds.sql) usados como respaldo al crear productos */
const CATEGORIA_ID_RESPALDO: Record<Categoria, number> = { Deportiva: 1, Casual: 3, Accesorios: 5 };

const TALLAS_API = ["S", "M", "L", "XL", "XXL"];

/* ------------------------------------------------------------------ */
/* Metadatos propios guardados dentro de `notes`                       */
/* ------------------------------------------------------------------ */

const META_TAG = "\n[[LFT-META]]";
const NOTES_MAX = 500; // límite del esquema Zod / columna de notas

interface Meta {
  c?: Pedido["canal"];
  te?: TipoEnvio;
  cd?: string;
  ag?: AgenciaEncomienda;
  ng?: string;
  no?: string;
  dni?: string;
  cu?: string;
  ds?: number;
  mp?: MetodoPago;
}

export function codificarNotas(p: Pedido): string | undefined {
  const meta: Meta = {
    c: p.canal,
    te: p.tipoEnvio,
    cd: p.ciudadDestino,
    ag: p.agenciaEncomienda,
    ng: p.numeroGuia,
    no: p.numeroOperacion,
    dni: p.cliente.dniRuc,
    cu: p.cuponAplicado,
    ds: p.descuento || undefined,
    mp: p.metodoPago,
  };
  (Object.keys(meta) as Array<keyof Meta>).forEach((k) => meta[k] === undefined && delete meta[k]);
  const bloque = META_TAG + JSON.stringify(meta);
  const libre = Math.max(0, NOTES_MAX - bloque.length);
  const texto = (p.notas ?? "").slice(0, libre);
  return texto + bloque;
}

export function decodificarNotas(notes?: string | null): { notas?: string; meta: Meta } {
  if (!notes) return { meta: {} };
  const i = notes.indexOf(META_TAG);
  if (i === -1) return { notas: notes || undefined, meta: {} };
  let meta: Meta = {};
  try {
    meta = JSON.parse(notes.slice(i + META_TAG.length));
  } catch {
    /* metadatos corruptos: se ignoran */
  }
  return { notas: notes.slice(0, i) || undefined, meta };
}

/* ------------------------------------------------------------------ */
/* Mapeadores API -> pantalla                                          */
/* ------------------------------------------------------------------ */

const fechaLocal = (iso?: string): string => {
  if (!iso) return new Date().toLocaleDateString("en-CA");
  const d = new Date(iso);
  return isNaN(d.getTime()) ? iso.slice(0, 10) : d.toLocaleDateString("en-CA"); // YYYY-MM-DD
};

export interface ProductoRef {
  productId: number;
  categoryId: number;
}

export function mapearProductos(lista: ApiProduct[]): { productos: Producto[]; refs: Map<string, ProductoRef> } {
  const productos: Producto[] = [];
  const refs = new Map<string, ProductoRef>();
  for (const p of lista) {
    if (p.is_active === false) continue;
    for (const v of p.variants ?? []) {
      const id = String(v.id);
      productos.push({
        id,
        nombre: p.name,
        categoria: CATEGORIA_DESDE_API[p.category_name ?? ""] ?? "Accesorios",
        talla: v.size === "UNICA" ? "Único" : v.size,
        color: v.color,
        precio: Number(p.base_price),
        stock: Number(v.stock),
      });
      refs.set(id, { productId: p.id, categoryId: p.category_id });
    }
  }
  return { productos, refs };
}

export function mapearPedido(o: ApiOrder): Pedido {
  const { notas, meta } = decodificarNotas(o.notes);
  const items = (o.items ?? []).map((i) => ({
    productoId: String(i.variant_id),
    nombre: i.product_name ?? "",
    cantidad: Number(i.quantity),
    precio: Number(i.unit_price),
  }));
  const subtotal = Number(o.subtotal);
  const delivery = Number(o.shipping_cost);
  const descuento = meta.ds ?? 0;
  const entregado = o.history?.find((h) => h.new_status === "ENTREGADO");

  return {
    id: String(o.id),
    numero: o.order_number,
    canal: meta.c ?? "Sistema",
    cliente: {
      nombre: o.client?.full_name ?? "",
      telefono: o.client?.phone ?? "",
      direccion: o.client?.address ?? "",
      distrito: o.client?.district || undefined,
      referencia: o.client?.reference || undefined,
      dniRuc: meta.dni,
    },
    tipoEnvio: meta.te ?? "Local",
    ciudadDestino: meta.cd,
    agenciaEncomienda: meta.ag,
    numeroGuia: meta.ng,
    items,
    total: Math.max(0, Math.round((subtotal + delivery - descuento) * 100) / 100),
    costoDelivery: delivery,
    descuento,
    cuponAplicado: meta.cu,
    metodoPago: meta.mp ?? PAGO_DESDE_API[o.payment_method] ?? "Contra Entrega",
    numeroOperacion: meta.no,
    estado: ESTADO_DESDE_API[o.status] ?? "Recibido",
    fecha: fechaLocal(o.created_at),
    fechaEntrega: entregado?.changed_at,
    notas,
  };
}

/* ------------------------------------------------------------------ */
/* Mapeadores pantalla -> API                                          */
/* ------------------------------------------------------------------ */

export function construirCuerpoPedido(p: Pedido) {
  // Une líneas repetidas de una misma variante (restricción única order_id + variant_id)
  const porVariante = new Map<number, { variantId: number; quantity: number; unitPrice: number }>();
  for (const it of p.items) {
    const variantId = Number(it.productoId);
    if (!Number.isInteger(variantId) || variantId <= 0) {
      throw new ApiError(`El producto "${it.nombre}" no existe en el catálogo del servidor.`, 400, "INVALID_ITEM");
    }
    const previo = porVariante.get(variantId);
    if (previo) previo.quantity += it.cantidad;
    else porVariante.set(variantId, { variantId, quantity: it.cantidad, unitPrice: it.precio });
  }
  return {
    clientData: {
      fullName: p.cliente.nombre,
      phone: p.cliente.telefono.replace(/\s+/g, ""),
      address: p.cliente.direccion,
      district: p.cliente.distrito || p.ciudadDestino || "Lima",
      ...(p.cliente.referencia ? { reference: p.cliente.referencia } : {}),
    },
    paymentMethod: PAGO_HACIA_API[p.metodoPago] ?? "EFECTIVO",
    shippingCost: p.costoDelivery,
    notes: codificarNotas(p),
    items: Array.from(porVariante.values()),
  };
}

/** Convierte una talla de pantalla a una talla válida del catálogo y conserva lo que no cabe en el color. */
export function normalizarVariante(talla: string, color: string): { size: string; color: string } {
  const t = talla.trim().toUpperCase();
  if (TALLAS_API.includes(t)) return { size: t, color };
  if (t === "ÚNICO" || t === "UNICO" || t === "UNICA" || t === "ÚNICA") return { size: "UNICA", color };
  return { size: "UNICA", color: `${color} · T${talla}`.slice(0, 50) };
}

/* ------------------------------------------------------------------ */
/* Operaciones de alto nivel                                           */
/* ------------------------------------------------------------------ */

export const api = {
  async login(email: string, password: string): Promise<string> {
    const { data } = await request<{ token: string }>("/auth/login", {
      method: "POST",
      body: { email, password },
      auth: false,
    });
    return data.token;
  },

  async perfil(): Promise<void> {
    await request("/auth/profile");
  },

  async listarProductos() {
    const { data } = await request<ApiProduct[]>("/products?isActive=true");
    return mapearProductos(data ?? []);
  },

  async listarPedidos(): Promise<Pedido[]> {
    const { data } = await request<ApiOrder[]>("/orders?limit=100");
    return (data ?? []).map(mapearPedido);
  },

  async crearPedido(p: Pedido): Promise<Pedido> {
    const { data } = await request<ApiOrder>("/orders", { method: "POST", body: construirCuerpoPedido(p) });
    return mapearPedido(data);
  },

  async cambiarEstado(id: string, estado: EstadoPedido): Promise<Pedido> {
    const { data } = await request<ApiOrder>(`/orders/${id}/status`, {
      method: "PATCH",
      body: { status: ESTADO_HACIA_API[estado] },
    });
    return mapearPedido(data);
  },

  async crearProducto(p: Producto, categoryId?: number): Promise<void> {
    const v = normalizarVariante(p.talla, p.color);
    const sufijo = Date.now().toString(36).toUpperCase();
    const base = p.nombre.replace(/[^A-Za-z0-9]/g, "").toUpperCase().slice(0, 10) || "PROD";
    await request("/products", {
      method: "POST",
      body: {
        categoryId: categoryId ?? CATEGORIA_ID_RESPALDO[p.categoria],
        name: p.nombre,
        basePrice: p.precio,
        variants: [{ size: v.size, color: v.color, sku: `LF-${base}-${sufijo}`, stock: p.stock, alertThreshold: 3 }],
      },
    });
  },

  async editarProducto(p: Producto, ref: ProductoRef, stockActual: number, categoryId: number): Promise<void> {
    await request(`/products/${ref.productId}`, {
      method: "PUT",
      body: { name: p.nombre, basePrice: p.precio, categoryId },
    });
    const delta = p.stock - stockActual;
    if (delta !== 0) {
      await request(`/products/variant/${p.id}/stock`, { method: "PATCH", body: { quantityDelta: delta } });
    }
  },

  /** id de categoría del servidor para una categoría de pantalla (respaldo: ids del seed) */
  categoriaId(categoria: Categoria): number {
    return CATEGORIA_ID_RESPALDO[categoria];
  },

  async eliminarProducto(ref: ProductoRef): Promise<void> {
    await request(`/products/${ref.productId}`, { method: "DELETE" });
  },
};
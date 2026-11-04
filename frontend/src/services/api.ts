import { triggerSessionExpired, validateAndDecodeJwt } from './authGuard';

export class ApiError extends Error {
  public code: string;
  public status: number;

  constructor(codeOrMessage: string, messageOrStatus?: string | number, code?: string) {
    if (typeof messageOrStatus === 'number') {
      // Firma de Víctor: new ApiError(message, status, code)
      super(codeOrMessage);
      this.status = messageOrStatus;
      this.code = code || 'API_ERROR';
    } else {
      // Firma de Main: new ApiError(code, message)
      super(messageOrStatus || codeOrMessage);
      this.code = codeOrMessage;
      this.status = 0;
    }
    this.name = 'ApiError';
  }
}

export function getApiBaseUrl(): string {
  const envApiUrl = import.meta.env.VITE_API_URL;
  const baseUrl = envApiUrl !== undefined
    ? envApiUrl
    : (typeof window !== 'undefined' && window.location.hostname === 'localhost'
        ? 'http://localhost:4000'
        : 'https://leofit-backend-api.onrender.com');

  if (!baseUrl) {
    throw new Error('VITE_API_URL no está definido');
  }

  return baseUrl.replace(/\/+$/, '');
}

let inMemoryAccessToken: string | null = null;
let refreshPromise: Promise<boolean> | null = null;
const authListeners = new Set<(evt: 'logout' | 'refreshed') => void>();

export function setAccessToken(token: string | null): void {
  inMemoryAccessToken = token;
  if (typeof sessionStorage !== 'undefined') {
    if (token) {
      sessionStorage.setItem('leofit_session', token);
    } else {
      sessionStorage.removeItem('leofit_session');
    }
  }
}

export function getAccessToken(): string | null {
  if (inMemoryAccessToken) return inMemoryAccessToken;
  if (typeof sessionStorage !== 'undefined') {
    return sessionStorage.getItem('leofit_session');
  }
  return null;
}

export function onAuthEvent(fn: (evt: 'logout' | 'refreshed') => void): () => void {
  authListeners.add(fn);
  return () => {
    authListeners.delete(fn);
  };
}

function emitAuthEvent(evt: 'logout' | 'refreshed'): void {
  authListeners.forEach((listener) => {
    try {
      listener(evt);
    } catch {
      // Ignorar errores de observadores
    }
  });
}

/**
 * Ejecuta la renovación silenciosa del access token usando la cookie HttpOnly leofit_rt.
 * Implementa Single-Flight para deduplicar peticiones concurrentes a /api/auth/refresh.
 */
export async function doRefresh(): Promise<boolean> {
  if (!refreshPromise) {
    refreshPromise = (async () => {
      try {
        const baseUrl = getApiBaseUrl();
        const res = await fetch(`${baseUrl}/api/auth/refresh`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' }
        });

        if (!res.ok) {
          return false;
        }

        const data = await res.json();
        const newAccessToken = data?.data?.accessToken || data?.data?.token;
        if (newAccessToken) {
          setAccessToken(newAccessToken);
          emitAuthEvent('refreshed');
          return true;
        }
        return false;
      } catch {
        return false;
      } finally {
        refreshPromise = null;
      }
    })();
  }
  return refreshPromise;
}

export async function apiBootstrap(): Promise<boolean> {
  return doRefresh();
}

export async function apiLogout(): Promise<void> {
  try {
    const baseUrl = getApiBaseUrl();
    await fetch(`${baseUrl}/api/auth/logout`, {
      method: 'POST',
      credentials: 'include'
    });
  } catch {
    // Si la red falla, aseguramos la limpieza local
  } finally {
    setAccessToken(null);
    emitAuthEvent('logout');
  }
}

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {},
  cerrarSesionFn?: () => void
): Promise<T> {
  const currentToken = getAccessToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>)
  };

  if (currentToken) {
    const isSynthetic = currentToken.startsWith('token-mock-') || currentToken.startsWith('token-offline-');
    if (!isSynthetic) {
      headers['Authorization'] = `Bearer ${currentToken}`;
    }
  }

  const baseUrl = getApiBaseUrl();
  const url = endpoint.startsWith('http') ? endpoint : `${baseUrl}${endpoint}`;

  const method = (options.method || 'GET').toUpperCase();
  const hasIdempotencyKey = !!(headers['Idempotency-Key'] || headers['idempotency-key'] || headers['X-Idempotency-Key']);
  const isRetryable = method === 'GET' || hasIdempotencyKey;
  const maxRetries = isRetryable ? 2 : 0;

  let res: Response | null = null;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      res = await fetch(url, { ...options, headers, credentials: 'include' });
    } catch (error: any) {
      if (attempt < maxRetries && error.name !== 'AbortError') {
        const delayMs = Math.min(4000, 1000 * Math.pow(2, attempt) + Math.random() * 250);
        await new Promise((resolve) => setTimeout(resolve, delayMs));
        continue;
      }
      throw new ApiError('NETWORK_ERROR', error.message || 'Error de red');
    }

    // Si el servidor está procesando concurrentemente la misma Idempotency-Key (409) o en cold-start (502, 503, 504)
    const isConcurrentIdempotency = (res.status === 409 || res.status === 425) && hasIdempotencyKey;
    const isServerWakingOrDegraded = [502, 503, 504].includes(res.status);

    if (res && (isServerWakingOrDegraded || isConcurrentIdempotency) && attempt < maxRetries) {
      const retryAfter = res.headers ? res.headers.get('Retry-After') : null;
      let delayMs = Math.min(4000, 1000 * Math.pow(2, attempt) + Math.random() * 250);
      if (retryAfter) {
        const seconds = parseInt(retryAfter, 10);
        if (!isNaN(seconds) && seconds > 0) {
          delayMs = Math.min(seconds * 1000, 6000);
        }
      }
      await new Promise((resolve) => setTimeout(resolve, delayMs));
      continue;
    }

    break;
  }

  if (!res) {
    throw new ApiError('NETWORK_ERROR', 'No se pudo obtener respuesta del servidor');
  }

  // 401 Manejo con Refresh Silencioso (siempre que no estemos llamando a los endpoints de auth)
  if (res.status === 401 && !endpoint.includes('/api/auth/')) {
    const refreshed = await doRefresh();
    if (refreshed) {
      const newAuthToken = getAccessToken();
      const retryHeaders = {
        ...headers,
        ...(newAuthToken ? { Authorization: `Bearer ${newAuthToken}` } : {})
      };
      res = await fetch(url, { ...options, headers: retryHeaders, credentials: 'include' });
    }
  }

  if (!res.ok) {
    let errCode = 'UNKNOWN_ERROR';
    let errMessage = `HTTP Error ${res.status}`;
    
    try {
      const errorData = await res.json();
      if (errorData && !errorData.success && errorData.error) {
        errCode = errorData.error.code || errCode;
        errMessage = errorData.error.message || errMessage;
      }
    } catch {
      // Ignore if not json
    }

    const isTokenExpiredOrInvalid =
      res.status === 401 ||
      (res.status === 403 && (
        errCode === 'FORBIDDEN' ||
        errMessage.toLowerCase().includes('token') ||
        errMessage.toLowerCase().includes('expirado') ||
        errMessage.toLowerCase().includes('inválido') ||
        errMessage.toLowerCase().includes('sesión')
      ));

    if (isTokenExpiredOrInvalid) {
      setAccessToken(null);
      emitAuthEvent('logout');
      if (cerrarSesionFn) {
        triggerSessionExpired(errMessage || 'Token de sesión inválido o expirado. Inicie sesión nuevamente.');
        cerrarSesionFn();
      }
      throw new ApiError('UNAUTHORIZED', errMessage);
    }
    
    throw new ApiError(errCode, errMessage);
  }

  if (res.status === 204) {
    return {} as T;
  }

  try {
    const data = await res.json();
    if (data && typeof data === 'object' && 'success' in data) {
      if (!data.success) {
         throw new ApiError(data.error?.code || 'API_ERROR', data.error?.message || 'Error en la respuesta');
      }
      return data.data as T;
    }
    return data as T;
  } catch (e) {
    if (e instanceof ApiError) throw e;
    return {} as T;
  }
}


/* ------------------------------------------------------------------ */
/* Compatibilidad con Feature Branch: Víctor Cárdenas (Backend/Mappers) */
/* ------------------------------------------------------------------ */

export const SESSION_KEY = 'leofit_session';
export const API_URL = getApiBaseUrl();
export const getToken = getAccessToken;
export const setToken = setAccessToken;
export const clearToken = () => setAccessToken(null);

import type {
  Pedido,
  Producto,
  EstadoPedido,
  MetodoPago,
  TipoEnvio,
  AgenciaEncomienda,
} from '../data/mockData';

async function request<T>(
  path: string,
  opts: { method?: string; body?: unknown; auth?: boolean } = {}
): Promise<{ json: any; data: T }> {
  const { method = 'GET', body, auth = true } = opts;
  const headers: Record<string, string> = {};
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (auth) {
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;
  }

  let res: Response;
  try {
    const baseUrl = getApiBaseUrl();
    res = await fetch(`${baseUrl}/api${path}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError('No se pudo conectar con el servidor. Verifique su conexión.', 0, 'NETWORK');
  }

  let json: any = null;
  try {
    json = await res.json();
  } catch {
    /* respuesta sin cuerpo JSON */
  }

  if (!res.ok) {
    const detalles = Array.isArray(json?.error?.details)
      ? ' (' + json.error.details.map((d: any) => `${d.field}: ${d.message}`).join('; ') + ')'
      : '';
    const msg = (json?.error?.message || `Error ${res.status}`) + detalles;
    if (res.status === 401 && auth) {
      clearToken();
      if (typeof window !== 'undefined') window.dispatchEvent(new Event('leofit:unauthorized'));
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
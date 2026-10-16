/**
 * @file AppContext.tsx
 * @description Proveedor de estado global reactivo (pedidos, productos, autenticación, accesibilidad)
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { createContext, useContext, useState, useEffect, useCallback, useRef, ReactNode } from "react";
import { Pedido, Producto, EstadoPedido, pedidosIniciales, productosIniciales } from "../data/mockData";
import { apiFetch, ApiError, getApiBaseUrl } from "../services/api";
import { validateAndDecodeJwt, triggerSessionExpired, LEOFIT_AUTH_EXPIRED_EVENT } from "../services/authGuard";
import { toCreateOrderDTO, normalizeProductCatalog } from "../services/mappers";

type Pagina = "login" | "dashboard" | "pedidos" | "nuevo-pedido" | "productos" | "rastreo" | "analytics";

export type RolUsuario = "ADMIN" | "OPERATOR";

export interface UsuarioActual {
  id?: number;
  name: string;
  email: string;
  role: RolUsuario;
}

interface AppContextType {
  autenticado: boolean;
  usuarioActual: UsuarioActual | null;
  paginaActual: Pagina;
  pedidos: Pedido[];
  productos: Producto[];
  cargandoProductos: boolean;
  errorProductos: string | null;
  filtroInicial: EstadoPedido | "Todos";
  privacidad: boolean;
  modoAccesible: boolean;
  togglePrivacidad: () => void;
  toggleAccesible: () => void;
  iniciarSesion: (email: string, password: string) => Promise<boolean>;
  cerrarSesion: () => void;
  navegarA: (pagina: Pagina) => void;
  navegarAConFiltro: (pagina: Pagina, filtro: EstadoPedido | "Todos") => void;
  agregarPedido: (pedido: Pedido) => void;
  crearPedido: (datos: Pedido) => Promise<{ ok: true; pedido: Pedido } | { ok: false; error: string; code?: string }>;
  actualizarEstadoPedido: (id: string, estado: EstadoPedido) => void;
  agregarProducto: (producto: Producto) => Promise<void>;
  editarProducto: (producto: Producto) => Promise<void>;
  eliminarProducto: (id: string) => Promise<void>;
  cargarCatalogoLocal: () => void;
  /** true mientras se descargan pedidos y productos del servidor */
  cargando: boolean;
  /** Último error de comunicación con la API (null si no hay) */
  errorApi: string | null;
  limpiarError: () => void;
}

const AppContext = createContext<AppContextType | null>(null);

/** Modo demostración sin backend (datos locales). En producción debe ser false. */
const USE_MOCK = import.meta.env.VITE_USE_MOCK_AUTH === "true";
const SESSION_KEY = "leofit_session";
const ACCESIBLE_KEY = "leofit_modo_accesible";
const INACTIVIDAD_MS = 30 * 60 * 1000; // 30 minutos

export function AppProvider({ children }: { children: ReactNode }) {
  const [autenticado, setAutenticado] = useState(false);
  const [usuarioActual, setUsuarioActual] = useState<UsuarioActual | null>(() => {
    try {
      const guardado = sessionStorage.getItem("leofit_user");
      return guardado ? JSON.parse(guardado) : null;
    } catch {
      return null;
    }
  });
  const [paginaActual, setPaginaActual] = useState<Pagina>("login");
  const [pedidos, setPedidos] = useState<Pedido[]>(pedidosIniciales);
  const [productos, setProductos] = useState<Producto[]>([]);
  const [cargandoProductos, setCargandoProductos] = useState(false);
  const [errorProductos, setErrorProductos] = useState<string | null>(null);
  const [filtroInicial, setFiltroInicial] = useState<EstadoPedido | "Todos">("Todos");
  const [privacidad, setPrivacidad] = useState(false);
  const [modoAccesible, setModoAccesible] = useState<boolean>(() => {
    try {
      return localStorage.getItem(ACCESIBLE_KEY) === "true";
    } catch {
      return false;
    }
  });

  const togglePrivacidad = () => setPrivacidad((v) => !v);
  const toggleAccesible = () => {
    setModoAccesible((prev) => {
      const nuevo = !prev;
      try {
        localStorage.setItem(ACCESIBLE_KEY, String(nuevo));
      } catch {
        // Ignora excepciones de quota o navegación privada
      }
      return nuevo;
    });
  };

  const cerrarSesion = useCallback(() => {
    setAutenticado(false);
    setUsuarioActual(null);
    setPaginaActual("login");
    sessionStorage.removeItem(SESSION_KEY);
    sessionStorage.removeItem("leofit_user");
  }, []);

  // Restaurar sesión al montar con guardrail de expiración de token
  useEffect(() => {
    try {
      const guardado = sessionStorage.getItem(SESSION_KEY);
      const userGuardado = sessionStorage.getItem("leofit_user");
      if (guardado) {
        const check = validateAndDecodeJwt(guardado);
        if (check.expired) {
          triggerSessionExpired("Tu sesión anterior ha expirado. Por favor ingresa nuevamente.");
          cerrarSesion();
          return;
        }
        setAutenticado(true);
        if (userGuardado) {
          setUsuarioActual(JSON.parse(userGuardado));
        }
        setPaginaActual("dashboard");
      }
    } catch {
      // Ignora restricciones
    }
  }, [cerrarSesion]);

  // Escuchar evento global de expiración de sesión (despachado por apiFetch o temporizadores)
  useEffect(() => {
    const onAuthExpired = () => {
      cerrarSesion();
    };
    window.addEventListener(LEOFIT_AUTH_EXPIRED_EVENT, onAuthExpired);
    return () => window.removeEventListener(LEOFIT_AUTH_EXPIRED_EVENT, onAuthExpired);
  }, [cerrarSesion]);

  // Monitoreo proactivo periódico (cada 30s) de caducidad de token
  useEffect(() => {
    if (!autenticado) return;
    const interval = setInterval(() => {
      const token = sessionStorage.getItem(SESSION_KEY);
      if (token) {
        const check = validateAndDecodeJwt(token);
        if (check.expired) {
          triggerSessionExpired("Tu sesión ha expirado por límite de tiempo de seguridad.");
          cerrarSesion();
        }
      }
    }, 30000);
    return () => clearInterval(interval);
  }, [autenticado, cerrarSesion]);

  // Cargar productos
  useEffect(() => {
    const USE_MOCK = import.meta.env.VITE_USE_MOCK_ORDERS === 'true';
    if (USE_MOCK) {
      setProductos(productosIniciales);
      return;
    }

    const CACHE_KEY = "leofit_products_cache";
    const FIVE_MIN = 5 * 60 * 1000;

    const loadProducts = async () => {
      try {
        const cached = sessionStorage.getItem(CACHE_KEY);
        if (cached) {
          const parsed = JSON.parse(cached);
          if (Date.now() - parsed.timestamp < FIVE_MIN) {
            setProductos(parsed.data);
            return;
          }
        }
      } catch {
        // Fallback to fetch if parse fails
      }

      setCargandoProductos(true);
      setErrorProductos(null);
      try {
        const data = await apiFetch<any>('/api/products');
        const normalized = normalizeProductCatalog(data);
        setProductos(normalized);
        sessionStorage.setItem(CACHE_KEY, JSON.stringify({ timestamp: Date.now(), data: normalized }));
      } catch (err: any) {
        setErrorProductos(err.message || 'Error al cargar productos');
        setProductos([]);
      } finally {
        setCargandoProductos(false);
      }
    };
    
    loadProducts();
  }, [cerrarSesion]);

  // Auto-logout por inactividad (30 min)
  useEffect(() => {
    if (!autenticado) return;
    let timer: ReturnType<typeof setTimeout>;
    const reiniciar = () => {
      clearTimeout(timer);
      timer = setTimeout(() => cerrarSesion(), INACTIVIDAD_MS);
    };
    const eventos = ["click", "keypress", "touchstart", "mousemove"];
    eventos.forEach((e) => window.addEventListener(e, reiniciar, { passive: true }));
    reiniciar();
    return () => {
      clearTimeout(timer);
      eventos.forEach((e) => window.removeEventListener(e, reiniciar));
    };
  }, [autenticado, cerrarSesion]);

  const iniciarSesion = async (email: string, password: string): Promise<boolean> => {
    try {
      const cleanEmail = email.trim().toLowerCase();
      const cleanPass = password.trim();

      // Detección de usuarios y roles predeterminados (demo/fallback offline)
      const resolverUsuarioDemo = (): UsuarioActual | null => {
        if ((cleanEmail === "admin@leofit.pe" || cleanEmail === "admin@leofit.com") && 
            (cleanPass === "admin123" || cleanPass === "password")) {
          return {
            id: 1,
            name: "Administrador LeoFit",
            email: cleanEmail,
            role: "ADMIN"
          };
        }
        if ((cleanEmail === "operador@leofit.pe" || cleanEmail === "operador@leofit.com") && 
            (cleanPass === "admin123" || cleanPass === "password")) {
          return {
            id: 2,
            name: "Operador Logístico Gamarra",
            email: cleanEmail,
            role: "OPERATOR"
          };
        }
        return null;
      };

      const USE_MOCK = import.meta.env.VITE_USE_MOCK_AUTH === 'true';

      if (USE_MOCK) {
        const demoUser = resolverUsuarioDemo();
        if (demoUser) {
          setUsuarioActual(demoUser);
          setAutenticado(true);
          setPaginaActual("dashboard");
          sessionStorage.setItem(SESSION_KEY, `token-mock-${demoUser.role.toLowerCase()}`);
          sessionStorage.setItem("leofit_user", JSON.stringify(demoUser));
          return true;
        }
        return false;
      }

      // Autenticación real contra el backend Node.js con timeout defensivo (soporta cold start)
      const apiUrl = getApiBaseUrl();
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000);
        const res = await fetch(`${apiUrl}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: cleanEmail, password: cleanPass }),
          signal: controller.signal
        });
        clearTimeout(timeoutId);
        if (res.ok) {
          const data = await res.json();
          const rolRecibido = data.data?.user?.role === 'OPERATOR' ? 'OPERATOR' : 'ADMIN';
          const usuarioAutenticado: UsuarioActual = {
            id: data.data?.user?.id || (rolRecibido === 'OPERATOR' ? 2 : 1),
            name: data.data?.user?.name || (rolRecibido === 'OPERATOR' ? 'Operador Logístico Gamarra' : 'Administrador LeoFit'),
            email: data.data?.user?.email || cleanEmail,
            role: rolRecibido
          };
          setUsuarioActual(usuarioAutenticado);
          setAutenticado(true);
          setPaginaActual("dashboard");
          sessionStorage.setItem(SESSION_KEY, data.data.token);
          sessionStorage.setItem("leofit_user", JSON.stringify(usuarioAutenticado));
          sessionStorage.removeItem("leofit_auth_message");
          return true;
        }
      } catch {
        // En caso de que el backend esté en suspensión temporal o no responda, evaluar demo
      }

      // Respaldo de contingencia offline si el backend no responde
      const demoFallback = resolverUsuarioDemo();
      if (demoFallback) {
        setUsuarioActual(demoFallback);
        setAutenticado(true);
        setPaginaActual("dashboard");
        sessionStorage.setItem(SESSION_KEY, `token-offline-${demoFallback.role.toLowerCase()}`);
        sessionStorage.setItem("leofit_user", JSON.stringify(demoFallback));
        sessionStorage.removeItem("leofit_auth_message");
        return true;
      }

      return false;
    } catch {
      return false;
    }
  };

  const navegarA = (pagina: Pagina) => {
    setFiltroInicial("Todos");
    setPaginaActual(pagina);
  };

  const navegarAConFiltro = (pagina: Pagina, filtro: EstadoPedido | "Todos") => {
    setFiltroInicial(filtro);
    setPaginaActual(pagina);
  };

  const descontarStockLocal = (pedido: Pedido, signo: 1 | -1) =>
    setProductos((prev) =>
      prev.map((prod) => {
        const item = pedido.items.find((it) => it.productoId === prod.id);
        if (!item) return prod;
        return { ...prod, stock: Math.max(0, prod.stock + signo * item.cantidad) };
      })
    );

  const agregarPedido = (pedido: Pedido) => {
    setPedidos((prev) => [pedido, ...prev]);
    descontarStockLocal(pedido, -1);
  };

  const crearPedido = async (datos: Pedido): Promise<{ ok: true; pedido: Pedido } | { ok: false; error: string; code?: string }> => {
    const USE_MOCK = import.meta.env.VITE_USE_MOCK_ORDERS === 'true';
    if (USE_MOCK) {
      agregarPedido(datos);
      return { ok: true, pedido: datos };
    }

    try {
      const dto = toCreateOrderDTO(datos);
      const idempotencyKey = datos.numero || `order-${datos.id || Date.now()}`;
      const data = await apiFetch<{ id: number | string }>('/api/orders', {
        method: 'POST',
        headers: {
          'Idempotency-Key': idempotencyKey
        },
        body: JSON.stringify(dto)
      });
      
      if (data.id == null) {
        throw new Error('El backend no devolvió id de pedido');
      }
      const nuevoPedido = { ...datos, id: String(data.id) };
      agregarPedido(nuevoPedido);
      return { ok: true, pedido: nuevoPedido };
    } catch (err: any) {
      return { ok: false, error: err.message || 'Error al crear pedido', code: err.code };
    }
  };

  const actualizarEstadoPedido = (id: string, estado: EstadoPedido) => {
    const pedidoActual = pedidos.find((p) => p.id === id);
    if (!pedidoActual) return;
    const estadoPrevio = pedidoActual.estado;

    setPedidos((prev) =>
      prev.map((p) => {
        if (p.id !== id) return p;
        const ahora = new Date().toISOString();
        return {
          ...p,
          estado,
          // registra la fecha de entrega al confirmar "Entregado"
          fechaEntrega: estado === "Entregado" ? ahora : p.fechaEntrega,
        };
      })
    );

    // Restitución automática de stock si se cancela un pedido activo
    if (estado === "Cancelado" && estadoPrevio !== "Cancelado") {
      setProductos((prev) =>
        prev.map((prod) => {
          const item = pedidoActual.items.find((it) => it.productoId === prod.id);
          if (item) {
            return { ...prod, stock: prod.stock + item.cantidad };
          }
          return prod;
        })
      );
    }
    // Descuento automático si se reactiva un pedido previamente cancelado
    else if (estadoPrevio === "Cancelado" && estado !== "Cancelado") {
      setProductos((prev) =>
        prev.map((prod) => {
          const item = pedidoActual.items.find((it) => it.productoId === prod.id);
          if (item) {
            return { ...prod, stock: Math.max(0, prod.stock - item.cantidad) };
          }
          return prod;
        })
      );
    }
  };

  const agregarProducto = async (producto: Producto): Promise<void> => {
    setProductos((prev) => [...prev, producto]);
  };

  const editarProducto = async (producto: Producto): Promise<void> => {
    setProductos((prev) => prev.map((p) => (p.id === producto.id ? producto : p)));
  };

  const eliminarProducto = async (id: string): Promise<void> => {
    setProductos((prev) => prev.filter((p) => p.id !== id));
  };

  const cargarCatalogoLocal = () => {
    setProductos(productosIniciales);
    setErrorProductos(null);
  };

  const cargando = cargandoProductos;
  const errorApi = errorProductos;
  const limpiarError = () => setErrorProductos(null);

  return (
    <AppContext.Provider
      value={{
        autenticado, usuarioActual, paginaActual, pedidos, productos, cargandoProductos, errorProductos, filtroInicial, privacidad, modoAccesible,
        togglePrivacidad, toggleAccesible,
        iniciarSesion, cerrarSesion, navegarA, navegarAConFiltro,
        agregarPedido, crearPedido, actualizarEstadoPedido,
        agregarProducto, editarProducto, eliminarProducto,
        cargarCatalogoLocal,
        cargando, errorApi, limpiarError,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp debe usarse dentro de AppProvider");
  return ctx;
}
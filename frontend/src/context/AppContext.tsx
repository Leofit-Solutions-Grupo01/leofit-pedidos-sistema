/**
 * @file AppContext.tsx
 * @description Proveedor de estado global reactivo (pedidos, productos, autenticación, accesibilidad)
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { createContext, useContext, useState, useEffect, useCallback, useRef, ReactNode } from "react";
import { Pedido, Producto, EstadoPedido, pedidosIniciales, productosIniciales } from "../data/mockData";
import { api, ApiError, ProductoRef, getToken, setToken, clearToken } from "../services/api";

type Pagina = "login" | "dashboard" | "pedidos" | "nuevo-pedido" | "productos" | "rastreo" | "analytics";

interface AppContextType {
  autenticado: boolean;
  paginaActual: Pagina;
  pedidos: Pedido[];
  productos: Producto[];
  filtroInicial: EstadoPedido | "Todos";
  privacidad: boolean;
  modoAccesible: boolean;
  togglePrivacidad: () => void;
  toggleAccesible: () => void;
  iniciarSesion: (email: string, password: string) => Promise<boolean>;
  cerrarSesion: () => void;
  navegarA: (pagina: Pagina) => void;
  navegarAConFiltro: (pagina: Pagina, filtro: EstadoPedido | "Todos") => void;
  /** Registra el pedido (en la API cuando hay backend) y devuelve el pedido definitivo con su número real. */
  agregarPedido: (pedido: Pedido) => Promise<Pedido>;
  actualizarEstadoPedido: (id: string, estado: EstadoPedido) => void;
  agregarProducto: (producto: Producto) => Promise<void>;
  editarProducto: (producto: Producto) => Promise<void>;
  eliminarProducto: (id: string) => Promise<void>;
  /** true mientras se descargan pedidos y productos del servidor */
  cargando: boolean;
  /** Último error de comunicación con la API (null si no hay) */
  errorApi: string | null;
  limpiarError: () => void;
}

const AppContext = createContext<AppContextType | null>(null);

/** Modo demostración sin backend (datos locales). En producción debe ser false. */
const USE_MOCK = import.meta.env.VITE_USE_MOCK_AUTH === "true";
const ACCESIBLE_KEY = "leofit_modo_accesible";
const INACTIVIDAD_MS = 30 * 60 * 1000; // 30 minutos

export function AppProvider({ children }: { children: ReactNode }) {
  const [autenticado, setAutenticado] = useState(false);
  const [paginaActual, setPaginaActual] = useState<Pagina>("login");
  const [pedidos, setPedidos] = useState<Pedido[]>(USE_MOCK ? pedidosIniciales : []);
  const [productos, setProductos] = useState<Producto[]>(USE_MOCK ? productosIniciales : []);
  const [cargando, setCargando] = useState(false);
  const [errorApi, setErrorApi] = useState<string | null>(null);
  // variante (id de pantalla) -> producto/categoría del servidor
  const refs = useRef<Map<string, ProductoRef>>(new Map());
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

  const limpiarError = () => setErrorApi(null);

  const cerrarSesion = useCallback(() => {
    setAutenticado(false);
    setPaginaActual("login");
    clearToken();
    if (!USE_MOCK) {
      setPedidos([]);
      setProductos([]);
    }
  }, []);

  /** Muestra el error al usuario; si el token venció/es inválido cierra la sesión. */
  const manejarError = useCallback(
    (e: unknown, contexto: string) => {
      if (e instanceof ApiError && e.status === 401) {
        cerrarSesion();
        return;
      }
      setErrorApi(`${contexto}: ${e instanceof Error ? e.message : "error desconocido"}`);
    },
    [cerrarSesion]
  );

  const recargarProductos = useCallback(async () => {
    const { productos: lista, refs: nuevas } = await api.listarProductos();
    refs.current = nuevas;
    setProductos(lista);
  }, []);

  /** Descarga productos y pedidos desde la API (PostgreSQL). */
  const cargarDatos = useCallback(async () => {
    setCargando(true);
    try {
      const [prods, ords] = await Promise.all([api.listarProductos(), api.listarPedidos()]);
      refs.current = prods.refs;
      setProductos(prods.productos);
      setPedidos(ords);
    } catch (e) {
      manejarError(e, "No se pudieron cargar los datos");
    } finally {
      setCargando(false);
    }
  }, [manejarError]);

  // Restaurar sesión al montar. Con backend se valida el token guardado contra /api/auth/profile;
  // sessionStorage se borra al cerrar la pestaña (equilibrio entre conveniencia y seguridad).
  useEffect(() => {
    const token = getToken();
    if (!token) return;
    if (USE_MOCK) {
      setAutenticado(true);
      setPaginaActual("dashboard");
      return;
    }
    let activo = true;
    api
      .perfil()
      .then(() => {
        if (!activo) return;
        setAutenticado(true);
        setPaginaActual("dashboard");
        void cargarDatos();
      })
      .catch(() => clearToken());
    return () => {
      activo = false;
    };
  }, [cargarDatos]);

  // Token rechazado por el servidor (vencido o revocado) -> volver al login
  useEffect(() => {
    const alExpirar = () => cerrarSesion();
    window.addEventListener("leofit:unauthorized", alExpirar);
    return () => window.removeEventListener("leofit:unauthorized", alExpirar);
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
    if (USE_MOCK) {
      if (email.trim().toLowerCase() === "admin@leofit.com" && password === "admin123") {
        setAutenticado(true);
        setPaginaActual("dashboard");
        setToken("dummy-token");
        return true;
      }
      return false;
    }
    try {
      const token = await api.login(email.trim(), password);
      setToken(token);
      setAutenticado(true);
      setPaginaActual("dashboard");
      void cargarDatos();
      return true;
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

  const agregarPedido = async (pedido: Pedido): Promise<Pedido> => {
    if (USE_MOCK) {
      setPedidos((prev) => [pedido, ...prev]);
      descontarStockLocal(pedido, -1);
      return pedido;
    }
    try {
      const creado = await api.crearPedido(pedido); // el servidor descuenta stock (trigger en PostgreSQL)
      setPedidos((prev) => [creado, ...prev]);
      await recargarProductos().catch(() => undefined);
      return creado;
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) cerrarSesion();
      throw e; // el formulario muestra el motivo (stock insuficiente, datos inválidos, etc.)
    }
  };

  const actualizarEstadoPedido = (id: string, estado: EstadoPedido) => {
    const pedidoActual = pedidos.find((p) => p.id === id);
    if (!pedidoActual) return;
    const estadoPrevio = pedidoActual.estado;
    if (estadoPrevio === estado) return;

    if (USE_MOCK) {
      setPedidos((prev) =>
        prev.map((p) =>
          p.id !== id
            ? p
            : { ...p, estado, fechaEntrega: estado === "Entregado" ? new Date().toISOString() : p.fechaEntrega }
        )
      );
      if (estado === "Cancelado" && estadoPrevio !== "Cancelado") descontarStockLocal(pedidoActual, 1);
      else if (estadoPrevio === "Cancelado" && estado !== "Cancelado") descontarStockLocal(pedidoActual, -1);
      return;
    }

    // Con backend: un pedido cancelado ya devolvió su stock y no puede reactivarse.
    if (estadoPrevio === "Cancelado") {
      setErrorApi("Un pedido cancelado no puede reactivarse. Registre un pedido nuevo.");
      return;
    }

    // Actualización optimista con reversión si el servidor rechaza el cambio
    setPedidos((prev) => prev.map((p) => (p.id === id ? { ...p, estado } : p)));
    api
      .cambiarEstado(id, estado)
      .then(async (actualizado) => {
        setPedidos((prev) => prev.map((p) => (p.id === id ? { ...actualizado, fechaEntrega: actualizado.fechaEntrega ?? (estado === "Entregado" ? new Date().toISOString() : p.fechaEntrega) } : p)));
        if (estado === "Cancelado") await recargarProductos().catch(() => undefined); // stock devuelto
      })
      .catch((e) => {
        setPedidos((prev) => prev.map((p) => (p.id === id ? { ...p, estado: estadoPrevio } : p)));
        manejarError(e, "No se pudo cambiar el estado del pedido");
      });
  };

  const agregarProducto = async (producto: Producto): Promise<void> => {
    if (USE_MOCK) {
      setProductos((prev) => [...prev, producto]);
      return;
    }
    try {
      const mismaCategoria = Array.from(refs.current.entries()).find(([id]) => productos.find((p) => p.id === id)?.categoria === producto.categoria);
      await api.crearProducto(producto, mismaCategoria?.[1].categoryId);
      await recargarProductos();
    } catch (e) {
      manejarError(e, "No se pudo crear el producto");
    }
  };

  const editarProducto = async (producto: Producto): Promise<void> => {
    if (USE_MOCK) {
      setProductos((prev) => prev.map((p) => (p.id === producto.id ? producto : p)));
      return;
    }
    const ref = refs.current.get(producto.id);
    const original = productos.find((p) => p.id === producto.id);
    if (!ref || !original) {
      setErrorApi("No se pudo editar: el producto no existe en el servidor.");
      return;
    }
    try {
      const categoryId = original.categoria === producto.categoria ? ref.categoryId : api.categoriaId(producto.categoria);
      await api.editarProducto(producto, ref, original.stock, categoryId);
      await recargarProductos();
    } catch (e) {
      manejarError(e, "No se pudo editar el producto");
    }
  };

  const eliminarProducto = async (id: string): Promise<void> => {
    if (USE_MOCK) {
      setProductos((prev) => prev.filter((p) => p.id !== id));
      return;
    }
    const ref = refs.current.get(id);
    if (!ref) {
      setErrorApi("No se pudo eliminar: el producto no existe en el servidor.");
      return;
    }
    try {
      await api.eliminarProducto(ref);
      await recargarProductos();
    } catch (e) {
      manejarError(e, "No se pudo eliminar el producto");
    }
  };

  return (
    <AppContext.Provider
      value={{
        autenticado, paginaActual, pedidos, productos, filtroInicial, privacidad, modoAccesible,
        togglePrivacidad, toggleAccesible,
        iniciarSesion, cerrarSesion, navegarA, navegarAConFiltro,
        agregarPedido, actualizarEstadoPedido,
        agregarProducto, editarProducto, eliminarProducto,
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
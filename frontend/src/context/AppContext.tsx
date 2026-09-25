/**
 * @file AppContext.tsx
 * @description Proveedor de estado global reactivo (pedidos, productos, autenticación, accesibilidad)
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { Pedido, Producto, EstadoPedido, pedidosIniciales, productosIniciales } from "../data/mockData";

type Pagina = "login" | "dashboard" | "pedidos" | "nuevo-pedido" | "productos" | "rastreo";

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
  iniciarSesion: (email: string, password: string) => boolean;
  cerrarSesion: () => void;
  navegarA: (pagina: Pagina) => void;
  navegarAConFiltro: (pagina: Pagina, filtro: EstadoPedido | "Todos") => void;
  agregarPedido: (pedido: Pedido) => void;
  actualizarEstadoPedido: (id: string, estado: EstadoPedido) => void;
  agregarProducto: (producto: Producto) => void;
  editarProducto: (producto: Producto) => void;
  eliminarProducto: (id: string) => void;
}

const AppContext = createContext<AppContextType | null>(null);

const SESSION_KEY = "leofit_session";
const ACCESIBLE_KEY = "leofit_modo_accesible";
const INACTIVIDAD_MS = 30 * 60 * 1000; // 30 minutos

export function AppProvider({ children }: { children: ReactNode }) {
  const [autenticado, setAutenticado] = useState(false);
  const [paginaActual, setPaginaActual] = useState<Pagina>("login");
  const [pedidos, setPedidos] = useState<Pedido[]>(pedidosIniciales);
  const [productos, setProductos] = useState<Producto[]>(productosIniciales);
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

  // Restaurar sesión al montar (sessionStorage: persiste durante la sesión del navegador,
  // se borra al cerrar la pestaña — equilibrio entre conveniencia y seguridad)
  useEffect(() => {
    try {
      const guardado = sessionStorage.getItem(SESSION_KEY);
      if (guardado === "victor") {
        setAutenticado(true);
        setPaginaActual("dashboard");
      }
    } catch {
      // Ignora restricciones de iframe/sandbox
    }
  }, []);

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
  }, [autenticado]);

  const iniciarSesion = (email: string, password: string): boolean => {
    if (email === "victor@leofit.com" && password === "leofit2026") {
      setAutenticado(true);
      setPaginaActual("dashboard");
      sessionStorage.setItem(SESSION_KEY, "victor");
      return true;
    }
    return false;
  };

  const cerrarSesion = () => {
    setAutenticado(false);
    setPaginaActual("login");
    sessionStorage.removeItem(SESSION_KEY);
  };

  const navegarA = (pagina: Pagina) => {
    setFiltroInicial("Todos");
    setPaginaActual(pagina);
  };

  const navegarAConFiltro = (pagina: Pagina, filtro: EstadoPedido | "Todos") => {
    setFiltroInicial(filtro);
    setPaginaActual(pagina);
  };

  const agregarPedido = (pedido: Pedido) => {
    setPedidos((prev) => [pedido, ...prev]);
    // Descontar inventario automáticamente
    setProductos((prev) =>
      prev.map((prod) => {
        const itemComprado = pedido.items.find((it) => it.productoId === prod.id);
        if (itemComprado) {
          return { ...prod, stock: Math.max(0, prod.stock - itemComprado.cantidad) };
        }
        return prod;
      })
    );
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

  const agregarProducto = (producto: Producto) => setProductos((prev) => [...prev, producto]);
  const editarProducto = (producto: Producto) => setProductos((prev) => prev.map((p) => (p.id === producto.id ? producto : p)));
  const eliminarProducto = (id: string) => setProductos((prev) => prev.filter((p) => p.id !== id));

  return (
    <AppContext.Provider
      value={{
        autenticado, paginaActual, pedidos, productos, filtroInicial, privacidad, modoAccesible,
        togglePrivacidad, toggleAccesible,
        iniciarSesion, cerrarSesion, navegarA, navegarAConFiltro,
        agregarPedido, actualizarEstadoPedido,
        agregarProducto, editarProducto, eliminarProducto,
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

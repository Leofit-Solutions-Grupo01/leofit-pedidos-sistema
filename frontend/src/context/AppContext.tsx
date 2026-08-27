import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { Pedido, Producto, EstadoPedido, pedidosIniciales, productosIniciales } from "../data/mockData";

type Pagina = "login" | "dashboard" | "pedidos" | "nuevo-pedido" | "productos";

interface AppContextType {
  autenticado: boolean;
  paginaActual: Pagina;
  pedidos: Pedido[];
  productos: Producto[];
  filtroInicial: EstadoPedido | "Todos";
  privacidad: boolean;
  togglePrivacidad: () => void;
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
const INACTIVIDAD_MS = 30 * 60 * 1000; // 30 minutos

export function AppProvider({ children }: { children: ReactNode }) {
  const [autenticado, setAutenticado] = useState(false);
  const [paginaActual, setPaginaActual] = useState<Pagina>("login");
  const [pedidos, setPedidos] = useState<Pedido[]>(pedidosIniciales);
  const [productos, setProductos] = useState<Producto[]>(productosIniciales);
  const [filtroInicial, setFiltroInicial] = useState<EstadoPedido | "Todos">("Todos");
  const [privacidad, setPrivacidad] = useState(false);

  const togglePrivacidad = () => setPrivacidad((v) => !v);

  // Restaurar sesión al montar (sessionStorage: persiste durante la sesión del navegador,
  // se borra al cerrar la pestaña — equilibrio entre conveniencia y seguridad)
  useEffect(() => {
    const guardado = sessionStorage.getItem(SESSION_KEY);
    if (guardado === "victor") {
      setAutenticado(true);
      setPaginaActual("dashboard");
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

  const agregarPedido = (pedido: Pedido) => setPedidos((prev) => [pedido, ...prev]);

  const actualizarEstadoPedido = (id: string, estado: EstadoPedido) => {
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
  };

  const agregarProducto = (producto: Producto) => setProductos((prev) => [...prev, producto]);
  const editarProducto = (producto: Producto) => setProductos((prev) => prev.map((p) => (p.id === producto.id ? producto : p)));
  const eliminarProducto = (id: string) => setProductos((prev) => prev.filter((p) => p.id !== id));

  return (
    <AppContext.Provider
      value={{
        autenticado, paginaActual, pedidos, productos, filtroInicial, privacidad, togglePrivacidad,
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

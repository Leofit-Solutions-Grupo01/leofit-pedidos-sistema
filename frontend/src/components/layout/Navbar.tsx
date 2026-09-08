import { useState, useRef, useEffect } from "react";
import { useApp } from "../../context/AppContext";

type NavPagina = "dashboard" | "pedidos" | "nuevo-pedido" | "productos";

const navItems: { label: string; icon: string; pagina: NavPagina; shortcut?: string }[] = [
  { label: "Inicio", icon: "dashboard", pagina: "dashboard" },
  { label: "Pedidos", icon: "receipt_long", pagina: "pedidos" },
  { label: "Nuevo Pedido", icon: "add_circle", pagina: "nuevo-pedido" },
  { label: "Inventario", icon: "inventory_2", pagina: "productos" },
];

export default function Navbar() {
  const {
    paginaActual,
    navegarA,
    cerrarSesion,
    privacidad,
    togglePrivacidad,
    modoAccesible,
    toggleAccesible,
  } = useApp();

  const [menuUsuarioAbierto, setMenuUsuarioAbierto] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Cerrar menú al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuUsuarioAbierto(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <>
      {/* Header Superior Principal */}
      <header className="fixed top-0 left-0 right-0 z-40 bg-[#0F223D]/95 backdrop-blur-md h-16 border-b border-slate-700/60 shadow-xl transition-all">
        <div className="max-w-6xl mx-auto h-full px-3 sm:px-6 flex items-center justify-between gap-2">
          
          {/* 1. SECCIÓN IZQUIERDA: Marca y Contexto */}
          <div
            onClick={() => navegarA("dashboard")}
            className="flex items-center gap-2.5 cursor-pointer group select-none py-1.5"
            role="button"
            tabIndex={0}
            onKeyDown={(e) => e.key === "Enter" && navegarA("dashboard")}
            aria-label="Ir al Inicio de LeoFit"
          >
            {/* Isotipo Logo */}
            <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-[#E63946] to-[#C62828] flex items-center justify-center shadow-md shadow-red-500/20 group-hover:scale-105 transition-transform border border-white/20">
              <span className="font-extrabold font-display text-white text-base sm:text-lg tracking-wider">LF</span>
            </div>
            
            {/* Logotipo y Subtítulo */}
            <div className="flex flex-col">
              <div className="flex items-baseline leading-none">
                <span className="font-extrabold font-display text-xl sm:text-2xl text-[#E63946] tracking-tight">LEO</span>
                <span className="font-extrabold font-display text-xl sm:text-2xl text-white tracking-tight">FIT</span>
              </div>
              <span className="text-[10px] sm:text-xs font-semibold text-slate-400 tracking-wider uppercase mt-0.5 hidden xs:inline">
                Gestión de Pedidos
              </span>
            </div>
          </div>

          {/* 2. SECCIÓN CENTRAL: Navegación de Escritorio (Tablet/Desktop) */}
          <nav className="hidden md:flex items-center gap-1 bg-slate-800/60 p-1 rounded-2xl border border-slate-700/70 shadow-inner">
            {navItems.map((item) => {
              const activo = paginaActual === item.pagina;
              return (
                <button
                  key={item.pagina}
                  onClick={() => navegarA(item.pagina)}
                  className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                    activo
                      ? "bg-[#E63946] text-white shadow-md shadow-red-500/30"
                      : "text-slate-300 hover:text-white hover:bg-white/10"
                  }`}
                  aria-label={item.label}
                >
                  <span className="material-icons" style={{ fontSize: "17px" }}>{item.icon}</span>
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* 3. SECCIÓN DERECHA: Controles de Preferencias y Usuario */}
          <div className="flex items-center gap-1.5 sm:gap-2">
            
            {/* Grupo de Herramientas Rápidas */}
            <div className="flex items-center bg-slate-800/70 p-1 rounded-2xl border border-slate-700/60 gap-1">
              
              {/* Botón Accesibilidad: Tamaño y Contraste */}
              <button
                onClick={toggleAccesible}
                className={`px-2.5 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all ${
                  modoAccesible
                    ? "bg-[#F59E0B] text-slate-950 shadow-md ring-1 ring-amber-300"
                    : "text-slate-300 hover:text-white hover:bg-white/10"
                }`}
                aria-label={modoAccesible ? "Desactivar modo vista grande" : "Activar modo vista grande"}
                title={modoAccesible ? "Modo Vista Grande Activado" : "Activar modo letra grande"}
              >
                <span className="material-icons" style={{ fontSize: "17px" }}>format_size</span>
                <span className="hidden sm:inline">{modoAccesible ? "A++ Grande" : "A+ Vista"}</span>
              </button>

              {/* Botón Modo Privacidad Montos */}
              <button
                onClick={togglePrivacidad}
                className={`p-1.5 sm:px-2.5 sm:py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all ${
                  privacidad
                    ? "bg-[#E63946] text-white shadow-md"
                    : "text-slate-300 hover:text-white hover:bg-white/10"
                }`}
                aria-label={privacidad ? "Mostrar cifras en Soles" : "Ocultar cifras en Soles (Modo Privacidad)"}
                title={privacidad ? "Montos ocultos (Privado)" : "Ocultar montos de ventas"}
              >
                <span className="material-icons" style={{ fontSize: "17px" }}>
                  {privacidad ? "visibility_off" : "visibility"}
                </span>
                <span className="hidden md:inline">{privacidad ? "Oculto" : "Visible"}</span>
              </button>
            </div>

            {/* Cápsula de Usuario / Menú Perfil */}
            <div className="relative" ref={menuRef}>
              <button
                onClick={() => setMenuUsuarioAbierto((prev) => !prev)}
                className="flex items-center gap-2 bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/80 rounded-2xl pl-1.5 pr-2.5 py-1 transition-all shadow-sm active:scale-95"
                aria-expanded={menuUsuarioAbierto}
                aria-label="Menú de usuario"
              >
                <div className="w-7 h-7 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-xs shadow-inner">
                  V
                </div>
                <span className="text-xs font-semibold text-slate-200 hidden sm:inline">Víctor</span>
                <span className="material-icons text-slate-400" style={{ fontSize: "16px" }}>
                  {menuUsuarioAbierto ? "expand_less" : "expand_more"}
                </span>
              </button>

              {/* Desplegable de Usuario */}
              {menuUsuarioAbierto && (
                <div className="absolute right-0 mt-2 w-48 bg-[#0F223D] border border-slate-700 rounded-2xl shadow-2xl p-2 z-50 text-slate-200 animate-in fade-in slide-in-from-top-2">
                  <div className="px-3 py-2 border-b border-slate-700/60 mb-1">
                    <p className="text-xs font-semibold text-white">Víctor (Administrador)</p>
                    <p className="text-[11px] font-normal text-slate-400 truncate">victor@leofit.com</p>
                  </div>

                  <button
                    onClick={() => {
                      setMenuUsuarioAbierto(false);
                      toggleAccesible();
                    }}
                    className="w-full flex items-center gap-2 px-3 py-2 text-xs font-medium text-slate-300 hover:text-white hover:bg-white/10 rounded-xl transition-colors text-left"
                  >
                    <span className="material-icons text-amber-400" style={{ fontSize: "16px" }}>format_size</span>
                    <span>{modoAccesible ? "Reducir tamaño fuente" : "Aumentar tamaño fuente"}</span>
                  </button>

                  <button
                    onClick={() => {
                      setMenuUsuarioAbierto(false);
                      togglePrivacidad();
                    }}
                    className="w-full flex items-center gap-2 px-3 py-2 text-xs font-medium text-slate-300 hover:text-white hover:bg-white/10 rounded-xl transition-colors text-left"
                  >
                    <span className="material-icons text-blue-400" style={{ fontSize: "16px" }}>
                      {privacidad ? "visibility" : "visibility_off"}
                    </span>
                    <span>{privacidad ? "Mostrar montos" : "Ocultar montos"}</span>
                  </button>

                  <div className="my-1 border-t border-slate-700/60" />

                  <button
                    onClick={() => {
                      setMenuUsuarioAbierto(false);
                      cerrarSesion();
                    }}
                    className="w-full flex items-center gap-2 px-3 py-2 text-xs font-semibold text-red-400 hover:bg-red-500/20 hover:text-red-300 rounded-xl transition-colors text-left"
                  >
                    <span className="material-icons" style={{ fontSize: "16px" }}>logout</span>
                    <span>Cerrar Sesión</span>
                  </button>
                </div>
              )}
            </div>

          </div>
        </div>
      </header>

      {/* Barra de Navegación Inferior (Móvil) */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#0F223D]/95 backdrop-blur-md border-t border-slate-700/70 flex shadow-2xl safe-bottom">
        {navItems.map((item) => {
          const activo = paginaActual === item.pagina;
          return (
            <button
              key={item.pagina}
              onClick={() => navegarA(item.pagina)}
              className={`flex-1 flex flex-col items-center justify-center py-2.5 gap-1 transition-all ${
                activo
                  ? "text-[#E63946] bg-white/10 border-t-2 border-[#E63946]"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
              aria-label={item.label}
            >
              <span
                className="material-icons transition-transform"
                style={{
                  fontSize: "22px",
                  transform: activo ? "scale(1.1)" : "scale(1)",
                  color: activo ? "#E63946" : "#94A3B8",
                }}
              >
                {item.icon}
              </span>
              <span className={`text-[11px] font-semibold tracking-wide ${activo ? "text-[#E63946]" : "text-slate-300"}`}>
                {item.label === "Nuevo Pedido" ? "Nuevo" : item.label}
              </span>
            </button>
          );
        })}
      </nav>
    </>
  );
}

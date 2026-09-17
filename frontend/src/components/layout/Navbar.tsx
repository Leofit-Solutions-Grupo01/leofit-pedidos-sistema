/**
 * @file Navbar.tsx
 * @description Barra de navegación superior y barra móvil inferior con créditos de desarrollo
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { useState, useRef, useEffect } from "react";
import { useApp } from "../../context/AppContext";

type NavPagina = "dashboard" | "pedidos" | "nuevo-pedido" | "productos" | "rastreo";

const navItems: { label: string; mobileLabel: string; icon: string; pagina: NavPagina }[] = [
  { label: "Inicio", mobileLabel: "Inicio", icon: "dashboard", pagina: "dashboard" },
  { label: "Pedidos", mobileLabel: "Pedidos", icon: "receipt_long", pagina: "pedidos" },
  { label: "Nuevo Pedido", mobileLabel: "Nuevo", icon: "add_circle", pagina: "nuevo-pedido" },
  { label: "Inventario", mobileLabel: "Stock", icon: "inventory_2", pagina: "productos" },
  { label: "Rastreo", mobileLabel: "Rastreo", icon: "track_changes", pagina: "rastreo" },
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
        <div className="max-w-5xl mx-auto h-full px-3 sm:px-6 flex items-center justify-between gap-2">
          
          {/* 1. SECCIÓN IZQUIERDA: Marca y Contexto */}
          <div
            onClick={() => navegarA("dashboard")}
            className="flex items-center gap-2 cursor-pointer group select-none py-1 shrink-0"
            role="button"
            tabIndex={0}
            onKeyDown={(e) => e.key === "Enter" && navegarA("dashboard")}
            aria-label="Ir al Inicio de LeoFit"
          >
            {/* Isotipo Logo */}
            <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-gradient-to-br from-[#E63946] to-[#C62828] flex items-center justify-center shadow-md shadow-red-500/20 group-hover:scale-105 transition-transform border border-white/20 shrink-0">
              <span className="font-extrabold font-display text-white text-xs sm:text-sm tracking-wider">LF</span>
            </div>
            
            {/* Logotipo y Subtítulo */}
            <div className="flex flex-col">
              <div className="flex items-baseline leading-none">
                <span className="font-extrabold font-display text-lg sm:text-xl text-[#E63946] tracking-tight">LEO</span>
                <span className="font-extrabold font-display text-lg sm:text-xl text-white tracking-tight">FIT</span>
              </div>
              <span className="text-[10px] font-semibold text-slate-400 tracking-wider uppercase mt-0.5 hidden md:inline">
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
                  className={`flex items-center gap-1.5 px-2.5 lg:px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                    activo
                      ? "bg-[#E63946] text-white shadow-md shadow-red-500/30"
                      : "text-slate-300 hover:text-white hover:bg-white/10"
                  }`}
                  aria-label={item.label}
                >
                  <span className="material-icons" style={{ fontSize: "16px" }}>{item.icon}</span>
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* 3. SECCIÓN DERECHA: Controles de Accesibilidad y Usuario */}
          <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
            
            {/* Botón Accesibilidad: Tamaño y Contraste */}
            <button
              onClick={toggleAccesible}
              className={`px-2.5 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1 transition-all border ${
                modoAccesible
                  ? "bg-[#F59E0B] text-slate-950 border-amber-300 shadow-md ring-1 ring-amber-300"
                  : "bg-slate-800/70 border-slate-700/60 text-slate-300 hover:text-white hover:bg-slate-700/80"
              }`}
              aria-label={modoAccesible ? "Desactivar modo vista grande" : "Activar modo vista grande"}
              title={modoAccesible ? "Modo Vista Grande Activado" : "Activar modo letra grande"}
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>format_size</span>
              <span>{modoAccesible ? "A++ Grande" : "A+ Vista"}</span>
            </button>

            {/* Cápsula de Usuario / Menú Perfil */}
            <div className="relative" ref={menuRef}>
              <button
                onClick={() => setMenuUsuarioAbierto((prev) => !prev)}
                className="flex items-center gap-1.5 bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/80 rounded-xl sm:rounded-2xl p-1 sm:pl-1.5 sm:pr-2.5 sm:py-1 transition-all shadow-sm active:scale-95"
                aria-expanded={menuUsuarioAbierto}
                aria-label="Menú de usuario"
              >
                <div className="w-6 h-6 sm:w-7 sm:h-7 rounded-lg sm:rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-xs shadow-inner shrink-0">
                  L
                </div>
                <span className="text-xs font-semibold text-slate-200 hidden sm:inline">Lady Loayza</span>
                <span className="material-icons text-slate-400" style={{ fontSize: "15px" }}>
                  {menuUsuarioAbierto ? "expand_less" : "expand_more"}
                </span>
              </button>

              {/* Desplegable de Usuario */}
              {menuUsuarioAbierto && (
                <div className="absolute right-0 mt-2 w-56 bg-[#0F223D] border border-slate-700 rounded-2xl shadow-2xl p-2.5 z-50 text-slate-200 animate-in fade-in slide-in-from-top-2">
                  <div className="px-3 py-2 border-b border-slate-700/60 mb-1 bg-slate-900/50 rounded-xl">
                    <p className="text-xs font-bold text-white">Lady Luz Loayza Rodriguez</p>
                    <p className="text-[10px] font-medium text-emerald-400">@LadyyLuz · Scrum Master</p>
                    <p className="text-[10px] font-normal text-slate-400 truncate">168585420+luzylay@users.noreply.github.com</p>
                  </div>

                  <div className="px-3 py-1 text-[11px] text-slate-400">
                    Operador: <strong className="text-slate-200">Víctor Raúl Cárdenas</strong>
                  </div>

                  <button
                    onClick={() => {
                      setMenuUsuarioAbierto(false);
                      toggleAccesible();
                    }}
                    className="w-full flex items-center gap-2 px-3 py-2 text-xs font-medium text-slate-300 hover:text-white hover:bg-white/10 rounded-xl transition-colors text-left mt-1"
                  >
                    <span className="material-icons text-amber-400" style={{ fontSize: "16px" }}>format_size</span>
                    <span>{modoAccesible ? "Reducir tamaño fuente" : "Aumentar tamaño fuente"}</span>
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

      {/* Barra de Navegación Inferior (Móvil Ultra-Optimizada) */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#0F223D]/95 backdrop-blur-md border-t border-slate-700/70 flex shadow-2xl safe-bottom">
        {navItems.map((item) => {
          const activo = paginaActual === item.pagina;
          return (
            <button
              key={item.pagina}
              onClick={() => navegarA(item.pagina)}
              className={`flex-1 min-w-0 flex flex-col items-center justify-center py-2 px-0.5 gap-0.5 transition-all ${
                activo
                  ? "text-[#E63946] bg-white/10 border-t-2 border-[#E63946]"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
              aria-label={item.label}
            >
              <span
                className="material-icons transition-transform"
                style={{
                  fontSize: "20px",
                  transform: activo ? "scale(1.1)" : "scale(1)",
                  color: activo ? "#E63946" : "#94A3B8",
                }}
              >
                {item.icon}
              </span>
              <span className={`text-[10px] font-semibold tracking-tight truncate max-w-full ${activo ? "text-[#E63946]" : "text-slate-300"}`}>
                {item.mobileLabel}
              </span>
            </button>
          );
        })}
      </nav>
    </>
  );
}

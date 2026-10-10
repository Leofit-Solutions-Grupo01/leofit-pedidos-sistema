/**
 * @file Login.tsx
 * @description Pantalla de autenticación y control de acceso para el operador administrativo
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { useState } from "react";
import { useApp } from "../context/AppContext";

export default function Login() {
  const { iniciarSesion } = useApp();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mostrarPass, setMostrarPass] = useState(false);
  const [error, setError] = useState("");
  const [cargando, setCargando] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!email || !password) {
      setError("Completa todos los campos para continuar.");
      return;
    }
    setCargando(true);
    setTimeout(async () => {
      const ok = await iniciarSesion(email, password);
      if (!ok) {
        setError("Credenciales incorrectas. Verifica tus datos.");
        setCargando(false);
      }
    }, 700);
  };

  return (
    <div className="min-h-screen bg-[#0F223D] flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="inline-flex items-baseline mb-2">
            <span className="font-extrabold font-display text-5xl text-[#E63946] tracking-tight">LEO</span>
            <span className="font-extrabold font-display text-5xl text-white tracking-tight">FIT</span>
          </div>
          <p className="text-amber-400 text-xs font-semibold tracking-widest uppercase">
            Gestión de Pedidos & Inventario
          </p>
        </div>

        <div className="bg-white rounded-3xl shadow-2xl p-7 border border-slate-200">
          <h1 className="text-xl font-bold text-slate-900 mb-6">Iniciar Sesión</h1>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                Correo Electrónico
              </label>
              <div className="relative">
                <span className="material-icons absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" style={{ fontSize: "20px" }}>
                  mail_outline
                </span>
                <input
                  id="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="correo@ejemplo.com"
                  className="w-full pl-12 pr-4 py-3.5 border-2 border-slate-300 rounded-2xl text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] bg-slate-50 focus:bg-white transition-all shadow-inner"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                Contraseña
              </label>
              <div className="relative">
                <span className="material-icons absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" style={{ fontSize: "20px" }}>
                  lock_outline
                </span>
                <input
                  id="password"
                  type={mostrarPass ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-12 pr-12 py-3.5 border-2 border-slate-300 rounded-2xl text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] bg-slate-50 focus:bg-white transition-all shadow-inner"
                />
                <button
                  type="button"
                  onClick={() => setMostrarPass(!mostrarPass)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 p-2 hover:bg-slate-200 rounded-xl transition-colors"
                  aria-label={mostrarPass ? "Ocultar contraseña" : "Mostrar contraseña"}
                  title="Mostrar/Ocultar contraseña"
                >
                  <span className="material-icons text-slate-500" style={{ fontSize: "20px" }}>
                    {mostrarPass ? "visibility_off" : "visibility"}
                  </span>
                </button>
              </div>
            </div>

            {error && (
              <div className="flex items-start gap-2.5 bg-red-100 border-2 border-red-300 rounded-2xl px-4 py-3">
                <span className="material-icons text-red-700 mt-0.5" style={{ fontSize: "18px" }}>error_outline</span>
                <p className="text-sm text-red-950 font-semibold leading-relaxed">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={cargando}
              className="w-full py-4 bg-[#E63946] hover:bg-[#C62828] active:scale-[0.98] text-white font-bold text-base rounded-2xl transition-all disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2 mt-3 shadow-xl shadow-red-500/30 ring-2 ring-white"
            >
              {cargando ? (
                <>
                  <span className="material-icons animate-spin" style={{ fontSize: "20px" }}>refresh</span>
                  Verificando...
                </>
              ) : (
                "Ingresar al Sistema"
              )}
            </button>
          </form>

          {/* Selector Rápido de Roles (Acceso Demo / Evaluación) */}
          <div className="mt-6 pt-5 border-t border-slate-200">
            <p className="text-[11px] font-bold text-slate-500 uppercase tracking-wider text-center mb-2.5">
              Acceso Rápido por Rol
            </p>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => {
                  setEmail("admin@leofit.pe");
                  setPassword("admin123");
                  setError("");
                }}
                className="py-2.5 px-3 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-xl text-left transition-all active:scale-95 group"
                title="Cargar credenciales de Administrador"
              >
                <span className="block text-[11px] font-extrabold text-blue-900 flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-blue-600"></span>
                  Admin
                </span>
                <span className="block text-[10px] text-blue-700 font-medium truncate">admin@leofit.pe</span>
              </button>

              <button
                type="button"
                onClick={() => {
                  setEmail("operador@leofit.pe");
                  setPassword("admin123");
                  setError("");
                }}
                className="py-2.5 px-3 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 rounded-xl text-left transition-all active:scale-95 group"
                title="Cargar credenciales de Operador"
              >
                <span className="block text-[11px] font-extrabold text-emerald-900 flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-emerald-600"></span>
                  Operador
                </span>
                <span className="block text-[10px] text-emerald-700 font-medium truncate">operador@leofit.pe</span>
              </button>
            </div>
          </div>
        </div>

        <p className="mt-5 text-center text-xs text-slate-300 font-normal">
          Sistema Oficial de Pedidos · LeoFit Sportswear
        </p>
      </div>
    </div>
  );
}

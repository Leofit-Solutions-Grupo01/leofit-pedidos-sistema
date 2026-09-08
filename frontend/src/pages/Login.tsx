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
    setTimeout(() => {
      const ok = iniciarSesion(email, password);
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
                  placeholder="victor@leofit.com"
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
        </div>

        <button
          type="button"
          onClick={() => {
            setEmail("victor@leofit.com");
            setPassword("leofit2026");
          }}
          className="mt-5 w-full flex items-center justify-center gap-2 py-3.5 bg-white/20 hover:bg-white/30 active:scale-[0.98] border-2 border-white/40 text-white rounded-2xl transition-all shadow-lg font-bold text-sm"
        >
          <span className="material-icons text-amber-400" style={{ fontSize: "20px" }}>bolt</span>
          <span>Autocompletar Datos de Prueba</span>
        </button>

        <p className="mt-5 text-center text-xs text-slate-300 font-normal">
          Sistema Oficial de Pedidos · LeoFit Sportswear
        </p>
      </div>
    </div>
  );
}

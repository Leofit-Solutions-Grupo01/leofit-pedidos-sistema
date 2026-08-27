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
    <div className="min-h-screen bg-[#1D3557] flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-sm">
        <div className="text-center mb-10">
          <div className="inline-flex items-baseline mb-3">
            <span className="font-black text-5xl text-[#E63946] tracking-tight">LEO</span>
            <span className="font-black text-5xl text-white tracking-tight">FIT</span>
          </div>
          <p className="text-white/50 text-sm font-medium tracking-widest uppercase">
            Gestión de Pedidos
          </p>
        </div>

        <div className="bg-white rounded-3xl shadow-2xl p-7">
          <h1 className="text-lg font-bold text-[#1D3557] mb-6">Iniciar Sesión</h1>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-xs font-bold text-[#1D3557]/60 uppercase tracking-wider mb-1.5">
                Correo electrónico
              </label>
              <div className="relative">
                <span className="material-icons absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-300" style={{ fontSize: "18px" }}>
                  mail_outline
                </span>
                <input
                  id="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="correo@leofit.com"
                  className="w-full pl-10 pr-4 py-3 border-2 border-gray-100 rounded-2xl text-sm text-[#1A1A1A] placeholder-gray-300 focus:outline-none focus:border-[#E63946] focus:ring-4 focus:ring-[#E63946]/10 transition-all"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-xs font-bold text-[#1D3557]/60 uppercase tracking-wider mb-1.5">
                Contraseña
              </label>
              <div className="relative">
                <span className="material-icons absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-300" style={{ fontSize: "18px" }}>
                  lock_outline
                </span>
                <input
                  id="password"
                  type={mostrarPass ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-12 py-3 border-2 border-gray-100 rounded-2xl text-sm text-[#1A1A1A] placeholder-gray-300 focus:outline-none focus:border-[#E63946] focus:ring-4 focus:ring-[#E63946]/10 transition-all"
                />
                <button
                  type="button"
                  onClick={() => setMostrarPass(!mostrarPass)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 p-0.5 hover:bg-gray-100 rounded-lg transition-colors"
                  aria-label={mostrarPass ? "Ocultar contraseña" : "Mostrar contraseña"}
                >
                  <span className="material-icons text-gray-300" style={{ fontSize: "18px" }}>
                    {mostrarPass ? "visibility_off" : "visibility"}
                  </span>
                </button>
              </div>
            </div>

            {error && (
              <div className="flex items-start gap-2.5 bg-red-50 border border-red-100 rounded-2xl px-4 py-3">
                <span className="material-icons text-[#E63946] mt-0.5" style={{ fontSize: "16px" }}>error_outline</span>
                <p className="text-xs text-red-600 font-medium leading-relaxed">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={cargando}
              className="w-full py-3.5 bg-[#E63946] hover:bg-[#C62828] active:scale-[0.98] text-white font-bold rounded-2xl transition-all disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2 mt-2 shadow-lg shadow-[#E63946]/30"
            >
              {cargando ? (
                <>
                  <span className="material-icons animate-spin" style={{ fontSize: "18px" }}>refresh</span>
                  Verificando...
                </>
              ) : (
                "Iniciar Sesión"
              )}
            </button>
          </form>

          <div className="mt-5 text-center">
            <button className="text-xs text-gray-400 hover:text-[#E63946] transition-colors font-medium">
              Olvidaste tu contraseña?
            </button>
          </div>
        </div>

        <button
          type="button"
          onClick={() => {
            setEmail("victor@leofit.com");
            setPassword("leofit2026");
          }}
          className="mt-4 w-full flex items-center justify-center gap-2.5 py-3 bg-white/10 hover:bg-white/15 active:scale-[0.98] border border-white/20 rounded-2xl transition-all"
        >
          <span className="material-icons text-white/50" style={{ fontSize: "16px" }}>science</span>
          <span className="text-sm font-semibold text-white/60">Usar cuenta de demostración</span>
        </button>

        <p className="mt-5 text-center text-xs text-white/20 font-medium">
          Acceso exclusivo para el equipo Leofit
        </p>
      </div>
    </div>
  );
}

import { useApp } from "../../context/AppContext";

type NavPagina = "dashboard" | "pedidos" | "nuevo-pedido" | "productos";

const navItems: { label: string; icon: string; pagina: NavPagina }[] = [
  { label: "Inicio", icon: "dashboard", pagina: "dashboard" },
  { label: "Pedidos", icon: "receipt_long", pagina: "pedidos" },
  { label: "Nuevo", icon: "add_circle", pagina: "nuevo-pedido" },
  { label: "Productos", icon: "inventory_2", pagina: "productos" },
];

export default function Navbar() {
  const { paginaActual, navegarA, cerrarSesion, privacidad, togglePrivacidad, modoAccesible, toggleAccesible } = useApp();

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-40 bg-[#0F223D] h-16 flex items-center px-4 shadow-lg border-b border-white/10">
        <div className="flex items-baseline cursor-pointer" onClick={() => navegarA("dashboard")}>
          <span className="font-black text-2xl text-[#E63946] tracking-tight leading-none">LEO</span>
          <span className="font-black text-2xl text-white tracking-tight leading-none">FIT</span>
        </div>
        <div className="ml-auto flex items-center gap-2">
          {/* Botón de Accesibilidad: Letra Grande / Alto Contraste */}
          <button
            onClick={toggleAccesible}
            className={`px-2.5 py-1.5 rounded-xl text-xs font-black flex items-center gap-1.5 transition-all shadow-sm ${
              modoAccesible
                ? "bg-[#F59E0B] text-slate-950 ring-2 ring-white"
                : "bg-white/15 text-white hover:bg-white/25"
            }`}
            aria-label={modoAccesible ? "Desactivar modo letra grande" : "Activar modo letra grande y alto contraste"}
            title="Aumentar tamaño de letra y contraste (Accesibilidad)"
          >
            <span className="material-icons" style={{ fontSize: "18px" }}>format_size</span>
            <span>{modoAccesible ? "A++ Grande" : "A+ Vista"}</span>
          </button>

          <div className="flex items-center gap-1.5 bg-white/10 px-2.5 py-1.5 rounded-xl">
            <span className="material-icons text-white/80" style={{ fontSize: "18px" }}>account_circle</span>
            <span className="text-sm font-bold text-white hidden sm:inline">Víctor</span>
          </div>

          <button
            onClick={togglePrivacidad}
            className={`p-2 rounded-xl transition-colors ${privacidad ? "bg-[#E63946] text-white ring-2 ring-white" : "bg-white/10 text-white hover:bg-white/20"}`}
            aria-label={privacidad ? "Mostrar montos en Soles" : "Ocultar montos en Soles"}
            title={privacidad ? "Mostrar montos" : "Ocultar montos"}
          >
            <span className="material-icons" style={{ fontSize: "20px" }}>
              {privacidad ? "visibility_off" : "visibility"}
            </span>
          </button>

          <button
            onClick={cerrarSesion}
            className="p-2 rounded-xl bg-white/10 text-white/70 hover:bg-[#E63946] hover:text-white transition-colors"
            aria-label="Cerrar sesión"
            title="Cerrar sesión"
          >
            <span className="material-icons" style={{ fontSize: "20px" }}>logout</span>
          </button>
        </div>
      </header>

      <nav className="fixed bottom-0 left-0 right-0 z-40 bg-[#0F223D] border-t-2 border-white/20 flex shadow-2xl safe-bottom">
        {navItems.map((item) => {
          const activo = paginaActual === item.pagina;
          return (
            <button
              key={item.pagina}
              onClick={() => navegarA(item.pagina)}
              className={`flex-1 flex flex-col items-center justify-center py-3 gap-1 transition-all ${
                activo
                  ? "bg-white/15 text-[#E63946] border-t-4 border-[#E63946]"
                  : "text-slate-300 hover:text-white hover:bg-white/5"
              }`}
              aria-label={item.label}
            >
              <span
                className="material-icons transition-transform"
                style={{
                  fontSize: "24px",
                  transform: activo ? "scale(1.15)" : "scale(1)",
                  color: activo ? "#E63946" : "#CBD5E1",
                }}
              >
                {item.icon}
              </span>
              <span className={`text-xs font-black tracking-wide ${activo ? "text-[#E63946]" : "text-slate-200"}`}>
                {item.label}
              </span>
            </button>
          );
        })}
      </nav>
    </>
  );
}

import { useApp } from "../../context/AppContext";

type NavPagina = "dashboard" | "pedidos" | "nuevo-pedido" | "productos";

const navItems: { label: string; icon: string; pagina: NavPagina }[] = [
  { label: "Inicio", icon: "dashboard", pagina: "dashboard" },
  { label: "Pedidos", icon: "receipt_long", pagina: "pedidos" },
  { label: "Nuevo", icon: "add_circle", pagina: "nuevo-pedido" },
  { label: "Productos", icon: "inventory_2", pagina: "productos" },
];

export default function Navbar() {
  const { paginaActual, navegarA, cerrarSesion, privacidad, togglePrivacidad } = useApp();

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-40 bg-[#1D3557] h-14 flex items-center px-4 shadow-md">
        <div className="flex items-baseline">
          <span className="font-black text-2xl text-[#E63946] tracking-tight leading-none">LEO</span>
          <span className="font-black text-2xl text-white tracking-tight leading-none">FIT</span>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <div className="flex items-center gap-1.5">
            <span className="material-icons text-white/50" style={{ fontSize: "18px" }}>account_circle</span>
            <span className="text-sm font-semibold text-white/80 hidden sm:inline">Víctor</span>
          </div>
          <button
            onClick={togglePrivacidad}
            className={`p-1.5 rounded-xl transition-colors ${privacidad ? "bg-[#E63946]/30 hover:bg-[#E63946]/40" : "hover:bg-white/10"}`}
            aria-label={privacidad ? "Mostrar montos" : "Ocultar montos"}
            title={privacidad ? "Mostrar montos" : "Ocultar montos"}
          >
            <span className="material-icons" style={{ fontSize: "18px", color: privacidad ? "#E63946" : "rgba(255,255,255,0.4)" }}>
              {privacidad ? "visibility_off" : "visibility"}
            </span>
          </button>
          <button
            onClick={cerrarSesion}
            className="p-1.5 rounded-xl hover:bg-white/10 transition-colors"
            aria-label="Cerrar sesión"
          >
            <span className="material-icons text-white/40" style={{ fontSize: "18px" }}>logout</span>
          </button>
        </div>
      </header>

      <nav className="fixed bottom-0 left-0 right-0 z-40 bg-[#1D3557] border-t border-white/10 flex safe-bottom">
        {navItems.map((item) => {
          const activo = paginaActual === item.pagina;
          return (
            <button
              key={item.pagina}
              onClick={() => navegarA(item.pagina)}
              className={`flex-1 flex flex-col items-center justify-center py-2.5 gap-0.5 transition-all ${
                activo ? "text-[#E63946]" : "text-white/40 hover:text-white/70"
              }`}
              aria-label={item.label}
            >
              <span
                className="material-icons transition-transform"
                style={{
                  fontSize: "22px",
                  transform: activo ? "scale(1.1)" : "scale(1)",
                }}
              >
                {item.icon}
              </span>
              <span className={`text-[10px] font-bold tracking-wide ${activo ? "text-[#E63946]" : ""}`}>
                {item.label}
              </span>
            </button>
          );
        })}
      </nav>
    </>
  );
}

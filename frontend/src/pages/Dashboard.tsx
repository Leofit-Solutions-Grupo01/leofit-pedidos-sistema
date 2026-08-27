import { useState, useEffect, useCallback } from "react";
import { useApp } from "../context/AppContext";
import Badge from "../components/common/Badge";
import MontoPrivado from "../components/common/MontoPrivado";
import { EstadoPedido, Pedido, estaEnRiesgo, calcularIngresos } from "../data/mockData";

// Hook: anima el número desde 0 hasta el valor objetivo
function useCountUp(target: number) {
  const [val, setVal] = useState(0);
  useEffect(() => {
    if (target === 0) { setVal(0); return; }
    const steps = 24;
    const delay = 500 / steps;
    let step = 0;
    setVal(0);
    const timer = setInterval(() => {
      step++;
      setVal(Math.round((target * step) / steps));
      if (step >= steps) clearInterval(timer);
    }, delay);
    return () => clearInterval(timer);
  }, [target]);
  return val;
}

// Hook: detecta si hay conexión a internet
function useOnlineStatus() {
  const [online, setOnline] = useState(navigator.onLine);
  useEffect(() => {
    const on = () => setOnline(true);
    const off = () => setOnline(false);
    window.addEventListener("online", on);
    window.addEventListener("offline", off);
    return () => { window.removeEventListener("online", on); window.removeEventListener("offline", off); };
  }, []);
  return online;
}

// Tooltip simple al hacer hover
function InfoTooltip({ texto }: { texto: string }) {
  const [visible, setVisible] = useState(false);
  return (
    <span className="relative inline-flex">
      <button
        onMouseEnter={() => setVisible(true)}
        onMouseLeave={() => setVisible(false)}
        onTouchStart={() => setVisible(v => !v)}
        className="ml-1 text-gray-300 hover:text-gray-400 transition-colors"
        aria-label="Más información"
      >
        <span className="material-icons" style={{ fontSize: "14px" }}>info_outline</span>
      </button>
      {visible && (
        <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-52 bg-[#1D3557] text-white text-[11px] font-medium rounded-xl px-3 py-2 shadow-xl z-50 leading-relaxed pointer-events-none">
          {texto}
          <span className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-[#1D3557]" />
        </span>
      )}
    </span>
  );
}

function saludo(): string {
  const h = new Date().getHours();
  if (h < 12) return "Buenos días";
  if (h < 19) return "Buenas tardes";
  return "Buenas noches";
}

function formatMiles(n: number): string {
  return n >= 1000 ? n.toLocaleString("es-PE") : String(n);
}

interface KpiCardProps {
  label: string;
  icon: string;
  valor: number;
  color: string;
  bg: string;
  border: string;
  tooltip: string;
  onClick: () => void;
  alerta?: boolean;
}

function KpiCard({ label, icon, valor, color, bg, border, tooltip, onClick, alerta }: KpiCardProps) {
  const animado = useCountUp(valor);
  return (
    <div
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === "Enter" && onClick()}
      className={`bg-white rounded-2xl p-3 border ${border} shadow-sm text-center w-full transition-all hover:shadow-md active:scale-95 cursor-pointer ${alerta ? "ring-2 ring-[#E63946]/40" : ""}`}
    >
      <div className={`inline-flex items-center justify-center w-8 h-8 rounded-xl ${bg} mb-2`}>
        <span className={`material-icons ${color} ${alerta ? "animate-pulse" : ""}`} style={{ fontSize: "16px" }}>{icon}</span>
      </div>
      <div className={`text-2xl font-black ${valor === 0 ? "text-gray-300" : color} leading-none`}>
        {valor === 0 ? "—" : formatMiles(animado)}
      </div>
      <div className="flex items-center justify-center mt-1">
        <span className="text-[10px] font-semibold text-gray-400 leading-tight">{label}</span>
        <InfoTooltip texto={tooltip} />
      </div>
    </div>
  );
}

function topProductos(pedidos: Pedido[]) {
  const mapa: Record<string, { nombre: string; cantidad: number; ingresos: number }> = {};
  pedidos.forEach((p) => {
    if (p.estado === "Cancelado") return;
    p.items.forEach((item) => {
      if (!mapa[item.nombre]) mapa[item.nombre] = { nombre: item.nombre, cantidad: 0, ingresos: 0 };
      mapa[item.nombre].cantidad += item.cantidad;
      mapa[item.nombre].ingresos += item.cantidad * item.precio;
    });
  });
  return Object.values(mapa).sort((a, b) => b.cantidad - a.cantidad).slice(0, 3);
}

export default function Dashboard() {
  const { pedidos, productos, navegarA, navegarAConFiltro, actualizarEstadoPedido, privacidad } = useApp();
  const isOnline = useOnlineStatus();
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const [ahora, setAhora] = useState(new Date());

  // Reloj en vivo — demuestra que los datos se actualizan sin recargar la página
  useEffect(() => {
    const t = setInterval(() => setAhora(new Date()), 60_000);
    return () => clearInterval(t);
  }, []);

  const HOY = ahora.toISOString().split("T")[0];
  const pedidosHoy = pedidos.filter((p) => p.fecha === HOY && p.estado !== "Cancelado");
  const pedidosActivos = pedidos.filter((p) => p.estado !== "Cancelado");
  const pedidosEnRiesgo = pedidos.filter(estaEnRiesgo);
  const ingresosHoy = pedidosHoy.filter((p) => p.estado === "Entregado").reduce((a, p) => a + p.total, 0);
  const ingresosTotal = calcularIngresos(pedidos);
  const productosStockBajo = productos.filter((p) => p.stock <= 5);
  const top3 = topProductos(pedidos);
  const ultimosPedidos = pedidos.filter((p) => p.estado !== "Cancelado").slice(0, 5);

  const estadosPipeline: { estado: EstadoPedido; label: string; bg: string; color: string }[] = [
    { estado: "Recibido",    label: "Recibido",    bg: "bg-[#3498DB]", color: "#3498DB" },
    { estado: "Preparación", label: "Preparación", bg: "bg-[#F1C40F]", color: "#B7950B" },
    { estado: "Camino",      label: "En Camino",   bg: "bg-[#E67E22]", color: "#E67E22" },
    { estado: "Entregado",   label: "Entregado",   bg: "bg-[#27AE60]", color: "#27AE60" },
  ];

  const kpis = [
    {
      label: "Creados hoy",
      icon: "event",
      valor: pedidosHoy.length,
      color: "text-[#1D3557]",
      bg: "bg-[#1D3557]/10",
      border: "border-[#1D3557]/20",
      filtro: "Todos" as const,
      tooltip: "Pedidos CREADOS hoy (no entregados). Se reinicia a medianoche. Incluye WhatsApp, llamadas y sistema.",
    },
    {
      label: "Pendientes",
      icon: "schedule",
      valor: pedidosActivos.filter((p) => p.estado === "Recibido" || p.estado === "Preparación").length,
      color: pedidosEnRiesgo.length > 0 ? "text-[#E63946]" : "text-[#E67E22]",
      bg: pedidosEnRiesgo.length > 0 ? "bg-[#E63946]/10" : "bg-[#E67E22]/10",
      border: pedidosEnRiesgo.length > 0 ? "border-[#E63946]/30" : "border-[#E67E22]/20",
      filtro: "Recibido" as EstadoPedido,
      alerta: pedidosEnRiesgo.length > 0,
      tooltip: "Pedidos en estado Recibido o Preparación. Los que llevan más de 24h se marcan como 'En Riesgo'. Solo Víctor decide cuándo avanzarlos.",
    },
    {
      label: "En Camino",
      icon: "local_shipping",
      valor: pedidosActivos.filter((p) => p.estado === "Camino").length,
      color: "text-[#3498DB]",
      bg: "bg-[#3498DB]/10",
      border: "border-[#3498DB]/20",
      filtro: "Camino" as EstadoPedido,
      tooltip: "Pedidos ya enviados con el delivery. Actualmente el estado se actualiza manualmente. El delivery confirma por WhatsApp.",
    },
    {
      label: "Entregados",
      icon: "check_circle",
      valor: pedidosActivos.filter((p) => p.estado === "Entregado").length,
      color: "text-[#27AE60]",
      bg: "bg-[#27AE60]/10",
      border: "border-[#27AE60]/20",
      filtro: "Entregado" as EstadoPedido,
      tooltip: "Víctor confirma la entrega al recibir notificación del delivery. Si hay reclamo, el pedido puede marcarse como Cancelado.",
    },
  ];

  const handleCambioEstado = useCallback((id: string, estado: EstadoPedido) => {
    actualizarEstadoPedido(id, estado);
    setEditandoId(null);
  }, [actualizarEstadoPedido]);

  return (
    <div className="pt-14 pb-24 min-h-screen bg-[#F1FAEE]">
      <div className="max-w-2xl mx-auto px-4 py-4 space-y-3">

        {/* Offline banner */}
        {!isOnline && (
          <div className="bg-yellow-50 border-2 border-yellow-200 rounded-2xl px-4 py-3 flex items-center gap-3">
            <span className="material-icons text-yellow-500" style={{ fontSize: "20px" }}>wifi_off</span>
            <div>
              <p className="text-sm font-bold text-yellow-800">Sin conexión a internet</p>
              <p className="text-xs text-yellow-600 font-medium">Mostrando datos guardados en caché. Los cambios se sincronizarán al reconectarse.</p>
            </div>
          </div>
        )}

        {/* Greeting + Revenue hero */}
        <div className="bg-[#1D3557] rounded-3xl p-5 text-white overflow-hidden relative">
          <div className="absolute top-0 right-0 w-36 h-36 bg-white/5 rounded-full -translate-y-10 translate-x-10" />
          <div className="absolute bottom-0 right-16 w-24 h-24 bg-[#E63946]/15 rounded-full translate-y-8" />
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-white/50 text-xs font-semibold uppercase tracking-widest">{saludo()}, Víctor</p>
              <p className="text-white/30 text-xs font-medium mt-0.5">
                {ahora.toLocaleDateString("es-PE", { weekday: "long", day: "numeric", month: "long" })}
                {" · "}
                {ahora.toLocaleTimeString("es-PE", { hour: "2-digit", minute: "2-digit" })}
              </p>
            </div>
            {/* indicador "en vivo" */}
            <div className="flex items-center gap-1.5 bg-white/10 rounded-full px-2.5 py-1">
              <span className="w-1.5 h-1.5 rounded-full bg-[#27AE60] animate-pulse" />
              <span className="text-[10px] font-bold text-white/60">EN VIVO</span>
            </div>
          </div>
          <div className="flex items-end justify-between relative">
            <div>
              <p className="text-white/40 text-xs font-semibold mb-0.5">Ingresos totales cobrados</p>
              <MontoPrivado
                valor={ingresosTotal}
                privacidad={privacidad}
                className="text-3xl font-black text-white leading-none block"
              />
              <p className="text-white/30 text-[11px] font-medium mt-1">
                {pedidos.filter((p) => p.estado === "Entregado").length} pedidos entregados · {pedidos.filter((p) => p.estado === "Cancelado").length} cancelados
              </p>
            </div>
            <div className="text-right">
              <p className="text-white/40 text-xs font-semibold mb-0.5">Hoy</p>
              <MontoPrivado
                valor={ingresosHoy}
                privacidad={privacidad}
                className={`text-2xl font-black block ${ingresosHoy > 0 ? "text-[#27AE60]" : "text-white/30"}`}
              />
              <p className="text-white/30 text-[11px] font-medium mt-1">
                {pedidosHoy.length} pedido{pedidosHoy.length !== 1 ? "s" : ""}
              </p>
            </div>
          </div>
        </div>

        {/* KPI strip — cada tarjeta es clickeable y navega al historial filtrado */}
        <div className="grid grid-cols-4 gap-2">
          {kpis.map((kpi) => (
            <KpiCard
              key={kpi.label}
              label={kpi.label}
              icon={kpi.icon}
              valor={kpi.valor}
              color={kpi.color}
              bg={kpi.bg}
              border={kpi.border}
              tooltip={kpi.tooltip}
              alerta={"alerta" in kpi ? kpi.alerta : false}
              onClick={() => navegarAConFiltro("pedidos", kpi.filtro)}
            />
          ))}
        </div>

        {/* Alerta: pedidos En Riesgo */}
        {pedidosEnRiesgo.length > 0 && (
          <div className="bg-[#E63946]/8 border-2 border-[#E63946]/25 rounded-2xl p-4">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 bg-[#E63946] rounded-xl flex items-center justify-center shrink-0">
                <span className="material-icons text-white" style={{ fontSize: "18px" }}>warning</span>
              </div>
              <div>
                <p className="text-sm font-bold text-[#E63946]">
                  {pedidosEnRiesgo.length} pedido{pedidosEnRiesgo.length !== 1 ? "s" : ""} En Riesgo
                </p>
                <p className="text-[11px] text-[#E63946]/70 font-medium">Llevan más de 24 h sin actualizarse</p>
              </div>
              <button
                onClick={() => navegarAConFiltro("pedidos", "Recibido")}
                className="ml-auto text-xs text-[#E63946] font-bold hover:underline flex items-center gap-0.5 shrink-0"
              >
                Ver todos
                <span className="material-icons" style={{ fontSize: "14px" }}>chevron_right</span>
              </button>
            </div>
            <div className="space-y-2">
              {pedidosEnRiesgo.slice(0, 3).map((p) => {
                const diasAtraso = Math.floor((new Date(HOY).getTime() - new Date(p.fecha).getTime()) / 86_400_000);
                return (
                  <div key={p.id} className="bg-white rounded-xl px-3 py-2.5 flex items-center gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5">
                        <span className="text-xs font-mono font-bold text-gray-400">{p.numero}</span>
                        <span className="text-xs font-semibold text-[#1A1A1A] truncate">{p.cliente.nombre}</span>
                      </div>
                      {p.notas && <p className="text-[10px] text-gray-400 truncate mt-0.5">{p.notas}</p>}
                    </div>
                    <span className="text-[10px] font-bold text-[#E63946] bg-[#E63946]/10 rounded-full px-2 py-0.5 whitespace-nowrap shrink-0">
                      {diasAtraso}d atraso
                    </span>
                    <a
                      href={`tel:${p.cliente.telefono}`}
                      className="p-1.5 bg-[#27AE60] rounded-xl shrink-0"
                      aria-label={`Llamar a ${p.cliente.nombre}`}
                      onClick={(e) => e.stopPropagation()}
                    >
                      <span className="material-icons text-white" style={{ fontSize: "16px" }}>call</span>
                    </a>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Alerta: stock bajo */}
        {productosStockBajo.length > 0 && (
          <div
            className="bg-[#F1C40F]/8 border-2 border-[#F1C40F]/30 rounded-2xl px-4 py-3 flex items-center gap-3 cursor-pointer active:scale-[0.99] transition-transform"
            onClick={() => navegarA("productos")}
          >
            <span className="material-icons text-[#B7950B]" style={{ fontSize: "20px" }}>inventory</span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold text-[#B7950B]">
                {productosStockBajo.length} producto{productosStockBajo.length !== 1 ? "s" : ""} con stock bajo
              </p>
              <p className="text-[11px] text-[#B7950B]/70 font-medium truncate">
                {productosStockBajo.map((p) => `${p.nombre} (${p.stock})`).join(", ")}
              </p>
            </div>
            <span className="material-icons text-[#B7950B]/50" style={{ fontSize: "18px" }}>chevron_right</span>
          </div>
        )}

        {/* Pipeline de estados */}
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
          <div className="flex items-center gap-2 mb-3">
            <h2 className="text-sm font-bold text-[#1D3557]">Pipeline de pedidos activos</h2>
            <InfoTooltip texto="Distribución de todos los pedidos activos por estado. Los cancelados no se contabilizan." />
          </div>
          <div className="flex gap-1 h-2.5 rounded-full overflow-hidden mb-3 bg-gray-100">
            {estadosPipeline.map(({ estado, bg }) => {
              const cant = pedidosActivos.filter((p) => p.estado === estado).length;
              const pct = pedidosActivos.length > 0 ? (cant / pedidosActivos.length) * 100 : 0;
              if (pct === 0) return null;
              return <div key={estado} className={`${bg} h-full`} style={{ width: `${pct}%` }} />;
            })}
          </div>
          <div className="grid grid-cols-2 gap-x-4 gap-y-2">
            {estadosPipeline.map(({ estado, label, bg, color }) => {
              const cant = pedidosActivos.filter((p) => p.estado === estado).length;
              const pct = pedidosActivos.length > 0 ? Math.round((cant / pedidosActivos.length) * 100) : 0;
              return (
                <button
                  key={estado}
                  onClick={() => navegarAConFiltro("pedidos", estado)}
                  className="flex items-center gap-2 hover:opacity-70 transition-opacity text-left"
                >
                  <div className={`w-2 h-2 rounded-full ${bg} shrink-0`} />
                  <span className="text-xs text-gray-500 font-medium flex-1">{label}</span>
                  <span className="text-xs font-black" style={{ color }}>{cant}</span>
                  <span className="text-[10px] text-gray-300 font-semibold w-7 text-right">{pct}%</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Top productos */}
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
          <h2 className="text-sm font-bold text-[#1D3557] mb-3">Productos más vendidos</h2>
          {top3.length === 0 ? (
            <p className="text-xs text-gray-400 text-center py-4">Sin ventas registradas aún</p>
          ) : (
            <div className="space-y-3">
              {top3.map((prod, i) => {
                const pct = Math.round((prod.cantidad / top3[0].cantidad) * 100);
                const medalColor = ["text-[#F1C40F]", "text-gray-400", "text-[#CD7F32]"][i];
                return (
                  <div key={prod.nombre}>
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center gap-1.5">
                        <span className={`material-icons ${medalColor}`} style={{ fontSize: "15px" }}>emoji_events</span>
                        <span className="text-sm font-semibold text-[#1A1A1A]">{prod.nombre}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-xs font-black text-[#1D3557]">{prod.cantidad} uds</span>
                        <span className="text-[10px] text-gray-400 font-medium ml-1.5">S/{prod.ingresos.toFixed(0)}</span>
                      </div>
                    </div>
                    <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                      <div className="h-full bg-[#E63946] rounded-full" style={{ width: `${pct}%`, opacity: 1 - i * 0.2 }} />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Acciones rápidas */}
        <div className="grid grid-cols-3 gap-2">
          {[
            { label: "Nuevo Pedido", icon: "add_circle", pagina: "nuevo-pedido" as const, color: "text-[#E63946]", bg: "bg-[#E63946]/10" },
            { label: "Ver Pedidos", icon: "receipt_long", pagina: "pedidos" as const, color: "text-[#3498DB]", bg: "bg-[#3498DB]/10" },
            { label: "Productos", icon: "inventory_2", pagina: "productos" as const, color: "text-[#27AE60]", bg: "bg-[#27AE60]/10" },
          ].map((acc) => (
            <button
              key={acc.label}
              onClick={() => navegarA(acc.pagina)}
              className="bg-white rounded-2xl p-3 flex flex-col items-center gap-2 shadow-sm border border-gray-100 hover:shadow-md active:scale-95 transition-all"
            >
              <div className={`w-10 h-10 ${acc.bg} rounded-xl flex items-center justify-center`}>
                <span className={`material-icons ${acc.color}`} style={{ fontSize: "22px" }}>{acc.icon}</span>
              </div>
              <span className="text-[11px] font-bold text-gray-600 leading-tight text-center">{acc.label}</span>
            </button>
          ))}
        </div>

        {/* Últimos pedidos — con cambio de estado directo desde el dashboard */}
        <div className="bg-white rounded-2xl shadow-sm overflow-hidden border border-gray-100">
          <div className="flex items-center justify-between px-4 py-3.5 border-b border-gray-100">
            <div className="flex items-center gap-2">
              <h2 className="font-bold text-[#1D3557]">Últimos Pedidos</h2>
              <InfoTooltip texto="Pedidos más recientes, ordenados por fecha de creación. Toca el icono de editar para cambiar el estado sin salir del dashboard." />
            </div>
            <button onClick={() => navegarA("pedidos")} className="text-xs text-[#E63946] font-bold hover:underline flex items-center gap-0.5">
              Ver todos <span className="material-icons" style={{ fontSize: "14px" }}>chevron_right</span>
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-[#F1FAEE]">
                  <th className="px-4 py-2.5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-wider">N°</th>
                  <th className="px-4 py-2.5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-wider">Cliente</th>
                  <th className="px-4 py-2.5 text-right text-[10px] font-bold text-gray-400 uppercase tracking-wider">Total</th>
                  <th className="px-4 py-2.5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-wider">Estado</th>
                  <th className="px-4 py-2.5" />
                </tr>
              </thead>
              <tbody>
                {ultimosPedidos.map((pedido, i) => (
                  <tr key={pedido.id} className={`transition-colors hover:bg-[#F1FAEE]/60 ${i < ultimosPedidos.length - 1 ? "border-b border-gray-50" : ""}`}>
                    <td className="px-4 py-3 font-mono text-xs font-semibold text-gray-500">{pedido.numero}</td>
                    <td className="px-4 py-3">
                      <div className="text-sm font-semibold text-[#1A1A1A] max-w-[100px] truncate">{pedido.cliente.nombre}</div>
                      <div className="text-[10px] text-gray-400 mt-0.5">{pedido.fecha}</div>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <MontoPrivado valor={pedido.total} privacidad={privacidad} className="text-sm font-black text-[#1D3557]" />
                    </td>
                    <td className="px-4 py-3">
                      {editandoId === pedido.id ? (
                        <select
                          value={pedido.estado}
                          onChange={(e) => handleCambioEstado(pedido.id, e.target.value as EstadoPedido)}
                          onBlur={() => setEditandoId(null)}
                          autoFocus
                          className="text-xs border-2 border-[#E63946] rounded-lg px-1.5 py-1 focus:outline-none"
                        >
                          {(["Recibido", "Preparación", "Camino", "Entregado", "Cancelado"] as EstadoPedido[]).map((e) => (
                            <option key={e}>{e}</option>
                          ))}
                        </select>
                      ) : (
                        <Badge estado={pedido.estado as EstadoPedido} enRiesgo={estaEnRiesgo(pedido)} />
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => setEditandoId(editandoId === pedido.id ? null : pedido.id)}
                        className="p-1.5 rounded-xl hover:bg-[#1D3557]/10 transition-colors"
                        aria-label="Cambiar estado"
                      >
                        <span className="material-icons text-[#1D3557]/30" style={{ fontSize: "16px" }}>edit</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <button
        onClick={() => navegarA("nuevo-pedido")}
        className="fixed bottom-20 right-4 bg-[#E63946] hover:bg-[#C62828] active:scale-95 text-white w-14 h-14 rounded-full shadow-xl shadow-[#E63946]/40 flex items-center justify-center transition-all z-30"
        aria-label="Nuevo pedido"
      >
        <span className="material-icons text-2xl">add</span>
      </button>
    </div>
  );
}

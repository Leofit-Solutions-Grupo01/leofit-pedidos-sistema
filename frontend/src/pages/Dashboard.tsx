/**
 * @file Dashboard.tsx
 * @description Tablero de control operativo, métricas de ingresos con privacidad granular y pipeline
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { useState, useEffect, useCallback } from "react";
import { useApp } from "../context/AppContext";
import Badge from "../components/common/Badge";
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
        className="ml-1 text-slate-400 hover:text-slate-600 transition-colors"
        aria-label="Más información"
      >
        <span className="material-icons" style={{ fontSize: "15px" }}>info_outline</span>
      </button>
      {visible && (
        <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-56 bg-[#0F223D] text-white text-xs font-normal rounded-xl px-3 py-2 shadow-xl z-50 leading-relaxed pointer-events-none border border-slate-700">
          {texto}
          <span className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-[#0F223D]" />
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
      className={`bg-white rounded-2xl p-3.5 border ${border} shadow-sm text-center w-full transition-all hover:shadow-md active:scale-95 cursor-pointer ${alerta ? "ring-2 ring-[#E63946]/40" : ""}`}
    >
      <div className={`inline-flex items-center justify-center w-9 h-9 rounded-xl ${bg} mb-2`}>
        <span className={`material-icons ${color} ${alerta ? "animate-pulse" : ""}`} style={{ fontSize: "18px" }}>{icon}</span>
      </div>
      <div className={`text-2xl font-bold font-display ${valor === 0 ? "text-slate-300" : color} leading-none`}>
        {valor === 0 ? "—" : formatMiles(animado)}
      </div>
      <div className="flex items-center justify-center mt-1.5">
        <span className="text-xs font-semibold text-slate-700 leading-tight">{label}</span>
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
  const { pedidos, productos, navegarA, navegarAConFiltro, actualizarEstadoPedido, modoAccesible } = useApp();
  const isOnline = useOnlineStatus();
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const [ahora, setAhora] = useState(new Date());
  const [ocultarTotal, setOcultarTotal] = useState(false);
  const [ocultarHoy, setOcultarHoy] = useState(false);

  // Reloj en vivo
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
  const ultimosPedidos = [...pedidos].slice(0, 5);

  const estadosPipeline: { estado: EstadoPedido; label: string; bg: string; color: string }[] = [
    { estado: "Recibido", label: "Recibido", bg: "bg-[#3498DB]", color: "#3498DB" },
    { estado: "Preparación", label: "En Preparación", bg: "bg-[#F1C40F]", color: "#B7950B" },
    { estado: "Camino", label: "En Camino", bg: "bg-[#E67E22]", color: "#E67E22" },
    { estado: "Entregado", label: "Entregado", bg: "bg-[#27AE60]", color: "#27AE60" },
  ];

  const kpis = [
    {
      label: "Creados hoy",
      icon: "calendar_today",
      valor: pedidosHoy.length,
      color: "text-[#0F223D]",
      bg: "bg-blue-100",
      border: "border-blue-300",
      filtro: "Todos" as const,
      tooltip: "Pedidos CREADOS hoy. Incluye WhatsApp, llamadas y sistema.",
    },
    {
      label: "Pendientes",
      icon: "schedule",
      valor: pedidosActivos.filter((p) => p.estado === "Recibido" || p.estado === "Preparación").length,
      color: pedidosEnRiesgo.length > 0 ? "text-red-700" : "text-amber-800",
      bg: pedidosEnRiesgo.length > 0 ? "bg-red-100" : "bg-amber-100",
      border: pedidosEnRiesgo.length > 0 ? "border-red-400" : "border-amber-300",
      filtro: "Recibido" as EstadoPedido,
      alerta: pedidosEnRiesgo.length > 0,
      tooltip: "Pedidos en estado Recibido o Preparación.",
    },
    {
      label: "En Camino",
      icon: "local_shipping",
      valor: pedidosActivos.filter((p) => p.estado === "Camino").length,
      color: "text-blue-900",
      bg: "bg-blue-100",
      border: "border-blue-400",
      filtro: "Camino" as EstadoPedido,
      tooltip: "Pedidos ya enviados con el delivery.",
    },
    {
      label: "Entregados",
      icon: "check_circle",
      valor: pedidosActivos.filter((p) => p.estado === "Entregado").length,
      color: "text-emerald-900",
      bg: "bg-emerald-100",
      border: "border-emerald-400",
      filtro: "Entregado" as EstadoPedido,
      tooltip: "Pedidos entregados confirmados.",
    },
  ];

  const handleCambioEstado = useCallback((id: string, estado: EstadoPedido) => {
    actualizarEstadoPedido(id, estado);
    setEditandoId(null);
  }, [actualizarEstadoPedido]);

  return (
    <div className={`pt-16 pb-32 sm:pb-28 min-h-screen ${modoAccesible ? "bg-[#E2E8F0]" : "bg-[#F1FAEE]"}`}>
      <div className="max-w-5xl mx-auto px-3 sm:px-6 py-4 space-y-4 sm:space-y-5">

        {/* Offline banner */}
        {!isOnline && (
          <div className="bg-amber-100 border-2 border-amber-400 rounded-2xl px-4 py-3 flex items-center gap-3">
            <span className="material-icons text-amber-800" style={{ fontSize: "24px" }}>wifi_off</span>
            <div>
              <p className="text-base font-bold text-amber-950">Sin conexión a internet</p>
              <p className="text-sm text-amber-900 font-medium">Mostrando datos guardados en caché. Los cambios se sincronizarán al reconectarse.</p>
            </div>
          </div>
        )}

        {/* Greeting + Revenue hero */}
        <div className="bg-[#0F223D] rounded-3xl p-5 sm:p-6 text-white overflow-hidden relative shadow-xl border border-slate-700">
          <div className="flex items-start justify-between gap-2 mb-4">
            <div>
              <p className="text-amber-400 text-xs font-bold uppercase tracking-wider">{saludo()}, Víctor</p>
              <p className="text-slate-200 text-xs sm:text-sm font-medium mt-0.5">
                {ahora.toLocaleDateString("es-PE", { weekday: "long", day: "numeric", month: "long" })}
                {" · "}
                {ahora.toLocaleTimeString("es-PE", { hour: "2-digit", minute: "2-digit" })}
              </p>
            </div>
            {/* indicador "en vivo" */}
            <div className="flex items-center gap-1.5 bg-white/20 rounded-full px-2.5 sm:px-3 py-1 sm:py-1.5 border border-white/30 shrink-0">
              <span className="w-2 sm:w-2.5 h-2 sm:h-2.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-[10px] sm:text-xs font-bold text-white tracking-wide">EN VIVO</span>
            </div>
          </div>
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 relative pt-1 sm:pt-2">
            <div>
              <div className="flex items-center gap-1.5 mb-1">
                <p className="text-slate-300 text-xs sm:text-sm font-medium">Ingresos totales cobrados</p>
                <button
                  type="button"
                  onClick={() => setOcultarTotal((v) => !v)}
                  className="text-slate-400 hover:text-white p-0.5 rounded-md hover:bg-white/10 transition-colors flex items-center"
                  title={ocultarTotal ? "Mostrar ingresos totales" : "Ocultar ingresos totales"}
                  aria-label={ocultarTotal ? "Mostrar ingresos totales" : "Ocultar ingresos totales"}
                >
                  <span className="material-icons" style={{ fontSize: "16px" }}>
                    {ocultarTotal ? "visibility_off" : "visibility"}
                  </span>
                </button>
              </div>
              {ocultarTotal ? (
                <span className={`${modoAccesible ? "text-3xl sm:text-4xl" : "text-2xl sm:text-3xl"} font-extrabold font-display text-slate-400 leading-none block tracking-widest`}>
                  ••••••
                </span>
              ) : (
                <span className={`${modoAccesible ? "text-3xl sm:text-4xl" : "text-2xl sm:text-3xl"} font-extrabold font-display text-white leading-none block`}>
                  S/{ingresosTotal.toFixed(2)}
                </span>
              )}
              <p className="text-slate-300 text-xs font-normal mt-2">
                {pedidos.filter((p) => p.estado === "Entregado").length} pedidos entregados · {pedidos.filter((p) => p.estado === "Cancelado").length} cancelados
              </p>
            </div>
            <div className="sm:text-right border-t sm:border-t-0 border-white/10 pt-3 sm:pt-0">
              <div className="flex items-center sm:justify-end gap-1.5 mb-1">
                <p className="text-slate-300 text-xs sm:text-sm font-medium">Hoy</p>
                <button
                  type="button"
                  onClick={() => setOcultarHoy((v) => !v)}
                  className="text-slate-400 hover:text-white p-0.5 rounded-md hover:bg-white/10 transition-colors flex items-center"
                  title={ocultarHoy ? "Mostrar ingresos de hoy" : "Ocultar ingresos de hoy"}
                  aria-label={ocultarHoy ? "Mostrar ingresos de hoy" : "Ocultar ingresos de hoy"}
                >
                  <span className="material-icons" style={{ fontSize: "16px" }}>
                    {ocultarHoy ? "visibility_off" : "visibility"}
                  </span>
                </button>
              </div>
              {ocultarHoy ? (
                <span className={`${modoAccesible ? "text-2xl sm:text-3xl" : "text-xl sm:text-2xl"} font-extrabold font-display text-slate-400 block tracking-widest`}>
                  ••••••
                </span>
              ) : (
                <span className={`${modoAccesible ? "text-2xl sm:text-3xl" : "text-xl sm:text-2xl"} font-extrabold font-display block ${ingresosHoy > 0 ? "text-emerald-400" : "text-slate-400"}`}>
                  S/{ingresosHoy.toFixed(2)}
                </span>
              )}
              <p className="text-slate-300 text-xs font-normal mt-1 sm:mt-2">
                {pedidosHoy.length} pedido{pedidosHoy.length !== 1 ? "s" : ""}
              </p>
            </div>
          </div>
        </div>

        {/* KPI strip */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-3">
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
          <div className="bg-red-50 border-2 border-red-300 rounded-3xl p-4 sm:p-5 shadow-sm">
            <div className="flex items-center gap-2.5 sm:gap-3 mb-3">
              <div className="w-9 h-9 sm:w-10 sm:h-10 bg-red-600 rounded-2xl flex items-center justify-center shrink-0 shadow-md">
                <span className="material-icons text-white" style={{ fontSize: "20px" }}>warning</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm sm:text-base font-bold text-red-950">
                  {pedidosEnRiesgo.length} pedido{pedidosEnRiesgo.length !== 1 ? "s" : ""} En Riesgo
                </p>
                <p className="text-xs text-red-800 font-medium">Llevan más de 24 h sin actualizarse</p>
              </div>
              <button
                onClick={() => navegarAConFiltro("pedidos", "Recibido")}
                className="text-xs text-red-800 font-bold hover:underline flex items-center gap-0.5 sm:gap-1 shrink-0 bg-red-100 px-2.5 sm:px-3 py-1.5 rounded-xl border border-red-200"
              >
                <span>Ver todos</span>
                <span className="material-icons" style={{ fontSize: "16px" }}>chevron_right</span>
              </button>
            </div>
            <div className="space-y-2.5">
              {pedidosEnRiesgo.slice(0, 3).map((p) => {
                const diasAtraso = Math.floor((new Date(HOY).getTime() - new Date(p.fecha).getTime()) / 86_400_000);
                return (
                  <div key={p.id} className="bg-white rounded-2xl px-3.5 sm:px-4 py-3 flex items-center gap-2.5 sm:gap-3 border border-red-100 shadow-sm">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5 sm:gap-2 flex-wrap">
                        <span className="text-xs font-mono font-bold text-slate-700">{p.numero}</span>
                        <span className="text-xs sm:text-sm font-semibold text-slate-900 truncate max-w-[120px] sm:max-w-none">{p.cliente.nombre}</span>
                      </div>
                      {p.notas && <p className="text-xs text-slate-600 font-normal truncate mt-0.5">{p.notas}</p>}
                    </div>
                    <span className="text-[11px] sm:text-xs font-bold text-red-800 bg-red-100 border border-red-200 rounded-full px-2 sm:px-2.5 py-0.5 sm:py-1 whitespace-nowrap shrink-0">
                      {diasAtraso}d atraso
                    </span>
                    <a
                      href={`tel:${p.cliente.telefono}`}
                      className="p-2 sm:p-2.5 bg-emerald-700 hover:bg-emerald-800 rounded-xl shrink-0 shadow-md text-white flex items-center justify-center"
                      aria-label={`Llamar a ${p.cliente.nombre}`}
                      title={`Llamar a ${p.cliente.nombre} (${p.cliente.telefono})`}
                      onClick={(e) => e.stopPropagation()}
                    >
                      <span className="material-icons text-white" style={{ fontSize: "18px" }}>call</span>
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
            className="bg-amber-50 border-2 border-amber-300 rounded-3xl px-4 sm:px-5 py-3.5 sm:py-4 flex items-center gap-3 cursor-pointer active:scale-[0.99] transition-transform shadow-sm"
            onClick={() => navegarA("productos")}
          >
            <div className="w-9 h-9 sm:w-10 sm:h-10 bg-amber-500 rounded-2xl flex items-center justify-center shrink-0">
              <span className="material-icons text-white" style={{ fontSize: "20px" }}>inventory</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm sm:text-base font-bold text-amber-950">
                {productosStockBajo.length} producto{productosStockBajo.length !== 1 ? "s" : ""} con stock bajo
              </p>
              <p className="text-xs text-amber-900 font-medium truncate">
                {productosStockBajo.map((p) => `${p.nombre} (${p.stock} uds)`).join(", ")}
              </p>
            </div>
            <span className="material-icons text-amber-800" style={{ fontSize: "20px" }}>chevron_right</span>
          </div>
        )}

        {/* Pipeline de estados */}
        <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-sm border border-slate-200">
          <div className="flex items-center gap-2 mb-3">
            <h2 className="text-sm sm:text-base font-bold text-slate-900">Pipeline de pedidos activos</h2>
            <InfoTooltip texto="Distribución de todos los pedidos activos por estado. Los cancelados no se contabilizan." />
          </div>
          <div className="flex gap-1 h-3 rounded-full overflow-hidden mb-4 bg-slate-100 border border-slate-200">
            {estadosPipeline.map(({ estado, bg }) => {
              const cant = pedidosActivos.filter((p) => p.estado === estado).length;
              const pct = pedidosActivos.length > 0 ? (cant / pedidosActivos.length) * 100 : 0;
              if (pct === 0) return null;
              return <div key={estado} className={`${bg} h-full`} style={{ width: `${pct}%` }} />;
            })}
          </div>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-3">
            {estadosPipeline.map(({ estado, label, bg, color }) => {
              const cant = pedidosActivos.filter((p) => p.estado === estado).length;
              const pct = pedidosActivos.length > 0 ? Math.round((cant / pedidosActivos.length) * 100) : 0;
              return (
                <button
                  key={estado}
                  onClick={() => navegarAConFiltro("pedidos", estado)}
                  className="flex items-center gap-2 p-2 rounded-xl hover:bg-slate-100 transition-colors text-left border border-slate-100 hover:border-slate-200"
                >
                  <div className={`w-3 h-3 rounded-full ${bg} shrink-0 border border-slate-300`} />
                  <span className="text-xs font-semibold text-slate-700 flex-1 truncate">{label}</span>
                  <span className="text-xs sm:text-sm font-bold font-mono shrink-0" style={{ color }}>{cant}</span>
                  <span className="text-[11px] text-slate-500 font-medium shrink-0">({pct}%)</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Acciones rápidas (Responsive: Stack on narrow mobile, horizontal on sm+) */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 sm:gap-3">
          {[
            { label: "Nuevo Pedido", desc: "Registrar venta", icon: "add_circle", pagina: "nuevo-pedido" as const, color: "text-[#E63946]", bg: "bg-red-50 border-red-200" },
            { label: "Ver Pedidos", desc: "Historial completo", icon: "receipt_long", pagina: "pedidos" as const, color: "text-[#1D3557]", bg: "bg-blue-50 border-blue-200" },
            { label: "Inventario", desc: "Stock de prendas", icon: "inventory_2", pagina: "productos" as const, color: "text-emerald-800", bg: "bg-emerald-50 border-emerald-200" },
          ].map((acc) => (
            <button
              key={acc.label}
              onClick={() => navegarA(acc.pagina)}
              className={`bg-white rounded-2xl sm:rounded-3xl p-3 sm:p-4 flex flex-row sm:flex-col items-center justify-start sm:justify-center gap-3 sm:gap-2 shadow-sm border ${acc.bg} hover:shadow-md active:scale-98 transition-all text-left sm:text-center`}
            >
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl sm:rounded-2xl flex items-center justify-center bg-slate-50 border border-slate-200 shadow-inner shrink-0">
                <span className={`material-icons ${acc.color}`} style={{ fontSize: "24px" }}>{acc.icon}</span>
              </div>
              <div className="flex flex-col">
                <span className="text-xs sm:text-sm font-bold text-slate-900 leading-tight">{acc.label}</span>
                <span className="text-[11px] text-slate-500 font-medium mt-0.5">{acc.desc}</span>
              </div>
            </button>
          ))}
        </div>

        {/* Últimos pedidos — Card View en Móvil (<640px) y Tabla en Tablet/Desktop (>=640px) */}
        <div className="bg-white rounded-3xl shadow-sm overflow-hidden border border-slate-200">
          <div className="flex items-center justify-between px-4 sm:px-5 py-3.5 sm:py-4 border-b border-slate-100 bg-slate-50/50">
            <div className="flex items-center gap-2">
              <h2 className="font-bold text-sm sm:text-base text-slate-900">Últimos Pedidos</h2>
              <InfoTooltip texto="Pedidos más recientes, ordenados por fecha de creación. Toca el icono de editar para cambiar el estado sin salir del dashboard." />
            </div>
            <button onClick={() => navegarA("pedidos")} className="text-xs text-[#E63946] font-bold hover:underline flex items-center gap-1 bg-red-50 px-2.5 py-1 rounded-xl border border-red-100">
              Ver todos <span className="material-icons" style={{ fontSize: "16px" }}>chevron_right</span>
            </button>
          </div>

          {/* VISTA MÓVIL: Tarjetas legibles en pantallas estrechas (<640px) */}
          <div className="block sm:hidden divide-y divide-slate-100">
            {ultimosPedidos.map((pedido) => (
              <div key={pedido.id} className="p-3.5 space-y-2.5">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-1.5 mb-1">
                      <span className="font-mono text-xs font-bold text-slate-700 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">{pedido.numero}</span>
                      <span className="text-xs text-slate-500 font-normal">{pedido.fecha}</span>
                    </div>
                    <div className="text-sm font-bold text-slate-900">{pedido.cliente.nombre}</div>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-bold font-mono text-slate-900">S/{pedido.total.toFixed(2)}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between gap-2 pt-1">
                  <div className="flex-1">
                    {editandoId === pedido.id ? (
                      <select
                        value={pedido.estado}
                        onChange={(e) => handleCambioEstado(pedido.id, e.target.value as EstadoPedido)}
                        onBlur={() => setEditandoId(null)}
                        autoFocus
                        className="text-xs font-semibold border-2 border-[#E63946] rounded-xl px-2 py-1.5 focus:outline-none bg-white shadow-md w-full"
                      >
                        {(["Recibido", "Preparación", "Camino", "Entregado", "Cancelado"] as EstadoPedido[]).map((e) => (
                          <option key={e}>{e}</option>
                        ))}
                      </select>
                    ) : (
                      <Badge estado={pedido.estado as EstadoPedido} enRiesgo={estaEnRiesgo(pedido)} />
                    )}
                  </div>
                  <button
                    onClick={() => setEditandoId(editandoId === pedido.id ? null : pedido.id)}
                    className="p-2 rounded-xl bg-slate-100 hover:bg-[#0F223D] hover:text-white text-slate-700 transition-colors border border-slate-200 shrink-0 flex items-center gap-1 text-xs font-semibold"
                    aria-label="Cambiar estado"
                    title="Cambiar estado del pedido"
                  >
                    <span className="material-icons" style={{ fontSize: "16px" }}>edit</span>
                    <span>Estado</span>
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* VISTA TABLET/DESKTOP: Tabla completa (>=640px) */}
          <div className="hidden sm:block overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-slate-100 text-slate-700">
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider">N°</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider">Cliente</th>
                  <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider">Total</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider">Estado</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold uppercase tracking-wider">Acción</th>
                </tr>
              </thead>
              <tbody>
                {ultimosPedidos.map((pedido, i) => (
                  <tr key={pedido.id} className={`transition-colors hover:bg-blue-50/40 ${i < ultimosPedidos.length - 1 ? "border-b border-slate-100" : ""}`}>
                    <td className="px-4 py-3.5 font-mono text-xs font-semibold text-slate-700">{pedido.numero}</td>
                    <td className="px-4 py-3.5">
                      <div className="text-sm font-semibold text-slate-900 max-w-[180px] truncate">{pedido.cliente.nombre}</div>
                      <div className="text-xs font-normal text-slate-500 mt-0.5">{pedido.fecha}</div>
                    </td>
                    <td className="px-4 py-3.5 text-right">
                      <span className="text-sm font-bold font-mono text-slate-900">S/{pedido.total.toFixed(2)}</span>
                    </td>
                    <td className="px-4 py-3.5">
                      {editandoId === pedido.id ? (
                        <select
                          value={pedido.estado}
                          onChange={(e) => handleCambioEstado(pedido.id, e.target.value as EstadoPedido)}
                          onBlur={() => setEditandoId(null)}
                          autoFocus
                          className="text-xs font-semibold border-2 border-[#E63946] rounded-xl px-2 py-1.5 focus:outline-none bg-white shadow-md"
                        >
                          {(["Recibido", "Preparación", "Camino", "Entregado", "Cancelado"] as EstadoPedido[]).map((e) => (
                            <option key={e}>{e}</option>
                          ))}
                        </select>
                      ) : (
                        <Badge estado={pedido.estado as EstadoPedido} enRiesgo={estaEnRiesgo(pedido)} />
                      )}
                    </td>
                    <td className="px-4 py-3.5 text-center">
                      <button
                        onClick={() => setEditandoId(editandoId === pedido.id ? null : pedido.id)}
                        className="p-2 rounded-xl bg-slate-100 hover:bg-[#0F223D] hover:text-white text-slate-700 transition-colors border border-slate-200"
                        aria-label="Cambiar estado"
                        title="Cambiar estado del pedido"
                      >
                        <span className="material-icons" style={{ fontSize: "18px" }}>edit</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>

      {/* Floating Action Button (Comfortable placement with high contrast ring) */}
      <button
        onClick={() => navegarA("nuevo-pedido")}
        className="fixed bottom-20 right-4 sm:bottom-8 sm:right-8 bg-[#E63946] hover:bg-[#C62828] active:scale-95 text-white w-14 h-14 sm:w-16 sm:h-16 rounded-full shadow-2xl shadow-red-500/50 flex items-center justify-center transition-all z-30 ring-4 ring-white"
        aria-label="Nuevo pedido"
        title="Crear un nuevo pedido"
      >
        <span className="material-icons text-2xl sm:text-3xl font-bold">add</span>
      </button>
    </div>
  );
}

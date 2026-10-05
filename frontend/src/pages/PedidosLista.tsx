/**
 * @file PedidosLista.tsx
 * @description Historial interactivo de pedidos con filtros por DNI, estado, flete y métodos de pago
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { useState, useMemo, useEffect } from "react";
import { useApp } from "../context/AppContext";
import Badge from "../components/common/Badge";
import ReciboModal from "../components/common/ReciboModal";
import { EstadoPedido, estaEnRiesgo, Pedido } from "../data/mockData";

const ESTADOS: (EstadoPedido | "Todos")[] = ["Todos", "Recibido", "Preparación", "Camino", "Entregado", "Cancelado"];
const POR_PAGINA = 10;

export default function PedidosLista() {
  const { pedidos, actualizarEstadoPedido, filtroInicial, modoAccesible } = useApp();
  const [busqueda, setBusqueda] = useState("");
  const [filtroEstado, setFiltroEstado] = useState<EstadoPedido | "Todos">("Todos");
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [pagina, setPagina] = useState(1);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const [expandidoId, setExpandidoId] = useState<string | null>(null);
  const [pedidoRecibo, setPedidoRecibo] = useState<Pedido | null>(null);

  // Aplica el filtro inicial que viene del dashboard
  useEffect(() => {
    if (filtroInicial !== "Todos") {
      setFiltroEstado(filtroInicial);
    }
  }, [filtroInicial]);

  const filtrados = useMemo(() => {
    return pedidos.filter((p) => {
      const q = busqueda.toLowerCase().trim();
      const matchBusqueda =
        !q ||
        p.cliente.nombre.toLowerCase().includes(q) ||
        p.numero.toLowerCase().includes(q) ||
        p.cliente.telefono.includes(q) ||
        (p.cliente.dniRuc && p.cliente.dniRuc.toLowerCase().includes(q)) ||
        (p.numeroOperacion && p.numeroOperacion.toLowerCase().includes(q)) ||
        (p.numeroGuia && p.numeroGuia.toLowerCase().includes(q)) ||
        (p.ciudadDestino && p.ciudadDestino.toLowerCase().includes(q));
      const matchEstado = filtroEstado === "Todos" || p.estado === filtroEstado;
      const matchDesde = !desde || p.fecha >= desde;
      const matchHasta = !hasta || p.fecha <= hasta;
      return matchBusqueda && matchEstado && matchDesde && matchHasta;
    });
  }, [pedidos, busqueda, filtroEstado, desde, hasta]);

  const enRiesgoCount = useMemo(() => filtrados.filter(estaEnRiesgo).length, [filtrados]);
  const totalPaginas = Math.max(1, Math.ceil(filtrados.length / POR_PAGINA));
  const paginados = filtrados.slice((pagina - 1) * POR_PAGINA, pagina * POR_PAGINA);

  const cambiar = <T,>(setter: (v: T) => void, val: T) => { setter(val); setPagina(1); };

  return (
    <div className={`pt-16 pb-32 sm:pb-28 min-h-screen ${modoAccesible ? "bg-[#E2E8F0]" : "bg-[#F1FAEE]"}`}>
      <div className="max-w-5xl mx-auto px-3 sm:px-6 py-4 sm:py-5">
        <div className="flex flex-wrap items-center justify-between gap-2.5 mb-4">
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900">Historial de Pedidos</h1>
          {enRiesgoCount > 0 && (
            <button
              onClick={() => cambiar(setFiltroEstado, "Recibido")}
              className="flex items-center gap-1.5 bg-red-600 text-white text-xs sm:text-sm font-bold px-3 py-1.5 rounded-full shadow-md animate-pulse"
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>warning</span>
              {enRiesgoCount} en riesgo
            </button>
          )}
        </div>

        {/* Search */}
        <div className="relative mb-3">
          <span className="material-icons absolute left-3.5 sm:left-4 top-1/2 -translate-y-1/2 text-slate-400" style={{ fontSize: "20px" }}>search</span>
          <input
            type="text"
            placeholder="Buscar por cliente, DNI/RUC, teléfono, N° pedido u operación..."
            value={busqueda}
            onChange={(e) => cambiar(setBusqueda, e.target.value)}
            className="w-full pl-11 sm:pl-12 pr-4 py-3 sm:py-3.5 bg-white border-2 border-slate-300 rounded-2xl text-sm sm:text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] shadow-sm"
          />
        </div>

        {/* Filters */}
        <div className="bg-white rounded-3xl p-3.5 sm:p-4 mb-4 shadow-sm border border-slate-200">
          <div className="flex items-center gap-2 mb-3">
            <select
              value={filtroEstado}
              onChange={(e) => cambiar(setFiltroEstado, e.target.value as EstadoPedido | "Todos")}
              className="flex-1 text-sm sm:text-base border-2 border-slate-300 rounded-2xl px-3 sm:px-4 py-2 sm:py-2.5 focus:outline-none focus:border-[#0F223D] bg-slate-50 font-semibold text-slate-900"
            >
              {ESTADOS.map((e) => <option key={e}>{e}</option>)}
            </select>
            <span className="text-xs font-semibold text-slate-700 bg-slate-100 px-2.5 sm:px-3 py-2 sm:py-2.5 rounded-2xl border border-slate-200 whitespace-nowrap">
              {filtrados.length} pedido{filtrados.length !== 1 ? "s" : ""}
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
            <div>
              <label className="block text-[11px] sm:text-xs font-semibold text-slate-600 uppercase tracking-wider mb-1 px-1">Fecha Desde</label>
              <input
                type="date"
                value={desde}
                onChange={(e) => cambiar(setDesde, e.target.value)}
                className="w-full text-xs sm:text-sm font-medium border-2 border-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:border-[#0F223D] bg-slate-50 text-slate-900"
              />
            </div>
            <div>
              <label className="block text-[11px] sm:text-xs font-semibold text-slate-600 uppercase tracking-wider mb-1 px-1">Fecha Hasta</label>
              <input
                type="date"
                value={hasta}
                onChange={(e) => cambiar(setHasta, e.target.value)}
                className="w-full text-xs sm:text-sm font-medium border-2 border-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:border-[#0F223D] bg-slate-50 text-slate-900"
              />
            </div>
          </div>
        </div>

        {/* Table / List */}
        <div className="bg-white rounded-3xl shadow-sm overflow-hidden border border-slate-200 mb-4">
          {paginados.length === 0 ? (
            <div className="py-16 text-center px-4">
              <span className="material-icons text-slate-300 text-5xl sm:text-6xl block mb-3">search_off</span>
              <p className="text-sm sm:text-base font-bold text-slate-700">Sin resultados para esta búsqueda</p>
              {filtroEstado !== "Todos" && (
                <button onClick={() => cambiar(setFiltroEstado, "Todos")} className="mt-3 text-xs sm:text-sm text-[#E63946] font-bold hover:underline bg-red-50 px-4 py-2 rounded-xl border border-red-200">
                  Ver todos los estados
                </button>
              )}
            </div>
          ) : (
            <>
              {paginados.map((pedido, i) => {
                const enRiesgo = estaEnRiesgo(pedido);
                const expandido = expandidoId === pedido.id;
                return (
                  <div key={pedido.id} className={i < paginados.length - 1 ? "border-b border-slate-200" : ""}>
                    {/* Main row */}
                    <div
                      className={`flex items-start sm:items-center gap-2.5 sm:gap-3 px-3.5 sm:px-5 py-3.5 sm:py-4 cursor-pointer transition-colors hover:bg-blue-50/50 ${enRiesgo ? "bg-red-50/70" : ""}`}
                      onClick={() => setExpandidoId(expandido ? null : pedido.id)}
                    >
                      {/* Left: order # + client */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-1.5 sm:gap-2 mb-1 flex-wrap">
                          <span className="font-mono text-xs font-semibold text-slate-700 shrink-0 bg-slate-100 px-2 py-0.5 rounded-lg border border-slate-200">{pedido.numero}</span>
                          <span className="text-sm sm:text-base font-semibold text-slate-900 truncate">{pedido.cliente.nombre}</span>
                          {pedido.tipoEnvio === "Nacional" ? (
                            <span className="text-[10px] font-bold bg-blue-100 text-blue-900 border border-blue-300 px-1.5 sm:px-2 py-0.5 rounded-md flex items-center gap-1">
                              <span className="material-icons" style={{ fontSize: "12px" }}>domain</span>
                              <span>{pedido.agenciaEncomienda || "Encomienda"}{pedido.ciudadDestino ? ` · ${pedido.ciudadDestino}` : ""}</span>
                            </span>
                          ) : (
                            <span className="text-[10px] font-bold bg-slate-100 text-slate-700 border border-slate-200 px-1.5 py-0.5 rounded-md flex items-center gap-0.5">
                              <span className="material-icons" style={{ fontSize: "12px" }}>two_wheeler</span>
                              <span>Lima</span>
                            </span>
                          )}
                          {pedido.metodoPago && (
                            <span className="text-[10px] font-bold bg-purple-100 text-purple-900 border border-purple-200 px-1.5 py-0.5 rounded-md">
                              {pedido.metodoPago}
                            </span>
                          )}
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge estado={pedido.estado} enRiesgo={enRiesgo} />
                          {pedido.cuponAplicado && (
                            <span className="text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 px-1.5 py-0.5 rounded-md">
                              Cupón: {pedido.cuponAplicado}
                            </span>
                          )}
                        </div>
                      </div>
                      {/* Right: total + expand */}
                      <div className="flex flex-col items-end shrink-0 gap-0.5 sm:gap-1">
                        <span className="text-sm sm:text-base font-bold font-mono text-slate-900">S/{pedido.total.toFixed(2)}</span>
                        <span className="text-[11px] sm:text-xs font-normal text-slate-500">{pedido.fecha}</span>
                      </div>
                      <span className="material-icons text-slate-400 transition-transform mt-0.5 sm:mt-0" style={{ fontSize: "20px", transform: expandido ? "rotate(180deg)" : "rotate(0deg)" }}>
                        expand_more
                      </span>
                    </div>

                    {/* Expanded detail */}
                    {expandido && (
                      <div className="bg-slate-50 px-3.5 sm:px-5 py-4 sm:py-5 border-t-2 border-slate-200 space-y-3">
                        {/* Dispatch info if national */}
                        {pedido.tipoEnvio === "Nacional" && (
                          <div className="bg-blue-50 border border-blue-200 rounded-2xl p-3 sm:p-3.5 flex items-center justify-between gap-2">
                            <div>
                              <p className="text-[11px] sm:text-xs font-semibold text-blue-950 uppercase tracking-wider mb-0.5">Envío Nacional por Encomienda</p>
                              <p className="text-xs sm:text-sm font-bold text-blue-900">
                                {pedido.agenciaEncomienda || "Agencia"} · {pedido.ciudadDestino || "Provincia"}
                              </p>
                              {pedido.numeroGuia && (
                                <p className="text-[11px] sm:text-xs text-blue-800 font-mono font-medium mt-0.5">
                                  N° Guía / Clave: <span className="font-bold">{pedido.numeroGuia}</span>
                                </p>
                              )}
                            </div>
                            <span className="material-icons text-blue-700 text-2xl shrink-0">local_shipping</span>
                          </div>
                        )}

                        {/* Customer Info & Document */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
                          <div className="bg-white p-3 sm:p-3.5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
                            <div>
                              <p className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-0.5">Teléfono</p>
                              <p className="text-sm font-bold font-mono text-slate-900">{pedido.cliente.telefono}</p>
                            </div>
                            <a
                              href={`tel:${pedido.cliente.telefono}`}
                              className="flex items-center gap-1 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold px-3 py-1.5 rounded-xl shadow-md"
                              aria-label="Llamar al cliente"
                            >
                              <span className="material-icons" style={{ fontSize: "15px" }}>call</span>
                              Llamar
                            </a>
                          </div>

                          <div className="bg-white p-3 sm:p-3.5 rounded-2xl border border-slate-200 shadow-sm">
                            <p className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-0.5">DNI / RUC Cliente</p>
                            <p className="text-sm font-bold font-mono text-slate-900">
                              {pedido.cliente.dniRuc ? pedido.cliente.dniRuc : <span className="text-slate-400 font-normal italic">No registrado</span>}
                            </p>
                          </div>
                        </div>

                        {/* Address & Reference */}
                        <div className="bg-white p-3 sm:p-3.5 rounded-2xl border border-slate-200 shadow-sm">
                          <p className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-0.5">
                            {pedido.tipoEnvio === "Nacional" ? "Agencia de Destino / Recojo" : "Dirección de Entrega"}
                          </p>
                          <p className="text-xs sm:text-sm font-semibold text-slate-800 leading-relaxed">{pedido.cliente.direccion}</p>
                          {(pedido.cliente.distrito || pedido.cliente.referencia) && (
                            <div className="mt-1.5 pt-1.5 border-t border-slate-100 flex flex-wrap gap-2 text-xs text-slate-600">
                              {pedido.cliente.distrito && (
                                <span><strong>Distrito:</strong> {pedido.cliente.distrito}</span>
                              )}
                              {pedido.cliente.referencia && (
                                <span><strong>Ref:</strong> {pedido.cliente.referencia}</span>
                              )}
                            </div>
                          )}
                        </div>

                        {/* Payment & Channel */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
                          <div className="bg-white p-3 sm:p-3.5 rounded-2xl border border-slate-200 shadow-sm">
                            <span className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">Método de Pago</span>
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold bg-purple-100 text-purple-900 border border-purple-200 px-2.5 py-1 rounded-xl">
                                {pedido.metodoPago || "No especificado"}
                              </span>
                              {pedido.numeroOperacion && (
                                <span className="text-xs font-mono font-semibold text-slate-600">
                                  OP: {pedido.numeroOperacion}
                                </span>
                              )}
                            </div>
                          </div>

                          <div className="bg-white p-3 sm:p-3.5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
                            <span className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider">Canal de Pedido</span>
                            <span className="text-xs font-bold bg-[#0F223D] text-white px-2.5 py-1 rounded-xl">{pedido.canal}</span>
                          </div>
                        </div>

                        {/* Items */}
                        <div className="bg-white p-3.5 sm:p-4 rounded-2xl border border-slate-200 shadow-sm">
                          <p className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Desglose de Prendas</p>
                          <div className="space-y-1.5">
                            {pedido.items.map((item) => (
                              <div key={item.productoId} className="flex items-center justify-between text-xs sm:text-sm">
                                <span className="text-slate-800 font-medium">{item.nombre} × {item.cantidad}</span>
                                <span className="font-bold font-mono text-slate-900">S/{(item.cantidad * item.precio).toFixed(2)}</span>
                              </div>
                            ))}
                          </div>
                          {pedido.costoDelivery > 0 && (
                            <div className="flex items-center justify-between text-xs sm:text-sm mt-2 text-slate-600 font-medium">
                              <span>Delivery</span>
                              <span className="font-mono font-medium text-slate-900">S/{pedido.costoDelivery.toFixed(2)}</span>
                            </div>
                          )}
                          {pedido.descuento > 0 && (
                            <div className="flex items-center justify-between text-xs sm:text-sm mt-1 text-emerald-700 font-medium">
                              <span>Descuento {pedido.cuponAplicado ? `(${pedido.cuponAplicado})` : ""}</span>
                              <span className="font-mono font-semibold">-S/{pedido.descuento.toFixed(2)}</span>
                            </div>
                          )}
                          <div className="flex items-center justify-between mt-3 pt-3 border-t-2 border-slate-200">
                            <span className="text-sm sm:text-base font-bold text-slate-900">Total</span>
                            <span className="text-lg sm:text-xl font-bold font-mono text-[#E63946]">S/{pedido.total.toFixed(2)}</span>
                          </div>
                        </div>

                        {/* Notas */}
                        {pedido.notas && (
                          <div className="bg-amber-50 border border-amber-300 rounded-2xl p-3 sm:p-3.5">
                            <p className="text-[11px] sm:text-xs font-semibold text-amber-950 uppercase tracking-wider mb-0.5">Notas Especiales</p>
                            <p className="text-xs sm:text-sm font-normal text-amber-900 leading-relaxed">{pedido.notas}</p>
                          </div>
                        )}
                        {/* Botones de Recibo PDF y Rótulo */}
                        <div className="pt-2 border-t border-slate-200 grid grid-cols-1 sm:grid-cols-2 gap-2">
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              setPedidoRecibo(pedido);
                            }}
                            className="flex items-center justify-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs sm:text-sm font-bold px-3.5 py-2.5 rounded-2xl shadow-sm transition-all"
                          >
                            <span className="material-icons" style={{ fontSize: "16px" }}>receipt_long</span>
                            <span>Ver Recibo / Imprimir PDF</span>
                          </button>

                          {pedido.tipoEnvio === "Nacional" ? (
                            <button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                setPedidoRecibo(pedido);
                              }}
                              className="flex items-center justify-center gap-1.5 bg-blue-700 hover:bg-blue-800 text-white text-xs sm:text-sm font-bold px-3.5 py-2.5 rounded-2xl shadow-sm transition-all"
                            >
                              <span className="material-icons" style={{ fontSize: "16px" }}>local_shipping</span>
                              <span>Rótulo Encomienda ({pedido.agenciaEncomienda || "Shalom"})</span>
                            </button>
                          ) : (
                            <a
                              href={`https://wa.me/51${pedido.cliente.telefono.replace(/\D/g, "")}?text=${encodeURIComponent(`Hola ${pedido.cliente.nombre}, te enviamos la confirmación de tu pedido ${pedido.numero} de LeoFit. Puedes rastrearlo aquí: https://leofit.com/rastreo?codigo=${pedido.numero}`)}`}
                              target="_blank"
                              rel="noreferrer"
                              onClick={(e) => e.stopPropagation()}
                              className="flex items-center justify-center gap-1.5 bg-emerald-700 hover:bg-emerald-800 text-white text-xs sm:text-sm font-bold px-3.5 py-2.5 rounded-2xl shadow-sm transition-all"
                            >
                              <span className="material-icons" style={{ fontSize: "16px" }}>chat</span>
                              <span>Enviar Resumen WhatsApp</span>
                            </a>
                          )}
                        </div>

                        {/* Status change */}
                        {pedido.estado !== "Entregado" && pedido.estado !== "Cancelado" && (
                          <div className="pt-2">
                            <p className="text-[11px] sm:text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">Cambiar Estado del Pedido</p>
                            {editandoId === pedido.id ? (
                              <select
                                value={pedido.estado}
                                onChange={(e) => { actualizarEstadoPedido(pedido.id, e.target.value as EstadoPedido); setEditandoId(null); }}
                                onBlur={() => setEditandoId(null)}
                                autoFocus
                                className="w-full text-xs sm:text-sm font-semibold border-2 border-[#E63946] rounded-2xl px-3 sm:px-4 py-2.5 sm:py-3 focus:outline-none bg-white shadow-md"
                              >
                                {((["Recibido", "Preparación", "Camino", "Entregado", "Cancelado"] as EstadoPedido[])).map((e) => (
                                  <option key={e}>{e}</option>
                                ))}
                              </select>
                            ) : (
                              <button
                                onClick={() => setEditandoId(pedido.id)}
                                className="flex items-center gap-2 bg-[#0F223D] text-white text-sm sm:text-base font-bold px-4 py-2.5 sm:py-3 rounded-2xl hover:bg-[#1D3557] transition-colors w-full justify-center shadow-md"
                              >
                                <span className="material-icons" style={{ fontSize: "18px" }}>edit</span>
                                Modificar Estado
                              </button>
                            )}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </>
          )}
        </div>

        {/* Pagination */}
        {totalPaginas > 1 && (
          <div className="flex items-center justify-center gap-1.5 sm:gap-2 flex-wrap">
            <button onClick={() => setPagina((p) => Math.max(1, p - 1))} disabled={pagina === 1}
              className="p-2.5 sm:p-3 rounded-2xl bg-white border border-slate-300 hover:bg-slate-100 disabled:opacity-30 transition-colors shadow-sm">
              <span className="material-icons text-slate-700 text-lg">chevron_left</span>
            </button>
            {Array.from({ length: totalPaginas }, (_, i) => i + 1).map((n) => (
              <button key={n} onClick={() => setPagina(n)}
                className={`w-9 h-9 sm:w-11 sm:h-11 rounded-2xl text-xs sm:text-base font-bold transition-all ${n === pagina ? "bg-[#E63946] text-white shadow-md shadow-red-500/30 ring-2 ring-white" : "bg-white border border-slate-300 hover:bg-slate-100 text-slate-800"}`}>
                {n}
              </button>
            ))}
            <button onClick={() => setPagina((p) => Math.min(totalPaginas, p + 1))} disabled={pagina === totalPaginas}
              className="p-2.5 sm:p-3 rounded-2xl bg-white border border-slate-300 hover:bg-slate-100 disabled:opacity-30 transition-colors shadow-sm">
              <span className="material-icons text-slate-700 text-lg">chevron_right</span>
            </button>
          </div>
        )}

        {/* Modal de Recibo / Rótulo de Encomienda */}
        {pedidoRecibo && (
          <ReciboModal
            pedido={pedidoRecibo}
            onClose={() => setPedidoRecibo(null)}
          />
        )}

      </div>
    </div>
  );
}

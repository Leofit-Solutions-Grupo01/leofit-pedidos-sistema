import { useState, useMemo, useEffect } from "react";
import { useApp } from "../context/AppContext";
import Badge from "../components/common/Badge";
import MontoPrivado from "../components/common/MontoPrivado";
import { EstadoPedido, estaEnRiesgo } from "../data/mockData";

const ESTADOS: (EstadoPedido | "Todos")[] = ["Todos", "Recibido", "Preparación", "Camino", "Entregado", "Cancelado"];
const POR_PAGINA = 10;

export default function PedidosLista() {
  const { pedidos, actualizarEstadoPedido, filtroInicial, privacidad } = useApp();
  const [busqueda, setBusqueda] = useState("");
  const [filtroEstado, setFiltroEstado] = useState<EstadoPedido | "Todos">("Todos");
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [pagina, setPagina] = useState(1);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const [expandidoId, setExpandidoId] = useState<string | null>(null);

  // Aplica el filtro inicial que viene del dashboard (click en KPI)
  useEffect(() => {
    if (filtroInicial !== "Todos") {
      setFiltroEstado(filtroInicial);
    }
  }, [filtroInicial]);

  const filtrados = useMemo(() => {
    return pedidos.filter((p) => {
      const matchBusqueda =
        p.cliente.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
        p.numero.toLowerCase().includes(busqueda.toLowerCase()) ||
        p.cliente.telefono.includes(busqueda);
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
    <div className="pt-14 pb-24 min-h-screen bg-[#F1FAEE]">
      <div className="max-w-2xl mx-auto px-4 py-5">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-black text-[#1D3557]">Historial</h1>
          {enRiesgoCount > 0 && (
            <button
              onClick={() => cambiar(setFiltroEstado, "Recibido")}
              className="flex items-center gap-1.5 bg-[#E63946]/10 border border-[#E63946]/20 text-[#E63946] text-xs font-bold px-3 py-1.5 rounded-full"
            >
              <span className="material-icons" style={{ fontSize: "14px" }}>warning</span>
              {enRiesgoCount} en riesgo
            </button>
          )}
        </div>

        {/* Search */}
        <div className="relative mb-3">
          <span className="material-icons absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-300" style={{ fontSize: "20px" }}>search</span>
          <input
            type="text"
            placeholder="Buscar por nombre, teléfono o N° pedido..."
            value={busqueda}
            onChange={(e) => cambiar(setBusqueda, e.target.value)}
            className="w-full pl-11 pr-4 py-3 bg-white border-2 border-gray-100 rounded-2xl text-sm focus:outline-none focus:border-[#E63946] focus:ring-4 focus:ring-[#E63946]/10 transition-all placeholder-gray-300"
          />
        </div>

        {/* Filters */}
        <div className="bg-white rounded-2xl p-3 mb-4 shadow-sm border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <select
              value={filtroEstado}
              onChange={(e) => cambiar(setFiltroEstado, e.target.value as EstadoPedido | "Todos")}
              className="flex-1 text-sm border-2 border-gray-100 rounded-xl px-3 py-2 focus:outline-none focus:border-[#E63946] bg-[#F1FAEE] font-medium text-[#1D3557]"
            >
              {ESTADOS.map((e) => <option key={e}>{e}</option>)}
            </select>
            <span className="text-xs text-gray-400 font-semibold px-2 whitespace-nowrap">
              {filtrados.length} resultado{filtrados.length !== 1 ? "s" : ""}
            </span>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1 px-1">Desde</label>
              <input type="date" value={desde} onChange={(e) => cambiar(setDesde, e.target.value)}
                className="w-full text-sm border-2 border-gray-100 rounded-xl px-3 py-2 focus:outline-none focus:border-[#E63946] bg-[#F1FAEE]" />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1 px-1">Hasta</label>
              <input type="date" value={hasta} onChange={(e) => cambiar(setHasta, e.target.value)}
                className="w-full text-sm border-2 border-gray-100 rounded-xl px-3 py-2 focus:outline-none focus:border-[#E63946] bg-[#F1FAEE]" />
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="bg-white rounded-2xl shadow-sm overflow-hidden border border-gray-100 mb-4">
          {paginados.length === 0 ? (
            <div className="py-16 text-center">
              <span className="material-icons text-gray-200 text-6xl block mb-3">search_off</span>
              <p className="text-sm text-gray-400 font-medium">Sin resultados para esta búsqueda</p>
              {filtroEstado !== "Todos" && (
                <button onClick={() => cambiar(setFiltroEstado, "Todos")} className="mt-2 text-xs text-[#E63946] font-semibold hover:underline">
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
                  <div key={pedido.id} className={i < paginados.length - 1 ? "border-b border-gray-50" : ""}>
                    {/* Main row */}
                    <div
                      className={`flex items-center gap-2 px-4 py-3 cursor-pointer transition-colors hover:bg-[#F1FAEE]/60 ${enRiesgo ? "bg-[#E63946]/3" : ""}`}
                      onClick={() => setExpandidoId(expandido ? null : pedido.id)}
                    >
                      {/* Left: order # + client */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-0.5">
                          <span className="font-mono text-xs font-bold text-gray-400 shrink-0">{pedido.numero}</span>
                          <span className="text-sm font-semibold text-[#1A1A1A] truncate">{pedido.cliente.nombre}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge estado={pedido.estado} enRiesgo={enRiesgo} />
                        </div>
                      </div>
                      {/* Right: total + expand */}
                      <div className="flex flex-col items-end shrink-0 gap-1">
                        <MontoPrivado valor={pedido.total} privacidad={privacidad} className="text-sm font-black text-[#1D3557]" />
                        <span className="text-[10px] text-gray-400 font-mono">{pedido.fecha}</span>
                      </div>
                      <span className="material-icons text-gray-300 transition-transform" style={{ fontSize: "18px", transform: expandido ? "rotate(180deg)" : "rotate(0deg)" }}>
                        expand_more
                      </span>
                    </div>

                    {/* Expanded detail */}
                    {expandido && (
                      <div className="bg-[#F1FAEE] px-4 py-4 border-t border-gray-100 space-y-3">
                        {/* Contact */}
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Teléfono</p>
                            <p className="text-sm font-semibold text-[#1A1A1A]">{pedido.cliente.telefono}</p>
                          </div>
                          <a
                            href={`tel:${pedido.cliente.telefono}`}
                            className="flex items-center gap-1.5 bg-[#27AE60] text-white text-xs font-bold px-3 py-2 rounded-xl"
                            aria-label="Llamar al cliente"
                          >
                            <span className="material-icons" style={{ fontSize: "16px" }}>call</span>
                            Llamar
                          </a>
                        </div>
                        <div>
                          <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Dirección</p>
                          <p className="text-sm text-[#1A1A1A]">{pedido.cliente.direccion}</p>
                        </div>
                        {/* Canal */}
                        <div>
                          <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Canal</p>
                          <span className="text-xs font-semibold bg-[#1D3557]/10 text-[#1D3557] px-2 py-0.5 rounded-full">{pedido.canal}</span>
                        </div>
                        {/* Items */}
                        <div>
                          <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Productos</p>
                          <div className="space-y-1">
                            {pedido.items.map((item) => (
                              <div key={item.productoId} className="flex items-center justify-between text-sm">
                                <span className="text-[#1A1A1A] font-medium">{item.nombre} ×{item.cantidad}</span>
                                <MontoPrivado valor={item.cantidad * item.precio} privacidad={privacidad} className="font-bold text-[#1D3557]" />
                              </div>
                            ))}
                          </div>
                          {pedido.costoDelivery > 0 && (
                            <div className="flex items-center justify-between text-sm mt-1 text-gray-400">
                              <span>Delivery</span>
                              <MontoPrivado valor={pedido.costoDelivery} privacidad={privacidad} />
                            </div>
                          )}
                          {pedido.descuento > 0 && (
                            <div className="flex items-center justify-between text-sm mt-1 text-[#27AE60]">
                              <span>Descuento</span>
                              <span>-<MontoPrivado valor={pedido.descuento} privacidad={privacidad} /></span>
                            </div>
                          )}
                          <div className="flex items-center justify-between mt-2 pt-2 border-t border-gray-200">
                            <span className="text-sm font-bold text-[#1D3557]">Total</span>
                            <MontoPrivado valor={pedido.total} privacidad={privacidad} className="text-lg font-black text-[#E63946]" />
                          </div>
                        </div>
                        {/* Notas */}
                        {pedido.notas && (
                          <div className="bg-yellow-50 border border-yellow-200 rounded-xl px-3 py-2">
                            <p className="text-[10px] font-bold text-yellow-700 uppercase tracking-wider mb-0.5">Notas</p>
                            <p className="text-xs text-yellow-800">{pedido.notas}</p>
                          </div>
                        )}
                        {/* Fecha entrega */}
                        {pedido.fechaEntrega && (
                          <div>
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Entregado el</p>
                            <p className="text-xs font-semibold text-[#27AE60]">
                              {new Date(pedido.fechaEntrega).toLocaleString("es-PE")}
                            </p>
                          </div>
                        )}
                        {/* Status change */}
                        {pedido.estado !== "Entregado" && pedido.estado !== "Cancelado" && (
                          <div>
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Actualizar estado</p>
                            {editandoId === pedido.id ? (
                              <select
                                value={pedido.estado}
                                onChange={(e) => { actualizarEstadoPedido(pedido.id, e.target.value as EstadoPedido); setEditandoId(null); }}
                                onBlur={() => setEditandoId(null)}
                                autoFocus
                                className="w-full text-sm border-2 border-[#E63946] rounded-xl px-3 py-2 focus:outline-none bg-white"
                              >
                                {(["Recibido", "Preparación", "Camino", "Entregado", "Cancelado"] as EstadoPedido[]).map((e) => (
                                  <option key={e}>{e}</option>
                                ))}
                              </select>
                            ) : (
                              <button
                                onClick={() => setEditandoId(pedido.id)}
                                className="flex items-center gap-2 bg-[#1D3557] text-white text-sm font-bold px-4 py-2.5 rounded-xl hover:bg-[#1D3557]/80 transition-colors w-full justify-center"
                              >
                                <span className="material-icons" style={{ fontSize: "16px" }}>edit</span>
                                Cambiar estado
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
          <div className="flex items-center justify-center gap-1.5">
            <button onClick={() => setPagina((p) => Math.max(1, p - 1))} disabled={pagina === 1}
              className="p-2 rounded-xl hover:bg-white disabled:opacity-30 transition-colors">
              <span className="material-icons text-[#1D3557]">chevron_left</span>
            </button>
            {Array.from({ length: totalPaginas }, (_, i) => i + 1).map((n) => (
              <button key={n} onClick={() => setPagina(n)}
                className={`w-9 h-9 rounded-xl text-sm font-bold transition-all ${n === pagina ? "bg-[#E63946] text-white shadow-md shadow-[#E63946]/30" : "hover:bg-white text-gray-500"}`}>
                {n}
              </button>
            ))}
            <button onClick={() => setPagina((p) => Math.min(totalPaginas, p + 1))} disabled={pagina === totalPaginas}
              className="p-2 rounded-xl hover:bg-white disabled:opacity-30 transition-colors">
              <span className="material-icons text-[#1D3557]">chevron_right</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

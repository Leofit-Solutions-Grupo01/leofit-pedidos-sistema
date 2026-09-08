import { useState } from "react";
import { useApp } from "../context/AppContext";
import Badge from "../components/common/Badge";
import { Pedido, estaEnRiesgo } from "../data/mockData";

const PASOS_ESTADO = [
  { estado: "Recibido", label: "Pedido Recibido", desc: "Registrado en el sistema", icon: "receipt_long" },
  { estado: "Preparación", label: "En Preparación", desc: "Selección de prendas y embalaje", icon: "inventory_2" },
  { estado: "Camino", label: "En Despacho / Ruta", desc: "En camino a tu dirección o agencia", icon: "local_shipping" },
  { estado: "Entregado", label: "Entregado con Éxito", desc: "Entrega confirmada", icon: "check_circle" },
];

export default function RastreoPublico() {
  const { pedidos, modoAccesible } = useApp();
  const [codigoBusqueda, setCodigoBusqueda] = useState("LFT-004");
  const [pedidoEncontrado, setPedidoEncontrado] = useState<Pedido | null>(() => {
    return pedidos.find((p) => p.numero === "LFT-004") || pedidos[0] || null;
  });
  const [errorBusqueda, setErrorBusqueda] = useState("");

  const handleBuscar = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorBusqueda("");
    const query = codigoBusqueda.trim().toUpperCase();
    if (!query) {
      setErrorBusqueda("Ingresa un número de pedido o teléfono.");
      return;
    }

    const encontrado = pedidos.find(
      (p) =>
        p.numero.toUpperCase() === query ||
        p.cliente.telefono === query ||
        p.numero.replace("-", "").toUpperCase() === query.replace("-", "")
    );

    if (encontrado) {
      setPedidoEncontrado(encontrado);
    } else {
      setErrorBusqueda(`No se encontró ningún pedido con el código o teléfono "${codigoBusqueda}".`);
    }
  };

  const calcularIndicePaso = (estado: string) => {
    switch (estado) {
      case "Recibido": return 0;
      case "Preparación": return 1;
      case "Camino": return 2;
      case "Entregado": return 3;
      default: return 0;
    }
  };

  const indiceActual = pedidoEncontrado ? calcularIndicePaso(pedidoEncontrado.estado) : 0;
  const esCancelado = pedidoEncontrado?.estado === "Cancelado";

  return (
    <div className={`pt-16 pb-32 sm:pb-28 min-h-screen ${modoAccesible ? "bg-[#E2E8F0]" : "bg-[#F1FAEE]"}`}>
      <div className="max-w-5xl mx-auto px-3 sm:px-6 py-4 sm:py-5 space-y-4 sm:space-y-5">

        {/* Hero de Rastreo */}
        <div className="bg-[#0F223D] rounded-3xl p-5 sm:p-6 text-white text-center shadow-xl border border-slate-700">
          <div className="inline-flex items-center justify-center w-11 h-11 sm:w-12 sm:h-12 rounded-2xl bg-gradient-to-br from-[#E63946] to-[#C62828] mb-3 shadow-md">
            <span className="material-icons text-white text-xl sm:text-2xl">track_changes</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white mb-1">Rastreo de Envíos en Vivo</h1>
          <p className="text-slate-300 text-xs sm:text-sm font-normal max-w-md mx-auto leading-relaxed">
            Ingresa tu código <strong className="text-amber-400 font-mono">LFT-XXX</strong> o tu número de teléfono para conocer el estado de tu entrega.
          </p>

          {/* Formulario de Búsqueda */}
          <form onSubmit={handleBuscar} className="mt-4 sm:mt-5 flex flex-col sm:flex-row gap-2 max-w-md mx-auto">
            <input
              type="text"
              value={codigoBusqueda}
              onChange={(e) => setCodigoBusqueda(e.target.value)}
              placeholder="ej. LFT-004 o 934567890"
              className="flex-1 px-4 py-3 bg-white text-slate-900 placeholder-slate-400 rounded-2xl text-sm sm:text-base font-semibold focus:outline-none focus:ring-4 focus:ring-red-500/40 shadow-inner"
            />
            <button
              type="submit"
              className="px-5 sm:px-6 py-3 bg-[#E63946] hover:bg-[#C62828] active:scale-95 text-white font-bold rounded-2xl transition-all flex items-center justify-center gap-1.5 shadow-md shadow-red-500/30 shrink-0 text-sm sm:text-base"
            >
              <span className="material-icons" style={{ fontSize: "18px" }}>search</span>
              <span>Rastrear</span>
            </button>
          </form>

          {/* Atajos Rápidos de Demostración */}
          <div className="mt-3.5 flex items-center justify-center gap-1.5 sm:gap-2 flex-wrap">
            <span className="text-[11px] sm:text-xs text-slate-400 font-medium">Ejemplos:</span>
            {[
              { cod: "LFT-004", label: "Shalom Trujillo" },
              { cod: "LFT-003", label: "Lima Directo" },
              { cod: "LFT-006", label: "Olva Arequipa" },
            ].map((ej) => (
              <button
                key={ej.cod}
                type="button"
                onClick={() => {
                  setCodigoBusqueda(ej.cod);
                  const p = pedidos.find((item) => item.numero === ej.cod);
                  if (p) setPedidoEncontrado(p);
                }}
                className="text-[11px] sm:text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white px-2.5 py-1 rounded-xl border border-slate-700 transition-colors font-mono"
              >
                {ej.cod} · {ej.label}
              </button>
            ))}
          </div>
        </div>

        {/* Error si no se encuentra */}
        {errorBusqueda && (
          <div className="bg-red-100 border-2 border-red-300 rounded-2xl p-3.5 sm:p-4 flex items-center gap-2.5 text-red-950">
            <span className="material-icons text-red-700" style={{ fontSize: "22px" }}>error_outline</span>
            <p className="text-xs sm:text-sm font-semibold">{errorBusqueda}</p>
          </div>
        )}

        {/* Detalle del Pedido Encontrado */}
        {pedidoEncontrado && (
          <div className="space-y-4">
            
            {/* Tarjeta de Resumen y Estado */}
            <div className="bg-white rounded-3xl p-4 sm:p-6 shadow-sm border border-slate-200">
              <div className="flex flex-wrap items-start justify-between gap-3 pb-4 border-b border-slate-100 mb-4 sm:mb-5">
                <div>
                  <div className="flex items-center gap-1.5 sm:gap-2 mb-1 flex-wrap">
                    <span className="text-xs sm:text-sm font-mono font-bold text-slate-700 bg-slate-100 px-2 sm:px-2.5 py-0.5 rounded-lg border border-slate-200">
                      {pedidoEncontrado.numero}
                    </span>
                    <span className="text-[11px] sm:text-xs font-semibold px-2 sm:px-2.5 py-0.5 rounded-lg bg-blue-100 text-blue-900 border border-blue-200">
                      {pedidoEncontrado.tipoEnvio === "Nacional" ? "Envío Nacional (Provincia)" : "Envío Local (Lima Capital)"}
                    </span>
                  </div>
                  <h2 className="text-lg sm:text-xl font-bold text-slate-900">{pedidoEncontrado.cliente.nombre}</h2>
                  <p className="text-xs text-slate-500 font-normal mt-0.5">Fecha de Compra: {pedidoEncontrado.fecha}</p>
                </div>
                <div>
                  <Badge estado={pedidoEncontrado.estado} enRiesgo={estaEnRiesgo(pedidoEncontrado)} />
                </div>
              </div>

              {/* Timeline de Envíos */}
              {esCancelado ? (
                <div className="bg-slate-100 border border-slate-300 rounded-2xl p-4 text-center">
                  <span className="material-icons text-slate-500 text-4xl block mb-1">cancel</span>
                  <p className="text-sm sm:text-base font-bold text-slate-800">Este pedido fue cancelado</p>
                  <p className="text-xs text-slate-500 font-normal mt-1">Comunícate con soporte si tienes alguna duda.</p>
                </div>
              ) : (
                <div className="relative pl-6 sm:pl-8 space-y-5 sm:space-y-6 my-2">
                  {/* Línea vertical de conexión */}
                  <div className="absolute left-2.5 sm:left-3.5 top-3 bottom-3 w-0.5 bg-slate-200" />

                  {PASOS_ESTADO.map((paso, index) => {
                    const completado = index < indiceActual;
                    const esActual = index === indiceActual;

                    return (
                      <div key={paso.estado} className="relative flex items-start gap-3 sm:gap-4">
                        {/* Nodo del timeline */}
                        <div
                          className={`absolute -left-6 sm:-left-8 w-6 sm:w-8 h-6 sm:h-8 rounded-full flex items-center justify-center border-2 transition-all ${
                            completado
                              ? "bg-emerald-600 border-emerald-600 text-white shadow-sm"
                              : esActual
                              ? "bg-[#E63946] border-[#E63946] text-white ring-4 ring-red-100 shadow-md animate-pulse"
                              : "bg-white border-slate-300 text-slate-400"
                          }`}
                        >
                          <span className="material-icons" style={{ fontSize: "14px" }}>
                            {completado ? "check" : paso.icon}
                          </span>
                        </div>

                        {/* Contenido del paso */}
                        <div className="flex-1 pt-0.5">
                          <div className="flex items-center gap-1.5 sm:gap-2 flex-wrap">
                            <p className={`text-sm sm:text-base font-bold ${esActual ? "text-slate-950 font-extrabold" : completado ? "text-slate-800" : "text-slate-400"}`}>
                              {paso.label}
                            </p>
                            {esActual && (
                              <span className="text-[10px] uppercase font-bold tracking-wider bg-red-100 text-red-700 px-2 py-0.5 rounded-full border border-red-200">
                                Estado Actual
                              </span>
                            )}
                          </div>
                          <p className={`text-xs ${esActual ? "text-slate-700 font-medium" : "text-slate-500 font-normal"} mt-0.5`}>
                            {paso.desc}
                          </p>

                          {/* Si está en camino y es Provincia o Lima, mostrar detalles del transportista */}
                          {paso.estado === "Camino" && (esActual || completado) && (
                            <div className="mt-2.5 bg-slate-50 border border-slate-200 rounded-2xl p-3 sm:p-3.5 space-y-2">
                              {pedidoEncontrado.tipoEnvio === "Nacional" ? (
                                <>
                                  <div className="flex items-center justify-between text-xs font-semibold text-slate-800 gap-2">
                                    <span className="flex items-center gap-1.5 text-blue-900">
                                      <span className="material-icons text-blue-700" style={{ fontSize: "16px" }}>domain</span>
                                      Empresa:
                                    </span>
                                    <span className="bg-[#0F223D] text-white px-2 py-0.5 rounded-lg font-bold">
                                      {pedidoEncontrado.agenciaEncomienda || "Shalom"}
                                    </span>
                                  </div>
                                  <div className="flex items-center justify-between text-xs text-slate-700 gap-2">
                                    <span className="font-medium">N° Guía:</span>
                                    <span className="font-mono font-bold text-slate-900 bg-white px-2 py-0.5 rounded border border-slate-300">
                                      {pedidoEncontrado.numeroGuia || "SH-990123"}
                                    </span>
                                  </div>
                                  <div className="text-xs text-slate-600">
                                    <span className="font-medium">Destino:</span> {pedidoEncontrado.ciudadDestino || "Provincia"}
                                  </div>
                                </>
                              ) : (
                                <div className="flex items-center justify-between text-xs">
                                  <div className="flex items-center gap-1.5 text-slate-900 font-semibold">
                                    <span className="material-icons text-emerald-700" style={{ fontSize: "16px" }}>two_wheeler</span>
                                    <span>Reparto Directo en Lima Capital (Víctor / Motorizado)</span>
                                  </div>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Dirección de Entrega y Contacto */}
            <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-sm border border-slate-200">
              <h3 className="text-xs sm:text-sm font-bold text-slate-900 uppercase tracking-wider mb-2.5 flex items-center gap-2">
                <span className="material-icons text-slate-600" style={{ fontSize: "18px" }}>place</span>
                Destino y Entrega
              </h3>
              <div className="space-y-2 text-xs sm:text-sm">
                <div>
                  <span className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider block">Dirección / Agencia:</span>
                  <p className="font-medium text-slate-800">{pedidoEncontrado.cliente.direccion}</p>
                </div>
                {pedidoEncontrado.notas && (
                  <div className="bg-amber-50 border border-amber-200 rounded-xl p-2.5 sm:p-3 text-xs text-amber-900 font-medium mt-2">
                    <strong>Nota de Entrega:</strong> {pedidoEncontrado.notas}
                  </div>
                )}
              </div>
            </div>

            {/* Desglose de Prendas */}
            <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-sm border border-slate-200">
              <h3 className="text-xs sm:text-sm font-bold text-slate-900 uppercase tracking-wider mb-2.5 flex items-center gap-2">
                <span className="material-icons text-slate-600" style={{ fontSize: "18px" }}>checkroom</span>
                Prendas en tu Pedido
              </h3>
              <div className="space-y-2">
                {pedidoEncontrado.items.map((item) => (
                  <div key={item.productoId} className="flex items-center justify-between text-xs sm:text-sm py-1 border-b border-slate-100 last:border-none">
                    <span className="text-slate-800 font-medium">{item.nombre} × {item.cantidad}</span>
                    <span className="font-mono font-bold text-slate-900">S/{(item.cantidad * item.precio).toFixed(2)}</span>
                  </div>
                ))}
                <div className="pt-2 flex items-center justify-between font-bold text-sm sm:text-base text-slate-950">
                  <span>Total Pagado / a Cobrar</span>
                  <span className="font-mono text-lg sm:text-xl text-[#E63946]">S/{pedidoEncontrado.total.toFixed(2)}</span>
                </div>
              </div>
            </div>

            {/* Botón de Ayuda por WhatsApp */}
            <div className="bg-emerald-50 border border-emerald-200 rounded-3xl p-4 sm:p-5 text-center shadow-sm">
              <p className="text-xs sm:text-sm font-bold text-emerald-950 mb-1">¿Tienes dudas o necesitas reprogramar la entrega?</p>
              <p className="text-[11px] sm:text-xs text-emerald-800 font-normal mb-3">Víctor y el equipo de atención están listos para ayudarte.</p>
              <a
                href={`https://wa.me/51987654321?text=${encodeURIComponent(`Hola LeoFit, deseo consultar sobre mi pedido ${pedidoEncontrado.numero}`)}`}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-4 sm:px-5 py-2.5 sm:py-3 rounded-2xl text-xs sm:text-sm transition-all shadow-md shadow-emerald-700/20"
              >
                <span className="material-icons" style={{ fontSize: "18px" }}>chat</span>
                Consultar por WhatsApp
              </a>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}

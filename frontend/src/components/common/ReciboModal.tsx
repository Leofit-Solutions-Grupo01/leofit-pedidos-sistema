/**
 * @file ReciboModal.tsx
 * @description Modal interactivo para visualización, descarga en PDF e impresión de Recibos Digitales y Rótulos de Encomienda
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { useState } from "react";
import { Pedido } from "../../data/mockData";

interface ReciboModalProps {
  pedido: Pedido | null;
  onClose: () => void;
}

export default function ReciboModal({ pedido, onClose }: ReciboModalProps) {
  const [vista, setVista] = useState<"recibo" | "rotulo">("recibo");

  if (!pedido) return null;

  const handlePrint = () => {
    window.print();
  };

  const whatsappText = encodeURIComponent(
    `*COMPROBANTE DE PEDIDO LEOFIT - ${pedido.numero}*\n` +
    `*Cliente:* ${pedido.cliente.nombre}\n` +
    `*DNI/RUC:* ${pedido.cliente.dniRuc || "No registrado"}\n` +
    `*Destino:* ${pedido.tipoEnvio === "Nacional" ? `${pedido.agenciaEncomienda} (${pedido.ciudadDestino})` : "Lima Metropolitana"}\n` +
    `*Pago:* ${pedido.metodoPago || "Efectivo"} ${pedido.numeroOperacion ? `(OP: ${pedido.numeroOperacion})` : ""}\n` +
    `*Total:* S/${pedido.total.toFixed(2)}\n\n` +
    `*Rastrea tu pedido en vivo aquí:* https://leofit.com/rastreo?codigo=${pedido.numero}\n` +
    `_Gracias por confiar en LeoFit Indumentaria._`
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/80 backdrop-blur-sm overflow-y-auto">
      {/* Contenedor del Modal */}
      <div className="bg-white rounded-3xl shadow-2xl max-w-lg w-full overflow-hidden border border-slate-200 my-auto animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header de la Modal con pestañas de cambio (No se imprime) */}
        <div className="p-4 bg-[#0F223D] text-white flex items-center justify-between gap-2 print:hidden">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setVista("recibo")}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1 ${
                vista === "recibo"
                  ? "bg-[#E63946] text-white shadow-md"
                  : "bg-slate-800 text-slate-300 hover:text-white"
              }`}
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>receipt</span>
              <span>Recibo Digital</span>
            </button>
            <button
              onClick={() => setVista("rotulo")}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1 ${
                vista === "rotulo"
                  ? "bg-[#E63946] text-white shadow-md"
                  : "bg-slate-800 text-slate-300 hover:text-white"
              }`}
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>local_shipping</span>
              <span>Rótulo Encomienda</span>
            </button>
          </div>

          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center transition-colors"
            aria-label="Cerrar recibo"
          >
            <span className="material-icons" style={{ fontSize: "18px" }}>close</span>
          </button>
        </div>

        {/* ================================================================= */}
        {/* VISTA 1: RECIBO / NOTA DE VENTA DIGITAL */}
        {/* ================================================================= */}
        {vista === "recibo" && (
          <div className="p-5 sm:p-6 bg-slate-50 overflow-y-auto max-h-[75vh] print:max-h-none print:bg-white print:p-0">
            {/* Tarjeta del Recibo con estética de voucher premium */}
            <div className="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-sm relative print:border-none print:shadow-none">
              
              {/* Encabezado con Logo y Datos de la Empresa */}
              <div className="text-center pb-4 border-b border-dashed border-slate-300">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-br from-[#E63946] to-[#C62828] text-white font-extrabold text-xl shadow-md mb-2">
                  LF
                </div>
                <h2 className="text-xl font-extrabold text-slate-900 tracking-tight">LEOFIT INDUMENTARIA</h2>
                <p className="text-xs text-slate-500 font-medium">Ropa & Accesorios Deportivos de Alto Rendimiento</p>
                <p className="text-[11px] text-slate-400">Lima, Perú · Atención WhatsApp: 987 654 321</p>
                <div className="mt-2 inline-block bg-slate-100 text-slate-800 border border-slate-300 px-3 py-1 rounded-full text-xs font-mono font-bold">
                  COMPROBANTE DE PEDIDO: {pedido.numero}
                </div>
              </div>

              {/* Información del Cliente y Despacho */}
              <div className="py-3.5 border-b border-dashed border-slate-300 text-xs space-y-1.5 text-slate-700">
                <div className="flex justify-between">
                  <span className="text-slate-500 font-medium">Fecha de Emisión:</span>
                  <span className="font-semibold text-slate-900">{pedido.fecha}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 font-medium">Cliente:</span>
                  <span className="font-bold text-slate-900 text-right">{pedido.cliente.nombre}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 font-medium">DNI / RUC:</span>
                  <span className="font-mono font-bold text-slate-900">{pedido.cliente.dniRuc || "No especificado"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 font-medium">Teléfono:</span>
                  <span className="font-mono font-semibold text-slate-900">{pedido.cliente.telefono}</span>
                </div>
                <div className="flex justify-between items-start gap-2">
                  <span className="text-slate-500 font-medium shrink-0">Destino:</span>
                  <span className="font-medium text-slate-800 text-right">
                    {pedido.tipoEnvio === "Nacional"
                      ? `${pedido.agenciaEncomienda || "Encomienda"} · ${pedido.ciudadDestino || "Provincia"}`
                      : `${pedido.cliente.distrito ? `${pedido.cliente.distrito}, ` : ""}Lima`}
                  </span>
                </div>
                {pedido.cliente.direccion && (
                  <div className="flex justify-between items-start gap-2">
                    <span className="text-slate-500 font-medium shrink-0">Dirección:</span>
                    <span className="text-slate-800 text-right font-medium">{pedido.cliente.direccion}</span>
                  </div>
                )}
                {pedido.cliente.referencia && (
                  <div className="flex justify-between items-start gap-2">
                    <span className="text-slate-500 font-medium shrink-0">Referencia:</span>
                    <span className="text-slate-600 text-right italic">{pedido.cliente.referencia}</span>
                  </div>
                )}
              </div>

              {/* Detalle de Artículos */}
              <div className="py-3.5 border-b border-dashed border-slate-300">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="text-slate-500 font-semibold border-b border-slate-200">
                      <th className="text-left pb-1 font-bold">Cant. / Prenda</th>
                      <th className="text-right pb-1 font-bold">P. Unit</th>
                      <th className="text-right pb-1 font-bold">Importe</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {pedido.items.map((item) => (
                      <tr key={item.productoId} className="text-slate-800">
                        <td className="py-1.5 font-medium">
                          {item.cantidad} × {item.nombre}
                        </td>
                        <td className="py-1.5 text-right font-mono text-slate-600">S/{item.precio.toFixed(2)}</td>
                        <td className="py-1.5 text-right font-mono font-bold text-slate-900">S/{(item.cantidad * item.precio).toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Totales y Descuentos */}
              <div className="py-3 border-b border-dashed border-slate-300 text-xs space-y-1 text-slate-700">
                <div className="flex justify-between">
                  <span>Subtotal Prendas:</span>
                  <span className="font-mono font-medium">
                    S/{pedido.items.reduce((acc, i) => acc + i.cantidad * i.precio, 0).toFixed(2)}
                  </span>
                </div>
                {pedido.costoDelivery > 0 && (
                  <div className="flex justify-between">
                    <span>Flete / Envío ({pedido.tipoEnvio}):</span>
                    <span className="font-mono font-medium">S/{pedido.costoDelivery.toFixed(2)}</span>
                  </div>
                )}
                {pedido.descuento > 0 && (
                  <div className="flex justify-between text-emerald-700 font-semibold">
                    <span>Descuento Cupón {pedido.cuponAplicado ? `(${pedido.cuponAplicado})` : ""}:</span>
                    <span className="font-mono">-S/{pedido.descuento.toFixed(2)}</span>
                  </div>
                )}
                <div className="flex justify-between items-center text-sm font-bold text-slate-950 pt-2 border-t border-slate-200">
                  <span className="text-base">TOTAL PAGADO:</span>
                  <span className="text-lg font-mono text-[#E63946]">S/{pedido.total.toFixed(2)}</span>
                </div>
              </div>

              {/* Método de Pago y N° de Operación */}
              <div className="py-3 text-xs bg-slate-50 rounded-xl p-3 my-2 border border-slate-200 space-y-1">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-slate-600">Forma de Pago:</span>
                  <span className="font-bold text-purple-900 bg-purple-100 px-2 py-0.5 rounded-lg border border-purple-200">
                    {pedido.metodoPago || "Yape / Transferencia"}
                  </span>
                </div>
                {pedido.numeroOperacion && (
                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">N° Operación Bancaria:</span>
                    <span className="font-mono font-bold text-slate-900">{pedido.numeroOperacion}</span>
                  </div>
                )}
              </div>

              {/* Sello de Garantía y QR */}
              <div className="pt-2 text-center text-slate-500">
                <div className="flex items-center justify-center gap-1 text-[11px] font-bold text-blue-900 mb-1">
                  <span className="material-icons" style={{ fontSize: "14px" }}>verified</span>
                  <span>GARANTÍA OFICIAL LEOFIT · CAMBIO DE TALLA GARANTIZADO</span>
                </div>
                <p className="text-[10px] text-slate-400">
                  Conserva este comprobante digital para cualquier cambio o seguimiento de tu orden.
                </p>
              </div>

            </div>
          </div>
        )}

        {/* ================================================================= */}
        {/* VISTA 2: RÓTULO DE DESPACHO PARA ENCOMIENDA (SHALOM / OLVA) */}
        {/* ================================================================= */}
        {vista === "rotulo" && (
          <div className="p-5 sm:p-6 bg-slate-50 overflow-y-auto max-h-[75vh] print:max-h-none print:bg-white print:p-0">
            <div className="bg-white rounded-2xl p-5 border-2 border-dashed border-slate-400 text-slate-900 shadow-sm print:border-solid print:border-2 print:border-black">
              
              {/* Encabezado Rótulo */}
              <div className="flex items-center justify-between pb-3 border-b-2 border-slate-900 mb-3">
                <div>
                  <h3 className="text-lg font-extrabold uppercase tracking-wider text-[#0F223D]">RÓTULO DE DESPACHO</h3>
                  <p className="text-xs font-bold text-slate-600">LEOFIT INDUMENTARIA DEPORTIVA</p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono font-bold bg-[#0F223D] text-white px-3 py-1 rounded-xl block">
                    {pedido.numero}
                  </span>
                  <span className="text-[10px] font-semibold text-slate-500 mt-0.5 block">{pedido.fecha}</span>
                </div>
              </div>

              {/* Remitente */}
              <div className="bg-slate-100 p-2.5 rounded-xl text-xs mb-3 border border-slate-200">
                <span className="text-[10px] font-bold text-slate-500 uppercase block mb-0.5">REMITENTE:</span>
                <p className="font-bold text-slate-900">LEOFIT SOLUTIONS E.I.R.L. / VÍCTOR CÁRDENAS</p>
                <p className="text-slate-700">Lima Metropolitana · Tel: 987 654 321</p>
              </div>

              {/* Destinatario Principal (Grande y Claro para la Agencia) */}
              <div className="border-2 border-slate-900 rounded-2xl p-3.5 mb-3 bg-white">
                <span className="text-[10px] font-extrabold text-[#E63946] uppercase block mb-1 tracking-wider">
                  DATOS DEL DESTINATARIO:
                </span>
                <p className="text-base font-extrabold text-slate-950 uppercase">{pedido.cliente.nombre}</p>
                <div className="grid grid-cols-2 gap-2 mt-1.5 text-xs">
                  <div>
                    <span className="text-slate-500 font-semibold block">DNI / RUC:</span>
                    <span className="font-mono font-bold text-sm text-slate-950">{pedido.cliente.dniRuc || "No registrado"}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 font-semibold block">TELÉFONO:</span>
                    <span className="font-mono font-bold text-sm text-slate-950">{pedido.cliente.telefono}</span>
                  </div>
                </div>
                <div className="mt-2 pt-2 border-t border-slate-200 text-xs">
                  <span className="text-slate-500 font-semibold block">DIRECCIÓN / AGENCIA DESTINO:</span>
                  <p className="font-bold text-slate-900 mt-0.5">{pedido.cliente.direccion}</p>
                  {pedido.cliente.distrito && (
                    <p className="text-slate-700 font-medium">Distrito: <strong>{pedido.cliente.distrito}</strong></p>
                  )}
                  {pedido.cliente.referencia && (
                    <p className="text-slate-600 italic">Ref: {pedido.cliente.referencia}</p>
                  )}
                </div>
              </div>

              {/* Destino y Agencia */}
              {pedido.tipoEnvio === "Nacional" ? (
                <div className="bg-blue-50 border-2 border-blue-400 rounded-xl p-3 text-xs mb-3">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-blue-950 uppercase">EMPRESA DE ENCOMIENDA:</span>
                    <span className="bg-blue-900 text-white font-bold px-2 py-0.5 rounded text-xs">
                      {pedido.agenciaEncomienda || "Shalom"}
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-blue-900">
                    <span>CIUDAD DESTINO:</span>
                    <span className="font-extrabold text-sm">{pedido.ciudadDestino || "PROVINCIA"}</span>
                  </div>
                  {pedido.numeroGuia && (
                    <div className="flex justify-between items-center text-blue-950 mt-1 pt-1 border-t border-blue-200">
                      <span>N° GUÍA / CLAVE:</span>
                      <span className="font-mono font-bold">{pedido.numeroGuia}</span>
                    </div>
                  )}
                </div>
              ) : (
                <div className="bg-emerald-50 border border-emerald-300 rounded-xl p-2.5 text-xs text-emerald-950 font-bold mb-3 flex items-center gap-2">
                  <span className="material-icons text-emerald-700" style={{ fontSize: "18px" }}>two_wheeler</span>
                  <span>REPARTO LOCAL DIRECTO EN LIMA METROPOLITANA</span>
                </div>
              )}

              {/* Advertencia de Cuidado Textil */}
              <div className="flex items-center justify-center gap-1 text-[10px] font-bold text-slate-600 uppercase tracking-wider">
                <span className="material-icons text-amber-600" style={{ fontSize: "14px" }}>warning</span>
                <span>CONTENIDO: INDUMENTARIA DEPORTIVA · MANIPULAR CON CUIDADO</span>
              </div>
            </div>
          </div>
        )}

        {/* Footer con Botones de Acción (No se imprime) */}
        <div className="p-4 bg-white border-t border-slate-200 flex flex-wrap items-center justify-between gap-2 print:hidden">
          <button
            onClick={onClose}
            className="px-4 py-2.5 text-xs sm:text-sm font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-colors"
          >
            Cerrar
          </button>

          <div className="flex items-center gap-2 flex-wrap">
            <a
              href={`https://wa.me/51${pedido.cliente.telefono.replace(/\D/g, "")}?text=${whatsappText}`}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs sm:text-sm font-bold px-3.5 py-2.5 rounded-xl shadow-md transition-all active:scale-95"
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>chat</span>
              <span>Enviar WhatsApp</span>
            </a>

            <button
              onClick={handlePrint}
              className="inline-flex items-center gap-1.5 bg-[#0F223D] hover:bg-[#1E293B] text-white text-xs sm:text-sm font-bold px-4 py-2.5 rounded-xl shadow-md transition-all active:scale-95"
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>print</span>
              <span>Imprimir / PDF</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

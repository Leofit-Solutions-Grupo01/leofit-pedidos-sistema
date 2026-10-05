/**
 * @file ReciboModal.tsx
 * @description Modal interactivo para emisión, descarga en PDF e impresión de Comprobantes Digitales y Rótulos de Encomienda
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { useState } from "react";
import { Pedido } from "../../data/mockData";
import { generarComprobantePDF, generarRotuloPDF, abrirVentanaImpresion } from "../../utils/pdfGenerator";

interface ReciboModalProps {
  pedido: Pedido | null;
  onClose: () => void;
}

export default function ReciboModal({ pedido, onClose }: ReciboModalProps) {
  const [vista, setVista] = useState<"recibo" | "rotulo">("recibo");

  if (!pedido) return null;

  const handleDescargarPdf = () => {
    if (vista === "recibo") {
      generarComprobantePDF(pedido);
    } else {
      generarRotuloPDF(pedido);
    }
  };

  const handleAbrirVentanaImpresion = () => {
    abrirVentanaImpresion(pedido, vista);
  };

  const trackingUrl = `https://leofit.com/rastreo?codigo=${pedido.numero}`;
  const whatsappMessage = encodeURIComponent(
    `*COMPROBANTE DE COMPRA LEOFIT*\n` +
    `*N° Pedido:* ${pedido.numero}\n` +
    `*Fecha:* ${pedido.fecha}\n` +
    `*Cliente:* ${pedido.cliente.nombre}\n` +
    `*DNI/RUC:* ${pedido.cliente.dniRuc || "No registrado"}\n` +
    `*Destino:* ${pedido.tipoEnvio === "Nacional" ? `${pedido.agenciaEncomienda || "Encomienda"} (${pedido.ciudadDestino})` : "Lima Metropolitana"}\n` +
    `*Total Pagado:* S/ ${pedido.total.toFixed(2)}\n\n` +
    `*Rastreo en línea:* ${trackingUrl}\n` +
    `_LeoFit Solutions E.I.R.L._`
  );

  const subtotalPrendas = pedido.items.reduce((acc, i) => acc + i.cantidad * i.precio, 0);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-slate-900/75 backdrop-blur-sm overflow-y-auto print:p-0 print:bg-white print:static">
      {/* Contenedor Principal del Modal */}
      <div className="bg-white rounded-2xl shadow-2xl max-w-xl w-full overflow-hidden border border-slate-200 my-auto animate-in fade-in zoom-in-95 duration-150 print:shadow-none print:border-none print:max-w-none print:w-full print:rounded-none">
        
        {/* Barra superior de control (No se imprime) */}
        <div className="p-3.5 bg-slate-900 text-white flex items-center justify-between gap-2 print:hidden border-b border-slate-800">
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={() => setVista("recibo")}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                vista === "recibo"
                  ? "bg-slate-100 text-slate-950 shadow-sm"
                  : "bg-slate-800 text-slate-300 hover:text-white"
              }`}
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>receipt_long</span>
              <span>Comprobante Digital</span>
            </button>
            <button
              type="button"
              onClick={() => setVista("rotulo")}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                vista === "rotulo"
                  ? "bg-slate-100 text-slate-950 shadow-sm"
                  : "bg-slate-800 text-slate-300 hover:text-white"
              }`}
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>local_shipping</span>
              <span>Rótulo de Encomienda</span>
            </button>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center transition-colors"
            aria-label="Cerrar modal"
          >
            <span className="material-icons" style={{ fontSize: "18px" }}>close</span>
          </button>
        </div>

        {/* ================================================================= */}
        {/* VISTA 1: COMPROBANTE DIGITAL MINIMALISTA Y ESTRUCTURADO           */}
        {/* ================================================================= */}
        {vista === "recibo" && (
          <div className="p-3.5 sm:p-6 bg-slate-100/70 overflow-y-auto max-h-[78vh] print:max-h-none print:bg-white print:p-0">
            {/* Hoja A5 / Comprobante */}
            <div className="bg-white rounded-xl p-5 sm:p-6 border border-slate-300 text-slate-900 shadow-sm print:border-none print:shadow-none print:p-2">
              {/* Encabezado Formal */}
              <div className="flex justify-between items-start pb-4 border-b-2 border-slate-900 gap-3">
                <div>
                  <h2 className="text-lg sm:text-xl font-bold text-slate-950 tracking-tight leading-none">
                    LEOFIT SOLUTIONS E.I.R.L.
                  </h2>
                  <p className="text-xs text-slate-600 font-medium mt-1">
                    R.U.C. 20600000000 · Lima, Perú
                  </p>
                  <p className="text-[11px] text-slate-500 font-medium">
                    Atención al Cliente: +51 987 654 321
                  </p>
                </div>
                <div className="text-right">
                  <span className="inline-block bg-slate-950 text-white px-2.5 py-1 rounded text-xs font-mono font-bold tracking-wider">
                    {pedido.numero}
                  </span>
                  <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mt-1">
                    Comprobante Electrónico
                  </p>
                  <p className="text-xs font-semibold text-slate-700">
                    Fecha: {pedido.fecha}
                  </p>
                </div>
              </div>

              {/* Información del Cliente y Despacho */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 py-3 border-b border-slate-200 text-xs">
                {/* Cliente */}
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                    Datos del Cliente
                  </span>
                  <p className="font-bold text-slate-950 text-sm">{pedido.cliente.nombre}</p>
                  <p className="text-slate-700">
                    <strong>DNI / RUC:</strong> <span className="font-mono">{pedido.cliente.dniRuc || "No registrado"}</span>
                  </p>
                  <p className="text-slate-700">
                    <strong>Teléfono:</strong> <span className="font-mono">{pedido.cliente.telefono}</span>
                  </p>
                </div>

                {/* Entrega */}
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                    Modalidad de Entrega
                  </span>
                  <p className="font-bold text-slate-900">
                    {pedido.tipoEnvio === "Nacional" ? `Nacional (${pedido.agenciaEncomienda || "Encomienda"})` : "Reparto Local Lima"}
                  </p>
                  <p className="text-slate-700">
                    <strong>Destino:</strong> {pedido.ciudadDestino || "Lima"}
                  </p>
                  <p className="text-slate-700">
                    <strong>Dirección:</strong> {pedido.cliente.direccion}
                  </p>
                  {pedido.cliente.referencia && (
                    <p className="text-slate-500 italic">
                      Ref: {pedido.cliente.referencia}
                    </p>
                  )}
                  {pedido.numeroGuia && (
                    <p className="text-blue-900 font-bold">
                      Guía / Clave: <span className="font-mono">{pedido.numeroGuia}</span>
                    </p>
                  )}
                </div>
              </div>

              {/* Tabla de Artículos */}
              <div className="py-3 border-b border-slate-200">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="border-b border-slate-300 text-slate-600">
                      <th className="text-center pb-1.5 font-bold uppercase text-[10px] w-12">Cant.</th>
                      <th className="text-left pb-1.5 font-bold uppercase text-[10px]">Descripción / Prenda</th>
                      <th className="text-right pb-1.5 font-bold uppercase text-[10px] w-20">P. Unit</th>
                      <th className="text-right pb-1.5 font-bold uppercase text-[10px] w-20">Total</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {pedido.items.map((item, idx) => (
                      <tr key={idx} className="text-slate-800">
                        <td className="py-1.5 text-center font-mono font-semibold">{item.cantidad}</td>
                        <td className="py-1.5 font-medium">{item.nombre}</td>
                        <td className="py-1.5 text-right font-mono text-slate-600">S/ {item.precio.toFixed(2)}</td>
                        <td className="py-1.5 text-right font-mono font-bold text-slate-950">
                          S/ {(item.cantidad * item.precio).toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Resumen Económico & Pago */}
              <div className="pt-3 flex flex-col sm:flex-row justify-between items-start sm:items-end gap-3 text-xs">
                {/* Pago */}
                <div className="space-y-1 text-slate-700">
                  <p>
                    <strong>Forma de Pago:</strong> {pedido.metodoPago || "Yape"}
                  </p>
                  {pedido.numeroOperacion && (
                    <p>
                      <strong>N° Operación:</strong> <span className="font-mono font-semibold">{pedido.numeroOperacion}</span>
                    </p>
                  )}
                  <p className="text-[11px] text-emerald-800 font-medium pt-1">
                    Garantía oficial LeoFit de 7 días por cambio de talla.
                  </p>
                </div>

                {/* Totales */}
                <div className="w-full sm:w-56 space-y-1 border-t sm:border-t-0 pt-2 sm:pt-0">
                  <div className="flex justify-between text-slate-600">
                    <span>Subtotal:</span>
                    <span className="font-mono font-medium">S/ {subtotalPrendas.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-slate-600">
                    <span>Envío / Flete:</span>
                    <span className="font-mono font-medium">
                      {pedido.costoDelivery > 0 ? `S/ ${pedido.costoDelivery.toFixed(2)}` : "GRATIS"}
                    </span>
                  </div>
                  {pedido.descuento > 0 && (
                    <div className="flex justify-between text-emerald-700 font-bold">
                      <span>Descuento ({pedido.cuponAplicado || "Cupón"}):</span>
                      <span className="font-mono">-S/ {pedido.descuento.toFixed(2)}</span>
                    </div>
                  )}
                  <div className="flex justify-between items-center text-sm font-bold text-slate-950 pt-1.5 border-t-2 border-slate-900">
                    <span>TOTAL PAGADO:</span>
                    <span className="text-base font-mono">S/ {pedido.total.toFixed(2)}</span>
                  </div>
                </div>
              </div>

              {/* Pie de página con enlace de rastreo */}
              <div className="mt-4 pt-2.5 border-t border-dashed border-slate-300 text-center text-[10px] text-slate-500">
                <p>Rastreo de pedido en vivo: <strong>leofit.com/rastreo?codigo={pedido.numero}</strong></p>
                <p className="mt-0.5">LeoFit Solutions E.I.R.L. · Documento Digital Oficial</p>
              </div>
            </div>
          </div>
        )}

        {/* ================================================================= */}
        {/* VISTA 2: RÓTULO DE ENCOMIENDA MINIMALISTA (SHALOM / OLVA)         */}
        {/* ================================================================= */}
        {vista === "rotulo" && (
          <div className="p-3.5 sm:p-6 bg-slate-100/70 overflow-y-auto max-h-[78vh] print:max-h-none print:bg-white print:p-0">
            <div className="bg-white rounded-xl p-5 border-2 border-slate-900 text-slate-900 shadow-sm print:border-2 print:border-black print:p-3">
              {/* Encabezado Rótulo */}
              <div className="flex justify-between items-center pb-3 border-b-2 border-slate-900 mb-3">
                <div>
                  <h3 className="text-base sm:text-lg font-bold uppercase tracking-tight text-slate-950">
                    RÓTULO DE PAQUETERÍA
                  </h3>
                  <p className="text-xs font-semibold text-slate-600">LEOFIT SOLUTIONS E.I.R.L.</p>
                </div>
                <div className="text-right">
                  <span className="text-sm font-mono font-bold bg-slate-950 text-white px-2.5 py-1 rounded">
                    {pedido.numero}
                  </span>
                  <p className="text-[10px] font-semibold text-slate-500 mt-0.5">{pedido.fecha}</p>
                </div>
              </div>

              {/* Destino y Agencia */}
              <div className="bg-slate-100 p-3 rounded-lg mb-3 border border-slate-300 text-xs">
                <div className="flex justify-between items-center font-bold">
                  <span className="text-slate-600 uppercase text-[11px]">AGENCIA / TRANSPORTE:</span>
                  <span className="text-sm text-slate-950 uppercase">
                    {pedido.agenciaEncomienda || (pedido.tipoEnvio === "Nacional" ? "Shalom" : "Reparto Local")}
                  </span>
                </div>
                <div className="flex justify-between items-center font-bold mt-1.5 pt-1.5 border-t border-slate-200">
                  <span className="text-slate-600 uppercase text-[11px]">CIUDAD DESTINO:</span>
                  <span className="text-sm text-slate-950 uppercase">
                    {pedido.ciudadDestino || "Lima"}
                  </span>
                </div>
                {pedido.numeroGuia && (
                  <div className="flex justify-between items-center font-bold mt-1.5 pt-1.5 border-t border-slate-200 text-blue-900">
                    <span className="uppercase text-[11px]">N° GUÍA / CLAVE:</span>
                    <span className="font-mono text-sm">{pedido.numeroGuia}</span>
                  </div>
                )}
              </div>

              {/* Destinatario */}
              <div className="p-3 border border-slate-300 rounded-lg mb-3 text-xs space-y-1">
                <span className="text-[10px] font-bold text-slate-500 uppercase block">
                  DESTINATARIO (CONSIGNADO):
                </span>
                <p className="text-base font-bold text-slate-950 uppercase">{pedido.cliente.nombre}</p>
                <div className="grid grid-cols-2 gap-2 pt-1 text-slate-700">
                  <p><strong>DNI/RUC:</strong> <span className="font-mono font-bold">{pedido.cliente.dniRuc || "No registrado"}</span></p>
                  <p><strong>Teléfono:</strong> <span className="font-mono font-bold">{pedido.cliente.telefono}</span></p>
                </div>
                <p className="pt-1 text-slate-800">
                  <strong>Dirección / Agencia:</strong> {pedido.cliente.direccion}
                </p>
                {pedido.cliente.referencia && (
                  <p className="text-slate-500 italic">Ref: {pedido.cliente.referencia}</p>
                )}
              </div>

              {/* Remitente */}
              <div className="p-2.5 bg-slate-50 rounded-lg text-[11px] text-slate-600 border border-slate-200 mb-2">
                <p><strong>REMITENTE:</strong> LEOFIT SOLUTIONS E.I.R.L. · RUC: 20600000000</p>
                <p>Lima, Perú · Teléfono: +51 987 654 321</p>
              </div>

              <div className="text-center text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                CONTENIDO: INDUMENTARIA DEPORTIVA · MANIPULAR CON CUIDADO
              </div>
            </div>
          </div>
        )}

        {/* Barra de Acciones Inferior (No se imprime) */}
        <div className="p-3.5 bg-white border-t border-slate-200 flex flex-wrap items-center justify-between gap-2 print:hidden">
          <button
            type="button"
            onClick={onClose}
            className="px-3.5 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors"
          >
            Cerrar
          </button>

          <div className="flex items-center gap-2 flex-wrap">
            <a
              href={`https://wa.me/51${pedido.cliente.telefono.replace(/\D/g, "")}?text=${whatsappMessage}`}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold px-3.5 py-2 rounded-lg transition-all active:scale-95 shadow-sm"
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>chat</span>
              <span>WhatsApp</span>
            </a>

            <button
              type="button"
              onClick={handleDescargarPdf}
              className="inline-flex items-center gap-1.5 bg-[#E63946] hover:bg-[#C62828] text-white text-xs font-bold px-3.5 py-2 rounded-lg transition-all active:scale-95 shadow-sm"
              title="Descargar archivo .pdf nativo"
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>picture_as_pdf</span>
              <span>Descargar PDF</span>
            </button>

            <button
              type="button"
              onClick={handleAbrirVentanaImpresion}
              className="inline-flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-3.5 py-2 rounded-lg transition-all active:scale-95 shadow-sm"
              title="Abrir comprobante limpio para imprimir o guardar PDF"
            >
              <span className="material-icons" style={{ fontSize: "16px" }}>print</span>
              <span>Imprimir / Guardar PDF</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

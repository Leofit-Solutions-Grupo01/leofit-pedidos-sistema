/**
 * @file pdfGenerator.ts
 * @description Generador nativo y robusto de PDFs vectoriales (jsPDF + autoTable) y ventanas de impresión para LeoFit
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import { Pedido } from "../data/mockData";

/**
 * Descarga de manera segura un objeto jsPDF como archivo .pdf con MIME application/pdf real
 */
function descargarBlobPdf(doc: jsPDF, nombreArchivo: string) {
  if (typeof window === "undefined" || typeof document === "undefined") {
    return;
  }

  const nombreFinal = nombreArchivo.endsWith(".pdf") ? nombreArchivo : `${nombreArchivo}.pdf`;

  try {
    const blob = doc.output("blob");
    const pdfBlob = new Blob([blob], { type: "application/pdf" });
    const blobUrl = URL.createObjectURL(pdfBlob);

    const a = document.createElement("a");
    a.style.display = "none";
    a.href = blobUrl;
    a.download = nombreFinal;
    a.setAttribute("download", nombreFinal);
    document.body.appendChild(a);
    a.click();

    // Mantener la URL viva por 60 segundos para asegurar que el navegador complete la escritura a disco
    setTimeout(() => {
      if (document.body.contains(a)) {
        document.body.removeChild(a);
      }
      try {
        URL.revokeObjectURL(blobUrl);
      } catch (_) {
        // Ignorar si ya fue liberado
      }
    }, 60000);
  } catch (error) {
    console.warn("Fallo descarga por Blob, usando doc.save:", error);
    doc.save(nombreFinal);
  }
}

/**
 * Genera y descarga un Comprobante de Venta Electrónico vectorial de alta definición (A5)
 */
export function generarComprobantePDF(pedido: Pedido) {
  const doc = new jsPDF({
    orientation: "portrait",
    unit: "mm",
    format: "a5", // 148 x 210 mm
  });

  const pageWidth = doc.internal.pageSize.getWidth(); // 148 mm
  const margin = 10;
  const contentWidth = pageWidth - margin * 2; // 128 mm

  // ==========================================
  // 1. CABECERA CORPORATIVA LEOFIT
  // ==========================================
  doc.setFillColor(15, 34, 61); // #0F223D
  doc.rect(margin, 10, contentWidth, 18, "F");

  // Logo / Título de la Empresa
  doc.setFont("helvetica", "bold");
  doc.setFontSize(13);
  doc.setTextColor(255, 255, 255);
  doc.text("LEOFIT SOLUTIONS E.I.R.L.", margin + 4, 17);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(7.5);
  doc.setTextColor(203, 213, 225);
  doc.text("R.U.C. 20600000000 · Lima, Perú · Tel: +51 987 654 321", margin + 4, 23);

  // Recuadro de Folio y Fecha (Derecha)
  doc.setFont("helvetica", "bold");
  doc.setFontSize(10);
  doc.setTextColor(255, 255, 255);
  doc.text(pedido.numero, pageWidth - margin - 4, 17, { align: "right" });

  doc.setFont("helvetica", "normal");
  doc.setFontSize(7.5);
  doc.setTextColor(254, 240, 138); // Amarillo suave
  doc.text(`Fecha: ${pedido.fecha}`, pageWidth - margin - 4, 23, { align: "right" });

  let y = 32;

  // ==========================================
  // 2. DATOS DEL CLIENTE Y DESPACHO (2 CAJAS)
  // ==========================================
  const colWidth = (contentWidth - 4) / 2; // ~62 mm cada columna

  // Caja 1: Cliente (Izquierda)
  doc.setDrawColor(203, 213, 225);
  doc.setFillColor(248, 250, 252);
  doc.roundedRect(margin, y, colWidth, 26, 1.5, 1.5, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(7.5);
  doc.setTextColor(15, 34, 61);
  doc.text("DATOS DEL CLIENTE", margin + 3, y + 4.5);

  doc.setFont("helvetica", "bold");
  doc.setFontSize(8.5);
  doc.setTextColor(15, 23, 42);
  const nombreCorto = doc.splitTextToSize(pedido.cliente.nombre, colWidth - 6);
  doc.text(nombreCorto, margin + 3, y + 9.5);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(7.5);
  doc.setTextColor(51, 65, 85);
  doc.text(`DNI/RUC: ${pedido.cliente.dniRuc || "No especificado"}`, margin + 3, y + 17.5);
  doc.text(`Teléfono: ${pedido.cliente.telefono}`, margin + 3, y + 22);

  // Caja 2: Despacho (Derecha)
  const col2X = margin + colWidth + 4;
  doc.roundedRect(col2X, y, colWidth, 26, 1.5, 1.5, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(7.5);
  doc.setTextColor(15, 34, 61);
  doc.text("MODALIDAD DE ENTREGA", col2X + 3, y + 4.5);

  doc.setFont("helvetica", "bold");
  doc.setFontSize(8);
  doc.setTextColor(15, 23, 42);
  const tipoEnvioTexto =
    pedido.tipoEnvio === "Nacional"
      ? `Nacional (${pedido.agenciaEncomienda || "Encomienda"})`
      : "Reparto Local Lima";
  doc.text(tipoEnvioTexto, col2X + 3, y + 9.5);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(7);
  doc.setTextColor(51, 65, 85);
  doc.text(`Destino: ${pedido.ciudadDestino || "Lima"}`, col2X + 3, y + 14);

  const dirTexto = doc.splitTextToSize(`Dirección: ${pedido.cliente.direccion}`, colWidth - 6);
  doc.text(dirTexto, col2X + 3, y + 18);

  if (pedido.numeroGuia) {
    doc.setFont("helvetica", "bold");
    doc.setTextColor(30, 64, 175);
    doc.text(`Guía: ${pedido.numeroGuia}`, col2X + 3, y + 23);
  }

  y += 30;

  // ==========================================
  // 3. TABLA DE PRENDAS Y ARTÍCULOS
  // ==========================================
  const tableData = pedido.items.map((item, idx) => [
    (idx + 1).toString(),
    item.nombre,
    item.cantidad.toString(),
    `S/ ${item.precio.toFixed(2)}`,
    `S/ ${(item.cantidad * item.precio).toFixed(2)}`,
  ]);

  autoTable(doc, {
    startY: y,
    margin: { left: margin, right: margin },
    head: [["#", "Descripción / Prenda", "Cant.", "P. Unit", "Importe"]],
    body: tableData,
    theme: "striped",
    headStyles: {
      fillColor: [15, 34, 61], // #0F223D
      textColor: [255, 255, 255],
      fontSize: 7.5,
      fontStyle: "bold",
      halign: "center",
      cellPadding: 2,
    },
    columnStyles: {
      0: { halign: "center", cellWidth: 8 },
      1: { halign: "left", cellWidth: "auto" },
      2: { halign: "center", cellWidth: 14 },
      3: { halign: "right", cellWidth: 20 },
      4: { halign: "right", cellWidth: 22, fontStyle: "bold" },
    },
    bodyStyles: {
      fontSize: 7.5,
      textColor: [30, 41, 59],
      cellPadding: 2,
    },
    alternateRowStyles: {
      fillColor: [248, 250, 252],
    },
  });

  // Obtener la posición Y final después de la tabla
  // @ts-expect-error autoTable adds lastAutoTable to doc
  const finalY = (doc.lastAutoTable?.finalY || y + 30) + 4;

  // ==========================================
  // 4. DESGLOSE ECONÓMICO Y FORMA DE PAGO
  // ==========================================
  const subtotalPrendas = pedido.items.reduce((acc, i) => acc + i.cantidad * i.precio, 0);

  // Caja de Pago & Rastreo (Izquierda)
  doc.setFillColor(245, 243, 255);
  doc.setDrawColor(221, 214, 254);
  doc.roundedRect(margin, finalY, colWidth, 24, 1.5, 1.5, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(7.5);
  doc.setTextColor(88, 28, 135);
  doc.text("FORMA DE PAGO & VERIFICACIÓN", margin + 3, finalY + 4.5);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(7.5);
  doc.setTextColor(51, 65, 85);
  doc.text(`Método: ${pedido.metodoPago || "Yape"}`, margin + 3, finalY + 9.5);
  if (pedido.numeroOperacion) {
    doc.text(`N° Operación: ${pedido.numeroOperacion}`, margin + 3, finalY + 14);
  }
  doc.setFont("helvetica", "bold");
  doc.setTextColor(22, 101, 52); // Verde esmeralda
  doc.text("Estado: PAGADO / REGISTRADO", margin + 3, finalY + 18.5);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(6.5);
  doc.setTextColor(100, 116, 139);
  doc.text(`Rastreo: leofit.com/rastreo?codigo=${pedido.numero}`, margin + 3, finalY + 22.5);

  // Caja de Totales (Derecha)
  const totalsX = margin + colWidth + 4;
  doc.setFillColor(248, 250, 252);
  doc.setDrawColor(203, 213, 225);
  doc.roundedRect(totalsX, finalY, colWidth, 24, 1.5, 1.5, "FD");

  doc.setFont("helvetica", "normal");
  doc.setFontSize(7.5);
  doc.setTextColor(71, 85, 105);

  doc.text("Subtotal Prendas:", totalsX + 3, finalY + 5);
  doc.text(`S/ ${subtotalPrendas.toFixed(2)}`, pageWidth - margin - 3, finalY + 5, { align: "right" });

  doc.text("Envío / Delivery:", totalsX + 3, finalY + 9);
  const envioStr = pedido.costoDelivery > 0 ? `S/ ${pedido.costoDelivery.toFixed(2)}` : "GRATIS";
  doc.text(envioStr, pageWidth - margin - 3, finalY + 9, { align: "right" });

  if (pedido.descuento > 0) {
    doc.setFont("helvetica", "bold");
    doc.setTextColor(22, 101, 52);
    doc.text(`Descuento (${pedido.cuponAplicado || "Cupón"}):`, totalsX + 3, finalY + 13);
    doc.text(`-S/ ${pedido.descuento.toFixed(2)}`, pageWidth - margin - 3, finalY + 13, { align: "right" });
  }

  // Cuadro destacado TOTAL
  doc.setFillColor(15, 34, 61);
  doc.rect(totalsX + 1, finalY + 15.5, colWidth - 2, 7.5, "F");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(8.5);
  doc.setTextColor(255, 255, 255);
  doc.text("TOTAL PAGADO:", totalsX + 3, finalY + 20.5);

  doc.setTextColor(254, 240, 138); // Amarillo
  doc.text(`S/ ${pedido.total.toFixed(2)}`, pageWidth - margin - 3, finalY + 20.5, { align: "right" });

  // ==========================================
  // 5. PIE DE PÁGINA Y GARANTÍA
  // ==========================================
  const footerY = 198;
  doc.setDrawColor(226, 232, 240);
  doc.line(margin, footerY, pageWidth - margin, footerY);

  doc.setFont("helvetica", "bold");
  doc.setFontSize(6.5);
  doc.setTextColor(15, 34, 61);
  doc.text(
    "GARANTÍA OFICIAL LEOFIT: 7 días de cobertura por cambio de talla o defecto de confección.",
    pageWidth / 2,
    footerY + 3.5,
    { align: "center" }
  );

  doc.setFont("helvetica", "normal");
  doc.setFontSize(6);
  doc.setTextColor(148, 163, 184);
  doc.text(
    "Comprobante digital generado por el Sistema LeoFit · www.leofit.com",
    pageWidth / 2,
    footerY + 7,
    { align: "center" }
  );

  // Descargar archivo PDF de forma robusta
  descargarBlobPdf(doc, `Comprobante-LeoFit-${pedido.numero}.pdf`);
}

/**
 * Genera y descarga un Rótulo de Encomienda para paquetería (Shalom, Olva, etc.) en alta definición
 */
export function generarRotuloPDF(pedido: Pedido) {
  const doc = new jsPDF({
    orientation: "portrait",
    unit: "mm",
    format: "a5",
  });

  const pageWidth = doc.internal.pageSize.getWidth();
  const margin = 10;
  const contentWidth = pageWidth - margin * 2;

  // 1. Cabecera Rótulo
  doc.setFillColor(15, 34, 61);
  doc.rect(margin, 10, contentWidth, 16, "F");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(12);
  doc.setTextColor(255, 255, 255);
  doc.text("RÓTULO DE DESPACHO - ENCOMIENDA", margin + 4, 18);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(8);
  doc.setTextColor(203, 213, 225);
  doc.text("LEOFIT INDUMENTARIA DEPORTIVA E.I.R.L.", margin + 4, 23);

  doc.setFont("helvetica", "bold");
  doc.setFontSize(11);
  doc.setTextColor(254, 240, 138);
  doc.text(pedido.numero, pageWidth - margin - 4, 18, { align: "right" });

  doc.setFont("helvetica", "normal");
  doc.setFontSize(7.5);
  doc.setTextColor(255, 255, 255);
  doc.text(pedido.fecha, pageWidth - margin - 4, 23, { align: "right" });

  let y = 30;

  // 2. Destino y Agencia de Transporte (Caja Destacada Grande)
  doc.setFillColor(239, 246, 255);
  doc.setDrawColor(59, 130, 246);
  doc.setLineWidth(0.8);
  doc.roundedRect(margin, y, contentWidth, 24, 2, 2, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(8);
  doc.setTextColor(30, 64, 175);
  doc.text("AGENCIA DE TRANSPORTE / ENCOMIENDA:", margin + 4, y + 6);

  doc.setFontSize(13);
  doc.setTextColor(15, 23, 42);
  const agenciaTexto = pedido.agenciaEncomienda || (pedido.tipoEnvio === "Nacional" ? "Shalom" : "Reparto Local");
  doc.text(agenciaTexto.toUpperCase(), pageWidth - margin - 4, y + 6, { align: "right" });

  doc.setFont("helvetica", "bold");
  doc.setFontSize(9);
  doc.setTextColor(30, 64, 175);
  doc.text("CIUDAD DE DESTINO:", margin + 4, y + 15);

  doc.setFontSize(14);
  doc.setTextColor(185, 28, 28); // Rojo oscuro
  doc.text((pedido.ciudadDestino || "LIMA").toUpperCase(), pageWidth - margin - 4, y + 15, { align: "right" });

  if (pedido.numeroGuia) {
    doc.setFont("helvetica", "bold");
    doc.setFontSize(8.5);
    doc.setTextColor(30, 64, 175);
    doc.text(`N° GUÍA / CLAVE: ${pedido.numeroGuia}`, margin + 4, y + 21);
  }

  y += 28;

  // 3. Destinatario (Consignado) - Caja Grande
  doc.setFillColor(255, 255, 255);
  doc.setDrawColor(15, 23, 42);
  doc.setLineWidth(0.8);
  doc.roundedRect(margin, y, contentWidth, 54, 2, 2, "FD");

  doc.setFillColor(15, 34, 61);
  doc.rect(margin + 0.8, y + 0.8, contentWidth - 1.6, 6.5, "F");
  doc.setFont("helvetica", "bold");
  doc.setFontSize(8);
  doc.setTextColor(255, 255, 255);
  doc.text("DATOS DEL DESTINATARIO (CONSIGNADO)", margin + 4, y + 5.5);

  doc.setFont("helvetica", "bold");
  doc.setFontSize(12);
  doc.setTextColor(15, 23, 42);
  doc.text(pedido.cliente.nombre.toUpperCase(), margin + 4, y + 14);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(9);
  doc.setTextColor(51, 65, 85);
  doc.text(`DNI / RUC:`, margin + 4, y + 21);
  doc.setFont("helvetica", "bold");
  doc.setTextColor(15, 23, 42);
  doc.text(`${pedido.cliente.dniRuc || "NO REGISTRADO"}`, margin + 25, y + 21);

  doc.setFont("helvetica", "normal");
  doc.setTextColor(51, 65, 85);
  doc.text(`Teléfono:`, margin + 70, y + 21);
  doc.setFont("helvetica", "bold");
  doc.setTextColor(15, 23, 42);
  doc.text(`${pedido.cliente.telefono}`, margin + 88, y + 21);

  doc.setFont("helvetica", "normal");
  doc.setTextColor(51, 65, 85);
  doc.text(`Dirección / Agencia:`, margin + 4, y + 29);
  doc.setFont("helvetica", "bold");
  doc.setTextColor(15, 23, 42);
  const dirLines = doc.splitTextToSize(pedido.cliente.direccion, contentWidth - 8);
  doc.text(dirLines, margin + 4, y + 35);

  if (pedido.cliente.referencia) {
    doc.setFont("helvetica", "italic");
    doc.setFontSize(8);
    doc.setTextColor(100, 116, 139);
    const refLines = doc.splitTextToSize(`Ref: ${pedido.cliente.referencia}`, contentWidth - 8);
    doc.text(refLines, margin + 4, y + 47);
  }

  y += 58;

  // 4. Remitente
  doc.setFillColor(248, 250, 252);
  doc.setDrawColor(203, 213, 225);
  doc.setLineWidth(0.4);
  doc.roundedRect(margin, y, contentWidth, 18, 1.5, 1.5, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(7.5);
  doc.setTextColor(71, 85, 105);
  doc.text("REMITENTE:", margin + 3, y + 4.5);

  doc.setFontSize(8.5);
  doc.setTextColor(15, 23, 42);
  doc.text("LEOFIT SOLUTIONS E.I.R.L. · RUC: 20600000000", margin + 3, y + 10);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(7.5);
  doc.setTextColor(100, 116, 139);
  doc.text("Lima Metropolitana, Perú · Teléfono: +51 987 654 321", margin + 3, y + 14.5);

  y += 22;

  // 5. Advertencia de Contenido
  doc.setFillColor(254, 242, 242);
  doc.setDrawColor(252, 165, 165);
  doc.roundedRect(margin, y, contentWidth, 12, 1.5, 1.5, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(8);
  doc.setTextColor(185, 28, 28);
  doc.text(
    "CONTENIDO: INDUMENTARIA & TEXTIL DEPORTIVO · MANIPULAR CON CUIDADO",
    pageWidth / 2,
    y + 7.5,
    { align: "center" }
  );

  descargarBlobPdf(doc, `Rotulo-Encomienda-${pedido.numero}.pdf`);
}

/**
 * Abre una ventana emergente limpia e independiente formateada para impresión física o Guardar como PDF
 */
export function abrirVentanaImpresion(pedido: Pedido, vista: "recibo" | "rotulo") {
  const printWindow = window.open("", "_blank", "width=800,height=900");
  if (!printWindow) {
    window.print();
    return;
  }

  const subtotalPrendas = pedido.items.reduce((acc, i) => acc + i.cantidad * i.precio, 0);

  const htmlContent = `
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>${vista === "recibo" ? `Comprobante_${pedido.numero}` : `Rotulo_${pedido.numero}`}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
    body { background: #f8fafc; color: #0f172a; padding: 20px; display: flex; justify-content: center; }
    .page { width: 148mm; min-height: 210mm; background: #ffffff; padding: 14mm; border: 1px solid #cbd5e1; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    @media print {
      body { background: #ffffff; padding: 0; }
      .page { width: 100%; border: none; box-shadow: none; padding: 10mm; }
      .no-print { display: none !important; }
    }
    .header { background: #0f223d; color: #ffffff; padding: 12px 14px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; }
    .header h1 { font-size: 14px; font-weight: 800; letter-spacing: -0.2px; }
    .header p { font-size: 10px; color: #94a3b8; margin-top: 2px; }
    .badge { background: #ffffff; color: #0f223d; font-family: monospace; font-weight: 800; font-size: 12px; padding: 3px 8px; border-radius: 4px; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 12px 0; }
    .card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; font-size: 11px; }
    .card-title { font-size: 9px; font-weight: 800; color: #64748b; text-transform: uppercase; margin-bottom: 4px; }
    table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 11px; }
    th { background: #0f223d; color: #ffffff; font-weight: 700; text-transform: uppercase; font-size: 9px; padding: 6px 8px; }
    td { padding: 6px 8px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) td { background: #f8fafc; }
    .totals-box { background: #0f223d; color: #ffffff; padding: 10px 12px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; font-weight: 800; margin-top: 8px; }
    .totals-amount { color: #fef08a; font-size: 16px; font-family: monospace; }
    .footer { margin-top: 14px; padding-top: 8px; border-top: 1px dashed #cbd5e1; text-align: center; font-size: 9px; color: #64748b; }
    .btn-bar { position: fixed; top: 12px; right: 12px; display: flex; gap: 8px; z-index: 999; }
    .btn { background: #0f223d; color: #ffffff; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; font-size: 12px; cursor: pointer; }
    .btn-red { background: #e63946; }
  </style>
</head>
<body>
  <div class="btn-bar no-print">
    <button class="btn btn-red" onclick="window.print()">Imprimir / Guardar como PDF</button>
    <button class="btn" onclick="window.close()">Cerrar</button>
  </div>

  <div class="page">
    ${
      vista === "recibo"
        ? `
      <div class="header">
        <div>
          <h1>LEOFIT SOLUTIONS E.I.R.L.</h1>
          <p>R.U.C. 20600000000 · Lima, Perú · Tel: +51 987 654 321</p>
        </div>
        <div style="text-align: right;">
          <span class="badge">${pedido.numero}</span>
          <p style="color: #fef08a; margin-top: 3px;">Fecha: ${pedido.fecha}</p>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title">Datos del Cliente</div>
          <p><strong>${pedido.cliente.nombre}</strong></p>
          <p style="color: #475569; margin-top: 2px;">DNI/RUC: <strong>${pedido.cliente.dniRuc || "No registrado"}</strong></p>
          <p style="color: #475569;">Teléfono: <strong>${pedido.cliente.telefono}</strong></p>
        </div>
        <div class="card">
          <div class="card-title">Entrega y Destino</div>
          <p><strong>${pedido.tipoEnvio === "Nacional" ? `Nacional (${pedido.agenciaEncomienda || "Shalom"})` : "Reparto Local Lima"}</strong></p>
          <p style="color: #475569; margin-top: 2px;">Destino: ${pedido.ciudadDestino || "Lima"}</p>
          <p style="color: #475569;">Dir: ${pedido.cliente.direccion}</p>
          ${pedido.numeroGuia ? `<p style="color: #1e40af; font-weight: bold;">Guía: ${pedido.numeroGuia}</p>` : ""}
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th style="text-align: center; width: 30px;">#</th>
            <th style="text-align: left;">Descripción / Prenda</th>
            <th style="text-align: center; width: 45px;">Cant.</th>
            <th style="text-align: right; width: 70px;">P. Unit</th>
            <th style="text-align: right; width: 75px;">Total</th>
          </tr>
        </thead>
        <tbody>
          ${pedido.items
            .map(
              (item, i) => `
            <tr>
              <td style="text-align: center; font-family: monospace;">${i + 1}</td>
              <td><strong>${item.nombre}</strong></td>
              <td style="text-align: center; font-family: monospace;">${item.cantidad}</td>
              <td style="text-align: right; font-family: monospace;">S/ ${item.precio.toFixed(2)}</td>
              <td style="text-align: right; font-family: monospace; font-weight: bold;">S/ ${(item.cantidad * item.precio).toFixed(2)}</td>
            </tr>
          `
            )
            .join("")}
        </tbody>
      </table>

      <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 10px;">
        <div style="font-size: 11px; color: #475569;">
          <p><strong>Forma de Pago:</strong> ${pedido.metodoPago || "Yape"}</p>
          ${pedido.numeroOperacion ? `<p><strong>N° Operación:</strong> ${pedido.numeroOperacion}</p>` : ""}
          <p style="color: #166534; font-weight: bold; margin-top: 4px;">Garantía LeoFit de 7 días por cambio de talla.</p>
        </div>
        <div style="width: 220px; font-size: 11px;">
          <div style="display: flex; justify-content: space-between; color: #64748b; margin-bottom: 2px;">
            <span>Subtotal:</span>
            <span style="font-family: monospace;">S/ ${subtotalPrendas.toFixed(2)}</span>
          </div>
          <div style="display: flex; justify-content: space-between; color: #64748b; margin-bottom: 2px;">
            <span>Envío / Delivery:</span>
            <span style="font-family: monospace;">${pedido.costoDelivery > 0 ? `S/ ${pedido.costoDelivery.toFixed(2)}` : "GRATIS"}</span>
          </div>
          ${
            pedido.descuento > 0
              ? `
            <div style="display: flex; justify-content: space-between; color: #166534; font-weight: bold; margin-bottom: 2px;">
              <span>Descuento:</span>
              <span style="font-family: monospace;">-S/ ${pedido.descuento.toFixed(2)}</span>
            </div>
          `
              : ""
          }
          <div class="totals-box">
            <span>TOTAL PAGADO:</span>
            <span class="totals-amount">S/ ${pedido.total.toFixed(2)}</span>
          </div>
        </div>
      </div>
    `
        : `
      <div class="header">
        <div>
          <h1>RÓTULO DE DESPACHO - ENCOMIENDA</h1>
          <p>LEOFIT INDUMENTARIA DEPORTIVA E.I.R.L.</p>
        </div>
        <div style="text-align: right;">
          <span class="badge">${pedido.numero}</span>
          <p style="color: #fef08a; margin-top: 3px;">${pedido.fecha}</p>
        </div>
      </div>

      <div style="background: #eff6ff; border: 2px solid #3b82f6; border-radius: 6px; padding: 12px; margin: 12px 0;">
        <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: bold; color: #1e40af;">
          <span>AGENCIA / TRANSPORTE:</span>
          <span style="font-size: 14px; color: #0f172a;">${(pedido.agenciaEncomienda || (pedido.tipoEnvio === "Nacional" ? "Shalom" : "Reparto Local")).toUpperCase()}</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: bold; color: #1e40af; margin-top: 6px; padding-top: 6px; border-top: 1px solid #bfdbfe;">
          <span>CIUDAD DE DESTINO:</span>
          <span style="font-size: 16px; color: #b91c1c;">${(pedido.ciudadDestino || "LIMA").toUpperCase()}</span>
        </div>
        ${pedido.numeroGuia ? `<div style="font-size: 11px; color: #1e40af; font-weight: bold; margin-top: 4px;">N° GUÍA / CLAVE: ${pedido.numeroGuia}</div>` : ""}
      </div>

      <div style="border: 2px solid #0f172a; border-radius: 6px; padding: 14px; margin-bottom: 12px; font-size: 12px;">
        <div style="background: #0f223d; color: #ffffff; padding: 4px 8px; margin: -14px -14px 10px -14px; font-size: 10px; font-weight: bold;">
          DESTINATARIO (CONSIGNADO)
        </div>
        <p style="font-size: 16px; font-weight: 800; text-transform: uppercase;">${pedido.cliente.nombre}</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 8px 0; padding: 6px 0; border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;">
          <p><strong>DNI / RUC:</strong> ${pedido.cliente.dniRuc || "No registrado"}</p>
          <p><strong>Teléfono:</strong> ${pedido.cliente.telefono}</p>
        </div>
        <p><strong>Dirección / Agencia:</strong> ${pedido.cliente.direccion}</p>
        ${pedido.cliente.referencia ? `<p style="color: #64748b; font-style: italic; margin-top: 4px;">Ref: ${pedido.cliente.referencia}</p>` : ""}
      </div>

      <div class="card" style="font-size: 10px; margin-bottom: 10px;">
        <p><strong>REMITENTE:</strong> LEOFIT SOLUTIONS E.I.R.L. · RUC: 20600000000</p>
        <p style="color: #64748b;">Lima Metropolitana, Perú · Tel: +51 987 654 321</p>
      </div>

      <div style="background: #fef2f2; border: 1px solid #fca5a5; padding: 8px; border-radius: 6px; text-align: center; font-size: 10px; font-weight: bold; color: #b91c1c;">
        CONTENIDO: INDUMENTARIA & TEXTIL DEPORTIVO · MANIPULAR CON CUIDADO
      </div>
    `
    }

    <div class="footer">
      <p>Rastreo en vivo: leofit.com/rastreo?codigo=${pedido.numero} · LeoFit Solutions E.I.R.L.</p>
    </div>
  </div>

  <script>
    window.onload = function() {
      // Opcional: auto-impresión lista al cargar
    };
  </script>
</body>
</html>
`;

  printWindow.document.open();
  printWindow.document.write(htmlContent);
  printWindow.document.close();
}

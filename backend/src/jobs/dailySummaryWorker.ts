/**
 * @file dailySummaryWorker.ts
 * @description Worker periódico para envío del Resumen Diario de Boletas de Venta Electrónicas (RC) a SUNAT.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * 
 * Normativa SUNAT:
 * - Las boletas electrónicas ('03') deben informarse formalmente mediante Resumen Diario dentro de los 7 días.
 * - Este job agrupa boletas emitidas que aún no tienen resumen_enviado_at, envía el RC a Nubefact y guarda el ticket.
 */

import { dbPool, isPostgresAvailable } from '../config/database';
import { NubefactService } from '../services/sunat/nubefact.service';
import { logger } from '../utils/logger';
import { alertSlack } from '../utils/alerts';

export async function sendDailySummary(): Promise<{ count: number; ticket?: string }> {
  if (!isPostgresAvailable()) {
    return { count: 0 };
  }

  const { rows } = await dbPool.query(`
    SELECT id, serie, numero, monto_total as total, created_at as fecha_emision, hash_sunat
      FROM invoices
     WHERE tipo = '03'
       AND estado = 'ACEPTADO'
       AND resumen_enviado_at IS NULL
     ORDER BY numero ASC
  `);

  if (rows.length === 0) {
    return { count: 0 };
  }

  const payload = {
    operacion: 'generar_comprobante',
    tipo_de_comprobante: 'RC',
    fecha_generacion: new Date().toISOString().slice(0, 10),
    fecha_resumen: new Date(Date.now() - 86400000).toISOString().slice(0, 10),
    moneda: 'PEN',
    comprobantes: rows.map((r) => ({
      tipo_doc: '03',
      serie: r.serie,
      numero: r.numero,
      total: Number(r.total),
      estado: '1' // 1 = Adición / Comprobante emitido
    }))
  };

  try {
    const res = await NubefactService.sendDailySummary(payload);
    await dbPool.query(
      `UPDATE invoices
          SET resumen_enviado_at = NOW(),
              resumen_ticket = $1,
              updated_at = NOW()
        WHERE id = ANY($2::int[])`,
      [res.ticket, rows.map((r) => r.id)]
    );

    logger.info('[Daily Summary] Resumen diario de boletas enviado exitosamente:', {
      count: rows.length,
      ticket: res.ticket
    });

    return { count: rows.length, ticket: res.ticket };
  } catch (err: any) {
    logger.error('[Daily Summary Error] Falló el envío del resumen diario a SUNAT:', { err: err.message });
    await alertSlack('❌ Resumen diario de boletas falló', {
      count: rows.length,
      err: err.message
    });
    throw err;
  }
}

export function startDailySummaryWorker(): NodeJS.Timeout {
  // Se ejecuta cada hora para comprobar si hay boletas pendientes de informar
  const handle = setInterval(() => {
    sendDailySummary().catch(() => {});
  }, 60 * 60_000);

  handle.unref();
  return handle;
}

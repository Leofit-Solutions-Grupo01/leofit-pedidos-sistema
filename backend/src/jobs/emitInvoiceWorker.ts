/**
 * @file emitInvoiceWorker.ts
 * @description Worker asíncrono para procesamiento de la cola de emisión de comprobantes SUNAT / Nubefact.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * 
 * Garantías Críticas:
 * 1. Correlativos atómicos sin gaps mediante reserveInvoiceNumber(client, tipo, serie).
 * 2. Desglose exacto de IGV con splitIgv(totalCents) (Decimal.js, sin drift).
 * 3. Si el pedido fue cancelado antes de emitir, se marca como SKIPPED (evita boletas indebidas).
 */

import { dbPool, isPostgresAvailable } from '../config/database';
import { NubefactService, NubefactResponse, reserveInvoiceNumber } from '../services/sunat/nubefact.service';
import { splitIgv } from '../utils/igv';
import { logger } from '../utils/logger';
import { alertSlack } from '../utils/alerts';
import { InMemoryDataStore } from '../infrastructure/repositories/memory.repositories';

export interface MemoryInvoiceQueueItem {
  id: number;
  orderId: number;
  tipo: '01' | '03' | '07';
  estado: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED' | 'SKIPPED';
  attempts: number;
  maxAttempts: number;
  nextAttemptAt: Date;
  lastError?: string;
  payload?: any;
}

export interface MemoryInvoice {
  id: number;
  orderId: number;
  tipo: string;
  serie: string;
  numero: number;
  clienteTipoDocumento: string;
  clienteNumeroDocumento: string;
  clienteDenominacion: string;
  montoSubtotal: number;
  montoIgv: number;
  montoTotal: number;
  moneda: string;
  xmlUrl: string;
  pdfUrl: string;
  cdrUrl: string;
  hashSunat: string;
  estado: 'PENDIENTE' | 'ACEPTADO' | 'RECHAZADO' | 'ANULADO';
  sunatResponse?: any;
  createdAt: Date;
}

export const memoryInvoiceQueue: MemoryInvoiceQueueItem[] = [];
export const memoryInvoices: MemoryInvoice[] = [];

// Tiempos de reintento exponencial: [1 minuto, 5 minutos, 30 minutos, 2 horas]
const BACKOFF_MINUTES = [1, 5, 30, 120];

export async function enqueueInvoice(
  orderId: number,
  tipo: '01' | '03' = '03',
  payload: Record<string, any> = {}
): Promise<number> {
  if (isPostgresAvailable()) {
    const { rows } = await dbPool.query(
      `INSERT INTO invoice_queue (order_id, tipo, estado, payload, next_attempt_at)
       VALUES ($1, $2, 'PENDING', $3, NOW())
       RETURNING id`,
      [orderId, tipo, JSON.stringify(payload)]
    );
    logger.info('[Invoice Queue] Tarea encolada para emisión:', { queueId: rows[0].id, orderId, tipo });
    return rows[0].id;
  } else {
    const nextId = memoryInvoiceQueue.length + 1;
    memoryInvoiceQueue.push({
      id: nextId,
      orderId,
      tipo,
      estado: 'PENDING',
      attempts: 0,
      maxAttempts: 5,
      nextAttemptAt: new Date(),
      payload
    });
    logger.info('[Invoice Queue Memory] Tarea encolada en memoria:', { queueId: nextId, orderId, tipo });
    return nextId;
  }
}

export async function processInvoiceQueue(): Promise<number> {
  let processedCount = 0;

  if (isPostgresAvailable()) {
    const { rows: jobs } = await dbPool.query(
      `SELECT q.id, q.order_id, q.tipo, q.attempts, q.max_attempts, q.payload,
              o.cliente_nombre, o.cliente_email, o.total_amount, o.estado as order_estado,
              COALESCE(o.total_cents, ROUND(o.total_amount * 100)::bigint) as total_cents
         FROM invoice_queue q
         JOIN orders o ON o.id = q.order_id
        WHERE q.estado IN ('PENDING', 'PROCESSING')
          AND q.next_attempt_at <= NOW()
        ORDER BY q.created_at ASC
        LIMIT 20`
    );

    for (const job of jobs) {
      // 1. Si el pedido fue cancelado antes de la emisión, saltar (SKIPPED)
      if (job.order_estado === 'CANCELADO') {
        await dbPool.query(
          `UPDATE invoice_queue
              SET estado = 'SKIPPED',
                  last_error = 'ORDER_CANCELLED_BEFORE_EMISSION',
                  updated_at = NOW()
            WHERE id = $1`,
          [job.id]
        );
        logger.info('[Invoice Worker] Pedido cancelado antes de emitir comprobante. Tarea marcada como SKIPPED.', {
          orderId: job.order_id,
          queueId: job.id
        });
        continue;
      }

      const attempts = job.attempts + 1;
      await dbPool.query(
        `UPDATE invoice_queue
            SET estado = 'PROCESSING',
                attempts = $1,
                updated_at = NOW()
          WHERE id = $2`,
        [attempts, job.id]
      );

      const client = await dbPool.connect();
      try {
        await client.query('BEGIN');

        // Consultar items del pedido
        const { rows: items } = await client.query(
          `SELECT oi.quantity, oi.unit_price, p.name
             FROM order_items oi
             JOIN product_variants pv ON pv.id = oi.variant_id
             JOIN products p ON p.id = pv.product_id
            WHERE oi.order_id = $1`,
          [job.order_id]
        );

        const invoiceItems = items.map((i) => ({
          name: i.name,
          quantity: i.quantity,
          unitPrice: Number(i.unit_price)
        }));

        const totalCents = Number(job.total_cents || Math.round(Number(job.total_amount) * 100));
        const { subtotal, igv, total } = splitIgv(totalCents);

        const serie = job.tipo === '01' ? 'FFF1' : 'BBB1';
        // Reserva atómica de correlativo sin gaps (SUNAT)
        const numero = await reserveInvoiceNumber(client, job.tipo, serie);

        // Llamar a Nubefact con el número reservado
        const cpeResult: NubefactResponse = await NubefactService.emitInvoice({
          orderId: job.order_id,
          tipoComprobante: job.tipo,
          clienteDenominacion: job.cliente_nombre || 'Cliente LeoFit',
          clienteEmail: job.cliente_email,
          totalAmount: total,
          numero,
          items: invoiceItems.length > 0 ? invoiceItems : [{ name: 'Prendas Deportivas LeoFit', quantity: 1, unitPrice: total }]
        });

        // Registrar comprobante oficial en la tabla `invoices`
        await client.query(
          `INSERT INTO invoices
             (order_id, tipo, serie, numero, cliente_denominacion, cliente_email,
              monto_subtotal, monto_igv, monto_total, xml_url, pdf_url, cdr_url,
              hash_sunat, estado, sunat_response)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, 'ACEPTADO', $14)
           ON CONFLICT (tipo, serie, numero) DO UPDATE
           SET estado = 'ACEPTADO', xml_url = EXCLUDED.xml_url, pdf_url = EXCLUDED.pdf_url, updated_at = NOW()`,
          [
            job.order_id,
            cpeResult.tipo,
            cpeResult.serie,
            cpeResult.numero,
            job.cliente_nombre || 'Cliente LeoFit',
            job.cliente_email,
            subtotal,
            igv,
            total,
            cpeResult.enlace_del_xml,
            cpeResult.enlace_del_pdf,
            cpeResult.enlace_del_cdr,
            cpeResult.codigo_hash,
            JSON.stringify(cpeResult.sunat_response || {})
          ]
        );

        // Marcar tarea como COMPLETED
        await client.query(
          `UPDATE invoice_queue
              SET estado = 'COMPLETED',
                  last_error = NULL,
                  updated_at = NOW()
            WHERE id = $1`,
          [job.id]
        );

        await client.query('COMMIT');

        logger.info('[Invoice Worker] Comprobante emitido con éxito:', {
          orderId: job.order_id,
          cpe: `${cpeResult.serie}-${cpeResult.numero}`
        });
        processedCount++;
      } catch (err: any) {
        await client.query('ROLLBACK').catch(() => {});
        logger.error('[Invoice Worker Error] Falló emisión de comprobante:', {
          queueId: job.id,
          orderId: job.order_id,
          error: err.message
        });

        if (attempts >= job.max_attempts) {
          await dbPool.query(
            `UPDATE invoice_queue
                SET estado = 'FAILED',
                    last_error = $1,
                    updated_at = NOW()
              WHERE id = $2`,
            [err.message, job.id]
          );
          await alertSlack('🚨 Emisión de comprobante SUNAT falló definitivamente tras 5 intentos', {
            orderId: job.order_id,
            error: err.message
          });
        } else {
          const delayMin = BACKOFF_MINUTES[attempts - 1] || 120;
          await dbPool.query(
            `UPDATE invoice_queue
                SET estado = 'PENDING',
                    last_error = $1,
                    next_attempt_at = NOW() + INTERVAL '${delayMin} minutes',
                    updated_at = NOW()
              WHERE id = $2`,
            [err.message, job.id]
          );
        }
      } finally {
        client.release();
      }
    }
  } else {
    // ─── Procesamiento en Memoria ───
    for (const job of memoryInvoiceQueue) {
      if (job.estado !== 'PENDING' && job.estado !== 'PROCESSING') continue;
      if (job.nextAttemptAt > new Date()) continue;

      const order = InMemoryDataStore.orders.find((o) => o.id === job.orderId);
      if (!order) {
        job.estado = 'FAILED';
        job.lastError = 'ORDER_NOT_FOUND';
        continue;
      }

      const orderEstado = ((order as any).estado || order.status || '').toUpperCase();
      if (orderEstado === 'CANCELADO') {
        job.estado = 'SKIPPED';
        job.lastError = 'ORDER_CANCELLED_BEFORE_EMISSION';
        continue;
      }

      job.estado = 'PROCESSING';
      job.attempts++;

      try {
        const totalCents = Math.round(Number(order.total_amount) * 100);
        const { subtotal, igv, total } = splitIgv(totalCents);

        const invoiceItems = (order.items || []).map((i: any) => ({
          name: i.product_name || i.variant?.product?.name || 'Prenda LeoFit',
          quantity: i.quantity,
          unitPrice: Number(i.unit_price)
        }));

        const cpeResult = await NubefactService.emitInvoice({
          orderId: order.id,
          tipoComprobante: job.tipo === '01' ? '01' : '03',
          clienteDenominacion: order.client?.full_name || (order.client as any)?.name || 'Cliente LeoFit',
          clienteEmail: (order.client as any)?.email || 'comprobantes@leofit.pe',
          totalAmount: total,
          items: invoiceItems.length > 0 ? invoiceItems : [{ name: 'Prenda Deportiva LeoFit', quantity: 1, unitPrice: total }]
        });

        memoryInvoices.push({
          id: memoryInvoices.length + 1,
          orderId: order.id,
          tipo: cpeResult.tipo,
          serie: cpeResult.serie,
          numero: cpeResult.numero,
          clienteTipoDocumento: '0',
          clienteNumeroDocumento: '00000000',
          clienteDenominacion: order.client?.full_name || 'Cliente LeoFit',
          montoSubtotal: subtotal,
          montoIgv: igv,
          montoTotal: total,
          moneda: 'PEN',
          xmlUrl: cpeResult.enlace_del_xml,
          pdfUrl: cpeResult.enlace_del_pdf,
          cdrUrl: cpeResult.enlace_del_cdr,
          hashSunat: cpeResult.codigo_hash,
          estado: 'ACEPTADO',
          sunatResponse: cpeResult.sunat_response,
          createdAt: new Date()
        });

        job.estado = 'COMPLETED';
        processedCount++;
      } catch (err: any) {
        job.lastError = err.message;
        if (job.attempts >= job.maxAttempts) {
          job.estado = 'FAILED';
        } else {
          job.estado = 'PENDING';
        }
      }
    }
  }

  return processedCount;
}

export function startInvoiceWorker(): NodeJS.Timeout {
  const INTERVAL_MS = parseInt(process.env.INVOICE_WORKER_INTERVAL_MS || '60000', 10); // 1 minuto
  const timer = setInterval(() => {
    processInvoiceQueue().catch((err) =>
      logger.error('[Invoice Worker Scheduler Error]', { error: err.message })
    );
  }, INTERVAL_MS);

  timer.unref();
  return timer;
}

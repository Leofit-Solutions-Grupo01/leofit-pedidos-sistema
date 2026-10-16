/**
 * @file invoice.controller.ts
 * @description Controlador para consulta de Comprobantes Electrónicos SUNAT, descarga de PDF/XML, notas de crédito y validación de RUC.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import { Request, Response, NextFunction } from 'express';
import { dbPool, isPostgresAvailable } from '../config/database';
import { validateRuc, NubefactService } from '../services/sunat/nubefact.service';
import { memoryInvoices } from '../jobs/emitInvoiceWorker';
import { logger } from '../utils/logger';

export class InvoiceController {
  /**
   * @route GET /api/sunat/ruc/:numero
   * @desc Valida un número de RUC contra el algoritmo de SUNAT y devuelve estado en el padrón
   */
  public static async validateRucEndpoint(req: Request, res: Response): Promise<void> {
    const { numero } = req.params;
    const result = validateRuc(numero);

    if (!result.valid) {
      res.status(400).json({
        success: false,
        error: {
          code: 'INVALID_RUC',
          message: result.error
        }
      });
      return;
    }

    res.status(200).json({
      success: true,
      data: result
    });
  }

  /**
   * @route GET /api/invoices/order/:orderId
   * @desc Retorna el comprobante de pago electrónico emitido para un pedido
   */
  public static async getByOrderId(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const orderId = Number(req.params.orderId);

      if (isPostgresAvailable()) {
        const { rows } = await dbPool.query(
          `SELECT id, order_id, tipo, serie, numero, cliente_denominacion,
                  monto_subtotal, monto_igv, monto_total, moneda,
                  xml_url, pdf_url, cdr_url, hash_sunat, estado, created_at
             FROM invoices
            WHERE order_id = $1
            ORDER BY created_at DESC LIMIT 1`,
          [orderId]
        );

        if (!rows[0]) {
          res.status(404).json({
            success: false,
            error: { code: 'INVOICE_NOT_FOUND', message: `No se encontró comprobante electrónico para el pedido #${orderId}` }
          });
          return;
        }

        res.status(200).json({ success: true, data: rows[0] });
      } else {
        const inv = memoryInvoices.find((i) => i.orderId === orderId);
        if (!inv) {
          res.status(404).json({
            success: false,
            error: { code: 'INVOICE_NOT_FOUND', message: `No se encontró comprobante electrónico para el pedido #${orderId}` }
          });
          return;
        }

        res.status(200).json({ success: true, data: inv });
      }
    } catch (err) {
      next(err);
    }
  }

  /**
   * @route GET /api/invoices/:id/pdf
   * @desc Redirecciona al PDF oficial emitido por el PSE Nubefact
   */
  public static async getPdf(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const id = Number(req.params.id);

      if (isPostgresAvailable()) {
        const { rows } = await dbPool.query(`SELECT pdf_url FROM invoices WHERE id = $1`, [id]);
        if (!rows[0]?.pdf_url) {
          res.status(404).json({ error: { code: 'PDF_NOT_FOUND', message: 'PDF no disponible' } });
          return;
        }
        res.redirect(rows[0].pdf_url);
      } else {
        const inv = memoryInvoices.find((i) => i.id === id);
        if (!inv?.pdfUrl) {
          res.status(404).json({ error: { code: 'PDF_NOT_FOUND', message: 'PDF no disponible' } });
          return;
        }
        res.redirect(inv.pdfUrl);
      }
    } catch (err) {
      next(err);
    }
  }

  /**
   * @route GET /api/invoices/:id/xml
   * @desc Redirecciona al XML firmado digitalmente
   */
  public static async getXml(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const id = Number(req.params.id);

      if (isPostgresAvailable()) {
        const { rows } = await dbPool.query(`SELECT xml_url FROM invoices WHERE id = $1`, [id]);
        if (!rows[0]?.xml_url) {
          res.status(404).json({ error: { code: 'XML_NOT_FOUND', message: 'XML no disponible' } });
          return;
        }
        res.redirect(rows[0].xml_url);
      } else {
        const inv = memoryInvoices.find((i) => i.id === id);
        if (!inv?.xmlUrl) {
          res.status(404).json({ error: { code: 'XML_NOT_FOUND', message: 'XML no disponible' } });
          return;
        }
        res.redirect(inv.xmlUrl);
      }
    } catch (err) {
      next(err);
    }
  }

  /**
   * @route POST /api/orders/:id/credit-note
   * @desc Emite una Nota de Crédito Electrónica vinculada al comprobante original por motivo de reembolso
   */
  /**
   * @route POST /api/orders/:id/credit-note
   * @desc Emite una Nota de Crédito Electrónica vinculada al comprobante original por motivo de reembolso (Catálogo 09 SUNAT)
   */
  public static async emitCreditNote(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const orderId = Number(req.params.id);
      const rawMotivo = req.body?.reasonCode || req.body?.motivo || '01';
      const reasonDescription = req.body?.reasonDescription || req.body?.descripcion || 'Anulación de la operación';

      const ALLOWED_MOTIVOS = ['01', '02', '06', '07', '13'];
      if (!ALLOWED_MOTIVOS.includes(rawMotivo)) {
        res.status(400).json({
          success: false,
          error: {
            code: 'INVALID_MOTIVO',
            message: `El motivo de la nota de crédito '${rawMotivo}' no es válido conforme al Catálogo 09 de SUNAT. Permitidos: ${ALLOWED_MOTIVOS.join(', ')}`
          }
        });
        return;
      }

      let originalInvoice: any = null;

      if (isPostgresAvailable()) {
        const { rows } = await dbPool.query(
          `SELECT id, tipo, serie, numero, monto_total, cliente_denominacion, cliente_tipo_documento, cliente_numero_documento
             FROM invoices
            WHERE order_id = $1 AND tipo IN ('01', '03') AND estado = 'ACEPTADO'
            ORDER BY created_at DESC LIMIT 1`,
          [orderId]
        );
        originalInvoice = rows[0];
      } else {
        originalInvoice = memoryInvoices.find(
          (i) => i.orderId === orderId && ['01', '03'].includes(i.tipo) && i.estado === 'ACEPTADO'
        );
      }

      if (!originalInvoice) {
        res.status(404).json({
          success: false,
          error: {
            code: 'ORIGINAL_INVOICE_NOT_FOUND',
            message: 'No existe un comprobante aceptado para generar la Nota de Crédito de este pedido.'
          }
        });
        return;
      }

      const isFactura = originalInvoice.tipo === '01';
      const serie = isFactura ? 'FC01' : 'BC01';

      let numero: number | undefined;
      let client: any = null;

      if (isPostgresAvailable()) {
        client = await dbPool.connect();
        await client.query('BEGIN');
        const { reserveInvoiceNumber } = await import('../services/sunat/nubefact.service');
        numero = await reserveInvoiceNumber(client, '07', serie);
      }

      try {
        const totalAmountNum = Number(originalInvoice.monto_total || originalInvoice.montoTotal);
        const { splitIgv } = await import('../utils/igv');
        const { subtotal, igv, total: totalAmount } = splitIgv(Math.round(totalAmountNum * 100));

        const ncResult = await NubefactService.emitCreditNote({
          orderId,
          invoiceToModify: {
            tipo: (originalInvoice.tipo as any) || '03',
            serie: originalInvoice.serie,
            numero: originalInvoice.numero,
            totalAmount
          },
          reasonCode: rawMotivo,
          reasonDescription,
          numero,
          clienteDenominacion: originalInvoice.cliente_denominacion || originalInvoice.clienteDenominacion,
          clienteDocTipo: originalInvoice.cliente_tipo_documento || originalInvoice.clienteTipoDocumento || '0',
          clienteDocNumero: originalInvoice.cliente_numero_documento || originalInvoice.clienteNumeroDocumento || '00000000'
        });

        if (client) {
          await client.query(
            `INSERT INTO invoices
               (order_id, tipo, serie, numero, cliente_denominacion,
                monto_subtotal, monto_igv, monto_total, xml_url, pdf_url, cdr_url,
                hash_sunat, estado, referencia_tipo, referencia_serie, referencia_numero, referencia_motivo,
                ref_tipo, ref_serie, ref_numero, motivo_nc)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, 'ACEPTADO', $13, $14, $15, $16, $13, $14, $15, $17)`,
            [
              orderId,
              ncResult.tipo,
              ncResult.serie,
              ncResult.numero,
              originalInvoice.cliente_denominacion,
              subtotal,
              igv,
              totalAmount,
              ncResult.enlace_del_xml,
              ncResult.enlace_del_pdf,
              ncResult.enlace_del_cdr,
              ncResult.codigo_hash,
              originalInvoice.tipo,
              originalInvoice.serie,
              originalInvoice.numero,
              reasonDescription,
              rawMotivo
            ]
          );
          await client.query('COMMIT');
        } else {
          memoryInvoices.push({
            id: memoryInvoices.length + 1,
            orderId,
            tipo: ncResult.tipo,
            serie: ncResult.serie,
            numero: ncResult.numero,
            clienteTipoDocumento: originalInvoice.clienteTipoDocumento || '0',
            clienteNumeroDocumento: originalInvoice.clienteNumeroDocumento || '00000000',
            clienteDenominacion: originalInvoice.clienteDenominacion,
            montoSubtotal: subtotal,
            montoIgv: igv,
            montoTotal: totalAmount,
            moneda: 'PEN',
            xmlUrl: ncResult.enlace_del_xml,
            pdfUrl: ncResult.enlace_del_pdf,
            cdrUrl: ncResult.enlace_del_cdr,
            hashSunat: ncResult.codigo_hash,
            estado: 'ACEPTADO',
            createdAt: new Date()
          });
        }

        logger.info('[SUNAT] Nota de crédito emitida:', {
          orderId,
          nc: `${ncResult.serie}-${ncResult.numero}`
        });

        res.status(200).json({
          success: true,
          data: ncResult
        });
      } catch (innerErr) {
        if (client) await client.query('ROLLBACK').catch(() => {});
        throw innerErr;
      } finally {
        if (client) client.release();
      }
    } catch (err) {
      next(err);
    }
  }
}

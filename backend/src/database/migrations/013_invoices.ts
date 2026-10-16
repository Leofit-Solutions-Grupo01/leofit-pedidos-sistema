/**
 * @file 013_invoices.ts
 * @description Migración 013: Esquema relacional para Comprobantes de Pago Electrónicos (SUNAT / Nubefact).
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration013: Migration = {
  version: '013',
  name: 'invoices',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      CREATE TABLE IF NOT EXISTS invoices (
        id SERIAL PRIMARY KEY,
        order_id INT REFERENCES orders(id) ON DELETE RESTRICT,
        tipo CHAR(2) NOT NULL, -- '01' = Factura, '03' = Boleta de Venta, '07' = Nota de Crédito
        serie CHAR(4) NOT NULL, -- Ej: 'BBB1', 'FFF1', 'FC01', 'BC01'
        numero INT NOT NULL,
        cliente_tipo_documento CHAR(1) NOT NULL DEFAULT '0', -- '1'=DNI, '6'=RUC, '4'=Carnet Ext., '0'=Sin documento
        cliente_numero_documento VARCHAR(20),
        cliente_denominacion VARCHAR(255) NOT NULL,
        cliente_direccion TEXT,
        cliente_email VARCHAR(150),
        monto_subtotal NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
        monto_igv NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
        monto_total NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
        moneda CHAR(3) NOT NULL DEFAULT 'PEN',
        xml_url TEXT,
        pdf_url TEXT,
        cdr_url TEXT,
        hash_sunat VARCHAR(100),
        estado VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE', -- 'PENDIENTE', 'ACEPTADO', 'RECHAZADO', 'ANULADO'
        nubefact_id VARCHAR(100),
        sunat_response JSONB,
        sunat_error TEXT,
        referencia_tipo CHAR(2), -- Para notas de crédito: tipo de comprobante modificado ('01' o '03')
        referencia_serie CHAR(4),
        referencia_numero INT,
        referencia_motivo VARCHAR(255),
        created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT uq_invoices_tipo_serie_numero UNIQUE (tipo, serie, numero),
        CONSTRAINT chk_invoice_estado CHECK (estado IN ('PENDIENTE', 'ACEPTADO', 'RECHAZADO', 'ANULADO'))
      );

      CREATE INDEX IF NOT EXISTS idx_invoices_order_id ON invoices(order_id);
      CREATE INDEX IF NOT EXISTS idx_invoices_tipo_serie ON invoices(tipo, serie, numero);
      CREATE INDEX IF NOT EXISTS idx_invoices_estado ON invoices(estado);
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query(`
      DROP TABLE IF EXISTS invoices CASCADE;
    `);
  }
};

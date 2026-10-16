/**
 * @file 015_invoice_series.ts
 * @description Migración 015: Control atómico de correlativos fiscales sin huecos (evita multas SUNAT),
 * tracking de resúmenes diarios de boletas (RC) y referencias de notas de crédito (Catálogo 09).
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration015: Migration = {
  version: '015',
  name: 'invoice_series_and_daily_summary',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      CREATE TABLE IF NOT EXISTS invoice_series (
        tipo CHAR(2) NOT NULL,
        serie VARCHAR(4) NOT NULL,
        last_number INT NOT NULL DEFAULT 0,
        PRIMARY KEY (tipo, serie)
      );

      INSERT INTO invoice_series (tipo, serie, last_number)
      VALUES 
        ('01', 'FFF1', 0),
        ('03', 'BBB1', 0),
        ('07', 'FC01', 0),
        ('07', 'BC01', 0)
      ON CONFLICT DO NOTHING;

      ALTER TABLE invoices
        ADD COLUMN IF NOT EXISTS resumen_enviado_at TIMESTAMPTZ,
        ADD COLUMN IF NOT EXISTS resumen_ticket TEXT,
        ADD COLUMN IF NOT EXISTS ref_tipo CHAR(2),
        ADD COLUMN IF NOT EXISTS ref_serie VARCHAR(4),
        ADD COLUMN IF NOT EXISTS ref_numero INT,
        ADD COLUMN IF NOT EXISTS motivo_nc CHAR(2);

      CREATE INDEX IF NOT EXISTS idx_invoices_resumen_boletas 
        ON invoices (tipo, estado, resumen_enviado_at)
        WHERE tipo = '03' AND estado = 'ACEPTADO';
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query(`
      DROP TABLE IF EXISTS invoice_series CASCADE;
      ALTER TABLE invoices
        DROP COLUMN IF EXISTS resumen_enviado_at,
        DROP COLUMN IF EXISTS resumen_ticket,
        DROP COLUMN IF EXISTS ref_tipo,
        DROP COLUMN IF EXISTS ref_serie,
        DROP COLUMN IF EXISTS ref_numero,
        DROP COLUMN IF EXISTS motivo_nc;
    `);
  }
};

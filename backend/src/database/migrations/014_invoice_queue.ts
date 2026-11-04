/**
 * @file 014_invoice_queue.ts
 * @description Migración 014: Cola asíncrona y transaccional de emisión de comprobantes SUNAT con reintentos exponenciales.
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration014: Migration = {
  version: '014',
  name: 'invoice_queue',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      CREATE TABLE IF NOT EXISTS invoice_queue (
        id SERIAL PRIMARY KEY,
        order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
        tipo CHAR(2) NOT NULL DEFAULT '03', -- '01'=Factura, '03'=Boleta, '07'=Nota de Crédito
        estado VARCHAR(20) NOT NULL DEFAULT 'PENDING',
        attempts INT NOT NULL DEFAULT 0,
        max_attempts INT NOT NULL DEFAULT 5,
        next_attempt_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_error TEXT,
        payload JSONB,
        created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT chk_invoice_queue_estado CHECK (estado IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED'))
      );

      CREATE INDEX IF NOT EXISTS idx_invoice_queue_pending
        ON invoice_queue(estado, next_attempt_at)
        WHERE estado IN ('PENDING', 'PROCESSING');

      CREATE INDEX IF NOT EXISTS idx_invoice_queue_order
        ON invoice_queue(order_id);
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query(`
      DROP TABLE IF EXISTS invoice_queue CASCADE;
    `);
  }
};

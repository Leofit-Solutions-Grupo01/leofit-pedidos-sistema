/**
 * @file 009_payments.ts
 * @description Migración 009: Tabla de pagos con cargos de proveedores y deduplicación.
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration009: Migration = {
  version: '009',
  name: 'payments',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      CREATE TABLE IF NOT EXISTS payments (
        id             BIGSERIAL PRIMARY KEY,
        order_id       INT NOT NULL REFERENCES orders(id) ON DELETE RESTRICT,
        provider       VARCHAR(30) NOT NULL,         -- 'culqi' | 'niubiz' | 'mercadopago' | 'manual'
        provider_charge_id TEXT NOT NULL,            -- id del cargo en el proveedor
        amount_cents   BIGINT NOT NULL CHECK (amount_cents > 0),
        currency       CHAR(3) NOT NULL DEFAULT 'PEN',
        status         VARCHAR(20) NOT NULL,         -- 'PENDING' | 'PAID' | 'FAILED' | 'REFUNDED'
        raw_response   JSONB,
        created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        UNIQUE (provider, provider_charge_id)
      );

      CREATE INDEX IF NOT EXISTS idx_payments_order ON payments(order_id);
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query('DROP TABLE IF EXISTS payments;');
  }
};

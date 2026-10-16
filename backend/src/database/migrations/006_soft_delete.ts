/**
 * @file 006_soft_delete.ts
 * @description Migración 006: Soporte para Soft Delete en productos y órdenes con 410 GONE.
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration006: Migration = {
  version: '006',
  name: 'soft_delete',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      ALTER TABLE products ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;
      ALTER TABLE orders   ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;

      CREATE INDEX IF NOT EXISTS idx_products_active
        ON products(id) WHERE deleted_at IS NULL;
      CREATE INDEX IF NOT EXISTS idx_orders_active
        ON orders(id) WHERE deleted_at IS NULL;
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query(`
      DROP INDEX IF EXISTS idx_products_active;
      DROP INDEX IF EXISTS idx_orders_active;
      ALTER TABLE products DROP COLUMN IF EXISTS deleted_at;
      ALTER TABLE orders   DROP COLUMN IF EXISTS deleted_at;
    `);
  }
};

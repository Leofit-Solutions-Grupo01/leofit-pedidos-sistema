import { PoolClient } from 'pg';
import { Migration } from './types';

export const migration002: Migration = {
  version: '20261016_002',
  name: 'add_shipping_logistics_fields',
  async up(client: PoolClient): Promise<void> {
    await client.query(`
      ALTER TABLE orders ADD COLUMN IF NOT EXISTS shipping_type VARCHAR(20) DEFAULT 'LIMA';
      ALTER TABLE orders ADD COLUMN IF NOT EXISTS destination_city VARCHAR(100) DEFAULT NULL;
      ALTER TABLE orders ADD COLUMN IF NOT EXISTS shipping_agency VARCHAR(50) DEFAULT NULL;
      ALTER TABLE orders ADD COLUMN IF NOT EXISTS tracking_number VARCHAR(50) DEFAULT NULL;

      -- Backfill seguro de registros históricos
      UPDATE orders SET shipping_type = 'LIMA' WHERE shipping_type IS NULL;
    `);
  }
};

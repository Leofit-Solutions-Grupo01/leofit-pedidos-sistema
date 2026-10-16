/**
 * @file 011_payments_orphan_status.ts
 * @description Migración 011: Soporte para estados PAID_ORPHAN y REFUND_PENDING en payments.
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration011: Migration = {
  version: '011',
  name: 'payments_orphan_status',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      ALTER TABLE payments DROP CONSTRAINT IF EXISTS chk_payments_status;
      ALTER TABLE payments DROP CONSTRAINT IF EXISTS payments_status_check;

      ALTER TABLE payments
        ADD CONSTRAINT chk_payments_status CHECK (status IN (
          'PENDING','PAID','FAILED','REFUNDED','PAID_ORPHAN','REFUND_PENDING'
        ));
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query(`ALTER TABLE payments DROP CONSTRAINT IF EXISTS chk_payments_status;`);
  }
};

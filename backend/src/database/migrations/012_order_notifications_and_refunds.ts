/**
 * @file 012_order_notifications_and_refunds.ts
 * @description Migración 012: Soporte para idempotencia en notificaciones al cliente y tracking de reembolsos parciales.
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration012: Migration = {
  version: '012',
  name: 'order_notifications_and_refunds',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      -- 1. Idempotencia en notificaciones post-pago
      ALTER TABLE orders
        ADD COLUMN IF NOT EXISTS notified_at TIMESTAMPTZ;

      -- 2. Soporte para tracking de reembolsos parciales y clave de idempotencia del reembolso
      ALTER TABLE payments
        ADD COLUMN IF NOT EXISTS refunded_amount_cents BIGINT DEFAULT 0,
        ADD COLUMN IF NOT EXISTS refund_idempotency_key VARCHAR(120);

      CREATE INDEX IF NOT EXISTS idx_payments_refund_idempotency
        ON payments(refund_idempotency_key) WHERE refund_idempotency_key IS NOT NULL;
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query(`
      DROP INDEX IF EXISTS idx_payments_refund_idempotency;
      ALTER TABLE payments
        DROP COLUMN IF EXISTS refund_idempotency_key,
        DROP COLUMN IF EXISTS refunded_amount_cents;
      ALTER TABLE orders
        DROP COLUMN IF EXISTS notified_at;
    `);
  }
};

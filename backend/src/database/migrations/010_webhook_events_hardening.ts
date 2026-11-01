/**
 * @file 010_webhook_events_hardening.ts
 * @description Migración 010: Hardening de eventos de webhook, reconciliación y normalización de total_cents en pedidos.
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration010: Migration = {
  version: '010',
  name: 'webhook_events_hardening',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      -- 1. Normalización de montos y divisas en la cabecera del pedido para validación estricta
      ALTER TABLE orders
        ADD COLUMN IF NOT EXISTS total_cents BIGINT,
        ADD COLUMN IF NOT EXISTS currency CHAR(3) NOT NULL DEFAULT 'PEN';

      UPDATE orders
        SET total_cents = ROUND(total_amount * 100)
      WHERE total_cents IS NULL;

      -- 2. Hardening del estado y trazabilidad de eventos de webhooks
      ALTER TABLE webhook_events
        ADD COLUMN IF NOT EXISTS status        VARCHAR(20) NOT NULL DEFAULT 'RECEIVED',
        ADD COLUMN IF NOT EXISTS processed_at  TIMESTAMPTZ,
        ADD COLUMN IF NOT EXISTS error_message TEXT,
        ADD COLUMN IF NOT EXISTS attempts      INT NOT NULL DEFAULT 0;

      ALTER TABLE webhook_events
        DROP CONSTRAINT IF EXISTS chk_webhook_status;

      ALTER TABLE webhook_events
        ADD CONSTRAINT chk_webhook_status CHECK (status IN (
          'RECEIVED','PROCESSED','IGNORED','FAILED'
        ));

      CREATE INDEX IF NOT EXISTS idx_webhook_status_created
        ON webhook_events(status, created_at DESC);

      -- 3. Campos para auditoría de reconciliación de pagos pendientes
      ALTER TABLE payments
        ADD COLUMN IF NOT EXISTS reconciled_at TIMESTAMPTZ,
        ADD COLUMN IF NOT EXISTS reconcile_note TEXT;

      CREATE INDEX IF NOT EXISTS idx_payments_pending_order
        ON payments(order_id, created_at DESC) WHERE status = 'PENDING';
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query(`
      DROP INDEX IF EXISTS idx_payments_pending_order;
      ALTER TABLE payments DROP COLUMN IF EXISTS reconcile_note;
      ALTER TABLE payments DROP COLUMN IF EXISTS reconciled_at;

      DROP INDEX IF EXISTS idx_webhook_status_created;
      ALTER TABLE webhook_events DROP CONSTRAINT IF EXISTS chk_webhook_status;
      ALTER TABLE webhook_events
        DROP COLUMN IF EXISTS status,
        DROP COLUMN IF EXISTS processed_at,
        DROP COLUMN IF EXISTS error_message,
        DROP COLUMN IF EXISTS attempts;

      ALTER TABLE orders
        DROP COLUMN IF EXISTS total_cents,
        DROP COLUMN IF EXISTS currency;
    `);
  }
};

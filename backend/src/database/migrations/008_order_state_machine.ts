/**
 * @file 008_order_state_machine.ts
 * @description Migración 008: Máquina de estados formal del pedido y auditoría de transiciones.
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration008: Migration = {
  version: '008',
  name: 'order_state_machine',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      ALTER TABLE orders
        ADD COLUMN IF NOT EXISTS estado VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',
        ADD COLUMN IF NOT EXISTS paid_at     TIMESTAMPTZ,
        ADD COLUMN IF NOT EXISTS shipped_at  TIMESTAMPTZ,
        ADD COLUMN IF NOT EXISTS delivered_at TIMESTAMPTZ,
        ADD COLUMN IF NOT EXISTS cancelled_at TIMESTAMPTZ,
        ADD COLUMN IF NOT EXISTS cancel_reason TEXT;

      ALTER TABLE orders
        DROP CONSTRAINT IF EXISTS chk_orders_estado;

      ALTER TABLE orders
        ADD CONSTRAINT chk_orders_estado CHECK (estado IN (
          'PENDIENTE','PAGADO','PREPARACION','EN_CAMINO','ENTREGADO','CANCELADO','REEMBOLSADO'
        ));

      -- Transiciones válidas y auditoría formal de negocio
      CREATE TABLE IF NOT EXISTS order_state_transitions (
        id         BIGSERIAL PRIMARY KEY,
        order_id   INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
        from_state VARCHAR(20),
        to_state   VARCHAR(20) NOT NULL,
        actor      VARCHAR(50) NOT NULL,     -- 'system', 'admin:<id>', 'webhook:<provider>'
        metadata   JSONB,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );

      CREATE INDEX IF NOT EXISTS idx_ost_order ON order_state_transitions(order_id, created_at DESC);
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query(`
      DROP TABLE IF EXISTS order_state_transitions;
      ALTER TABLE orders DROP CONSTRAINT IF EXISTS chk_orders_estado;
      ALTER TABLE orders
        DROP COLUMN IF EXISTS estado,
        DROP COLUMN IF EXISTS paid_at,
        DROP COLUMN IF EXISTS shipped_at,
        DROP COLUMN IF EXISTS delivered_at,
        DROP COLUMN IF EXISTS cancelled_at,
        DROP COLUMN IF EXISTS cancel_reason;
    `);
  }
};

/**
 * @file 007_webhook_events.ts
 * @description Migración 007: Tabla de eventos de webhooks con deduplicación e idempotencia.
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration007: Migration = {
  version: '007',
  name: 'webhook_events',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      CREATE TABLE IF NOT EXISTS webhook_events (
        id           BIGSERIAL PRIMARY KEY,
        provider     VARCHAR(64) NOT NULL,
        event_id     VARCHAR(255) NOT NULL,
        payload      JSONB NOT NULL,
        processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        CONSTRAINT uq_webhook_provider_event UNIQUE (provider, event_id)
      );

      CREATE INDEX IF NOT EXISTS idx_webhook_provider_event
        ON webhook_events(provider, event_id);
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query('DROP TABLE IF EXISTS webhook_events;');
  }
};

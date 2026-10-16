/**
 * @file 005_audit_log.ts
 * @description Migración 005: Registro de auditoría administrativa (OWASP A09).
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration005: Migration = {
  version: '005',
  name: 'audit_log',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      CREATE TABLE IF NOT EXISTS audit_log (
        id             BIGSERIAL PRIMARY KEY,
        user_id        INT REFERENCES users(id) ON DELETE SET NULL,
        action         VARCHAR(64) NOT NULL,
        resource_type  VARCHAR(64) NOT NULL,
        resource_id    TEXT,
        before_state   JSONB,
        after_state    JSONB,
        ip             INET,
        user_agent     TEXT,
        correlation_id TEXT,
        created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );

      CREATE INDEX IF NOT EXISTS idx_audit_user_created
        ON audit_log(user_id, created_at DESC);
      CREATE INDEX IF NOT EXISTS idx_audit_resource
        ON audit_log(resource_type, resource_id);
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query('DROP TABLE IF EXISTS audit_log;');
  }
};

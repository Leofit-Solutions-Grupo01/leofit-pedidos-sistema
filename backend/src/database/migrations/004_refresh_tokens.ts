/**
 * @file 004_refresh_tokens.ts
 * @description Migración 004: Tabla de refresh tokens con soporte para rotación y detección de reuso por familias.
 */

import type { PoolClient } from 'pg';
import { Migration } from './types';

export const migration004: Migration = {
  version: '004',
  name: 'refresh_tokens',

  async up(client: PoolClient): Promise<void> {
    await client.query(`
      CREATE TABLE IF NOT EXISTS refresh_tokens (
        id           BIGSERIAL PRIMARY KEY,
        user_id      INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        token_hash   CHAR(64) NOT NULL UNIQUE,
        family_id    UUID NOT NULL DEFAULT gen_random_uuid(),
        expires_at   TIMESTAMPTZ NOT NULL,
        revoked_at   TIMESTAMPTZ,
        replaced_by  BIGINT REFERENCES refresh_tokens(id),
        user_agent   TEXT,
        ip           INET,
        created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );

      CREATE INDEX IF NOT EXISTS idx_refresh_active
        ON refresh_tokens(user_id) WHERE revoked_at IS NULL;
      CREATE INDEX IF NOT EXISTS idx_refresh_family
        ON refresh_tokens(family_id);
    `);
  },

  async down(client: PoolClient): Promise<void> {
    await client.query('DROP TABLE IF EXISTS refresh_tokens;');
  }
};

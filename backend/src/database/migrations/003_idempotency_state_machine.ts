import { PoolClient } from 'pg';
import { Migration } from './types';

export const migration003: Migration = {
  version: '20261016_003',
  name: 'idempotency_state_machine_and_locks',
  async up(client: PoolClient): Promise<void> {
    await client.query(`
      CREATE TABLE IF NOT EXISTS idempotency_keys (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL DEFAULT 0,
        key VARCHAR(128) NOT NULL,
        request_hash VARCHAR(64) DEFAULT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
        status_code INT NOT NULL DEFAULT 0,
        response_body JSONB NOT NULL DEFAULT '{}'::jsonb,
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        locked_until TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP + INTERVAL '30 seconds'),
        expires_at TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP + INTERVAL '48 hours')
      );

      ALTER TABLE idempotency_keys ADD COLUMN IF NOT EXISTS user_id INT NOT NULL DEFAULT 0;
      ALTER TABLE idempotency_keys ADD COLUMN IF NOT EXISTS request_hash VARCHAR(64) DEFAULT NULL;
      ALTER TABLE idempotency_keys ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'PENDING';
      ALTER TABLE idempotency_keys ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;
      ALTER TABLE idempotency_keys ADD COLUMN IF NOT EXISTS locked_until TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP + INTERVAL '30 seconds');
      ALTER TABLE idempotency_keys ADD COLUMN IF NOT EXISTS expires_at TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP + INTERVAL '48 hours');

      CREATE UNIQUE INDEX IF NOT EXISTS idx_user_idempotency_key ON idempotency_keys(user_id, key);
      CREATE INDEX IF NOT EXISTS idx_idempotency_expires_at ON idempotency_keys(expires_at);
      CREATE INDEX IF NOT EXISTS idx_idempotency_status ON idempotency_keys(status);

      DELETE FROM idempotency_keys WHERE expires_at < CURRENT_TIMESTAMP;
    `);
  }
};

/**
 * @file runner.ts
 * @description Ejecutor transaccional de migraciones versionadas (ACID).
 */

import { dbPool, isPostgresAvailable } from '../../config/database';
import { migration001 } from './001_initial_schema';
import { migration002 } from './002_add_shipping_fields';
import { migration003 } from './003_idempotency_state_machine';
import { Migration } from './types';
import { logger } from '../../utils/logger';

const MIGRATIONS: Migration[] = [
  migration001,
  migration002,
  migration003
];

export async function runVersionedMigrations(): Promise<void> {
  if (!isPostgresAvailable()) {
    logger.info('[Migration Runner] PostgreSQL no conectado. Omitiendo migraciones de base de datos.');
    return;
  }

  let client: any = null;
  try {
    client = await dbPool.connect();

    // 1. Crear tabla de control de versiones de esquema si no existe
    await client.query(`
      CREATE TABLE IF NOT EXISTS schema_migrations (
        version VARCHAR(64) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        applied_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 2. Obtener lista de migraciones ya aplicadas
    const { rows } = await client.query('SELECT version FROM schema_migrations');
    const appliedVersions = new Set(rows.map((r: any) => r.version));

    // 3. Aplicar migraciones pendientes en orden secuencial estricto
    for (const migration of MIGRATIONS) {
      if (!appliedVersions.has(migration.version)) {
        logger.info(`[Migration Runner] Aplicando migración versionada: ${migration.version} - ${migration.name}...`);
        
        await client.query('BEGIN');
        try {
          await migration.up(client);
          await client.query(
            'INSERT INTO schema_migrations (version, name) VALUES ($1, $2)',
            [migration.version, migration.name]
          );
          await client.query('COMMIT');
          logger.info(`[Migration Runner] ✅ Migración ${migration.version} aplicada exitosamente.`);
        } catch (err: any) {
          await client.query('ROLLBACK');
          logger.error(`[Migration Runner] ❌ Falló la migración ${migration.version}. Rollback ejecutado.`, { error: err.message });
          throw err;
        }
      }
    }

    logger.info('[Migration Runner] Todas las migraciones versionadas están al día.');
  } catch (error: any) {
    logger.error('[Migration Runner Error] No se pudieron completar las migraciones versionadas:', { error: error.message });
  } finally {
    if (client) {
      client.release();
    }
  }
}

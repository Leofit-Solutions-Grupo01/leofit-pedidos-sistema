/**
 * @file runner.ts
 * @description Ejecutor transaccional de migraciones versionadas (ACID) con Advisory Lock global.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import { dbPool, isPostgresAvailable } from '../../config/database';
import { migration001 } from './001_initial_schema';
import { migration002 } from './002_add_shipping_fields';
import { migration003 } from './003_idempotency_state_machine';
import { migration004 } from './004_refresh_tokens';
import { migration005 } from './005_audit_log';
import { migration006 } from './006_soft_delete';
import { migration007 } from './007_webhook_events';
import { Migration } from './types';
import { logger } from '../../utils/logger';

const RUNNER_LOCK_ID = 728394756; // Identificador unívoco para serializar arranques multi-instancia en Render

const MIGRATIONS: Migration[] = [
  migration001,
  migration002,
  migration003,
  migration004,
  migration005,
  migration006,
  migration007
];

export async function runVersionedMigrations(): Promise<void> {
  if (!isPostgresAvailable()) {
    logger.info('[Migration Runner] PostgreSQL no conectado. Omitiendo migraciones de base de datos.');
    return;
  }

  let client: any = null;
  try {
    client = await dbPool.connect();

    // 1. Serializar ejecuciones concurrentes entre réplicas con advisory lock global
    await client.query('SELECT pg_advisory_lock($1)', [RUNNER_LOCK_ID]);

    // 2. Crear tabla de control de versiones de esquema si no existe
    await client.query(`
      CREATE TABLE IF NOT EXISTS schema_migrations (
        version VARCHAR(64) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        applied_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 3. Obtener lista de migraciones ya aplicadas
    const { rows } = await client.query('SELECT version FROM schema_migrations');
    const appliedVersions = new Set(rows.map((r: any) => r.version));

    // 4. Aplicar migraciones pendientes ordenadas por versión
    const sorted = [...MIGRATIONS].sort((a, b) => a.version.localeCompare(b.version));
    for (const migration of sorted) {
      if (!appliedVersions.has(migration.version)) {
        logger.info(`[Migration Runner] Aplicando migración: ${migration.version} - ${migration.name}...`);
        
        const needsNoTx = migration.noTransaction === true;
        if (!needsNoTx) await client.query('BEGIN');

        try {
          await migration.up(client);
          await client.query(
            'INSERT INTO schema_migrations (version, name) VALUES ($1, $2)',
            [migration.version, migration.name]
          );
          if (!needsNoTx) await client.query('COMMIT');
          logger.info(`[Migration Runner] ✅ Migración ${migration.version} aplicada exitosamente.`);
        } catch (err: any) {
          if (!needsNoTx) await client.query('ROLLBACK').catch(() => {});
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
      await client.query('SELECT pg_advisory_unlock($1)', [RUNNER_LOCK_ID]).catch(() => {});
      client.release();
    }
  }
}

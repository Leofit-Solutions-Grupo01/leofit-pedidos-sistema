/**
 * @file autoMigrate.ts
 * @description Auto-migrador de esquema seguro e idempotente para PostgreSQL en entornos Cloud (Render/Supabase).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Función:
 * - Asegura la existencia de columnas de logística incorporadas en versiones recientes.
 * - Evita errores de base de datos SQLSTATE 42703 (undefined_column) que provocan HTTP 500 en producción.
 * - Garantiza la existencia de secuencias y métodos de pago esenciales.
 */

import { dbPool } from '../config/database';

export async function runAutoMigrations(): Promise<void> {
  let client;
  try {
    client = await dbPool.connect();
    console.log('🔄 [AutoMigrate] Verificando compatibilidad de esquema PostgreSQL en producción...');

    // 1. Columnas de logística dual en tabla orders
    await client.query(`
      ALTER TABLE orders ADD COLUMN IF NOT EXISTS shipping_type VARCHAR(20) DEFAULT NULL;
      ALTER TABLE orders ADD COLUMN IF NOT EXISTS destination_city VARCHAR(100) DEFAULT NULL;
      ALTER TABLE orders ADD COLUMN IF NOT EXISTS shipping_agency VARCHAR(50) DEFAULT NULL;
      ALTER TABLE orders ADD COLUMN IF NOT EXISTS tracking_number VARCHAR(50) DEFAULT NULL;
    `);

    // 2. Secuencia para correlativo de pedidos si no existe
    await client.query(`
      CREATE SEQUENCE IF NOT EXISTS order_number_seq;
    `);

    // 3. Catálogo esencial de distritos (fallback)
    await client.query(`
      INSERT INTO districts (id, name) VALUES (1, 'Lima')
      ON CONFLICT (id) DO NOTHING;
    `);

    // 4. Métodos de pago normalizados
    await client.query(`
      INSERT INTO payment_methods (id, code, name) VALUES
        (1, 'YAPE',           'Yape'),
        (2, 'PLIN',           'Plin'),
        (3, 'TRANSFERENCIA',  'Transferencia Bancaria'),
        (4, 'CONTRAENTREGA',  'Contraentrega en Efectivo'),
        (5, 'EFECTIVO',       'Efectivo Directo')
      ON CONFLICT (id) DO UPDATE SET code = EXCLUDED.code, name = EXCLUDED.name;
    `);

    // 5. Ajustar secuencia de payment_methods si existe
    try {
      await client.query(`
        SELECT setval('payment_methods_id_seq', (SELECT GREATEST(COALESCE(MAX(id), 1), 5) FROM payment_methods));
      `);
    } catch {
      // Ignorar si la secuencia tiene otro nombre
    }

    // 6. Tabla de llaves de idempotencia para prevenir órdenes duplicadas por timeout / reintentos
    await client.query(`
      CREATE TABLE IF NOT EXISTS idempotency_keys (
        key VARCHAR(128) PRIMARY KEY,
        status_code INT NOT NULL,
        response_body JSONB NOT NULL,
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
      );
      CREATE INDEX IF NOT EXISTS idx_idempotency_created_at ON idempotency_keys(created_at);
    `);

    console.log('✅ [AutoMigrate] Esquema verificado y sincronizado correctamente sin inconsistencias.');
  } catch (error) {
    console.error('⚠️ [AutoMigrate Warning] No se pudieron aplicar todas las migraciones automáticas:', error);
  } finally {
    if (client) {
      client.release();
    }
  }
}

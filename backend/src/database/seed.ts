// =============================================================================
// DATABASE SEEDING UTILITY (POSTGRESQL & CLI RUNNER)
// =============================================================================

import fs from 'fs';
import path from 'path';
import { dbPool, checkDatabaseConnection } from '../config/database';

async function runSeed() {
  console.log('🌱 Ejecutando migración y sembrado de datos Leofit Solutions...');

  const isConnected = await checkDatabaseConnection();
  if (!isConnected) {
    console.log('ℹ️ PostgreSQL no está disponible localmente. Los datos se mantienen en el Almacén Transaccional en memoria para pruebas y desarrollo.');
    process.exit(0);
  }

  const schemaPath = path.resolve(__dirname, '../../../database/schema.sql');
  const seedsPath = path.resolve(__dirname, '../../../database/seeds.sql');

  const schemaSql = fs.readFileSync(schemaPath, 'utf-8');
  const seedsSql = fs.readFileSync(seedsPath, 'utf-8');

  const client = await dbPool.connect();
  try {
    console.log('⚙️ Creando tablas de esquema DDL...');
    await client.query(schemaSql);
    console.log('✅ Tablas y relaciones creadas exitosamente.');

    console.log('📦 Insertando datos iniciales DML...');
    await client.query(seedsSql);
    console.log('✅ Datos de prueba insertados satisfactoriamente.');
  } catch (error) {
    console.error('❌ Error durante la ejecución del seed:', error);
  } finally {
    client.release();
    await dbPool.end();
  }
}

runSeed();

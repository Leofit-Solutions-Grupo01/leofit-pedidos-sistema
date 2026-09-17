// =============================================================================
// DATABASE CONFIGURATION & CONNECTION POOL - POSTGRESQL (PG)
// =============================================================================

import { Pool, PoolConfig } from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const isProduction = process.env.NODE_ENV === 'production';

const poolConfig: PoolConfig = process.env.DATABASE_URL
  ? {
      connectionString: process.env.DATABASE_URL,
      ssl: process.env.DB_SSL === 'true' ? { rejectUnauthorized: false } : undefined,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 5000,
    }
  : {
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432', 10),
      user: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASSWORD || 'postgres',
      database: process.env.DB_NAME || 'leofit_db',
      ssl: process.env.DB_SSL === 'true' ? { rejectUnauthorized: false } : undefined,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 5000,
    };

export const dbPool = new Pool(poolConfig);

let isPgConnected = false;

export async function checkDatabaseConnection(): Promise<boolean> {
  try {
    const client = await dbPool.connect();
    await client.query('SELECT 1');
    client.release();
    isPgConnected = true;
    console.log('✅ Conexión exitosa al clúster PostgreSQL / Supabase.');
    return true;
  } catch (error) {
    console.warn('⚠️ No se detectó instancia activa de PostgreSQL local. Activando Almacén Transaccional en Memoria (Repository Pattern Fallback).');
    isPgConnected = false;
    return false;
  }
}

export function isPostgresAvailable(): boolean {
  return isPgConnected;
}

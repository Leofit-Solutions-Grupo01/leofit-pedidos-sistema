// =============================================================================
// DATABASE CONFIGURATION & CONNECTION POOL - POSTGRESQL (PG)
// =============================================================================

import { Pool, PoolConfig } from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const isProduction = process.env.NODE_ENV === 'production';

const rawDatabaseUrl = process.env.DATABASE_URL?.trim().replace(/^["']|["']$/g, '');

const requiresSsl =
  process.env.DB_SSL === 'true' ||
  (rawDatabaseUrl
    ? /sslmode=require|neon\.tech|supabase\.co|render\.com/i.test(rawDatabaseUrl)
    : false);

const normalizedConnectionString = rawDatabaseUrl
  ? rawDatabaseUrl
      .replace(/([?&])channel_binding=require(&|$)/i, '$1')
      .replace(/[?&]$/, '')
  : undefined;

const poolConfig: PoolConfig = normalizedConnectionString
  ? {
      connectionString: normalizedConnectionString,
      ssl: requiresSsl ? { rejectUnauthorized: false } : undefined,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 15000,
    }
  : {
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432', 10),
      user: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASSWORD || 'postgres',
      database: process.env.DB_NAME || 'leofit_db',
      ssl: requiresSsl ? { rejectUnauthorized: false } : undefined,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 15000,
    };

export const dbPool = new Pool(poolConfig);

let isPgConnected = false;

// Evita caídas del proceso si la instancia de PostgreSQL (ej. Render Free Tier / Neon Serverless) cierra conexiones inactivas
dbPool.on('error', (err) => {
  console.warn('⚠️ Conexión PostgreSQL interrumpida en runtime. Conmutando a Almacén Transaccional en Memoria (Fallback):', err.message);
  isPgConnected = false;
});

export async function checkDatabaseConnection(): Promise<boolean> {
  try {
    const client = await dbPool.connect();
    await client.query('SELECT 1');
    client.release();
    isPgConnected = true;
    console.log('✅ Conexión exitosa al clúster PostgreSQL (Neon / Render / Supabase).');
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

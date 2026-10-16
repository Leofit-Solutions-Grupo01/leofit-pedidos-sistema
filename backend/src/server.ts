// =============================================================================
// SERVER ENTRY POINT - LEOFIT SOLUTIONS
// =============================================================================

import { createApp } from './app';
import { checkDatabaseConnection, isPostgresAvailable, dbPool } from './config/database';
import { runAutoMigrations } from './database/autoMigrate';
import { logger } from './utils/logger';

const PORT = parseInt(process.env.PORT || '4000', 10);
// Ventana de draining: 20s en producción para permitir que Render/LB actualicen health checks (10-15s interval)
const DRAIN_TIMEOUT_MS = parseInt(process.env.DRAIN_TIMEOUT_MS || (process.env.NODE_ENV === 'test' ? '100' : '20000'), 10);

async function startServer() {
  console.log('🚀 Iniciando Leofit Backend Server...');
  await checkDatabaseConnection();

  if (isPostgresAvailable()) {
    await runAutoMigrations();
  }

  let isDraining = false;
  const app = createApp(() => isDraining);

  const server = app.listen(PORT, () => {
    console.log(`\n=============================================================`);
    console.log(`✅ Servidor API REST activo en: http://localhost:${PORT}`);
    console.log(`📡 Health Check & Métricas:     http://localhost:${PORT}/api/health`);
    console.log(`🔒 Módulo Auth:                http://localhost:${PORT}/api/auth`);
    console.log(`📦 Módulo Pedidos:             http://localhost:${PORT}/api/orders`);
    console.log(`👕 Módulo Productos:           http://localhost:${PORT}/api/products`);
    console.log(`=============================================================\n`);
  });

  // Graceful Shutdown & Connection Draining (cero 502/503 en despliegues)
  const gracefulShutdown = (signal: string) => {
    if (isDraining) return;
    isDraining = true;
    logger.warn(`[${signal}] Iniciando ciclo de apagado seguro. Instancia en modo DRAINING.`);
    console.log(`\n🛑 [${signal}] Instancia en modo DRAINING (/health/ready responde 503, Connection: close).`);
    console.log(`⏳ Manteniendo sockets activos durante ${DRAIN_TIMEOUT_MS / 1000}s para retiro limpio del Load Balancer...`);

    // Durante DRAIN_TIMEOUT_MS el servidor sigue respondiendo a peticiones en vuelo,
    // pero devuelve 503 en /health/ready y Connection: close para desviar tráfico nuevo.
    setTimeout(() => {
      server.close(async () => {
        console.log('🔒 Servidor HTTP cerrado. Drenaje de solicitudes completado.');
        try {
          await dbPool.end();
          console.log('✅ Pool de conexiones PostgreSQL liberado exitosamente.');
          process.exit(0);
        } catch (err: any) {
          console.error('❌ Error liberando pool de base de datos:', err);
          process.exit(1);
        }
      });
    }, DRAIN_TIMEOUT_MS);

    // Timeout de seguridad final (35s)
    setTimeout(() => {
      console.warn('⏰ Timeout de apagado forzado alcanzado (35s). Saliendo del proceso.');
      process.exit(1);
    }, DRAIN_TIMEOUT_MS + 15000).unref();
  };

  process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
  process.on('SIGINT', () => gracefulShutdown('SIGINT'));
}

startServer().catch(err => {
  console.error('Fatal error al iniciar el servidor:', err);
  process.exit(1);
});

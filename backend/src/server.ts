// =============================================================================
// SERVER ENTRY POINT - LEOFIT SOLUTIONS
// =============================================================================

import { createApp } from './app';
import { checkDatabaseConnection, isPostgresAvailable, dbPool } from './config/database';
import { runVersionedMigrations } from './database/migrations/runner';
import { startReconciliationJob } from './jobs/reconcilePayments';
import { logger } from './utils/logger';

const PORT = parseInt(process.env.PORT || '4000', 10);
// Ventana de draining: 15s en producción (Render otorga 30s de grace period antes de SIGKILL)
const DRAIN_TIMEOUT_MS = parseInt(process.env.DRAIN_TIMEOUT_MS || (process.env.NODE_ENV === 'test' ? '100' : '15000'), 10);
const FORCE_KILL_TIMEOUT_MS = parseInt(process.env.FORCE_KILL_TIMEOUT_MS || '25000', 10);

async function startServer() {
  console.log('🚀 Iniciando Leofit Backend Server...');
  await checkDatabaseConnection();

  if (isPostgresAvailable()) {
    await runVersionedMigrations();
  }

  // Arrancar job de reconciliación periódica de pagos pendientes
  startReconciliationJob();

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
    console.log(`\n🛑 [${signal}] Instancia en modo DRAINING (/health responde 503, Connection: close).`);
    console.log(`⏳ Manteniendo sockets activos durante ${DRAIN_TIMEOUT_MS / 1000}s para retiro limpio del Load Balancer...`);

    // Durante DRAIN_TIMEOUT_MS el servidor sigue respondiendo a peticiones en vuelo,
    // pero devuelve 503 en /health y Connection: close para desviar tráfico nuevo.
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

    // Timeout de seguridad forzado (25s): strictly < 30s de Render SIGKILL
    setTimeout(() => {
      console.warn(`⏰ Timeout de apagado forzado alcanzado (${FORCE_KILL_TIMEOUT_MS / 1000}s). Saliendo del proceso antes de SIGKILL.`);
      process.exit(1);
    }, FORCE_KILL_TIMEOUT_MS).unref();
  };

  process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
  process.on('SIGINT', () => gracefulShutdown('SIGINT'));
}

startServer().catch(err => {
  console.error('Fatal error al iniciar el servidor:', err);
  process.exit(1);
});

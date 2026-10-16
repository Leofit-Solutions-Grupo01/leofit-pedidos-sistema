// =============================================================================
// SERVER ENTRY POINT - LEOFIT SOLUTIONS
// =============================================================================

import { createApp } from './app';
import { checkDatabaseConnection, isPostgresAvailable, dbPool } from './config/database';
import { runAutoMigrations } from './database/autoMigrate';

const PORT = parseInt(process.env.PORT || '4000', 10);

async function startServer() {
  console.log('🚀 Iniciando Leofit Backend Server...');
  await checkDatabaseConnection();

  if (isPostgresAvailable()) {
    await runAutoMigrations();
  }

  const app = createApp();

  const server = app.listen(PORT, () => {
    console.log(`\n=============================================================`);
    console.log(`✅ Servidor API REST activo en: http://localhost:${PORT}`);
    console.log(`📡 Health Check & Métricas:     http://localhost:${PORT}/api/health`);
    console.log(`🔒 Módulo Auth:                http://localhost:${PORT}/api/auth`);
    console.log(`📦 Módulo Pedidos:             http://localhost:${PORT}/api/orders`);
    console.log(`👕 Módulo Productos:           http://localhost:${PORT}/api/products`);
    console.log(`=============================================================\n`);
  });

  // Graceful Shutdown para despliegues en la nube sin cortar peticiones en vuelo
  const gracefulShutdown = (signal: string) => {
    console.log(`\n🛑 [${signal}] Recibida señal de terminación. Drenando conexiones activas...`);
    server.close(async () => {
      console.log('🔒 Servidor HTTP cerrado para nuevas solicitudes.');
      try {
        await dbPool.end();
        console.log('✅ Pool de conexiones PostgreSQL liberado exitosamente.');
        process.exit(0);
      } catch (err) {
        console.error('❌ Error liberando pool de base de datos:', err);
        process.exit(1);
      }
    });

    // Forzar terminación si las conexiones no drenan en 10s
    setTimeout(() => {
      console.error('⏰ Timeout de apagado seguro superado (10s). Forzando cierre del proceso.');
      process.exit(1);
    }, 10000).unref();
  };

  process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
  process.on('SIGINT', () => gracefulShutdown('SIGINT'));
}

startServer().catch(err => {
  console.error('Fatal error al iniciar el servidor:', err);
  process.exit(1);
});

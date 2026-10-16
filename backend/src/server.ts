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
    console.log(`\n🛑 [${signal}] Marcando instancia como DRAINING (readiness = 503, Connection: close)...`);

    // Margen de 1.5s para que los balanceadores de carga (Render/Cloudflare) redirijan el tráfico
    setTimeout(() => {
      server.close(async () => {
        console.log('🔒 Servidor HTTP cerrado. Drenaje de solicitudes completado.');
        try {
          await dbPool.end();
          console.log('✅ Pool de conexiones PostgreSQL liberado exitosamente.');
          process.exit(0);
        } catch (err) {
          console.error('❌ Error liberando pool de base de datos:', err);
          process.exit(1);
        }
      });
    }, 1500);

    // Timeout de seguridad amplio (25s) para permitir requests en vuelo pesados antes de terminar
    setTimeout(() => {
      console.warn('⏰ Timeout de apagado seguro alcanzado (25s). Forzando cierre del proceso.');
      process.exit(1);
    }, 25000).unref();
  };

  process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
  process.on('SIGINT', () => gracefulShutdown('SIGINT'));
}

startServer().catch(err => {
  console.error('Fatal error al iniciar el servidor:', err);
  process.exit(1);
});

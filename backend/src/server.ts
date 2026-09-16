// =============================================================================
// SERVER ENTRY POINT - LEOFIT SOLUTIONS
// =============================================================================

import { createApp } from './app';
import { checkDatabaseConnection } from './config/database';

const PORT = parseInt(process.env.PORT || '4000', 10);

async function startServer() {
  console.log('🚀 Iniciando Leofit Backend Server...');
  await checkDatabaseConnection();

  const app = createApp();

  app.listen(PORT, () => {
    console.log(`\n=============================================================`);
    console.log(`✅ Servidor API REST activo en: http://localhost:${PORT}`);
    console.log(`📡 Health Check & Métricas:     http://localhost:${PORT}/api/health`);
    console.log(`🔒 Módulo Auth:                http://localhost:${PORT}/api/auth`);
    console.log(`📦 Módulo Pedidos:             http://localhost:${PORT}/api/orders`);
    console.log(`👕 Módulo Productos:           http://localhost:${PORT}/api/products`);
    console.log(`=============================================================\n`);
  });
}

startServer().catch(err => {
  console.error('Fatal error al iniciar el servidor:', err);
  process.exit(1);
});

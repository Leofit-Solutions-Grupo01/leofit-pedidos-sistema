/**
 * @file App.tsx
 * @description Punto de entrada principal y enrutamiento SPA para el sistema LeoFit
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { AppProvider, useApp } from "./context/AppContext";
import Navbar from "./components/layout/Navbar";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import PedidosLista from "./pages/PedidosLista";
import PedidoForm from "./pages/PedidoForm";
import ProductosGestion from "./pages/ProductosGestion";
import RastreoPublico from "./pages/RastreoPublico";
import Analytics from "./pages/Analytics";
import ErrorBoundary from "./components/common/ErrorBoundary";
import { SessionExpiredModal } from "./components/common/SessionExpiredModal";

function AppContent() {
  const { autenticado, paginaActual } = useApp();

  if (!autenticado) return <Login />;

  return (
    <div className="min-h-screen bg-[#F1FAEE]">
      <Navbar />
      {paginaActual === "dashboard" && <Dashboard />}
      {paginaActual === "nuevo-pedido" && (
        <div className="pt-16 pb-32 sm:pb-28 min-h-screen bg-[#F1FAEE]">
          <PedidoForm />
        </div>
      )}
      {paginaActual === "analytics" && <Analytics />}
      {paginaActual === "pedidos" && <PedidosLista />}
      {paginaActual === "productos" && <ProductosGestion />}
      {paginaActual === "rastreo" && <RastreoPublico />}
      <SessionExpiredModal />
    </div>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <AppProvider>
        <AppContent />
      </AppProvider>
    </ErrorBoundary>
  );
}

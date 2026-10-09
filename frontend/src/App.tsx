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

function AppContent() {
  const { autenticado, paginaActual, errorApi, limpiarError, cargando } = useApp();

  if (!autenticado) return <Login />;

  return (
    <div className="min-h-screen bg-[#F1FAEE]">
      <Navbar />
      {(paginaActual === "dashboard" || paginaActual === "nuevo-pedido") && <Dashboard />}
      {paginaActual === "analytics" && <Analytics />}
      {paginaActual === "pedidos" && <PedidosLista />}
      {paginaActual === "productos" && <ProductosGestion />}
      {paginaActual === "rastreo" && <RastreoPublico />}
      
      {/* Modal Nuevo Pedido */}
      {paginaActual === "nuevo-pedido" && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white w-full max-w-4xl max-h-[95vh] overflow-y-auto rounded-2xl shadow-2xl relative">
            <PedidoForm />
          </div>
        </div>
      )}
    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

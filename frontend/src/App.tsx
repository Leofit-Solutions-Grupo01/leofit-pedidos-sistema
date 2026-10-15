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

function AppContent() {
  const { autenticado, paginaActual, navegarA } = useApp();

  if (!autenticado) return <Login />;

  return (
    <div className="min-h-screen bg-[#F1FAEE]">
      <Navbar />
      {(paginaActual === "dashboard" || paginaActual === "nuevo-pedido") && <Dashboard />}
      {paginaActual === "analytics" && <Analytics />}
      {paginaActual === "pedidos" && <PedidosLista />}
      {paginaActual === "productos" && <ProductosGestion />}
      {paginaActual === "rastreo" && <RastreoPublico />}
      
      {/* Modal Nuevo Pedido con cierre accesible por backdrop y botón */}
      {paginaActual === "nuevo-pedido" && (
        <div
          onClick={() => navegarA("dashboard")}
          className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-900/60 backdrop-blur-sm animate-in fade-in"
          role="dialog"
          aria-modal="true"
          aria-label="Formulario de Nuevo Pedido"
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="bg-white w-full max-w-4xl max-h-[95vh] overflow-y-auto rounded-3xl shadow-2xl relative border border-slate-200"
          >
            {/* Botón flotante para cerrar modal */}
            <button
              onClick={() => navegarA("dashboard")}
              className="absolute top-4 right-4 z-20 w-9 h-9 bg-slate-100 hover:bg-red-50 text-slate-500 hover:text-red-600 rounded-full flex items-center justify-center transition-colors shadow-sm"
              aria-label="Cerrar modal"
              title="Cerrar modal y volver al panel principal"
            >
              <span className="material-icons" style={{ fontSize: "20px" }}>close</span>
            </button>
            <PedidoForm />
          </div>
        </div>
      )}
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

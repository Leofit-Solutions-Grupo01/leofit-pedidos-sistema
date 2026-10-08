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

function AppContent() {
  const { autenticado, paginaActual, errorApi, limpiarError, cargando } = useApp();

  if (!autenticado) return <Login />;

  return (
    <div className="min-h-screen bg-[#F1FAEE]">
      <Navbar />
      {cargando && (
        <div role="status" className="fixed top-14 inset-x-0 z-40 text-center text-xs font-semibold bg-slate-800 text-white py-1">
          Sincronizando con el servidor…
        </div>
      )}
      {errorApi && (
        <div role="alert" className="fixed top-16 inset-x-2 sm:inset-x-auto sm:right-4 sm:max-w-md z-50 bg-red-50 border border-red-300 text-red-900 text-sm rounded-xl shadow-lg p-3 flex items-start gap-3">
          <span className="flex-1">{errorApi}</span>
          <button onClick={limpiarError} aria-label="Cerrar aviso" className="font-bold text-red-700 hover:text-red-900">×</button>
        </div>
      )}
      {paginaActual === "dashboard" && <Dashboard />}
      {paginaActual === "pedidos" && <PedidosLista />}
      {paginaActual === "nuevo-pedido" && <PedidoForm />}
      {paginaActual === "productos" && <ProductosGestion />}
      {paginaActual === "rastreo" && <RastreoPublico />}
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

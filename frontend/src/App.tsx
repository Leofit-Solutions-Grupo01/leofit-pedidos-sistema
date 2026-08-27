import { AppProvider, useApp } from "./context/AppContext";
import Navbar from "./components/layout/Navbar";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import PedidosLista from "./pages/PedidosLista";
import PedidoForm from "./pages/PedidoForm";
import ProductosGestion from "./pages/ProductosGestion";

function AppContent() {
  const { autenticado, paginaActual } = useApp();

  if (!autenticado) return <Login />;

  return (
    <div className="min-h-screen bg-[#F1FAEE]">
      <Navbar />
      {paginaActual === "dashboard" && <Dashboard />}
      {paginaActual === "pedidos" && <PedidosLista />}
      {paginaActual === "nuevo-pedido" && <PedidoForm />}
      {paginaActual === "productos" && <ProductosGestion />}
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

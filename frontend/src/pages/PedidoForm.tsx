import { useState } from "react";
import { useApp } from "../context/AppContext";
import { Pedido } from "../data/mockData";

const CANALES = ["WhatsApp", "Llamada", "Sistema"] as const;

interface ItemTemp {
  productoId: string;
  nombre: string;
  cantidad: number;
  precio: number;
}

export default function PedidoForm() {
  const { productos, pedidos, agregarPedido, navegarA } = useApp();
  const [nombre, setNombre] = useState("");
  const [telefono, setTelefono] = useState("");
  const [direccion, setDireccion] = useState("");
  const [canal, setCanal] = useState<typeof CANALES[number]>("WhatsApp");
  const [notas, setNotas] = useState("");
  const [costoDelivery, setCostoDelivery] = useState(8);
  const [descuento, setDescuento] = useState(0);
  const [productoSeleccionado, setProductoSeleccionado] = useState(productos[0]?.id || "");
  const [cantidad, setCantidad] = useState(1);
  const [items, setItems] = useState<ItemTemp[]>([]);
  const [guardado, setGuardado] = useState(false);
  const [errores, setErrores] = useState<string[]>([]);

  const fechaHoy = new Date().toLocaleDateString("es-PE", { day: "2-digit", month: "2-digit", year: "numeric" });

  const subtotal = items.reduce((acc, item) => acc + item.cantidad * item.precio, 0);
  const total = Math.max(0, subtotal + costoDelivery - descuento);

  // Genera número de pedido en formato LFT-NNN
  const siguienteNumero = () => {
    const maximo = pedidos
      .map((p) => parseInt(p.numero.replace("LFT-", ""), 10))
      .filter((n) => !isNaN(n))
      .reduce((a, b) => Math.max(a, b), 0);
    return `LFT-${String(maximo + 1).padStart(3, "0")}`;
  };

  const agregarItem = () => {
    const producto = productos.find((p) => p.id === productoSeleccionado);
    if (!producto) return;
    setItems((prev) => {
      const existente = prev.find((i) => i.productoId === producto.id);
      if (existente) return prev.map((i) => i.productoId === producto.id ? { ...i, cantidad: i.cantidad + cantidad } : i);
      return [...prev, { productoId: producto.id, nombre: producto.nombre, cantidad, precio: producto.precio }];
    });
    setCantidad(1);
  };

  const quitarItem = (productoId: string) => setItems((prev) => prev.filter((i) => i.productoId !== productoId));

  const handleGuardar = () => {
    const errList: string[] = [];
    if (!nombre.trim()) errList.push("El nombre del cliente es obligatorio.");
    if (!telefono.trim()) errList.push("El teléfono es obligatorio.");
    if (!direccion.trim()) errList.push("La dirección de entrega es obligatoria.");
    if (items.length === 0) errList.push("Agrega al menos un producto al pedido.");
    if (errList.length > 0) { setErrores(errList); return; }
    setErrores([]);

    const nuevoPedido: Pedido = {
      id: `o${Date.now()}`,
      numero: siguienteNumero(),
      canal,
      cliente: { nombre, telefono, direccion },
      items: items.map((i) => ({ productoId: i.productoId, nombre: i.nombre, cantidad: i.cantidad, precio: i.precio })),
      total,
      costoDelivery,
      descuento,
      estado: "Recibido",
      fecha: new Date().toISOString().split("T")[0],
      notas: notas.trim() || undefined,
    };
    agregarPedido(nuevoPedido);
    setGuardado(true);
    setTimeout(() => navegarA("pedidos"), 1600);
  };

  if (guardado) {
    return (
      <div className="pt-14 pb-24 min-h-screen bg-[#F1FAEE] flex items-center justify-center">
        <div className="text-center px-6">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-[#27AE60]/10 rounded-full mb-5">
            <span className="material-icons text-[#27AE60]" style={{ fontSize: "44px" }}>check_circle</span>
          </div>
          <h2 className="text-xl font-black text-[#1D3557] mb-1">Pedido registrado</h2>
          <p className="text-sm text-gray-400 font-medium">Redirigiendo al historial...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pt-14 pb-24 min-h-screen bg-[#F1FAEE]">
      <div className="max-w-2xl mx-auto px-4 py-5">
        <div className="flex items-center justify-between mb-5">
          <h1 className="text-2xl font-black text-[#1D3557]">Nuevo Pedido</h1>
          <span className="text-xs text-gray-400 font-mono bg-white px-3 py-1.5 rounded-xl border border-gray-100">{fechaHoy}</span>
        </div>

        {errores.length > 0 && (
          <div className="bg-red-50 border-2 border-red-100 rounded-2xl p-4 mb-4">
            {errores.map((e, i) => (
              <div key={i} className="flex items-start gap-2 mb-1 last:mb-0">
                <span className="material-icons text-[#E63946] mt-0.5" style={{ fontSize: "14px" }}>error_outline</span>
                <p className="text-xs text-red-600 font-medium">{e}</p>
              </div>
            ))}
          </div>
        )}

        {/* Cliente */}
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 mb-4">
          <h2 className="text-sm font-bold text-[#1D3557] mb-4 flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-7 h-7 bg-[#E63946]/10 rounded-lg">
              <span className="material-icons text-[#E63946]" style={{ fontSize: "16px" }}>person</span>
            </span>
            Datos del Cliente
          </h2>
          <div className="space-y-3">
            <div>
              <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Nombre Completo *</label>
              <input type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="ej. Juan Pérez" required
                className="w-full px-3.5 py-2.5 border-2 border-gray-100 rounded-xl text-sm placeholder-gray-300 focus:outline-none focus:border-[#E63946] focus:ring-4 focus:ring-[#E63946]/10 transition-all" />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Teléfono *</label>
              <input type="tel" value={telefono} onChange={(e) => setTelefono(e.target.value)} placeholder="ej. 987654321" required
                className="w-full px-3.5 py-2.5 border-2 border-gray-100 rounded-xl text-sm placeholder-gray-300 focus:outline-none focus:border-[#E63946] focus:ring-4 focus:ring-[#E63946]/10 transition-all" />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Dirección de Entrega *</label>
              <input type="text" value={direccion} onChange={(e) => setDireccion(e.target.value)} placeholder="ej. Av. Siempreviva 123, Lima" required
                className="w-full px-3.5 py-2.5 border-2 border-gray-100 rounded-xl text-sm placeholder-gray-300 focus:outline-none focus:border-[#E63946] focus:ring-4 focus:ring-[#E63946]/10 transition-all" />
            </div>
            <div>
              <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Canal de venta</label>
              <div className="flex gap-2">
                {CANALES.map((c) => (
                  <button key={c} type="button"
                    onClick={() => setCanal(c)}
                    className={`flex-1 py-2 rounded-xl text-xs font-bold border-2 transition-all ${canal === c ? "bg-[#1D3557] text-white border-[#1D3557]" : "border-gray-100 text-gray-400 hover:border-gray-200"}`}
                  >
                    {c}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Productos */}
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 mb-4">
          <h2 className="text-sm font-bold text-[#1D3557] mb-4 flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-7 h-7 bg-[#E63946]/10 rounded-lg">
              <span className="material-icons text-[#E63946]" style={{ fontSize: "16px" }}>inventory_2</span>
            </span>
            Productos
          </h2>
          <div className="flex gap-2 mb-4">
            <select value={productoSeleccionado} onChange={(e) => setProductoSeleccionado(e.target.value)}
              className="flex-1 text-sm border-2 border-gray-100 rounded-xl px-3 py-2.5 focus:outline-none focus:border-[#E63946] bg-[#F1FAEE] font-medium text-[#1D3557] min-w-0">
              {productos.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.nombre} — S/{p.precio.toFixed(2)} {p.stock <= 5 ? `(stock: ${p.stock})` : ""}
                </option>
              ))}
            </select>
            <input type="number" min="1" value={cantidad} onChange={(e) => setCantidad(Math.max(1, parseInt(e.target.value) || 1))}
              className="w-16 text-sm border-2 border-gray-100 rounded-xl px-2 py-2.5 text-center focus:outline-none focus:border-[#E63946] font-bold text-[#1D3557]" />
            <button onClick={agregarItem}
              className="px-3.5 py-2.5 bg-[#1D3557] hover:bg-[#1D3557]/80 text-white rounded-xl font-bold transition-colors flex items-center shrink-0">
              <span className="material-icons" style={{ fontSize: "18px" }}>add</span>
            </button>
          </div>

          {items.length > 0 ? (
            <div className="border-2 border-gray-100 rounded-xl overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="bg-[#F1FAEE]">
                    <th className="px-3 py-2.5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-wider">Producto</th>
                    <th className="px-3 py-2.5 text-center text-[10px] font-bold text-gray-400 uppercase tracking-wider">Cant.</th>
                    <th className="px-3 py-2.5 text-right text-[10px] font-bold text-gray-400 uppercase tracking-wider">Subtotal</th>
                    <th className="px-3 py-2.5" />
                  </tr>
                </thead>
                <tbody>
                  {items.map((item, i) => (
                    <tr key={item.productoId} className={i < items.length - 1 ? "border-b border-gray-50" : ""}>
                      <td className="px-3 py-3 text-sm font-semibold text-[#1A1A1A]">{item.nombre}</td>
                      <td className="px-3 py-3 text-sm text-center text-gray-500 font-semibold">{item.cantidad}</td>
                      <td className="px-3 py-3 text-sm text-right font-bold text-[#1D3557]">S/{(item.cantidad * item.precio).toFixed(2)}</td>
                      <td className="px-3 py-3 text-right">
                        <button onClick={() => quitarItem(item.productoId)} className="p-1 hover:bg-red-50 rounded-lg transition-colors" aria-label="Quitar">
                          <span className="material-icons text-red-300" style={{ fontSize: "16px" }}>close</span>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {/* Desglose económico */}
              <div className="border-t border-gray-100 px-4 py-3 space-y-2">
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>Subtotal productos</span>
                  <span>S/{subtotal.toFixed(2)}</span>
                </div>
                <div className="flex items-center justify-between">
                  <label className="text-sm text-gray-500">Delivery (S/)</label>
                  <input type="number" min="0" step="1" value={costoDelivery}
                    onChange={(e) => setCostoDelivery(Math.max(0, parseFloat(e.target.value) || 0))}
                    className="w-20 text-sm border border-gray-200 rounded-lg px-2 py-1 text-right focus:outline-none focus:border-[#E63946]" />
                </div>
                <div className="flex items-center justify-between">
                  <label className="text-sm text-gray-500">Descuento (S/)</label>
                  <input type="number" min="0" step="1" value={descuento}
                    onChange={(e) => setDescuento(Math.max(0, parseFloat(e.target.value) || 0))}
                    className="w-20 text-sm border border-gray-200 rounded-lg px-2 py-1 text-right focus:outline-none focus:border-[#27AE60]" />
                </div>
                <div className="flex items-center justify-between bg-[#1D3557] rounded-xl px-4 py-3">
                  <span className="text-sm font-bold text-white/70">Total a cobrar</span>
                  <span className="text-2xl font-black text-[#E63946]">S/{total.toFixed(2)}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="border-2 border-dashed border-gray-200 rounded-xl py-8 text-center">
              <span className="material-icons text-gray-200 text-4xl block mb-2">add_shopping_cart</span>
              <p className="text-xs text-gray-400 font-medium">Agrega productos al pedido</p>
            </div>
          )}
        </div>

        {/* Notas */}
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 mb-4">
          <h2 className="text-sm font-bold text-[#1D3557] mb-3 flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-7 h-7 bg-[#F1C40F]/20 rounded-lg">
              <span className="material-icons text-[#B7950B]" style={{ fontSize: "16px" }}>notes</span>
            </span>
            Notas del pedido
            <span className="text-[10px] text-gray-400 font-medium ml-1">(opcional)</span>
          </h2>
          <textarea
            value={notas}
            onChange={(e) => setNotas(e.target.value)}
            placeholder="ej. Cliente prefiere entrega por la mañana, paga contra entrega, talla especial..."
            rows={3}
            className="w-full px-3.5 py-2.5 border-2 border-gray-100 rounded-xl text-sm placeholder-gray-300 focus:outline-none focus:border-[#E63946] focus:ring-4 focus:ring-[#E63946]/10 transition-all resize-none"
          />
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          <button onClick={() => navegarA("dashboard")}
            className="flex-1 py-3.5 border-2 border-gray-200 text-gray-400 font-bold rounded-2xl hover:bg-gray-50 transition-colors">
            Cancelar
          </button>
          <button onClick={handleGuardar}
            className="flex-[2] py-3.5 bg-[#27AE60] hover:bg-[#219150] active:scale-[0.98] text-white font-bold rounded-2xl transition-all flex items-center justify-center gap-2 shadow-lg shadow-[#27AE60]/30">
            <span className="material-icons" style={{ fontSize: "18px" }}>save</span>
            Guardar Pedido
          </button>
        </div>
      </div>
    </div>
  );
}

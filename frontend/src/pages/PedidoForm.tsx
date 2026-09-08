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
  const { productos, pedidos, agregarPedido, navegarA, modoAccesible } = useApp();
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
          <h2 className="text-xl font-bold text-[#1D3557] mb-1">Pedido registrado</h2>
          <p className="text-sm text-slate-500 font-medium">Redirigiendo al historial...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`pt-16 pb-24 min-h-screen ${modoAccesible ? "bg-[#E2E8F0]" : "bg-[#F1FAEE]"}`}>
      <div className="max-w-2xl mx-auto px-4 py-5">
        <div className="flex items-center justify-between mb-5">
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900">Nuevo Pedido</h1>
          <span className="text-xs sm:text-sm text-slate-700 font-mono font-medium bg-white px-3.5 py-2 rounded-xl border border-slate-300 shadow-sm">{fechaHoy}</span>
        </div>

        {errores.length > 0 && (
          <div className="bg-red-100 border-2 border-red-400 rounded-2xl p-4 mb-5 shadow-sm">
            {errores.map((e, i) => (
              <div key={i} className="flex items-start gap-2.5 mb-1.5 last:mb-0">
                <span className="material-icons text-red-700 mt-0.5" style={{ fontSize: "18px" }}>error_outline</span>
                <p className="text-sm text-red-950 font-semibold">{e}</p>
              </div>
            ))}
          </div>
        )}

        {/* Cliente */}
        <div className="bg-white rounded-3xl p-5 shadow-sm border border-slate-200 mb-5">
          <h2 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2.5">
            <span className="inline-flex items-center justify-center w-8 h-8 bg-red-100 rounded-xl border border-red-200">
              <span className="material-icons text-red-600" style={{ fontSize: "20px" }}>person</span>
            </span>
            Datos del Cliente
          </h2>
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                Nombre Completo <span className="text-red-600">*</span>
              </label>
              <input
                type="text"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                placeholder="ej. Carlos Mendoza"
                className="w-full px-4 py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all shadow-inner"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                Teléfono WhatsApp <span className="text-red-600">*</span>
              </label>
              <input
                type="tel"
                value={telefono}
                onChange={(e) => setTelefono(e.target.value)}
                placeholder="ej. 987654321"
                className="w-full px-4 py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all shadow-inner"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                Dirección de Entrega / Distrito <span className="text-red-600">*</span>
              </label>
              <input
                type="text"
                value={direccion}
                onChange={(e) => setDireccion(e.target.value)}
                placeholder="ej. Av. Arequipa 1234, Lince"
                className="w-full px-4 py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all shadow-inner"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">Canal de Venta</label>
              <div className="grid grid-cols-3 gap-2">
                {CANALES.map((c) => (
                  <button
                    key={c}
                    type="button"
                    onClick={() => setCanal(c)}
                    className={`py-3 px-2 rounded-2xl text-sm font-semibold border-2 transition-all flex items-center justify-center gap-1.5 ${
                      canal === c
                        ? "bg-[#0F223D] border-[#0F223D] text-white shadow-md ring-2 ring-slate-300"
                        : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100"
                    }`}
                  >
                    <span className="material-icons" style={{ fontSize: "16px" }}>
                      {c === "WhatsApp" ? "chat" : c === "Llamada" ? "call" : "laptop"}
                    </span>
                    {c}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Productos */}
        <div className="bg-white rounded-3xl p-5 shadow-sm border border-slate-200 mb-5">
          <h2 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2.5">
            <span className="inline-flex items-center justify-center w-8 h-8 bg-blue-100 rounded-xl border border-blue-200">
              <span className="material-icons text-blue-700" style={{ fontSize: "20px" }}>inventory_2</span>
            </span>
            Selección de Prendas
          </h2>
          <div className="flex flex-col sm:flex-row gap-2.5 mb-4">
            <select
              value={productoSeleccionado}
              onChange={(e) => setProductoSeleccionado(e.target.value)}
              className="flex-1 text-sm sm:text-base border-2 border-slate-300 rounded-2xl px-4 py-3 focus:outline-none focus:border-[#0F223D] bg-slate-50 font-semibold text-slate-900"
            >
              {productos.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.nombre} — S/{p.precio.toFixed(2)} {p.stock <= 5 ? `(⚠️ Stock: ${p.stock})` : `(Stock: ${p.stock})`}
                </option>
              ))}
            </select>
            <div className="flex gap-2">
              <input
                type="number"
                min="1"
                value={cantidad}
                onChange={(e) => setCantidad(Math.max(1, parseInt(e.target.value) || 1))}
                className="w-20 text-base border-2 border-slate-300 rounded-2xl px-3 py-3 text-center focus:outline-none focus:border-[#0F223D] font-bold font-mono text-slate-900 bg-slate-50"
              />
              <button
                onClick={agregarItem}
                className="flex-1 sm:flex-initial px-5 py-3 bg-[#0F223D] hover:bg-[#1D3557] text-white rounded-2xl font-bold transition-all flex items-center justify-center gap-1.5 shadow-md shadow-slate-400/30"
              >
                <span className="material-icons" style={{ fontSize: "20px" }}>add</span>
                <span>Agregar</span>
              </button>
            </div>
          </div>

          {items.length > 0 ? (
            <div className="border-2 border-slate-200 rounded-2xl overflow-hidden shadow-inner">
              <table className="w-full">
                <thead>
                  <tr className="bg-slate-100 text-slate-700">
                    <th className="px-4 py-3 text-left text-xs font-semibold uppercase">Prenda</th>
                    <th className="px-3 py-3 text-center text-xs font-semibold uppercase">Cant.</th>
                    <th className="px-4 py-3 text-right text-xs font-semibold uppercase">Subtotal</th>
                    <th className="px-3 py-3 text-center text-xs font-semibold uppercase">Quitar</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((item, i) => (
                    <tr key={item.productoId} className={`transition-colors hover:bg-slate-50 ${i < items.length - 1 ? "border-b border-slate-200" : ""}`}>
                      <td className="px-4 py-3.5 text-sm font-semibold text-slate-900">{item.nombre}</td>
                      <td className="px-3 py-3.5 text-sm text-center text-slate-800 font-medium font-mono">{item.cantidad}</td>
                      <td className="px-4 py-3.5 text-sm text-right font-bold font-mono text-slate-950">S/{(item.cantidad * item.precio).toFixed(2)}</td>
                      <td className="px-3 py-3.5 text-center">
                        <button
                          onClick={() => quitarItem(item.productoId)}
                          className="p-2 hover:bg-red-100 text-red-600 rounded-xl transition-colors"
                          aria-label="Quitar producto"
                        >
                          <span className="material-icons" style={{ fontSize: "20px" }}>delete</span>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Desglose económico */}
              <div className="border-t-2 border-slate-200 bg-slate-50 p-4 space-y-3">
                <div className="flex items-center justify-between text-sm font-semibold text-slate-700">
                  <span>Subtotal prendas</span>
                  <span className="text-base font-bold font-mono text-slate-900">S/{subtotal.toFixed(2)}</span>
                </div>
                <div className="flex items-center justify-between text-sm font-semibold text-slate-700">
                  <label>Costo de Envío / Delivery (S/)</label>
                  <input
                    type="number"
                    min="0"
                    step="1"
                    value={costoDelivery}
                    onChange={(e) => setCostoDelivery(Math.max(0, parseFloat(e.target.value) || 0))}
                    className="w-24 text-base font-bold font-mono border-2 border-slate-300 rounded-xl px-3 py-1.5 text-right focus:outline-none focus:border-[#0F223D] bg-white text-slate-900 shadow-sm"
                  />
                </div>
                <div className="flex items-center justify-between text-sm font-semibold text-slate-700">
                  <label>Descuento Especial (S/)</label>
                  <input
                    type="number"
                    min="0"
                    step="1"
                    value={descuento}
                    onChange={(e) => setDescuento(Math.max(0, parseFloat(e.target.value) || 0))}
                    className="w-24 text-base font-bold font-mono border-2 border-emerald-400 rounded-xl px-3 py-1.5 text-right focus:outline-none focus:border-emerald-600 bg-white text-emerald-900 shadow-sm"
                  />
                </div>
                <div className="flex items-center justify-between bg-[#0F223D] rounded-2xl px-5 py-4 text-white shadow-md">
                  <span className="text-base font-semibold text-slate-200">Total a cobrar</span>
                  <span className="text-3xl font-extrabold font-display text-amber-400">S/{total.toFixed(2)}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="border-2 border-dashed border-slate-300 rounded-2xl py-8 text-center bg-slate-50">
              <span className="material-icons text-slate-300 text-5xl block mb-2">add_shopping_cart</span>
              <p className="text-sm text-slate-600 font-medium">Agrega al menos una prenda para continuar</p>
            </div>
          )}
        </div>

        {/* Notas */}
        <div className="bg-white rounded-3xl p-5 shadow-sm border border-slate-200 mb-6">
          <h2 className="text-base font-bold text-slate-900 mb-3 flex items-center gap-2.5">
            <span className="inline-flex items-center justify-center w-8 h-8 bg-amber-100 rounded-xl border border-amber-200">
              <span className="material-icons text-amber-700" style={{ fontSize: "20px" }}>notes</span>
            </span>
            Notas del Pedido
            <span className="text-xs text-slate-500 font-normal ml-1">(opcional)</span>
          </h2>
          <textarea
            value={notas}
            onChange={(e) => setNotas(e.target.value)}
            placeholder="ej. Entregar por la mañana, pago contra entrega con Yape..."
            rows={3}
            className="w-full px-4 py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-sm sm:text-base font-normal text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all resize-none shadow-inner leading-relaxed"
          />
        </div>

        {/* Actions */}
        <div className="flex gap-4">
          <button
            onClick={() => navegarA("dashboard")}
            className="flex-1 py-4 border-2 border-slate-300 text-slate-700 font-bold text-base rounded-2xl hover:bg-slate-100 transition-colors shadow-sm"
          >
            Cancelar
          </button>
          <button
            onClick={handleGuardar}
            className="flex-[2] py-4 bg-emerald-700 hover:bg-emerald-800 active:scale-[0.98] text-white font-bold text-base rounded-2xl transition-all flex items-center justify-center gap-2 shadow-xl shadow-emerald-700/30 ring-2 ring-white"
          >
            <span className="material-icons" style={{ fontSize: "22px" }}>save</span>
            Guardar Pedido
          </button>
        </div>
      </div>
    </div>
  );
}

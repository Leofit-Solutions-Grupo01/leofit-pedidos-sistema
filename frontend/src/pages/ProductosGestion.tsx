import { useState } from "react";
import { useApp } from "../context/AppContext";
import { Producto } from "../data/mockData";
import Modal from "../components/common/Modal";

const CATEGORIAS: Producto["categoria"][] = ["Deportiva", "Casual", "Accesorios"];
const TALLAS = ["S", "M", "L", "XL", "Único", "38", "40", "42", "44"];
const COLORES = ["Rojo", "Azul", "Negro", "Blanco", "Gris", "Verde", "Amarillo", "Naranja", "Morado"];

type FormData = Omit<Producto, "id">;

function formVacio(): FormData {
  return { nombre: "", categoria: "Deportiva", talla: "M", color: "Negro", precio: 0, stock: 0 };
}

export default function ProductosGestion() {
  const { productos, agregarProducto, editarProducto, eliminarProducto } = useApp();
  const [modalAbierto, setModalAbierto] = useState(false);
  const [editando, setEditando] = useState<Producto | null>(null);
  const [form, setForm] = useState<FormData>(formVacio());
  const [formError, setFormError] = useState("");
  const [confirmando, setConfirmando] = useState<Producto | null>(null);

  const abrirNuevo = () => {
    setEditando(null);
    setForm(formVacio());
    setFormError("");
    setModalAbierto(true);
  };

  const abrirEditar = (producto: Producto) => {
    setEditando(producto);
    setForm({
      nombre: producto.nombre,
      categoria: producto.categoria,
      talla: producto.talla,
      color: producto.color,
      precio: producto.precio,
      stock: producto.stock,
    });
    setFormError("");
    setModalAbierto(true);
  };

  const handleGuardar = () => {
    if (!form.nombre.trim()) { setFormError("El nombre del producto es obligatorio."); return; }
    if (form.precio <= 0) { setFormError("El precio debe ser mayor a 0."); return; }
    setFormError("");
    if (editando) {
      editarProducto({ ...editando, ...form });
    } else {
      agregarProducto({ id: `p${Date.now()}`, ...form });
    }
    setModalAbierto(false);
  };

  const handleEliminar = () => {
    if (confirmando) {
      eliminarProducto(confirmando.id);
      setConfirmando(null);
    }
  };

  const categoriaColor: Record<Producto["categoria"], string> = {
    Deportiva: "bg-[#3498DB]/10 text-[#3498DB]",
    Casual: "bg-[#E67E22]/10 text-[#E67E22]",
    Accesorios: "bg-[#27AE60]/10 text-[#27AE60]",
  };

  return (
    <div className="pt-14 pb-24 min-h-screen bg-[#F1FAEE]">
      <div className="max-w-2xl mx-auto px-4 py-5">
        <div className="flex items-center justify-between mb-5">
          <h1 className="text-2xl font-black text-[#1D3557]">Catalogo</h1>
          <button
            onClick={abrirNuevo}
            className="flex items-center gap-1.5 bg-[#E63946] hover:bg-[#C62828] active:scale-95 text-white px-4 py-2.5 rounded-xl text-sm font-bold transition-all shadow-md shadow-[#E63946]/30"
          >
            <span className="material-icons" style={{ fontSize: "18px" }}>add</span>
            Nuevo
          </button>
        </div>

        <div className="bg-white rounded-2xl shadow-sm overflow-hidden border border-gray-100">
          {productos.length === 0 ? (
            <div className="py-16 text-center">
              <span className="material-icons text-gray-200 text-6xl block mb-3">inventory_2</span>
              <p className="text-sm text-gray-400 font-medium">Sin productos registrados</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-[#F1FAEE]">
                    <th className="px-4 py-3 text-left text-[10px] font-bold text-gray-400 uppercase tracking-wider">Producto</th>
                    <th className="px-4 py-3 text-left text-[10px] font-bold text-gray-400 uppercase tracking-wider hidden sm:table-cell">Cat.</th>
                    <th className="px-4 py-3 text-right text-[10px] font-bold text-gray-400 uppercase tracking-wider">Precio</th>
                    <th className="px-4 py-3 text-center text-[10px] font-bold text-gray-400 uppercase tracking-wider">Stock</th>
                    <th className="px-4 py-3 text-center text-[10px] font-bold text-gray-400 uppercase tracking-wider">Acc.</th>
                  </tr>
                </thead>
                <tbody>
                  {productos.map((prod, i) => (
                    <tr
                      key={prod.id}
                      className={`transition-colors hover:bg-[#F1FAEE]/60 ${i < productos.length - 1 ? "border-b border-gray-50" : ""}`}
                    >
                      <td className="px-4 py-3.5">
                        <div className="text-sm font-bold text-[#1A1A1A]">{prod.nombre}</div>
                        <div className="text-[10px] text-gray-400 font-medium mt-0.5">
                          {prod.talla} · {prod.color}
                        </div>
                      </td>
                      <td className="px-4 py-3.5 hidden sm:table-cell">
                        <span className={`text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wide ${categoriaColor[prod.categoria]}`}>
                          {prod.categoria}
                        </span>
                      </td>
                      <td className="px-4 py-3.5 text-right">
                        <span className="text-sm font-black text-[#1D3557]">S/{prod.precio.toFixed(2)}</span>
                      </td>
                      <td className="px-4 py-3.5 text-center">
                        <span className={`text-sm font-black ${prod.stock <= 5 ? "text-[#E63946]" : "text-[#27AE60]"}`}>
                          {prod.stock}
                        </span>
                      </td>
                      <td className="px-4 py-3.5">
                        <div className="flex items-center justify-center gap-1">
                          <button
                            onClick={() => abrirEditar(prod)}
                            className="p-1.5 rounded-xl hover:bg-[#3498DB]/10 transition-colors"
                            aria-label="Editar producto"
                          >
                            <span className="material-icons text-[#3498DB]" style={{ fontSize: "18px" }}>edit</span>
                          </button>
                          <button
                            onClick={() => setConfirmando(prod)}
                            className="p-1.5 rounded-xl hover:bg-[#E63946]/10 transition-colors"
                            aria-label="Eliminar producto"
                          >
                            <span className="material-icons text-[#E63946]" style={{ fontSize: "18px" }}>delete</span>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {modalAbierto && (
        <Modal titulo={editando ? "Editar Producto" : "Nuevo Producto"} onCerrar={() => setModalAbierto(false)}>
          <div className="space-y-4">
            <div>
              <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Nombre *</label>
              <input
                type="text"
                value={form.nombre}
                onChange={(e) => setForm((f) => ({ ...f, nombre: e.target.value }))}
                placeholder="ej. Camiseta Deportiva Pro"
                className="w-full px-3.5 py-2.5 border-2 border-gray-100 rounded-xl text-sm focus:outline-none focus:border-[#E63946] focus:ring-4 focus:ring-[#E63946]/10 transition-all"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Categoria</label>
                <select
                  value={form.categoria}
                  onChange={(e) => setForm((f) => ({ ...f, categoria: e.target.value as Producto["categoria"] }))}
                  className="w-full px-3 py-2.5 border-2 border-gray-100 rounded-xl text-sm focus:outline-none focus:border-[#E63946] bg-white"
                >
                  {CATEGORIAS.map((c) => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Talla</label>
                <select
                  value={form.talla}
                  onChange={(e) => setForm((f) => ({ ...f, talla: e.target.value }))}
                  className="w-full px-3 py-2.5 border-2 border-gray-100 rounded-xl text-sm focus:outline-none focus:border-[#E63946] bg-white"
                >
                  {TALLAS.map((t) => <option key={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Color</label>
                <select
                  value={form.color}
                  onChange={(e) => setForm((f) => ({ ...f, color: e.target.value }))}
                  className="w-full px-3 py-2.5 border-2 border-gray-100 rounded-xl text-sm focus:outline-none focus:border-[#E63946] bg-white"
                >
                  {COLORES.map((c) => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Precio (S/) *</label>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={form.precio || ""}
                  onChange={(e) => setForm((f) => ({ ...f, precio: parseFloat(e.target.value) || 0 }))}
                  placeholder="0.00"
                  className="w-full px-3.5 py-2.5 border-2 border-gray-100 rounded-xl text-sm focus:outline-none focus:border-[#E63946] focus:ring-4 focus:ring-[#E63946]/10 transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1.5">Stock *</label>
              <input
                type="number"
                min="0"
                value={form.stock || ""}
                onChange={(e) => setForm((f) => ({ ...f, stock: parseInt(e.target.value) || 0 }))}
                placeholder="0"
                className="w-full px-3.5 py-2.5 border-2 border-gray-100 rounded-xl text-sm focus:outline-none focus:border-[#E63946] focus:ring-4 focus:ring-[#E63946]/10 transition-all"
              />
            </div>

            {formError && (
              <div className="flex items-center gap-2 bg-red-50 border border-red-100 rounded-xl px-3 py-2.5">
                <span className="material-icons text-[#E63946]" style={{ fontSize: "16px" }}>error_outline</span>
                <p className="text-xs text-red-600 font-medium">{formError}</p>
              </div>
            )}

            <div className="flex gap-3 pt-1">
              <button
                onClick={() => setModalAbierto(false)}
                className="flex-1 py-3 border-2 border-gray-100 text-gray-400 font-bold rounded-xl hover:bg-gray-50 transition-colors"
              >
                Cancelar
              </button>
              <button
                onClick={handleGuardar}
                className="flex-1 py-3 bg-[#27AE60] hover:bg-[#219150] text-white font-bold rounded-xl transition-colors flex items-center justify-center gap-2 shadow-md shadow-[#27AE60]/20"
              >
                <span className="material-icons" style={{ fontSize: "18px" }}>save</span>
                Guardar
              </button>
            </div>
          </div>
        </Modal>
      )}

      {confirmando && (
        <Modal titulo="Confirmar eliminación" onCerrar={() => setConfirmando(null)}>
          <div className="text-center py-2">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-red-50 rounded-2xl mb-4">
              <span className="material-icons text-[#E63946]" style={{ fontSize: "36px" }}>delete_forever</span>
            </div>
            <p className="text-sm text-gray-500 font-medium mb-1">Esta acción no se puede deshacer</p>
            <p className="text-base font-black text-[#1D3557] mb-6">"{confirmando.nombre}"</p>
            <div className="flex gap-3">
              <button
                onClick={() => setConfirmando(null)}
                className="flex-1 py-3 border-2 border-gray-100 text-gray-400 font-bold rounded-xl hover:bg-gray-50 transition-colors"
              >
                Cancelar
              </button>
              <button
                onClick={handleEliminar}
                className="flex-1 py-3 bg-[#E63946] hover:bg-[#C62828] text-white font-bold rounded-xl transition-colors shadow-md shadow-[#E63946]/20"
              >
                Si, eliminar
              </button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}

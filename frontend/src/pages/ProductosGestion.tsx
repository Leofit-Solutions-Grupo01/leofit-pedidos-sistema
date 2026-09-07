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
  const { productos, agregarProducto, editarProducto, eliminarProducto, modoAccesible } = useApp();
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
    Deportiva: "bg-blue-100 text-blue-950 border-blue-300",
    Casual: "bg-orange-100 text-orange-950 border-orange-300",
    Accesorios: "bg-emerald-100 text-emerald-950 border-emerald-300",
  };

  return (
    <div className={`pt-16 pb-24 min-h-screen ${modoAccesible ? "bg-[#E2E8F0]" : "bg-[#F1FAEE]"}`}>
      <div className="max-w-2xl mx-auto px-4 py-5">
        <div className="flex items-center justify-between mb-5">
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900">Catálogo e Inventario</h1>
          <button
            onClick={abrirNuevo}
            className="flex items-center gap-2 bg-[#E63946] hover:bg-[#C62828] active:scale-95 text-white px-5 py-3 rounded-2xl text-base font-black transition-all shadow-lg shadow-red-500/30 ring-2 ring-white"
          >
            <span className="material-icons" style={{ fontSize: "20px" }}>add</span>
            + Nuevo
          </button>
        </div>

        <div className="bg-white rounded-3xl shadow-sm overflow-hidden border border-slate-200">
          {productos.length === 0 ? (
            <div className="py-16 text-center">
              <span className="material-icons text-slate-300 text-6xl block mb-3">inventory_2</span>
              <p className="text-base font-black text-slate-700">Sin productos registrados</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-slate-100 text-slate-700">
                    <th className="px-4 py-3.5 text-left text-xs font-black uppercase tracking-wider">Prenda</th>
                    <th className="px-4 py-3.5 text-left text-xs font-black uppercase tracking-wider hidden sm:table-cell">Cat.</th>
                    <th className="px-4 py-3.5 text-right text-xs font-black uppercase tracking-wider">Precio</th>
                    <th className="px-4 py-3.5 text-center text-xs font-black uppercase tracking-wider">Stock</th>
                    <th className="px-4 py-3.5 text-center text-xs font-black uppercase tracking-wider">Acción</th>
                  </tr>
                </thead>
                <tbody>
                  {productos.map((prod, i) => (
                    <tr
                      key={prod.id}
                      className={`transition-colors hover:bg-blue-50/40 ${i < productos.length - 1 ? "border-b border-slate-200" : ""}`}
                    >
                      <td className="px-4 py-4">
                        <div className="text-base font-black text-slate-950">{prod.nombre}</div>
                        <div className="text-xs font-bold text-slate-600 mt-0.5">
                          Talla: <span className="text-slate-900 font-black">{prod.talla}</span> · Color: <span className="text-slate-900 font-black">{prod.color}</span>
                        </div>
                      </td>
                      <td className="px-4 py-4 hidden sm:table-cell">
                        <span className={`text-xs font-black px-3 py-1 rounded-xl uppercase tracking-wide border ${categoriaColor[prod.categoria]}`}>
                          {prod.categoria}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className="text-base font-black text-slate-950">S/{prod.precio.toFixed(2)}</span>
                      </td>
                      <td className="px-4 py-4 text-center">
                        <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-xl text-xs font-black border ${
                          prod.stock <= 5
                            ? "bg-red-100 text-red-900 border-red-300 animate-pulse"
                            : "bg-emerald-100 text-emerald-950 border-emerald-300"
                        }`}>
                          {prod.stock <= 5 && <span className="material-icons" style={{ fontSize: "14px" }}>warning</span>}
                          {prod.stock} uds
                        </span>
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex items-center justify-center gap-2">
                          <button
                            onClick={() => abrirEditar(prod)}
                            className="p-2.5 rounded-xl bg-blue-50 text-blue-800 hover:bg-[#0F223D] hover:text-white transition-colors border border-blue-200"
                            aria-label="Editar producto"
                            title="Editar prenda"
                          >
                            <span className="material-icons" style={{ fontSize: "20px" }}>edit</span>
                          </button>
                          <button
                            onClick={() => setConfirmando(prod)}
                            className="p-2.5 rounded-xl bg-red-50 text-red-700 hover:bg-red-600 hover:text-white transition-colors border border-red-200"
                            aria-label="Eliminar producto"
                            title="Eliminar prenda"
                          >
                            <span className="material-icons" style={{ fontSize: "20px" }}>delete</span>
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
        <Modal titulo={editando ? "Editar Prenda" : "Nueva Prenda"} onCerrar={() => setModalAbierto(false)}>
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-black text-slate-700 uppercase tracking-wider mb-1.5">Nombre de Prenda *</label>
              <input
                type="text"
                value={form.nombre}
                onChange={(e) => setForm((f) => ({ ...f, nombre: e.target.value }))}
                placeholder="ej. Camiseta Dry-Fit Pro"
                className="w-full px-4 py-3 bg-slate-50 border-2 border-slate-300 rounded-2xl text-base font-bold text-slate-900 focus:outline-none focus:border-[#0F223D] focus:bg-white"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-black text-slate-700 uppercase tracking-wider mb-1.5">Categoría</label>
                <select
                  value={form.categoria}
                  onChange={(e) => setForm((f) => ({ ...f, categoria: e.target.value as Producto["categoria"] }))}
                  className="w-full px-4 py-3 border-2 border-slate-300 rounded-2xl text-base font-bold text-slate-900 bg-slate-50"
                >
                  {CATEGORIAS.map((c) => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-black text-slate-700 uppercase tracking-wider mb-1.5">Talla</label>
                <select
                  value={form.talla}
                  onChange={(e) => setForm((f) => ({ ...f, talla: e.target.value }))}
                  className="w-full px-4 py-3 border-2 border-slate-300 rounded-2xl text-base font-bold text-slate-900 bg-slate-50"
                >
                  {TALLAS.map((t) => <option key={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-black text-slate-700 uppercase tracking-wider mb-1.5">Color</label>
                <select
                  value={form.color}
                  onChange={(e) => setForm((f) => ({ ...f, color: e.target.value }))}
                  className="w-full px-4 py-3 border-2 border-slate-300 rounded-2xl text-base font-bold text-slate-900 bg-slate-50"
                >
                  {COLORES.map((c) => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-black text-slate-700 uppercase tracking-wider mb-1.5">Precio (S/) *</label>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={form.precio || ""}
                  onChange={(e) => setForm((f) => ({ ...f, precio: parseFloat(e.target.value) || 0 }))}
                  placeholder="0.00"
                  className="w-full px-4 py-3 border-2 border-slate-300 rounded-2xl text-base font-bold text-slate-900 bg-slate-50"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-black text-slate-700 uppercase tracking-wider mb-1.5">Stock Disponible *</label>
              <input
                type="number"
                min="0"
                value={form.stock || ""}
                onChange={(e) => setForm((f) => ({ ...f, stock: parseInt(e.target.value) || 0 }))}
                placeholder="0"
                className="w-full px-4 py-3 border-2 border-slate-300 rounded-2xl text-base font-bold text-slate-900 bg-slate-50"
              />
            </div>

            {formError && (
              <div className="flex items-center gap-2 bg-red-100 border-2 border-red-300 rounded-2xl px-4 py-3">
                <span className="material-icons text-red-700" style={{ fontSize: "20px" }}>error_outline</span>
                <p className="text-sm text-red-950 font-black">{formError}</p>
              </div>
            )}

            <div className="flex gap-3 pt-2">
              <button
                onClick={() => setModalAbierto(false)}
                className="flex-1 py-3.5 border-2 border-slate-300 text-slate-700 font-black rounded-2xl hover:bg-slate-100 transition-colors"
              >
                Cancelar
              </button>
              <button
                onClick={handleGuardar}
                className="flex-1 py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white font-black rounded-2xl transition-colors flex items-center justify-center gap-2 shadow-lg shadow-emerald-700/30 ring-2 ring-white"
              >
                <span className="material-icons" style={{ fontSize: "20px" }}>save</span>
                Guardar Prenda
              </button>
            </div>
          </div>
        </Modal>
      )}

      {confirmando && (
        <Modal titulo="Confirmar Eliminación" onCerrar={() => setConfirmando(null)}>
          <div className="text-center py-3">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-red-100 border border-red-200 rounded-3xl mb-4">
              <span className="material-icons text-red-600" style={{ fontSize: "36px" }}>delete_forever</span>
            </div>
            <p className="text-base text-slate-600 font-bold mb-1">¿Estás seguro de eliminar esta prenda?</p>
            <p className="text-lg font-black text-slate-950 mb-6 bg-slate-100 py-2 px-4 rounded-xl border border-slate-200">"{confirmando.nombre}"</p>
            <div className="flex gap-3">
              <button
                onClick={() => setConfirmando(null)}
                className="flex-1 py-3.5 border-2 border-slate-300 text-slate-700 font-black rounded-2xl hover:bg-slate-100 transition-colors"
              >
                Cancelar
              </button>
              <button
                onClick={handleEliminar}
                className="flex-1 py-3.5 bg-red-600 hover:bg-red-700 text-white font-black rounded-2xl transition-colors shadow-lg shadow-red-500/30 ring-2 ring-white"
              >
                Sí, eliminar
              </button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}

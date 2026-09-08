/**
 * @file ProductosGestion.tsx
 * @description Módulo de administración y control de inventario de prendas y accesorios LeoFit
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

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
    <div className={`pt-16 pb-32 sm:pb-28 min-h-screen ${modoAccesible ? "bg-[#E2E8F0]" : "bg-[#F1FAEE]"}`}>
      <div className="max-w-5xl mx-auto px-3 sm:px-6 py-4 sm:py-5">
        <div className="flex flex-wrap items-center justify-between gap-2.5 mb-5">
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900">Catálogo e Inventario</h1>
          <button
            onClick={abrirNuevo}
            className="flex items-center gap-1.5 sm:gap-2 bg-[#E63946] hover:bg-[#C62828] active:scale-95 text-white px-4 sm:px-5 py-2.5 sm:py-3 rounded-2xl text-sm sm:text-base font-bold transition-all shadow-lg shadow-red-500/30 ring-2 ring-white"
          >
            <span className="material-icons" style={{ fontSize: "18px" }}>add</span>
            <span>+ Nueva Prenda</span>
          </button>
        </div>

        <div className="bg-white rounded-3xl shadow-sm overflow-hidden border border-slate-200">
          {productos.length === 0 ? (
            <div className="py-16 text-center px-4">
              <span className="material-icons text-slate-300 text-5xl sm:text-6xl block mb-3">inventory_2</span>
              <p className="text-base font-bold text-slate-700">Sin productos registrados</p>
            </div>
          ) : (
            <>
              {/* VISTA MÓVIL (<640px): Cards legibles */}
              <div className="block sm:hidden divide-y divide-slate-100">
                {productos.map((prod) => (
                  <div key={prod.id} className="p-3.5 space-y-2.5">
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <div className="text-sm font-bold text-slate-900">{prod.nombre}</div>
                        <div className="text-xs text-slate-500 font-normal mt-0.5">
                          Talla: <strong className="text-slate-800">{prod.talla}</strong> · Color: <strong className="text-slate-800">{prod.color}</strong>
                        </div>
                      </div>
                      <span className="text-sm font-bold font-mono text-slate-900 shrink-0">
                        S/{prod.precio.toFixed(2)}
                      </span>
                    </div>

                    <div className="flex items-center justify-between gap-2 pt-1">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-lg uppercase tracking-wide border ${categoriaColor[prod.categoria]}`}>
                          {prod.categoria}
                        </span>
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-lg text-[11px] font-bold border font-mono ${
                          prod.stock <= 5
                            ? "bg-red-100 text-red-900 border-red-300 animate-pulse"
                            : "bg-emerald-100 text-emerald-950 border-emerald-300"
                        }`}>
                          {prod.stock <= 5 && <span className="material-icons" style={{ fontSize: "12px" }}>warning</span>}
                          {prod.stock} uds
                        </span>
                      </div>

                      <div className="flex items-center gap-1.5">
                        <button
                          onClick={() => abrirEditar(prod)}
                          className="p-2 rounded-xl bg-blue-50 text-blue-800 hover:bg-[#0F223D] hover:text-white transition-colors border border-blue-200"
                          aria-label="Editar producto"
                        >
                          <span className="material-icons" style={{ fontSize: "16px" }}>edit</span>
                        </button>
                        <button
                          onClick={() => setConfirmando(prod)}
                          className="p-2 rounded-xl bg-red-50 text-red-700 hover:bg-red-600 hover:text-white transition-colors border border-red-200"
                          aria-label="Eliminar producto"
                        >
                          <span className="material-icons" style={{ fontSize: "16px" }}>delete</span>
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* VISTA TABLET/DESKTOP (>=640px): Tabla completa */}
              <div className="hidden sm:block overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-slate-100 text-slate-700">
                      <th className="px-4 py-3.5 text-left text-xs font-semibold uppercase tracking-wider">Prenda</th>
                      <th className="px-4 py-3.5 text-left text-xs font-semibold uppercase tracking-wider">Cat.</th>
                      <th className="px-4 py-3.5 text-right text-xs font-semibold uppercase tracking-wider">Precio</th>
                      <th className="px-4 py-3.5 text-center text-xs font-semibold uppercase tracking-wider">Stock</th>
                      <th className="px-4 py-3.5 text-center text-xs font-semibold uppercase tracking-wider">Acción</th>
                    </tr>
                  </thead>
                  <tbody>
                    {productos.map((prod, i) => (
                      <tr
                        key={prod.id}
                        className={`transition-colors hover:bg-blue-50/40 ${i < productos.length - 1 ? "border-b border-slate-200" : ""}`}
                      >
                        <td className="px-4 py-4">
                          <div className="text-sm sm:text-base font-semibold text-slate-900">{prod.nombre}</div>
                          <div className="text-xs font-normal text-slate-600 mt-0.5">
                            Talla: <span className="text-slate-800 font-semibold">{prod.talla}</span> · Color: <span className="text-slate-800 font-semibold">{prod.color}</span>
                          </div>
                        </td>
                        <td className="px-4 py-4">
                          <span className={`text-xs font-semibold px-2.5 py-1 rounded-xl uppercase tracking-wide border ${categoriaColor[prod.categoria]}`}>
                            {prod.categoria}
                          </span>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <span className="text-sm sm:text-base font-bold font-mono text-slate-900">S/{prod.precio.toFixed(2)}</span>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-xl text-xs font-bold border font-mono ${
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
                              <span className="material-icons" style={{ fontSize: "18px" }}>edit</span>
                            </button>
                            <button
                              onClick={() => setConfirmando(prod)}
                              className="p-2.5 rounded-xl bg-red-50 text-red-700 hover:bg-red-600 hover:text-white transition-colors border border-red-200"
                              aria-label="Eliminar producto"
                              title="Eliminar prenda"
                            >
                              <span className="material-icons" style={{ fontSize: "18px" }}>delete</span>
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </div>
      </div>

      {modalAbierto && (
        <Modal titulo={editando ? "Editar Prenda" : "Nueva Prenda"} onCerrar={() => setModalAbierto(false)}>
          <div className="space-y-3.5 sm:space-y-4 max-h-[75vh] overflow-y-auto px-1">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Nombre de Prenda *</label>
              <input
                type="text"
                value={form.nombre}
                onChange={(e) => setForm((f) => ({ ...f, nombre: e.target.value }))}
                placeholder="ej. Camiseta Dry-Fit Pro"
                className="w-full px-3.5 py-2.5 sm:py-3 bg-slate-50 border-2 border-slate-300 rounded-2xl text-sm sm:text-base font-medium text-slate-900 focus:outline-none focus:border-[#0F223D] focus:bg-white"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Categoría</label>
                <select
                  value={form.categoria}
                  onChange={(e) => setForm((f) => ({ ...f, categoria: e.target.value as Producto["categoria"] }))}
                  className="w-full px-3.5 py-2.5 border-2 border-slate-300 rounded-2xl text-sm sm:text-base font-medium text-slate-900 bg-slate-50"
                >
                  {CATEGORIAS.map((c) => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Talla</label>
                <select
                  value={form.talla}
                  onChange={(e) => setForm((f) => ({ ...f, talla: e.target.value }))}
                  className="w-full px-3.5 py-2.5 border-2 border-slate-300 rounded-2xl text-sm sm:text-base font-medium text-slate-900 bg-slate-50"
                >
                  {TALLAS.map((t) => <option key={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Color</label>
                <select
                  value={form.color}
                  onChange={(e) => setForm((f) => ({ ...f, color: e.target.value }))}
                  className="w-full px-3.5 py-2.5 border-2 border-slate-300 rounded-2xl text-sm sm:text-base font-medium text-slate-900 bg-slate-50"
                >
                  {COLORES.map((c) => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Precio (S/) *</label>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={form.precio || ""}
                  onChange={(e) => setForm((f) => ({ ...f, precio: parseFloat(e.target.value) || 0 }))}
                  placeholder="0.00"
                  className="w-full px-3.5 py-2.5 border-2 border-slate-300 rounded-2xl text-sm sm:text-base font-medium font-mono text-slate-900 bg-slate-50"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Stock Disponible *</label>
              <input
                type="number"
                min="0"
                value={form.stock || ""}
                onChange={(e) => setForm((f) => ({ ...f, stock: parseInt(e.target.value) || 0 }))}
                placeholder="0"
                className="w-full px-3.5 py-2.5 border-2 border-slate-300 rounded-2xl text-sm sm:text-base font-medium font-mono text-slate-900 bg-slate-50"
              />
            </div>

            {formError && (
              <div className="flex items-center gap-2 bg-red-100 border-2 border-red-300 rounded-2xl px-3.5 py-2.5">
                <span className="material-icons text-red-700" style={{ fontSize: "18px" }}>error_outline</span>
                <p className="text-xs sm:text-sm text-red-950 font-semibold">{formError}</p>
              </div>
            )}

            <div className="flex gap-2.5 pt-2">
              <button
                onClick={() => setModalAbierto(false)}
                className="flex-1 py-3 border-2 border-slate-300 text-slate-700 font-bold rounded-2xl hover:bg-slate-100 transition-colors text-sm"
              >
                Cancelar
              </button>
              <button
                onClick={handleGuardar}
                className="flex-1 py-3 bg-emerald-700 hover:bg-emerald-800 text-white font-bold rounded-2xl transition-colors flex items-center justify-center gap-1.5 shadow-lg shadow-emerald-700/30 ring-2 ring-white text-sm"
              >
                <span className="material-icons" style={{ fontSize: "18px" }}>save</span>
                <span>Guardar</span>
              </button>
            </div>
          </div>
        </Modal>
      )}

      {confirmando && (
        <Modal titulo="Confirmar Eliminación" onCerrar={() => setConfirmando(null)}>
          <div className="text-center py-3">
            <div className="inline-flex items-center justify-center w-14 h-14 bg-red-100 border border-red-200 rounded-3xl mb-3">
              <span className="material-icons text-red-600" style={{ fontSize: "32px" }}>delete_forever</span>
            </div>
            <p className="text-sm sm:text-base text-slate-600 font-medium mb-1">¿Estás seguro de eliminar esta prenda?</p>
            <p className="text-base sm:text-lg font-bold text-slate-950 mb-5 bg-slate-100 py-2 px-3 rounded-xl border border-slate-200">"{confirmando.nombre}"</p>
            <div className="flex gap-2.5">
              <button
                onClick={() => setConfirmando(null)}
                className="flex-1 py-3 border-2 border-slate-300 text-slate-700 font-bold rounded-2xl hover:bg-slate-100 transition-colors text-sm"
              >
                Cancelar
              </button>
              <button
                onClick={handleEliminar}
                className="flex-1 py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-2xl transition-colors shadow-lg shadow-red-500/30 ring-2 ring-white text-sm"
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

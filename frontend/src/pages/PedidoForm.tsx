/**
 * @file PedidoForm.tsx
 * @description Formulario reactivo de registro de pedidos con DNI/RUC, cupones y pasarela de pago
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { useState } from "react";
import { useApp } from "../context/AppContext";
import ReciboModal from "../components/common/ReciboModal";
import { Pedido, TipoEnvio, AgenciaEncomienda, MetodoPago, CUPONES_VALIDOS } from "../data/mockData";

const CANALES = ["WhatsApp", "Llamada", "Sistema"] as const;
const AGENCIAS: AgenciaEncomienda[] = ["Shalom", "Olva Courier", "Marvisur", "Flores Hermanos", "Otra"];
const METODOS_PAGO: { id: MetodoPago; label: string; icon: string; color: string }[] = [
  { id: "Yape", label: "Yape", icon: "phone_android", color: "bg-purple-600 text-white" },
  { id: "Plin", label: "Plin", icon: "smartphone", color: "bg-cyan-600 text-white" },
  { id: "Transferencia BCP", label: "BCP", icon: "account_balance", color: "bg-blue-800 text-white" },
  { id: "Transferencia BBVA", label: "BBVA", icon: "account_balance", color: "bg-blue-600 text-white" },
  { id: "Contra Entrega", label: "Contra Entrega", icon: "payments", color: "bg-emerald-700 text-white" },
  { id: "Tarjeta/Link", label: "Tarjeta / Link", icon: "credit_card", color: "bg-slate-800 text-white" },
];

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
  const [dniRuc, setDniRuc] = useState("");
  const [distrito, setDistrito] = useState("");
  const [direccion, setDireccion] = useState("");
  const [referencia, setReferencia] = useState("");
  const [tipoEnvio, setTipoEnvio] = useState<TipoEnvio>("Local");
  const [ciudadDestino, setCiudadDestino] = useState("");
  const [agenciaEncomienda, setAgenciaEncomienda] = useState<AgenciaEncomienda>("Shalom");
  const [numeroGuia, setNumeroGuia] = useState("");
  const [canal, setCanal] = useState<typeof CANALES[number]>("WhatsApp");
  const [metodoPago, setMetodoPago] = useState<MetodoPago>("Yape");
  const [numeroOperacion, setNumeroOperacion] = useState("");
  const [notas, setNotas] = useState("");
  const [costoDelivery, setCostoDelivery] = useState(8);
  const [codigoCuponInput, setCodigoCuponInput] = useState("");
  const [cuponAplicado, setCuponAplicado] = useState<{ codigo: string; descuento: number; descripcion: string } | null>(null);
  const [mensajeCupon, setMensajeCupon] = useState<{ texto: string; tipo: "exito" | "error" } | null>(null);
  const [descuentoManual, setDescuentoManual] = useState(0);

  const [productoSeleccionado, setProductoSeleccionado] = useState(productos[0]?.id || "");
  const [cantidad, setCantidad] = useState(1);
  const [items, setItems] = useState<ItemTemp[]>([]);
  const [pedidoCreado, setPedidoCreado] = useState<Pedido | null>(null);
  const [mostrarRecibo, setMostrarRecibo] = useState(false);
  const [errores, setErrores] = useState<string[]>([]);

  const fechaHoy = new Date().toLocaleDateString("es-PE", { day: "2-digit", month: "2-digit", year: "numeric" });

  const siguienteNumero = () => {
    const maxNum = pedidos.reduce((max, p) => {
      const n = parseInt(p.numero.replace("LFT-", ""));
      return isNaN(n) ? max : Math.max(max, n);
    }, 0);
    return `LFT-${String(maxNum + 1).padStart(3, "0")}`;
  };

  const subtotal = items.reduce((acc, i) => acc + i.precio * i.cantidad, 0);
  const descuentoCuponMonto = cuponAplicado ? cuponAplicado.descuento : 0;
  const descuentoTotal = descuentoCuponMonto + descuentoManual;
  const total = Math.max(0, subtotal + costoDelivery - descuentoTotal);

  const agregarItem = () => {
    const prod = productos.find((p) => p.id === productoSeleccionado);
    if (!prod) return;
    const existente = items.find((i) => i.productoId === prod.id);
    const cantExistente = existente ? existente.cantidad : 0;
    const cantNueva = cantExistente + cantidad;

    if (cantNueva > prod.stock) {
      alert(`Stock insuficiente. Solo quedan ${prod.stock} unidades de "${prod.nombre}".`);
      return;
    }

    if (existente) {
      setItems(items.map((i) => (i.productoId === prod.id ? { ...i, cantidad: cantNueva } : i)));
    } else {
      setItems([...items, { productoId: prod.id, nombre: `${prod.nombre} (${prod.talla})`, cantidad, precio: prod.precio }]);
    }
    setCantidad(1);
  };

  const eliminarItem = (prodId: string) => {
    setItems(items.filter((i) => i.productoId !== prodId));
  };

  const aplicarCupon = (e: React.FormEvent) => {
    e.preventDefault();
    setMensajeCupon(null);
    const code = codigoCuponInput.trim().toUpperCase();
    if (!code) {
      setMensajeCupon({ texto: "Ingresa un código de cupón.", tipo: "error" });
      return;
    }

    const encontrado = CUPONES_VALIDOS.find((c) => c.codigo === code);
    if (encontrado) {
      setCuponAplicado(encontrado);
      setMensajeCupon({ texto: `¡Cupón ${encontrado.codigo} aplicado! (-S/ ${encontrado.descuento.toFixed(2)})`, tipo: "exito" });
    } else {
      setMensajeCupon({ texto: `El código "${codigoCuponInput}" no es válido. Prueba: LEOFIT10`, tipo: "error" });
    }
  };

  const quitarCupon = () => {
    setCuponAplicado(null);
    setCodigoCuponInput("");
    setMensajeCupon(null);
  };

  const handleGuardar = () => {
    const errList: string[] = [];
    if (!nombre.trim()) errList.push("El nombre completo del cliente es obligatorio.");
    if (!telefono.trim()) errList.push("El teléfono de contacto es obligatorio.");
    if (tipoEnvio === "Nacional" && !dniRuc.trim()) {
      errList.push("El DNI o RUC es obligatorio para envíos nacionales por encomienda (Exigencia legal de Shalom / Olva).");
    }
    if (!direccion.trim()) errList.push("La dirección de entrega o agencia es obligatoria.");
    if (tipoEnvio === "Nacional" && !ciudadDestino.trim()) errList.push("Indica la ciudad/departamento de destino para el envío nacional.");
    if (items.length === 0) errList.push("Agrega al menos una prenda al pedido.");
    if (errList.length > 0) {
      setErrores(errList);
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }
    setErrores([]);

    const nuevoPedido: Pedido = {
      id: `o${Date.now()}`,
      numero: siguienteNumero(),
      canal,
      cliente: {
        nombre: nombre.trim(),
        telefono: telefono.trim(),
        dniRuc: dniRuc.trim() || undefined,
        distrito: distrito.trim() || undefined,
        direccion: direccion.trim(),
        referencia: referencia.trim() || undefined,
      },
      tipoEnvio,
      ciudadDestino: tipoEnvio === "Nacional" ? ciudadDestino.trim() : "Lima Capital",
      agenciaEncomienda: tipoEnvio === "Nacional" ? agenciaEncomienda : undefined,
      numeroGuia: tipoEnvio === "Nacional" && numeroGuia.trim() ? numeroGuia.trim() : undefined,
      items: items.map((i) => ({ productoId: i.productoId, nombre: i.nombre, cantidad: i.cantidad, precio: i.precio })),
      total,
      costoDelivery,
      descuento: descuentoTotal,
      cuponAplicado: cuponAplicado?.codigo,
      metodoPago,
      numeroOperacion: numeroOperacion.trim() || undefined,
      estado: "Recibido",
      fecha: new Date().toISOString().split("T")[0],
      notas: notas.trim() || undefined,
    };

    agregarPedido(nuevoPedido);
    setPedidoCreado(nuevoPedido);
  };

  if (pedidoCreado) {
    return (
      <div className="pt-20 pb-32 min-h-screen bg-[#F1FAEE] flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl p-6 sm:p-8 max-w-lg w-full text-center shadow-xl border border-slate-200 animate-in zoom-in-95">
          <div className="inline-flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 bg-emerald-100 rounded-3xl mb-4 text-emerald-600 shadow-inner">
            <span className="material-icons" style={{ fontSize: "40px" }}>check_circle</span>
          </div>

          <span className="text-xs font-mono font-bold bg-[#0F223D] text-white px-3 py-1 rounded-xl inline-block mb-2">
            {pedidoCreado.numero}
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-1">¡Pedido Registrado con Éxito!</h2>
          <p className="text-xs sm:text-sm text-slate-600 font-medium mb-6">
            El pedido de <strong>{pedidoCreado.cliente.nombre}</strong> por <strong>S/{pedidoCreado.total.toFixed(2)}</strong> ha sido registrado en el sistema.
          </p>

          <div className="space-y-2.5">
            <button
              onClick={() => setMostrarRecibo(true)}
              className="w-full py-3.5 bg-[#0F223D] hover:bg-[#1E293B] text-white font-bold text-sm sm:text-base rounded-2xl shadow-lg transition-all flex items-center justify-center gap-2 active:scale-95"
            >
              <span className="material-icons" style={{ fontSize: "20px" }}>receipt_long</span>
              <span>Ver y Descargar Recibo PDF / Rótulo</span>
            </button>

            <a
              href={`https://wa.me/51${pedidoCreado.cliente.telefono.replace(/\D/g, "")}?text=${encodeURIComponent(`Hola ${pedidoCreado.cliente.nombre}, confirmamos tu pedido ${pedidoCreado.numero} en LeoFit por S/${pedidoCreado.total.toFixed(2)}. Puedes ver el detalle y rastrear tu envío aquí: https://leofit.com/rastreo?codigo=${pedidoCreado.numero}`)}`}
              target="_blank"
              rel="noreferrer"
              className="w-full py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm sm:text-base rounded-2xl shadow-md transition-all flex items-center justify-center gap-2 active:scale-95"
            >
              <span className="material-icons" style={{ fontSize: "20px" }}>chat</span>
              <span>Enviar Confirmación por WhatsApp</span>
            </a>

            <button
              onClick={() => navegarA("pedidos")}
              className="w-full py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs sm:text-sm rounded-2xl transition-colors mt-2"
            >
              Ir al Historial de Pedidos
            </button>
          </div>
        </div>

        {mostrarRecibo && (
          <ReciboModal
            pedido={pedidoCreado}
            onClose={() => setMostrarRecibo(false)}
          />
        )}
      </div>
    );
  }

  return (
    <div className={`pt-16 pb-32 sm:pb-28 min-h-screen ${modoAccesible ? "bg-[#E2E8F0]" : "bg-[#F1FAEE]"}`}>
      <div className="max-w-5xl mx-auto px-3 sm:px-6 py-4 sm:py-5">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-5">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900">Nuevo Pedido</h1>
            <p className="text-xs sm:text-sm text-slate-600 font-medium mt-0.5">
              Registro completo con despacho dual, validación de DNI y métodos de pago
            </p>
          </div>
          <span className="text-xs sm:text-sm text-slate-700 font-mono font-medium bg-white px-3 sm:px-3.5 py-1.5 sm:py-2 rounded-xl border border-slate-300 shadow-sm">
            {fechaHoy}
          </span>
        </div>

        {errores.length > 0 && (
          <div className="bg-red-100 border-2 border-red-400 rounded-2xl p-3.5 sm:p-4 mb-5 shadow-sm animate-shake">
            <p className="text-sm font-bold text-red-950 mb-1 flex items-center gap-1.5">
              <span className="material-icons text-red-700" style={{ fontSize: "18px" }}>error</span>
              Corrige los siguientes campos antes de guardar:
            </p>
            {errores.map((e, i) => (
              <div key={i} className="flex items-start gap-2 mb-1 last:mb-0 ml-1">
                <span className="text-red-700 font-bold">•</span>
                <p className="text-xs sm:text-sm text-red-900 font-medium">{e}</p>
              </div>
            ))}
          </div>
        )}

        {/* 1. Modalidad de Envío */}
        <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-sm border border-slate-200 mb-5">
          <h2 className="text-sm sm:text-base font-bold text-slate-900 mb-3 flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-8 h-8 bg-blue-100 rounded-xl border border-blue-200 shrink-0">
              <span className="material-icons text-blue-700" style={{ fontSize: "18px" }}>local_shipping</span>
            </span>
            <span>1. Modalidad de Despacho y Destino</span>
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3 mb-4">
            <button
              type="button"
              onClick={() => handleTipoEnvioChange("Local")}
              className={`p-3.5 rounded-2xl border-2 text-left transition-all flex flex-col gap-1 ${
                tipoEnvio === "Local"
                  ? "border-[#0F223D] bg-[#0F223D] text-white shadow-md ring-2 ring-slate-300"
                  : "border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100"
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold">Lima Capital (Reparto Local)</span>
                <span className="material-icons" style={{ fontSize: "18px" }}>two_wheeler</span>
              </div>
              <span className={`text-xs ${tipoEnvio === "Local" ? "text-slate-300" : "text-slate-500"}`}>
                Entrega directa con Víctor / Motorizado express
              </span>
            </button>

            <button
              type="button"
              onClick={() => handleTipoEnvioChange("Nacional")}
              className={`p-3.5 rounded-2xl border-2 text-left transition-all flex flex-col gap-1 ${
                tipoEnvio === "Nacional"
                  ? "border-[#0F223D] bg-[#0F223D] text-white shadow-md ring-2 ring-slate-300"
                  : "border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100"
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold">Provincia / Nacional (Encomienda)</span>
                <span className="material-icons" style={{ fontSize: "18px" }}>domain</span>
              </div>
              <span className={`text-xs ${tipoEnvio === "Nacional" ? "text-slate-300" : "text-slate-500"}`}>
                Vía agencia (Shalom, Olva, Marvisur) con Guía y DNI
              </span>
            </button>
          </div>

          {/* Campos adicionales para Envío Nacional */}
          {tipoEnvio === "Nacional" && (
            <div className="bg-blue-50/70 rounded-2xl p-3.5 sm:p-4 border border-blue-200 space-y-3">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] sm:text-xs font-semibold text-slate-800 uppercase tracking-wider mb-1">
                    Ciudad / Departamento de Destino <span className="text-red-600">*</span>
                  </label>
                  <input
                    type="text"
                    value={ciudadDestino}
                    onChange={(e) => setCiudadDestino(e.target.value)}
                    placeholder="ej. Trujillo, Arequipa, Cusco, Piura"
                    className="w-full px-3.5 py-2.5 bg-white border-2 border-slate-300 rounded-xl text-sm font-medium text-slate-900 focus:outline-none focus:border-[#0F223D]"
                  />
                </div>
                <div>
                  <label className="block text-[11px] sm:text-xs font-semibold text-slate-800 uppercase tracking-wider mb-1">
                    Empresa de Encomienda
                  </label>
                  <select
                    value={agenciaEncomienda}
                    onChange={(e) => setAgenciaEncomienda(e.target.value as AgenciaEncomienda)}
                    className="w-full px-3.5 py-2.5 bg-white border-2 border-slate-300 rounded-xl text-sm font-semibold text-slate-900 focus:outline-none focus:border-[#0F223D]"
                  >
                    {AGENCIAS.map((ag) => (
                      <option key={ag} value={ag}>{ag}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-[11px] sm:text-xs font-semibold text-slate-800 uppercase tracking-wider mb-1">
                  N° Guía de Remisión / Clave (si ya fue despachado a la agencia)
                </label>
                <input
                  type="text"
                  value={numeroGuia}
                  onChange={(e) => setNumeroGuia(e.target.value)}
                  placeholder="ej. SH-789412 o OLV-993210"
                  className="w-full px-3.5 py-2.5 bg-white border-2 border-slate-300 rounded-xl text-sm font-mono font-medium text-slate-900 focus:outline-none focus:border-[#0F223D]"
                />
              </div>
            </div>
          )}
        </div>

        {/* 2. Datos del Cliente y Dirección Estructurada */}
        <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-sm border border-slate-200 mb-5">
          <h2 className="text-sm sm:text-base font-bold text-slate-900 mb-3 sm:mb-4 flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-8 h-8 bg-red-100 rounded-xl border border-red-200 shrink-0">
              <span className="material-icons text-red-600" style={{ fontSize: "18px" }}>person</span>
            </span>
            <span>2. Datos del Cliente y Entrega</span>
          </h2>
          <div className="space-y-3 sm:space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="sm:col-span-2">
                <label className="block text-[11px] sm:text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Nombre Completo <span className="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  placeholder="ej. Lady Luz Loayza Rodriguez"
                  className="w-full px-3.5 sm:px-4 py-2.5 sm:py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-sm sm:text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all shadow-inner"
                />
              </div>
              <div>
                <label className="block text-[11px] sm:text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  DNI / RUC {tipoEnvio === "Nacional" ? <span className="text-red-600 font-bold">* (Obligatorio)</span> : <span className="text-slate-400">(Opcional)</span>}
                </label>
                <input
                  type="text"
                  maxLength={11}
                  value={dniRuc}
                  onChange={(e) => setDniRuc(e.target.value.replace(/\D/g, ""))}
                  placeholder="ej. 72217190"
                  className="w-full px-3.5 sm:px-4 py-2.5 sm:py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-sm sm:text-base font-mono font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all shadow-inner"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-[11px] sm:text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Teléfono WhatsApp <span className="text-red-600">*</span>
                </label>
                <div className="relative">
                  <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-xs font-bold text-slate-500 font-mono">+51</span>
                  <input
                    type="tel"
                    maxLength={9}
                    value={telefono}
                    onChange={(e) => setTelefono(e.target.value.replace(/\D/g, ""))}
                    placeholder="960188015"
                    className="w-full pl-12 pr-4 py-2.5 sm:py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-sm sm:text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all shadow-inner"
                  />
                </div>
              </div>
              <div>
                <label className="block text-[11px] sm:text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Distrito / Localidad
                </label>
                <input
                  type="text"
                  value={distrito}
                  onChange={(e) => setDistrito(e.target.value)}
                  placeholder="ej. Carabayllo, Miraflores, Trujillo"
                  className="w-full px-3.5 sm:px-4 py-2.5 sm:py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-sm sm:text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all shadow-inner"
                />
              </div>
            </div>

            <div>
              <label className="block text-[11px] sm:text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                {tipoEnvio === "Nacional" ? "Dirección de Agencia de Destino *" : "Dirección Exacta de Entrega en Lima *"}
              </label>
              <input
                type="text"
                value={direccion}
                onChange={(e) => setDireccion(e.target.value)}
                placeholder={tipoEnvio === "Nacional" ? "ej. Agencia Shalom - Av. España 1020, Trujillo" : "ej. Jr. Vargas Machuca #332, El Progreso"}
                className="w-full px-3.5 sm:px-4 py-2.5 sm:py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-sm sm:text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all shadow-inner"
              />
            </div>

            <div>
              <label className="block text-[11px] sm:text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                Referencia de Entrega <span className="text-slate-400">(Muy importante para el reparto)</span>
              </label>
              <input
                type="text"
                value={referencia}
                onChange={(e) => setReferencia(e.target.value)}
                placeholder="ej. A espaldas de MiBanco, al costado del Hotel Cars, casa portón verde"
                className="w-full px-3.5 sm:px-4 py-2.5 sm:py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-sm sm:text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all shadow-inner"
              />
            </div>

            <div>
              <label className="block text-[11px] sm:text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">Canal de Pedido</label>
              <div className="grid grid-cols-3 gap-2">
                {CANALES.map((c) => (
                  <button
                    key={c}
                    type="button"
                    onClick={() => setCanal(c)}
                    className={`py-2.5 sm:py-3 px-1.5 sm:px-2 rounded-2xl text-xs sm:text-sm font-semibold border-2 transition-all flex items-center justify-center gap-1 sm:gap-1.5 ${
                      canal === c
                        ? "bg-[#0F223D] border-[#0F223D] text-white shadow-md ring-2 ring-slate-300"
                        : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100"
                    }`}
                  >
                    <span className="material-icons" style={{ fontSize: "16px" }}>
                      {c === "WhatsApp" ? "chat" : c === "Llamada" ? "call" : "laptop"}
                    </span>
                    <span>{c}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* 3. Selección de Prendas & Control de Stock */}
        <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-sm border border-slate-200 mb-5">
          <h2 className="text-sm sm:text-base font-bold text-slate-900 mb-3 sm:mb-4 flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-8 h-8 bg-emerald-100 rounded-xl border border-emerald-200 shrink-0">
              <span className="material-icons text-emerald-800" style={{ fontSize: "18px" }}>inventory_2</span>
            </span>
            <span>3. Selección de Prendas</span>
          </h2>
          <div className="flex flex-col sm:flex-row gap-2.5 mb-4">
            <select
              value={productoSeleccionado}
              onChange={(e) => setProductoSeleccionado(e.target.value)}
              className="flex-1 text-xs sm:text-base border-2 border-slate-300 rounded-2xl px-3 sm:px-4 py-2.5 sm:py-3 focus:outline-none focus:border-[#0F223D] bg-slate-50 font-semibold text-slate-900"
            >
              {productos.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.nombre} — S/{p.precio.toFixed(2)} {p.stock <= 5 ? `([ULTIMAS UNIDADES] Solo quedan ${p.stock} uds)` : `(Stock: ${p.stock})`}
                </option>
              ))}
            </select>
            <div className="flex gap-2">
              <input
                type="number"
                min="1"
                value={cantidad}
                onChange={(e) => setCantidad(Math.max(1, parseInt(e.target.value) || 1))}
                className="w-20 text-sm sm:text-base border-2 border-slate-300 rounded-2xl px-2 sm:px-3 py-2.5 sm:py-3 text-center focus:outline-none focus:border-[#0F223D] font-bold font-mono text-slate-900 bg-slate-50"
              />
              <button
                onClick={agregarItem}
                className="flex-1 sm:flex-initial px-4 sm:px-5 py-2.5 sm:py-3 bg-[#0F223D] hover:bg-[#1D3557] text-white rounded-2xl font-bold transition-all flex items-center justify-center gap-1.5 shadow-md text-xs sm:text-sm"
              >
                <span className="material-icons" style={{ fontSize: "18px" }}>add</span>
                <span>Agregar</span>
              </button>
            </div>
          </div>

          {items.length > 0 ? (
            <div className="border-2 border-slate-200 rounded-2xl overflow-x-auto shadow-inner mb-4">
              <table className="w-full min-w-[320px]">
                <thead>
                  <tr className="bg-slate-100 text-slate-700">
                    <th className="px-3 sm:px-4 py-2.5 sm:py-3 text-left text-xs font-semibold uppercase">Prenda</th>
                    <th className="px-2 sm:px-3 py-2.5 sm:py-3 text-center text-xs font-semibold uppercase">Cant.</th>
                    <th className="px-3 sm:px-4 py-2.5 sm:py-3 text-right text-xs font-semibold uppercase">Subtotal</th>
                    <th className="px-2 sm:px-3 py-2.5 sm:py-3 text-center text-xs font-semibold uppercase">Quitar</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((item, i) => (
                    <tr key={item.productoId} className={`transition-colors hover:bg-slate-50 ${i < items.length - 1 ? "border-b border-slate-200" : ""}`}>
                      <td className="px-3 sm:px-4 py-3 text-xs sm:text-sm font-semibold text-slate-900">{item.nombre}</td>
                      <td className="px-2 sm:px-3 py-3 text-xs sm:text-sm text-center text-slate-800 font-medium font-mono">{item.cantidad}</td>
                      <td className="px-3 sm:px-4 py-3 text-xs sm:text-sm text-right font-bold font-mono text-slate-950">S/{(item.cantidad * item.precio).toFixed(2)}</td>
                      <td className="px-2 sm:px-3 py-3 text-center">
                        <button
                          onClick={() => quitarItem(item.productoId)}
                          className="p-1.5 hover:bg-red-100 text-red-600 rounded-xl transition-colors"
                          aria-label="Quitar producto"
                        >
                          <span className="material-icons" style={{ fontSize: "18px" }}>delete</span>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="border-2 border-dashed border-slate-300 rounded-2xl py-8 text-center bg-slate-50 mb-4">
              <span className="material-icons text-slate-300 text-4xl sm:text-5xl block mb-2">add_shopping_cart</span>
              <p className="text-xs sm:text-sm text-slate-600 font-medium">Agrega al menos una prenda para continuar</p>
            </div>
          )}

          {/* Cupón Promocional */}
          <div className="bg-slate-50 rounded-2xl p-3.5 sm:p-4 border border-slate-200">
            <label className="block text-[11px] sm:text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <span className="material-icons text-amber-600" style={{ fontSize: "16px" }}>local_offer</span>
              Cupón de Descuento Promocional
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={codigoCuponInput}
                onChange={(e) => setCodigoCuponInput(e.target.value.toUpperCase())}
                placeholder="ej. LEOFIT10 o PROMOVERANO"
                className="flex-1 px-3.5 py-2.5 bg-white border-2 border-slate-300 rounded-xl text-xs sm:text-sm font-mono font-bold text-slate-900 focus:outline-none focus:border-[#0F223D]"
              />
              <button
                type="button"
                onClick={handleAplicarCupon}
                className="px-4 py-2.5 bg-[#0F223D] hover:bg-[#1D3557] text-white font-bold text-xs sm:text-sm rounded-xl transition-all shadow-sm shrink-0"
              >
                Aplicar
              </button>
            </div>

            {mensajeCupon && (
              <div className={`mt-2 text-xs font-bold flex items-center gap-1 ${mensajeCupon.tipo === "exito" ? "text-emerald-700" : "text-red-600"}`}>
                <span className="material-icons" style={{ fontSize: "15px" }}>
                  {mensajeCupon.tipo === "exito" ? "check_circle" : "error"}
                </span>
                <span>{mensajeCupon.texto}</span>
                {cuponAplicado && (
                  <button onClick={handleRemoverCupon} className="text-slate-500 hover:text-red-700 underline ml-2 font-normal">
                    Quitar cupón
                  </button>
                )}
              </div>
            )}
          </div>
        </div>

        {/* 4. Método de Pago & Desglose Financiero */}
        <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-sm border border-slate-200 mb-5">
          <h2 className="text-sm sm:text-base font-bold text-slate-900 mb-3 sm:mb-4 flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-8 h-8 bg-purple-100 rounded-xl border border-purple-200 shrink-0">
              <span className="material-icons text-purple-700" style={{ fontSize: "18px" }}>payments</span>
            </span>
            <span>4. Método de Pago y Liquidación</span>
          </h2>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 sm:gap-2.5 mb-4">
            {METODOS_PAGO.map((m) => {
              const seleccionado = metodoPago === m.id;
              return (
                <button
                  key={m.id}
                  type="button"
                  onClick={() => setMetodoPago(m.id)}
                  className={`p-2.5 sm:p-3 rounded-2xl border-2 text-left transition-all flex items-center gap-2 ${
                    seleccionado
                      ? "border-[#0F223D] bg-[#0F223D] text-white shadow-md ring-2 ring-slate-300"
                      : "border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100"
                  }`}
                >
                  <span className={`w-7 h-7 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 ${m.color}`}>
                    <span className="material-icons" style={{ fontSize: "16px" }}>{m.icon}</span>
                  </span>
                  <span className="text-xs sm:text-sm font-bold truncate">{m.label}</span>
                </button>
              );
            })}
          </div>

          {(metodoPago === "Yape" || metodoPago === "Plin" || metodoPago.startsWith("Transferencia")) && (
            <div className="mb-4">
              <label className="block text-[11px] sm:text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                N° de Operación / Código de Constancia
              </label>
              <input
                type="text"
                value={numeroOperacion}
                onChange={(e) => setNumeroOperacion(e.target.value)}
                placeholder="ej. OP-982143 o BCP-8834120"
                className="w-full px-3.5 py-2.5 bg-slate-50 border-2 border-slate-200 rounded-xl text-xs sm:text-sm font-mono font-medium text-slate-900 focus:outline-none focus:border-[#0F223D] focus:bg-white"
              />
            </div>
          )}

          {/* Desglose económico */}
          <div className="border-t-2 border-slate-200 pt-4 space-y-2.5">
            <div className="flex items-center justify-between text-xs sm:text-sm font-semibold text-slate-700">
              <span>Subtotal de Prendas</span>
              <span className="text-sm sm:text-base font-bold font-mono text-slate-900">S/{subtotal.toFixed(2)}</span>
            </div>
            <div className="flex items-center justify-between text-xs sm:text-sm font-semibold text-slate-700">
              <label>{tipoEnvio === "Nacional" ? "Costo Encomienda (S/)" : "Costo Delivery Local (S/)"}</label>
              <input
                type="number"
                min="0"
                step="1"
                value={costoDelivery}
                onChange={(e) => setCostoDelivery(Math.max(0, parseFloat(e.target.value) || 0))}
                className="w-20 sm:w-24 text-sm sm:text-base font-bold font-mono border-2 border-slate-300 rounded-xl px-2.5 sm:px-3 py-1 text-right focus:outline-none focus:border-[#0F223D] bg-white text-slate-900 shadow-sm"
              />
            </div>
            {cuponAplicado && (
              <div className="flex items-center justify-between text-xs sm:text-sm font-bold text-emerald-700">
                <span>Cupón ({cuponAplicado.codigo})</span>
                <span className="font-mono">-S/{cuponAplicado.descuento.toFixed(2)}</span>
              </div>
            )}
            <div className="flex items-center justify-between text-xs sm:text-sm font-semibold text-slate-700">
              <label>Descuento Adicional Manual (S/)</label>
              <input
                type="number"
                min="0"
                step="1"
                value={descuentoManual}
                onChange={(e) => setDescuentoManual(Math.max(0, parseFloat(e.target.value) || 0))}
                className="w-20 sm:w-24 text-sm sm:text-base font-bold font-mono border-2 border-emerald-400 rounded-xl px-2.5 sm:px-3 py-1 text-right focus:outline-none focus:border-emerald-600 bg-white text-emerald-900 shadow-sm"
              />
            </div>
            <div className="flex items-center justify-between bg-[#0F223D] rounded-2xl px-4 sm:px-5 py-3.5 sm:py-4 text-white shadow-md mt-3">
              <div>
                <span className="text-xs sm:text-sm font-semibold text-slate-300 block">Total a Cobrar</span>
                <span className="text-[10px] text-amber-300 uppercase tracking-wide font-bold">Pago: {metodoPago}</span>
              </div>
              <span className="text-xl sm:text-3xl font-extrabold font-display text-amber-400">S/{total.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* 5. Notas y Garantía */}
        <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-sm border border-slate-200 mb-6">
          <h2 className="text-sm sm:text-base font-bold text-slate-900 mb-2 sm:mb-3 flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-8 h-8 bg-amber-100 rounded-xl border border-amber-200 shrink-0">
              <span className="material-icons text-amber-700" style={{ fontSize: "18px" }}>notes</span>
            </span>
            <span>Notas Especiales</span>
            <span className="text-xs text-slate-500 font-normal ml-1">(opcional)</span>
          </h2>
          <textarea
            value={notas}
            onChange={(e) => setNotas(e.target.value)}
            placeholder="ej. Llevar sencillo de S/ 50, entregar en portería si no responden..."
            rows={2}
            className="w-full px-3.5 sm:px-4 py-2.5 sm:py-3 bg-slate-50 border-2 border-slate-200 rounded-2xl text-xs sm:text-sm font-normal text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#0F223D] focus:bg-white transition-all resize-none shadow-inner leading-relaxed"
          />

          {/* Sello de Garantía LeoFit */}
          <div className="mt-3 bg-emerald-50 border border-emerald-200 rounded-2xl p-3 flex items-center gap-2.5">
            <span className="material-icons text-emerald-700 text-2xl shrink-0">verified_user</span>
            <div className="text-xs text-emerald-950 font-medium">
              <strong>Garantía Oficial LeoFit:</strong> Cambio por falla de fábrica o talla garantizado dentro de los 7 días.
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col-reverse sm:flex-row gap-2.5 sm:gap-4">
          <button
            onClick={() => navegarA("dashboard")}
            className="w-full sm:flex-1 py-3 sm:py-3.5 border-2 border-slate-300 text-slate-700 font-bold text-sm sm:text-base rounded-2xl hover:bg-slate-100 transition-colors shadow-sm"
          >
            Cancelar
          </button>
          <button
            onClick={handleGuardar}
            className="w-full sm:flex-[2] py-3 sm:py-3.5 bg-emerald-700 hover:bg-emerald-800 active:scale-[0.98] text-white font-bold text-sm sm:text-base rounded-2xl transition-all flex items-center justify-center gap-2 shadow-xl shadow-emerald-700/30 ring-2 ring-white"
          >
            <span className="material-icons" style={{ fontSize: "20px" }}>save</span>
            <span>Guardar y Registrar Pedido</span>
          </button>
        </div>
      </div>
    </div>
  );
}

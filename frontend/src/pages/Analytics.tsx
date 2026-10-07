/**
 * @file Analytics.tsx
 * @description Tablero estratégico de análisis y reportes históricos.
 * @project LeoFit Pedidos Sistema (UTP)
 */

import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from "recharts";
import { useApp } from "../context/AppContext";

export default function Analytics() {
  const { modoAccesible } = useApp();

  const dataSemanal = [
    { name: 'Lun', pedidos: 4, ingresos: 350 },
    { name: 'Mar', pedidos: 3, ingresos: 210 },
    { name: 'Mie', pedidos: 6, ingresos: 580 },
    { name: 'Jue', pedidos: 2, ingresos: 120 },
    { name: 'Vie', pedidos: 8, ingresos: 940 },
    { name: 'Sab', pedidos: 5, ingresos: 430 },
    { name: 'Dom', pedidos: 7, ingresos: 670 }
  ];

  const dataCategorias = [
    { name: 'Tops', ventas: 120 },
    { name: 'Bottoms', ventas: 95 },
    { name: 'Accesorios', ventas: 40 },
    { name: 'Packs', ventas: 65 },
  ];

  return (
    <div className={`pt-16 pb-32 sm:pb-28 min-h-screen ${modoAccesible ? "bg-[#E2E8F0]" : "bg-[#F1FAEE]"}`}>
      <div className="max-w-5xl mx-auto px-3 sm:px-6 py-4 space-y-4 sm:space-y-5">
        
        <div className="flex flex-col gap-1">
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">Reportes y Analíticas</h1>
          <p className="text-sm text-slate-600">Visualización estratégica del desempeño histórico.</p>
        </div>

        {/* Gráfico Principal */}
        <div className="bg-white rounded-3xl p-5 shadow-sm border border-slate-200">
          <h2 className="text-base font-bold text-slate-900 mb-6">Ingresos Brutos (Últimos 7 días)</h2>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={dataSemanal} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorIngresos" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(val) => `S/${val}`} />
                <Tooltip contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }} />
                <Area type="monotone" dataKey="ingresos" stroke="#10B981" strokeWidth={3} fillOpacity={1} fill="url(#colorIngresos)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Gráficos Secundarios */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white rounded-3xl p-5 shadow-sm border border-slate-200">
            <h2 className="text-base font-bold text-slate-900 mb-6">Volumen de Pedidos (Unidades)</h2>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={dataSemanal} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip cursor={{ fill: '#f1f5f9' }} contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                  <Bar dataKey="pedidos" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-white rounded-3xl p-5 shadow-sm border border-slate-200">
            <h2 className="text-base font-bold text-slate-900 mb-6">Ventas por Categoría</h2>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart layout="vertical" data={dataCategorias} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
                  <XAxis type="number" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis dataKey="name" type="category" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} width={80} />
                  <Tooltip cursor={{ fill: '#f1f5f9' }} contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                  <Bar dataKey="ventas" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

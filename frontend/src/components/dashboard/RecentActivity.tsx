import { useState, useEffect } from "react";
import { apiFetch } from "../../services/api";

export interface ActivityRecord {
  id: number;
  order_id: number;
  user_id?: number | null;
  previous_status?: string | null;
  new_status: string;
  changed_at: string;
  comments?: string | null;
  order_number: string;
  client_name: string;
  user_name: string;
}

export default function RecentActivity() {
  const [actividad, setActividad] = useState<ActivityRecord[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchActivity = async () => {
      try {
        const USE_MOCK = import.meta.env.VITE_USE_MOCK_ORDERS === 'true';
        if (USE_MOCK) {
          // Si estamos en mock, mostramos data dummy simulada
          setActividad([
            {
              id: 1, order_id: 101, new_status: 'RECIBIDO', changed_at: new Date().toISOString(), order_number: 'ORD-2026-001', client_name: 'Juan Perez', user_name: 'Admin'
            },
            {
              id: 2, order_id: 102, previous_status: 'RECIBIDO', new_status: 'PREPARACION', changed_at: new Date(Date.now() - 3600000).toISOString(), order_number: 'ORD-2026-002', client_name: 'Maria Gomez', user_name: 'Operador'
            }
          ]);
          setCargando(false);
          return;
        }

        const data = await apiFetch<ActivityRecord[]>("/api/dashboard/activity");
        setActividad(data || []);
      } catch (err: any) {
        setError(err.message || 'Error al cargar la actividad');
      } finally {
        setCargando(false);
      }
    };
    fetchActivity();
  }, []);

  if (cargando) {
    return (
      <div className="bg-white rounded-3xl p-5 shadow-sm border border-slate-200 animate-pulse h-64 flex items-center justify-center">
        <span className="text-slate-400 font-medium">Cargando línea de tiempo...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 rounded-3xl p-5 shadow-sm border border-red-200 text-red-800 text-sm">
        <span className="font-bold">Error: </span> {error}
      </div>
    );
  }

  if (actividad.length === 0) {
    return (
      <div className="bg-white rounded-3xl p-5 shadow-sm border border-slate-200 text-center py-10">
        <span className="material-icons text-slate-300 mb-2" style={{ fontSize: '48px' }}>history</span>
        <p className="text-slate-500 font-medium text-sm">No hay actividad reciente registrada.</p>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'RECIBIDO': return 'bg-blue-500';
      case 'PREPARACION': return 'bg-amber-500';
      case 'EN_CAMINO': return 'bg-orange-500';
      case 'ENTREGADO': return 'bg-emerald-500';
      case 'CANCELADO': return 'bg-red-500';
      default: return 'bg-slate-500';
    }
  };

  return (
    <div className="bg-white rounded-3xl p-5 shadow-sm border border-slate-200">
      <div className="flex items-center gap-2 mb-5">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <span className="material-icons text-slate-600">timeline</span>
          Línea de Tiempo (Actividad)
        </h2>
      </div>
      
      <div className="relative border-l-2 border-slate-100 ml-3 space-y-6 pb-2">
        {actividad.map((evento) => {
          const hora = new Date(evento.changed_at).toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' });
          const dia = new Date(evento.changed_at).toLocaleDateString('es-PE', { day: 'numeric', month: 'short' });
          
          return (
            <div key={evento.id} className="relative pl-6">
              <span className={`absolute -left-[9px] top-1 w-4 h-4 rounded-full border-2 border-white shadow-sm ${getStatusColor(evento.new_status)}`} />
              
              <div className="flex flex-col sm:flex-row sm:items-baseline gap-1 sm:gap-2 mb-0.5">
                <span className="text-xs font-bold text-slate-800 bg-slate-100 px-2 py-0.5 rounded border border-slate-200 self-start">
                  {evento.order_number}
                </span>
                <span className="text-xs font-bold text-slate-500">
                  {dia} · {hora}
                </span>
              </div>
              
              <p className="text-sm text-slate-700 leading-snug mt-1.5">
                <span className="font-semibold text-slate-900">{evento.user_name}</span>{' '}
                {evento.previous_status ? 'actualizó el pedido de' : 'registró el pedido de'}{' '}
                <span className="font-semibold text-slate-900">{evento.client_name}</span>
                {evento.previous_status && (
                  <>
                    {' '}de <span className="text-slate-500 font-medium line-through">{evento.previous_status}</span>
                  </>
                )}
                {' '}a <span className={`font-bold text-xs px-1.5 py-0.5 rounded text-white ${getStatusColor(evento.new_status)}`}>{evento.new_status}</span>
              </p>
              
              {evento.comments && (
                <p className="text-xs text-slate-500 mt-1.5 italic bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-100 inline-block">
                  "{evento.comments}"
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

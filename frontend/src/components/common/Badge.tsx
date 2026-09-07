import { EstadoPedido } from "../../data/mockData";

const configs: Record<EstadoPedido, { bg: string; text: string; border: string; icon: string; label: string }> = {
  Recibido:     { bg: "bg-blue-100", text: "text-blue-950", border: "border-blue-400", icon: "inbox", label: "Recibido" },
  "Preparación":{ bg: "bg-amber-100", text: "text-amber-950", border: "border-amber-400", icon: "inventory_2", label: "Preparación" },
  Camino:       { bg: "bg-orange-100", text: "text-orange-950", border: "border-orange-400", icon: "local_shipping", label: "En Camino" },
  Entregado:    { bg: "bg-emerald-100", text: "text-emerald-950", border: "border-emerald-500", icon: "check_circle", label: "Entregado" },
  Cancelado:    { bg: "bg-slate-200", text: "text-slate-800", border: "border-slate-400", icon: "cancel", label: "Cancelado" },
};

interface BadgeProps {
  estado: EstadoPedido;
  enRiesgo?: boolean;
}

export default function Badge({ estado, enRiesgo = false }: BadgeProps) {
  const cfg = configs[estado] || configs.Recibido;
  return (
    <span className="inline-flex items-center gap-1.5 flex-wrap">
      <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-black border ${cfg.bg} ${cfg.text} ${cfg.border} shadow-sm`}>
        <span className="material-icons" style={{ fontSize: "14px" }}>{cfg.icon}</span>
        {cfg.label}
      </span>
      {enRiesgo && (
        <span
          className="inline-flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-black bg-red-600 text-white border border-red-700 shadow-sm animate-pulse"
          title="Este pedido lleva más de 24 horas sin actualizarse"
        >
          <span className="material-icons" style={{ fontSize: "14px" }}>warning</span>
          En Riesgo
        </span>
      )}
    </span>
  );
}

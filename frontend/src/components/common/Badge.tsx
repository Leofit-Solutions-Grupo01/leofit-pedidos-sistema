import { EstadoPedido } from "../../data/mockData";

const configs: Record<EstadoPedido, { className: string; label: string }> = {
  Recibido:     { className: "bg-[#3498DB]/15 text-[#3498DB] border border-[#3498DB]/30",    label: "Recibido" },
  "Preparación":{ className: "bg-[#F1C40F]/15 text-[#B7950B] border border-[#F1C40F]/40",   label: "Preparación" },
  Camino:       { className: "bg-[#E67E22]/15 text-[#E67E22] border border-[#E67E22]/30",    label: "En Camino" },
  Entregado:    { className: "bg-[#27AE60]/15 text-[#27AE60] border border-[#27AE60]/30",    label: "Entregado" },
  Cancelado:    { className: "bg-gray-100 text-gray-400 border border-gray-200",              label: "Cancelado" },
};

interface BadgeProps {
  estado: EstadoPedido;
  enRiesgo?: boolean;
}

export default function Badge({ estado, enRiesgo = false }: BadgeProps) {
  const { className, label } = configs[estado];
  return (
    <span className="inline-flex items-center gap-1">
      <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold whitespace-nowrap ${className}`}>
        {label}
      </span>
      {enRiesgo && (
        <span
          className="inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-[#E63946]/10 text-[#E63946] border border-[#E63946]/20 whitespace-nowrap"
          title="Este pedido lleva más de 24 horas sin actualizarse"
        >
          En Riesgo
        </span>
      )}
    </span>
  );
}

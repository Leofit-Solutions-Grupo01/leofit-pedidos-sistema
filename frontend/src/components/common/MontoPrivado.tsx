// Muestra un monto monetario o lo oculta según el modo privacidad
interface Props {
  valor: number;
  privacidad: boolean;
  className?: string;
  prefijo?: string;
}

export default function MontoPrivado({ valor, privacidad, className = "", prefijo = "S/" }: Props) {
  return (
    <span className={className}>
      {privacidad ? (
        <span className="tracking-widest text-current opacity-40 select-none">••••</span>
      ) : (
        `${prefijo}${valor.toFixed(2)}`
      )}
    </span>
  );
}

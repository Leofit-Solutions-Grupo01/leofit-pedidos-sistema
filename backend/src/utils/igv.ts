import Decimal from 'decimal.js';

/**
 * Desglose exacto de IGV 18% con redondeo bancario y ajuste de tolerancia cero.
 * Garantiza: subtotal + igv === total con precisión de centavos, previniendo rechazos de SUNAT.
 */
export function splitIgv(totalCents: number) {
  const total = new Decimal(totalCents).div(100);
  const subtotal = total.div(1.18).toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
  const igv = total.minus(subtotal).toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
  // Ajuste de 1 centavo si la suma no cuadra exacto por redondeo
  const drift = total.minus(subtotal.plus(igv));
  const igvFinal = igv.plus(drift);
  return {
    total: total.toNumber(),
    subtotal: subtotal.toNumber(),
    igv: igvFinal.toNumber(),
    totalCents: Math.round(total.toNumber() * 100),
    subtotalCents: Math.round(subtotal.toNumber() * 100),
    igvCents: Math.round(igvFinal.toNumber() * 100),
  };
}

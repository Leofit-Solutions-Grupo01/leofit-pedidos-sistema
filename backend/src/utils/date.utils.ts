/**
 * @file date.utils.ts
 * @description Utilidades de fecha y hora localizadas para Perú (Zona horaria: America/Lima, UTC-5).
 * Garantiza consistencia en números de pedido, facturación electrónica SUNAT y pistas de auditoría.
 */

/**
 * Retorna la fecha actual en formato compacto YYYYMMDD en zona horaria America/Lima.
 * Ejemplo: "20261105"
 */
export function getLimaDateStr(date: Date = new Date()): string {
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Lima',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  return formatter.format(date).replace(/-/g, '');
}

/**
 * Retorna la fecha actual en formato ISO YYYY-MM-DD en zona horaria America/Lima.
 * Ejemplo: "2026-11-05"
 */
export function getLimaIsoDate(date: Date = new Date()): string {
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Lima',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  return formatter.format(date);
}


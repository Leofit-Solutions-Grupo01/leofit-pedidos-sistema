/**
 * @file dateUtils.ts
 * @description Utilidades de fecha y hora localizadas para Perú (America/Lima - UTC-5).
 * Evita saltos de fecha hacia el día siguiente por desfase con UTC.
 */

export function getLimaDateToday(): string {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Lima',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).format(new Date());
}

export function getLimaDisplayDate(date: Date = new Date()): string {
  return new Intl.DateTimeFormat('es-PE', {
    timeZone: 'America/Lima',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date);
}

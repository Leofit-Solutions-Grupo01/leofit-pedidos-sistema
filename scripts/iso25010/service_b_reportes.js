// =============================================================================
// SERVICIO B - "Reportes LeoFit" (carga conocida para prueba de coexistencia)
// ISO/IEC 25010:2023 - Compatibilidad / Coexistencia (Semana 11)
// -----------------------------------------------------------------------------
// Servicio HTTP independiente, sin dependencias externas, que simula un proceso
// de generación de reportes que comparte host (CPU, RAM) con la API LeoFit.
// Cada GET /report genera N registros de venta sintéticos (sin datos personales),
// los agrega por categoría, ordena y calcula un hash SHA-256 del resultado.
// Uso: node scripts/iso25010/service_b_reportes.js [puerto] [registros]
// =============================================================================
const http = require('http');
const crypto = require('crypto');

const PORT = parseInt(process.argv[2] || process.env.SERVICE_B_PORT || '4100', 10);
const RECORDS = parseInt(process.argv[3] || process.env.SERVICE_B_RECORDS || '40000', 10);
const CATEGORIES = ['POLOS', 'SHORTS', 'CASACAS', 'BUZOS', 'MEDIAS', 'GORRAS'];

function buildReport() {
  const rows = new Array(RECORDS);
  for (let i = 0; i < RECORDS; i++) {
    rows[i] = {
      id: i,
      category: CATEGORIES[i % CATEGORIES.length],
      qty: (i * 7) % 13 + 1,
      price: ((i * 31) % 200) + 19.9,
    };
  }
  const totals = {};
  for (const r of rows) {
    totals[r.category] = (totals[r.category] || 0) + r.qty * r.price;
  }
  rows.sort((a, b) => b.qty * b.price - a.qty * a.price);
  const payload = JSON.stringify({ totals, top: rows.slice(0, 20) });
  const digest = crypto.createHash('sha256').update(JSON.stringify(rows)).digest('hex');
  return { records: RECORDS, totals, digest, bytes: payload.length };
}

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'UP', service: 'reportes-b' }));
  }
  if (req.url && req.url.startsWith('/report')) {
    try {
      const report = buildReport();
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify(report));
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ error: String(err) }));
    }
  }
  res.writeHead(404);
  res.end();
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`[Servicio B - Reportes] escuchando en http://127.0.0.1:${PORT} (registros por reporte: ${RECORDS})`);
});

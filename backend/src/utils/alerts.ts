/**
 * @file alerts.ts
 * @description Sistema de Alertas Operativas para Slack Webhook ante incidentes 5xx y fallos de infraestructura.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

export async function alertSlack(message: string, fields: Record<string, any> = {}): Promise<void> {
  const url = process.env.SLACK_WEBHOOK_URL;
  if (!url) return;

  const text = Object.entries(fields)
    .map(([k, v]) => `• *${k}*: \`${String(v).slice(0, 200)}\``)
    .join('\n');

  try {
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: `🚨 ${message}\n${text}` }),
    });
  } catch {
    // Silencioso ante fallos de conexión al webhook externo
  }
}

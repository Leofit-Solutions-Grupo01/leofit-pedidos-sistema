/**
 * @file culqi.ts
 * @description Integración con la pasarela de pagos Culqi (checkout idempotente y reuso de enlaces).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import { dbPool, isPostgresAvailable } from '../../config/database';
import { memoryPayments } from '../../controllers/paymentWebhook.controller';

export interface CulqiCheckoutParams {
  id: number;
  totalCents: number;
  email: string;
}

export interface CulqiCheckoutResult {
  checkoutUrl: string;
  providerOrderId: string;
  reused?: boolean;
}

export async function createOrReuseCulqiCheckout(order: CulqiCheckoutParams): Promise<CulqiCheckoutResult> {
  // 1) ¿Ya existe un checkout PENDING para este pedido? -> Reusar (idempotencia real)
  if (isPostgresAvailable()) {
    const existing = await dbPool.query(
      `SELECT raw_response->>'checkout_url' AS url,
              provider_charge_id
         FROM payments
        WHERE order_id = $1
          AND provider = 'culqi'
          AND status = 'PENDING'
        ORDER BY created_at DESC LIMIT 1`,
      [order.id]
    );

    if (existing.rows[0]?.url) {
      return {
        checkoutUrl: existing.rows[0].url,
        providerOrderId: existing.rows[0].provider_charge_id,
        reused: true
      };
    }
  } else {
    const existingMem = memoryPayments.find(
      (p) => p.orderId === order.id && p.provider === 'culqi' && p.status === 'PENDING'
    );
    if (existingMem?.rawResponse?.checkout_url) {
      return {
        checkoutUrl: existingMem.rawResponse.checkout_url,
        providerOrderId: existingMem.providerChargeId,
        reused: true
      };
    }
  }

  // 2) Crear nuevo checkout en Culqi (o fallback sandbox)
  const secretKey = process.env.CULQI_SECRET_KEY;
  let body: any;

  if (secretKey && secretKey.startsWith('sk_')) {
    const res = await fetch('https://api.culqi.com/v2/orders', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${secretKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        amount: order.totalCents,
        currency_code: 'PEN',
        description: `Pedido #${order.id} — LeoFit`,
        order_number: `LEO-${order.id}`,
        client_details: { email: order.email },
        metadata: { order_id: String(order.id) }
      })
    });

    if (!res.ok) {
      throw new Error(`CULQI_ERROR_${res.status}`);
    }
    body = await res.json();
  } else {
    const mockId = `ord_live_mock_${order.id}_${Date.now()}`;
    body = {
      id: mockId,
      checkout_url: `https://checkout.culqi.com/sandbox/#/order/${mockId}`
    };
  }

  const checkoutUrl = body.checkout_url || `https://checkout.culqi.com/#/order/${body.id}`;
  const providerOrderId = body.id;

  // 3) Persistir pago PENDING (idempotente por provider_charge_id)
  if (isPostgresAvailable()) {
    await dbPool.query(
      `INSERT INTO payments
         (order_id, provider, provider_charge_id, amount_cents, currency, status, raw_response)
       VALUES ($1, 'culqi', $2, $3, 'PEN', 'PENDING', $4)
       ON CONFLICT (provider, provider_charge_id) DO NOTHING`,
      [order.id, providerOrderId, order.totalCents, JSON.stringify(body)]
    );
  } else {
    memoryPayments.push({
      orderId: order.id,
      provider: 'culqi',
      providerChargeId: providerOrderId,
      amountCents: order.totalCents,
      currency: 'PEN',
      status: 'PENDING',
      rawResponse: body
    });
  }

  return { checkoutUrl, providerOrderId, reused: false };
}

// Alias de conveniencia retrocompatible
export const createCulqiCheckout = createOrReuseCulqiCheckout;

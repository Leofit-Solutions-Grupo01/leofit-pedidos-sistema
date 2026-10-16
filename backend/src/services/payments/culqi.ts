/**
 * @file culqi.ts
 * @description Integración con la pasarela de pagos Culqi (checkout y preferencias de pago).
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

export interface CulqiCheckoutParams {
  id: number;
  totalCents: number;
  email: string;
}

export interface CulqiCheckoutResult {
  checkoutUrl: string;
  providerOrderId: string;
}

export async function createCulqiCheckout(order: CulqiCheckoutParams): Promise<CulqiCheckoutResult> {
  const secretKey = process.env.CULQI_SECRET_KEY;

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

    const body = (await res.json()) as any;
    return {
      checkoutUrl: body.checkout_url || `https://checkout.culqi.com/#/order/${body.id}`,
      providerOrderId: body.id
    };
  }

  // Fallback seguro de sandbox para entornos de prueba o desarrollo local
  const mockId = `ord_live_mock_${order.id}_${Date.now()}`;
  return {
    checkoutUrl: `https://checkout.culqi.com/sandbox/#/order/${mockId}`,
    providerOrderId: mockId
  };
}

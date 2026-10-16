/**
 * @file stateMachine.ts
 * @description Máquina de estados formal para el ciclo de vida de pedidos en LeoFit.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import type { PoolClient } from 'pg';
import { InMemoryDataStore } from '../../infrastructure/repositories/memory.repositories';

export type OrderState =
  | 'PENDIENTE'
  | 'PAGADO'
  | 'PREPARACION'
  | 'EN_CAMINO'
  | 'ENTREGADO'
  | 'CANCELADO'
  | 'REEMBOLSADO';

const TRANSICIONES: Record<OrderState, OrderState[]> = {
  PENDIENTE:   ['PAGADO', 'CANCELADO'],
  PAGADO:      ['PREPARACION', 'REEMBOLSADO', 'CANCELADO'],
  PREPARACION: ['EN_CAMINO', 'CANCELADO'],
  EN_CAMINO:   ['ENTREGADO', 'CANCELADO'],
  ENTREGADO:   ['REEMBOLSADO'],
  CANCELADO:   [],
  REEMBOLSADO: []
};

export interface TransitionResult {
  from: OrderState;
  to: OrderState;
  noop: boolean;
}

export async function transitionOrder(
  client: PoolClient | null,
  orderId: number,
  to: OrderState,
  actor: string,
  metadata: Record<string, any> = {}
): Promise<TransitionResult> {
  if (client) {
    // SELECT ... FOR UPDATE serializa transiciones concurrentes en Postgres
    const { rows } = await client.query(
      `SELECT COALESCE(estado, status, 'PENDIENTE') as estado FROM orders WHERE id = $1 FOR UPDATE`,
      [orderId]
    );

    if (!rows[0]) {
      throw Object.assign(new Error('ORDER_NOT_FOUND'), { status: 404, code: 'ORDER_NOT_FOUND' });
    }

    let rawFrom = (rows[0].estado || 'PENDIENTE').toUpperCase();
    if (rawFrom === 'RECIBIDO') rawFrom = 'PENDIENTE';

    const from = rawFrom as OrderState;
    if (from === to) {
      return { from, to, noop: true };
    }

    const allowed = TRANSICIONES[from] || [];
    if (!allowed.includes(to)) {
      throw Object.assign(new Error(`Transición inválida de ${from} a ${to}`), {
        status: 409,
        code: 'INVALID_TRANSITION',
        from,
        to
      });
    }

    const timestampColMap: Partial<Record<OrderState, string>> = {
      PAGADO: 'paid_at',
      EN_CAMINO: 'shipped_at',
      ENTREGADO: 'delivered_at',
      CANCELADO: 'cancelled_at'
    };
    const timestampCol = timestampColMap[to];

    await client.query(
      `UPDATE orders
          SET estado = $1,
              status = $1
              ${timestampCol ? `, ${timestampCol} = NOW()` : ''}
        WHERE id = $2`,
      [to, orderId]
    );

    await client.query(
      `INSERT INTO order_state_transitions (order_id, from_state, to_state, actor, metadata)
       VALUES ($1, $2, $3, $4, $5)`,
      [orderId, from, to, actor, JSON.stringify(metadata)]
    );

    return { from, to, noop: false };
  } else {
    // Modo memoria (pruebas unitarias sin conexión a Postgres)
    const order = InMemoryDataStore.orders.find((o) => o.id === orderId);
    if (!order) {
      throw Object.assign(new Error('ORDER_NOT_FOUND'), { status: 404, code: 'ORDER_NOT_FOUND' });
    }

    let rawFrom = ((order as any).estado || order.status || 'PENDIENTE').toUpperCase();
    if (rawFrom === 'RECIBIDO') rawFrom = 'PENDIENTE';

    const from = rawFrom as OrderState;
    if (from === to) {
      return { from, to, noop: true };
    }

    const allowed = TRANSICIONES[from] || [];
    if (!allowed.includes(to)) {
      throw Object.assign(new Error(`Transición inválida de ${from} a ${to}`), {
        status: 409,
        code: 'INVALID_TRANSITION',
        from,
        to
      });
    }

    (order as any).estado = to;
    order.status = (to === 'PENDIENTE' ? 'RECIBIDO' : to) as any;

    if (to === 'PAGADO') (order as any).paid_at = new Date();
    if (to === 'EN_CAMINO') (order as any).shipped_at = new Date();
    if (to === 'ENTREGADO') (order as any).delivered_at = new Date();
    if (to === 'CANCELADO') (order as any).cancelled_at = new Date();

    return { from, to, noop: false };
  }
}

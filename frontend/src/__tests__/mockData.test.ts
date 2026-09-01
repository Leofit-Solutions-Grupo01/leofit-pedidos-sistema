import { describe, it, expect } from 'vitest';
import { productosIniciales, pedidosIniciales, type Producto, type Pedido } from '../data/mockData';

describe('Inventario y Productos Iniciales', () => {
  it('debe contener productos con estructura válida y stock no negativo', () => {
    expect(productosIniciales.length).toBeGreaterThan(0);
    productosIniciales.forEach((producto: Producto) => {
      expect(producto.id).toBeDefined();
      expect(producto.nombre.length).toBeGreaterThan(0);
      expect(producto.precio).toBeGreaterThan(0);
      expect(producto.stock).toBeGreaterThanOrEqual(0);
      expect(['Deportiva', 'Casual', 'Accesorios']).toContain(producto.categoria);
    });
  });

  it('debe tener identificadores de producto únicos', () => {
    const ids = productosIniciales.map((p) => p.id);
    const uniqueIds = new Set(ids);
    expect(uniqueIds.size).toBe(ids.length);
  });
});

describe('Gestión de Pedidos Iniciales', () => {
  it('debe contener pedidos iniciales con identificador y cliente válido', () => {
    expect(pedidosIniciales.length).toBeGreaterThan(0);
    pedidosIniciales.forEach((pedido: Pedido) => {
      expect(pedido.id).toBeDefined();
      expect(pedido.numero).toMatch(/^LFT-\d{3}$/);
      expect(pedido.cliente.nombre).toBeDefined();
      expect(pedido.cliente.telefono).toMatch(/^\d{9}$/);
      expect(pedido.items.length).toBeGreaterThan(0);
      expect(pedido.total).toBeGreaterThan(0);
      expect(['Recibido', 'Preparación', 'Camino', 'Entregado', 'Cancelado']).toContain(pedido.estado);
    });
  });

  it('debe calcular consistencia entre items y subtotales en pedidos', () => {
    pedidosIniciales.forEach((pedido) => {
      const itemsSum = pedido.items.reduce((acc, item) => acc + item.cantidad * item.precio, 0);
      expect(itemsSum).toBeGreaterThan(0);
      expect(pedido.total).toBeCloseTo(itemsSum, 1);
    });
  });
});

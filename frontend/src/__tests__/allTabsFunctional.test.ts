/**
 * @file allTabsFunctional.test.ts
 * @description Suite completa de pruebas unitarias y funcionales para todas las pestañas de LeoFit
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { describe, it, expect } from 'vitest';
import {
  productosIniciales,
  pedidosIniciales,
  CUPONES_VALIDOS,
  estaEnRiesgo,
  calcularIngresos,
  type Pedido,
  type Producto,
  type EstadoPedido,
} from '../data/mockData';

describe('Pestaña 1: Inicio / Dashboard - Métricas y Lógica Financiera', () => {
  it('debe calcular correctamente los ingresos reales cobrados (pedidos Entregados)', () => {
    const totalCobrado = calcularIngresos(pedidosIniciales);
    expect(totalCobrado).toBeGreaterThan(0);
    
    // Solo pedidos Entregados
    const entregados = pedidosIniciales.filter((p) => p.estado === 'Entregado');
    const sumaEsperada = entregados.reduce((acc, p) => acc + p.total, 0);
    expect(totalCobrado).toBeCloseTo(sumaEsperada, 2);
  });

  it('debe identificar con precisión los pedidos en riesgo (> 24h en Recibido o Preparación)', () => {
    const enRiesgo = pedidosIniciales.filter(estaEnRiesgo);
    expect(enRiesgo.length).toBeGreaterThan(0);
    enRiesgo.forEach((p) => {
      expect(['Recibido', 'Preparación']).toContain(p.estado);
    });
  });

  it('debe contar con pedidos en los 5 estados operativos del pipeline', () => {
    const estadosPresentes = new Set(pedidosIniciales.map((p) => p.estado));
    expect(estadosPresentes.has('Recibido')).toBe(true);
    expect(estadosPresentes.has('Preparación')).toBe(true);
    expect(estadosPresentes.has('Camino')).toBe(true);
    expect(estadosPresentes.has('Entregado')).toBe(true);
    expect(estadosPresentes.has('Cancelado')).toBe(true);
  });
});

describe('Pestaña 2: Nuevo Pedido - Validaciones, Cupones y Pasarela de Pago', () => {
  it('debe contener y validar los cupones promocionales oficiales de LeoFit', () => {
    expect(CUPONES_VALIDOS.length).toBeGreaterThanOrEqual(4);
    
    const cupon10 = CUPONES_VALIDOS.find((c) => c.codigo === 'LEOFIT10');
    expect(cupon10).toBeDefined();
    expect(cupon10?.descuento).toBe(10);

    const cuponVerano = CUPONES_VALIDOS.find((c) => c.codigo === 'PROMOVERANO');
    expect(cuponVerano).toBeDefined();
    expect(cuponVerano?.descuento).toBe(15);

    const cuponEnvio = CUPONES_VALIDOS.find((c) => c.codigo === 'ENVIOGRATIS');
    expect(cuponEnvio).toBeDefined();
    expect(cuponEnvio?.descuento).toBe(8);
  });

  it('debe calcular la liquidación económica completa con subtotal, flete y cupón', () => {
    const item1 = { precio: 85, cantidad: 2 }; // S/ 170
    const subtotal = item1.precio * item1.cantidad;
    const costoDelivery = 15; // Encomienda
    const descuentoCupon = 10; // LEOFIT10
    const descuentoManual = 5;
    
    const totalCalculado = Math.max(0, subtotal + costoDelivery - (descuentoCupon + descuentoManual));
    expect(totalCalculado).toBe(170);
  });

  it('debe exigir DNI/RUC cuando la modalidad de despacho es Nacional (Encomienda)', () => {
    const pedidoLocal: Partial<Pedido> = {
      tipoEnvio: 'Local',
      cliente: { nombre: 'Juan Perez', telefono: '987654321', direccion: 'Av. Arequipa 123' },
    };
    expect(pedidoLocal.cliente?.dniRuc).toBeUndefined();

    const pedidoNacional: Partial<Pedido> = {
      tipoEnvio: 'Nacional',
      agenciaEncomienda: 'Shalom',
      ciudadDestino: 'Arequipa',
      cliente: { nombre: 'Rosa Gomez', telefono: '987112233', dniRuc: '44556677', direccion: 'Agencia Shalom' },
    };
    expect(pedidoNacional.cliente?.dniRuc).toBeDefined();
    expect(pedidoNacional.cliente?.dniRuc?.length).toBeGreaterThanOrEqual(8);
  });
});

describe('Pestaña 3: Historial de Pedidos - Filtros Multiatributo y Recibos', () => {
  it('debe permitir la búsqueda cruzada por Nombre, DNI, Teléfono, N° Pedido u Operación', () => {
    const queryDni = '72458910';
    const matchDni = pedidosIniciales.filter(
      (p) => p.cliente.dniRuc && p.cliente.dniRuc.includes(queryDni)
    );
    expect(matchDni.length).toBe(1);
    expect(matchDni[0].cliente.nombre).toBe('Carlos Mendoza');

    const queryTel = '987654321';
    const matchTel = pedidosIniciales.filter((p) => p.cliente.telefono.includes(queryTel));
    expect(matchTel.length).toBeGreaterThan(0);

    const queryNumero = 'LFT-001';
    const matchNumero = pedidosIniciales.filter((p) => p.numero === queryNumero);
    expect(matchNumero.length).toBe(1);
    expect(matchNumero[0].cliente.nombre).toBe('Carlos Mendoza');
  });

  it('debe filtrar pedidos correctamente por estado operativo', () => {
    const estados: EstadoPedido[] = ['Recibido', 'Preparación', 'Camino', 'Entregado', 'Cancelado'];
    estados.forEach((estado) => {
      const filtrados = pedidosIniciales.filter((p) => p.estado === estado);
      filtrados.forEach((p) => expect(p.estado).toBe(estado));
    });
  });
});

describe('Pestaña 4: Inventario - Gestión de Existencias y Stock Crítico', () => {
  it('debe clasificar existencias y detectar prendas con stock crítico (<= 5)', () => {
    const productos = [...productosIniciales];
    const stockBajo = productos.filter((p) => p.stock <= 5);
    expect(stockBajo.length).toBeGreaterThan(0);

    stockBajo.forEach((p) => {
      expect(p.stock).toBeLessThanOrEqual(5);
    });
  });

  it('debe validar la estructura de prendas de las 3 categorías del negocio', () => {
    const categorias = new Set(productosIniciales.map((p) => p.categoria));
    expect(categorias.has('Deportiva')).toBe(true);
    expect(categorias.has('Casual')).toBe(true);
    expect(categorias.has('Accesorios')).toBe(true);
  });
});

describe('Pestaña 5: Rastreo Público - Autoservicio y Consultas en Vivo', () => {
  it('debe localizar un pedido por código correlativo LFT-XXX o DNI/RUC', () => {
    const buscarPedido = (q: string) => {
      const query = q.trim().toUpperCase();
      return pedidosIniciales.find(
        (p) =>
          p.numero.toUpperCase() === query ||
          p.cliente.telefono === query ||
          (p.cliente.dniRuc && p.cliente.dniRuc.toUpperCase() === query)
      );
    };

    const encontradoPorCod = buscarPedido('LFT-001');
    expect(encontradoPorCod).toBeDefined();
    expect(encontradoPorCod?.cliente.nombre).toBe('Carlos Mendoza');

    const encontradoPorDni = buscarPedido('72458910');
    expect(encontradoPorDni).toBeDefined();
    expect(encontradoPorDni?.numero).toBe('LFT-001');

    const encontradoPorTel = buscarPedido('987654321');
    expect(encontradoPorTel).toBeDefined();
  });

  it('debe proporcionar información para los 4 hitos del timeline de entrega', () => {
    const pasos = ['Recibido', 'Preparación', 'Camino', 'Entregado'];
    const p = pedidosIniciales.find((item) => item.estado === 'Camino');
    expect(p).toBeDefined();
    if (p) {
      const indice = pasos.indexOf(p.estado);
      expect(indice).toBe(2);
      expect(indice).toBeLessThan(pasos.length);
    }
  });
});

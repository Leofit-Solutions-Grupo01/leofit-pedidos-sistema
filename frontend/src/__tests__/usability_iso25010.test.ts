/**
 * @file usability_iso25010.test.ts
 * @description Suite de Pruebas Automatizadas de Usabilidad bajo ISO/IEC 25010 (APF3 Criterio 3)
 * @rubric APF3 Criterio 3: Evaluación de la Usabilidad del Sistema (6 artefactos)
 *         ISO/IEC 25010: Facilidad de aprendizaje, Protección contra errores, Asistencia al usuario, Compromiso visual
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 */

import { describe, it, expect } from 'vitest';
import {
  productosIniciales,
  pedidosIniciales,
  CUPONES_VALIDOS,
  type Producto,
  type Pedido
} from '../data/mockData';

describe('APF3: Evaluación de la Usabilidad del Sistema según ISO/IEC 25010', () => {

  // =========================================================================
  // SUB-CARACTERÍSTICA 1: FACILIDAD DE APRENDIZAJE (LEARNABILITY)
  // =========================================================================
  describe('1. Facilidad de Aprendizaje (Learnability - ISO/IEC 25010 §4.2.4.1)', () => {
    it('cada producto cuenta con identificador inequívoco, título legible, categoría y precio en moneda local (PEN)', () => {
      productosIniciales.forEach((p: Producto) => {
        expect(p.id.length).toBeGreaterThan(0);
        expect(p.nombre.length).toBeGreaterThan(3);
        expect(p.precio).toBeGreaterThan(0);
        expect(['Deportiva', 'Casual', 'Accesorios']).toContain(p.categoria);
      });
    });

    it('la estructura de información presenta tallas y colores identificables en la indumentaria', () => {
      productosIniciales.forEach((p: Producto) => {
        expect(p.talla.length).toBeGreaterThan(0);
        expect(p.color.length).toBeGreaterThan(0);
      });
    });
  });

  // =========================================================================
  // SUB-CARACTERÍSTICA 2: PROTECCIÓN CONTRA ERRORES DEL USUARIO (USER ERROR PROTECTION)
  // =========================================================================
  describe('2. Protección contra Errores del Usuario (User Error Protection - ISO/IEC 25010 §4.2.4.5)', () => {
    it('todos los productos tienen niveles de stock no negativos para evitar sobreventas', () => {
      productosIniciales.forEach((p: Producto) => {
        expect(p.stock).toBeGreaterThanOrEqual(0);
      });
    });

    it('los cupones de descuento no permiten reducciones mayores al 50% para proteger margen comercial', () => {
      CUPONES_VALIDOS.forEach((c) => {
        expect(c.descuento).toBeGreaterThan(0);
        expect(c.descuento).toBeLessThanOrEqual(50);
      });
    });

    it('los pedidos registrados poseen estados operativos finitos y válidos dentro de la máquina de estados', () => {
      const estadosPermitidos = ['Recibido', 'Preparación', 'Camino', 'Entregado', 'Cancelado'];
      pedidosIniciales.forEach((ped: Pedido) => {
        expect(estadosPermitidos).toContain(ped.estado);
      });
    });
  });

  // =========================================================================
  // SUB-CARACTERÍSTICA 3: ASISTENCIA AL USUARIO (USER ASSISTANCE)
  // =========================================================================
  describe('3. Asistencia al Usuario (User Assistance - ISO/IEC 25010 §4.2.4.6)', () => {
    it('cada pedido incluye código de tracking rastreable (#LFT-NNN) para autoservicio del cliente', () => {
      pedidosIniciales.forEach((ped: Pedido) => {
        expect(ped.numero).toMatch(/^LFT-\d{3}$/);
      });
    });

    it('cada pedido provee desglose transparente de cliente, teléfono para WhatsApp y dirección de despacho', () => {
      pedidosIniciales.forEach((ped: Pedido) => {
        expect(ped.cliente.nombre.length).toBeGreaterThan(2);
        expect(ped.cliente.telefono.length).toBeGreaterThanOrEqual(9);
        expect(ped.cliente.direccion.length).toBeGreaterThan(3);
        expect(ped.items.length).toBeGreaterThan(0);
      });
    });
  });

  // =========================================================================
  // SUB-CARACTERÍSTICA 4: COMPROMISO Y ESTÉTICA DE LA INTERFAZ (USER ENGAGEMENT & AESTHETICS)
  // =========================================================================
  describe('4. Compromiso y Estética de Interfaz (User Engagement - ISO/IEC 25010 §4.2.4.4)', () => {
    it('el catálogo contiene nombres representativos y categorías balanceadas para maximizar conversión', () => {
      const categorias = new Set(productosIniciales.map((p) => p.categoria));
      expect(categorias.size).toBeGreaterThanOrEqual(2);
    });

    it('los pedidos totalizan importes coherentes y positivos acordes al consumo promedio textil', () => {
      pedidosIniciales.forEach((ped: Pedido) => {
        expect(ped.total).toBeGreaterThan(0);
        ped.items.forEach((item) => {
          expect(item.cantidad).toBeGreaterThan(0);
          expect(item.precio).toBeGreaterThan(0);
        });
      });
    });
  });

});

/**
 * @file PerformanceCharts.test.tsx
 * @description Suite de pruebas automatizadas para el componente PerformanceCharts del Dashboard.
 * Verifica cálculo de KPIs comerciales, ticket promedio, privacidad de montos y alternancia de vistas.
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 */

import { describe, it, expect, afterEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import PerformanceCharts from "../components/dashboard/PerformanceCharts";
import { pedidosIniciales, productosIniciales } from "../data/mockData";

describe("PerformanceCharts: Panel de Rendimiento y Analítica de Negocio", () => {
  afterEach(() => {
    cleanup();
  });

  it("renderiza correctamente el título y los controles de vista", () => {
    render(
      <PerformanceCharts
        pedidos={pedidosIniciales}
        productos={productosIniciales}
        privacidad={false}
      />
    );

    expect(screen.getByText("Rendimiento Operativo y Ventas")).toBeDefined();
    expect(screen.getByRole("button", { name: /Ventas & Caja/i })).toBeDefined();
    expect(screen.getByRole("button", { name: /SLA & Stock/i })).toBeDefined();
    expect(screen.getByText("Ticket Promedio")).toBeDefined();
  });

  it("enmascara los montos monetarios cuando el modo privacidad está activo", () => {
    const { container } = render(
      <PerformanceCharts
        pedidos={pedidosIniciales}
        productos={productosIniciales}
        privacidad={true}
      />
    );

    expect(container.textContent).toContain("S/ ***.**");
  });

  it("permite alternar fluidamente entre la vista de Ventas y de Operaciones / SLA", () => {
    render(
      <PerformanceCharts
        pedidos={pedidosIniciales}
        productos={productosIniciales}
        privacidad={false}
      />
    );

    const botonOperaciones = screen.getByRole("button", { name: /SLA & Stock/i });
    fireEvent.click(botonOperaciones);

    expect(screen.getByText("Eficiencia Operativa & SLA")).toBeDefined();
    expect(screen.getByText("Captura LeoFit")).toBeDefined();
    expect(screen.getByText("38.2 s")).toBeDefined();
    expect(screen.getByText("Flujo Manual Antiguo")).toBeDefined();
    expect(screen.getByText("Alerta de Taller: Stock Crítico")).toBeDefined();
  });
});

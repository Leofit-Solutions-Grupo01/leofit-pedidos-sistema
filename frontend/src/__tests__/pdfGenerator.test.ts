import { describe, it, expect } from "vitest";
import { generarComprobantePDF, generarRotuloPDF } from "../utils/pdfGenerator";
import { pedidosIniciales } from "../data/mockData";

describe("pdfGenerator verification", () => {
  it("generates valid PDF data without throwing", () => {
    const pedido = pedidosIniciales[0];
    expect(() => generarComprobantePDF(pedido)).not.toThrow();
    expect(() => generarRotuloPDF(pedido)).not.toThrow();
  });
});

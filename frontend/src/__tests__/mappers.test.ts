import { describe, it, expect } from 'vitest';
import { toCreateOrderDTO } from '../services/mappers';
import { Pedido } from '../data/mockData';

describe('mappers: toCreateOrderDTO', () => {
  const basePedido: Pedido = {
    id: "o999",
    numero: "LFT-999",
    canal: "WhatsApp",
    cliente: { nombre: "Test", telefono: "987654321", direccion: "Calle 1" },
    tipoEnvio: "Local",
    ciudadDestino: "Lima Capital",
    items: [{ productoId: "p1", nombre: "Camiseta", cantidad: 1, precio: 50 }],
    total: 50,
    costoDelivery: 5,
    descuento: 0,
    metodoPago: "Yape",
    estado: "Recibido",
    fecha: "2026-10-08"
  };

  it('T1: Debe mapear correctamente un envío Local con método Yape', () => {
    const dto = toCreateOrderDTO(basePedido);
    expect(dto.shippingType).toBe('LIMA');
    expect(dto.paymentMethod).toBe('YAPE');
    expect(dto.items[0].variantId).toBe(1);
    expect(dto.clientData.fullName).toBe("Test");
  });

  it('T2: Debe mapear un envío Nacional con Contra Entrega', () => {
    const nacional: Pedido = {
      ...basePedido,
      tipoEnvio: "Nacional",
      ciudadDestino: "Arequipa",
      agenciaEncomienda: "Shalom",
      metodoPago: "Contra Entrega",
      cliente: { ...basePedido.cliente, dniRuc: "12345678" }
    };
    const dto = toCreateOrderDTO(nacional);
    expect(dto.shippingType).toBe('PROVINCIA');
    expect(dto.destinationCity).toBe('Arequipa');
    expect(dto.shippingAgency).toBe('Shalom');
    expect(dto.paymentMethod).toBe('CONTRAENTREGA');
  });

  it('T3: Debe agrupar Transferencia BCP y BBVA hacia TRANSFERENCIA', () => {
    const dtoBCP = toCreateOrderDTO({ ...basePedido, metodoPago: "Transferencia BCP" });
    expect(dtoBCP.paymentMethod).toBe('TRANSFERENCIA');
    
    const dtoBBVA = toCreateOrderDTO({ ...basePedido, metodoPago: "Transferencia BBVA" });
    expect(dtoBBVA.paymentMethod).toBe('TRANSFERENCIA');
  });

  it('T4: Fail-Fast - Debe arrojar error si cliente.telefono está vacío', () => {
    const sinTel = { ...basePedido, cliente: { ...basePedido.cliente, telefono: " " } };
    expect(() => toCreateOrderDTO(sinTel)).toThrowError();
  });

  it('T5: Fail-Fast - Debe arrojar error si es Nacional y falta cliente.dniRuc', () => {
    const sinDni = { ...basePedido, tipoEnvio: "Nacional", cliente: { ...basePedido.cliente, dniRuc: "" } };
    expect(() => toCreateOrderDTO(sinDni as any)).toThrowError();
  });

  it('T6: Fail-Fast - Debe arrojar error si es Nacional y falta ciudadDestino', () => {
    const sinCiudad = { ...basePedido, tipoEnvio: "Nacional", ciudadDestino: "  " };
    expect(() => toCreateOrderDTO(sinCiudad as any)).toThrowError();
  });

  it('T7: Fail-Fast - Debe arrojar error si un item tiene productoId no parseable', () => {
    const malo1 = { ...basePedido, items: [{ ...basePedido.items[0], productoId: "abc" }] };
    expect(() => toCreateOrderDTO(malo1)).toThrowError('variantId inválido: abc');

    const malo2 = { ...basePedido, items: [{ ...basePedido.items[0], productoId: "" }] };
    expect(() => toCreateOrderDTO(malo2)).toThrowError('variantId inválido: ');
  });
});

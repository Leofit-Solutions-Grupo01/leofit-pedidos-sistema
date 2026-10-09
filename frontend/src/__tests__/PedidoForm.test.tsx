/**
 * @vitest-environment jsdom
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import React from 'react';
import PedidoForm from '../pages/PedidoForm';

const mockCrearPedido = vi.fn();
const mockNavegarA = vi.fn();

vi.mock('../context/AppContext', () => ({
  useApp: () => ({
    crearPedido: mockCrearPedido,
    navegarA: mockNavegarA,
    pedidos: [],
    productos: [
      { id: '1', nombre: 'Producto 1', precio: 100, stock: 10, categoria: 'cat', imageUrl: '' }
    ]
  })
}));

describe('PedidoForm: submit', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('T4: PedidoForm deshabilita submit y muestra spinner mientras enviando', async () => {
    let resolveCrear: any;
    mockCrearPedido.mockImplementation(() => new Promise(resolve => {
      resolveCrear = resolve;
    }));

    render(<PedidoForm />);

    // Llenar campos requeridos
    fireEvent.change(screen.getByPlaceholderText(/Juan Carlos Pérez/i), { target: { value: 'Juan' } });
    fireEvent.change(screen.getByPlaceholderText(/987654321/i), { target: { value: '1234567' } });
    fireEvent.change(screen.getByPlaceholderText(/Av. Las Flores 456/i), { target: { value: 'Calle 123' } });
    
    // Seleccionar producto
    const selectProducto = screen.getByRole('combobox');
    fireEvent.change(selectProducto, { target: { value: '1' } });
    fireEvent.click(screen.getByText('Agregar'));

    // Submit
    const btnSubmit = screen.getByRole('button', { name: /confirmar/i });
    fireEvent.click(btnSubmit);

    // Debe deshabilitarse y mostrar texto alternativo (ej. Enviando...)
    expect((btnSubmit as HTMLButtonElement).disabled).toBe(true);
    expect(screen.getByText(/enviando/i)).toBeTruthy();

    // Resolve
    resolveCrear({ 
      ok: true, 
      pedido: { 
        numero: 'LFT-001', 
        cliente: { nombre: 'Juan', telefono: '123' }, 
        total: 10 
      } 
    });

    await waitFor(() => {
      expect(screen.getByText(/¡Pedido Registrado con Éxito!/i)).toBeTruthy();
    });
  });

  it('T6: PedidoForm no muestra Tarjeta/Link en métodos de pago', () => {
    render(<PedidoForm />);
    
    // El texto "Tarjeta / Link" o "Tarjeta/Link" no debería estar en el documento
    const tarjeta = screen.queryByText(/Tarjeta \/ Link/i) || screen.queryByText(/Tarjeta\/Link/i);
    expect(tarjeta).toBeNull();
  });
});

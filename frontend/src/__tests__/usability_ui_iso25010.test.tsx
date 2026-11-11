/**
 * @vitest-environment jsdom
 * @file usability_ui_iso25010.test.tsx
 * @description Pruebas automatizadas de USABILIDAD sobre la interfaz renderizada (APF3 - Artefacto 3).
 *              Herramientas: Vitest + React Testing Library (interacción) + axe-core (accesibilidad WCAG).
 *              Subatributos ISO/IEC 25010: Learnability, User Error Protection,
 *              User Assistance y User Engagement.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react';
import axe from 'axe-core';
import React from 'react';
import Login from '../pages/Login';
import PedidoForm from '../pages/PedidoForm';

const mockIniciarSesion = vi.fn();
const mockCrearPedido = vi.fn();

vi.mock('../context/AppContext', () => ({
  useApp: () => ({
    iniciarSesion: mockIniciarSesion,
    crearPedido: mockCrearPedido,
    navegarA: vi.fn(),
    pedidos: [],
    productos: [
      { id: '1', nombre: 'Polo Deportivo', precio: 100, stock: 10, categoria: 'Deportiva', imageUrl: '' },
    ],
  }),
}));

async function violacionesAxe(container: HTMLElement) {
  // color-contrast no es calculable en jsdom (sin motor de layout): se audita con Lighthouse en la nube.
  const r = await axe.run(container, {
    rules: { 'color-contrast': { enabled: false } },
    runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] },
  });
  return r.violations.map((v) => `${v.id}: ${v.help} -> ${v.nodes.map((n) => n.html.slice(0, 110)).join(' | ')}`);
}

beforeEach(() => vi.clearAllMocks());
afterEach(() => cleanup());

describe('ISO/IEC 25010 - Usabilidad (UI real)', () => {
  describe('1. Facilidad de aprendizaje (Learnability)', () => {
    it('UL-01 Login expone campos con etiqueta asociada y una acción primaria clara', () => {
      render(<Login />);
      expect(screen.getByLabelText(/^correo|^email/i)).toBeTruthy();
      expect(screen.getByLabelText(/^contraseña$/i)).toBeTruthy();
      expect(screen.getByRole('button', { name: /ingresar al sistema/i })).toBeTruthy();
    });

    it('UL-02 Login ofrece acceso rápido por rol que precarga credenciales demo', () => {
      render(<Login />);
      fireEvent.click(screen.getByTitle(/administrador/i));
      expect((screen.getByLabelText(/^correo|^email/i) as HTMLInputElement).value).toBe('admin@leofit.pe');
    });

    it('UL-03 PedidoForm guía el llenado con placeholders de ejemplo', () => {
      render(<PedidoForm />);
      expect(screen.getByPlaceholderText(/Juan Carlos Pérez/i)).toBeTruthy();
      expect(screen.getByPlaceholderText(/987654321/i)).toBeTruthy();
      expect(screen.getByPlaceholderText(/Av. Las Flores 456/i)).toBeTruthy();
    });
  });

  describe('2. Protección contra errores del usuario (User Error Protection)', () => {
    it('UE-01 Login bloquea el envío con campos vacíos (campos requeridos) y no llama al servicio', () => {
      render(<Login />);
      const email = screen.getByLabelText(/^correo|^email/i) as HTMLInputElement;
      const pass = screen.getByLabelText(/^contraseña$/i) as HTMLInputElement;
      expect(email.required).toBe(true);
      expect(pass.required).toBe(true);
      fireEvent.click(screen.getByRole('button', { name: /ingresar al sistema/i }));
      expect(email.validity.valid).toBe(false);
      expect(mockIniciarSesion).not.toHaveBeenCalled();
    });

    it('UE-02 Login permite ocultar/mostrar la contraseña para evitar errores de tipeo', () => {
      render(<Login />);
      const input = screen.getByLabelText(/^contraseña$/i) as HTMLInputElement;
      expect(input.type).toBe('password');
      fireEvent.click(screen.getByRole('button', { name: /mostrar contraseña/i }));
      expect(input.type).toBe('text');
    });

    it('UE-03 PedidoForm no registra un pedido sin datos obligatorios', () => {
      render(<PedidoForm />);
      fireEvent.click(screen.getByRole('button', { name: /confirmar/i }));
      expect(mockCrearPedido).not.toHaveBeenCalled();
    });
  });

  describe('3. Asistencia al usuario (User Assistance)', () => {
    it('UA-01 Login informa con un mensaje claro cuando las credenciales son incorrectas', async () => {
      mockIniciarSesion.mockResolvedValue(false);
      render(<Login />);
      fireEvent.change(screen.getByLabelText(/^correo|^email/i), { target: { value: 'x@y.pe' } });
      fireEvent.change(screen.getByLabelText(/^contraseña$/i), { target: { value: 'mala' } });
      fireEvent.click(screen.getByRole('button', { name: /ingresar al sistema/i }));
      await waitFor(() => expect(screen.getByText(/credenciales incorrectas/i)).toBeTruthy(), { timeout: 3000 });
    });

    it('UA-02 PedidoForm muestra banner de error cuando el servicio falla', async () => {
      mockCrearPedido.mockResolvedValueOnce({ ok: false, error: 'Error de red', code: 'NETWORK_ERROR' });
      render(<PedidoForm />);
      fireEvent.change(screen.getByPlaceholderText(/Juan Carlos Pérez/i), { target: { value: 'Juan' } });
      fireEvent.change(screen.getByPlaceholderText(/987654321/i), { target: { value: '987654321' } });
      fireEvent.change(screen.getByPlaceholderText(/Av. Las Flores 456/i), { target: { value: 'Calle 123' } });
      fireEvent.change(screen.getByRole('combobox'), { target: { value: '1' } });
      fireEvent.click(screen.getByText('Agregar'));
      fireEvent.click(screen.getByRole('button', { name: /confirmar/i }));
      await waitFor(() => expect(screen.getByText(/error de red/i)).toBeTruthy());
    });
  });

  describe('4. Compromiso del usuario (User Engagement) y retroalimentación', () => {
    it('UG-01 Login muestra estado de carga y bloquea doble envío', async () => {
      mockIniciarSesion.mockImplementation(() => new Promise(() => {}));
      render(<Login />);
      fireEvent.change(screen.getByLabelText(/^correo|^email/i), { target: { value: 'a@b.pe' } });
      fireEvent.change(screen.getByLabelText(/^contraseña$/i), { target: { value: 'password' } });
      const btn = screen.getByRole('button', { name: /ingresar al sistema/i }) as HTMLButtonElement;
      fireEvent.click(btn);
      expect(btn.disabled).toBe(true);
      expect(screen.getByText(/verificando/i)).toBeTruthy();
    });
  });

  describe('5. Accesibilidad automatizada (axe-core, WCAG 2.1 A/AA)', () => {
    it('UX-01 Login sin violaciones WCAG', async () => {
      const { container } = render(<Login />);
      expect(await violacionesAxe(container)).toEqual([]);
    });

    it('UX-02 PedidoForm sin violaciones WCAG', async () => {
      const { container } = render(<PedidoForm />);
      expect(await violacionesAxe(container)).toEqual([]);
    });
  });
});

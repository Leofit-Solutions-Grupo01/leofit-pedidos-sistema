/**
 * @vitest-environment jsdom
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, cleanup } from '@testing-library/react';
import { AppProvider, useApp } from '../context/AppContext';
import { apiFetch } from '../services/api';
import React from 'react';

vi.mock('../services/api', () => ({
  apiFetch: vi.fn(),
}));

const TestComponent = () => {
  const { productos, cargandoProductos, errorProductos } = useApp() as any;
  return (
    <div>
      <span data-testid="cargando">{cargandoProductos ? 'true' : 'false'}</span>
      <span data-testid="error">{errorProductos || 'none'}</span>
      <span data-testid="productos-count">{productos.length}</span>
    </div>
  );
};

describe('AppContext: fetch productos', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
    vi.stubEnv('VITE_USE_MOCK_ORDERS', 'false');
  });

  afterEach(() => {
    vi.unstubAllEnvs();
    cleanup();
  });

  it('T1: Carga productos desde API si no hay cache', async () => {
    vi.mocked(apiFetch).mockResolvedValueOnce([{ id: 'prod1' }, { id: 'prod2' }]);
    
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId('cargando').textContent).toBe('false');
    });

    expect(apiFetch).toHaveBeenCalledWith('/api/products');
    expect(screen.getByTestId('productos-count').textContent).toBe('2');
  });

  it('T2: Usa cache si existe y es fresca (<5 min)', async () => {
    const freshCache = {
      timestamp: Date.now() - 60000, // 1 min ago
      data: [{ id: 'cache1' }]
    };
    sessionStorage.setItem('leofit_products_cache', JSON.stringify(freshCache));

    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId('cargando').textContent).toBe('false');
    });

    expect(apiFetch).not.toHaveBeenCalled();
    expect(screen.getByTestId('productos-count').textContent).toBe('1');
  });

  it('T3: Refetch si cache es vieja (>5 min)', async () => {
    const oldCache = {
      timestamp: Date.now() - (6 * 60 * 1000), // 6 mins ago
      data: [{ id: 'cache1' }]
    };
    sessionStorage.setItem('leofit_products_cache', JSON.stringify(oldCache));
    vi.mocked(apiFetch).mockResolvedValueOnce([{ id: 'new1' }, { id: 'new2' }]);

    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId('cargando').textContent).toBe('false');
    });

    expect(apiFetch).toHaveBeenCalledWith('/api/products');
    expect(screen.getByTestId('productos-count').textContent).toBe('2');
  });

  it('T4: Si API falla -> errorProductos seteado, productos vacio, no crashea', async () => {
    vi.mocked(apiFetch).mockRejectedValueOnce(new Error('API caída'));

    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId('cargando').textContent).toBe('false');
    });

    expect(screen.getByTestId('error').textContent).toBe('API caída');
    expect(screen.getByTestId('productos-count').textContent).toBe('0'); // It should be empty, not the mocks
  });

  it('T5: Si VITE_USE_MOCK_ORDERS=true -> usa mocks, no llama API', async () => {
    vi.stubEnv('VITE_USE_MOCK_ORDERS', 'true');

    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId('cargando').textContent).toBe('false');
    });

    expect(apiFetch).not.toHaveBeenCalled();
    expect(screen.getByTestId('productos-count').textContent).toBe('5');
  });

  it('T6: Si la cache está corrupta, hace refetch', async () => {
    sessionStorage.setItem('leofit_products_cache', 'not-valid-json');
    vi.mocked(apiFetch).mockResolvedValueOnce([{ id: 'new1' }]);
    
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId('cargando').textContent).toBe('false');
    });

    expect(apiFetch).toHaveBeenCalledWith('/api/products');
    expect(screen.getByTestId('productos-count').textContent).toBe('1');
  });

  it('T7: No hace setState si el componente se desmontó durante el fetch', async () => {
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    let resolveApi: (val: any) => void = () => {};
    vi.mocked(apiFetch).mockImplementationOnce(() => new Promise((resolve) => {
      resolveApi = resolve;
    }));

    const { unmount } = render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    unmount();
    
    // Resolvemos el API después del unmount
    resolveApi([{ id: 'prod1' }]);
    
    // Esperamos un tick
    await new Promise(r => setTimeout(r, 50));
    
    expect(errorSpy).not.toHaveBeenCalled();
    errorSpy.mockRestore();
  });
});

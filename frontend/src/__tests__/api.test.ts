import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiFetch, ApiError } from '../services/api';

const globalFetch = vi.fn();
global.fetch = globalFetch as any;

describe('apiFetch', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
    vi.stubEnv('VITE_API_URL', 'http://localhost:3000');
  });

  it('T1: Añade Authorization si hay token en sessionStorage', async () => {
    sessionStorage.setItem('leofit_session', 'test-token');
    globalFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, data: { ok: true } })
    });

    await apiFetch('/test');
    expect(globalFetch).toHaveBeenCalledWith(
      expect.stringContaining('/test'),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: 'Bearer test-token'
        })
      })
    );
  });

  it('T2: No añade Authorization si no hay token', async () => {
    globalFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, data: { ok: true } })
    });

    await apiFetch('/test');
    // El header puede no existir, o existir pero sin Authorization
    const callArgs = globalFetch.mock.calls[0];
    const options = callArgs[1] || {};
    const headers = options.headers || {};
    expect(headers).not.toHaveProperty('Authorization');
  });

  it('T3: 401 llama cerrarSesionFn y arroja ApiError UNAUTHORIZED', async () => {
    globalFetch.mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ success: false, error: { code: 'UNAUTHORIZED', message: 'Token expiro' } })
    });

    const cerrarFn = vi.fn();
    try {
      await apiFetch('/test', {}, cerrarFn);
      expect.fail('Should have thrown');
    } catch (e) {
      expect(e).toBeInstanceOf(ApiError);
      expect((e as ApiError).code).toBe('UNAUTHORIZED');
    }
    expect(cerrarFn).toHaveBeenCalled();
  });

  it('T4: Envelope con success: false arroja ApiError con el código devuelto', async () => {
    globalFetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => ({ success: false, error: { code: 'VALIDATION_ERROR', message: 'Datos invalidos' } })
    });

    try {
      await apiFetch('/test');
      expect.fail('Should have thrown');
    } catch (e) {
      expect(e).toBeInstanceOf(ApiError);
      expect((e as ApiError).code).toBe('VALIDATION_ERROR');
      expect((e as ApiError).message).toBe('Datos invalidos');
    }
  });

  it('T5: Envelope success: true devuelve data directamente', async () => {
    globalFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, data: { id: 1, name: 'Pedro' } })
    });

    const result = await apiFetch<{ id: number; name: string }>('/test');
    expect(result).toEqual({ id: 1, name: 'Pedro' });
  });

  it('T6: Lanza error si VITE_API_URL no está definido', async () => {
    vi.stubEnv('VITE_API_URL', '');
    try {
      await apiFetch('/test');
      expect.fail('Should have thrown');
    } catch (e: any) {
      expect(e).toBeInstanceOf(Error);
      expect(e.message).toBe('VITE_API_URL no está definido');
    }
  });
});

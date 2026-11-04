import { triggerSessionExpired, validateAndDecodeJwt } from './authGuard';

export class ApiError extends Error {
  constructor(public code: string, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export function getApiBaseUrl(): string {
  const envApiUrl = import.meta.env.VITE_API_URL;
  const baseUrl = envApiUrl !== undefined
    ? envApiUrl
    : (typeof window !== 'undefined' && window.location.hostname === 'localhost'
        ? 'http://localhost:4000'
        : 'https://leofit-backend-api.onrender.com');

  if (!baseUrl) {
    throw new Error('VITE_API_URL no está definido');
  }

  return baseUrl.replace(/\/+$/, '');
}

let inMemoryAccessToken: string | null = null;
let refreshPromise: Promise<boolean> | null = null;
const authListeners = new Set<(evt: 'logout' | 'refreshed') => void>();

export function setAccessToken(token: string | null): void {
  inMemoryAccessToken = token;
  if (typeof sessionStorage !== 'undefined') {
    if (token) {
      sessionStorage.setItem('leofit_session', token);
    } else {
      sessionStorage.removeItem('leofit_session');
    }
  }
}

export function getAccessToken(): string | null {
  if (inMemoryAccessToken) return inMemoryAccessToken;
  if (typeof sessionStorage !== 'undefined') {
    return sessionStorage.getItem('leofit_session');
  }
  return null;
}

export function onAuthEvent(fn: (evt: 'logout' | 'refreshed') => void): () => void {
  authListeners.add(fn);
  return () => {
    authListeners.delete(fn);
  };
}

function emitAuthEvent(evt: 'logout' | 'refreshed'): void {
  authListeners.forEach((listener) => {
    try {
      listener(evt);
    } catch {
      // Ignorar errores de observadores
    }
  });
}

/**
 * Ejecuta la renovación silenciosa del access token usando la cookie HttpOnly leofit_rt.
 * Implementa Single-Flight para deduplicar peticiones concurrentes a /api/auth/refresh.
 */
export async function doRefresh(): Promise<boolean> {
  if (!refreshPromise) {
    refreshPromise = (async () => {
      try {
        const baseUrl = getApiBaseUrl();
        const res = await fetch(`${baseUrl}/api/auth/refresh`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' }
        });

        if (!res.ok) {
          return false;
        }

        const data = await res.json();
        const newAccessToken = data?.data?.accessToken || data?.data?.token;
        if (newAccessToken) {
          setAccessToken(newAccessToken);
          emitAuthEvent('refreshed');
          return true;
        }
        return false;
      } catch {
        return false;
      } finally {
        refreshPromise = null;
      }
    })();
  }
  return refreshPromise;
}

export async function apiBootstrap(): Promise<boolean> {
  return doRefresh();
}

export async function apiLogout(): Promise<void> {
  try {
    const baseUrl = getApiBaseUrl();
    await fetch(`${baseUrl}/api/auth/logout`, {
      method: 'POST',
      credentials: 'include'
    });
  } catch {
    // Si la red falla, aseguramos la limpieza local
  } finally {
    setAccessToken(null);
    emitAuthEvent('logout');
  }
}

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {},
  cerrarSesionFn?: () => void
): Promise<T> {
  const currentToken = getAccessToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>)
  };

  if (currentToken) {
    const isSynthetic = currentToken.startsWith('token-mock-') || currentToken.startsWith('token-offline-');
    if (!isSynthetic) {
      headers['Authorization'] = `Bearer ${currentToken}`;
    }
  }

  const baseUrl = getApiBaseUrl();
  const url = endpoint.startsWith('http') ? endpoint : `${baseUrl}${endpoint}`;

  const method = (options.method || 'GET').toUpperCase();
  const hasIdempotencyKey = !!(headers['Idempotency-Key'] || headers['idempotency-key'] || headers['X-Idempotency-Key']);
  const isRetryable = method === 'GET' || hasIdempotencyKey;
  const maxRetries = isRetryable ? 2 : 0;

  let res: Response | null = null;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      res = await fetch(url, { ...options, headers, credentials: 'include' });
    } catch (error: any) {
      if (attempt < maxRetries && error.name !== 'AbortError') {
        const delayMs = Math.min(4000, 1000 * Math.pow(2, attempt) + Math.random() * 250);
        await new Promise((resolve) => setTimeout(resolve, delayMs));
        continue;
      }
      throw new ApiError('NETWORK_ERROR', error.message || 'Error de red');
    }

    // Si el servidor está procesando concurrentemente la misma Idempotency-Key (409) o en cold-start (502, 503, 504)
    const isConcurrentIdempotency = (res.status === 409 || res.status === 425) && hasIdempotencyKey;
    const isServerWakingOrDegraded = [502, 503, 504].includes(res.status);

    if (res && (isServerWakingOrDegraded || isConcurrentIdempotency) && attempt < maxRetries) {
      const retryAfter = res.headers ? res.headers.get('Retry-After') : null;
      let delayMs = Math.min(4000, 1000 * Math.pow(2, attempt) + Math.random() * 250);
      if (retryAfter) {
        const seconds = parseInt(retryAfter, 10);
        if (!isNaN(seconds) && seconds > 0) {
          delayMs = Math.min(seconds * 1000, 6000);
        }
      }
      await new Promise((resolve) => setTimeout(resolve, delayMs));
      continue;
    }

    break;
  }

  if (!res) {
    throw new ApiError('NETWORK_ERROR', 'No se pudo obtener respuesta del servidor');
  }

  // 401 Manejo con Refresh Silencioso (siempre que no estemos llamando a los endpoints de auth)
  if (res.status === 401 && !endpoint.includes('/api/auth/')) {
    const refreshed = await doRefresh();
    if (refreshed) {
      const newAuthToken = getAccessToken();
      const retryHeaders = {
        ...headers,
        ...(newAuthToken ? { Authorization: `Bearer ${newAuthToken}` } : {})
      };
      res = await fetch(url, { ...options, headers: retryHeaders, credentials: 'include' });
    }
  }

  if (!res.ok) {
    let errCode = 'UNKNOWN_ERROR';
    let errMessage = `HTTP Error ${res.status}`;
    
    try {
      const errorData = await res.json();
      if (errorData && !errorData.success && errorData.error) {
        errCode = errorData.error.code || errCode;
        errMessage = errorData.error.message || errMessage;
      }
    } catch {
      // Ignore if not json
    }

    const isTokenExpiredOrInvalid =
      res.status === 401 ||
      (res.status === 403 && (
        errCode === 'FORBIDDEN' ||
        errMessage.toLowerCase().includes('token') ||
        errMessage.toLowerCase().includes('expirado') ||
        errMessage.toLowerCase().includes('inválido') ||
        errMessage.toLowerCase().includes('sesión')
      ));

    if (isTokenExpiredOrInvalid) {
      setAccessToken(null);
      emitAuthEvent('logout');
      if (cerrarSesionFn) {
        triggerSessionExpired(errMessage || 'Token de sesión inválido o expirado. Inicie sesión nuevamente.');
        cerrarSesionFn();
      }
      throw new ApiError('UNAUTHORIZED', errMessage);
    }
    
    throw new ApiError(errCode, errMessage);
  }

  if (res.status === 204) {
    return {} as T;
  }

  try {
    const data = await res.json();
    if (data && typeof data === 'object' && 'success' in data) {
      if (!data.success) {
         throw new ApiError(data.error?.code || 'API_ERROR', data.error?.message || 'Error en la respuesta');
      }
      return data.data as T;
    }
    return data as T;
  } catch (e) {
    if (e instanceof ApiError) throw e;
    return {} as T;
  }
}

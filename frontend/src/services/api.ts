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

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {},
  cerrarSesionFn?: () => void
): Promise<T> {
  const token = sessionStorage.getItem("leofit_session");
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>)
  };

  if (token) {
    const isSynthetic = token.startsWith('token-mock-') || token.startsWith('token-offline-');
    if (!isSynthetic) {
      const tokenCheck = validateAndDecodeJwt(token);
      if (tokenCheck.expired && cerrarSesionFn) {
        triggerSessionExpired('Tu sesión ha expirado. Por favor ingresa nuevamente.');
        cerrarSesionFn();
        throw new ApiError('UNAUTHORIZED', 'Tu sesión ha expirado');
      }
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  const baseUrl = getApiBaseUrl();
  const url = endpoint.startsWith('http') ? endpoint : `${baseUrl}${endpoint}`;

  let res: Response;
  try {
    res = await fetch(url, { ...options, headers });
  } catch (error: any) {
    throw new ApiError('NETWORK_ERROR', error.message || 'Error de red');
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

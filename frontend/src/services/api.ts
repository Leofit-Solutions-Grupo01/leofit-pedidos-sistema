export class ApiError extends Error {
  constructor(public code: string, message: string) {
    super(message);
    this.name = 'ApiError';
  }
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
    headers['Authorization'] = `Bearer ${token}`;
  }

  const baseUrl = import.meta.env?.VITE_API_URL || '';
  const url = endpoint.startsWith('http') ? endpoint : `${baseUrl}${endpoint}`;

  const res = await fetch(url, { ...options, headers });

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

    if (res.status === 401) {
      if (cerrarSesionFn) cerrarSesionFn();
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

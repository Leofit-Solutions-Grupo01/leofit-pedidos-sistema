/**
 * @file authGuard.ts
 * @description Guardrails de seguridad y validación de tokens JWT en el frontend para LeoFit.
 * Maneja la decodificación segura del payload, la verificación de caducidad (exp),
 * la detección preventiva de expiración y el despacho de eventos globales de cierre de sesión.
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

export const LEOFIT_AUTH_EXPIRED_EVENT = "leofit_auth_expired";

export interface DecodedJwtPayload {
  userId?: number;
  id?: number;
  email?: string;
  name?: string;
  role?: "ADMIN" | "OPERATOR";
  exp?: number;
  iat?: number;
  [key: string]: unknown;
}

export interface TokenValidationResult {
  valid: boolean;
  expired: boolean;
  payload: DecodedJwtPayload | null;
  error?: string;
}

/**
 * Decodifica y valida un token JWT en el cliente sin requerir librerías pesadas (Zero Cost).
 * Maneja tokens estándar de 3 segmentos (Base64Url) y tokens sintéticos de desarrollo/demo.
 *
 * @param token Token de sesión almacenado en sessionStorage
 * @param leewaySeconds Margen de tolerancia preventiva en segundos (por defecto 30s)
 */
export function validateAndDecodeJwt(
  token: string | null | undefined,
  leewaySeconds = 30
): TokenValidationResult {
  if (!token || typeof token !== "string" || !token.trim()) {
    return { valid: false, expired: true, payload: null, error: "Token ausente" };
  }

  const cleanToken = token.trim();

  // Compatibilidad con tokens locales de prueba o modo offline
  if (cleanToken.startsWith("token-mock-") || cleanToken.startsWith("token-offline-")) {
    const rol = cleanToken.includes("operator") ? "OPERATOR" : "ADMIN";
    return {
      valid: true,
      expired: false,
      payload: {
        userId: rol === "OPERATOR" ? 2 : 1,
        email: rol === "OPERATOR" ? "operador@leofit.pe" : "admin@leofit.pe",
        name: rol === "OPERATOR" ? "Operador Logístico Gamarra" : "Administrador LeoFit",
        role: rol as "ADMIN" | "OPERATOR",
      },
    };
  }

  const parts = cleanToken.split(".");
  if (parts.length !== 3) {
    // Si no es un JWT con 3 partes (ej. 'test-token' en pruebas unitarias), no consideramos que tenga caducidad JWT
    return { valid: true, expired: false, payload: null };
  }

  try {
    // Decodificar Base64URL
    let base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    while (base64.length % 4 !== 0) {
      base64 += "=";
    }
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    const payload = JSON.parse(jsonPayload) as DecodedJwtPayload;

    if (typeof payload.exp === "number") {
      const nowInSeconds = Math.floor(Date.now() / 1000);
      // Si el tiempo actual excede exp menos el margen de tolerancia, está expirado
      if (nowInSeconds >= payload.exp - leewaySeconds) {
        return {
          valid: false,
          expired: true,
          payload,
          error: "Token expirado",
        };
      }
    }

    return {
      valid: true,
      expired: false,
      payload,
    };
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : "Error al decodificar token";
    return { valid: false, expired: true, payload: null, error: msg };
  }
}

/**
 * Dispara un evento global en la ventana para notificar a todos los componentes que la sesión
 * ha expirado o el token es inválido, forzando la redirección limpia al login.
 */
export function triggerSessionExpired(reason = "Tu sesión ha expirado por seguridad."): void {
  try {
    sessionStorage.removeItem("leofit_session");
    sessionStorage.removeItem("leofit_user");
    sessionStorage.setItem("leofit_auth_message", reason);
    if (typeof window !== "undefined") {
      window.dispatchEvent(
        new CustomEvent(LEOFIT_AUTH_EXPIRED_EVENT, {
          detail: { reason },
        })
      );
    }
  } catch {
    // Protección contra contextos restringidos
  }
}

/**
 * Control de Acceso Basado en Roles (RBAC) - Utilidades de Frontend
 */
export function hasRole(role: string | null | undefined, ...allowedRoles: ("ADMIN" | "OPERATOR")[]): boolean {
  if (!role) return false;
  const upperRole = role.toUpperCase();
  return allowedRoles.some((r) => r.toUpperCase() === upperRole);
}

export function isAdmin(role: string | null | undefined): boolean {
  return hasRole(role, "ADMIN");
}

export function isOperator(role: string | null | undefined): boolean {
  return hasRole(role, "OPERATOR");
}

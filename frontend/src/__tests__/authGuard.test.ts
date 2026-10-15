import { describe, it, expect, vi, beforeEach } from "vitest";
import { validateAndDecodeJwt, triggerSessionExpired, LEOFIT_AUTH_EXPIRED_EVENT } from "../services/authGuard";

describe("authGuard Guardrails", () => {
  beforeEach(() => {
    sessionStorage.clear();
    vi.clearAllMocks();
  });

  it("T1: Detecta token nulo o vacío como expirado/inválido", () => {
    expect(validateAndDecodeJwt(null).expired).toBe(true);
    expect(validateAndDecodeJwt("").expired).toBe(true);
    expect(validateAndDecodeJwt("   ").expired).toBe(true);
  });

  it("T2: Tokens de prueba o modo offline son considerados válidos", () => {
    const resMock = validateAndDecodeJwt("token-mock-admin");
    expect(resMock.valid).toBe(true);
    expect(resMock.expired).toBe(false);
    expect(resMock.payload?.role).toBe("ADMIN");

    const resOffline = validateAndDecodeJwt("token-offline-operator");
    expect(resOffline.valid).toBe(true);
    expect(resOffline.expired).toBe(false);
    expect(resOffline.payload?.role).toBe("OPERATOR");
  });

  it("T3: Detecta JWT expirado cuando exp es en el pasado", () => {
    const expPasado = Math.floor(Date.now() / 1000) - 3600; // 1 hora atrás
    const payload = { userId: 1, email: "admin@leofit.pe", role: "ADMIN", exp: expPasado };
    const base64Payload = btoa(JSON.stringify(payload));
    const tokenExpirado = `header.${base64Payload}.signature`;

    const result = validateAndDecodeJwt(tokenExpirado);
    expect(result.valid).toBe(false);
    expect(result.expired).toBe(true);
    expect(result.error).toBe("Token expirado");
  });

  it("T4: Detecta JWT válido cuando exp es en el futuro", () => {
    const expFuturo = Math.floor(Date.now() / 1000) + 7200; // 2 horas adelante
    const payload = { userId: 1, email: "admin@leofit.pe", role: "ADMIN", exp: expFuturo };
    const base64Payload = btoa(JSON.stringify(payload));
    const tokenValido = `header.${base64Payload}.signature`;

    const result = validateAndDecodeJwt(tokenValido);
    expect(result.valid).toBe(true);
    expect(result.expired).toBe(false);
    expect(result.payload?.email).toBe("admin@leofit.pe");
  });

  it("T5: triggerSessionExpired limpia sessionStorage y dispara evento", () => {
    sessionStorage.setItem("leofit_session", "algun-token");
    sessionStorage.setItem("leofit_user", "{\"name\":\"Lady\"}");

    const listener = vi.fn();
    window.addEventListener(LEOFIT_AUTH_EXPIRED_EVENT, listener);

    triggerSessionExpired("Sesión finalizada por inactividad");

    expect(sessionStorage.getItem("leofit_session")).toBeNull();
    expect(sessionStorage.getItem("leofit_user")).toBeNull();
    expect(sessionStorage.getItem("leofit_auth_message")).toBe("Sesión finalizada por inactividad");
    expect(listener).toHaveBeenCalled();

    window.removeEventListener(LEOFIT_AUTH_EXPIRED_EVENT, listener);
  });
});

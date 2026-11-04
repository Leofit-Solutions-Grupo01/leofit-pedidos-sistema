/**
 * @file auth.tokens.ts
 * @description Servicio criptográfico para emisión y rotación de Refresh Tokens y cookies HttpOnly.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 */

import crypto from 'node:crypto';
import type { Response, CookieOptions } from 'express';
import { JWTService, JWTPayload } from '../infrastructure/security/jwt.utils';

export const ACCESS_TTL_SECONDS = 15 * 60; // 15 minutos
export const REFRESH_TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 días en ms
export const REFRESH_COOKIE_NAME = 'leofit_rt';
export const REFRESH_COOKIE_PATH = '/api/auth';

export interface RefreshTokenDescriptor {
  raw: string;
  hash: string;
  expiresAt: Date;
}

/**
 * Emite un nuevo refresh token de alta entropía (48 bytes base64url) con su hash SHA-256.
 */
export function newRefreshToken(): RefreshTokenDescriptor {
  const raw = crypto.randomBytes(48).toString('base64url');
  const hash = crypto.createHash('sha256').update(raw).digest('hex');
  const expiresAt = new Date(Date.now() + REFRESH_TTL_MS);
  return { raw, hash, expiresAt };
}

/**
 * Calcula el hash SHA-256 de un token crudo recibido en la cookie.
 */
export function hashRefresh(raw: string): string {
  return crypto.createHash('sha256').update(raw).digest('hex');
}

/**
 * Genera las opciones seguras de cookie HttpOnly conforme a directrices de seguridad OWASP.
 */
export function refreshCookieOptions(): CookieOptions {
  const isProd = process.env.NODE_ENV === 'production';
  return {
    httpOnly: true,
    secure: isProd,
    sameSite: isProd ? 'none' : 'lax', // Permite envío cross-origin con credenciales
    path: REFRESH_COOKIE_PATH,
    maxAge: REFRESH_TTL_MS,
    domain: process.env.COOKIE_DOMAIN || undefined
  };
}

/**
 * Establece la cookie segura HttpOnly en la respuesta HTTP.
 */
export function setRefreshCookie(res: Response, raw: string): void {
  res.cookie(REFRESH_COOKIE_NAME, raw, refreshCookieOptions());
}

/**
 * Limpia la cookie de refresh token con los mismos parámetros de ruta para garantizar su eliminación en el cliente.
 */
export function clearRefreshCookie(res: Response): void {
  const isProd = process.env.NODE_ENV === 'production';
  res.clearCookie(REFRESH_COOKIE_NAME, {
    path: REFRESH_COOKIE_PATH,
    httpOnly: true,
    secure: isProd,
    sameSite: isProd ? 'none' : 'lax',
    domain: process.env.COOKIE_DOMAIN || undefined
  });
}

/**
 * Helper para emitir un access token usando el JWTService con rotación kid.
 */
export function issueAccessToken(payload: JWTPayload): string {
  return JWTService.generateToken(payload);
}

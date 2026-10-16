// =============================================================================
// JSON WEB TOKEN (JWT) UTILITIES - LEOFIT SECURITY CON ROTACIÓN DE CLAVES (KID)
// =============================================================================

import jwt from 'jsonwebtoken';
import { UserRole } from '../../domain/entities/models';

export interface JWTPayload {
  userId: number;
  id?: number;
  email: string;
  name: string;
  role: UserRole;
  sub?: number;
}

if (!process.env.JWT_SECRET && !process.env.JWT_SECRET_V1) {
  throw new Error('FATAL ERROR: JWT_SECRET must be defined in the environment.');
}

const DEFAULT_SECRET = process.env.JWT_SECRET || process.env.JWT_SECRET_V1!;

const KEYS: Record<string, string> = {
  v1: process.env.JWT_SECRET_V1 || DEFAULT_SECRET,
  v2: process.env.JWT_SECRET_V2 || ''
};

const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '15m';

export class JWTService {
  /**
   * Emite un token JWT firmado con el kid actual (v1/v2) para rotación sin downtime.
   */
  public static generateToken(payload: JWTPayload): string {
    const kid = process.env.JWT_KID || 'v1';
    const secret = KEYS[kid] || DEFAULT_SECRET;

    const tokenPayload = {
      ...payload,
      id: payload.userId,
      sub: payload.userId
    };

    return jwt.sign(tokenPayload, secret, {
      expiresIn: JWT_EXPIRES_IN as jwt.SignOptions['expiresIn'],
      keyid: kid,
      algorithm: 'HS256',
      issuer: 'leofit',
      audience: 'leofit-app'
    });
  }

  /**
   * Valida cualquier token firmado con v1 o v2 decodificando el kid de la cabecera.
   */
  public static verifyToken(token: string): JWTPayload | null {
    try {
      const decoded = jwt.decode(token, { complete: true });
      if (!decoded || typeof decoded !== 'object') return null;

      // Confusión de algoritmo: rechazar explícitamente alg "none" o disímil a HS256
      const alg = (decoded.header as any)?.alg;
      if (!alg || alg.toLowerCase() === 'none' || alg !== 'HS256') {
        return null;
      }

      const kid = (decoded.header as any)?.kid || 'v1';
      const secret = KEYS[kid] || (kid === 'v1' ? DEFAULT_SECRET : '');

      if (!secret) return null;

      const verified = jwt.verify(token, secret, {
        algorithms: ['HS256'],
        issuer: 'leofit',
        audience: 'leofit-app'
      }) as any;

      return {
        userId: verified.userId || verified.sub,
        id: verified.userId || verified.sub,
        email: verified.email || '',
        name: verified.name || '',
        role: verified.role as UserRole
      };
    } catch {
      return null;
    }
  }
}

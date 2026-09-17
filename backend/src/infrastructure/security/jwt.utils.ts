// =============================================================================
// JSON WEB TOKEN (JWT) UTILITIES - LEOFIT SECURITY
// =============================================================================

import jwt from 'jsonwebtoken';
import { UserRole } from '../../domain/entities/models';

export interface JWTPayload {
  userId: number;
  email: string;
  name: string;
  role: UserRole;
}

const JWT_SECRET = process.env.JWT_SECRET || 'leofit_super_secret_jwt_key_academic_2026_production_ready';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '24h';

export class JWTService {
  public static generateToken(payload: JWTPayload): string {
    return jwt.sign(payload, JWT_SECRET, {
      expiresIn: JWT_EXPIRES_IN as jwt.SignOptions['expiresIn']
    });
  }

  public static verifyToken(token: string): JWTPayload | null {
    try {
      return jwt.verify(token, JWT_SECRET) as JWTPayload;
    } catch {
      return null;
    }
  }
}

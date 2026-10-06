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

if (!process.env.JWT_SECRET) {
  throw new Error('FATAL ERROR: JWT_SECRET must be defined in the environment.');
}

const JWT_SECRET = process.env.JWT_SECRET;
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '1h';

export class JWTService {
  public static generateToken(payload: JWTPayload): string {
    return jwt.sign(payload, JWT_SECRET, {
      expiresIn: JWT_EXPIRES_IN as jwt.SignOptions['expiresIn']
    });
  }

  public static verifyToken(token: string): JWTPayload | null {
    try {
      return jwt.verify(token, JWT_SECRET, { algorithms: ['HS256'] }) as JWTPayload;
    } catch {
      return null;
    }
  }
}

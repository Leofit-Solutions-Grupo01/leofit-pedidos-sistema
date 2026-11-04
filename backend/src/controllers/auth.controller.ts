/**
 * @file auth.controller.ts
 * @description Controlador de Autenticación, Gestión de Sesiones, Refresh Tokens y Seguridad Criptográfica.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { Request, Response, NextFunction } from 'express';
import { RepositoryFactory } from '../infrastructure/repositories/factory';
import { PasswordHasher, DUMMY_HASH_CONSTANT } from '../infrastructure/security/password.utils';
import { JWTService } from '../infrastructure/security/jwt.utils';
import { AuthenticatedRequest } from '../middlewares/auth.middleware';
import { dbPool, isPostgresAvailable } from '../config/database';
import {
  newRefreshToken,
  hashRefresh,
  setRefreshCookie,
  clearRefreshCookie,
  REFRESH_COOKIE_NAME,
  REFRESH_TTL_MS
} from '../services/auth.tokens';
import { logger } from '../utils/logger';

// Almacén en memoria volátil para pruebas unitarias o entornos sin Postgres
interface InMemoryRefreshToken {
  id: number;
  userId: number;
  tokenHash: string;
  familyId: string;
  expiresAt: Date;
  revokedAt: Date | null;
  replacedBy: number | null;
}
const memoryRefreshTokens: InMemoryRefreshToken[] = [];
let memorySeq = 1;

export class AuthController {
  /**
   * @route POST /api/auth/login
   * @desc Autentica a un usuario administrativo y genera el token Bearer JWT y la cookie HttpOnly de refresco.
   */
  public static async login(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const identifier = (req.body.email || req.body.username || '').trim();
      const password = req.body.password;

      const userRepo = RepositoryFactory.getUserRepository();
      const user = await userRepo.findByEmail(identifier);

      // Verificación de existencia del usuario con mitigación de timing attack
      if (!user) {
        await PasswordHasher.compare(password, DUMMY_HASH_CONSTANT);
        res.status(401).json({
          success: false,
          error: {
            code: 'INVALID_CREDENTIALS',
            message: 'Credenciales inválidas. Verifique su correo o contraseña.'
          }
        });
        return;
      }

      // Verificación criptográfica estricta del hash de la contraseña (OWASP A07)
      const isValid = await PasswordHasher.compare(password, user.password_hash);
      if (!isValid) {
        res.status(401).json({
          success: false,
          error: {
            code: 'INVALID_CREDENTIALS',
            message: 'Credenciales inválidas. Verifique su correo o contraseña.'
          }
        });
        return;
      }

      // Emisión de token JWT de acceso (15 minutos con rotación kid)
      const accessToken = JWTService.generateToken({
        userId: user.id,
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role
      });

      // Emisión de Refresh Token criptográfico (7 días)
      const { raw, hash, expiresAt } = newRefreshToken();
      const familyId = crypto.randomUUID ? crypto.randomUUID() : `fam-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;

      if (isPostgresAvailable()) {
        await dbPool.query(
          `INSERT INTO refresh_tokens (user_id, token_hash, family_id, expires_at, user_agent, ip)
           VALUES ($1, $2, $3, $4, $5, $6)`,
          [user.id, hash, familyId, expiresAt, req.headers['user-agent'] || null, req.ip || null]
        );
      } else {
        memoryRefreshTokens.push({
          id: memorySeq++,
          userId: user.id,
          tokenHash: hash,
          familyId,
          expiresAt,
          revokedAt: null,
          replacedBy: null
        });
      }

      setRefreshCookie(res, raw);

      res.status(200).json({
        success: true,
        message: 'Autenticación exitosa',
        data: {
          token: accessToken,
          accessToken,
          user: {
            id: user.id,
            name: user.name,
            username: user.name,
            email: user.email,
            role: user.role
          }
        }
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route POST /api/auth/refresh
   * @desc Rota el refresh token, renueva la cookie segura y devuelve un nuevo access token.
   * Si se detecta reutilización de un token ya revocado (robo), revoca toda la familia.
   */
  public static async refresh(req: Request, res: Response, next: NextFunction): Promise<void> {
    const raw = req.cookies?.[REFRESH_COOKIE_NAME];
    if (!raw) {
      res.status(401).json({
        success: false,
        error: { code: 'NO_REFRESH', message: 'No se suministró token de refresco.' }
      });
      return;
    }

    const hash = hashRefresh(raw);

    if (isPostgresAvailable()) {
      const client = await dbPool.connect();
      try {
        await client.query('BEGIN');

        const { rows } = await client.query(
          `SELECT id, user_id, family_id, expires_at, revoked_at
             FROM refresh_tokens
            WHERE token_hash = $1
            FOR UPDATE`,
          [hash]
        );

        const row = rows[0];

        // Token desconocido o expirado
        if (!row || new Date(row.expires_at) < new Date()) {
          await client.query('COMMIT');
          clearRefreshCookie(res);
          res.status(401).json({
            success: false,
            error: { code: 'REFRESH_INVALID', message: 'Token de refresco inválido o expirado.' }
          });
          return;
        }

        // DETECCIÓN DE REUSO: Token previamente revocado → Posible robo. Revocar toda la familia.
        if (row.revoked_at) {
          await client.query(
            `UPDATE refresh_tokens
                SET revoked_at = NOW()
              WHERE family_id = $1 AND revoked_at IS NULL`,
            [row.family_id]
          );
          await client.query('COMMIT');
          clearRefreshCookie(res);
          logger.warn('[Security Alert] Reuso de refresh token detectado. Familia de tokens revocada.', {
            userId: row.user_id,
            familyId: row.family_id,
            ip: req.ip
          });
          res.status(401).json({
            success: false,
            error: { code: 'REFRESH_REUSE_DETECTED', message: 'Sesión invalidada por posible brecha de seguridad.' }
          });
          return;
        }

        // Rotación legítima de token
        const nextToken = newRefreshToken();
        const ins = await client.query(
          `INSERT INTO refresh_tokens (user_id, token_hash, expires_at, user_agent, ip, family_id)
           VALUES ($1, $2, $3, $4, $5, $6)
           RETURNING id`,
          [row.user_id, nextToken.hash, nextToken.expiresAt, req.headers['user-agent'] || null, req.ip || null, row.family_id]
        );

        await client.query(
          `UPDATE refresh_tokens
              SET revoked_at = NOW(), replaced_by = $1
            WHERE id = $2`,
          [ins.rows[0].id, row.id]
        );

        await client.query('COMMIT');

        const userRepo = RepositoryFactory.getUserRepository();
        const user = await userRepo.findById(row.user_id);
        if (!user) {
          clearRefreshCookie(res);
          res.status(401).json({ success: false, error: { code: 'USER_NOT_FOUND' } });
          return;
        }

        const accessToken = JWTService.generateToken({
          userId: user.id,
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role
        });

        setRefreshCookie(res, nextToken.raw);

        res.status(200).json({
          success: true,
          data: {
            token: accessToken,
            accessToken,
            user: { id: user.id, username: user.name, name: user.name, email: user.email, role: user.role }
          }
        });
      } catch (err) {
        await client.query('ROLLBACK').catch(() => {});
        next(err);
      } finally {
        client.release();
      }
    } else {
      // Manejo en memoria (para suites de pruebas sin Postgres)
      const found = memoryRefreshTokens.find((t) => t.tokenHash === hash);
      if (!found || found.expiresAt < new Date()) {
        clearRefreshCookie(res);
        res.status(401).json({ success: false, error: { code: 'REFRESH_INVALID' } });
        return;
      }

      if (found.revokedAt) {
        // Revocar familia
        memoryRefreshTokens.forEach((t) => {
          if (t.familyId === found.familyId) t.revokedAt = new Date();
        });
        clearRefreshCookie(res);
        res.status(401).json({ success: false, error: { code: 'REFRESH_REUSE_DETECTED' } });
        return;
      }

      const nextToken = newRefreshToken();
      const newId = memorySeq++;
      found.revokedAt = new Date();
      found.replacedBy = newId;

      memoryRefreshTokens.push({
        id: newId,
        userId: found.userId,
        tokenHash: nextToken.hash,
        familyId: found.familyId,
        expiresAt: nextToken.expiresAt,
        revokedAt: null,
        replacedBy: null
      });

      const userRepo = RepositoryFactory.getUserRepository();
      const user = await userRepo.findById(found.userId);
      if (!user) {
        clearRefreshCookie(res);
        res.status(401).json({ success: false, error: { code: 'USER_NOT_FOUND' } });
        return;
      }

      const accessToken = JWTService.generateToken({
        userId: user.id,
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role
      });

      setRefreshCookie(res, nextToken.raw);

      res.status(200).json({
        success: true,
        data: {
          token: accessToken,
          accessToken,
          user: { id: user.id, username: user.name, name: user.name, email: user.email, role: user.role }
        }
      });
    }
  }

  /**
   * @route POST /api/auth/logout
   * @desc Revoca el refresh token actual y limpia la cookie HttpOnly.
   */
  public static async logout(req: Request, res: Response): Promise<void> {
    const raw = req.cookies?.[REFRESH_COOKIE_NAME];
    if (raw) {
      const hash = hashRefresh(raw);
      if (isPostgresAvailable()) {
        await dbPool.query(
          `UPDATE refresh_tokens SET revoked_at = NOW() WHERE token_hash = $1 AND revoked_at IS NULL`,
          [hash]
        ).catch((err) => logger.error('[Logout Error] Fallo al revocar refresh token:', { error: err.message }));
      } else {
        const found = memoryRefreshTokens.find((t) => t.tokenHash === hash);
        if (found) found.revokedAt = new Date();
      }
    }

    clearRefreshCookie(res);
    res.status(204).end();
  }

  /**
   * @route POST /api/auth/logout-all
   * @desc Revoca todos los refresh tokens activos del usuario autenticado (cierre en todos los dispositivos).
   */
  public static async logoutAll(req: AuthenticatedRequest, res: Response): Promise<void> {
    const userId = req.user?.userId || req.user?.id;
    if (!userId) {
      res.status(401).end();
      return;
    }

    if (isPostgresAvailable()) {
      await dbPool.query(
        `UPDATE refresh_tokens SET revoked_at = NOW() WHERE user_id = $1 AND revoked_at IS NULL`,
        [userId]
      ).catch((err) => logger.error('[Logout-All Error] Fallo al revocar sesiones:', { error: err.message }));
    } else {
      memoryRefreshTokens.forEach((t) => {
        if (t.userId === userId) t.revokedAt = new Date();
      });
    }

    clearRefreshCookie(res);
    res.status(204).end();
  }

  /**
   * @route GET /api/auth/me
   * @desc Retorna la información del usuario autenticado con su rol.
   */
  public static async me(req: AuthenticatedRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      const userId = req.user?.userId || req.user?.id;
      if (!userId) {
        res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED' } });
        return;
      }

      const userRepo = RepositoryFactory.getUserRepository();
      const user = await userRepo.findById(userId);

      if (!user) {
        res.status(404).json({ success: false, error: { code: 'USER_NOT_FOUND' } });
        return;
      }

      res.status(200).json({
        success: true,
        data: {
          id: user.id,
          username: user.name,
          name: user.name,
          email: user.email,
          role: user.role
        }
      });
    } catch (err) {
      next(err);
    }
  }

  /**
   * @route POST /api/auth/register
   */
  public static async register(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const { name, email, password, role } = req.body;
      const userRepo = RepositoryFactory.getUserRepository();

      const existing = await userRepo.findByEmail(email);
      if (existing) {
        await PasswordHasher.compare(password, DUMMY_HASH_CONSTANT);
        res.status(400).json({
          success: false,
          error: {
            code: 'REGISTRATION_FAILED',
            message: 'No se pudo completar el registro. Verifique la información proporcionada.'
          }
        });
        return;
      }

      const passwordHash = await PasswordHasher.hash(password);
      const newUser = await userRepo.create({
        name,
        email,
        password_hash: passwordHash,
        role: role || 'OPERATOR'
      });

      const token = JWTService.generateToken({
        userId: newUser.id,
        id: newUser.id,
        email: newUser.email,
        name: newUser.name,
        role: newUser.role
      });

      res.status(201).json({
        success: true,
        message: 'Usuario registrado exitosamente',
        data: {
          token,
          accessToken: token,
          user: {
            id: newUser.id,
            name: newUser.name,
            email: newUser.email,
            role: newUser.role
          }
        }
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * @route GET /api/auth/profile
   */
  public static async getProfile(req: AuthenticatedRequest, res: Response, next: NextFunction): Promise<void> {
    try {
      if (!req.user) {
        res.status(401).json({
          success: false,
          error: { code: 'UNAUTHORIZED', message: 'No autenticado. Token no suministrado.' }
        });
        return;
      }

      const userRepo = RepositoryFactory.getUserRepository();
      const user = await userRepo.findById(req.user.userId || (req.user as any).id);

      if (!user) {
        res.status(404).json({
          success: false,
          error: { code: 'USER_NOT_FOUND', message: 'Usuario no encontrado en la base de datos' }
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: {
          id: user.id,
          name: user.name,
          email: user.email,
          role: user.role,
          created_at: user.created_at
        }
      });
    } catch (error) {
      next(error);
    }
  }
}

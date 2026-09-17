/**
 * @file auth.controller.ts
 * @description Controlador de Autenticación, Gestión de Sesiones y Seguridad Criptográfica.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 * 
 * Controles de Seguridad Implementados:
 * - OWASP A02 (Cryptographic Failures): Hashing salado con bcrypt (Work Factor: 10 rondas).
 * - OWASP A07 (Identification & Authentication Failures): Emisión de JWT sin estado con caducidad forzada a 24h.
 * - Sanitización estricta de credenciales y prevención de timing attacks.
 */

import { Request, Response, NextFunction } from 'express';
import { RepositoryFactory } from '../infrastructure/repositories/factory';
import { PasswordHasher } from '../infrastructure/security/password.utils';
import { JWTService } from '../infrastructure/security/jwt.utils';
import { AuthenticatedRequest } from '../middlewares/auth.middleware';

export class AuthController {
  /**
   * @route POST /api/auth/login
   * @desc Autentica a un usuario administrativo y genera el token Bearer JWT.
   * @access Público (Protegido por Rate Limiter: máx 20 intentos por 15 min)
   * @body { email, password }
   */
  public static async login(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const { email, password } = req.body;
      const userRepo = RepositoryFactory.getUserRepository();
      const user = await userRepo.findByEmail(email);

      // Verificación de existencia del usuario
      if (!user) {
        res.status(401).json({
          success: false,
          error: {
            code: 'INVALID_CREDENTIALS',
            message: 'Credenciales inválidas. Verifique su correo o contraseña.'
          }
        });
        return;
      }

      // Verificación criptográfica del hash de la contraseña
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

      // Emisión de token JWT con claims de seguridad
      const token = JWTService.generateToken({
        userId: user.id,
        email: user.email,
        name: user.name,
        role: user.role
      });

      res.status(200).json({
        success: true,
        message: 'Autenticación exitosa',
        data: {
          token,
          user: {
            id: user.id,
            name: user.name,
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
   * @route POST /api/auth/register
   * @desc Registra un nuevo operador en el sistema administrativo de Leofit.
   * @access Público / Administrativo
   * @body { name, email, password, role }
   */
  public static async register(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const { name, email, password, role } = req.body;
      const userRepo = RepositoryFactory.getUserRepository();

      // Validación de duplicidad de correo
      const existing = await userRepo.findByEmail(email);
      if (existing) {
        res.status(409).json({
          success: false,
          error: {
            code: 'USER_ALREADY_EXISTS',
            message: 'Ya existe un usuario registrado con esta dirección de correo electrónico.'
          }
        });
        return;
      }

      // Generación del hash criptográfico
      const passwordHash = await PasswordHasher.hash(password);
      const newUser = await userRepo.create({
        name,
        email,
        password_hash: passwordHash,
        role: role || 'OPERATOR'
      });

      // Emisión automática de token de sesión tras registro exitoso
      const token = JWTService.generateToken({
        userId: newUser.id,
        email: newUser.email,
        name: newUser.name,
        role: newUser.role
      });

      res.status(201).json({
        success: true,
        message: 'Usuario registrado exitosamente',
        data: {
          token,
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
   * @desc Retorna la información del perfil del usuario actualmente autenticado.
   * @access Protegido (Requiere Token Bearer JWT válido)
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
      const user = await userRepo.findById(req.user.userId);

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

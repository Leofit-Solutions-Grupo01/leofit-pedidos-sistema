// =============================================================================
// AUTH ROUTES - /api/auth
// =============================================================================

import { Router } from 'express';
import { AuthController } from '../controllers/auth.controller';
import { validateBody } from '../middlewares/validate.middleware';
import { requireRole } from '../middlewares/role.middleware';
import { LoginSchema, RegisterUserSchema } from '../infrastructure/validators/schemas';
import { authenticateToken } from '../middlewares/auth.middleware';
import { authRateLimiter, refreshLimiter } from '../middlewares/rateLimit.middleware';

const router = Router();

router.post('/login', authRateLimiter, validateBody(LoginSchema), AuthController.login);
router.post('/refresh', refreshLimiter, AuthController.refresh);
router.post('/logout', AuthController.logout);
router.post('/logout-all', authenticateToken, AuthController.logoutAll);
router.get('/me', authenticateToken, AuthController.me);
router.post('/register', authenticateToken, requireRole('ADMIN'), validateBody(RegisterUserSchema), AuthController.register);
router.get('/profile', authenticateToken, AuthController.getProfile);

export default router;

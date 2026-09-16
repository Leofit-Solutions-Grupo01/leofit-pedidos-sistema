// =============================================================================
// AUTH ROUTES - /api/auth
// =============================================================================

import { Router } from 'express';
import { AuthController } from '../controllers/auth.controller';
import { validateBody } from '../middlewares/validate.middleware';
import { LoginSchema, RegisterUserSchema } from '../infrastructure/validators/schemas';
import { authenticateToken } from '../middlewares/auth.middleware';
import { authRateLimiter } from '../middlewares/rateLimit.middleware';

const router = Router();

router.post('/login', authRateLimiter, validateBody(LoginSchema), AuthController.login);
router.post('/register', validateBody(RegisterUserSchema), AuthController.register);
router.get('/profile', authenticateToken, AuthController.getProfile);

export default router;

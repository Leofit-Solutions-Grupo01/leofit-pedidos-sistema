// =============================================================================
// EXPRESS APPLICATION INITIALIZATION - LEOFIT BACKEND API
// =============================================================================

import express, { Express } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import apiRoutes from './routes';
import { errorHandler } from './middlewares/error.middleware';
import { apiRateLimiter } from './middlewares/rateLimit.middleware';
import { externalController } from './controllers/external.controller';

dotenv.config();

export function createApp(): Express {
  const app = express();

  // Security Headers (Helmet)
  app.use(helmet({
    contentSecurityPolicy: false,
    crossOriginResourcePolicy: { policy: 'cross-origin' }
  }));

  // CORS Policy (Permite GitHub Pages, Netlify y Desarrollo Local)
  if (process.env.NODE_ENV === 'production' && !process.env.CORS_ORIGIN) {
    throw new Error('FATAL ERROR: CORS_ORIGIN must be defined in production environment.');
  }
  const corsOrigin = process.env.CORS_ORIGIN || 'http://localhost:5173';
  const allowedList = corsOrigin.split(',').map((o) => o.trim()).filter(Boolean);

  app.use(cors({
    origin: (origin, callback) => {
      // Peticiones sin origen (ej. curl, salud, mobile, postman)
      if (!origin) return callback(null, true);

      // Coincidencia exacta con lista configurada
      if (allowedList.includes(origin) || allowedList.includes('*')) {
        return callback(null, true);
      }

      // Soporte dinámico para Netlify, GitHub Pages y Localhost
      if (
        origin.endsWith('.netlify.app') ||
        origin.endsWith('.github.io') ||
        origin.endsWith('.vercel.app') ||
        /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin)
      ) {
        return callback(null, true);
      }

      return callback(new Error(`CORS bloqueado para el origen: ${origin}`));
    },
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Idempotency-Key', 'X-Idempotency-Key', 'X-Correlation-ID'],
    exposedHeaders: ['X-Total-Count', 'X-Correlation-ID', 'Idempotency-Key', 'Retry-After', 'X-Cache-Lookup'],
    credentials: true
  }));

  // Correlation ID & Request Tracking (Trazabilidad E2E en logs y errores)
  app.use((req, res, next) => {
    const rawCorrId = req.headers['x-correlation-id'] || req.headers['x-request-id'];
    const correlationId = (typeof rawCorrId === 'string' && rawCorrId.trim())
      ? rawCorrId.trim()
      : (crypto.randomUUID ? crypto.randomUUID() : `req-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`);
    req.headers['x-correlation-id'] = correlationId;
    res.setHeader('X-Correlation-ID', correlationId);
    next();
  });

  // Request Rate Limiting
  app.use('/api/', apiRateLimiter);

  // Webhook Route (MUST be before express.json to capture raw buffer)
  app.post('/api/external/payments/webhook', express.raw({ type: 'application/json', limit: '1mb' }), externalController.handlePaymentWebhook);

  // Body parsers
  app.use(express.json({ limit: '100kb' }));
  app.use(express.urlencoded({ extended: true, limit: '100kb' }));

  // HTTP Request Logging
  if (process.env.NODE_ENV !== 'test') {
    app.use(morgan('dev'));
  }

  // Root welcome
  app.get('/', (req, res) => {
    res.json({
      name: 'Leofit Solutions Backend API',
      version: '2.0.0',
      status: 'ONLINE',
      docs: '/api/health',
      timestamp: new Date().toISOString()
    });
  });

  // API Routes
  app.use('/api', apiRoutes);

  // 404 Route Handler
  app.use((req, res) => {
    res.status(404).json({
      success: false,
      error: {
        code: 'NOT_FOUND',
        message: `La ruta solicitada [${req.method} ${req.originalUrl}] no existe en el servidor`
      }
    });
  });

  // Centralized Error Handling
  app.use(errorHandler);

  return app;
}

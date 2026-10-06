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

  // CORS Policy
  if (process.env.NODE_ENV === 'production' && !process.env.CORS_ORIGIN) {
    throw new Error('FATAL ERROR: CORS_ORIGIN must be defined in production environment.');
  }
  const corsOrigin = process.env.CORS_ORIGIN || 'http://localhost:5173';
  app.use(cors({
    origin: corsOrigin.split(','),
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
  }));

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

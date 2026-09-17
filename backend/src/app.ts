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

dotenv.config();

export function createApp(): Express {
  const app = express();

  // Security Headers (Helmet)
  app.use(helmet({
    contentSecurityPolicy: false,
    crossOriginResourcePolicy: { policy: 'cross-origin' }
  }));

  // CORS Policy
  const corsOrigin = process.env.CORS_ORIGIN || '*';
  app.use(cors({
    origin: corsOrigin === '*' ? '*' : corsOrigin.split(','),
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
  }));

  // Request Rate Limiting
  app.use('/api/', apiRateLimiter);

  // Body parsers
  app.use(express.json({ limit: '10mb' }));
  app.use(express.urlencoded({ extended: true, limit: '10mb' }));

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

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
import { logger, asyncLocalStorage } from './utils/logger';

dotenv.config();

export function createApp(isDrainingSupplier?: () => boolean): Express {
  const app = express();

  // Security Headers (Helmet con OWASP Best Practices y HSTS estricto)
  app.use(helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
        connectSrc: ["'self'", 'https://leofit.netlify.app', 'https://*.onrender.com'],
      },
    },
    hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
    frameguard: { action: 'deny' },
    crossOriginResourcePolicy: { policy: 'cross-origin' },
    xContentTypeOptions: true,
    referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
  }));

  // Draining & Graceful Disconnect Middleware (quitar la instancia de cualquier sonda de Render/AWS/Cloudflare)
  app.use((req, res, next) => {
    if (isDrainingSupplier && isDrainingSupplier()) {
      res.setHeader('Connection', 'close');
      if (req.path.includes('/health')) {
        res.setHeader('Retry-After', '5');
        res.status(503).json({
          status: 'DRAINING',
          message: 'Instancia en proceso de apagado seguro. Tráfico redirigido.'
        });
        return;
      }
    }
    next();
  });

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
    exposedHeaders: ['X-Total-Count', 'X-Correlation-ID', 'Idempotency-Key', 'Retry-After', 'X-Cache-Lookup', 'RateLimit-Limit', 'RateLimit-Remaining', 'RateLimit-Reset', 'X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-Reset'],
    credentials: true
  }));

  // Correlation ID con Sanitización Estricta y Propagación vía AsyncLocalStorage
  app.use((req, res, next) => {
    const rawCorrId = req.headers['x-correlation-id'] || req.headers['x-request-id'];
    let correlationId: string;

    if (typeof rawCorrId === 'string') {
      const trimmed = rawCorrId.trim();
      if (/^[a-zA-Z0-9_\-]{8,64}$/.test(trimmed)) {
        correlationId = trimmed;
      } else {
        // Log de auditoría por posible intento de log injection o header malformado
        logger.audit('Alerta de Seguridad: X-Correlation-ID rechazado por formato inválido', {
          rejectedCid: rawCorrId,
          ip: req.ip,
          path: req.path
        });
        correlationId = crypto.randomUUID ? crypto.randomUUID() : `req-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
      }
    } else {
      correlationId = crypto.randomUUID ? crypto.randomUUID() : `req-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    }

    req.headers['x-correlation-id'] = correlationId;
    res.setHeader('X-Correlation-ID', correlationId);

    asyncLocalStorage.run({ correlationId }, () => {
      next();
    });
  });

  // Content-Type Guard (HTTP 415 Unsupported Media Type para mutaciones)
  app.use((req, res, next) => {
    if (['POST', 'PUT', 'PATCH'].includes(req.method)) {
      if (req.path.includes('/webhook')) return next();
      const contentType = req.headers['content-type'];
      const contentLength = parseInt(req.headers['content-length'] || '0', 10);
      if (contentLength > 0 && contentType && !contentType.includes('application/json') && !contentType.includes('application/x-www-form-urlencoded')) {
        res.status(415).json({
          success: false,
          error: {
            code: 'UNSUPPORTED_MEDIA_TYPE',
            message: 'El tipo de contenido no es compatible. Envíe application/json'
          }
        });
        return;
      }
    }
    next();
  });

  // Request Rate Limiting (excluye /health para no quemar cuotas de orquestadores)
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

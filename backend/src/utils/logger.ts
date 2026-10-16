/**
 * @file logger.ts
 * @description Logger estructurado JSON con propagación automática de Correlation-ID vía AsyncLocalStorage.
 * @project LeoFit Solutions - Sistema de Gestión de Pedidos
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz)
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import { AsyncLocalStorage } from 'async_hooks';

export interface LogContext {
  correlationId: string;
  userId?: number;
}

export const asyncLocalStorage = new AsyncLocalStorage<LogContext>();

export function getCorrelationId(): string {
  return asyncLocalStorage.getStore()?.correlationId || 'no-cid';
}

function formatLog(level: 'INFO' | 'WARN' | 'ERROR' | 'AUDIT', message: string, meta?: any): string {
  const store = asyncLocalStorage.getStore();
  const logObject = {
    timestamp: new Date().toISOString(),
    level,
    correlationId: store?.correlationId || 'no-cid',
    ...(store?.userId ? { userId: store.userId } : {}),
    message,
    ...(meta ? { meta } : {})
  };
  return JSON.stringify(logObject);
}

export const logger = {
  info: (message: string, meta?: any) => {
    console.log(formatLog('INFO', message, meta));
  },
  warn: (message: string, meta?: any) => {
    console.warn(formatLog('WARN', message, meta));
  },
  error: (message: string, meta?: any) => {
    console.error(formatLog('ERROR', message, meta));
  },
  audit: (message: string, meta?: any) => {
    console.warn(formatLog('AUDIT', message, meta));
  }
};

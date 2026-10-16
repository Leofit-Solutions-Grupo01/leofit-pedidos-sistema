/**
 * @file types.ts
 * @description Contrato estándar para migraciones versionadas y transaccionales en PostgreSQL.
 */

import { PoolClient } from 'pg';

export interface Migration {
  version: string;
  name: string;
  up(client: PoolClient): Promise<void>;
  down?(client: PoolClient): Promise<void>;
}

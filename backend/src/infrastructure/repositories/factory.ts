// =============================================================================
// REPOSITORY FACTORY - DEPENDENCY INJECTION & REPOSITORY PATTERN
// =============================================================================

import { isPostgresAvailable } from '../../config/database';
import {
  IUserRepository,
  ICategoryRepository,
  IProductRepository,
  IClientRepository,
  IOrderRepository
} from '../../domain/repositories/interfaces';
import {
  MemoryUserRepository,
  MemoryCategoryRepository,
  MemoryProductRepository,
  MemoryClientRepository,
  MemoryOrderRepository
} from './memory.repositories';
import {
  PgUserRepository,
  PgCategoryRepository,
  PgProductRepository,
  PgClientRepository,
  PgOrderRepository
} from './pg.repositories';

// Cached singleton instances
const memoryUserRepo = new MemoryUserRepository();
const memoryCategoryRepo = new MemoryCategoryRepository();
const memoryProductRepo = new MemoryProductRepository();
const memoryClientRepo = new MemoryClientRepository();
const memoryOrderRepo = new MemoryOrderRepository();

const pgUserRepo = new PgUserRepository();
const pgCategoryRepo = new PgCategoryRepository();
const pgProductRepo = new PgProductRepository();
const pgClientRepo = new PgClientRepository();
const pgOrderRepo = new PgOrderRepository();

export class RepositoryFactory {
  public static getUserRepository(): IUserRepository {
    return isPostgresAvailable() ? pgUserRepo : memoryUserRepo;
  }

  public static getCategoryRepository(): ICategoryRepository {
    return isPostgresAvailable() ? pgCategoryRepo : memoryCategoryRepo;
  }

  public static getProductRepository(): IProductRepository {
    return isPostgresAvailable() ? pgProductRepo : memoryProductRepo;
  }

  public static getClientRepository(): IClientRepository {
    return isPostgresAvailable() ? pgClientRepo : memoryClientRepo;
  }

  public static getOrderRepository(): IOrderRepository {
    return isPostgresAvailable() ? pgOrderRepo : memoryOrderRepo;
  }
}

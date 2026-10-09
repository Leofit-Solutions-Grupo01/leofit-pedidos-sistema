// =============================================================================
// POSTGRESQL PRODUCTION REPOSITORIES (DAO / REPOSITORY PATTERN)
// PARAMETERIZED QUERIES AGAINST SQL INJECTION & ACID TRANSACTIONS
// =============================================================================

import { Pool, PoolClient } from 'pg';
import { dbPool } from '../../config/database';
import {
  User,
  Category,
  Product,
  ProductVariant,
  Client,
  Order,
  OrderItem,
  OrderStatus,
  DashboardMetrics,
  ActivityRecord
} from '../../domain/entities/models';
import {
  IUserRepository,
  ICategoryRepository,
  IProductRepository,
  IClientRepository,
  IOrderRepository,
  CreateOrderDTO,
  IsolationLevel
} from '../../domain/repositories/interfaces';

// -----------------------------------------------------------------------------
// FRAGMENTOS SQL COMPARTIDOS — alineados con el esquema normalizado (BCNF)
// de database/schema.sql: tallas, colores, distritos y métodos de pago viven en
// tablas de catálogo y se resuelven con JOIN (no son columnas de texto).
// -----------------------------------------------------------------------------
const VARIANT_COLUMNS = `
  pv.id, pv.product_id, s.code AS size, col.name AS color, pv.sku, pv.stock,
  pv.alert_threshold, pv.created_at, pv.updated_at`;
const VARIANT_FROM = `
  FROM product_variants pv
  JOIN sizes  s   ON s.id   = pv.size_id
  JOIN colors col ON col.id = pv.color_id`;
const CLIENT_COLUMNS = `
  c.id, c.full_name, c.phone, c.address, d.name AS district,
  c.reference, c.created_at, c.updated_at`;
const CLIENT_FROM = `
  FROM clients c
  JOIN districts d ON d.id = c.district_id`;
const ORDER_ITEM_SELECT = `
  SELECT oi.id, oi.order_id, oi.variant_id, oi.quantity, oi.unit_price, oi.subtotal,
         p.name AS product_name, s.code AS size, col.name AS color, pv.sku
  FROM order_items oi
  JOIN product_variants pv ON oi.variant_id = pv.id
  JOIN sizes   s   ON s.id   = pv.size_id
  JOIN colors  col ON col.id = pv.color_id
  JOIN products p  ON pv.product_id = p.id`;

/** Redondeo monetario a 2 decimales (evita 99.80000000000001 en CHECK de NUMERIC). */
const round2 = (n: number): number => Math.round((n + Number.EPSILON) * 100) / 100;

/** Devuelve el id del distrito, creándolo si aún no existe en el catálogo. */
async function upsertDistrict(db: Pool | PoolClient, name: string): Promise<number> {
  const res = await db.query(
    `INSERT INTO districts (name) VALUES ($1)
     ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
     RETURNING id`,
    [name.trim()]
  );
  return res.rows[0].id;
}

const mapOrderItem = (item: any) => ({
  id: item.id,
  variant_id: item.variant_id,
  product_name: item.product_name,
  size: item.size,
  color: item.color,
  sku: item.sku,
  quantity: item.quantity,
  unit_price: parseFloat(item.unit_price),
  subtotal: parseFloat(item.subtotal)
});

export class PgUserRepository implements IUserRepository {
  private pool: Pool = dbPool;

  async findByEmail(email: string): Promise<User | null> {
    const res = await this.pool.query(
      'SELECT id, name, email, password_hash, role, created_at, updated_at FROM users WHERE LOWER(email) = LOWER($1)',
      [email]
    );
    return res.rows[0] || null;
  }

  async findById(id: number): Promise<User | null> {
    const res = await this.pool.query(
      'SELECT id, name, email, password_hash, role, created_at, updated_at FROM users WHERE id = $1',
      [id]
    );
    return res.rows[0] || null;
  }

  async create(user: Omit<User, 'id' | 'created_at' | 'updated_at'>): Promise<User> {
    const res = await this.pool.query(
      'INSERT INTO users (name, email, password_hash, role) VALUES ($1, $2, $3, $4) RETURNING *',
      [user.name, user.email, user.password_hash, user.role]
    );
    return res.rows[0];
  }

  async listAll(): Promise<User[]> {
    const res = await this.pool.query(
      'SELECT id, name, email, role, created_at, updated_at FROM users ORDER BY id ASC'
    );
    return res.rows;
  }
}

export class PgCategoryRepository implements ICategoryRepository {
  private pool: Pool = dbPool;

  async listAll(): Promise<Category[]> {
    const res = await this.pool.query('SELECT * FROM categories ORDER BY id ASC');
    return res.rows;
  }

  async findById(id: number): Promise<Category | null> {
    const res = await this.pool.query('SELECT * FROM categories WHERE id = $1', [id]);
    return res.rows[0] || null;
  }

  async create(category: Omit<Category, 'id' | 'created_at'>): Promise<Category> {
    const res = await this.pool.query(
      'INSERT INTO categories (name, description) VALUES ($1, $2) RETURNING *',
      [category.name, category.description || null]
    );
    return res.rows[0];
  }
}

export class PgProductRepository implements IProductRepository {
  private pool: Pool = dbPool;

  async listAll(filters?: { categoryId?: number; isActive?: boolean; search?: string }): Promise<Product[]> {
    let query = `
      SELECT p.*, c.name as category_name 
      FROM products p 
      JOIN categories c ON p.category_id = c.id
      WHERE 1=1
    `;
    const params: any[] = [];

    if (filters?.categoryId) {
      params.push(filters.categoryId);
      query += ` AND p.category_id = $${params.length}`;
    }
    if (filters?.isActive !== undefined) {
      params.push(filters.isActive);
      query += ` AND p.is_active = $${params.length}`;
    }
    if (filters?.search) {
      params.push(`%${filters.search}%`);
      query += ` AND (LOWER(p.name) LIKE LOWER($${params.length}) OR LOWER(p.description) LIKE LOWER($${params.length}))`;
    }

    query += ' ORDER BY p.id ASC';
    const res = await this.pool.query(query, params);

    // Variantes de todos los productos en UNA consulta (evita N+1)
    const products: Product[] = res.rows;
    if (products.length > 0) {
      const vRes = await this.pool.query(
        `SELECT ${VARIANT_COLUMNS} ${VARIANT_FROM}
         WHERE pv.product_id = ANY($1::int[]) ORDER BY pv.id ASC`,
        [products.map((p) => p.id)]
      );
      for (const prod of products) {
        prod.variants = vRes.rows.filter((v) => v.product_id === prod.id);
      }
    }

    return products;
  }

  async findById(id: number): Promise<Product | null> {
    const res = await this.pool.query(
      `SELECT p.*, c.name as category_name 
       FROM products p 
       JOIN categories c ON p.category_id = c.id 
       WHERE p.id = $1`,
      [id]
    );
    if (res.rows.length === 0) return null;
    const prod: Product = res.rows[0];
    const vRes = await this.pool.query(
      `SELECT ${VARIANT_COLUMNS} ${VARIANT_FROM} WHERE pv.product_id = $1 ORDER BY pv.id ASC`,
      [prod.id]
    );
    prod.variants = vRes.rows;
    return prod;
  }

  async findBySku(sku: string): Promise<ProductVariant | null> {
    const res = await this.pool.query(
      `SELECT ${VARIANT_COLUMNS} ${VARIANT_FROM} WHERE LOWER(pv.sku) = LOWER($1)`,
      [sku]
    );
    return res.rows[0] || null;
  }

  async create(product: Omit<Product, 'id' | 'created_at' | 'updated_at'>): Promise<Product> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      const pRes = await client.query(
        `INSERT INTO products (category_id, name, description, base_price, image_url, is_active)
         VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
        [product.category_id, product.name, product.description || null, product.base_price, product.image_url || null, product.is_active ?? true]
      );
      const newProd = pRes.rows[0];

      if (product.variants && product.variants.length > 0) {
        for (const v of product.variants) {
          const sizeRes = await client.query('SELECT id FROM sizes WHERE code = $1', [v.size]);
          if (sizeRes.rows.length === 0) throw new Error(`Talla no válida: ${v.size}`);
          const colorRes = await client.query(
            `INSERT INTO colors (name) VALUES ($1)
             ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id`,
            [v.color]
          );
          await client.query(
            `INSERT INTO product_variants (product_id, size_id, color_id, sku, stock, alert_threshold)
             VALUES ($1, $2, $3, $4, $5, $6)`,
            [newProd.id, sizeRes.rows[0].id, colorRes.rows[0].id, v.sku, v.stock, v.alert_threshold ?? 3]
          );
        }
      }

      await client.query('COMMIT');
      return this.findById(newProd.id) as Promise<Product>;
    } catch (e) {
      await client.query('ROLLBACK');
      throw e;
    } finally {
      client.release();
    }
  }

  async update(id: number, product: Partial<Product>): Promise<Product | null> {
    const fields: string[] = [];
    const values: any[] = [];

    if (product.category_id !== undefined) {
      values.push(product.category_id);
      fields.push(`category_id = $${values.length}`);
    }
    if (product.name !== undefined) {
      values.push(product.name);
      fields.push(`name = $${values.length}`);
    }
    if (product.description !== undefined) {
      values.push(product.description);
      fields.push(`description = $${values.length}`);
    }
    if (product.base_price !== undefined) {
      values.push(product.base_price);
      fields.push(`base_price = $${values.length}`);
    }
    if (product.image_url !== undefined) {
      values.push(product.image_url);
      fields.push(`image_url = $${values.length}`);
    }
    if (product.is_active !== undefined) {
      values.push(product.is_active);
      fields.push(`is_active = $${values.length}`);
    }

    if (fields.length === 0) return this.findById(id);

    values.push(id);
    const query = `UPDATE products SET ${fields.join(', ')}, updated_at = CURRENT_TIMESTAMP WHERE id = $${values.length} RETURNING *`;
    await this.pool.query(query, values);
    return this.findById(id);
  }

  async updateVariantStock(variantId: number, quantityDelta: number): Promise<ProductVariant | null> {
    const res = await this.pool.query(
      `UPDATE product_variants 
       SET stock = stock + $1, updated_at = CURRENT_TIMESTAMP 
       WHERE id = $2 AND (stock + $1) >= 0 
        RETURNING id`,
      [quantityDelta, variantId]
    );
    if (res.rows.length === 0) {
      throw new Error(`Stock insuficiente o variante no encontrada (ID: ${variantId})`);
    }
    const vRes = await this.pool.query(`SELECT ${VARIANT_COLUMNS} ${VARIANT_FROM} WHERE pv.id = $1`, [variantId]);
    return vRes.rows[0];
  }

  async delete(id: number): Promise<boolean> {
    const res = await this.pool.query(
      'UPDATE products SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP WHERE id = $1',
      [id]
    );
    return (res.rowCount ?? 0) > 0;
  }

  async getLowStockVariants(): Promise<Array<ProductVariant & { productName: string }>> {
    const res = await this.pool.query(`
      SELECT ${VARIANT_COLUMNS}, p.name AS "productName"
      ${VARIANT_FROM}
      JOIN products p ON pv.product_id = p.id
      WHERE pv.stock <= pv.alert_threshold AND p.is_active = TRUE
      ORDER BY pv.stock ASC
    `);
    return res.rows;
  }
}

export class PgClientRepository implements IClientRepository {
  private pool: Pool = dbPool;

  async listAll(search?: string): Promise<Client[]> {
    if (search) {
      const res = await this.pool.query(
        `SELECT ${CLIENT_COLUMNS} ${CLIENT_FROM}
         WHERE LOWER(c.full_name) LIKE LOWER($1) OR c.phone LIKE $1 OR LOWER(d.name) LIKE LOWER($1)
         ORDER BY c.id DESC`,
        [`%${search}%`]
      );
      return res.rows;
    }
    const res = await this.pool.query(`SELECT ${CLIENT_COLUMNS} ${CLIENT_FROM} ORDER BY c.id DESC`);
    return res.rows;
  }

  async findById(id: number): Promise<Client | null> {
    const res = await this.pool.query(`SELECT ${CLIENT_COLUMNS} ${CLIENT_FROM} WHERE c.id = $1`, [id]);
    return res.rows[0] || null;
  }

  async findByPhone(phone: string): Promise<Client | null> {
    const res = await this.pool.query(`SELECT ${CLIENT_COLUMNS} ${CLIENT_FROM} WHERE c.phone = $1`, [phone]);
    return res.rows[0] || null;
  }

  async create(client: Omit<Client, 'id' | 'created_at' | 'updated_at'>): Promise<Client> {
    const districtId = await upsertDistrict(this.pool, client.district);
    const res = await this.pool.query(
      `INSERT INTO clients (full_name, phone, address, district_id, reference)
       VALUES ($1, $2, $3, $4, $5) RETURNING id`,
      [client.full_name, client.phone, client.address, districtId, client.reference || null]
    );
    return (await this.findById(res.rows[0].id)) as Client;
  }

  async update(id: number, client: Partial<Client>): Promise<Client | null> {
    const districtId = client.district ? await upsertDistrict(this.pool, client.district) : null;
    const res = await this.pool.query(
      `UPDATE clients
       SET full_name = COALESCE($1, full_name),
           phone = COALESCE($2, phone),
           address = COALESCE($3, address),
           district_id = COALESCE($4, district_id),
           reference = COALESCE($5, reference),
           updated_at = CURRENT_TIMESTAMP
       WHERE id = $6 RETURNING id`,
      [client.full_name, client.phone, client.address, districtId, client.reference, id]
    );
    if (res.rows.length === 0) return null;
    return this.findById(id);
  }
}

export class PgOrderRepository implements IOrderRepository {
  private pool: Pool = dbPool;

  async listAll(filters?: { status?: OrderStatus; dateFrom?: string; dateTo?: string; search?: string; page?: number; limit?: number }): Promise<{ data: Order[], total: number }> {
    let whereQuery = `
      FROM orders o
      JOIN clients c ON o.client_id = c.id
      JOIN districts d ON c.district_id = d.id
      JOIN payment_methods pm ON o.payment_method_id = pm.id
      LEFT JOIN users u ON o.user_id = u.id
      JOIN payment_methods pm ON o.payment_method_id = pm.id
      WHERE 1=1
    `;
    const params: any[] = [];

    if (filters?.status) {
      params.push(filters.status);
      whereQuery += ` AND o.status = $${params.length}`;
    }
    if (filters?.search) {
      params.push(`%${filters.search}%`);
      whereQuery += ` AND (LOWER(o.order_number) LIKE LOWER($${params.length}) OR LOWER(c.full_name) LIKE LOWER($${params.length}) OR c.phone LIKE $${params.length})`;
    }

    const countQuery = `SELECT COUNT(*)::int AS total ${whereQuery}`;
    const countRes = await this.pool.query(countQuery, params);
    const total = parseInt(countRes.rows[0].total, 10);

    let dataQuery = `
      SELECT o.*, c.full_name as client_name, c.phone as client_phone, c.address as client_address, c.district as client_district,
             u.name as user_name, pm.code as payment_method
      ${whereQuery}
      ORDER BY o.id DESC
    `;

    const page = filters?.page || 1;
    const limit = filters?.limit || 50; // unificado con Zod a 50
    const offset = (page - 1) * limit;

    const dataParams = [...params];
    dataParams.push(limit, offset);
    dataQuery += ` LIMIT $${dataParams.length - 1} OFFSET $${dataParams.length}`;

    const res = await this.pool.query(dataQuery, dataParams);

    const orders: Order[] = res.rows.map(row => ({
      id: row.id,
      order_number: row.order_number,
      client_id: row.client_id,
      client: {
        id: row.client_id,
        full_name: row.client_name,
        phone: row.client_phone,
        address: row.client_address,
        district: row.client_district,
        reference: row.client_reference
      },
      user_id: row.user_id,
      user_name: row.user_name,
      status: row.status,
      subtotal: parseFloat(row.subtotal),
      shipping_cost: parseFloat(row.shipping_cost),
      total_amount: parseFloat(row.total_amount),
      payment_method: row.payment_method,
      shippingType: row.shipping_type || undefined,
      destinationCity: row.destination_city || undefined,
      shippingAgency: row.shipping_agency || undefined,
      trackingNumber: row.tracking_number || undefined,
      notes: row.notes,
      items: itemsByOrder.get(row.id) || [],
      created_at: row.created_at,
      updated_at: row.updated_at
    }));

    return { data: orders, total };
  }

  async findById(id: number): Promise<Order | null> {
    const res = await this.pool.query(
      `SELECT o.*, c.full_name as client_name, c.phone as client_phone, c.address as client_address, c.district as client_district, c.reference as client_reference,
              u.name as user_name, pm.code as payment_method
       FROM orders o
       JOIN clients c ON o.client_id = c.id
       JOIN districts d ON c.district_id = d.id
       JOIN payment_methods pm ON o.payment_method_id = pm.id
       LEFT JOIN users u ON o.user_id = u.id
       JOIN payment_methods pm ON o.payment_method_id = pm.id
       WHERE o.id = $1`,
      [id]
    );
    if (res.rows.length === 0) return null;
    const row = res.rows[0];

    const itemsRes = await this.pool.query(`${ORDER_ITEM_SELECT} WHERE oi.order_id = $1 ORDER BY oi.id ASC`, [id]);

    const histRes = await this.pool.query(
      `SELECT osh.*, u.name as user_name
       FROM order_status_history osh
       LEFT JOIN users u ON osh.user_id = u.id
       WHERE osh.order_id = $1
       ORDER BY osh.id ASC`,
      [id]
    );

    return {
      id: row.id,
      order_number: row.order_number,
      client_id: row.client_id,
      client: {
        id: row.client_id,
        full_name: row.client_name,
        phone: row.client_phone,
        address: row.client_address,
        district: row.client_district,
        reference: row.client_reference
      },
      user_id: row.user_id,
      user_name: row.user_name,
      status: row.status,
      subtotal: parseFloat(row.subtotal),
      shipping_cost: parseFloat(row.shipping_cost),
      total_amount: parseFloat(row.total_amount),
      payment_method: row.payment_method,
      shippingType: row.shipping_type || undefined,
      destinationCity: row.destination_city || undefined,
      shippingAgency: row.shipping_agency || undefined,
      trackingNumber: row.tracking_number || undefined,
      notes: row.notes,
      items: itemsRes.rows.map(mapOrderItem),
      history: histRes.rows,
      created_at: row.created_at,
      updated_at: row.updated_at
    };
  }  

  async findByOrderNumber(orderNumber: string): Promise<Order | null> {
    const res = await this.pool.query('SELECT id FROM orders WHERE LOWER(order_number) = LOWER($1)', [orderNumber]);
    if (res.rows.length === 0) return null;
    return this.findById(res.rows[0].id);
  }

  async create(dto: CreateOrderDTO, isolationLevel: IsolationLevel = 'READ COMMITTED'): Promise<Order> {
    const MAX_RETRIES = 10;
    const BASE_BACKOFF_MS = 2;
    const MAX_BACKOFF_MS = 100;

    const isolationSql: Record<IsolationLevel, string> = {
      'READ COMMITTED': 'READ COMMITTED',
      'REPEATABLE READ': 'REPEATABLE READ',
      'SERIALIZABLE': 'SERIALIZABLE',
    };

    for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
      const client = await this.pool.connect();
      try {
        await client.query(`BEGIN ISOLATION LEVEL ${isolationSql[isolationLevel]}`);

        // 1. Resolve client
        let clientId = dto.clientId;
        if (!clientId && dto.clientData) {
          const checkClient = await client.query('SELECT id FROM clients WHERE phone = $1', [dto.clientData.phone]);
          if (checkClient.rows.length > 0) {
            clientId = checkClient.rows[0].id;
          } else {
            const newClientRes = await client.query(
              `INSERT INTO clients (full_name, phone, address, district, reference)
               VALUES ($1, $2, $3, $4, $5) RETURNING id`,
              [dto.clientData.fullName, dto.clientData.phone, dto.clientData.address, dto.clientData.district, dto.clientData.reference || null]
            );
            clientId = newClientRes.rows[0].id;
          }
        }

        if (!clientId) throw new Error('Cliente inválido');

        // 2. Validate and deduct stock
        let subtotal = 0;
        for (const item of dto.items) {
          const selectQuery = isolationLevel === 'SERIALIZABLE'
            ? 'SELECT stock, sku FROM product_variants WHERE id = $1'
            : 'SELECT stock, sku FROM product_variants WHERE id = $1 FOR UPDATE';

          const vRes = await client.query(selectQuery, [item.variantId]);
          if (vRes.rows.length === 0) throw new Error(`Variante ID ${item.variantId} no encontrada`);
          const stock = vRes.rows[0].stock;
          if (stock < item.quantity) {
            throw new Error(`Stock insuficiente para SKU ${vRes.rows[0].sku}. Disponible: ${stock}, pedido: ${item.quantity}`);
          }

          await client.query('UPDATE product_variants SET stock = stock - $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2', [item.quantity, item.variantId]);
          subtotal += item.unitPrice * item.quantity;
        }

        // 3. Create Order
        const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
        const seqRes = await client.query("SELECT nextval('order_number_seq') AS seq");
        const seq = parseInt(seqRes.rows[0].seq, 10).toString().padStart(6, '0');
        const orderNumber = `LEO-${dateStr}-${seq}`;
        const totalAmount = subtotal + dto.shippingCost;

        const pmRes = await client.query('SELECT id FROM payment_methods WHERE code = $1', [dto.paymentMethod]);
        if (pmRes.rows.length === 0) {
          throw new Error(`Método de pago no soportado por el esquema de DB: ${dto.paymentMethod}`);
        }
        const paymentMethodId = pmRes.rows[0].id;

        const orderRes = await client.query(
          `INSERT INTO orders (
             order_number, client_id, user_id, status, subtotal, shipping_cost, total_amount, 
             payment_method_id, notes, shipping_type, destination_city, shipping_agency, tracking_number
           )
           VALUES ($1, $2, $3, 'RECIBIDO', $4, $5, $6, $7, $8, $9, $10, $11, $12) RETURNING id`,
          [
            orderNumber, clientId, dto.userId || null, 
            subtotal, dto.shippingCost, totalAmount, 
            paymentMethodId, dto.notes || null,
            dto.shippingType || null, dto.destinationCity || null, dto.shippingAgency || null, dto.trackingNumber || null
          ]
        );
        const orderId = orderRes.rows[0].id;

        // 4. Insert Order Items
        for (const item of dto.items) {
          await client.query(
            `INSERT INTO order_items (order_id, variant_id, quantity, unit_price, subtotal)
             VALUES ($1, $2, $3, $4, $5)`,
            [orderId, item.variantId, item.quantity, item.unitPrice, item.unitPrice * item.quantity]
          );
        }

        // 5. Insert History
        await client.query(
          `INSERT INTO order_status_history (order_id, user_id, previous_status, new_status, comments)
           VALUES ($1, $2, NULL, 'RECIBIDO', 'Pedido creado exitosamente')`,
          [orderId, dto.userId || null]
        );

        await client.query('COMMIT');
        
        // No liberar el client aqui todavia para evitar fugas si findById falla
        // El cliente se liberara en el finally block global de la iteracion.
        return await this.findById(orderId) as Order;
      } catch (e: any) {
        try { await client.query('ROLLBACK'); } catch { /* no-op si no hay tx activa */ }
        
        const isSerializationError = e.code === '40001';
        const isDeadlockError = e.code === '40P01';

        if ((isSerializationError || isDeadlockError) && attempt < MAX_RETRIES) {
          // Exponential backoff con 20% jitter
          const backoff = Math.min(MAX_BACKOFF_MS, BASE_BACKOFF_MS * Math.pow(2, attempt - 1));
          const jitter = backoff * 0.2;
          const waitTime = backoff - jitter + Math.random() * (jitter * 2);
          await new Promise(resolve => setTimeout(resolve, waitTime));
          continue; // Retry
        }

        throw e;
      } finally {
        client.release(); // Safe release UNA SOLA VEZ garantizado por iteración
      }
    }
    
    throw new Error('Max retries reached without successful transaction.');
  }

  async updateStatus(orderId: number, newStatus: OrderStatus, userId?: number, comments?: string): Promise<Order | null> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      const oRes = await client.query('SELECT status FROM orders WHERE id = $1 FOR UPDATE', [orderId]);
      if (oRes.rows.length === 0) {
        await client.query('ROLLBACK');
        return null;
      }
      const prevStatus = oRes.rows[0].status;

      await client.query('UPDATE orders SET status = $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2', [newStatus, orderId]);
      await client.query(
        `INSERT INTO order_status_history (order_id, user_id, previous_status, new_status, comments)
         VALUES ($1, $2, $3, $4, $5)`,
        [orderId, userId || null, prevStatus, newStatus, comments || `Cambio de estado a ${newStatus}`]
      );

      await client.query('COMMIT');
      return this.findById(orderId);
    } catch (e) {
      await client.query('ROLLBACK');
      throw e;
    } finally {
      client.release();
    }
  }

  async cancelOrder(orderId: number, userId?: number, reason?: string): Promise<Order | null> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      const oRes = await client.query('SELECT status FROM orders WHERE id = $1 FOR UPDATE', [orderId]);
      if (oRes.rows.length === 0) {
        await client.query('ROLLBACK');
        return null;
      }
      const prev = oRes.rows[0].status;
      if (prev === 'CANCELADO') {
        await client.query('ROLLBACK');
        return this.findById(orderId);
      }

      // Restore Stock
      const itemsRes = await client.query('SELECT variant_id, quantity FROM order_items WHERE order_id = $1', [orderId]);
      for (const item of itemsRes.rows) {
        await client.query('UPDATE product_variants SET stock = stock + $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2', [item.quantity, item.variant_id]);
      }

      await client.query("UPDATE orders SET status = 'CANCELADO', updated_at = CURRENT_TIMESTAMP WHERE id = $1", [orderId]);
      await client.query(
        `INSERT INTO order_status_history (order_id, user_id, previous_status, new_status, comments)
         VALUES ($1, $2, $3, 'CANCELADO', $4)`,
        [orderId, userId || null, prev, reason || 'Pedido cancelado y stock retornado']
      );

      await client.query('COMMIT');
      return this.findById(orderId);
    } catch (e) {
      await client.query('ROLLBACK');
      throw e;
    } finally {
      client.release();
    }
  }

  async getMetrics(): Promise<DashboardMetrics> {
    const countRes = await this.pool.query(`
      SELECT 
        COUNT(*) as total_orders,
        COUNT(*) FILTER (WHERE status = 'RECIBIDO') as received_count,
        COUNT(*) FILTER (WHERE status = 'PREPARACION') as prep_count,
        COUNT(*) FILTER (WHERE status = 'EN_CAMINO') as shipping_count,
        COUNT(*) FILTER (WHERE status = 'ENTREGADO') as delivered_count,
        COUNT(*) FILTER (WHERE status = 'CANCELADO') as cancelled_count,
        COALESCE(SUM(total_amount) FILTER (WHERE status != 'CANCELADO'), 0) as total_revenue
      FROM orders
    `);

    const lowStockRes = await this.pool.query(`
      SELECT COUNT(*) as low_stock_count 
      FROM product_variants pv
      JOIN products p ON pv.product_id = p.id
      WHERE pv.stock <= pv.alert_threshold AND p.is_active = TRUE
    `);

    const listRes = await this.listAll({});
    const recentOrders = listRes.data;

    const topProdRes = await this.pool.query(`
      SELECT p.id as "productId", p.name, SUM(oi.quantity)::int as "totalQuantity", SUM(oi.subtotal)::float as "totalRevenue"
      FROM order_items oi
      JOIN product_variants pv ON oi.variant_id = pv.id
      JOIN products p ON pv.product_id = p.id
      JOIN orders o ON oi.order_id = o.id
      WHERE o.status != 'CANCELADO'
      GROUP BY p.id, p.name
      ORDER BY "totalQuantity" DESC
      LIMIT 5
    `);

    const row = countRes.rows[0];
    return {
      totalOrders: parseInt(row.total_orders, 10),
      ordersByStatus: {
        RECIBIDO: parseInt(row.received_count, 10),
        PREPARACION: parseInt(row.prep_count, 10),
        EN_CAMINO: parseInt(row.shipping_count, 10),
        ENTREGADO: parseInt(row.delivered_count, 10),
        CANCELADO: parseInt(row.cancelled_count, 10)
      },
      totalRevenue: parseFloat(row.total_revenue),
      lowStockCount: parseInt(lowStockRes.rows[0].low_stock_count, 10),
      recentOrders: recentOrders.slice(0, 5),
      topSellingProducts: topProdRes.rows
    };
  }

  async getRecentActivity(limit: number = 20): Promise<ActivityRecord[]> {
    const res = await this.pool.query(`
      SELECT 
        osh.id,
        osh.order_id,
        osh.user_id,
        osh.previous_status,
        osh.new_status,
        osh.changed_at,
        osh.comments,
        o.order_number,
        c.full_name as client_name,
        u.name as user_name
      FROM order_status_history osh
      JOIN orders o ON osh.order_id = o.id
      JOIN clients c ON o.client_id = c.id
      LEFT JOIN users u ON osh.user_id = u.id
      ORDER BY osh.changed_at DESC
      LIMIT $1
    `, [limit]);

    return res.rows;
  }
}

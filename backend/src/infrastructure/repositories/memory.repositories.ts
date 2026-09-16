// =============================================================================
// IN-MEMORY TRANSACTIONAL REPOSITORIES (FALLBACK / TEST SUITE ADAPTER)
// IMPLEMENTS FULL REPOSITORY PATTERN FOR LEOFIT SOLUTIONS
// =============================================================================

import {
  User,
  Category,
  Product,
  ProductVariant,
  Client,
  Order,
  OrderItem,
  OrderStatus,
  OrderStatusHistory,
  DashboardMetrics
} from '../../domain/entities/models';
import {
  IUserRepository,
  ICategoryRepository,
  IProductRepository,
  IClientRepository,
  IOrderRepository,
  CreateOrderDTO
} from '../../domain/repositories/interfaces';
import { PasswordHasher } from '../security/password.utils';

// In-memory data store with predefined initial seeds
export class InMemoryDataStore {
  public static users: User[] = [
    {
      id: 1,
      name: 'Lady Luz Loayza (Scrum Master)',
      email: 'admin@leofit.pe',
      password_hash: '$2a$10$wNqHj6Wn7Bfg3VwKqm5cbeUfg5Y0l5B2yPzT93kG3K04D6BqG7kca', // admin123
      role: 'ADMIN',
      created_at: new Date('2026-03-01T10:00:00Z')
    },
    {
      id: 2,
      name: 'Operador Logístico Gamarra',
      email: 'operador@leofit.pe',
      password_hash: '$2a$10$wNqHj6Wn7Bfg3VwKqm5cbeUfg5Y0l5B2yPzT93kG3K04D6BqG7kca', // admin123
      role: 'OPERATOR',
      created_at: new Date('2026-03-01T10:00:00Z')
    }
  ];

  public static categories: Category[] = [
    { id: 1, name: 'Polos Oversize Dry-Fit', description: 'Polos deportivos de corte holgado transpirables' },
    { id: 2, name: 'Shorts de Alto Rendimiento', description: 'Shorts con lycra interior de compresión y bolsillo' },
    { id: 3, name: 'Joggers Térmicos', description: 'Pantalones de entrenamiento con ajuste ergonómico' },
    { id: 4, name: 'Tops de Compresión', description: 'Prendas superiores ajustadas para soporte muscular' }
  ];

  public static products: Product[] = [
    {
      id: 1,
      category_id: 1,
      category_name: 'Polos Oversize Dry-Fit',
      name: 'Polo Oversize Gym Beast - Negro',
      description: 'Polo de algodón peinado 24/1 con tecnología Dry-Fit para máxima absorción de sudor.',
      base_price: 49.90,
      image_url: 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60',
      is_active: true,
      created_at: new Date('2026-03-01T10:00:00Z')
    },
    {
      id: 2,
      category_id: 1,
      category_name: 'Polos Oversize Dry-Fit',
      name: 'Polo Oversize Iron Core - Crema',
      description: 'Polo oversize premium color crema con estampado en serigrafía de alta densidad.',
      base_price: 54.90,
      image_url: 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60',
      is_active: true,
      created_at: new Date('2026-03-01T10:00:00Z')
    },
    {
      id: 3,
      category_id: 2,
      category_name: 'Shorts de Alto Rendimiento',
      name: 'Short 2 en 1 Pro Performance - Negro',
      description: 'Short con lycra interior de compresión anti-roces y bolsillo para smartphone.',
      base_price: 59.90,
      image_url: 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500&auto=format&fit=crop&q=60',
      is_active: true,
      created_at: new Date('2026-03-01T10:00:00Z')
    },
    {
      id: 4,
      category_id: 3,
      category_name: 'Joggers Térmicos',
      name: 'Jogger Cargo Fit - Gris Plomo',
      description: 'Pantalón deportivo entallado con 4 bolsillos con cremallera y tejido elastano.',
      base_price: 79.90,
      image_url: 'https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=500&auto=format&fit=crop&q=60',
      is_active: true,
      created_at: new Date('2026-03-01T10:00:00Z')
    }
  ];

  public static variants: ProductVariant[] = [
    { id: 1, product_id: 1, size: 'S', color: 'Negro', sku: 'POL-GYM-NEG-S', stock: 15, alert_threshold: 3 },
    { id: 2, product_id: 1, size: 'M', color: 'Negro', sku: 'POL-GYM-NEG-M', stock: 20, alert_threshold: 4 },
    { id: 3, product_id: 1, size: 'L', color: 'Negro', sku: 'POL-GYM-NEG-L', stock: 8, alert_threshold: 3 },
    { id: 4, product_id: 1, size: 'XL', color: 'Negro', sku: 'POL-GYM-NEG-XL', stock: 2, alert_threshold: 3 }, // low stock
    { id: 5, product_id: 2, size: 'S', color: 'Crema', sku: 'POL-IRO-CRE-S', stock: 12, alert_threshold: 3 },
    { id: 6, product_id: 2, size: 'M', color: 'Crema', sku: 'POL-IRO-CRE-M', stock: 18, alert_threshold: 4 },
    { id: 7, product_id: 2, size: 'L', color: 'Crema', sku: 'POL-IRO-CRE-L', stock: 10, alert_threshold: 3 },
    { id: 8, product_id: 3, size: 'M', color: 'Negro', sku: 'SHO-2N1-NEG-M', stock: 14, alert_threshold: 3 },
    { id: 9, product_id: 3, size: 'L', color: 'Negro', sku: 'SHO-2N1-NEG-L', stock: 11, alert_threshold: 3 },
    { id: 10, product_id: 4, size: 'M', color: 'Gris Plomo', sku: 'JOG-CAR-GRI-M', stock: 9, alert_threshold: 3 },
    { id: 11, product_id: 4, size: 'L', color: 'Gris Plomo', sku: 'JOG-CAR-GRI-L', stock: 1, alert_threshold: 3 } // low stock
  ];

  public static clients: Client[] = [
    {
      id: 1,
      full_name: 'Carlos Mendoza Ramos',
      phone: '987654321',
      address: 'Av. Las Palmeras 450, Dpto 302',
      district: 'San Isidro',
      reference: 'Frente al Parque Renán Elías',
      created_at: new Date('2026-03-02T11:00:00Z')
    },
    {
      id: 2,
      full_name: 'Andrea Morales Silva',
      phone: '912345678',
      address: 'Jr. Huascarán 124',
      district: 'Miraflores',
      reference: 'A media cuadra de Larco',
      created_at: new Date('2026-03-03T14:30:00Z')
    },
    {
      id: 3,
      full_name: 'Diego Valdivia Torres',
      phone: '998877665',
      address: 'Calle Los Sauces 789',
      district: 'Surco',
      reference: 'Cerca a Chacarilla',
      created_at: new Date('2026-03-04T09:15:00Z')
    }
  ];

  public static orders: Order[] = [
    {
      id: 1,
      order_number: 'LEO-20260302-001',
      client_id: 1,
      user_id: 1,
      user_name: 'Lady Luz Loayza (Scrum Master)',
      status: 'ENTREGADO',
      subtotal: 109.80,
      shipping_cost: 10.00,
      total_amount: 119.80,
      payment_method: 'YAPE',
      notes: 'Dejar en recepción si no responde',
      created_at: new Date('2026-03-02T11:30:00Z'),
      updated_at: new Date('2026-03-02T16:00:00Z'),
      items: [
        { id: 1, order_id: 1, variant_id: 2, product_name: 'Polo Oversize Gym Beast - Negro', size: 'M', color: 'Negro', sku: 'POL-GYM-NEG-M', quantity: 1, unit_price: 49.90, subtotal: 49.90 },
        { id: 2, order_id: 1, variant_id: 8, product_name: 'Short 2 en 1 Pro Performance - Negro', size: 'M', color: 'Negro', sku: 'SHO-2N1-NEG-M', quantity: 1, unit_price: 59.90, subtotal: 59.90 }
      ]
    },
    {
      id: 2,
      order_number: 'LEO-20260303-002',
      client_id: 2,
      user_id: 2,
      user_name: 'Operador Logístico Gamarra',
      status: 'EN_CAMINO',
      subtotal: 54.90,
      shipping_cost: 12.00,
      total_amount: 66.90,
      payment_method: 'PLIN',
      notes: 'Llamar antes de llegar',
      created_at: new Date('2026-03-03T15:00:00Z'),
      updated_at: new Date('2026-03-03T16:30:00Z'),
      items: [
        { id: 3, order_id: 2, variant_id: 6, product_name: 'Polo Oversize Iron Core - Crema', size: 'M', color: 'Crema', sku: 'POL-IRO-CRE-M', quantity: 1, unit_price: 54.90, subtotal: 54.90 }
      ]
    },
    {
      id: 3,
      order_number: 'LEO-20260304-003',
      client_id: 3,
      user_id: 1,
      user_name: 'Lady Luz Loayza (Scrum Master)',
      status: 'PREPARACION',
      subtotal: 79.90,
      shipping_cost: 10.00,
      total_amount: 89.90,
      payment_method: 'TRANSFERENCIA',
      notes: 'Empacar en bolsa ecológica de regalo',
      created_at: new Date('2026-03-04T09:45:00Z'),
      updated_at: new Date('2026-03-04T10:00:00Z'),
      items: [
        { id: 4, order_id: 3, variant_id: 10, product_name: 'Jogger Cargo Fit - Gris Plomo', size: 'M', color: 'Gris Plomo', sku: 'JOG-CAR-GRI-M', quantity: 1, unit_price: 79.90, subtotal: 79.90 }
      ]
    }
  ];

  public static orderStatusHistory: OrderStatusHistory[] = [
    { id: 1, order_id: 1, user_id: 1, previous_status: null, new_status: 'RECIBIDO', changed_at: new Date('2026-03-02T11:30:00Z'), comments: 'Pedido creado exitosamente' },
    { id: 2, order_id: 1, user_id: 1, previous_status: 'RECIBIDO', new_status: 'PREPARACION', changed_at: new Date('2026-03-02T12:15:00Z'), comments: 'Prendas empacadas en taller' },
    { id: 3, order_id: 1, user_id: 1, previous_status: 'PREPARACION', new_status: 'EN_CAMINO', changed_at: new Date('2026-03-02T14:00:00Z'), comments: 'Asignado a motorizado courier' },
    { id: 4, order_id: 1, user_id: 1, previous_status: 'EN_CAMINO', new_status: 'ENTREGADO', changed_at: new Date('2026-03-02T16:00:00Z'), comments: 'Firma y pago verificado' },
    { id: 5, order_id: 2, user_id: 2, previous_status: null, new_status: 'RECIBIDO', changed_at: new Date('2026-03-03T15:00:00Z'), comments: 'Confirmado por WhatsApp' },
    { id: 6, order_id: 2, user_id: 2, previous_status: 'RECIBIDO', new_status: 'EN_CAMINO', changed_at: new Date('2026-03-03T16:30:00Z'), comments: 'Despacho express Miraflores' },
    { id: 7, order_id: 3, user_id: 1, previous_status: null, new_status: 'RECIBIDO', changed_at: new Date('2026-03-04T09:45:00Z'), comments: 'Comprobante validado' },
    { id: 8, order_id: 3, user_id: 1, previous_status: 'RECIBIDO', new_status: 'PREPARACION', changed_at: new Date('2026-03-04T10:00:00Z'), comments: 'En proceso de confección final' }
  ];
}

// Memory UserRepository
export class MemoryUserRepository implements IUserRepository {
  async findByEmail(email: string): Promise<User | null> {
    const user = InMemoryDataStore.users.find(u => u.email.toLowerCase() === email.toLowerCase());
    return user ? { ...user } : null;
  }

  async findById(id: number): Promise<User | null> {
    const user = InMemoryDataStore.users.find(u => u.id === id);
    return user ? { ...user } : null;
  }

  async create(userData: Omit<User, 'id' | 'created_at' | 'updated_at'>): Promise<User> {
    const newUser: User = {
      id: InMemoryDataStore.users.length + 1,
      ...userData,
      created_at: new Date(),
      updated_at: new Date()
    };
    InMemoryDataStore.users.push(newUser);
    return { ...newUser };
  }

  async listAll(): Promise<User[]> {
    return InMemoryDataStore.users.map(u => ({ ...u, password_hash: '***' }));
  }
}

// Memory CategoryRepository
export class MemoryCategoryRepository implements ICategoryRepository {
  async listAll(): Promise<Category[]> {
    return [...InMemoryDataStore.categories];
  }

  async findById(id: number): Promise<Category | null> {
    const cat = InMemoryDataStore.categories.find(c => c.id === id);
    return cat ? { ...cat } : null;
  }

  async create(data: Omit<Category, 'id' | 'created_at'>): Promise<Category> {
    const newCat: Category = {
      id: InMemoryDataStore.categories.length + 1,
      ...data,
      created_at: new Date()
    };
    InMemoryDataStore.categories.push(newCat);
    return { ...newCat };
  }
}

// Memory ProductRepository
export class MemoryProductRepository implements IProductRepository {
  async listAll(filters?: { categoryId?: number; isActive?: boolean; search?: string }): Promise<Product[]> {
    let result = InMemoryDataStore.products.map(p => {
      const variants = InMemoryDataStore.variants.filter(v => v.product_id === p.id);
      return { ...p, variants };
    });

    if (filters?.categoryId) {
      result = result.filter(p => p.category_id === filters.categoryId);
    }
    if (filters?.isActive !== undefined) {
      result = result.filter(p => p.is_active === filters.isActive);
    }
    if (filters?.search) {
      const q = filters.search.toLowerCase();
      result = result.filter(p => p.name.toLowerCase().includes(q) || p.description?.toLowerCase().includes(q));
    }

    return result;
  }

  async findById(id: number): Promise<Product | null> {
    const p = InMemoryDataStore.products.find(item => item.id === id);
    if (!p) return null;
    const variants = InMemoryDataStore.variants.filter(v => v.product_id === p.id);
    return { ...p, variants };
  }

  async findBySku(sku: string): Promise<ProductVariant | null> {
    const v = InMemoryDataStore.variants.find(item => item.sku.toLowerCase() === sku.toLowerCase());
    return v ? { ...v } : null;
  }

  async create(data: Omit<Product, 'id' | 'created_at' | 'updated_at'>): Promise<Product> {
    const newProduct: Product = {
      id: InMemoryDataStore.products.length + 1,
      ...data,
      created_at: new Date(),
      updated_at: new Date()
    };
    InMemoryDataStore.products.push(newProduct);

    if (data.variants && data.variants.length > 0) {
      for (const v of data.variants) {
        const newVariant: ProductVariant = {
          id: InMemoryDataStore.variants.length + 1,
          product_id: newProduct.id,
          size: v.size,
          color: v.color,
          sku: v.sku,
          stock: v.stock,
          alert_threshold: v.alert_threshold || 3,
          created_at: new Date(),
          updated_at: new Date()
        };
        InMemoryDataStore.variants.push(newVariant);
      }
    }

    return this.findById(newProduct.id) as Promise<Product>;
  }

  async update(id: number, data: Partial<Product>): Promise<Product | null> {
    const idx = InMemoryDataStore.products.findIndex(p => p.id === id);
    if (idx === -1) return null;
    InMemoryDataStore.products[idx] = {
      ...InMemoryDataStore.products[idx],
      ...data,
      updated_at: new Date()
    };
    return this.findById(id);
  }

  async updateVariantStock(variantId: number, quantityDelta: number): Promise<ProductVariant | null> {
    const idx = InMemoryDataStore.variants.findIndex(v => v.id === variantId);
    if (idx === -1) return null;
    const target = InMemoryDataStore.variants[idx];
    const newStock = target.stock + quantityDelta;
    if (newStock < 0) {
      throw new Error(`Stock insuficiente para la variante SKU ${target.sku}. Disponible: ${target.stock}, Solicitado delta: ${quantityDelta}`);
    }
    InMemoryDataStore.variants[idx].stock = newStock;
    InMemoryDataStore.variants[idx].updated_at = new Date();
    return { ...InMemoryDataStore.variants[idx] };
  }

  async delete(id: number): Promise<boolean> {
    const idx = InMemoryDataStore.products.findIndex(p => p.id === id);
    if (idx === -1) return false;
    InMemoryDataStore.products[idx].is_active = false;
    return true;
  }

  async getLowStockVariants(): Promise<Array<ProductVariant & { productName: string }>> {
    const lowStock = InMemoryDataStore.variants.filter(v => v.stock <= v.alert_threshold);
    return lowStock.map(v => {
      const prod = InMemoryDataStore.products.find(p => p.id === v.product_id);
      return {
        ...v,
        productName: prod ? prod.name : 'Desconocido'
      };
    });
  }
}

// Memory ClientRepository
export class MemoryClientRepository implements IClientRepository {
  async listAll(search?: string): Promise<Client[]> {
    if (!search) return [...InMemoryDataStore.clients];
    const q = search.toLowerCase();
    return InMemoryDataStore.clients.filter(
      c => c.full_name.toLowerCase().includes(q) || c.phone.includes(q) || c.district.toLowerCase().includes(q)
    );
  }

  async findById(id: number): Promise<Client | null> {
    const c = InMemoryDataStore.clients.find(item => item.id === id);
    return c ? { ...c } : null;
  }

  async findByPhone(phone: string): Promise<Client | null> {
    const c = InMemoryDataStore.clients.find(item => item.phone === phone);
    return c ? { ...c } : null;
  }

  async create(data: Omit<Client, 'id' | 'created_at' | 'updated_at'>): Promise<Client> {
    const newClient: Client = {
      id: InMemoryDataStore.clients.length + 1,
      ...data,
      created_at: new Date(),
      updated_at: new Date()
    };
    InMemoryDataStore.clients.push(newClient);
    return { ...newClient };
  }

  async update(id: number, data: Partial<Client>): Promise<Client | null> {
    const idx = InMemoryDataStore.clients.findIndex(c => c.id === id);
    if (idx === -1) return null;
    InMemoryDataStore.clients[idx] = {
      ...InMemoryDataStore.clients[idx],
      ...data,
      updated_at: new Date()
    };
    return { ...InMemoryDataStore.clients[idx] };
  }
}

// Memory OrderRepository with ACID Transactional guarantees
export class MemoryOrderRepository implements IOrderRepository {
  private clientRepo = new MemoryClientRepository();
  private productRepo = new MemoryProductRepository();

  async listAll(filters?: { status?: OrderStatus; dateFrom?: string; dateTo?: string; search?: string }): Promise<Order[]> {
    let list = InMemoryDataStore.orders.map(o => {
      const client = InMemoryDataStore.clients.find(c => c.id === o.client_id);
      return { ...o, client };
    });

    if (filters?.status) {
      list = list.filter(o => o.status === filters.status);
    }
    if (filters?.search) {
      const q = filters.search.toLowerCase();
      list = list.filter(o => 
        o.order_number.toLowerCase().includes(q) || 
        o.client?.full_name.toLowerCase().includes(q) ||
        o.client?.phone.includes(q)
      );
    }
    return list.sort((a, b) => new Date(b.created_at || '').getTime() - new Date(a.created_at || '').getTime());
  }

  async findById(id: number): Promise<Order | null> {
    const o = InMemoryDataStore.orders.find(item => item.id === id);
    if (!o) return null;
    const client = InMemoryDataStore.clients.find(c => c.id === o.client_id);
    const history = InMemoryDataStore.orderStatusHistory.filter(h => h.order_id === o.id);
    return { ...o, client, history };
  }

  async findByOrderNumber(orderNumber: string): Promise<Order | null> {
    const o = InMemoryDataStore.orders.find(item => item.order_number.toLowerCase() === orderNumber.toLowerCase());
    if (!o) return null;
    return this.findById(o.id);
  }

  async create(dto: CreateOrderDTO): Promise<Order> {
    // 1. Resolver o registrar cliente
    let client: Client | null = null;
    if (dto.clientId) {
      client = await this.clientRepo.findById(dto.clientId);
      if (!client) throw new Error(`Cliente ID ${dto.clientId} no encontrado.`);
    } else if (dto.clientData) {
      const existing = await this.clientRepo.findByPhone(dto.clientData.phone);
      if (existing) {
        client = existing;
      } else {
        client = await this.clientRepo.create({
          full_name: dto.clientData.fullName,
          phone: dto.clientData.phone,
          address: dto.clientData.address,
          district: dto.clientData.district,
          reference: dto.clientData.reference || null
        });
      }
    } else {
      throw new Error('Información del cliente requerida para crear el pedido.');
    }

    // 2. Validar stock atómicamente antes de registrar
    for (const item of dto.items) {
      const variant = InMemoryDataStore.variants.find(v => v.id === item.variantId);
      if (!variant) throw new Error(`Variante ID ${item.variantId} no existe.`);
      if (variant.stock < item.quantity) {
        throw new Error(`Stock insuficiente para SKU ${variant.sku}. En stock: ${variant.stock}, solicitado: ${item.quantity}`);
      }
    }

    // 3. Descontar stock (Transacción)
    const orderItems: OrderItem[] = [];
    let subtotal = 0;

    for (const item of dto.items) {
      await this.productRepo.updateVariantStock(item.variantId, -item.quantity);
      const variant = InMemoryDataStore.variants.find(v => v.id === item.variantId)!;
      const product = InMemoryDataStore.products.find(p => p.id === variant.product_id)!;
      const lineSubtotal = item.unitPrice * item.quantity;
      subtotal += lineSubtotal;

      orderItems.push({
        id: Math.floor(Math.random() * 100000),
        variant_id: variant.id,
        product_name: product.name,
        size: variant.size,
        color: variant.color,
        sku: variant.sku,
        quantity: item.quantity,
        unit_price: item.unitPrice,
        subtotal: lineSubtotal
      });
    }

    // 4. Crear Cabecera del Pedido
    const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const countSeq = (InMemoryDataStore.orders.length + 1).toString().padStart(3, '0');
    const orderNumber = `LEO-${dateStr}-${countSeq}`;
    const totalAmount = subtotal + dto.shippingCost;

    const newOrder: Order = {
      id: InMemoryDataStore.orders.length + 1,
      order_number: orderNumber,
      client_id: client.id,
      client,
      user_id: dto.userId || null,
      status: 'RECIBIDO',
      subtotal,
      shipping_cost: dto.shippingCost,
      total_amount: totalAmount,
      payment_method: dto.paymentMethod,
      notes: dto.notes || null,
      items: orderItems,
      created_at: new Date(),
      updated_at: new Date()
    };

    InMemoryDataStore.orders.push(newOrder);

    // 5. Registrar Historial Inicial
    InMemoryDataStore.orderStatusHistory.push({
      id: InMemoryDataStore.orderStatusHistory.length + 1,
      order_id: newOrder.id,
      user_id: dto.userId || null,
      previous_status: null,
      new_status: 'RECIBIDO',
      changed_at: new Date(),
      comments: 'Pedido creado exitosamente en el sistema'
    });

    return newOrder;
  }

  async updateStatus(orderId: number, newStatus: OrderStatus, userId?: number, comments?: string): Promise<Order | null> {
    const idx = InMemoryDataStore.orders.findIndex(o => o.id === orderId);
    if (idx === -1) return null;

    const prev = InMemoryDataStore.orders[idx].status;
    InMemoryDataStore.orders[idx].status = newStatus;
    InMemoryDataStore.orders[idx].updated_at = new Date();

    InMemoryDataStore.orderStatusHistory.push({
      id: InMemoryDataStore.orderStatusHistory.length + 1,
      order_id: orderId,
      user_id: userId || null,
      previous_status: prev,
      new_status: newStatus,
      changed_at: new Date(),
      comments: comments || `Transición de estado a ${newStatus}`
    });

    return this.findById(orderId);
  }

  async cancelOrder(orderId: number, userId?: number, reason?: string): Promise<Order | null> {
    const order = await this.findById(orderId);
    if (!order) return null;
    if (order.status === 'CANCELADO') return order;

    // Restaurar stock de los items
    if (order.items) {
      for (const item of order.items) {
        await this.productRepo.updateVariantStock(item.variant_id, item.quantity);
      }
    }

    return this.updateStatus(orderId, 'CANCELADO', userId, reason || 'Pedido cancelado y stock retornado');
  }

  async getMetrics(): Promise<DashboardMetrics> {
    const orders = InMemoryDataStore.orders;
    const totalRevenue = orders
      .filter(o => o.status !== 'CANCELADO')
      .reduce((sum, o) => sum + Number(o.total_amount), 0);

    const ordersByStatus: Record<OrderStatus, number> = {
      RECIBIDO: orders.filter(o => o.status === 'RECIBIDO').length,
      PREPARACION: orders.filter(o => o.status === 'PREPARACION').length,
      EN_CAMINO: orders.filter(o => o.status === 'EN_CAMINO').length,
      ENTREGADO: orders.filter(o => o.status === 'ENTREGADO').length,
      CANCELADO: orders.filter(o => o.status === 'CANCELADO').length
    };

    const lowStock = await this.productRepo.getLowStockVariants();

    // Top selling products calculation
    const salesByProd: Record<number, { name: string; quantity: number; revenue: number }> = {};
    for (const ord of orders) {
      if (ord.status === 'CANCELADO') continue;
      for (const item of ord.items || []) {
        const prodId = item.variant_id; // approximate grouping
        if (!salesByProd[prodId]) {
          salesByProd[prodId] = { name: item.product_name || 'Producto', quantity: 0, revenue: 0 };
        }
        salesByProd[prodId].quantity += item.quantity;
        salesByProd[prodId].revenue += item.subtotal;
      }
    }

    const topSellingProducts = Object.entries(salesByProd)
      .map(([id, data]) => ({
        productId: parseInt(id, 10),
        name: data.name,
        totalQuantity: data.quantity,
        totalRevenue: data.revenue
      }))
      .sort((a, b) => b.totalQuantity - a.totalQuantity)
      .slice(0, 5);

    return {
      totalOrders: orders.length,
      ordersByStatus,
      totalRevenue,
      lowStockCount: lowStock.length,
      recentOrders: orders.slice(-5).reverse(),
      topSellingProducts
    };
  }
}

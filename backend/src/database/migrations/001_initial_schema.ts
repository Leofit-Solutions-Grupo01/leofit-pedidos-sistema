import { PoolClient } from 'pg';
import { Migration } from './types';

export const migration001: Migration = {
  version: '20261016_001',
  name: 'initial_schema_setup',
  async up(client: PoolClient): Promise<void> {
    await client.query(`
      -- Tipos ENUM para dominios cerrados (BCNF)
      DO $$ BEGIN
        CREATE TYPE user_role_enum AS ENUM ('ADMIN', 'OPERATOR');
      EXCEPTION
        WHEN duplicate_object THEN NULL;
      END $$;

      DO $$ BEGIN
        CREATE TYPE order_status_enum AS ENUM ('RECIBIDO', 'PREPARACION', 'EN_CAMINO', 'ENTREGADO', 'CANCELADO');
      EXCEPTION
        WHEN duplicate_object THEN NULL;
      END $$;

      -- Tablas de dominio (BCNF)
      CREATE TABLE IF NOT EXISTS sizes (
        id    SMALLSERIAL PRIMARY KEY,
        code  VARCHAR(10)  NOT NULL UNIQUE,
        label VARCHAR(30)  NOT NULL
      );

      CREATE TABLE IF NOT EXISTS colors (
        id   SMALLSERIAL PRIMARY KEY,
        name VARCHAR(60) NOT NULL UNIQUE,
        hex  CHAR(7)
      );

      CREATE TABLE IF NOT EXISTS districts (
        id   SMALLSERIAL PRIMARY KEY,
        name VARCHAR(80) NOT NULL UNIQUE
      );

      CREATE TABLE IF NOT EXISTS payment_methods (
        id   SMALLSERIAL PRIMARY KEY,
        code VARCHAR(30) NOT NULL UNIQUE,
        name VARCHAR(60) NOT NULL
      );

      -- Entidades principales
      CREATE TABLE IF NOT EXISTS users (
        id            SERIAL          PRIMARY KEY,
        name          VARCHAR(100)    NOT NULL,
        email         VARCHAR(150)    NOT NULL UNIQUE,
        password_hash VARCHAR(255)    NOT NULL,
        role          user_role_enum  NOT NULL DEFAULT 'OPERATOR',
        is_active     BOOLEAN         NOT NULL DEFAULT TRUE,
        created_at    TIMESTAMPTZ     NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at    TIMESTAMPTZ     NOT NULL DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS categories (
        id          SERIAL       PRIMARY KEY,
        name        VARCHAR(60)  NOT NULL UNIQUE,
        description TEXT,
        created_at  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS products (
        id          SERIAL          PRIMARY KEY,
        category_id INT             NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
        name        VARCHAR(120)    NOT NULL,
        description TEXT,
        base_price  NUMERIC(10,2)   NOT NULL CHECK (base_price >= 0),
        image_url   VARCHAR(512),
        is_active   BOOLEAN         NOT NULL DEFAULT TRUE,
        created_at  TIMESTAMPTZ     NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at  TIMESTAMPTZ     NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT uq_product_name_category UNIQUE (category_id, name)
      );

      CREATE TABLE IF NOT EXISTS product_variants (
        id              SERIAL        PRIMARY KEY,
        product_id      INT           NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        size_id         SMALLINT      NOT NULL REFERENCES sizes(id)    ON DELETE RESTRICT,
        color_id        SMALLINT      NOT NULL REFERENCES colors(id)   ON DELETE RESTRICT,
        sku             VARCHAR(60)   NOT NULL UNIQUE,
        stock           INT           NOT NULL DEFAULT 0  CHECK (stock >= 0),
        alert_threshold INT           NOT NULL DEFAULT 3  CHECK (alert_threshold >= 0),
        created_at      TIMESTAMPTZ   NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at      TIMESTAMPTZ   NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT uq_variant UNIQUE (product_id, size_id, color_id)
      );

      CREATE TABLE IF NOT EXISTS clients (
        id          SERIAL       PRIMARY KEY,
        full_name   VARCHAR(120) NOT NULL,
        phone       VARCHAR(20)  NOT NULL UNIQUE,
        address     TEXT         NOT NULL,
        district_id SMALLINT     NOT NULL REFERENCES districts(id) ON DELETE RESTRICT,
        reference   TEXT,
        created_at  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP
      );

      CREATE SEQUENCE IF NOT EXISTS order_number_seq;

      CREATE TABLE IF NOT EXISTS orders (
        id                SERIAL             PRIMARY KEY,
        order_number      VARCHAR(30)        NOT NULL UNIQUE,
        client_id         INT                NOT NULL REFERENCES clients(id)         ON DELETE RESTRICT,
        user_id           INT                         REFERENCES users(id)           ON DELETE SET NULL,
        payment_method_id SMALLINT           NOT NULL REFERENCES payment_methods(id) ON DELETE RESTRICT,
        status            order_status_enum  NOT NULL DEFAULT 'RECIBIDO',
        subtotal          NUMERIC(10,2)      NOT NULL DEFAULT 0.00 CHECK (subtotal      >= 0),
        shipping_cost     NUMERIC(10,2)      NOT NULL DEFAULT 0.00 CHECK (shipping_cost >= 0),
        total_amount      NUMERIC(10,2)      NOT NULL DEFAULT 0.00 CHECK (total_amount  >= 0),
        shipping_type     VARCHAR(20)        DEFAULT NULL,
        destination_city  VARCHAR(100)       DEFAULT NULL,
        shipping_agency   VARCHAR(50)        DEFAULT NULL,
        tracking_number   VARCHAR(50)        DEFAULT NULL,
        notes             TEXT,
        created_at        TIMESTAMPTZ        NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at        TIMESTAMPTZ        NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT chk_total CHECK (total_amount = subtotal + shipping_cost)
      );

      CREATE TABLE IF NOT EXISTS order_items (
        id         SERIAL        PRIMARY KEY,
        order_id   INT           NOT NULL REFERENCES orders(id)          ON DELETE CASCADE,
        variant_id INT           NOT NULL REFERENCES product_variants(id) ON DELETE RESTRICT,
        quantity   INT           NOT NULL CHECK (quantity > 0),
        unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
        subtotal   NUMERIC(10,2) NOT NULL CHECK (subtotal   >= 0),
        CONSTRAINT chk_item_subtotal CHECK (subtotal = quantity * unit_price),
        CONSTRAINT uq_order_variant UNIQUE (order_id, variant_id)
      );

      CREATE TABLE IF NOT EXISTS order_status_history (
        id              SERIAL             PRIMARY KEY,
        order_id        INT                NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
        user_id         INT                         REFERENCES users(id)  ON DELETE SET NULL,
        previous_status order_status_enum,
        new_status      order_status_enum  NOT NULL,
        changed_at      TIMESTAMPTZ        NOT NULL DEFAULT CURRENT_TIMESTAMP,
        comments        TEXT
      );

      -- Funciones y triggers de auditoría y stock
      CREATE OR REPLACE FUNCTION fn_set_updated_at()
      RETURNS TRIGGER LANGUAGE plpgsql AS $$
      BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
      END;
      $$;

      DROP TRIGGER IF EXISTS trg_users_updated_at ON users;
      CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

      DROP TRIGGER IF EXISTS trg_products_updated_at ON products;
      CREATE TRIGGER trg_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

      DROP TRIGGER IF EXISTS trg_product_variants_updated_at ON product_variants;
      CREATE TRIGGER trg_product_variants_updated_at BEFORE UPDATE ON product_variants FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

      DROP TRIGGER IF EXISTS trg_clients_updated_at ON clients;
      CREATE TRIGGER trg_clients_updated_at BEFORE UPDATE ON clients FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

      DROP TRIGGER IF EXISTS trg_orders_updated_at ON orders;
      CREATE TRIGGER trg_orders_updated_at BEFORE UPDATE ON orders FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

      CREATE OR REPLACE FUNCTION fn_decrement_stock()
      RETURNS TRIGGER LANGUAGE plpgsql AS $$
      BEGIN
        UPDATE product_variants SET stock = stock - NEW.quantity WHERE id = NEW.variant_id;
        IF (SELECT stock FROM product_variants WHERE id = NEW.variant_id) < 0 THEN
          RAISE EXCEPTION 'Stock insuficiente para la variante %', NEW.variant_id;
        END IF;
        RETURN NEW;
      END;
      $$;

      DROP TRIGGER IF EXISTS trg_decrement_stock_on_order ON order_items;
      CREATE TRIGGER trg_decrement_stock_on_order AFTER INSERT ON order_items FOR EACH ROW EXECUTE FUNCTION fn_decrement_stock();

      -- Índices de optimización
      CREATE INDEX IF NOT EXISTS idx_orders_status        ON orders(status);
      CREATE INDEX IF NOT EXISTS idx_orders_created_at    ON orders(created_at DESC);
      CREATE INDEX IF NOT EXISTS idx_orders_client        ON orders(client_id);
      CREATE INDEX IF NOT EXISTS idx_orders_payment       ON orders(payment_method_id);
      CREATE INDEX IF NOT EXISTS idx_variants_product     ON product_variants(product_id);
      CREATE INDEX IF NOT EXISTS idx_variants_sku         ON product_variants(sku);
      CREATE INDEX IF NOT EXISTS idx_variants_stock       ON product_variants(stock) WHERE stock <= alert_threshold;
      CREATE INDEX IF NOT EXISTS idx_clients_phone        ON clients(phone);
      CREATE INDEX IF NOT EXISTS idx_clients_district     ON clients(district_id);
      CREATE INDEX IF NOT EXISTS idx_order_items_order    ON order_items(order_id);
      CREATE INDEX IF NOT EXISTS idx_order_items_variant  ON order_items(variant_id);
      CREATE INDEX IF NOT EXISTS idx_status_history_order ON order_status_history(order_id);
      CREATE INDEX IF NOT EXISTS idx_status_history_date  ON order_status_history(changed_at DESC);
      CREATE INDEX IF NOT EXISTS idx_products_category    ON products(category_id) WHERE is_active = TRUE;

      -- Vistas operativas y analíticas
      CREATE OR REPLACE VIEW vw_low_stock_alert AS
      SELECT
        pv.id          AS variant_id,
        p.name         AS product_name,
        s.code         AS size,
        c.name         AS color,
        pv.sku,
        pv.stock,
        pv.alert_threshold,
        (pv.alert_threshold - pv.stock) AS units_below_threshold
      FROM product_variants pv
      JOIN products p ON pv.product_id = p.id
      JOIN sizes    s ON pv.size_id    = s.id
      JOIN colors   c ON pv.color_id   = c.id
      WHERE pv.stock <= pv.alert_threshold
        AND p.is_active = TRUE
      ORDER BY units_below_threshold DESC;

      CREATE OR REPLACE VIEW vw_orders_summary AS
      SELECT
        o.id,
        o.order_number,
        cl.full_name        AS client_name,
        cl.phone            AS client_phone,
        d.name              AS district,
        pm.name             AS payment_method,
        o.status,
        o.subtotal,
        o.shipping_cost,
        o.total_amount,
        o.created_at
      FROM orders o
      JOIN clients         cl ON o.client_id         = cl.id
      JOIN districts       d  ON cl.district_id       = d.id
      JOIN payment_methods pm ON o.payment_method_id  = pm.id
      ORDER BY o.created_at DESC;

      -- Seeds iniciales idempotentes (Catálogo, Usuarios, Variantes, Clientes y Pedidos base)
      INSERT INTO sizes (id, code, label) VALUES
        (1, 'S',     'Small'),
        (2, 'M',     'Medium'),
        (3, 'L',     'Large'),
        (4, 'XL',    'Extra Large'),
        (5, 'XXL',   'Double Extra Large'),
        (6, 'UNICA', 'Talla Única')
      ON CONFLICT (code) DO UPDATE SET label = EXCLUDED.label;
      SELECT setval('sizes_id_seq', (SELECT COALESCE(MAX(id), 1) FROM sizes));

      INSERT INTO colors (id, name, hex) VALUES
        (1,  'Negro Lavado',    '#1A1A1A'),
        (2,  'Blanco Crudo',    '#F5F0E8'),
        (3,  'Gris Jaspe',      '#8A8A8A'),
        (4,  'Negro Mate',      '#0D0D0D'),
        (5,  'Azul Marino',     '#002368'),
        (6,  'Rojo Fuego',      '#CC2200'),
        (7,  'Verde Militar',   '#3B4A2F'),
        (8,  'Negro / Rojo',    '#440000'),
        (9,  'Gris / Blanco',   '#C0C0C0'),
        (10, 'Azul / Negro',    '#001338')
      ON CONFLICT (name) DO UPDATE SET hex = EXCLUDED.hex;
      SELECT setval('colors_id_seq', (SELECT COALESCE(MAX(id), 1) FROM colors));

      INSERT INTO districts (id, name) VALUES
        (1,  'Jesús María'),
        (2,  'San Isidro'),
        (3,  'San Miguel'),
        (4,  'Barranco'),
        (5,  'Miraflores'),
        (6,  'Surco'),
        (7,  'La Molina'),
        (8,  'Lince'),
        (9,  'San Borja'),
        (10, 'Magdalena del Mar')
      ON CONFLICT (name) DO NOTHING;
      SELECT setval('districts_id_seq', (SELECT COALESCE(MAX(id), 1) FROM districts));

      INSERT INTO payment_methods (id, code, name) VALUES
        (1, 'YAPE',           'Yape'),
        (2, 'PLIN',           'Plin'),
        (3, 'TRANSFERENCIA',  'Transferencia Bancaria'),
        (4, 'CONTRAENTREGA',  'Contraentrega en Efectivo'),
        (5, 'EFECTIVO',       'Efectivo Directo')
      ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name;
      SELECT setval('payment_methods_id_seq', (SELECT COALESCE(MAX(id), 1) FROM payment_methods));

      INSERT INTO users (id, name, email, password_hash, role, is_active) VALUES
        (1, 'Administrador LeoFit', 'admin@leofit.pe',    '$2a$10$RFM9LaopMTzwwFXrBtkWh.I/AFVC3m0Qf62ZsXT06IT4WIejbsBUe', 'ADMIN',    TRUE),
        (2, 'Operador Logistico',   'operador@leofit.pe', '$2a$10$RFM9LaopMTzwwFXrBtkWh.I/AFVC3m0Qf62ZsXT06IT4WIejbsBUe', 'OPERATOR', TRUE)
      ON CONFLICT (email) DO NOTHING;
      SELECT setval('users_id_seq', (SELECT COALESCE(MAX(id), 1) FROM users));

      INSERT INTO categories (id, name, description) VALUES
        (1, 'Camisetas',         'Línea de camisetas oversize y fit en algodón peinado 20/1 y 24/1'),
        (2, 'Shorts',            'Shorts deportivos con forro de compresión y bolsillos con cierre'),
        (3, 'Joggers',           'Pantalones de entrenamiento corte slim con rib ajustado'),
        (4, 'Tirantes / Bividis','Prendas sin mangas corte halter y espalda nadadora para entrenamiento'),
        (5, 'Accesorios',        'Correas de levantamiento, muñequeras, shakers y gorras deportivas')
      ON CONFLICT (id) DO NOTHING;
      SELECT setval('categories_id_seq', (SELECT COALESCE(MAX(id), 1) FROM categories));

      INSERT INTO products (id, category_id, name, description, base_price, image_url, is_active) VALUES
        (1, 1, 'Camiseta Oversize Heavy Acid Wash',
           'Confeccionada en algodón 100% 20/1 con proceso acid wash industrial y estampado serigráfico de alta densidad.',
           65.00, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500', TRUE),
        (2, 2, 'Short 2-en-1 Pro Performance',
           'Short exterior de secado rápido con calza interior de compresión y bolsillo elástico para smartphone.',
           55.00, 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500', TRUE),
        (3, 3, 'Jogger Slim Tech Fleece',
           'Jogger térmico con tecnología stretch de 4 vías, bolsillos termosellados y pretina reforzada.',
           79.00, 'https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=500', TRUE),
        (4, 4, 'Bividi Drop Cut Raw Edge',
           'Musculosa deportiva con corte drop armhole para máxima ventilación y rango de movimiento.',
           45.00, 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=500', TRUE),
        (5, 5, 'Straps de Levantamiento Reforzados',
           'Par de correas de algodón con soporte acolchado de neopreno para muñecas.',
           28.00, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500', TRUE),
        (6, 1, 'Camiseta Slim Fit Essential',
           'Camiseta entallada de algodón 24/1 peinado, corte recto con cuello acanalado reforzado.',
           55.00, 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=500', TRUE),
        (7, 2, 'Short Board 5" Training',
           'Short running liviano con bolsillos traseros con velcro y banda reflectante para seguridad.',
           49.00, 'https://images.unsplash.com/photo-1562886877-f88e38ac9b55?w=500', TRUE),
        (8, 5, 'Gorra Snapback Dry-Fit',
           'Gorra deportiva con tejido dry-fit, visera pre-curvada y cierre snapback regulable.',
           38.00, 'https://images.unsplash.com/photo-1523450001312-faa4e2e37f0f?w=500', TRUE)
      ON CONFLICT (id) DO NOTHING;
      SELECT setval('products_id_seq', (SELECT COALESCE(MAX(id), 1) FROM products));

      ALTER TABLE order_items DISABLE TRIGGER trg_decrement_stock_on_order;

      INSERT INTO product_variants (id, product_id, size_id, color_id, sku, stock, alert_threshold) VALUES
        (1,  1, 1, 1, 'LF-TSH-OVR-BLK-S',   12, 3),
        (2,  1, 2, 1, 'LF-TSH-OVR-BLK-M',   18, 3),
        (3,  1, 3, 1, 'LF-TSH-OVR-BLK-L',    8, 3),
        (4,  1, 4, 1, 'LF-TSH-OVR-BLK-XL',   2, 3),
        (5,  1, 5, 1, 'LF-TSH-OVR-BLK-XXL',  4, 3),
        (6,  2, 2, 3, 'LF-SHT-2N1-GRY-M',   15, 4),
        (7,  2, 3, 3, 'LF-SHT-2N1-GRY-L',   10, 4),
        (8,  2, 4, 3, 'LF-SHT-2N1-GRY-XL',   3, 4),
        (9,  3, 2, 4, 'LF-JOG-SLM-BLK-M',    7, 3),
        (10, 3, 3, 4, 'LF-JOG-SLM-BLK-L',    5, 3),
        (11, 3, 4, 4, 'LF-JOG-SLM-BLK-XL',   9, 3),
        (12, 4, 2, 2, 'LF-BIV-DRP-WHT-M',   14, 3),
        (13, 4, 3, 2, 'LF-BIV-DRP-WHT-L',    6, 3),
        (14, 4, 2, 1, 'LF-BIV-DRP-BLK-M',   11, 3),
        (15, 5, 6, 8, 'LF-ACC-STP-RED-U',    25, 5),
        (16, 6, 1, 5, 'LF-TSH-SLM-NVY-S',    9, 3),
        (17, 6, 2, 5, 'LF-TSH-SLM-NVY-M',   14, 3),
        (18, 6, 3, 5, 'LF-TSH-SLM-NVY-L',    7, 3),
        (19, 6, 2, 6, 'LF-TSH-SLM-RED-M',    5, 3),
        (20, 6, 3, 6, 'LF-TSH-SLM-RED-L',    2, 3),
        (21, 7, 2, 7, 'LF-SHT-BRD-GRN-M',   12, 3),
        (22, 7, 3, 7, 'LF-SHT-BRD-GRN-L',    8, 3),
        (23, 8, 6, 4, 'LF-ACC-CAP-BLK-U',   30, 5)
      ON CONFLICT (id) DO NOTHING;
      SELECT setval('product_variants_id_seq', (SELECT COALESCE(MAX(id), 1) FROM product_variants));

      INSERT INTO clients (id, full_name, phone, address, district_id, reference) VALUES
        (1, 'Carlos Eduardo Mendoza Flores',   '987654321', 'Av. Brasil 1420 Dpto 802', 1, 'A dos cuadras del Hospital del Niño'),
        (2, 'Valeria Sofía Alarcón Benavides', '912345678', 'Calle Las Begonias 340', 2, 'Frente a la torre financiera'),
        (3, 'Rodrigo Alonso Quispe Huamán',    '998877665', 'Av. Universitaria 2100 Cond. Los Robles Torre B 401', 3, 'Espalda de Plaza San Miguel'),
        (4, 'Maricielo Andrea Peña Ruiz',      '934567890', 'Jr. Batalla de Junín 215', 4, 'Cerca a la estación Bulevar del Metropolitano'),
        (5, 'Diego Sebastián Torres Vílchez',  '945678123', 'Av. Larco 880 Piso 3', 5, 'Frente al Parque Kennedy'),
        (6, 'Luciana Paola Ramos Callupe',     '976543210', 'Calle Monte Bello 230', 6, 'A media cuadra del Ovalo Higuereta'),
        (7, 'Andrés Felipe Huanca Mamani',     '923456789', 'Av. La Molina 1234 Urb. El Remanso', 7, 'Portón azul, referencia estación La Molina')
      ON CONFLICT (id) DO NOTHING;
      SELECT setval('clients_id_seq', (SELECT COALESCE(MAX(id), 1) FROM clients));

      INSERT INTO orders (id, order_number, client_id, user_id, payment_method_id, status, subtotal, shipping_cost, total_amount, notes) VALUES
        (1, 'ORD-2026-001', 1, 1, 1, 'RECIBIDO',    130.00, 10.00, 140.00, 'Cliente solicita entrega entre 2:00 pm y 5:00 pm'),
        (2, 'ORD-2026-002', 2, 1, 2, 'PREPARACION', 134.00, 12.00, 146.00, 'Empaque para regalo con dedicatoria'),
        (3, 'ORD-2026-003', 3, 2, 3, 'EN_CAMINO',    79.00,  8.00,  87.00, 'Repartidor motorizado en ruta. Código de seguimiento enviado.'),
        (4, 'ORD-2026-004', 4, 1, 4, 'ENTREGADO',    65.00, 10.00,  75.00, 'Pedido recibido conforme y cobrado en efectivo.'),
        (5, 'ORD-2026-005', 5, 2, 1, 'RECIBIDO',    183.00, 12.00, 195.00, 'Cliente VIP — empacar con bolsa premium y tarjeta de agradecimiento.'),
        (6, 'ORD-2026-006', 6, 1, 5, 'CANCELADO',    55.00,  8.00,  63.00, 'Cliente canceló por error en la talla seleccionada.')
      ON CONFLICT (id) DO NOTHING;
      SELECT setval('orders_id_seq', (SELECT COALESCE(MAX(id), 1) FROM orders));
      SELECT setval('order_number_seq', (SELECT COALESCE(MAX(id), 6) FROM orders));

      INSERT INTO order_items (id, order_id, variant_id, quantity, unit_price, subtotal) VALUES
        (1,  1, 2,  2, 65.00, 130.00),
        (2,  2, 6,  1, 55.00,  55.00),
        (3,  2, 3,  1, 65.00,  65.00),
        (4,  2, 15, 1, 14.00,  14.00),
        (5,  3, 9,  1, 79.00,  79.00),
        (6,  4, 1,  1, 65.00,  65.00),
        (7,  5, 17, 1, 55.00,  55.00),
        (8,  5, 11, 1, 79.00,  79.00),
        (9,  5, 23, 1, 38.00,  38.00),
        (10, 6, 6,  1, 55.00,  55.00)
      ON CONFLICT (id) DO NOTHING;
      SELECT setval('order_items_id_seq', (SELECT COALESCE(MAX(id), 1) FROM order_items));

      ALTER TABLE order_items ENABLE TRIGGER trg_decrement_stock_on_order;

      INSERT INTO order_status_history (id, order_id, user_id, previous_status, new_status, comments) VALUES
        (1, 1, 1, NULL,          'RECIBIDO',    'Pedido creado exitosamente desde WhatsApp'),
        (2, 2, 1, 'RECIBIDO',    'PREPARACION', 'Prendas separadas en taller y empaquetadas'),
        (3, 3, 2, 'PREPARACION', 'EN_CAMINO',   'Entregado a servicio de courier local'),
        (4, 4, 1, 'EN_CAMINO',   'ENTREGADO',   'Entrega confirmada y recibida por el cliente'),
        (5, 5, 2, NULL,          'RECIBIDO',    'Pedido VIP creado y priorizado'),
        (6, 6, 1, NULL,          'RECIBIDO',    'Pedido creado'),
        (7, 6, 1, 'RECIBIDO',    'CANCELADO',   'Cliente solicitó cancelación por talla incorrecta')
      ON CONFLICT (id) DO NOTHING;
      SELECT setval('order_status_history_id_seq', (SELECT COALESCE(MAX(id), 1) FROM order_status_history));
    `);
  }
};

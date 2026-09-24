-- =============================================================================
-- SISTEMA DE GESTIÓN DE PEDIDOS Y CONTROL DE INVENTARIO - LEOFIT SOLUTIONS
-- SCRIPT DDL: ESQUEMA RELACIONAL POSTGRESQL 16
-- NORMALIZACIÓN: BOYCE-CODD NORMAL FORM (BCNF)
-- Alta Disponibilidad | Streaming Replication | Inventario de Prendas
-- =============================================================================
-- VERSION : 2.0.0
-- MOTOR   : PostgreSQL 16+
-- =============================================================================

-- Limpiar objetos previos (orden correcto por FK)
DROP TABLE IF EXISTS order_status_history CASCADE;
DROP TABLE IF EXISTS order_items         CASCADE;
DROP TABLE IF EXISTS orders              CASCADE;
DROP TABLE IF EXISTS product_variants    CASCADE;
DROP TABLE IF EXISTS products            CASCADE;
DROP TABLE IF EXISTS categories          CASCADE;
DROP TABLE IF EXISTS clients             CASCADE;
DROP TABLE IF EXISTS users               CASCADE;
DROP TABLE IF EXISTS sizes               CASCADE;
DROP TABLE IF EXISTS colors              CASCADE;
DROP TABLE IF EXISTS districts           CASCADE;
DROP TABLE IF EXISTS payment_methods     CASCADE;

-- Tipos ENUM para dominios cerrados (BCNF: sin dependencias parciales por literales)
DROP TYPE IF EXISTS user_role_enum     CASCADE;
DROP TYPE IF EXISTS order_status_enum  CASCADE;

CREATE TYPE user_role_enum    AS ENUM ('ADMIN', 'OPERATOR');
CREATE TYPE order_status_enum AS ENUM ('RECIBIDO', 'PREPARACION', 'EN_CAMINO', 'ENTREGADO', 'CANCELADO');

-- =============================================================================
-- TABLAS DE DOMINIO (lookup / catálogo)
-- BCNF: toda dependencia funcional tiene como determinante una superclave.
-- Extraer dominios en tablas propias elimina dependencias transitivas.
-- =============================================================================

-- Tallas (dominio cerrado extraído a tabla propia → BCNF)
CREATE TABLE sizes (
    id    SMALLSERIAL PRIMARY KEY,
    code  VARCHAR(10)  NOT NULL UNIQUE,        -- 'S', 'M', 'L', 'XL', 'XXL', 'UNICA'
    label VARCHAR(30)  NOT NULL                -- etiqueta legible
);
COMMENT ON TABLE sizes IS 'Catálogo maestro de tallas; elimina dependencia transitiva en product_variants.';

-- Colores (dominio extraído → BCNF)
CREATE TABLE colors (
    id   SMALLSERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL UNIQUE,
    hex  CHAR(7)                               -- representación HEX opcional
);
COMMENT ON TABLE colors IS 'Catálogo de colores disponibles en el inventario de prendas.';

-- Distritos de reparto (dominio extraído → BCNF: evita repetición de strings)
CREATE TABLE districts (
    id   SMALLSERIAL  PRIMARY KEY,
    name VARCHAR(80)  NOT NULL UNIQUE
);
COMMENT ON TABLE districts IS 'Catálogo de distritos de Lima para entregas; centraliza el dominio geográfico.';

-- Métodos de pago (dominio cerrado extraído → BCNF)
CREATE TABLE payment_methods (
    id   SMALLSERIAL PRIMARY KEY,
    code VARCHAR(30)  NOT NULL UNIQUE,         -- 'YAPE', 'PLIN', etc.
    name VARCHAR(60)  NOT NULL
);
COMMENT ON TABLE payment_methods IS 'Métodos de pago disponibles; permite ampliar sin ALTER TABLE.';

-- =============================================================================
-- ENTIDADES PRINCIPALES
-- =============================================================================

-- 1. Usuarios del sistema
CREATE TABLE users (
    id            SERIAL          PRIMARY KEY,
    name          VARCHAR(100)    NOT NULL,
    email         VARCHAR(150)    NOT NULL UNIQUE,
    password_hash VARCHAR(255)    NOT NULL,
    role          user_role_enum  NOT NULL DEFAULT 'OPERATOR',
    is_active     BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMPTZ     NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE users IS 'Usuarios administrativos del sistema. BCNF: cada atributo depende únicamente de id (PK).';

-- 2. Categorías de indumentaria
CREATE TABLE categories (
    id          SERIAL       PRIMARY KEY,
    name        VARCHAR(60)  NOT NULL UNIQUE,
    description TEXT,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE categories IS 'Categorías de productos (Camisetas, Shorts, Joggers…). name es superclave alternativa.';

-- 3. Productos (catálogo base)
CREATE TABLE products (
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
COMMENT ON TABLE products IS 'Catálogo base de prendas. BCNF: base_price → product, no dependencia de categoría.';

-- 4. Variantes de producto (inventario por talla y color) — BCNF
--    Dependencias funcionales:
--      sku → {product_id, size_id, color_id, stock, alert_threshold}   (sku es superclave)
--      {product_id, size_id, color_id} → sku                           (clave candidata compuesta)
--    Ambas determinantes son superclaves → BCNF satisfecho.
CREATE TABLE product_variants (
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
COMMENT ON TABLE product_variants IS
  'Inventario por combinación única (producto, talla, color). SKU es clave alternativa. BCNF verificado.';

-- 5. Clientes
CREATE TABLE clients (
    id          SERIAL       PRIMARY KEY,
    full_name   VARCHAR(120) NOT NULL,
    phone       VARCHAR(20)  NOT NULL UNIQUE,
    address     TEXT         NOT NULL,
    district_id SMALLINT     NOT NULL REFERENCES districts(id) ON DELETE RESTRICT,
    reference   TEXT,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE clients IS
  'Clientes. district_id FK a tabla districts (dominio extraído → BCNF eliminó dependencia transitiva).';

-- 6. Cabecera de pedidos
CREATE TABLE orders (
    id                SERIAL             PRIMARY KEY,
    order_number      VARCHAR(30)        NOT NULL UNIQUE,
    client_id         INT                NOT NULL REFERENCES clients(id)         ON DELETE RESTRICT,
    user_id           INT                         REFERENCES users(id)           ON DELETE SET NULL,
    payment_method_id SMALLINT           NOT NULL REFERENCES payment_methods(id) ON DELETE RESTRICT,
    status            order_status_enum  NOT NULL DEFAULT 'RECIBIDO',
    subtotal          NUMERIC(10,2)      NOT NULL DEFAULT 0.00 CHECK (subtotal      >= 0),
    shipping_cost     NUMERIC(10,2)      NOT NULL DEFAULT 0.00 CHECK (shipping_cost >= 0),
    total_amount      NUMERIC(10,2)      NOT NULL DEFAULT 0.00 CHECK (total_amount  >= 0),
    notes             TEXT,
    created_at        TIMESTAMPTZ        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMPTZ        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_total CHECK (total_amount = subtotal + shipping_cost)
);
COMMENT ON TABLE orders IS 'Cabecera de pedido. payment_method_id FK a tabla propia → BCNF.';

-- 7. Detalle de ítems del pedido
CREATE TABLE order_items (
    id         SERIAL        PRIMARY KEY,
    order_id   INT           NOT NULL REFERENCES orders(id)          ON DELETE CASCADE,
    variant_id INT           NOT NULL REFERENCES product_variants(id) ON DELETE RESTRICT,
    quantity   INT           NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    subtotal   NUMERIC(10,2) NOT NULL CHECK (subtotal   >= 0),
    CONSTRAINT chk_item_subtotal CHECK (subtotal = quantity * unit_price),
    CONSTRAINT uq_order_variant UNIQUE (order_id, variant_id)
);
COMMENT ON TABLE order_items IS 'Ítems por pedido. subtotal = quantity × unit_price (restricción declarativa).';

-- 8. Historial de auditoría de estados
CREATE TABLE order_status_history (
    id              SERIAL             PRIMARY KEY,
    order_id        INT                NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    user_id         INT                         REFERENCES users(id)  ON DELETE SET NULL,
    previous_status order_status_enum,
    new_status      order_status_enum  NOT NULL,
    changed_at      TIMESTAMPTZ        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comments        TEXT
);
COMMENT ON TABLE order_status_history IS 'Traza inmutable de cambios de estado por pedido.';

-- =============================================================================
-- FUNCIÓN Y TRIGGERS: updated_at automático
-- =============================================================================
CREATE OR REPLACE FUNCTION fn_set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_product_variants_updated_at
    BEFORE UPDATE ON product_variants
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_clients_updated_at
    BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE TRIGGER trg_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

-- =============================================================================
-- TRIGGER: Descuento automático de stock al confirmar ítem de pedido
-- =============================================================================
CREATE OR REPLACE FUNCTION fn_decrement_stock()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    UPDATE product_variants
       SET stock = stock - NEW.quantity
     WHERE id = NEW.variant_id;

    IF (SELECT stock FROM product_variants WHERE id = NEW.variant_id) < 0 THEN
        RAISE EXCEPTION 'Stock insuficiente para la variante %', NEW.variant_id;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_decrement_stock_on_order
    AFTER INSERT ON order_items
    FOR EACH ROW EXECUTE FUNCTION fn_decrement_stock();

-- =============================================================================
-- ÍNDICES DE OPTIMIZACIÓN
-- =============================================================================
CREATE INDEX idx_orders_status        ON orders(status);
CREATE INDEX idx_orders_created_at    ON orders(created_at DESC);
CREATE INDEX idx_orders_client        ON orders(client_id);
CREATE INDEX idx_orders_payment       ON orders(payment_method_id);
CREATE INDEX idx_variants_product     ON product_variants(product_id);
CREATE INDEX idx_variants_sku         ON product_variants(sku);
CREATE INDEX idx_variants_stock       ON product_variants(stock) WHERE stock <= alert_threshold;
CREATE INDEX idx_clients_phone        ON clients(phone);
CREATE INDEX idx_clients_district     ON clients(district_id);
CREATE INDEX idx_order_items_order    ON order_items(order_id);
CREATE INDEX idx_order_items_variant  ON order_items(variant_id);
CREATE INDEX idx_status_history_order ON order_status_history(order_id);
CREATE INDEX idx_status_history_date  ON order_status_history(changed_at DESC);
CREATE INDEX idx_products_category    ON products(category_id) WHERE is_active = TRUE;

-- =============================================================================
-- VISTA: Alerta de Stock Bajo (para dashboard operativo)
-- =============================================================================
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

COMMENT ON VIEW vw_low_stock_alert IS 'Prendas con stock ≤ umbral de alerta; alimenta el dashboard.';

-- =============================================================================
-- VISTA: Resumen de pedidos con datos de cliente y método de pago
-- =============================================================================
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

COMMENT ON VIEW vw_orders_summary IS 'Vista desnormalizada para consultas de listado y reportes de pedidos.';
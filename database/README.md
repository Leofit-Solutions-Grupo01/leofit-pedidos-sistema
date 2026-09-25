# Módulo de Base de Datos — Leofit Solutions

Este directorio contiene el esquema relacional, datos iniciales, configuración de
replicación, estrategia de respaldo y connection pooling del
**Sistema de Gestión de Pedidos de Leofit**.

---

## 1. Selección del Motor de Base de Datos

### Motor Elegido: **PostgreSQL 16**

#### Justificación Técnica
1. **Garantía ACID & Transaccionalidad:** La creación de un pedido y el descuento
   de inventario son operaciones atómicas (trigger `fn_decrement_stock`).
2. **Integridad Referencial Estricta:** FK con `ON DELETE RESTRICT / CASCADE`
   evitan pedidos huérfanos o ventas de productos inexistentes.
3. **Alta Disponibilidad:** Streaming Replication física con slot
   `standby_slot_leofit_replica1` y Hot Standby para consultas de reportes.
4. **Connection Pooling:** PgBouncer en modo `transaction` multiplexando hasta
   200 conexiones de cliente sobre 25 conexiones reales al servidor.

---

## 2. Estructura de Archivos

```
database/
├── schema.sql              # DDL normalizado en BCNF — PostgreSQL 16
├── seeds.sql               # DML: catálogo deportivo, tallas, colores, clientes
├── replication_setup.sql   # Streaming Replication + slot standby_slot_leofit_replica1
├── backup_strategy.sh      # Backup automatizado con firmas SHA-256
└── pgbouncer/
    ├── pgbouncer.ini       # Configuración connection pooling transaccional
    ├── userlist.txt        # Usuarios y hashes SCRAM-SHA-256
    └── setup_pgbouncer.sh  # Script de instalación y configuración
```

---

## 3. Diagramas del Modelo de Datos (Alta Resolución 300 DPI)

* 📐 **Modelo Lógico de Dominio (DER):** [`diagrams/12_Modelo_Logico_BD.png`](../diagrams/12_Modelo_Logico_BD.png)
* 🗄️ **Modelo Físico Implementado (Esquema DDL Relacional):** [`diagrams/13_Modelo_Fisico_BD.png`](../diagrams/13_Modelo_Fisico_BD.png)
* 📊 **Diagrama de Entidades Complementario:** [`diagrams/14_Diagrama_DB.png`](../diagrams/14_Diagrama_DB.png)

### 3.1. Diagrama Entidad-Relación (ERD) — Esquema BCNF

```mermaid
erDiagram
  SIZES ||--o{ PRODUCT_VARIANTS : "define_talla"
  COLORS ||--o{ PRODUCT_VARIANTS : "define_color"
  DISTRICTS ||--o{ CLIENTS : "ubica"
  PAYMENT_METHODS ||--o{ ORDERS : "método_de_pago"
  USERS ||--o{ ORDERS : "registra"
  CLIENTS ||--o{ ORDERS : "realiza"
  CATEGORIES ||--|{ PRODUCTS : "clasifica"
  PRODUCTS ||--|{ PRODUCT_VARIANTS : "posee"
  PRODUCT_VARIANTS ||--o{ ORDER_ITEMS : "incluido_en"
  ORDERS ||--|{ ORDER_ITEMS : "contiene"
  ORDERS ||--|{ ORDER_STATUS_HISTORY : "historial"

  SIZES {
    smallint id PK
    varchar  code UK
    varchar  label
  }
  COLORS {
    smallint id PK
    varchar  name UK
    char     hex
  }
  DISTRICTS {
    smallint id PK
    varchar  name UK
  }
  PAYMENT_METHODS {
    smallint id PK
    varchar  code UK
    varchar  name
  }
  USERS {
    int      id PK
    varchar  name
    varchar  email UK
    varchar  password_hash
    enum     role "ADMIN|OPERATOR"
    boolean  is_active
    timestamptz created_at
    timestamptz updated_at
  }
  CATEGORIES {
    int     id PK
    varchar name UK
    text    description
  }
  PRODUCTS {
    int      id PK
    int      category_id FK
    varchar  name
    numeric  base_price
    boolean  is_active
    timestamptz updated_at
  }
  PRODUCT_VARIANTS {
    int      id PK
    int      product_id FK
    smallint size_id FK
    smallint color_id FK
    varchar  sku UK
    int      stock
    int      alert_threshold
    timestamptz updated_at
  }
  CLIENTS {
    int      id PK
    varchar  full_name
    varchar  phone UK
    text     address
    smallint district_id FK
    timestamptz updated_at
  }
  ORDERS {
    int      id PK
    varchar  order_number UK
    int      client_id FK
    int      user_id FK
    smallint payment_method_id FK
    enum     status
    numeric  subtotal
    numeric  shipping_cost
    numeric  total_amount
    timestamptz created_at
    timestamptz updated_at
  }
  ORDER_ITEMS {
    int     id PK
    int     order_id FK
    int     variant_id FK
    int     quantity
    numeric unit_price
    numeric subtotal
  }
  ORDER_STATUS_HISTORY {
    int         id PK
    int         order_id FK
    int         user_id FK
    enum        previous_status
    enum        new_status
    timestamptz changed_at
    text        comments
  }
```

---

## 4. Normalización BCNF — Justificación de Tablas de Dominio

Las siguientes tablas fueron **extraídas** del esquema original para eliminar
dependencias transitivas y cumplir con la Forma Normal de Boyce-Codd:

| Tabla extraída | Dependencia transitiva eliminada |
|---|---|
| `sizes` | `product_variants.size (string)` → catálogo centralizado |
| `colors` | `product_variants.color (string)` → catálogo centralizado |
| `districts` | `clients.district (string)` → catálogo centralizado |
| `payment_methods` | `orders.payment_method (enum string)` → catálogo centralizado |

En la BCNF toda dependencia funcional `X → Y` requiere que `X` sea superclave.
Al extraer estos dominios, cada atributo depende únicamente de la PK de su tabla.

---

## 5. Diccionario de Datos

### `sizes` — Catálogo de Tallas
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SMALLSERIAL | PK | Identificador auto |
| `code` | VARCHAR(10) | UNIQUE NOT NULL | Código: S, M, L, XL, XXL, UNICA |
| `label` | VARCHAR(30) | NOT NULL | Etiqueta legible |

### `colors` — Catálogo de Colores
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SMALLSERIAL | PK | Identificador auto |
| `name` | VARCHAR(60) | UNIQUE NOT NULL | Nombre del color |
| `hex` | CHAR(7) | | Código hexadecimal (#RRGGBB) |

### `districts` — Distritos de Reparto
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SMALLSERIAL | PK | Identificador auto |
| `name` | VARCHAR(80) | UNIQUE NOT NULL | Nombre del distrito |

### `payment_methods` — Métodos de Pago
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SMALLSERIAL | PK | Identificador auto |
| `code` | VARCHAR(30) | UNIQUE NOT NULL | YAPE, PLIN, TRANSFERENCIA… |
| `name` | VARCHAR(60) | NOT NULL | Nombre legible |

### `users` — Usuarios del Sistema
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SERIAL | PK | Identificador auto |
| `name` | VARCHAR(100) | NOT NULL | Nombre completo |
| `email` | VARCHAR(150) | UNIQUE NOT NULL | Correo de acceso |
| `password_hash` | VARCHAR(255) | NOT NULL | Hash bcrypt |
| `role` | user_role_enum | NOT NULL DEFAULT 'OPERATOR' | ADMIN / OPERATOR |
| `is_active` | BOOLEAN | NOT NULL DEFAULT TRUE | Estado del usuario |
| `created_at` | TIMESTAMPTZ | NOT NULL | Fecha de creación |
| `updated_at` | TIMESTAMPTZ | NOT NULL | Actualizado por trigger |

### `categories` — Categorías de Indumentaria
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SERIAL | PK | Identificador auto |
| `name` | VARCHAR(60) | UNIQUE NOT NULL | Camisetas, Shorts, Joggers… |
| `description` | TEXT | | Descripción de la línea |

### `products` — Catálogo Base de Prendas
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SERIAL | PK | Identificador auto |
| `category_id` | INT | FK → categories | Categoría asociada |
| `name` | VARCHAR(120) | NOT NULL | Nombre de la prenda |
| `base_price` | NUMERIC(10,2) | CHECK ≥ 0 | Precio en Soles (PEN) |
| `image_url` | VARCHAR(512) | | URL de la fotografía |
| `is_active` | BOOLEAN | NOT NULL DEFAULT TRUE | Disponible para venta |
| `updated_at` | TIMESTAMPTZ | NOT NULL | Actualizado por trigger |

### `product_variants` — Inventario por Talla y Color
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SERIAL | PK | Identificador auto |
| `product_id` | INT | FK → products | Prenda base |
| `size_id` | SMALLINT | FK → sizes | Talla de la variante |
| `color_id` | SMALLINT | FK → colors | Color de la variante |
| `sku` | VARCHAR(60) | UNIQUE NOT NULL | Código único (LF-TSH-BLK-M) |
| `stock` | INT | CHECK ≥ 0 | Unidades disponibles |
| `alert_threshold` | INT | CHECK ≥ 0 DEFAULT 3 | Umbral de alerta de stock |
| `updated_at` | TIMESTAMPTZ | NOT NULL | Actualizado por trigger |

### `clients` — Clientes
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SERIAL | PK | Identificador auto |
| `full_name` | VARCHAR(120) | NOT NULL | Nombre y apellido |
| `phone` | VARCHAR(20) | UNIQUE NOT NULL | WhatsApp de contacto |
| `address` | TEXT | NOT NULL | Dirección de entrega |
| `district_id` | SMALLINT | FK → districts | Distrito de entrega |
| `reference` | TEXT | | Referencia para el repartidor |
| `updated_at` | TIMESTAMPTZ | NOT NULL | Actualizado por trigger |

### `orders` — Cabecera de Pedidos
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SERIAL | PK | Identificador interno |
| `order_number` | VARCHAR(30) | UNIQUE NOT NULL | Código visible: ORD-2026-001 |
| `client_id` | INT | FK → clients | Cliente comprador |
| `user_id` | INT | FK → users | Operador que registró |
| `payment_method_id` | SMALLINT | FK → payment_methods | Método de pago |
| `status` | order_status_enum | NOT NULL DEFAULT 'RECIBIDO' | Estado del pedido |
| `subtotal` | NUMERIC(10,2) | CHECK ≥ 0 | Suma de ítems |
| `shipping_cost` | NUMERIC(10,2) | CHECK ≥ 0 | Costo de envío |
| `total_amount` | NUMERIC(10,2) | CHECK = subtotal + shipping | Total a cobrar |
| `notes` | TEXT | | Indicaciones especiales |
| `updated_at` | TIMESTAMPTZ | NOT NULL | Actualizado por trigger |

### `order_items` — Detalle de Ítems
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SERIAL | PK | Identificador auto |
| `order_id` | INT | FK → orders CASCADE | Pedido padre |
| `variant_id` | INT | FK → product_variants | Variante comprada |
| `quantity` | INT | CHECK > 0 | Unidades pedidas |
| `unit_price` | NUMERIC(10,2) | CHECK ≥ 0 | Precio al momento de la venta |
| `subtotal` | NUMERIC(10,2) | CHECK = qty × price | Subtotal del ítem |

### `order_status_history` — Historial de Auditoría
| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | SERIAL | PK | Identificador auto |
| `order_id` | INT | FK → orders CASCADE | Pedido auditado |
| `user_id` | INT | FK → users SET NULL | Operador que realizó el cambio |
| `previous_status` | order_status_enum | | Estado anterior |
| `new_status` | order_status_enum | NOT NULL | Nuevo estado asignado |
| `changed_at` | TIMESTAMPTZ | NOT NULL | Momento exacto del cambio |
| `comments` | TEXT | | Observaciones del operador |

---

## 6. Triggers

| Trigger | Tabla | Evento | Función |
|---|---|---|---|
| `trg_users_updated_at` | users | BEFORE UPDATE | `fn_set_updated_at()` |
| `trg_products_updated_at` | products | BEFORE UPDATE | `fn_set_updated_at()` |
| `trg_product_variants_updated_at` | product_variants | BEFORE UPDATE | `fn_set_updated_at()` |
| `trg_clients_updated_at` | clients | BEFORE UPDATE | `fn_set_updated_at()` |
| `trg_orders_updated_at` | orders | BEFORE UPDATE | `fn_set_updated_at()` |
| `trg_decrement_stock_on_order` | order_items | AFTER INSERT | `fn_decrement_stock()` |

---

## 7. Índices de Optimización

```sql
-- Consultas de listado y filtro por estado/fecha
idx_orders_status         ON orders(status)
idx_orders_created_at     ON orders(created_at DESC)
idx_orders_client         ON orders(client_id)
idx_orders_payment        ON orders(payment_method_id)

-- Búsqueda de variantes e inventario
idx_variants_product      ON product_variants(product_id)
idx_variants_sku          ON product_variants(sku)
idx_variants_stock        ON product_variants(stock) WHERE stock <= alert_threshold

-- Búsqueda de clientes
idx_clients_phone         ON clients(phone)
idx_clients_district      ON clients(district_id)

-- Consultas de detalle e historial
idx_order_items_order     ON order_items(order_id)
idx_order_items_variant   ON order_items(variant_id)
idx_status_history_order  ON order_status_history(order_id)
idx_status_history_date   ON order_status_history(changed_at DESC)
idx_products_category     ON products(category_id) WHERE is_active = TRUE
```

---

## 8. Vistas Operativas

### `vw_low_stock_alert`
Prendas con `stock <= alert_threshold`. Alimenta el dashboard de alertas.

### `vw_orders_summary`
Vista desnormalizada con datos de cliente, distrito, método de pago y estado
para consultas de listado de pedidos y reportes.

---

## 9. Datos Iniciales (Seeds)

| Tabla | Registros |
|---|---|
| sizes | 6 (S, M, L, XL, XXL, UNICA) |
| colors | 10 (Negro Lavado, Blanco Crudo, Gris Jaspe…) |
| districts | 10 (distritos de Lima) |
| payment_methods | 5 (Yape, Plin, Transferencia, Contraentrega, Efectivo) |
| users | 2 (Admin + Operator) |
| categories | 5 (Camisetas, Shorts, Joggers, Tirantes, Accesorios) |
| products | 8 prendas deportivas |
| product_variants | 23 variantes con SKU único |
| clients | 7 clientes |
| orders | 6 pedidos con historial de estados |

---

## 10. Levantar con Docker

```bash
# Clonar e ingresar al proyecto
cd leofit-pedidos-sistema

# Primera vez — limpia y levanta
docker-compose down -v
docker-compose up -d

# Ver logs de inicialización
docker logs -f leofit_postgres

# Verificar la BD
psql -h 127.0.0.1 -p 5432 -U postgres -d leofit_db -f verify_leofit.sql
```

Servicios disponibles:

| Servicio | Puerto | URL |
|---|---|---|
| PostgreSQL | 5432 | `postgresql://postgres:***@localhost:5432/leofit_db` |
| PgBouncer | 6432 | `postgresql://postgres:***@localhost:6432/leofit_db` |
| Adminer | 8080 | http://localhost:8080 |
| Backend API | 4000 | http://localhost:4000 |
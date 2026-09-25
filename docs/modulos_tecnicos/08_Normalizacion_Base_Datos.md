# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# INFORME FORMAL DE NORMALIZACIÓN DE BASE DE DATOS RELACIONAL
## FORMAS NORMALES: 1FN, 2FN, 3FN Y FORMA NORMAL DE BOYCE-CODD (BCNF)
### PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

## 1. CONTROL DEL DOCUMENTO

* **Institución:** Universidad Tecnológica del Perú (UTP)
* **Curso:** Curso Integrador II: Software (100000S12F)
* **Proyecto:** Sistema de Gestión de Pedidos & Inventario LeoFit
* **Equipo Responsable (Grupo 01):**
  1. **Loayza Rodriguez, Lady Luz** - Scrum Master
  2. **Cárdenas Fernández, Víctor Leandro** - Product Owner / Diseñador de Base de Datos
  3. **Roman Delgado, Harley Anthony** - Front-End Lead
  4. **Dávila Morales, Jim Alessandro** - QA / Testing
  5. **Rojas Sanchez, Daniel Enrique** - Analista de Negocio
* **Versión:** 1.0.0 (Formal Académica)

---

## 2. PROCESO PASO A PASO DE NORMALIZACIÓN

### 2.1. Forma No Normalizada (UNF) - Estructura Inicial Desnormalizada
El registro inicial en los cuadernos de notas de LeoFit agrupaba de forma redundante y no atómica los datos del cliente, múltiples prendas en una sola celda y subtotales mezclados:

$$\text{REGISTRO\_PEDIDO}(\underline{\text{ID\_Pedido}}, \text{Fecha}, \text{Cliente\_Nombre}, \text{Cliente\_Tel}, \text{Direccion}, \{\text{Cod\_Prenda}, \text{Prenda}, \text{Talla}, \text{Color}, \text{Cant}, \text{PrecioUnit}\}, \text{Flete}, \text{Total})$$

---

### 2.2. Primera Forma Normal (1FN) - Atomicidad y Eliminación de Grupos Repetitivos
* **Regla Aplicada:** Se eliminan los grupos repetitivos extrayendo el detalle de productos a una entidad separada y se garantiza que todos los atributos contengan valores atómicos individuales.
* **Entidades Resultantes en 1FN:**
  - $\text{PEDIDOS\_1FN}(\underline{\text{id\_pedido}}, \text{fecha}, \text{cliente\_nombre}, \text{cliente\_telefono}, \text{cliente\_direccion}, \text{costo\_envio}, \text{monto\_total})$
  - $\text{DETALLE\_PEDIDO\_1FN}(\underline{\text{id\_pedido}, \text{id\_producto}}, \text{nombre\_producto}, \text{talla}, \text{color}, \text{cantidad}, \text{precio\_unitario}, \text{subtotal})$

---

### 2.3. Segunda Forma Normal (2FN) - Eliminación de Dependencias Funcionales Parciales
* **Regla Aplicada:** Todos los atributos que no forman parte de la clave primaria deben depender funcionalmente de la totalidad de la clave primaria compuesta, no de una parte de ella.
* **Entidades Resultantes en 2FN:**
  - $\text{PRODUCTOS}(\underline{\text{id\_producto}}, \text{nombre}, \text{categoria}, \text{precio}, \text{stock}, \text{talla}, \text{color})$
  - $\text{DETALLE\_PEDIDOS}(\underline{\text{id\_pedido}, \text{id\_producto}}, \text{cantidad}, \text{precio\_unitario})$
  - $\text{PEDIDOS}(\underline{\text{id\_pedido}}, \text{fecha}, \text{id\_cliente}, \text{costo\_envio}, \text{total}, \text{id\_estado})$

---

### 2.4. Tercera Forma Normal (3FN) y Forma Normal de Boyce-Codd (BCNF)
* **Condición 3FN:** Estar en 2FN y eliminar dependencias transitivas donde atributos no clave determinen a otros atributos no clave.
* **Condición BCNF (Boyce-Codd Normal Form):** Una relación está en BCNF si y solo si para toda Dependencia Funcional no trivial $X \to Y$, el determinante $X$ es una **superclave** (clave primaria o clave candidata).
* **Descomposición BCNF Aplicada a LeoFit:**
  1. **Aislamiento de Dominios Cerrados:** `talla`, `color`, `distrito` y `metodo_pago` se extrajeron a tablas maestras (`sizes`, `colors`, `districts`, `payment_methods`), evitando redundancia semántica y anomalías de modificación.
  2. **Descomposición del Inventario Multivariante:** La tupla `{producto, talla, color}` determina unívocamente el `sku` y el `stock`. Ambas determinantes ($\{ \text{product\_id}, \text{size\_id}, \text{color\_id} \}$ y $\text{sku}$) son superclaves, cumpliendo estrictamente BCNF en `product_variants`.
  3. **Trazabilidad Inmutable:** Se independiza `order_status_history` para auditoría temporal sin violar la unicidad de `orders`.

* **Esquema Relacional DDL Oficial en PostgreSQL 16 (BCNF):**

```sql
-- Tipos ENUM para dominios cerrados
CREATE TYPE user_role_enum    AS ENUM ('ADMIN', 'OPERATOR');
CREATE TYPE order_status_enum AS ENUM ('RECIBIDO', 'PREPARACION', 'EN_CAMINO', 'ENTREGADO', 'CANCELADO');

-- 1. Catálogo Maestro de Tallas (sizes)
CREATE TABLE sizes (
    id    SMALLSERIAL PRIMARY KEY,
    code  VARCHAR(10) NOT NULL UNIQUE,
    label VARCHAR(30) NOT NULL
);

-- 2. Catálogo de Colores (colors)
CREATE TABLE colors (
    id   SMALLSERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL UNIQUE,
    hex  CHAR(7)
);

-- 3. Distritos de Reparto Geográfico (districts)
CREATE TABLE districts (
    id   SMALLSERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE
);

-- 4. Métodos de Pago Disponibles (payment_methods)
CREATE TABLE payment_methods (
    id   SMALLSERIAL PRIMARY KEY,
    code VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(60) NOT NULL
);

-- 5. Usuarios Administrativos y Operadores (users)
CREATE TABLE users (
    id            SERIAL         PRIMARY KEY,
    name          VARCHAR(100)   NOT NULL,
    email         VARCHAR(150)   NOT NULL UNIQUE,
    password_hash VARCHAR(255)   NOT NULL,
    role          user_role_enum NOT NULL DEFAULT 'OPERATOR',
    is_active     BOOLEAN        NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMPTZ    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 6. Categorías de Indumentaria (categories)
CREATE TABLE categories (
    id          SERIAL      PRIMARY KEY,
    name        VARCHAR(60) NOT NULL UNIQUE,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 7. Catálogo Base de Prendas (products)
CREATE TABLE products (
    id          SERIAL        PRIMARY KEY,
    category_id INT           NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    name        VARCHAR(120)  NOT NULL,
    description TEXT,
    base_price  NUMERIC(10,2) NOT NULL CHECK (base_price >= 0),
    image_url   VARCHAR(512),
    is_active   BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_product_name_category UNIQUE (category_id, name)
);

-- 8. Variantes e Inventario por Talla y Color (product_variants - BCNF)
CREATE TABLE product_variants (
    id              SERIAL      PRIMARY KEY,
    product_id      INT         NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    size_id         SMALLINT    NOT NULL REFERENCES sizes(id)    ON DELETE RESTRICT,
    color_id        SMALLINT    NOT NULL REFERENCES colors(id)   ON DELETE RESTRICT,
    sku             VARCHAR(60) NOT NULL UNIQUE,
    stock           INT         NOT NULL DEFAULT 0 CHECK (stock >= 0),
    alert_threshold INT         NOT NULL DEFAULT 3 CHECK (alert_threshold >= 0),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_variant UNIQUE (product_id, size_id, color_id)
);

-- 9. Clientes Registrados (clients)
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

-- 10. Cabecera de Pedidos (orders)
CREATE TABLE orders (
    id                SERIAL            PRIMARY KEY,
    order_number      VARCHAR(30)       NOT NULL UNIQUE,
    client_id         INT               NOT NULL REFERENCES clients(id)         ON DELETE RESTRICT,
    user_id           INT                        REFERENCES users(id)           ON DELETE SET NULL,
    payment_method_id SMALLINT          NOT NULL REFERENCES payment_methods(id) ON DELETE RESTRICT,
    status            order_status_enum NOT NULL DEFAULT 'RECIBIDO',
    subtotal          NUMERIC(10,2)     NOT NULL DEFAULT 0.00 CHECK (subtotal      >= 0),
    shipping_cost     NUMERIC(10,2)     NOT NULL DEFAULT 0.00 CHECK (shipping_cost >= 0),
    total_amount      NUMERIC(10,2)     NOT NULL DEFAULT 0.00 CHECK (total_amount  >= 0),
    notes             TEXT,
    created_at        TIMESTAMPTZ       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMPTZ       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_total CHECK (total_amount = subtotal + shipping_cost)
);

-- 11. Detalle de Ítems del Pedido (order_items)
CREATE TABLE order_items (
    id         SERIAL        PRIMARY KEY,
    order_id   INT           NOT NULL REFERENCES orders(id)           ON DELETE CASCADE,
    variant_id INT           NOT NULL REFERENCES product_variants(id) ON DELETE RESTRICT,
    quantity   INT           NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    subtotal   NUMERIC(10,2) NOT NULL CHECK (subtotal   >= 0),
    CONSTRAINT chk_item_subtotal CHECK (subtotal = quantity * unit_price),
    CONSTRAINT uq_order_variant UNIQUE (order_id, variant_id)
);

-- 12. Historial de Auditoría de Estados (order_status_history)
CREATE TABLE order_status_history (
    id              SERIAL            PRIMARY KEY,
    order_id        INT               NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    user_id         INT                        REFERENCES users(id)  ON DELETE SET NULL,
    previous_status order_status_enum,
    new_status      order_status_enum NOT NULL,
    changed_at      TIMESTAMPTZ       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comments        TEXT
);
```

---

## 3. DIAGRAMAS ARQUITECTURALES DE BASE DE DATOS

* 📐 **Diagrama de Modelo Lógico (DER Conceptual):** [`diagrams/12_Modelo_Logico_BD.png`](../diagrams/12_Modelo_Logico_BD.png)
* 🗄️ **Diagrama de Modelo Físico (DDL Relacional 3FN/BCNF):** [`diagrams/13_Modelo_Fisico_BD.png`](../diagrams/13_Modelo_Fisico_BD.png)
* 📊 **Diagrama de Entidades Complementario:** [`diagrams/14_Diagrama_DB.png`](../diagrams/14_Diagrama_DB.png)

---

## 4. CONCLUSIÓN TÉCNICA
El esquema normalizado en **BCNF** garantiza:
1. **Cero redundancia de datos** en catálogo, pedidos y clientes.
2. **Integridad referencial total** mediante claves primarias y foráneas con restricciones `CHECK`.
3. **Alto rendimiento en consultas transaccionales** con índices sobre claves foráneas y fechas de creación.

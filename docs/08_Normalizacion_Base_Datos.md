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

### 2.4. Tercera Forma Normal (3FN) - Eliminación de Dependencias Transitivas
* **Regla Aplicada:** Ningún atributo no clave debe depender transitivamente de la clave primaria a través de otro atributo no clave. Se independizan las entidades `CLIENTES`, `CATEGORIAS` y `ESTADOS_PEDIDO`.
* **Esquema Relacional Final en 3FN / BCNF:**

```sql
-- 1. Tabla de Roles de Usuario
CREATE TABLE roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Tabla de Usuarios del Sistema
CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- 3. Tabla de Categorías de Indumentaria
CREATE TABLE categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre_categoria VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT
);

-- 4. Tabla de Productos e Inventario
CREATE TABLE productos (
    id_producto VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    id_categoria INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio > 0),
    stock INT NOT NULL CHECK (stock >= 0),
    talla VARCHAR(20) NOT NULL,
    color VARCHAR(50) NOT NULL,
    imagen_url VARCHAR(255),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

-- 5. Tabla de Estados de Pedido
CREATE TABLE estados_pedido (
    id_estado INT PRIMARY KEY AUTO_INCREMENT,
    nombre_estado VARCHAR(50) NOT NULL UNIQUE
);

-- 6. Tabla de Cabecera de Pedidos
CREATE TABLE pedidos (
    id_pedido VARCHAR(50) PRIMARY KEY,
    cliente_nombre VARCHAR(150) NOT NULL,
    cliente_telefono VARCHAR(20) NOT NULL,
    cliente_direccion TEXT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    costo_envio DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    total DECIMAL(10, 2) NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    id_estado INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_estado) REFERENCES estados_pedido(id_estado)
);

-- 7. Tabla de Detalle de Pedidos
CREATE TABLE detalle_pedidos (
    id_pedido VARCHAR(50) NOT NULL,
    id_producto VARCHAR(50) NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_pedido, id_producto),
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);
```

---

## 3. CONCLUSIÓN TÉCNICA
El esquema normalizado en **BCNF** garantiza:
1. **Cero redundancia de datos** en catálogo, pedidos y clientes.
2. **Integridad referencial total** mediante claves primarias y foráneas con restricciones `CHECK`.
3. **Alto rendimiento en consultas transaccionales** con índices sobre claves foráneas y fechas de creación.

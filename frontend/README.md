# Módulo Frontend - Leofit Solutions

Este directorio contiene el diseño de interfaz de usuario (UI), la experiencia de usuario (UX) y el código fuente de la aplicación cliente para el **Sistema de Gestión de Pedidos de Leofit**.

---

## 1. Decisiones de Diseño UI/UX

La interfaz de usuario ha sido concebida específicamente para satisfacer las necesidades operativas de Víctor (dueño de Leofit), quien administra el negocio principalmente desde su teléfono móvil mientras realiza tareas en el almacén o atiende clientes.

### Principios de Diseño:
* **Enfoque Mobile-First & PWA:** Totalmente optimizado para pantallas táctiles de smartphones (botones de fácil pulsación con área mínima de 44x44px, formularios ágiles) sin perder ergonomía en pantallas de escritorio.
* **Cero Fricción en Registro:** Crear un pedido requiere menos de 3 pasos: ingresar cliente ➔ seleccionar prendas con tallas ➔ confirmar con un clic.
* **Trazabilidad Visual por Código de Color:** Los estados de los pedidos están codificados con colores universales para identificar prioridades al instante.
* **Heurísticas de Usabilidad:** Visibilidad del estado del sistema en todo momento, consistencia en formularios y prevención de errores mediante validaciones inline.

---

## 2. Sistema de Diseño & Tokens Visuales

### Paleta de Colores:
* **Fondo Principal / Dark Sidebar:** `#0F172A` (Slate 900) - Elegancia, enfoque y modernidad.
* **Color Primario de Marca:** `#0284C7` (Sky Blue) - Confianza, dinamismo deportivo y claridad.
* **Superficies y Tarjetas:** `#FFFFFF` y `#F8FAFC` (Slate 50) con bordes suaves `#E2E8F0`.
* **Estados de Pedido:**
  * `Recibido`: Azul `#3B82F6` (Pendiente de atención).
  * `En Preparación`: Ámbar `#F59E0B` (En empaque en almacén).
  * `En Camino`: Púrpura `#8B5CF6` (Con el delivery motorizado).
  * `Entregado`: Verde Esmeralda `#10B981` (Venta completada).
  * `Cancelado / Sin Stock`: Rojo `#EF4444` (Alerta crítica).

### Tipografía:
* Familia tipográfica: `Inter`, `Roboto`, `sans-serif`.
* Jerarquía clara con pesos `400` (Regular), `600` (Semi-bold) y `700` (Bold) para lectura rápida de montos y códigos de pedido.

---

## 3. Mockups y Vistas Diseñadas

En la carpeta [`mockups/`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/frontend/mockups) se encuentran las pantallas clave del sistema:

| Mockup | Archivo | Descripción |
|:---|:---|:---|
| **01. Login** | [`01_Login.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/frontend/mockups/01_Login.png) | Pantalla de acceso autenticado para el administrador con diseño oscuro y moderno. |
| **02. Dashboard** | [`02_Dashboard.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/frontend/mockups/02_Dashboard.png) | Panel de control con métricas clave (ventas del día, pedidos activos, alertas de stock crítico). |
| **03. Listado de Pedidos** | [`03_Listado_Pedidos.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/frontend/mockups/03_Listado_Pedidos.png) | Tabla interactiva con filtros rápidos por estado, buscador predictivo y detalles de entrega. |
| **04. Formulario de Pedido** | [`04_Formulario_Pedido.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/frontend/mockups/04_Formulario_Pedido.png) | Formulario optimizado de captura de pedido con selector de prendas, cálculo automático de total y delivery. |
| **05. Gestión de Productos** | [`05_Gestion_Productos.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/frontend/mockups/05_Gestion_Productos.png) | Catálogo de prendas deportivas con tallas, colores, precios y badges de alerta de stock bajo. |

---

## 4. Stack Tecnológico Sugerido para Frontend

* **Framework:** React 18+ con Vite (compilación ultrarrápida y estándar de la industria).
* **Enrutamiento:** React Router DOM v6+.
* **Gestión de Estado:** Zustand o Context API para el estado global del carrito de pedidos y sesión.
* **Peticiones HTTP:** Axios con interceptores para inyección automática del token JWT.
* **Componentes / Estilos:** Vanilla CSS / CSS Modules o Tailwind CSS para máxima velocidad de desarrollo y diseño responsive.

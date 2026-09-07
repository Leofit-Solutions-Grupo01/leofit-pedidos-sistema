# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# ESPECIFICACIÓN DE REQUERIMIENTOS DE SOFTWARE (ERS)
## ESTÁNDAR IEEE STD 830-1998
### PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

## 1. INTRODUCCIÓN

### 1.1. Propósito del Documento
El presente documento especifica de manera formal y estructurada los Requerimientos Funcionales (RF) y Requisitos No Funcionales (RNF) para el desarrollo del **Sistema de Gestión de Pedidos e Inventario de LeoFit**, siguiendo las directrices del estándar internacional **IEEE Std 830-1998** y los lineamientos del Curso Integrador II: Software de la Universidad Tecnológica del Perú.

### 1.2. Alcance del Sistema
El software es una **Progressive Web App (PWA)** que automatiza la captura, validación, registro, costeo y seguimiento de pedidos de indumentaria deportiva, proporcionando sincronización en tiempo real con el inventario y permitiendo la administración operativa desde cualquier dispositivo móvil o de escritorio.

### 1.3. Objetivos del Sistema
* Reducir el tiempo promedio de atención y toma de pedidos de 25 minutos a $\le 3$ minutos.
* Eliminar en un 100% las pérdidas de pedidos y sobreventas originadas por anotaciones manuscritas.
* Proporcionar trazabilidad total del ciclo de vida de la orden a través de 5 estados operativos normalizados.

---

## 2. DESCRIPCIÓN GENERAL

### 2.1. Perspectiva del Producto
El sistema opera de forma autónoma e independiente, interactuando con clientes y administradores mediante una arquitectura web modular basada en componentes y desacoplada en capas (Presentación, Estado, Lógica de Negocio y Persistencia).

### 2.2. Características de los Usuarios
* **Cliente Deportivo:** Usuario final sin formación técnica especializada que navega por el catálogo, selecciona artículos y formaliza órdenes de compra.
* **Administrador del Sistema (Víctor Raúl Cárdenas):** Responsable de la gestión de existencias, actualización de precios, cambio de estados de pedidos y visualización de métricas en el panel.

### 2.3. Restricciones de Diseño e Implementación
* Uso obligatorio de estándares web modernos (HTML5, CSS3, ECMAScript 2022+).
* Tipado estricto mediante TypeScript 5+.
* Rendimiento optimizado bajo métricas Core Web Vitals (FCP $< 0.5$ s, LCP $< 1.2$ s, bundle JS $< 80$ kB gzipped).
* Compatibilidad multi-navegador en Google Chrome, Microsoft Edge, Mozilla Firefox y Safari Mobile.

---

## 3. MATRIZ DE REQUISITOS FUNCIONALES (RF-001 A RF-012)

| ID | Nombre del Requisito | Actor Principal | Descripción Funcional | Prioridad | Criterios de Aceptación | Módulo | Estado |
|:---|:---|:---|:---|:---:|:---|:---|:---:|
| **RF-001** | Catálogo Interactivo | Cliente / Admin | El sistema debe mostrar el catálogo de prendas deportivas con fotografía HD, nombre, precio, tallas disponibles y stock en existencias. | Alta | Carga reactiva de productos con formato de moneda nacional (S/) y badges de disponibilidad. | Catálogo | Implementado |
| **RF-002** | Búsqueda y Filtrado Dinámico | Cliente / Admin | El sistema debe permitir filtrar productos por categoría, talla y texto predictivo en tiempo real sin recargar la página. | Alta | Respuesta del filtro en menos de 100 ms ante cualquier interacción del usuario. | Catálogo | Implementado |
| **RF-003** | Carrito de Compras Reactivo | Cliente / Admin | El sistema debe permitir añadir artículos, modificar cantidades y eliminar prendas, recalculando el subtotal al instante. | Alta | Persistencia del estado del carrito durante la sesión y actualización reactiva de montos. | Carrito | Implementado |
| **RF-004** | Validación Automática de Stock | Sistema | El sistema debe impedir la selección o compra de cantidades que excedan las existencias físicas registradas. | Alta | Deshabilitación de botones de incremento y presentación de alerta contextual de stock agotado. | Inventario | Implementado |
| **RF-005** | Formulario de Registro de Orden | Cliente / Admin | El sistema debe capturar los datos de entrega: nombre completo, teléfono móvil, dirección de envío y método de pago. | Alta | Validación estricta de campos obligatorios y generación de identificador único correlativo (`PED-2026-XXXX`). | Pedidos | Implementado |
| **RF-006** | Liquidación de Flete y Totales | Sistema | El sistema debe calcular el costo de despacho según la zona geográfica seleccionada y consolidar el monto total a pagar. | Media | Desglose aritmético exacto de subtotal de prendas, tarifa de flete y total de la orden. | Pedidos | Implementado |
| **RF-007** | Trazabilidad y Control de Estados | Administrador | El sistema debe permitir la actualización de estados de la orden (`Recibido`, `En Preparación`, `En Camino`, `Entregado`, `Cancelado`). | Alta | Cambio de estado con un solo clic en la interfaz y registro de la marca de tiempo correspondiente. | Gestión | Implementado |
| **RF-008** | Bandeja de Gestión de Pedidos | Administrador | El sistema debe presentar la lista consolidada de pedidos con filtros por estado, cliente, fecha y rango de importes. | Alta | Visualización en tarjetas interactivas y tabla responsiva con badges de colores normalizados. | Gestión | Implementado |
| **RF-009** | Gestión de Existencias y Catálogo | Administrador | El sistema debe permitir la creación, modificación de precios, edición de tallas y ajuste de stock de productos. | Alta | Modal interactivo para actualización inmediata de existencias en el catálogo. | Inventario | Implementado |
| **RF-010** | Dashboard de Control Operativo | Administrador | El sistema debe mostrar tarjetas métricas con total de pedidos del día, importe bruto recaudado y prendas en nivel crítico ($< 5$ unid). | Media | Cálculo reactivo de totales de la jornada sin sobrecarga en la memoria del navegador. | Dashboard | Implementado |
| **RF-011** | Generación de Resumen para WhatsApp | Cliente / Admin | El sistema debe generar un mensaje de texto formateado con el resumen de la orden listo para compartir por mensajería. | Media | Formato limpio con ID de pedido, detalle de ítems, flete, total y datos de contacto del cliente. | Pedidos | Implementado |
| **RF-012** | Control de Acceso Administrativo | Administrador | El sistema debe proteger las rutas de gestión de inventario y configuración mediante credenciales de autenticación. | Alta | Validación segura de credenciales de administrador y persistencia de sesión controlada. | Seguridad | Implementado |

---

## 4. MATRIZ DE REQUISITOS NO FUNCIONALES (RNF-001 A RNF-010)

| ID | Categoría | Requisito No Funcional | Descripción Técnica | Métrica Verificable | Prioridad | Método de Validación | Estado |
|:---|:---|:---|:---|:---|:---:|:---|:---:|
| **RNF-001** | Usabilidad | Diseño Mobile-First | La interfaz debe ser altamente intuitiva y ergonómica en pantallas táctiles de smartphones. | Registro de orden completado en $\le 2$ minutos por usuarios no técnicos. | Alta | Prueba de usabilidad con 3 usuarios finales. | Validado |
| **RNF-002** | Rendimiento | Tiempo de Carga y Render | Las vistas y filtros del catálogo deben desplegarse de manera instantánea. | First Contentful Paint (FCP) $\le 0.5$ s y tiempo de respuesta P95 $< 100$ ms. | Alta | Auditoría con Google Lighthouse y Chrome DevTools. | Validado |
| **RNF-003** | Rendimiento (WPO) | Optimización de Paquete | El bundle compilado de producción debe ser minúsculo para operar en redes móviles lentas. | Bundle JS $\le 80$ kB gzipped y Bundle CSS $\le 10$ kB gzipped. | Alta | Análisis de compilación con Vite / Rollup bundle analyzer. | Validado |
| **RNF-004** | Disponibilidad | Operatividad Continua | La plataforma debe permanecer disponible y accesible en la nube de forma ininterrumpida. | Uptime mensual $\ge 99.5\%$ garantizado por CDN Serverless en el Edge. | Alta | Bitácora y monitoreo de disponibilidad en hosting. | Validado |
| **RNF-005** | Compatibilidad | Multi-Plataforma | El sistema debe operar con total fidelidad visual en todos los navegadores modernos. | 100% funcional en Google Chrome, Microsoft Edge, Firefox y Safari. | Media | Pruebas de compatibilidad cruzada en navegadores. | Validado |
| **RNF-006** | Mantenibilidad | Arquitectura Modular | El código fuente debe estar estructurado en capas desacopladas con tipado estricto. | 100% código TypeScript sin errores de compilación (`tsc --noEmit`). | Alta | Análisis estático de código y suite de linters. | Validado |
| **RNF-007** | Trazabilidad | Integridad de Transacciones | Toda orden debe conservar su historial y no puede ser eliminada físicamente sin registro. | Cada orden almacena identificador correlativo, fecha, hora y estado actual. | Alta | Verificación de esquemas de datos y persistencia. | Validado |
| **RNF-008** | Seguridad | Rutas Protegidas | Las opciones de edición de existencias deben estar restringidas a sesiones autenticadas. | Denegación inmediata de acceso ante solicitudes no autorizadas. | Alta | Pruebas de navegación a rutas administrativas sin sesión. | Validado |
| **RNF-009** | Confiabilidad | Suite de Pruebas Unitarias | La lógica de cálculo y consistencia de datos debe estar respaldada por pruebas automatizadas. | Cobertura de pruebas unitarias $\ge 80\%$ con 100% de tests aprobados. | Alta | Ejecución automatizada de `vitest run` en CI/CD. | Validado |
| **RNF-010** | Accesibilidad | Contraste y Tipografía | Textos, botones y componentes interactivos deben cumplir con estándares de legibilidad. | Cumplimiento estricto de directrices WCAG 2.1 nivel AA (contraste $\ge 4.5:1$). | Media | Auditoría con extensión Axe y Lighthouse Accessibility. | Validado |

---

## 5. MATRIZ DE TRAZABILIDAD (REQUISITOS VS HISTORIAS DE USUARIO)

| Requisito Funcional | Historia de Usuario Vinculada | Épica Asociada | Módulo de Software |
|:---|:---:|:---:|:---|
| **RF-001, RF-002** | HU-001 (Filtrado de Catálogo) | EP-01 | `src/pages/Dashboard.tsx` |
| **RF-003, RF-004** | HU-002 (Carrito de Compras) | EP-02 | `src/context/AppContext.tsx` |
| **RF-005, RF-006, RF-011** | HU-003 (Registro de Pedidos) | EP-02 | `src/pages/PedidoForm.tsx` |
| **RF-007, RF-008** | HU-004 (Control de Estados) | EP-03 | `src/pages/PedidosLista.tsx` |
| **RF-009** | HU-006 (Gestión de Inventario) | EP-01 | `src/pages/ProductosGestion.tsx` |
| **RF-010** | HU-005 (Métricas de Dashboard) | EP-04 | `src/pages/Dashboard.tsx` |
| **RF-012** | HU-007 (Seguridad y Acceso) | EP-03 | `src/pages/Login.tsx` |

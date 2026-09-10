# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# FICHA DE IDENTIFICACIÓN Y MAPEO INICIAL DE EMPRESA Y PROBLEMA (SEMANA 1)
## PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

### 1. DATOS DEL EQUIPO DE TRABAJO (GRUPO 01)

| N° | Apellidos y Nombres | Rol en el Proyecto | Responsabilidad Técnica Principal |
|:---:|:---|:---|:---|
| 1 | **Loayza Rodriguez, Lady Luz** | Scrum Master | Coordinación general, facilitación ágil y diseño UX/UI. |
| 2 | **Cárdenas Fernández, Víctor Leandro** | Product Owner | Definición de requerimientos, arquitectura Back-End y Base de Datos. |
| 3 | **Roman Delgado, Harley Anthony** | Front-End Lead | Desarrollo de interfaz PWA, componentes React y optimización WPO. |
| 4 | **Dávila Morales, Jim Alessandro** | QA / DevOps | Automatización de pruebas unitarias, CI/CD y aseguramiento de calidad. |
| 5 | **Rojas Sanchez, Daniel Enrique** | Analista de Negocio | Levantamiento de requisitos, modelado de procesos y documentación técnica. |

---

### 2. IDENTIFICACIÓN DE LA ORGANIZACIÓN

* **Nombre Comercial:** LeoFit Indumentaria & Nutrición Deportiva.
* **Rubro Comercial:** Comercialización minorista de indumentaria deportiva (conjuntos térmicos, lycras de compresión, camisetas dry-fit, fajas deportivas) y accesorios de entrenamiento.
* **Ubicación Geográfica:** Lima Metropolitana, Perú.
* **Modelo de Operación:** Ventas directas al consumidor (B2C) en Lima y despachos a provincias mediante agencias de encomienda.
* **Justificación de la Selección:** LeoFit es un emprendimiento comercial independiente en fase de expansión que gestiona sus ventas de forma reactiva y no estandarizada a través de redes sociales (Facebook y WhatsApp). Representa un caso de estudio real, accesible y de alta pertinencia para la implementación de una solución de software orientada a la eficiencia operativa.

---

### 3. CONTACTO Y EVIDENCIA DE ACCESO AL STAKEHOLDER

* **Representante y Contacto Principal:** Víctor Raúl Cárdenas Ramírez.
* **Cargo:** Fundador, Gerente General y Operador Principal.
* **Disponibilidad y Compromiso:** El representante ha suscrito actas de conformidad y se encuentra plenamente comprometido para participar en las sesiones semanales de Sprint Review y validación de prototipos.
* **Evidencias Disponibles:** Registros históricos en cuadernos físicos de notas, capturas anonimizadas de conversaciones de WhatsApp comercial y catálogo fotográfico actual de prendas.

---

### 4. MAPEO INICIAL DEL PROCESO Y DEFINICIÓN DEL PROBLEMA

* **Proceso Crítico Seleccionado:** Recepción, validación de existencias, registro y despacho de pedidos.
* **Definición Formal del Problema:**
  "La gestión manual, descentralizada y reactiva de los pedidos comerciales a través de canales de mensajería informal (WhatsApp y llamadas telefónicas) en LeoFit ocasiona cuellos de botella operativos, demoras de hasta 25 minutos en la atención por cliente, quiebres de inventario no advertidos y errores en las direcciones de despacho, impactando negativamente en la rentabilidad y en la satisfacción del cliente."

---

### 5. ACTORES Y MATRIZ DE NECESIDADES

| Actor / Usuario | Rol en el Negocio | Necesidad Principal | Dificultad Actual | Validación Propuesta |
|:---|:---|:---|:---|:---|
| **Víctor Raúl Cárdenas** | Administrador / Dueño | Centralizar pedidos, controlar stock en tiempo real y actualizar estados de entrega con un clic. | Sobrecarga de trabajo operativo, errores de registro manuscrito y falta de trazabilidad. | Pruebas de usabilidad del panel administrativo y flujo de pedidos en vivo. |
| **Cliente Deportivo** | Comprador final | Explorar prendas con tallas y precios actualizados, calcular totales y confirmar su orden en $< 2$ minutos. | Respuestas demoradas por chat, falta de catálogo ordenado y desconocimiento del estado de entrega. | Tasa de conversión de pedidos y reducción del tiempo de espera. |
| **Equipo de Proyecto** | Desarrolladores UTP | Requerimientos técnicos claros, acceso a datos sintéticos y retroalimentación iterativa. | Tiempo limitado del stakeholder por su dedicación a la operación diaria. | Sesiones semanales de Sprint Review estructuradas de 30 minutos. |

---

### 6. HIPÓTESIS DE SOLUCIÓN Y ALCANCE DEL MVP

* **Tipo de Solución:** Sistema Web Progresivo (PWA) responsivo, accesible desde navegadores móviles y de escritorio sin requerir descargas pesadas desde tiendas de aplicaciones.
* **Cinco Funcionalidades Principales del MVP:**
  1. *Catálogo Interactivo:* Visualización reactiva con filtros dinámicos por categoría, talla, color y precio.
  2. *Carrito de Compras y Control de Stock:* Cálculo automático de importes y bloqueo de pedidos que excedan existencias reales.
  3. *Toma y Registro Formal de Pedidos:* Formulario validado con generación automática de código identificador único de orden.
  4. *Módulo de Trazabilidad de Estados:* Cambio de estados operativo (`Recibido`, `En Preparación`, `En Camino`, `Entregado`, `Cancelado`).
  5. *Dashboard Administrativo:* Indicadores cuantitativos en tiempo real de ventas de la jornada, pedidos pendientes y alertas de stock bajo.

---

### 7. FACTIBILIDAD Y EVALUACIÓN DE VIABILIDAD

| Criterio de Viabilidad | Evaluación | Sustentación Técnica |
|:---|:---:|:---|
| **Acceso a Experto del Proceso** | Sí | Contacto directo y comprometido con el dueño del negocio. |
| **Evidencia Comprobable** | Sí | Registros físicos, capturas de chat y validación presencial. |
| **Alcance Acotado** | Sí | Enfocado estrictamente en la gestión de pedidos e inventario. |
| **Factibilidad Técnica** | Sí | Pila tecnológica madura y probada (React 18, TypeScript, Vite, Tailwind CSS y Node.js). |
| **Protección de Datos** | Sí | Uso de datos sintéticos y homologación conforme a la Ley de Protección de Datos Personales. |
| **Despliegue Operativo** | Sí | Despliegue automatizado en CDN Serverless (GitHub Pages / Vercel) con alta disponibilidad. |

---

### 8. PITCH TÉCNICO DEL PROYECTO

"LeoFit es un negocio peruano de indumentaria deportiva que gestiona sus ventas manualmente por WhatsApp y notas en papel, generando demoras de 25 minutos por orden y riesgos de sobreventa. Desarrollamos una Progressive Web App (PWA) de ultra-bajo peso que permite a los clientes confirmar pedidos en 2 minutos con stock en tiempo real y brinda al administrador control integral del inventario y trazabilidad de despachos con un solo clic."

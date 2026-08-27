# GLOSARIO DE TÉRMINOS
## Proyecto: Sistema de Gestión de Pedidos - Leofit

El presente glosario define los conceptos clave de negocio y los términos tecnológicos utilizados a lo largo del ciclo de vida del proyecto.

---

## 1. Términos del Negocio y Dominio

* **AS-IS (Estado Actual):** Representación del flujo de trabajo y procesos operativos tal como funcionan actualmente en Leofit (proceso manual mediante WhatsApp, llamadas y notas en cuaderno).
* **TO-BE (Estado Futuro):** Representación del proceso optimizado y digitalizado con la implementación del nuevo sistema web.
* **Cuello de Botella:** Punto de congestión en el proceso comercial (específicamente la atención individual de mensajes y la comprobación física de existencias) que limita la capacidad de atender más clientes.
* **Inventario / Stock Disponible:** Cantidad física exacta de unidades de prendas deportivas disponibles para la venta inmediata, discriminada por modelo, talla y color.
* **Lead Time (Tiempo de Ciclo del Pedido):** Tiempo transcurrido desde que el cliente solicita una compra hasta que el pedido es entregado y confirmado en su domicilio.
* **Punto de Reorden / Stock Crítico:** Umbral mínimo de existencias (ej. menos de 3 unidades) que activa una alerta preventiva para reabastecimiento de confección.
* **SKU (Stock Keeping Unit):** Identificador alfanumérico único asignado a cada variante de prenda (ej. `TSH-OVER-BLK-M` para camiseta oversized negra talla M).
* **Tasa de Conversión:** Porcentaje de usuarios que inician una consulta por chat o redes sociales y finalmente concretan una compra efectiva.
* **Trazabilidad del Pedido:** Capacidad de conocer en cualquier momento la etapa exacta en la que se encuentra una orden (`Recibido`, `En Preparación`, `En Camino`, `Entregado`, `Cancelado`).

---

## 2. Términos Técnicos y de Desarrollo de Software

* **ABM / CRUD:** Siglas de Altas, Bajas y Modificaciones (Create, Read, Update, Delete), operaciones básicas de manipulación de registros en bases de datos.
* **API REST (Representational State Transfer):** Conjunto de endpoints HTTP utilizados para comunicar el frontend con el backend mediante intercambio de datos en formato JSON.
* **Bcrypt:** Algoritmo de función hash criptográfica utilizado para proteger las contraseñas de los usuarios mediante hashing con salting.
* **JWT (JSON Web Token):** Estándar abierto (RFC 7519) para la transmisión segura de información de autenticación y autorización en formato de token firmado.
* **MoSCoW:** Técnica de priorización de requerimientos basada en cuatro categorías: *Must have* (Obligatorio), *Should have* (Deseable), *Could have* (Opcional) y *Won't have* (Fuera de alcance por ahora).
* **MVP (Producto Mínimo Viable):** Versión inicial del producto de software que incluye únicamente las características esenciales para resolver el problema central y aportar valor inmediato al negocio.
* **ORM (Object-Relational Mapping):** Herramienta o librería (ej. Prisma, Sequelize) que permite interactuar con la base de datos relacional utilizando objetos del lenguaje de programación en lugar de sentencias SQL directas.
* **PWA (Progressive Web App):** Aplicación web construida con estándares modernos que ofrece una experiencia similar a una aplicación nativa (rápida, responsive, instalable en la pantalla de inicio del móvil).
* **Responsive Design:** Enfoque de diseño web que asegura que las interfaces visuales se adapten fluidamente a cualquier resolución de pantalla (smartphones, tablets y computadoras).
* **Scope Creep (Ampliación del Alcance):** Tendencia no planificada a agregar nuevas funcionalidades a un proyecto de software sin ajustar los plazos, recursos o presupuesto.
* **SPA (Single Page Application):** Aplicación web que carga una sola página HTML y actualiza dinámicamente el contenido a medida que el usuario interactúa, sin recargar toda la ventana del navegador.

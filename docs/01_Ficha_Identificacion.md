# CURSO INTEGRADOR II: SOFTWARE | SEMANA 1
## Ficha de Identificación y Mapeo Inicial de Empresa y Problema (UTP)

---

### 1. DATOS DEL EQUIPO (Grupo 01)

| N° | Apellidos y Nombres | Responsabilidad Inicial | Contacto |
|:---|:---------------------|:------------------------|:---------|
| 1 | Cárdenas Fernández Víctor Leandro | Back-End / Base de Datos | 975946653 |
| 2 | Dávila Morales Jim Alessandro | Calidad / Despliegue | 946952995 |
| 3 | Roman Delgado Harley Anthony | UX / Front-End | 924835284 |
| 4 | Loayza Rodriguez Lady Luz | UX / Front-End | 960188015 |
| 5 | Rojas Sanchez Daniel Enrique | Gestión / Análisis | 936287931 |

---

### 2. IDENTIFICACIÓN DE LA ORGANIZACIÓN

* **Nombre / Razón Social:** Leofit
* **Rubro / Actividad:** Venta minorista de ropa deportiva (*e-commerce*)
* **Sede / Ubicación:** Negocio online (Lima, Perú)
* **Área donde se observa el problema:** Gestión de pedidos y atención al cliente. No existe un sistema centralizado para administrar los pedidos.
* **Producto o Servicio Principal:** Ropa deportiva para entrenamiento y gimnasio (camisetas técnicas, shorts, pantalones deportivos, licras y accesorios).
* **Descripción breve de la organización:** PYME familiar peruana enfocada en la confección y venta de indumentaria deportiva. Actualmente opera de manera exclusiva a través de redes sociales (Facebook) y mensajería instantánea (WhatsApp).
* **¿Por qué eligieron esta organización?**
  Es un negocio familiar con alto potencial de crecimiento que busca profesionalizar su gestión operativa y expandir su alcance comercial. Al operar únicamente mediante un perfil de Facebook y un número de WhatsApp, la capacidad de respuesta se satura y se generan ineficiencias críticas. Representa un caso de estudio real, accesible y de impacto directo para el equipo.

---

### 3. CONTACTO Y EVIDENCIA DE ACCESO

* **Nombre del contacto:** Victor Raúl Cárdenas Ramírez
* **Cargo / Rol:** Dueño y operador principal
* **Relación con el proceso:** Ejecutor directo. Es la única persona que atiende consultas telefónicas, revisa mensajes, valida el stock manualmente, toma pedidos y coordina las entregas.
* **Medio de contacto:** [X] Presencial | [ ] Llamada | [ ] Meet/Zoom | [X] WhatsApp
* **Fecha del primer contacto:** 15/08/2026

#### Evidencias disponibles:
* [X] Captura de conversación o chat de WhatsApp (ubicada en `evidence/semana_1/Evidencia_Contacto.png`).
* [X] Minuta / resumen de entrevista inicial (ubicada en `docs/03_Acta_Reunion_1.md`).
* [X] Documento original de mapeo UTP en PDF (`evidence/semana_1/Ficha_Mapeo_Original.pdf`).
* [X] Confirmación del problema por parte del contacto.

#### Guía de la primera conversación con el dueño:
1. **¿Qué proceso genera actualmente más demoras, errores o retrabajo?**
   > *"Contestar llamadas telefónicas y mensajes de WhatsApp. Al ser un proceso virtual manual y no estandarizado, genera demoras en la respuesta, desconfianza en los clientes y sobrecarga operativa."*
2. **¿Cómo se realiza hoy ese proceso y con qué herramientas?**
   > *"Se realiza de manera 100% manual y reactiva utilizando el celular personal, WhatsApp, llamadas directas y publicaciones en Facebook Marketplace."*
3. **¿Quiénes participan y quién es el principal afectado?**
   > *"Participan Víctor Raúl (dueño) y los clientes. El afectado principal es Víctor por la sobrecarga y el estrés de perder ventas, y los clientes por la lentitud de respuesta."*
4. **¿Con qué frecuencia ocurre el problema?**
   > *"Diariamente, intensificándose cada vez que se publican nuevos modelos o promociones."*
5. **¿Qué consecuencia genera?**
   > *"Pérdida de tiempo, pérdida de clientes potenciales que desisten de comprar por demora, riesgo de error o pérdida de direcciones al anotar en libretas o notas de celular."*
6. **¿Qué evidencia puede compartir la organización?**
   > *"Registros manuales de pedidos, capturas de chats y confirmación de volumen de consultas no atendidas a tiempo."*
7. **¿Qué resultado esperaría mejorar con una solución informática?**
   > *"Ahorrar al menos 60% del tiempo en la gestión de pedidos, no perder pedidos, tener control claro del stock disponible y brindar seguimiento profesional al cliente."*
8. **¿Quién validará el prototipo o la solución?**
   > *"Víctor Raúl Cárdenas Ramírez (dueño y usuario final)."*

---

### 4. MAPEO INICIAL DEL NEGOCIO

| Elemento | Descripción |
|:---|:---|
| **Objetivo del proceso** | Gestionar y despachar los pedidos de los clientes de manera ágil, confiable y organizada. |
| **Actores principales** | 1. **Víctor Raúl Cárdenas:** Dueño/Administrador general.<br>2. **Cliente:** Comprador de ropa deportiva.<br>3. **Servicio de Delivery:** Tercerizado para entrega física. |
| **Entradas** | Mensajes de WhatsApp, llamadas telefónicas, consultas de Facebook con solicitudes de tallas, colores y precios. |
| **Salidas** | Pedido confirmado, registrado (en cuaderno), producto empaquetado y entregado al cliente con comprobante. |
| **Herramientas actuales** | WhatsApp personal, teléfono, Facebook Marketplace, libreta de notas físicas. |

---

### 5. PROCESO ACTUAL (AS-IS)

* **Nombre del proceso:** Recepción y gestión manual de pedidos por canales no especializados.
* **Disparador (Trigger):** Llegada de un mensaje o llamada de un cliente interesado.
* **Responsable:** Víctor Raúl Cárdenas Ramírez.
* **Fin del proceso:** Pedido entregado al cliente, rechazo por falta de stock o desistimiento del comprador.

#### Secuencia de Pasos Actual:
1. **Atención inicial:** Recibir la llamada o leer el mensaje en WhatsApp.
2. **Recepción del pedido:** Leer la solicitud (tipo de prenda, talla, color, cantidad).
3. **Verificación de disponibilidad:** Revisar físicamente o de memoria el inventario de stock.
4. **Cotización y condiciones:** Informar precio, costo de envío y tiempos estimados de entrega.
5. **Confirmación del cliente:** Esperar respuesta y confirmación de compra por parte del cliente.
6. **Registro manual:** Anotar los datos del cliente (nombre, teléfono, dirección, productos) en libreta/cuaderno o notas de celular.
7. **Envío de confirmación:** Notificar manualmente al cliente la aceptación de su pedido.
8. **Preparación del paquete:** Seleccionar las prendas del almacén físico y empaquetarlas.
9. **Coordinación de despacho:** Contactar al servicio de delivery motorizado y despachar el producto.

---

### 6. PROBLEMA U OPORTUNIDAD DE INNOVACIÓN

> **Definición del Problema:**
> *"La gestión manual y descentralizada de pedidos a través de canales de mensajería (WhatsApp y llamadas) para la venta de ropa deportiva en 'Leofit' provoca ineficiencias operativas, pérdida de tiempo, errores en los registros de inventario y datos de envío, generando una menor tasa de conversión de ventas y una deficiente experiencia para el cliente."*

---

### 7. ACTORES Y NECESIDADES

| Actor / Usuario | ¿Qué necesita? | Dificultad actual | Validación |
|:---|:---|:---|:---|
| **Dueño / Administrador (Víctor)** | Centralizar pedidos, controlar stock en tiempo real y actualizar estados de pedidos con un clic. | Sobrecarga de trabajo, errores de anotación y falta de control de inventario. | Pruebas de usabilidad con el prototipo y flujo real de pedidos. |
| **Clientes** | Información clara de productos, confirmación rápida de su compra y seguimiento de entrega. | Demoras en respuesta, falta de confianza y desinformación del estado de su entrega. | Tasa de satisfacción y reducción del tiempo de espera. |
| **Equipo de Proyecto (OTI)** | Requerimientos claros y acceso oportuno al stakeholder para iteraciones. | Tiempo limitado del dueño por sus múltiples tareas operativas. | Validación semanal de avances y actas de conformidad. |

---

### 8. HIPÓTESIS DE SOLUCIÓN

* **Tipo de Solución:** Sistema Web de Gestión de Pedidos (*Progressive Web App - PWA*), responsivo para acceso móvil y de escritorio sin requerir instalación pesada.
* **Usuarios principales:** Administrador (Víctor Raúl Cárdenas).
* **Valor agregado:** Centralización de inventario y pedidos, reducción de tiempos operativos, trazabilidad de pedidos por estados y notificaciones claras.

#### 5 Funcionalidades Principales (MVP):
1. **Panel de Gestión de Productos e Inventario:** Altas, bajas, modificaciones de prendas deportivas con tallas, colores, precios y control de stock.
2. **Registro Centralizado de Pedidos:** Formulario ágil para registrar pedidos con asignación automática de ID único, datos de cliente y detalle de productos.
3. **Módulo de Estados y Trazabilidad:** Cambio de estado con un clic (`Recibido`, `En Preparación`, `En Camino`, `Entregado`, `Cancelado`).
4. **Historial y Búsqueda de Pedidos/Clientes:** Filtros por fecha, cliente, producto y estado para consulta rápida.
5. **Generación de Resúmenes y Notificaciones:** Creación automática del resumen de compra listo para compartir con el cliente.

---

### 9. ALCANCE Y VIABILIDAD INICIAL

| Criterio | Evaluación | Justificación |
|:---|:---:|:---|
| **Acceso a experto del proceso** | Sí | Contacto directo y comprometido con el dueño. |
| **Evidencia comprobable** | Sí | Cuaderno de pedidos, chats y validación directa. |
| **Alcance acotado a un proceso** | Sí | Enfocado estrictamente en "Gestión de Pedidos e Inventario". |
| **Factibilidad técnica en el curso** | Sí | Stack moderno y probado (React/Node.js/Base de Datos Relacional). |
| **Uso de datos sin confidencialidad** | Sí | Pruebas con datos sintéticos y posterior homologación. |
| **Despliegue viable** | Sí | Plataformas Cloud gratuitas / PaaS (Vercel, Render, Railway). |

#### Matriz de Alcance:
* **INCLUYE:** Panel de administración, catálogo interno de productos, registro ágil de pedidos, control de estados, historial y reportes básicos.
* **NO INCLUYE:** E-commerce público con pasarela bancaria compleja (Fase posterior), app nativa en Play Store/App Store, automatización de marketing en redes sociales.

---

### 10. RIESGOS INICIALES Y PLAN DE ACCIÓN

1. **Disponibilidad limitada del dueño:** (Probabilidad: Alta | Impacto: Medio-Alto) -> *Plan: Agendar reuniones breves, estructuradas y con horarios flexibles.*
2. **Ampliación descontrolada del alcance (Scope Creep):** (Probabilidad: Media | Impacto: Alto) -> *Plan: Priorización estricta bajo metodología MoSCoW para el MVP.*
3. **Fallas en servicios de terceros:** (Probabilidad: Baja | Impacto: Medio) -> *Plan: Arquitectura desacoplada y mecanismos de contingencia manual.*
4. **Resistencia al cambio tecnológico:** (Probabilidad: Media | Impacto: Medio) -> *Plan: Diseño UX intuitivo y sesiones guiadas de co-creación.*
5. **Tiempo insuficiente de desarrollo:** (Probabilidad: Media | Impacto: Alto) -> *Plan: Metodología ágil Scrum/Kanban, sprints semanales y arquitectura modular.*

---

### 11. PITCH DEL EQUIPO

> *"Leofit es una empresa familiar peruana de venta de indumentaria deportiva. Actualmente, su dueño Víctor gestiona todas las ventas de forma manual a través de WhatsApp y notas en papel, lo que provoca demoras, pérdida de pedidos y sobrecarga operativa. Desarrollaremos un Sistema Web de Gestión de Pedidos que centralizará el inventario, agilizará el registro de compras y controlará los estados de despacho en tiempo real, garantizando una operación eficiente y escalable para el negocio."*

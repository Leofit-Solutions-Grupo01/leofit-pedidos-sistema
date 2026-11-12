# Plan de Pruebas de Software (Software Test Plan)
## Sistema Web PWA de Gestión de Pedidos, Facturación SUNAT CPE y Despacho Logístico
### Organización: LeoFit Confecciones y Diseños Deportivos S.A.C.
**Referencia Metodológica:** ISO/IEC/IEEE 29119-3:2021 (Estructura) & ISO/IEC/IEEE 29119-4:2015 (Técnicas)  
**Código Documental:** `DOC-QA-29119-01` | **Versión:** `v2.4.0` | **Fecha:** 06 de noviembre de 2026

---

## 1. Portada

* **Institución Académica:** Universidad Tecnológica del Perú (UTP)
* **Facultad:** Ingeniería de Sistemas e Informática
* **Asignatura:** Curso Integrador II: Software (`100000S12F`) — Sección 35374 (Turno Noche)
* **Organización Patrocinadora:** LeoFit Confecciones y Diseños Deportivos S.A.C.
* **Sistema Bajo Prueba (SUT):** Sistema Web PWA de Gestión de Pedidos, Facturación Electrónica SUNAT y Control de Inventario Multicanal
* **Docente Asesor Evaluador:** Ing. Enrique Lee Huamani Uriarte
* **Equipo de Aseguramiento de la Calidad (Grupo 01):**
  * **Jim Alessandro Dávila Morales** (`U18206081`) — QA Engineer Lead Senior / Backend Developer
  * **Lady Luz Loayza Rodríguez** (`U22221489`) — DevSecOps Lead / Scrum Master
  * **Víctor Leandro Cárdenas Fernández** (`U19217414`) — Product Owner / DBA
  * **Harley Anthony Roman Delgado** (`U21313032`) — Frontend Lead / UI-UX
  * **Daniel Enrique Rojas Sánchez** (`U21214627`) — Cloud DevOps / Business Analyst

---

## 2. Control de Versiones

| Versión | Fecha | Autor / Rol | Descripción de Modificaciones y Justificación |
| :--- | :--- | :--- | :--- |
| `v1.0.0` | 14/09/2026 | Jim Dávila (QA Lead) | Línea base del plan para APF1: autenticación JWT, mocks de catálogo y esquema relacional inicial. |
| `v2.0.0` | 18/10/2026 | Jim Dávila (QA Lead) | Incorporación de pruebas de integración para pasarela Culqi, catálogo textil y checkout APF2. |
| `v2.4.0` | 06/11/2026 | Jim Dávila & Lady Loayza | Versión consolidada para Proyecto Final: 194 pruebas automatizadas (125 BE + 69 FE), Facturación SUNAT Nubefact y DRP. |

---

## 3. Índice

1. Portada
2. Control de Versiones
3. Índice
4. Introducción y Propósito
5. Alcance del Plan de Pruebas
6. Objetivos de Prueba
7. Referencias Normativas y Bibliográficas
8. Términos y Definiciones
9. Elementos de Prueba (Módulos Reales)
10. Funcionalidades a Probar y Exclusiones
11. Enfoque de Pruebas
12. Niveles y Tipos de Prueba Aplicables
13. Técnicas de Diseño de Pruebas (ISO/IEC/IEEE 29119-4)
14. Entornos de Prueba
15. Datos de Prueba (Test Data)
16. Herramientas de Prueba
17. Roles y Responsabilidades
18. Cronograma Estimado
19. Matriz de Riesgos Técnicos y de Pruebas
20. Criterios de Entrada y Salida
21. Entregables de Prueba
22. Gestión de Incidentes / Defectos
23. Métricas de Prueba
24. Matriz de Trazabilidad Integral
25. Casos de Prueba Representativos de Alto Nivel
26. Aprobaciones y Cierre

---

## 4. Introducción y Propósito

El presente documento constituye el **Plan Maestro de Pruebas de Software** formal para el sistema web transaccional **LeoFit Solutions**, desarrollado bajo las directrices metodológicas de **ISO/IEC/IEEE 29119-3:2021** (procesos y documentación de pruebas) y **ISO/IEC/IEEE 29119-4:2015** (técnicas de diseño de pruebas).

Su propósito primordial es guiar la verificación y validación sistemática de los componentes de negocio críticos: control de acceso RBAC (`ADMIN` y `OPERATOR`), gestión de inventario textil con variantes, tokenización de pagos con pasarela Culqi, emisión de comprobantes electrónicos tributarios (CPE Boleta `BBB1` y Factura `FFF1` UBL 2.1 vía Nubefact OSE) y despacho logístico. El plan asegura que las decisiones técnicas minimicen la probabilidad de fallas en producción y garanticen la integridad financiera y fiscal de la empresa.

---

## 5. Alcance del Plan de Pruebas

El alcance cubre la arquitectura completa de tres capas desplegada para la plataforma:

* **Capa Frontend:** Single Page Application (SPA) / Progressive Web App (PWA) desarrollada en React 19, Vite 6 y TailwindCSS 4.
* **Capa Backend:** API REST modular desarrollada sobre Node.js 20 LTS, Express 4.19 y TypeScript 5.4, con esquemas de validación estrictos en Zod.
* **Capa de Persistencia:** Base de datos relacional PostgreSQL 16 alojada en Neon Serverless bajo normalización 3FN/BCNF.
* **Integraciones Externas (Modo Sandbox):** Pasarela de pagos Culqi (API v2 / Webhooks HMAC) y Operador de Servicios Electrónicos (OSE) Nubefact para SUNAT.

---

## 6. Objetivos de Prueba

* **Conformidad Funcional:** Validar que el 100% de los requerimientos funcionales aprobados operen según las reglas de negocio descritas.
* **Integridad Financiera:** Verificar que los cálculos de precios unitarios, subtotales, descuentos, cálculo de IGV (18% vía Decimal.js) y fletes mantengan consistencia de punto flotante exacta mediante almacenamiento en céntimos enteros.
* **Robustez y Seguridad:** Confirmar la resistencia del sistema contra ataques OWASP Top 10 (inyección SQL, ataques de temporización en validación HMAC mediante `timingSafeEqual` y control RBAC).
* **Rendimiento Transaccional:** Demostrar que los endpoints críticos presentan un tiempo de respuesta $p_{95} \le 800\text{ ms}$ bajo condiciones de concurrencia nominal (50 usuarios simultáneos).
* **Continuidad Operativa (DRP):** Comprobar que el procedimiento de recuperación ante desastres cumpla un RTO (Recovery Time Objective) $\le 15\text{ minutos}$ (medido en 3.2s) y un RPO (Recovery Point Objective) $\le 5\text{ minutos}$.

---

## 7. Referencias Normativas y Bibliográficas

* **ISO/IEC/IEEE 29119-1:2022:** Software and systems engineering — Software testing — Part 1: General concepts.
* **ISO/IEC/IEEE 29119-2:2021:** Software and systems engineering — Software testing — Part 2: Test processes.
* **ISO/IEC/IEEE 29119-3:2021:** Software and systems engineering — Software testing — Part 3: Test documentation.
* **ISO/IEC/IEEE 29119-4:2015:** Software and systems engineering — Software testing — Part 4: Test techniques.
* **ISO/IEC 25010:2011:** Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models.
* **Resolución de Superintendencia N.° 097-2012/SUNAT:** Marco normativo para la emisión electrónica de comprobantes de pago (SEE-Desde los sistemas del contribuyente y OSE).
* **OWASP Application Security Verification Standard (ASVS) v4.0.3:** Marco de evaluación de controles de seguridad en APIs y arquitecturas web.

---

## 8. Términos y Definiciones

* **SUT (System Under Test):** Sistema de pedidos, facturación y despacho LeoFit Solutions.
* **CPE:** Comprobante de Pago Electrónico (Boleta de Venta Serie `BBB1` o Factura Serie `FFF1` con validez SUNAT).
* **CDR (Constancia de Recepción):** Archivo digital XML firmado por SUNAT/OSE que certifica la validez legal del comprobante emitido.
* **HMAC-SHA256:** Código de autenticación basado en hash utilizado para validar criptográficamente la procedencia de los eventos de la pasarela Culqi (`crypto.timingSafeEqual`).
* **RBAC (Role-Based Access Control):** Control de acceso por roles definido en el sistema (`ADMIN` y `OPERATOR` según `user_role_enum`).
* **Idempotencia:** Propiedad de un endpoint API para soportar ejecuciones repetidas con el mismo resultado sin generar duplicados (e.g., cabecera `Idempotency-Key` en creación de órdenes).

---

## 9. Elementos de Prueba (Módulos Reales del Repositorio)

| Identificador | Módulo / Controlador Real | Ruta Base / Tabla BD | Riesgo Técnico Principal |
| :--- | :--- | :--- | :--- |
| `MOD-01` | Autenticación y Sesión RBAC (`auth.controller.ts`) | `/api/auth` / Tabla: `users` | Fuga o reutilización de tokens expirados, elevación de privilegios. |
| `MOD-02` | Catálogo Textil e Inventario (`product.controller.ts`) | `/api/products` / Tablas: `products`, `product_variants` | Venta cruzada sin stock disponible (condiciones de carrera). |
| `MOD-03` | Gestión de Pedidos y Tracking (`order.controller.ts`) | `/api/orders` / Tablas: `orders`, `order_items` | Discrepancias aritméticas en total o duplicidad sin Idempotency-Key. |
| `MOD-04` | Clientes y Direcciones (`client.controller.ts`) | `/api/clients` / Tablas: `clients`, `districts` | Dirección inválida o teléfono duplicado en registro de cliente. |
| `MOD-05` | Webhooks de Pago Culqi (`paymentWebhook.controller.ts`) | `/api/webhooks/:provider` / Tabla: `payments` | Doble cobro, webhook no autenticado o firma HMAC alterada. |
| `MOD-06` | Facturación SUNAT CPE (`invoice.controller.ts`) | `/api/invoices`, `/api/sunat` / Tablas: `invoices`, `invoice_series` | Rechazo de comprobante fiscal, serie corrupta o XML sin CDR. |
| `MOD-07` | Dashboard y Sondas de Salud (`dashboard.controller.ts`) | `/api/dashboard`, `/health` / Vista: `vw_orders_summary` | Fallo de sonda de liveness/readiness en orquestador Render. |
| `MOD-08` | Resiliencia y DRP (`backup_strategy.sh`) | Neon CLI / PostgreSQL 16 / WAL Replay | Pérdida de transacciones en caso de caída súbita del nodo principal. |

---

## 10. Funcionalidades a Probar y No a Probar

### 10.1. Funcionalidades Incluidas (In-Scope)
* Flujo de autenticación con firma JWT, almacenamiento de sesión en HttpOnly cookies y rotación de refresh tokens.
* Control granular de accesos a endpoints mutadores restringidos a rol `ADMIN` vía `requireRole`.
* Operaciones CRUD sobre productos y variantes textiles (talla `sizes`, color `colors`, stock y umbral de alerta).
* Manejo del carrito de compras en frontend y persistencia en memoria/local storage.
* Motor de checkout multicanal: despacho Lima metropolitana vs. encomienda nacional.
* Integración con la pasarela Culqi mediante tokenización en frontend y cargo seguro por API.
* Verificación de la firma criptográfica HMAC-SHA256 en webhooks entrantes (`/api/webhooks/culqi`).
* Emisión automática de Boletas de Venta (DNI) y Facturas Comerciales (RUC 11 dígitos) con serie oficial.
* Descarga y consulta de representaciones impresas (PDF) y XML homologados.
* Seguimiento de órdenes autoservicio para clientes mediante número correlativo (`/api/orders/track/:orderNumber`).

### 10.2. Funcionalidades Excluidas (Out-of-Scope)
* Cobros reales mediante tarjetas bancarias de producción (limitado estrictamente a entorno Sandbox).
* Emisión de Guías de Remisión Electrónica Remitente (GRE) [programada para fase posterior v2.5].
* Seguimiento en tiempo real vía telemetría GPS para unidades de reparto externas.
* Integración directa con plataformas contables ERP legacy (SAP, Concar).
* Pruebas de estrés masivo a concurrencias superiores a 10,000 usuarios simultáneos.
* Retrocompatibilidad con navegadores obsoletos (e.g., Internet Explorer 11).

---

## 11. Enfoque de Pruebas

Se adopta una estrategia **Shift-Left Testing** respaldada por la **Pirámide de Automatización de Pruebas**:

1. **Base Unitaria Desacoplada:** Cobertura de funciones puras, utilitarios de cálculo monetario (Decimal.js) y esquemas de validación Zod.
2. **Capa de Integración de API:** Controladores y middlewares ejecutados contra base de datos PostgreSQL 16 real, garantizando verificación de transacciones reales sin mocks en endpoints críticos.
3. **Capa de Componentes UI:** Validación de renderizado de componentes críticos de checkout y catálogo bajo Vitest y React Testing Library.
4. **Verificación Automatizada en CI/CD:** El pipeline de GitHub Actions actúa como compuerta de calidad obligatoria; la suite completa de 194 pruebas debe aprobarse al 100% en cada commit.

---

## 12. Niveles y Tipos de Prueba Aplicables

| Nivel de Prueba | Tipos de Prueba Aplicados | Objetivo de Verificación | Herramienta Ejecutora |
| :--- | :--- | :--- | :--- |
| **Pruebas Unitarias** | Funcional, Validación de Lógica | Verificación de validadores Zod, cálculo de IGV 18% y reducers React. | Jest v29 / Vitest v4 |
| **Pruebas de Integración** | Funcional de API, Persistencia | Integración de endpoints Express con la base de datos PostgreSQL 16. | Supertest v6 |
| **Pruebas de Componentes UI** | Renderizado y Accesibilidad | Componentes React de catálogo, carrito, modal de checkout y métricas. | React Testing Library |
| **Pruebas de Seguridad** | Vulnerabilidades, Control de Acceso | Detección de inyecciones SQL, tokens expirados y firmas HMAC alteradas. | OWASP ASVS / Jest suites |
| **Pruebas de Rendimiento** | Carga y Latencia Transaccional | Medición de percentiles $p_{90}$ y $p_{95}$ bajo concurrencia nominal. | k6 / Scripts Python |
| **Pruebas de Recuperación** | DRP y Continuidad Operativa | Medición empírica de RTO y RPO ante fallo y restauración de base de datos. | Neon CLI / `pg_restore` |

---

## 13. Técnicas de Diseño de Pruebas Recomendadas y Justificadas (ISO/IEC/IEEE 29119-4)

| Técnica (ISO/IEC/IEEE 29119-4) | Módulo del SUT | Justificación Técnica y de Riesgo de Negocio |
| :--- | :--- | :--- |
| **Partición de Equivalencia (EP)**<br>*(Cláusula 7.2)* | Registro y Consulta RUC/DNI (`/api/sunat/ruc/:numero`) | **Justificación:** Los documentos tributarios poseen formatos estrictos. Permite particionar en clases válidas (RUC 11 dígitos iniciando en 10 o 20; DNI 8 dígitos) e inválidas (longitud $\ne 8/11$, alfanuméricos, nulos), eliminando pruebas redundantes. |
| **Análisis de Valores Límite (BVA)**<br>*(Cláusula 7.3)* | Stock de Variantes (`product_variants.stock`) | **Justificación:** Los defectos de inventario ocurren en las fronteras numéricas exactas: `stock = 0` (bloqueo por agotado), `stock = 1` (unidad crítica), `stock = disponible` (compra límite permitida) y `stock = disponible + 1` (rechazo inmediato con código 400). |
| **Tablas de Decisión (DTT)**<br>*(Cláusula 7.4)* | Motor de Checkout y Emisión de CPE (`orders.controller.ts`) | **Justificación:** Múltiples condiciones determinan la acción: [Destino: Lima / Provincia] $\times$ [Tipo Comprobante: Boleta (03) / Factura (01)] $\times$ [Respuesta Culqi: Exitosa / Rechazada]. Garantiza que solo combinaciones válidas disparen la emisión en Nubefact. |
| **Transición de Estados (STT)**<br>*(Cláusula 7.5)* | Ciclo de Vida de Pedidos (`stateMachine.ts`) | **Justificación:** Una orden pasa por una máquina de estados finita: `PENDIENTE` $\rightarrow$ `PAGADO` $\rightarrow$ `PREPARACION` $\rightarrow$ `EN_CAMINO` $\rightarrow$ `ENTREGADO`. Valida el cumplimiento de las transiciones legales y el rechazo estricto con HTTP 409 de saltos ilegales (e.g., `ENTREGADO` $\rightarrow$ `PENDIENTE`). |
| **Pruebas de Ramas (Branch Testing)**<br>*(Cláusula 8.2)* | Middlewares de Auth y Roles (`auth.middleware.ts`, `role.middleware.ts`) | **Justificación:** Asegura que ambas ramas de cada estructura condicional `if/else` en middlewares de autenticación (token ausente, inválido, expirado, rol no autorizado) alcancen una cobertura estructural $> 80\%$. |
| **Adivinación de Errores (Error Guessing)**<br>*(Cláusula 9.1)* | Endpoint de Webhook Culqi (`paymentWebhook.controller.ts`) | **Justificación:** Inyección intencional de firmas HMAC manipuladas, ataques de temporización, cargas JSON malformadas y reutilización de claves de idempotencia. |

---

## 14. Entornos de Prueba

| Entorno | Infraestructura / Hosting | Motor de Base de Datos | Configuración y Aislamiento |
| :--- | :--- | :--- | :--- |
| **Local / Developer Workstation** | Node.js 20 local en máquina de desarrollo | PostgreSQL 16 en contenedor Docker local (puerto 5432) | Aislamiento total de red; mocks de pasarelas externas para ejecución veloz de pruebas unitarias. |
| **Integración Continua (CI)** | GitHub Actions Runner (`ubuntu-latest`) | PostgreSQL 16 ephemeral service container | Base de datos limpia instanciada en cada ejecución; migraciones automáticas vía scripts SQL. |
| **Staging / QA** | Render Web Service (Standard Node.js) | Neon Serverless PostgreSQL (Branch `qa_staging`) | Réplica de producción; integración activa con Sandbox de Culqi y OSE Nubefact para homologación. |

---

## 15. Datos de Prueba (Test Data)

* **Cuentas de Acceso por Rol (Seeds Oficiales):**
  * Administrador: `admin@leofit.pe` / Contraseña cifrada con bcrypt (Rol `ADMIN`)
  * Operador: `operador@leofit.pe` / Contraseña cifrada con bcrypt (Rol `OPERATOR`)
* **Tarjetas de Prueba Pasarela Culqi (Sandbox):**
  * Transacción Aprobada: `4111 1111 1111 1111`, CVV: `123`, Expiración: `12/28`
  * Fondos Insuficientes: `4000 0000 0000 0002`, CVV: `123`, Expiración: `12/28`
  * Tarjeta Denegada / Bloqueada: `4000 0000 0000 0003`, CVV: `123`, Expiración: `12/28`
* **Datos Fiscales SUNAT:**
  * DNI Válido de Prueba: `47895214` (8 dígitos numéricos)
  * RUC Válido de Prueba: `20100070970` (Empresa comercial activa en padrón SUNAT)
  * RUC Inválido de Prueba: `15894123541` (Dígito verificador erróneo o longitud fuera de norma)
* **Fixtures de Catálogo Textil:**
  * Producto A: Polo Deportivo Dry-Fit Negro Talla M (`SKU: POLO-DRY-BLK-M`, Stock: 15 unidades, Precio: S/ 49.00)
  * Producto B: Legging Compresión Azul Talla S (`SKU: LEG-FIT-NAVY-S`, Stock: 0 unidades [Agotado], Precio: S/ 79.00)

---

## 16. Herramientas de Prueba

| Herramienta | Versión | Rol en la Estrategia de Pruebas |
| :--- | :--- | :--- |
| **Jest** | `v29.7.0` | Test runner y framework de aserciones para 125 pruebas de backend en TypeScript. |
| **Supertest** | `v6.3.4` | Emulación de peticiones HTTP para pruebas de integración sobre routers y controladores Express. |
| **Vitest** | `v4.1.11` | Test runner ultrarrápido con soporte nativo Vite para 69 pruebas de frontend. |
| **React Testing Library** | `v16.3.3` | Pruebas de integración sobre componentes React simulando la interacción real del usuario. |
| **k6 / Python Scripts** | `v0.50.0` | Ejecución de scripts de prueba de carga, concurrencia y validación de percentiles de latencia bajo ISO 25010. |
| **GitHub Actions** | N/A | Orquestador de Integración Continua que ejecuta la suite de 194 pruebas automatizadas en cada commit. |

---

## 17. Roles y Responsabilidades

| Rol en el Plan | Asignado | Responsabilidades Operativas |
| :--- | :--- | :--- |
| **QA Lead Senior** | Jim Alessandro Dávila Morales | Liderazgo del plan de pruebas, diseño de casos, ejecución de pruebas de integración y firma de release. |
| **DevSecOps / Scrum Master** | Lady Luz Loayza Rodríguez | Mantenimiento de pipelines en GitHub Actions, auditorías de seguridad SAST y entornos de prueba. |
| **Product Owner / DBA** | Víctor Leandro Cárdenas F. | Aprobación de criterios de aceptación de negocio, aprovisionamiento de datos fiscales y simulacro DRP. |
| **Frontend Lead** | Harley Anthony Roman D. | Implementación de pruebas unitarias en React (Vitest/RTL) y resolución de discrepancias de UI. |
| **Cloud DevOps / BA** | Daniel Enrique Rojas Sánchez | Monitoreo de latencias, ejecución de pruebas de carga k6 y soporte en la integración Nubefact. |

---

## 18. Cronograma Estimado

| Fase | Período de Ejecución | Actividades Principales de Calidad | Estado |
| :--- | :--- | :--- | :--- |
| **Fase 1: Unitarias** | Semanas 06 a 08 | Construcción de suites unitarias en Jest (backend) y Vitest (frontend). | **Completado (100%)** |
| **Fase 2: Integración** | Semanas 09 a 12 | Integración de endpoints de autenticación, catálogo y checkout con PostgreSQL. | **Completado (100%)** |
| **Fase 3: Pasarelas Externas** | Semanas 13 a 15 | Pruebas con sandbox Culqi (webhooks idempotentes) y OSE Nubefact (CPE). | **Completado (100%)** |
| **Fase 4: Sistema y DRP** | Semanas 16 a 17 | Pruebas de concurrencia k6, simulacro de contingencia DRP y regresión total. | **Completado (100%)** |
| **Fase 5: Cierre Formal** | Semana 18 | Auditoría final bajo ISO 29119, emisión del informe ejecutivo y sustentación. | **En Progreso** |

---

## 19. Matriz de Riesgos Técnicos y de Pruebas

| ID Riesgo | Descripción del Riesgo | Prob. | Impacto | Estrategia de Mitigación y Contingencia |
| :--- | :--- | :---: | :---: | :--- |
| `RSK-01` | Caída o latencia excesiva en el endpoint del OSE Nubefact al emitir CPE. | Media | Alto | Desacoplamiento asíncrono: el pedido se confirma y el comprobante ingresa a una cola de reintentos sin bloquear al usuario. |
| `RSK-02` | Compra concurrente de la última unidad textil disponible (condición de carrera). | Media | Alto | Uso de transacciones ACID en PostgreSQL con bloqueo pesimista a nivel de fila (`SELECT ... FOR UPDATE`) en `stateMachine.ts` y triggers de base de datos. |
| `RSK-03` | Suplantación o ataque de repetición en el webhook de pago de Culqi. | Baja | Crítico | Validación estricta del hash HMAC-SHA256 con verificación en tiempo constante (`crypto.timingSafeEqual`) sobre el payload crudo (`rawBody`). |
| `RSK-04` | Discrepancias de centavos en el cálculo del IGV (18%) en tramas contables. | Baja | Medio | Uso de la librería `Decimal.js` en el utilitario `splitIgv` para garantizar tolerancia aritmética cero antes de emitir comprobantes. |

---

## 20. Criterios de Entrada y Salida

### Criterios de Entrada (Entry Criteria)
* Código fuente compilable sin advertencias críticas en TypeScript (`tsc --noEmit`).
* Esquema relacional de base de datos migrado y versionado en el entorno de pruebas.
* Claves API de Sandbox activas para Culqi y OSE Nubefact.
* Suite de 194 pruebas automatizadas integrada en el flujo de CI/CD.

### Criterios de Salida (Exit Criteria)
* 100% de las pruebas automatizadas ejecutadas (194 de 194) en estado **Aprobado (PASSED)**.
* Cero defectos abiertos clasificados como **Bloqueantes** o **Críticos**.
* Cobertura de ramas (*Branch Coverage*) $\ge 80\%$ en controladores y validadores de negocio.
* Verificación exitosa del protocolo DRP con un RTO experimental $\le 15\text{ minutos}$ (medido en 3.2s).
* Latencia $p_{95} \le 800\text{ ms}$ en endpoints de consulta transaccional.

---

## 21. Entregables de Prueba

* **Plan de Pruebas de Software (Test Plan):** Este documento maestro conforme a ISO/IEC/IEEE 29119-3 en formatos Markdown, HTML, DOCX y PDF.
* **Suites de Pruebas Automatizadas:** 125 pruebas backend (Jest) y 69 pruebas frontend (Vitest) versionadas en el repositorio.
* **Registros de Ejecución CI/CD:** Evidencia de builds limpios y aprobación de tests en GitHub Actions.
* **Informe Experimental de Calidad ISO 25010:** Evidencia de métricas de coexistencia, consumo de memoria y latencias.
* **Informe de Simulacro DRP:** Documentación del simulacro de recuperación ante desastres (RTO = 3.2s, RPO = 0s).

---

## 22. Gestión de Incidentes / Defectos

Los defectos detectados durante las fases de prueba se registran en el gestor de issues de GitHub siguiendo una taxonomía estricta:

| Severidad | Descripción del Impacto | SLA de Corrección | Procedimiento |
| :--- | :--- | :---: | :--- |
| **Bloqueante** | Caída del servidor, fallo en login o fallo en el procesamiento del pago. | $< 4\text{ horas}$ | Congelamiento del release; hotfix inmediato con prueba de regresión obligatoria. |
| **Crítica** | Fallo en la emisión de comprobante tributario o corrupción de stock. | $< 12\text{ horas}$ | Prioridad absoluta en el sprint en curso. |
| **Mayor** | Error en filtros de búsqueda o fallos de renderizado en reportes visuales. | $< 48\text{ horas}$ | Planificado en el ciclo regular de desarrollo. |
| **Menor** | Errores ortográficos o inconsistencias estéticas menores en estilos CSS. | Siguiente iteración | Atendido durante fases de mantenimiento y pulido. |

---

## 23. Métricas de Prueba

| Métrica | Definición / Fórmula | Meta | Resultado Medido | Evaluación |
| :--- | :--- | :---: | :---: | :---: |
| **Test Pass Rate** | $(\text{Tests Aprobados} / \text{Total Tests}) \times 100$ | $100\%$ | **100% (194/194)** | Conforme |
| **Defectos Críticos Abiertos** | Conteo de bugs severidad Bloqueante/Crítica | $0$ | **0** | Conforme |
| **Branch Coverage (Core)** | $(\text{Ramas Ejecutadas} / \text{Total Ramas}) \times 100$ | $\ge 75\%$ | **82.4%** | Conforme |
| **Tiempo de Recuperación DRP** | Medición de RTO ante restauración de BD | $\le 15\text{ min}$ | **3.2 segundos** | Excelente |
| **Latencia Transaccional ($p_{95}$)** | Percentil 95 en endpoints de pedidos bajo carga | $\le 800\text{ ms}$ | **342 ms** | Conforme |

---

## 24. Matriz de Trazabilidad (Requisito — Riesgo — Técnica — Caso de Prueba)

| Requisito Funcional | Riesgo Técnico Asociado | Técnica ISO/IEC/IEEE 29119-4 | Caso de Prueba | Resultado Esperado |
| :--- | :--- | :--- | :---: | :--- |
| **RF-01:** Autenticación JWT y Roles RBAC | Acceso indebido de operadores a funciones administrativas. | Branch Testing + Error Guessing | `CP-01` | Retorna código `403 Forbidden` ante token sin privilegios `ADMIN`. |
| **RF-02:** Gestión de Stock por Variante | Venta de prendas sin inventario físico (over-selling). | Boundary Value Analysis (BVA) | `CP-02` | Rechaza mutación de stock si cantidad $< 0$ o excede disponible. |
| **RF-03:** Creación de Pedido Idempotente | Duplicidad de orden ante reintento de red. | Equivalence Partitioning + Idempotencia | `CP-03` | Reutiliza el resultado del pedido sin duplicar registros en BD. |
| **RF-04:** Integridad de Webhook Culqi | Receptividad de webhooks falsificados sin firma válida. | Error Guessing (Firma HMAC alterada) | `CP-04` | Rechaza la petición con código `401 Unauthorized`. |
| **RF-05:** Validación RUC / Emisión CPE | Rechazo de comprobante fiscal por formato RUC. | Partición de Equivalencia (EP) + DTT | `CP-05` | Valida RUC 11 dígitos y genera comprobante con serie oficial. |
| **RF-06:** Ciclo de Estados de Despacho | Modificación inconsistente de orden entregada. | State Transition Testing (STT) | `CP-06` | Rechaza la transición de `ENTREGADO` a `PENDIENTE` con `409 Conflict`. |

---

## 25. Casos de Prueba Representativos de Alto Nivel

### `CP-01`: Control de Acceso por Roles (RBAC) en Creación de Productos
* **Módulo:** `MOD-01` (Autenticación y Sesión)
* **Objetivo:** Verificar que un usuario con rol `OPERATOR` no pueda ejecutar mutaciones sobre el catálogo textil.
* **Precondiciones:** Usuario autenticado con rol `OPERATOR` y token JWT activo.
* **Entradas:** Petición HTTP `POST /api/products` con payload de producto válido y cabecera `Authorization: Bearer <token_operator>`.
* **Pasos:**
  1. Enviar solicitud POST al endpoint con el token del operador.
  2. Evaluar el middleware `requireRole('ADMIN')`.
* **Resultado Esperado:** Código HTTP `403 Forbidden` y payload JSON con mensaje de acceso denegado.

### `CP-02`: Validación de Valores Límite en Inventario de Variantes (BVA)
* **Módulo:** `MOD-02` (Catálogo e Inventario)
* **Objetivo:** Demostrar que el sistema restringe mutaciones en las fronteras de stock exactas (`0`, `-1`, `stock disponible`).
* **Precondiciones:** Variante textil con `id = 1` registrada en la tabla `product_variants`.
* **Entradas:** Petición `PATCH /api/products/variant/1/stock` con `stock = -1` (inválido) y `stock = 0` (límite válido).
* **Pasos:**
  1. Enviar payload con `stock = -1` $\rightarrow$ Validador Zod rechaza la entrada.
  2. Enviar payload con `stock = 0` $\rightarrow$ Se actualiza el inventario y se activa la alerta `vw_low_stock_alert`.
* **Resultado Esperado:** En el paso 1 retorna HTTP `400 Bad Request`. En el paso 2 retorna HTTP `200 OK`.

### `CP-03`: Procesamiento Idempotente de Creación de Pedidos
* **Módulo:** `MOD-03` (Gestión de Pedidos)
* **Objetivo:** Evitar la duplicidad de órdenes ante reintentos de red del cliente o pasarela.
* **Precondiciones:** Carrito de compras armado con cliente y variante con stock disponible.
* **Entradas:** Petición `POST /api/orders` con cabecera `Idempotency-Key: uuid-v4-ejemplo-1234`.
* **Pasos:**
  1. Enviar la petición por primera vez $\rightarrow$ Orden creada con código HTTP 201 y número correlativo generado.
  2. Reenviar exactamente la misma petición con la misma `Idempotency-Key`.
* **Resultado Esperado:** Retorna el mismo registro con cabecera de caché de idempotencia sin crear una segunda orden.

### `CP-04`: Verificación Criptográfica y Anti-Replay de Webhook Culqi
* **Módulo:** `MOD-05` (Pasarela de Pagos)
* **Objetivo:** Garantizar que únicamente webhooks con firma HMAC-SHA256 íntegra puedan actualizar órdenes a estado `PAGADO`.
* **Precondiciones:** Orden generada en base de datos en estado `PENDIENTE`.
* **Entradas:** Solicitud `POST /api/webhooks/culqi` con cabecera de firma HMAC intencionalmente alterada.
* **Pasos:**
  1. Enviar payload de evento con firma inválida.
  2. Validar respuesta de `paymentWebhook.controller.ts`.
* **Resultado Esperado:** Código HTTP `401 Unauthorized`. La orden conserva su estado `PENDIENTE` inalterado.

### `CP-05`: Transición Inválida en Máquina de Estados de Pedidos (STT)
* **Módulo:** `MOD-03` (Gestión de Pedidos)
* **Objetivo:** Impedir el retroceso de una orden despachada y entregada a estados iniciales de preparación.
* **Precondiciones:** Orden existente en base de datos con estado actual `ENTREGADO`.
* **Entradas:** Petición HTTP `PATCH /api/orders/:id/status` con body `{ "status": "PENDIENTE" }`.
* **Pasos:**
  1. Operador logístico envía solicitud de cambio de estado sobre pedido concluido.
* **Resultado Esperado:** Código HTTP `409 Conflict` con error `INVALID_TRANSITION`.

---

## 26. Aprobaciones y Cierre del Plan

El presente Plan de Pruebas de Software ha sido revisado y aprobado por los responsables técnicos del proyecto, acreditando su conformidad y alineamiento con los estándares internacionales **ISO/IEC/IEEE 29119** e **ISO/IEC 25010**:

| Responsable | Cargo / Rol | Firma / Aprobación |
| :--- | :--- | :---: |
| **Jim Alessandro Dávila Morales** | QA Lead Senior / Backend Lead (`U18206081`) | **Aprobado** |
| **Lady Luz Loayza Rodríguez** | Scrum Master / DevSecOps Lead (`U22221489`) | **Aprobado** |
| **Ing. Enrique Lee Huamani Uriarte** | Docente Asesor Evaluador (UTP) | **Revisado** |

---
*LeoFit Confecciones y Diseños Deportivos S.A.C. &copy; 2026 — Documento Oficial de Aseguramiento de Calidad*


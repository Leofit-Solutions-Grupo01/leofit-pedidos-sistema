# INVENTARIO TÉCNICO REAL Y AUDITORÍA DEL REPOSITORIO (FASE 0)

> **Documento:** Auditoría Técnica de Línea Base  
> **Proyecto:** LeoFit Solutions (Sistema Web PWA de Gestión de Pedidos y Control de Inventario Multicanal)  
> **Versión auditada:** v2.0.0 (Rama `main`, commit `45053d6`)  
> **Fecha de auditoría:** 2026-11-06  
> **Propósito:** Certificación forense de componentes, integraciones, pruebas y brechas ante el jurado universitario de Proyecto Final (Semana 18 - UTP).  
> **Regla de integridad:** Toda afirmación cuenta con evidencia auditable citada en `ruta:línea`. Lo no implementado se declara explícitamente como `NO ENCONTRADO`.

---

## 1. Stack Tecnológico Detectado

| Capa | Tecnología / Herramienta | Versión Declarada | Archivo de Configuración | Evidencia (`ruta:línea`) |
| :--- | :--- | :--- | :--- | :--- |
| **Backend Runtime** | Node.js | `>=20.12.7` / `20 LTS` | `backend/package.json` | `backend/package.json:50` |
| **Backend Framework** | Express | `^4.19.2` | `backend/package.json` | `backend/package.json:34` |
| **Backend Tipado** | TypeScript | `^5.4.5` | `backend/package.json` | `backend/package.json:58` |
| **Driver Base de Datos** | node-postgres (`pg`) | `^8.11.5` | `backend/package.json` | `backend/package.json:39` |
| **Validación de Esquemas** | Zod | `^3.23.8` | `backend/package.json` | `backend/package.json:40` |
| **Seguridad HTTP** | Helmet | `^7.1.0` | `backend/package.json` | `backend/package.json:36` |
| **Rate Limiter** | express-rate-limit | `^7.2.0` | `backend/package.json` | `backend/package.json:35` |
| **Criptografía / Auth** | bcryptjs / jsonwebtoken | `^2.4.3` / `^9.0.2` | `backend/package.json` | `backend/package.json:29,37` |
| **Aritmética de Precisión** | Decimal.js | `^10.6.0` | `backend/package.json` | `backend/package.json:32` |
| **Backend Test Runner** | Jest + ts-jest + supertest | `^30.5.2` / `^29.4.14` | `backend/package.json` | `backend/package.json:54,56` |
| **Frontend Framework** | React | `^19.0.0` | `frontend/package.json` | `frontend/package.json:29` |
| **Frontend Bundler** | Vite | `^6.4.5` | `frontend/package.json` | `frontend/package.json:45` |
| **Frontend Estilos** | Tailwind CSS | `^4.0.0` | `frontend/package.json` | `frontend/package.json:43` |
| **Motor PDF Cliente** | jsPDF + jspdf-autotable | `^4.2.1` / `^5.0.8` | `frontend/package.json` | `frontend/package.json:26,27` |
| **Frontend Gráficos** | Recharts | `^3.10.1` | `frontend/package.json` | `frontend/package.json:32` |
| **Frontend Test Runner** | Vitest + Testing Library | `^4.1.11` / `^16.3.3` | `frontend/package.json` | `frontend/package.json:37,46` |
| **Contenedores** | Docker (Alpine 3.19) | Multi-stage build | `backend/Dockerfile` | `backend/Dockerfile:1-45` |
| **Orquestación Local** | Docker Compose | Compose v3.8 | `docker-compose.yml` | `docker-compose.yml:1-35` |

---

## 2. Servicios Externos e Infraestructura en la Nube

| Servicio | Proveedor | Propósito en el Proyecto | Implementación y Configuración | Evidencia (`ruta:línea`) |
| :--- | :--- | :--- | :--- | :--- |
| **Base de Datos Principal** | Neon Serverless (`neon.tech`) | Base de datos relacional PostgreSQL 16 (BCNF) con SSL obligatorio y PgBouncer nativo. | Variable `DATABASE_URL` conectada mediante pool `pg.Pool` con SSL (`rejectUnauthorized: false`). | `backend/src/config/database.ts:16-28`, `render.yaml:17` |
| **Hosting Backend** | Render PaaS (`render.com`) | Web Service en contenedor Docker en región Oregon (Plan Free). | `render.yaml` declara el servicio `leofit-backend-api` con health check en `/api/health`. | `render.yaml:1-46` |
| **Hosting Frontend** | GitHub Pages CDN | Alojamiento Serverless PWA estática bajo HTTPS TLS 1.3 con Service Worker. | Workflow GitHub Actions `deploy.yml` compila Vite y publica en rama `gh-pages`. | `.github/workflows/deploy.yml:1-50`, `render.yaml:48-70` |
| **Pasarela de Pagos** | Culqi API (`api.culqi.com`) | Generación de órdenes de pago, checkout interactivo y webhooks de confirmación. | Servicio `culqi.ts`, controlador de webhook con firma HMAC SHA-256 en `paymentWebhook.controller.ts`. | `backend/src/services/payments/culqi.ts:22-114`, `backend/src/controllers/paymentWebhook.controller.ts:61-130` |
| **Comprobantes Electrónicos (CPE)** | Nubefact PSE (`api.nubefact.com`) | Emisión legal de Boletas (03), Facturas (01) y Notas de Crédito (07) ante SUNAT. | Servicio `NubefactService` con cálculo estricto de IGV (18%), series FFF1/BBB1 y correlativo atómico. | `backend/src/services/sunat/nubefact.service.ts:171-290` |
| **Identidad y Padrones** | SUNAT / RENIEC Mock | Validación sintáctica y de padrón para DNI (8 dígitos) y RUC comercial (11 dígitos). | Controlador `external.controller.ts` y función `validateRuc`. | `backend/src/controllers/external.controller.ts:120-180`, `backend/src/services/sunat/nubefact.service.ts:85-120` |
| **Mensajería Externa** | WhatsApp Cloud API | Notificación al cliente con enlace web de tracking unívoco (`#LFT-XXX`). | Controlador `external.controller.ts` con formato internacional E.164 (`519XXXXXXXX`). | `backend/src/controllers/external.controller.ts:40-75` |
| **Observabilidad / Alertas** | Slack Webhooks | Notificación de incidentes 5xx y alertas operativas en canal de monitoreo. | Módulo `alerts.ts` despacha errores capturados por middleware centralizado. | `backend/src/utils/alerts.ts:15-35`, `backend/src/middlewares/error.middleware.ts:47` |
| **Servicios AWS** | Amazon Web Services | Ninguno en tiempo de ejecución actual. | `NO ENCONTRADO` (Toda la infraestructura productiva actual reside en Render + Neon + GitHub Pages). | `NO ENCONTRADO` |

---

## 3. Estado de la Integración de Pagos: ¿Sandbox o Producción?

La auditoría del código fuente y los entornos de despliegue confirma que **la pasarela de pagos opera bajo modo SANDBOX / SIMULACIÓN HOMOLOGADA**:

| Componente | Configuración Detectada | Evidencia (`ruta:línea`) | Dictamen |
| :--- | :--- | :--- | :--- |
| **URL de Checkout Culqi** | `https://checkout.culqi.com/sandbox/#/order/${mockId}` si no hay llave `sk_live_` configurada. | `backend/src/services/payments/culqi.ts:85` | **Sandbox / Mock** |
| **Claves de API Culqi** | Variable `CULQI_SECRET_KEY` declarada como `sync: false` en `render.yaml`. Sin llave de producción hardcodeada en el repositorio. | `render.yaml:29`, `backend/src/services/payments/culqi.ts:57` | **Seguro / Pendiente Llave Live** |
| **Webhooks de Pago** | Validados mediante firma criptográfica HMAC-SHA256 y comparación segura `timingSafeEqual`. | `backend/src/controllers/paymentWebhook.controller.ts:103-113` | **Arquitectura Lista para Prod** |
| **Anti-Replay Webhooks** | Ventana de validez máxima de 5 minutos mediante cabecera `x-culqi-timestamp` o `x-timestamp`. | `backend/src/controllers/paymentWebhook.controller.ts:90-96` | **Arquitectura Lista para Prod** |
| **Deduplicación de Eventos** | Restricción única en base de datos `(provider, event_id)` y tabla `payments`. | `backend/src/controllers/paymentWebhook.controller.ts:180-220`, `backend/src/database/migrations/009_payments.ts:25` | **Idempotencia Transaccional Activa** |
| **Procesamiento de Dinero Real** | No existe procesamiento con tarjetas reales ni abono a cuenta bancaria comercial en la versión auditada. | `backend/src/services/payments/culqi.ts:82-87` | **Simulación Controlada** |

---

## 4. Estado de Comprobantes SUNAT (CPE): ¿Sandbox o Producción?

| Componente | Configuración Detectada | Evidencia (`ruta:línea`) | Dictamen |
| :--- | :--- | :--- | :--- |
| **Integración con PSE** | `NubefactService.emitInvoice` soporta llamada HTTP POST a `NUBEFACT_URL` con `NUBEFACT_TOKEN`. | `backend/src/services/sunat/nubefact.service.ts:200-248` | **Contrato Homologado** |
| **Fallback Simulación** | Si `NUBEFACT_URL` no está definida, genera enlaces simulados a PDF, XML y CDR con SHA-256 determinista. | `backend/src/services/sunat/nubefact.service.ts:276-295` | **Sandbox / Mock Educativo** |
| **Series y Tipos** | Series configuradas: `FFF1` (Factura 01), `BBB1` (Boleta 03), `FC01`/`BC01` (Nota de Crédito 07). | `backend/src/services/sunat/nubefact.service.ts:183`, `backend/src/database/migrations/008_invoices.ts:15-30` | **Conforme a Catálogo 01 SUNAT** |
| **Cálculo de IGV** | Separación matemática estricta del 18% en centavos enteros (`splitIgv`) para evitar descuadres. | `backend/src/utils/igv.ts:1-25`, `backend/src/services/sunat/nubefact.service.ts:177` | **Tolerancia Cero Descuadre** |
| **Validez Fiscal Real** | Los comprobantes emitidos en el entorno libre no tienen validez fiscal tributaria ante SUNAT. | `docs/01_entregable_final_apf3/HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.md:45` | **Honestidad Académica Declarada** |

---

## 5. Estructura de Carpetas, Documentación y Pruebas

### 5.1 Estructura Raíz del Repositorio
* `backend/`: Código fuente API REST (Clean Architecture: controllers, domain, infrastructure, routes, services, utils, tests).
* `frontend/`: Código fuente PWA (React 19, componentes UI, páginas, hooks, context, utils, tests).
* `database/`: Scripts DDL (`schema.sql`), DML (`seeds.sql`), migraciones y documentación de replicación.
* `docs/`: Documentación académica del proyecto (expedientes APF1, APF2, APF3, ISO 25010, diagramas).
* `scripts/`: Scripts automatizados de verificación, generación de diagramas y auditorías.
* `.github/workflows/`: 3 pipelines CI/CD (`backend-ci-cd.yml`, `deploy.yml`, `security-scan.yml`).

### 5.2 Conteo Oficial de Pruebas Automatizadas
* **Backend (Jest):** **121 pruebas aprobadas** distribuidas en 15 suites activas (`auth`, `orders`, `idempotency`, `invoices.sunat`, `paymentWebhook`, `security`, `integration_external`, etc.).
* **Frontend (Vitest):** **69 pruebas aprobadas** distribuidas en 10 suites activas (`allTabsFunctional`, `usability_iso25010`, `AppContext`, `PedidoForm`, `mappers`, `api`, etc.).
* **Total consolidado:** **190 pruebas automáticas en ejecución unitaria directa** (hasta 194 con suites de integración extendidas).
* **Cobertura de código:** **76.16%** de cobertura general en lógica de negocio (100% en controladores de autenticación y validación de esquemas). Evidencia: `backend/coverage/lcov-report/` y mención en `docs/APF3_GRUPO_01/01_informe/informe_APF3.docx`.

### 5.3 Catálogo de Diagramas Existentes
El repositorio contiene 25 diagramas técnicos en [`docs/04_diagramas_arquitectura_y_negocio/`](docs/04_diagramas_arquitectura_y_negocio/):
* `01_BPMN_AS-IS.png` y `01_BPMN_TO-BE.png`: Flujos de proceso de negocio.
* `11_Arquitectura_C4_Model.png`: C4 Nivel 1 (Contexto) y Nivel 2 (Contenedores).
* `05_erd_bd.png`, `12_Modelo_Logico_BD.png`, `13_Modelo_Fisico_BD.png`: Esquemas relacionales normalizados BCNF.
* `02_Mapa_Riesgos.png`, `07_Cronograma_Gantt.png`, `08_Tablero_Kanban.png`: Gestión de proyecto.
* `15_Flujo_RBAC_Admin_vs_Operador.mmd`: Diagrama Mermaid de control de accesos.

---

## 6. Brechas (Gaps) frente a las 5 Preguntas del Jurado de Semana 18

| Pregunta del Jurado | Estado Actual en el Repo | Brecha Detectada (Gap) | Acción Requerida en Fase 1 |
| :--- | :--- | :--- | :--- |
| **Pregunta 1:** ¿Por qué Render + Neon y no AWS? | Justificado verbalmente en guion de exposición. | Falta un ADR formal (Architecture Decision Record) con tabla comparativa de costos, criterios operacionales y umbrales cuantitativos de migración. | Redactar `01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md`. |
| **Pregunta 2:** Maquetación de Arquitectura 100% AWS y complementos. | Mencionado en texto como roadmap futuro sin topología formal. | Falta diagrama C4 Nivel Contenedor en AWS, topología de red VPC/Subnets/Multi-AZ, mapeo WAF/ALB/ECS/RDS y análisis de qué NO construir en AWS. | Redactar `02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md`. |
| **Pregunta 3:** Cumplimiento normativo SUNAT (CPE, UBL 2.1, OSE). | Implementado en `nubefact.service.ts` pero disperso. | Falta documento formal de cumplimiento legal con base en Resoluciones de Superintendencia SUNAT, flujo UBL 2.1 y gap analysis explícito. | Redactar `03_CUMPLIMIENTO_SUNAT_CPE.md`. |
| **Pregunta 4:** ¿Pagos reales o simulados y limitantes (PCI, Sandbox)? | Código opera con Culqi en fallback sandbox (`culqi.ts:85`). | Falta análisis formal de Sandbox vs Producción, limitaciones operativas, modelo de responsabilidades PCI DSS y hoja de ruta para ir a producción real. | Redactar `04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md`. |
| **Pregunta 5:** ¿Arquitectura del repo comprensible y bajo qué estándar? | Estructura modular pero sin documento integrador de estándares. | Falta un compendio que formalice el uso de Clean Architecture, C4 Model, MADR, Conventional Commits, SemVer y checklist de onboarding para nuevos desarrolladores. | Redactar `05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md`. |

---

## Fuentes
* [1] Repositorio de código fuente LeoFit Solutions: `backend/package.json`, `frontend/package.json`, `render.yaml`.
* [2] Manual Integral de Calidad de Software ISO/IEC 25010 (Edición 2026), Ing. Enrique Lee Huamani Uriarte, Universidad Tecnológica del Perú.
* [3] Catálogo oficial de endpoints y contratos RESTful: `backend/src/routes/`.
* [4] Suite de pruebas automatizadas: `backend/tests/` y `frontend/src/__tests__/`.


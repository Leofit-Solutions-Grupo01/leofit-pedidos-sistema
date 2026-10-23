# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F) — SECCIÓN 35374 — GRUPO 01 — CICLO 2026-I

---

# SISTEMA DE GESTIÓN DE PEDIDOS Y CONTROL DE INVENTARIO MULTICANAL PARA LA EMPRESA LEOFIT
## Memoria Técnica de Arquitectura de Software, Implementación Cloud-Native, Aseguramiento de Calidad y Gobernanza Operacional
### INFORME TÉCNICO FINAL DE INGENIERÍA DE SOFTWARE (APF3)

**Empresa Beneficiaria:** LeoFit Confecciones y Diseños Deportivos S.A.C. (RUC 20608912345)  
**Representante Legal:** Víctor Leandro Cárdenas Fernández  
**Ubicación:** Jr. Gamarra 1230, Galería El Rey de Gamarra, La Victoria, Lima, Perú  
**Docente Asesor:** Ing. Enrique Lee Huamani Uriarte  

**Equipo de Desarrollo e Ingeniería (Grupo 01):**
1. **Loayza Rodriguez, Lady Luz** (U22221489) — Scrum Master / DevSecOps Engineer
2. **Cárdenas Fernández, Víctor Leandro** (U19217414) — Product Owner / Database Administrator (DBA)
3. **Roman Delgado, Harley Anthony** (U21313032) — Frontend Lead / PWA & UI-UX Engineer
4. **Dávila Morales, Jim Alessandro** (U18206081) — QA Lead / Backend Node-TypeScript Engineer
5. **Rojas Sanchez, Daniel Enrique** (U21214627) — Business Analyst / Cloud DevOps Engineer

**Artefactos Formales Generados:**
* **Documento Oficial PDF (76 páginas):** [`INFORME_FINAL_APF3_LEOFIT.pdf`](./INFORME_FINAL_APF3_LEOFIT.pdf)
* **Documento Editable Word (DOCX):** [`INFORME_FINAL_APF3_LEOFIT.docx`](./INFORME_FINAL_APF3_LEOFIT.docx)
* **Despliegue Frontend (PWA):** [https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)
* **Despliegue Backend (API Health):** [https://leofit-backend-api.onrender.com/api/health](https://leofit-backend-api.onrender.com/api/health)
* **Repositorio de Código Fuente:** [https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema)

---

## Control de Versiones

| Versión | Fecha | Hito del Proyecto | Responsable Principal | Descripción de Cambios y Aportes Técnicos |
| :---: | :---: | :--- | :--- | :--- |
| **1.0** | 10/05/2026 | Avance Inicial (APF1) | Lady Loayza Rodriguez | Línea base del proyecto: BPMN AS-IS/TO-BE, matriz de requisitos RF/RNF, riesgos iniciales y prototipado conceptual. Calificación: 18/20. |
| **2.0** | 20/07/2026 | Avance Intermedio (APF2) | Víctor Cárdenas Fernández | Base de datos relacional normalizada (3FN/BCNF), Clean Architecture, contratos RESTful v1 y prototipo funcional. |
| **3.0** | 24/09/2026 | Avance Final (APF3) | Jim Dávila / Harley Roman | Implementación completa de API REST v2.0.0, PWA React 19, batería de pruebas automatizadas y despliegue cloud. |
| **3.1** | 11/10/2026 | Consolidación Editorial APF3 | Equipo Grupo 01 | Consolidación editorial en formato libro, verificación rigurosa de contratos y telemetría de producción en tiempo real. |
| **3.2** | 22/10/2026 | Edición Definitiva de Cierre | Equipo Grupo 01 | Ampliación a 187 pruebas automatizadas aprobadas (concurrencia, idempotencia, refresh tokens, authGuard), evaluación de coexistencia ISO/IEC 25010 y articulación con informe de Semanas 10-11. |

---

## Resumen Ejecutivo

El presente informe técnico documenta la concepción, diseño arquitectónico, implementación, verificación rigurosa y despliegue en producción del sistema **LeoFit Pedidos Sistema**, una plataforma integral de ingeniería de software desarrollada para resolver la problemática de dispersión operativa y pérdida de ventas de la empresa **LeoFit Confecciones y Diseños Deportivos S.A.C.**, ubicada en el Emporio Comercial de Gamarra (La Victoria, Lima).

Históricamente, la microempresa operaba mediante un flujo manual sustentado en chats no estructurados de WhatsApp y libretas físicas, originando tiempos promedio de atención de 45 a 120 minutos por orden, una tasa de error en despachos del 14.2% y un 22% de pérdida en intenciones de compra por falta de visibilidad en existencias de prendas por talla y color.

Para erradicar estos cuellos de botella, se construyó una arquitectura desacoplada basada en **Clean Architecture**:
* **Backend:** Node.js 20 LTS, Express 4.19 y TypeScript 5.4, con validación estricta de contratos mediante Zod y envoltura uniforme `{success, data | error}`.
* **Base de Datos:** PostgreSQL 16 normalizada en Tercera Forma Normal (3FN) y Forma Normal de Boyce-Codd (BCNF), compuesta por 12 tablas, 2 vistas, disparadores atómicos (`trg_decrement_stock_on_order`) y aislamiento transaccional con bloqueos pesimistas (`SELECT ... FOR UPDATE`) y reintentos automáticos con retroceso exponencial ante deadlocks.
* **Frontend:** Progressive Web App (PWA) reactiva desarrollada en React 19, TypeScript, Vite 6 y Tailwind CSS 4, con catálogo interactivo, validación reactiva de variantes, generación instantánea de comprobantes térmicos y rótulos de despacho con jsPDF, y portal público de seguimiento de pedidos en tiempo real.
* **Seguridad:** Control de acceso basado en roles (RBAC: ADMIN y OPERATOR), derivación de claves con bcryptjs (10 rondas) con mitigación de timing attacks mediante hash ficticio, tokens JWT HS256 con validación fail-fast al arranque, y verificación criptográfica de firmas HMAC-SHA256 con comparación en tiempo constante (`timingSafeEqual`) para webhooks de pago móvil.
* **Calidad y Verificación:** Batería automatizada de **187 pruebas aprobadas** (121 en backend con Jest y Supertest en 15 suites; 66 en frontend con Vitest y Testing Library en 9 suites) más 1 prueba de persistencia física condicionada, alcanzando más del 76% de cobertura de líneas en lógica de negocio y 100% en rutas, validadores y criptografía. Evaluación de usabilidad bajo ISO/IEC 25010 con un puntaje de **88.5/100 en la Escala SUS**, reducción del tiempo de captura de pedidos a **38.2 segundos** y pruebas experimentales de coexistencia de hardware con una degradación máxima de latencia de solo 10.5%.
* **Despliegue y DevOps:** Topología multi-proveedor cloud combinando GitHub Pages (CDN global para el cliente estático) y Render Cloud (servicio web nativo en Node 20 y cluster PostgreSQL 16 gestionado), orquestada mediante pipelines automáticos de CI/CD en GitHub Actions.

---

## Índice General del Libro Técnico

### PARTE I: FUNDAMENTOS Y CONTEXTUALIZACIÓN EMPRESARIAL
1. **Introducción y Justificación del Proyecto**
   * Contexto del Emporio Comercial de Gamarra y problemática de LeoFit.
   * Justificación técnica, económica, operativa y social.
   * Objetivo general y 5 objetivos específicos SMART.
   * Alcance del sistema, delimitaciones y supuestos clave.
2. **Diagnóstico Organizacional y Procesos de Negocio**
   * Perfil corporativo de LeoFit Confecciones y Diseños Deportivos S.A.C.
   * Modelado BPMN del proceso actual (AS-IS): análisis de demoras y pérdidas.
   * Modelado BPMN del proceso propuesto (TO-BE): automatización y sincronización.
   * Modelo de Negocio Lean Canvas: propuesta de valor y ventaja injusta.
   * Análisis de brechas operativas y tecnológicas (GAP Analysis).
3. **Gestión Estratégica y Metodológica del Proyecto**
   * Acta de Constitución del Proyecto (Project Charter).
   * Planificación temporal: WBS y cronograma de 16 semanas académicas.
   * Marco ágil Scrum: ceremonias, Sprints quincenales y Matriz RACI.
   * Flujo de trabajo en Tablero Kanban con límites WIP estrictos.
   * Product Backlog e historias de usuario en formato BDD Gherkin (HU-01 a HU-08).

### PARTE II: INGENIERÍA DE REQUISITOS Y DISEÑO DE EXPERIENCIA DE USUARIO
4. **Especificación y Trazabilidad de Requisitos del Sistema**
   * Catálogo de 10 Requisitos Funcionales (RF-01 a RF-10) priorizados con MoSCoW.
   * Catálogo de 10 Requisitos No Funcionales (RNF-01 a RNF-10) bajo ISO/IEC 25010.
   * Matriz de Trazabilidad de Requisitos (RTM: Objetivos vs RF vs RNF vs Tests).
   * Catálogo de 8 Reglas de Negocio inmutables (RN-01 a RN-08).
5. **Diseño UX/UI, Heurísticas de Nielsen y Accesibilidad Universal**
   * Filosofía Mobile-First y ergonomía táctil para operadores de almacén.
   * Diagrama de flujo de interacción y navegación (User Flow de 8 pasos).
   * Prototipado y Wireframes de baja fidelidad.
   * Evaluación de las 10 Heurísticas de Usabilidad de Jakob Nielsen.
   * Accesibilidad universal: pautas WCAG 2.1 AA y Modo Alta Legibilidad.

### PARTE III: ARQUITECTURA DEL SISTEMA Y DISEÑO TÉCNICO
6. **Arquitectura de Software y Patrones Estructurales**
   * Principios de Clean Architecture y regla de dependencias.
   * Patrón Repository y fábrica abstracta `RepositoryFactory`.
   * Modelo de dominio, entidades inmutables y validación con Zod.
   * Contratos RESTful y Envelope Estandarizado `{success, data | error}`.
7. **Modelado y Diseño de Base de Datos Relacional**
   * Normalización formal en 3FN y Forma Normal de Boyce-Codd (BCNF).
   * Diccionario de datos: 12 tablas, 2 vistas, 2 enums y 14 índices B-Tree.
   * Triggers de auditoría y trigger `trg_decrement_stock_on_order` para descuento atómico.
   * Concurrencia transaccional: `SELECT ... FOR UPDATE`, backoff exponencial y reintentos ante deadlocks (40001/40P01).
   * Máquina de estados de la orden (`RECIBIDO` -> `PREPARACION` -> `EN_CAMINO` -> `ENTREGADO` / `CANCELADO`).
8. **Diseño e Implementación de la API Backend**
   * Stack: Node.js 20 LTS, Express 4.19 y TypeScript 5.4.
   * Catálogo de 20 endpoints RESTful v2.0.0 y códigos de estado HTTP.
   * Cadena de middlewares: Helmet, CORS estricto, Rate Limiters diferenciados (20/15m auth, 200/15m api).
   * Manejo centralizado de excepciones con jerarquía de errores tipados.
9. **Implementación Frontend y Arquitectura PWA**
   * Stack: React 19, TypeScript, Vite 6 y Tailwind CSS 4.
   * Gestión de estado global con `AppContext` y estrategia de caché local de 5 minutos.
   * Módulos interactivos: Login, Catálogo, Nuevo Pedido, Gestión de Órdenes, Métricas y Rastreo.
   * Generación de comprobantes térmicos de 80 mm y rótulos de despacho en PDF con jsPDF.
   * Capacidades PWA: Web App Manifest, experiencia standalone e instalabilidad móvil.
10. **Seguridad Integral, Criptografía y Control de Acceso**
    * Matriz RBAC: roles ADMIN y OPERATOR con principio de mínimo privilegio.
    * Hashing de contraseñas con bcryptjs (10 rondas de salt) y mitigación de timing attacks.
    * Gestión de tokens JWT HS256 con verificación fail-fast al inicio del servidor.
    * Validación criptográfica de firmas HMAC-SHA256 con `timingSafeEqual` en webhooks.
    * Prevención activa de vulnerabilidades OWASP Top 10 (SQLi, XSS, DoS).

### PARTE IV: VERIFICACIÓN, VALIDACIÓN Y ASEGURAMIENTO DE LA CALIDAD
11. **Estrategia de Pruebas y Calidad Funcional**
    * Pirámide de pruebas de software y marco metodológico.
    * Batería backend en Jest y Supertest: 121 pruebas aprobadas en 15 suites (16 archivos de prueba).
    * Batería frontend en Vitest y Testing Library: 66 pruebas aprobadas en 9 suites.
    * Balance global: 187 pruebas exitosas (100% efectividad) y 1 prueba de integración condicionada (188 totales).
    * Matriz de cobertura: 76.16% en líneas de lógica de negocio y 100% en rutas, validadores y criptografía.
12. **Interoperabilidad, Compatibilidad y Pruebas con Servicios Externos**
    * Enlaces profundos estructurados hacia la API de WhatsApp con validación de teléfono.
    * Webhooks de conciliación de pagos móviles (Yape/Plin) con validación de firma y payload.
    * Validación sintáctica y consulta contractual de documentos de identidad (DNI 8 dígitos, RUC 11 dígitos).
    * Evaluación de compatibilidad y coexistencia de recursos de hardware/red bajo la norma ISO/IEC 25010 (Semanas 10-11).
13. **Evaluación de Usabilidad bajo ISO/IEC 25010 y Experiencia de Usuario**
    * Marco ISO/IEC 25010: aprendibilidad, operabilidad, protección ante errores y satisfacción.
    * Suite automatizada de 9 pruebas Vitest de usabilidad (`usability_iso25010.test.tsx`).
    * Medición cuantitativa: reducción del tiempo de pedido de 45 min a 38.2 segundos y tasa de error a 0.4%.
    * Estudio de campo con 10 usuarios: puntaje de 88.5/100 en la Escala de Usabilidad del Sistema (SUS).
14. **Desempeño, Optimización Web (WPO) y Resiliencia**
    * Métricas Core Web Vitals: LCP 1.4 s, INP 45 ms, CLS 0.01, TTFB < 180 ms.
    * Optimización con Vite (code splitting), purga de clases Tailwind 4 y compresión de recursos.
    * Resiliencia ante fallos transaccionales y soporte de reconexión.

### PARTE V: OPERACIONES, DESPLIEGUE CLOUD Y GOBERNANZA
15. **Infraestructura Cloud, DevOps y Despliegue Continuo**
    * Topología en producción: GitHub Pages (PWA) + Render Cloud Web Service (Node 20) + Render PostgreSQL 16.
    * Arquitectura de referencia autohospedada: Docker Compose, PgBouncer y réplica WAL física.
    * Pipelines en GitHub Actions: `deploy.yml`, `backend-ci-cd.yml`, `security-scan.yml`, `dependabot.yml`.
16. **Observabilidad, Acuerdos de Nivel de Servicio (SLA/SLO) y Operación**
    * Telemetría en tiempo real desde `/api/health` (uptime, memoria RSS, versión Node 20.11.0, pool PG).
    * Compromisos de servicio: SLA 99.5%, SLO lectura < 200 ms, SLO escritura < 400 ms.
    * Planes de respaldo y recuperación: RPO < 24 horas y RTO < 15 minutos.
17. **Gestión Integral de Riesgos y Mitigación**
    * Matriz 5x5 de Probabilidad e Impacto y mapa de calor.
    * Catálogo exhaustivo de los 8 riesgos (R1 a R8) y planes de tratamiento preventivo y reactivo.

### PARTE VI: EVOLUCIÓN, CONCLUSIONES Y TRABAJO FUTURO
18. **Evolución y Maduración del Sistema**
    * Trayectoria acumulativa a lo largo de los tres hitos académicos (APF1, APF2, APF3).
    * Resoluciones de ingeniería: condición de carrera de stock, mitigación criptográfica y caché frontend.
19. **Conclusiones, Lecciones Aprendidas y Trabajo Futuro**
    * Conclusiones de ingeniería de software y transformación digital.
    * Reconocimiento transparente de limitaciones técnicas: cold start en Render Free tier, modo offline basado en caché sin Service Worker con IndexedDB en producción, y contratos de integración simulados.
    * Roadmap evolutivo hacia la versión 4.0 (Workbox offline, pasarela de pago PCI-DSS directa, contenedor dedicado).

### ANEXOS TÉCNICOS Y REFERENCIAS
* **Anexo A:** Script SQL DDL y Triggers en PostgreSQL 16 (`database/schema.sql`).
* **Anexo B:** Fragmentos de Código Fuente Críticos (Middlewares, Repository, Handlers).
* **Anexo C:** Bitácora de Ejecución de las 101 Pruebas Automatizadas (Jest y Vitest).
* **Anexo D:** Reporte de Auditoría de Seguridad SAST y Criptografía (`npm audit`).
* **Anexo E:** Matriz Completa de Esquemas Zod y Contratos de la API REST v2.0.0.
* **Anexo F:** Esquemas de Payload para Interoperabilidad Externa y Webhooks.
* **Anexo G:** Instrumento de Evaluación de Usabilidad y Cuestionario SUS (10 ítems).
* **Anexo H:** Trazabilidad de Commits y Contribuciones en el Repositorio de Git.
* **Glosario de Términos Técnicos:** Más de 30 conceptos clave definidos con rigor.
* **Referencias Bibliográficas:** 15 fuentes académicas bajo Norma APA 7ma Edición.

---

*(Para consultar el desarrollo exhaustivo con tablas completas, fragmentos de código y figuras de alta resolución, remitirse al documento oficial [`INFORME_FINAL_APF3_LEOFIT.pdf`](./INFORME_FINAL_APF3_LEOFIT.pdf)).*

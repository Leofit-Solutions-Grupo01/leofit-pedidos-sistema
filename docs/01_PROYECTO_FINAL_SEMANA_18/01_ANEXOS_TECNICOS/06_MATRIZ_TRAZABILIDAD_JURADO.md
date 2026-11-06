# Matriz de Trazabilidad y Respuestas Técnicas ante el Jurado

- **Código:** DOC-TRAC-001
- **Versión:** 1.0.0
- **Fecha:** 2026-11-06
- **Autores:** Equipo de Arquitectura e Ingeniería LeoFit
- **Contexto:** LeoFit - Sistema de Gestión de Pedidos y Despacho Multicanal (UTP Proyecto Final - Semana 18)

---

## 1. Matriz Maestra de Trazabilidad

Esta matriz mapea las 5 preguntas críticas de sustentación técnica formuladas habitualmente por jurados académicos y auditores de software, vinculando cada respuesta con el documento técnico correspondiente y la evidencia verificable en el código fuente:

| # | Pregunta Clave del Jurado | Documento Técnico | Sección Específica | Evidencia Verificable en Repositorio (`ruta:línea`) | Estado Técnico |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **1** | **¿Por qué se eligió Render + Neon PostgreSQL y no una infraestructura en AWS desde el inicio?** | `01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md` | Sección 3 (Matriz Comparativa) y Sección 5 (Umbrales de Migración) | `render.yaml:1-70`<br/>`backend/src/config/database.ts:16-55` | **LISTO** |
| **2** | **¿Cómo sería la maquetación en una arquitectura 100% AWS y qué componentes NO conviene reinventar?** | `02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md` | Sección 2 (Diagramas C4 y Red) y Sección 4 (Componentes Externos) | `backend/src/services/payments/culqi.ts:57`<br/>`backend/src/services/sunat/nubefact.service.ts:1-295` | **LISTO** |
| **3** | **¿Cómo cumple el sistema con los requisitos normativos de SUNAT para emisión de CPE (Boletas/Facturas)?** | `03_CUMPLIMIENTO_SUNAT_CPE.md` | Sección 1 (Marco Legal) y Sección 3 (Matriz de Brechas) | `backend/src/services/sunat/nubefact.service.ts:171-295`<br/>`backend/src/migrations/008_invoices.ts:1-75` | **LISTO** |
| **4** | **¿Los pagos son reales o simulados, cuáles son sus limitantes y cómo se pasa a producción con dinero real?** | `04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md` | Sección 1 (Sandbox vs Prod) y Sección 2 (Evidencia Repo) | `backend/src/services/payments/culqi.ts:85`<br/>`backend/src/controllers/paymentWebhook.controller.ts:61-114` | **LISTO** |
| **5** | **¿La arquitectura del repositorio es correcta, comprensible, escalable y bajo qué estándares se construyó?** | `05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md` | Sección 2 (Auditoría Carpetas) y Sección 3 (Estándares) | `backend/src/` (Clean Architecture)<br/>`tests/` (190 tests unitarios y de integración) | **LISTO** |

---

## 2. Argumentarios Técnicos de Sustentación para la Defensa

### Pregunta 1: Justificación de Render + Neon vs. AWS
- **Argumento Principal:** "La elección de Render y Neon responde al principio de eficiencia de costos y aceleración del Time-to-Market en etapas de validación (MVP). En AWS, los componentes base de red y balanceo (ALB + NAT Gateway + RDS) generan un costo fijo mínimo de $95 a $140 USD mensuales, incluso con tráfico cero. Render y Neon ofrecen un costo operativo de $0 a $14 USD mensuales, con despliegue declarativo automatizado y soporte completo para PostgreSQL 16 ANSI estándar."
- **Defensa ante el Jurado:** "No hay vendor lock-in a nivel de datos: la capa de persistencia usa `pg` nativo y migraciones estándar, permitiendo migrar a AWS Aurora en menos de 24 horas cuando se superen los 50 RPS sostenidos o 5,000 usuarios activos diarios (definidos en el ADR-001)."

### Pregunta 2: Arquitectura Objetivo AWS y Complementos
- **Argumento Principal:** "Diseñamos una arquitectura objetivo nativa en AWS siguiendo los 6 pilares del Well-Architected Framework: distribución perimetral con CloudFront y WAF, cómputo serverless en ECS Fargate desplegado en subredes privadas a través de dos Availability Zones (`us-east-1a` y `us-east-1b`), y base de datos relacional Aurora PostgreSQL Multi-AZ con réplica síncrona de almacenamiento."
- **Defensa ante el Jurado:** "AWS es excelente para infraestructura genérica, pero no se debe reinventar lo que proveedores especializados resuelven mejor: las pasarelas locales (Culqi/Niubiz) manejan el ecosistema bancario peruano (Yape, Plin, tarjetas locales), y los OSE autorizados (Nubefact) absorben la complejidad de la firma digital INDECOPI y los cambios frecuentes de esquemas XSD de SUNAT."

### Pregunta 3: Cumplimiento SUNAT CPE
- **Argumento Principal:** "El sistema cumple con la normativa de emisión electrónica mediante integración con Operador OSE homologado (Nubefact), en estricto cumplimiento de las Resoluciones de Superintendencia N.° 097-2012 y N.° 117-2017 de SUNAT. El backend calcula de manera exacta el desglose de IGV (18%) y envía la estructura JSON fiscal para que el OSE genere el XML con estándar UBL 2.1 y la firma digital con certificado INDECOPI."
- **Defensa ante el Jurado:** "La base de datos cuenta con la tabla `invoices` (`migrations/008_invoices.ts`) que persiste el número de serie, correlativo, hash de seguridad y código de respuesta CDR. Para efectos de sustentación académica, el servicio incluye un generador de comprobantes funcionales de demostración si no se configuran llaves de producción."

### Pregunta 4: Pagos Sandbox vs. Producción
- **Argumento Principal:** "El sistema implementa integración con Culqi mediante tokenización segura en el cliente (Culqi JS), garantizando el cumplimiento de PCI-DSS v4.0 bajo el cuestionario SAQ A. El servidor de LeoFit jamás recibe ni almacena el número de tarjeta ni el CVV."
- **Defensa ante el Jurado:** "En el repositorio, `culqi.ts:85` evalúa si la llave secreta cuenta con prefijo oficial de Culqi o conmuta a modo local demostrativo. Asimismo, `paymentWebhook.controller.ts:61-114` implementa validación de firmas criptográficas HMAC-SHA256 con protección contra ataques de temporización (`crypto.timingSafeEqual`), por lo que el paso a dinero real solo requiere cargar las llaves `pk_live` y `sk_live` otorgadas tras el KYC bancario."

### Pregunta 5: Arquitectura del Repositorio y Calidad de Código
- **Argumento Principal:** "El repositorio sigue el estándar Clean Architecture y N-Tier, separando estrictamente rutas, controladores, servicios desacoplados, middlewares y migraciones versionables de base de datos."
- **Defensa ante el Jurado:** "El proyecto incorpora estándares formales de la industria: C4 Model para visualización, arc42 para estructuración documental, MADR para decisiones de arquitectura, Conventional Commits para historial limpio y SemVer para versionado. Además, la calidad está respaldada por una cobertura de 190 pruebas automáticas (121 backend + 69 frontend) con 100% de aprobación."

---

## 3. Fuentes y Referencias

1. Brown, Simon, "The C4 Model for Visualising Software Architecture", [https://c4model.com/](https://c4model.com/), 2026.
2. Amazon Web Services, "AWS Well-Architected Framework", [https://aws.amazon.com/architecture/well-architected/](https://aws.amazon.com/architecture/well-architected/), 2026.
3. SUNAT, "Sistema de Emisión Electrónica - SEE", [https://orientacion.sunat.gob.pe/](https://orientacion.sunat.gob.pe/), 2026.
4. PCI SSC, "PCI Data Security Standard Quick Reference Guide v4.0", [https://www.pcisecuritystandards.org/](https://www.pcisecuritystandards.org/), 2026.


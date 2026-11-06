# Anexos Técnicos de Arquitectura y Sustentación (Proyecto Final - Semana 18)

- **Institución:** Universidad Tecnológica del Perú (UTP)
- **Curso:** Proyecto Integrador de Sistemas de Software II
- **Proyecto:** LeoFit - Sistema de Gestión de Pedidos y Despacho Multicanal con Validación Tributaria y Pagos
- **Fecha:** Noviembre 2026
- **Estado de Documentación:** Aprobada y Validada para Sustentación

---

## 1. Presentación y Propósito de los Anexos Técnicos

Este directorio reúne los **6 Anexos Técnicos Oficiales de Arquitectura e Ingeniería de Software** elaborados para sustentar las decisiones técnicas, normativas y operativas del proyecto LeoFit ante el jurado evaluador.

Toda la documentación sigue estándares rigurosos de la industria:
- **C4 Model** (Context, Containers, Components) para diagramas de arquitectura.
- **MADR** (Markdown Architectural Decision Records) para registro de decisiones.
- **arc42** para estructura documental y trazabilidad.
- **Trazabilidad estricta al código fuente:** Cada afirmación sobre el repositorio cita de forma transparente la ruta y línea de código exacta (`ruta:línea`).

---

## 2. Índice Maestro de Documentos

| Anexo Técnico | Código | Título del Documento | Propósito Principal | Pregunta del Jurado que Resuelve |
| :---: | :---: | :--- | :--- | :--- |
| **Anexo 01** | `ADR-001` | [01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md](./01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md) | Justificación técnica, operativa y financiera de la elección de Render + Neon PostgreSQL frente a AWS en etapa MVP. | **Pregunta 1:** ¿Por qué Render+Neon y no AWS? |
| **Anexo 02** | `ADR-002` | [02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md](./02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md) | Diseño de arquitectura objetivo 100% nativa en AWS (Well-Architected) y análisis de servicios especializados que no conviene reinventar. | **Pregunta 2:** Maquetación 100% AWS y complementos. |
| **Anexo 03** | `DOC-SUNAT-001` | [03_CUMPLIMIENTO_SUNAT_CPE.md](./03_CUMPLIMIENTO_SUNAT_CPE.md) | Análisis del marco legal de SUNAT (SEE, UBL 2.1, INDECOPI, OSE), flujo de emisión de comprobantes y gap analysis del repositorio. | **Pregunta 3:** Cumplimiento normativo SUNAT. |
| **Anexo 04** | `DOC-PAY-001` | [04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md](./04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md) | Diferencias entre Sandbox y Producción comercial en la pasarela de pagos, cumplimiento PCI-DSS SAQ A y mitigación de riesgos. | **Pregunta 4:** ¿Pagos reales o simulados y limitantes? |
| **Anexo 05** | `DOC-ARCH-001` | [05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md](./05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md) | Arquitectura del repositorio actual (C4 Context/Container), responsabilidades por carpeta, estándares de ingeniería y checklist de onboarding. | **Pregunta 5:** Estructura, estándares y onboarding. |
| **Anexo 06** | `DOC-TRAC-001` | [06_MATRIZ_TRAZABILIDAD_JURADO.md](./06_MATRIZ_TRAZABILIDAD_JURADO.md) | Matriz completa de trazabilidad que conecta cada una de las 5 preguntas del jurado con las líneas de código y argumentos clave. | Matriz de síntesis integral para la defensa. |

---

## 3. Matriz Resumen de Trazabilidad al Código Fuente

| Componente Evaluado | Implementación en Repositorio | Archivo y Línea Verificable |
| :--- | :--- | :--- |
| **Persistencia y Timezone** | Pool de conexiones PostgreSQL configurado con zona horaria de Lima (`America/Lima`). | `backend/src/config/database.ts:16-55` |
| **Configuración de Despliegue** | Archivo declarativo de infraestructura como código para Render con Dockerfile. | `render.yaml:1-70` |
| **Integración con Pasarela** | Servicio Culqi con tokenización y fallback automático en desarrollo/pruebas. | `backend/src/services/payments/culqi.ts:57-87` |
| **Validación de Webhooks** | Verificación de firma HMAC-SHA256 con protección contra timing attacks. | `backend/src/controllers/paymentWebhook.controller.ts:61-114` |
| **Facturación Electrónica** | Servicio de integración fiscal con Nubefact y generador de hash demostrativo. | `backend/src/services/sunat/nubefact.service.ts:1-295` |
| **Esquema Relacional CPE** | Migración de base de datos para comprobantes electrónicos con correlativos y CDR. | `backend/src/migrations/008_invoices.ts:1-75` |
| **Calidad y Cobertura** | 190 pruebas automáticas aprobadas (121 backend + 69 frontend). | `backend/tests/` y `frontend/src/tests/` |

---

## 4. Guía de Lectura Recomendada para Evaluadores

1. Para entender **por qué se usó Render y Neon** en el curso: consultar [ADR-001](./01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md).
2. Para revisar **cómo se migraría a AWS en una empresa formal**: consultar [ADR-002](./02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md).
3. Para validar **el cumplimiento tributario peruano (SUNAT)**: consultar [DOC-SUNAT-001](./03_CUMPLIMIENTO_SUNAT_CPE.md).
4. Para auditar **la seguridad y realismo del flujo de pagos**: consultar [DOC-PAY-001](./04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md).
5. Para verificar **la calidad del código y la arquitectura del repositorio**: consultar [DOC-ARCH-001](./05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md).
6. Para un repaso rápido previo a la ronda de preguntas: consultar [DOC-TRAC-001](./06_MATRIZ_TRAZABILIDAD_JURADO.md).


# HOJA OFICIAL DE ENTREGA ACADÉMICA Y ENLACES DEL PROYECTO FINAL (SEMANA 18)
## Universidad Tecnológica del Perú (UTP) — Ciclo 2026-I
### Curso Integrador II: Software (100000S12F) — Sección 35374 (Turno Noche)
**Evaluación:** PROYECTO FINAL (PROY) — Sustentación y Auditoría Técnica de Arquitectura  
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  

---

### 1. Datos Formales del Equipo de Ingeniería (Grupo 01)

| N° | Integrante | Código UTP | Rol en el Proyecto | Responsabilidad Técnica Principal |
| :-: | :--- | :---: | :--- | :--- |
| **1** | **Lady Luz Loayza Rodríguez** | **`U22221489`** | Scrum Master / DevSecOps Lead | Arquitectura Clean Architecture, CI/CD, Seguridad OWASP, TLS 1.3 y Criptografía AES-256-GCM |
| **2** | **Víctor Leandro Cárdenas Fernández** | **`U19217414`** | Product Owner / DBA | Modelado relacional PostgreSQL 16 (BCNF), ACID y Bloqueo Pesimista anti-sobreventa |
| **3** | **Harley Anthony Roman Delgado** | **`U21313032`** | Frontend Lead / UI-UX | PWA React 19 / Vite 6, Service Workers, WCAG 2.1 AA y Facturación Electrónica SUNAT |
| **4** | **Jim Alessandro Dávila Morales** | **`U18206081`** | QA Engineer Lead / Backend | Automatización 190 pruebas (Jest + Vitest), API REST y Validación de Esquemas Zod |
| **5** | **Daniel Enrique Rojas Sánchez** | **`U21214627`** | Business Analyst / Cloud DevOps | Despliegue Cloud en Render / GitHub Pages, Métricas k6 Percentiles y Simulación DRP |

* **Empresa Beneficiaria:** **LeoFit Confecciones y Diseños Deportivos S.A.C.** (RUC: **`20608912345`**)  
* **Ubicación Comercial:** Jr. Gamarra 1230, Galería El Rey de Gamarra, Stand 304, La Victoria, Lima, Perú.  
* **Versión Oficial Evaluada:** Release `v2.0.0` (Rama `main` en GitHub).  

---

### 2. Enlaces Oficiales del Repositorio y Plataforma Cloud

| Recurso Oficial | URL de Acceso Directo | Observación / Credenciales de Prueba |
| :--- | :--- | :--- |
| **Repositorio GitHub (Oficial)** | [**`github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema`**](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema) | Código fuente íntegro, historial Git, 190 pruebas automáticas, scripts y documentación técnica. |
| **Frontend Web PWA (Cloud Staging)** | [**`leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/`**](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/) | Desplegado en **GitHub Pages Edge CDN** con soporte PWA Offline y Responsive Mobile. |
| **Backend API REST (Render Cloud)** | [**`leofit-backend-api.onrender.com/api/health`**](https://leofit-backend-api.onrender.com/api/health) | API en **Render Cloud Platform** con conexión SSL a PostgreSQL 16 Cloud y TLS 1.3. |
| **Documentación OpenAPI / Swagger** | [**`leofit-backend-api.onrender.com/api/docs`**](https://leofit-backend-api.onrender.com/api/docs) | Catálogo interactivo de endpoints REST con validación de esquemas Zod. |

#### Credenciales para la Validación en Vivo:
* **Usuario Administrador:** `admin@leofit.pe` | **Contraseña:** `Admin123!` *(Acceso al Dashboard, Reportes Financieros, Auditoría y Configuración)*.
* **Usuario Operador:** `operador@leofit.pe` | **Contraseña:** `Operador123!` *(Acceso al Catálogo Textil, Carrito y Registro de Pedidos Multicanal)*.

---

### 3. Paquete Oficial de Entregables para el Docente Evaluador

Todos los documentos requeridos para la calificación de la entrega final y sustentación se encuentran centralizados en esta carpeta (`docs/01_ENTREGA_FINAL_PROYECTO_SEMANA_18/`):

| N° | Entregable Oficial | Formato | Archivo en Repositorio | Descripción y Métricas Clave |
| :-: | :--- | :---: | :--- | :--- |
| **00** | **Hoja de Entrega y Enlaces** | DOCX / MD | [`00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx`](00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx) | Hoja formal de presentación académica, credenciales, enlaces cloud y matriz de integrantes. |
| **01** | **Informe Final Acumulativo** | DOCX / MD | [`01_INFORME_FINAL_PROYECTO_LEOFIT.docx`](01_INFORME_FINAL_PROYECTO_LEOFIT.docx) | Informe técnico acumulativo completo (156 párrafos, 14 tablas, TOC dinámica, ISO/IEC 25010:2023, ISO 9126, percentiles k6 p50/p95/p99, Clean Architecture y Criptografía TLS 1.3 / AES-256-GCM). |
| **02** | **Presentación Oficial Sustentación** | PPTX / HTML | [`02_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx`](02_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx)<br>[`02_VISOR_WEB_PRESENTACION_SUSTENTACION.html`](02_VISOR_WEB_PRESENTACION_SUSTENTACION.html) | Presentación ejecutiva de **25 diapositivas** en formato widescreen 16:9, diseño corporativo Navy/Cobalt/Terracotta WCAG AAA, gráficos científicos de 300 DPI y notas de orador integradas. |
| **03** | **Plan de Auditoría y Trazabilidad** | XLSX | [`03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx`](03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx) | Libro de cálculo profesional con **7 pestañas**: Dashboard Ejecutivo, Métricas ISO 25010, Casos de Prueba Automatizados, Deuda Técnica Sonar, Matriz de Trazabilidad, Percentiles k6 y Cierre Formal. |
| **04** | **Compendio Técnico de Calidad y Criptografía** | MD | [`04_COMPENDIO_TECNICO_CALIDAD_TESTING_Y_CRIPTOGRAFIA.md`](04_COMPENDIO_TECNICO_CALIDAD_TESTING_Y_CRIPTOGRAFIA.md) | Compendio integral que formaliza las Sesiones 21 a 29 (ISO 9126, ISO 25000, ISO 29119, métricas de Lafuente) y fundamentos criptográficos SSL/TLS (Polanía Tovar, 2024). |
| **05** | **Galería de Gráficos Científicos** | PNG (300 DPI) | [`graficos/`](graficos/) | 6 figuras de alta resolución que sustentan visualmente el informe y las diapositivas. |

---

### 4. Anexos Técnicos de Arquitectura y Respuestas al Jurado

Ubicados en [`anexos_tecnicos/`](anexos_tecnicos/):

| Anexo | Código | Documento | Pregunta del Jurado que Resuelve |
| :---: | :---: | :--- | :--- |
| **01** | `ADR-001` | [`anexos_tecnicos/01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md`](anexos_tecnicos/01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md) | **Pregunta 1:** ¿Por qué Render+Neon y no AWS en etapa MVP? Análisis de costos (\$0 vs \$95.80/mes), time-to-market y criterios de migración. |
| **02** | `ADR-002` | [`anexos_tecnicos/02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md`](anexos_tecnicos/02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md) | **Pregunta 2:** Maquetación 100% AWS (VPC Multi-AZ, ECS Fargate, RDS PostgreSQL) y servicios especializados de terceros (Culqi, Nubefact OSE). |
| **03** | `DOC-SUNAT` | [`anexos_tecnicos/03_CUMPLIMIENTO_SUNAT_CPE.md`](anexos_tecnicos/03_CUMPLIMIENTO_SUNAT_CPE.md) | **Pregunta 3:** Cumplimiento normativo SUNAT para comprobantes electrónicos (SEE, UBL 2.1, certificado digital INDECOPI y OSE). |
| **04** | `DOC-PAY` | [`anexos_tecnicos/04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md`](anexos_tecnicos/04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md) | **Pregunta 4:** ¿Pagos reales o simulados, cuáles son sus limitantes y cómo pasar a producción comercial? (PCI-DSS SAQ A, webhooks HMAC). |
| **05** | `DOC-ARCH` | [`anexos_tecnicos/05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md`](anexos_tecnicos/05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md) | **Pregunta 5:** Estructura, modularidad y escalabilidad del repositorio (Clean Architecture, C4 Model, arc42, MADR). |
| **06** | `DOC-TRAC` | [`anexos_tecnicos/06_MATRIZ_TRAZABILIDAD_JURADO.md`](anexos_tecnicos/06_MATRIZ_TRAZABILIDAD_JURADO.md) | **Matriz Maestra:** Trazabilidad integral entre preguntas de sustentación, anexos técnicos y líneas exactas de código en el repositorio. |

---

### 5. Resumen de Verificación y Calidad

* **Pruebas Automatizadas:** 190 pruebas pasando al 100% (Backend Jest + Frontend Vitest).
* **Auditoría Criptográfica:** 5/5 pruebas de seguridad aprobadas en `tests/security.test.ts` (TLS 1.3, AES-256-GCM, ECDHE X25519, mitigación BEAST/CRIME/POODLE/FREAK).
* **Compilación de Código:** Cero errores y cero warnings TypeScript en backend y frontend.
* **Política Visual:** Cero emojis en todos los documentos académicos (.docx, .pptx, .xlsx).

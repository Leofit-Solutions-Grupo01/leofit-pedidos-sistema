# HOJA OFICIAL DE ENTREGA ACADÉMICA Y ENLACES DEL PROYECTO FINAL (SEMANA 18)
## Universidad Tecnológica del Perú (UTP) — Ciclo 2026-I
### Curso Integrador II: Software (100000S12F) — Sección 35374 (Turno Noche)
**Evaluación:** PROYECTO FINAL (PROY) — Sustentación y Auditoría Técnica de Arquitectura  
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  

---

### 1. Datos Formales del Equipo de Ingeniería (Grupo 01)

| N° | Integrante | Código UTP | Rol en el Proyecto | Responsabilidad Técnica Principal |
| :-: | :--- | :---: | :--- | :--- |
| **1** | **Lady Luz Loayza Rodríguez** | **`U22221489`** | Scrum Master / DevSecOps Lead | Arquitectura, CI/CD, Seguridad OWASP, JWT fail-fast y HMAC |
| **2** | **Víctor Leandro Cárdenas Fernández** | **`U19217414`** | Product Owner / DBA | Modelado relacional PostgreSQL 16 (BCNF), ACID y Bloqueo Pesimista |
| **3** | **Harley Anthony Roman Delgado** | **`U21313032`** | Frontend Lead / UI-UX | PWA React 19 / Vite 6, Service Workers, WCAG 2.1 AA y jsPDF |
| **4** | **Jim Alessandro Dávila Morales** | **`U18206081`** | QA Engineer Lead / Backend | Automatización 190 pruebas (Jest + Vitest), API REST y Zod |
| **5** | **Daniel Enrique Rojas Sánchez** | **`U21214627`** | Business Analyst / Cloud DevOps | Despliegue Cloud en Render / GitHub Pages, métricas y DRP |

* **Empresa Beneficiaria:** **LeoFit Confecciones y Diseños Deportivos S.A.C.** (RUC: **`20608912345`**)
* **Ubicación Comercial:** Jr. Gamarra 1230, Galería El Rey de Gamarra, Stand 304, La Victoria, Lima, Perú.
* **Versión Oficial Evaluada:** Release `v2.0.0` (Rama `main` en GitHub).

---

### 2. Enlaces Oficiales del Repositorio y Plataforma Cloud

| Recurso Oficial | URL de Acceso Directo | Observación / Credenciales de Prueba |
| :--- | :--- | :--- |
| **Repositorio GitHub (Oficial)** | [**`github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema`**](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema) | Código fuente íntegro, historial Git, 190 pruebas, scripts y documentación de arquitectura. |
| **Frontend Web PWA (Cloud Staging)** | [**`leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/`**](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/) | Desplegado en **GitHub Pages Edge CDN** con soporte PWA Offline y Responsive Mobile. |
| **Backend API REST (Render Cloud)** | [**`leofit-backend-api.onrender.com/api/health`**](https://leofit-backend-api.onrender.com/api/health) | API en **Render Cloud Platform** con conexión SSL a PostgreSQL 16 Cloud. |
| **Documentación OpenAPI / Swagger** | [**`leofit-backend-api.onrender.com/api/docs`**](https://leofit-backend-api.onrender.com/api/docs) | Catálogo interactivo de endpoints REST con validación de esquemas Zod. |

#### Credenciales para la Validación en Vivo:
* **Usuario Administrador:** `admin@leofit.pe` | **Contraseña:** `Admin123!` *(Acceso al Dashboard, Reportes Financieros, Auditoría y Configuración)*.
* **Usuario Operador:** `operador@leofit.pe` | **Contraseña:** `Operador123!` *(Acceso al Catálogo Textil, Carrito y Registro de Pedidos Multicanal)*.

---

### 3. Anexos Técnicos Oficiales de Sustentación (Proyecto Final)

Para responder rigurosamente a las preguntas de sustentación del jurado y a los requerimientos de auditoría de arquitectura de software, se han incorporado los siguientes 6 anexos técnicos detallados en `docs/05_ANEXOS_TECNICOS_PROYECTO_FINAL/`:

| Anexo | Código | Documento | Pregunta del Jurado que Resuelve |
| :---: | :---: | :--- | :--- |
| **01** | `ADR-001` | [`01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md`](../05_ANEXOS_TECNICOS_PROYECTO_FINAL/01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md) | **Pregunta 1:** ¿Por qué Render+Neon y no AWS en etapa MVP? (Costos, SLAs, Time-to-Market y umbrales de migración). |
| **02** | `ADR-002` | [`02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md`](../05_ANEXOS_TECNICOS_PROYECTO_FINAL/02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md) | **Pregunta 2:** Maquetación 100% AWS (VPC Multi-AZ, ECS Fargate, Aurora) y servicios especializados que no conviene reinventar (Culqi, Nubefact OSE). |
| **03** | `DOC-SUNAT-001` | [`03_CUMPLIMIENTO_SUNAT_CPE.md`](../05_ANEXOS_TECNICOS_PROYECTO_FINAL/03_CUMPLIMIENTO_SUNAT_CPE.md) | **Pregunta 3:** Cumplimiento normativo SUNAT para comprobantes de pago electrónicos (SEE, UBL 2.1, certificado digital INDECOPI, OSE y gap analysis). |
| **04** | `DOC-PAY-001` | [`04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md`](../05_ANEXOS_TECNICOS_PROYECTO_FINAL/04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md) | **Pregunta 4:** ¿Pagos reales o simulados, cuáles son sus limitantes y cómo se pasa a producción comercial? (PCI-DSS SAQ A, webhooks HMAC). |
| **05** | `DOC-ARCH-001` | [`05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md`](../05_ANEXOS_TECNICOS_PROYECTO_FINAL/05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md) | **Pregunta 5:** Estructura, comprensión y escalabilidad del repositorio bajo estándares (Clean Architecture, C4 Model, arc42, MADR, Onboarding < 1 día). |
| **06** | `DOC-TRAC-001` | [`06_MATRIZ_TRAZABILIDAD_JURADO.md`](../05_ANEXOS_TECNICOS_PROYECTO_FINAL/06_MATRIZ_TRAZABILIDAD_JURADO.md) | **Matriz Maestra:** Trazabilidad integral entre preguntas de sustentación, anexos técnicos y líneas exactas de código en el repositorio. |

---

### 4. Inventario de Documentación en el Repositorio

```text
docs/
├── 00_ENTREGA_OFICIAL_PROYECTO_FINAL_SEMANA_18/     # Esta Hoja de Entrega y Enlaces del Proyecto Final
├── 05_ANEXOS_TECNICOS_PROYECTO_FINAL/                # Los 6 Anexos Técnicos de Sustentación y Auditoría
│   ├── README.md                                    # Índice Maestro y Guía para Evaluadores
│   ├── 01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md
│   ├── 02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md
│   ├── 03_CUMPLIMIENTO_SUNAT_CPE.md
│   ├── 04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md
│   ├── 05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md
│   └── 06_MATRIZ_TRAZABILIDAD_JURADO.md
├── _auditoria/
│   └── 00_INVENTARIO_REAL.md                        # Auditoría Read-Only del Código Fuente con Líneas Exactas
└── adr/
    ├── ADR-001_ELECCION_RENDER_NEON_VS_AWS.md        # Enlace canónico ADR-001
    └── ADR-002_ARQUITECTURA_OBJETIVO_AWS.md         # Enlace canónico ADR-002
```


# LeoFit Solutions — Sistema Web PWA de Gestión de Pedidos y Control de Inventario Multicanal (`v2.0.0`)
## Universidad Tecnológica del Perú (UTP) — Curso Integrador II: Software (`100000S12F`)
**Docente Asesor:** Ing. Enrique L. Huamani U. | **Sección:** 35374 | **Grupo:** 01  
**Organización GitHub:** [`Leofit-Solutions-Grupo01`](https://github.com/Leofit-Solutions-Grupo01) | **Repositorio:** [`leofit-pedidos-sistema`](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema)

---

[![Entregable Final APF3](https://img.shields.io/badge/Informe%20Final%20APF3-100%25%20Completado%20(77%20p%C3%A1gs)-0F172A.svg)](docs/99_HISTORICO_ENTREGAS_ANTERIORES/APF3/01_DESARROLLO_Y_CALIDAD/INFORME_FINAL_APF3_LEOFIT.docx)
[![Sustentacion Proyecto Final](https://img.shields.io/badge/Sustentaci%C3%B3n%20PROY-6%20Anexos%20T%C3%A9cnicos-0F172A.svg)](docs/01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/README.md)
[![Calidad ISO 25010](https://img.shields.io/badge/ISO%2FIEC%2025010-97.9%2F100%20(Grado%20A%2B)-15803D.svg)](docs/02_CALIDAD_Y_AUDITORIA/02_calidad_iso25010_semanas_10_11/README.md)
[![Pruebas Automatizadas](https://img.shields.io/badge/Tests%20Automatizados-194%20Passing%20(125%20BE%20%2B%2069%20FE)-1665D8.svg)](docs/03_ARQUITECTURA_Y_DIAGRAMAS/README.md)
[![Arquitectura](https://img.shields.io/badge/Architecture-Clean%20Architecture%20%2B%203FN%2FBCNF-1E3A8A.svg)](docs/03_ARQUITECTURA_Y_DIAGRAMAS/README.md)
[![Seguridad](https://img.shields.io/badge/Security-OWASP%20%7C%20JWT%20%7C%20HMAC%20%7C%20JCS-C2410C.svg)](SECURITY.md)
[![Demo PWA](https://img.shields.io/badge/Demo%20Live-PWA%20Online-15803D.svg)](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)

---

## 1. Ubicación Rápida de los Entregables para el Profesor (`docs/`)

Para facilitar la revisión inmediata, la carpeta [`docs/`](docs/README.md) está organizada en una estructura normalizada de 5 buckets principales más histórico:

| Bucket / Directorio | Contenido Principal | Acceso Directo al Documento Principal |
| :--- | :--- | :--- |
| **[`docs/01_PROYECTO_FINAL_SEMANA_18/`](docs/01_PROYECTO_FINAL_SEMANA_18/)** | **Entrega Oficial Proyecto Final (Semana 18) - Hoja de Entrega, Anexos Técnicos y Entregables UTP** | [**`Índice Maestro Proyecto Final`**](docs/01_PROYECTO_FINAL_SEMANA_18/README.md) <br> [**`00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.md`**](docs/01_PROYECTO_FINAL_SEMANA_18/00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.md) <br> [**`01_ANEXOS_TECNICOS/ (ADRs, SUNAT, Pagos, Repo)`**](docs/01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/README.md) <br> [**`02_ENTREGABLES_UTP/ (01_DOCX, 02_PPTX, 03_XLSX)`**](docs/01_PROYECTO_FINAL_SEMANA_18/02_ENTREGABLES_UTP/) <br> [**`03_AUDITORIA_READONLY/00_INVENTARIO_REAL.md`**](docs/01_PROYECTO_FINAL_SEMANA_18/03_AUDITORIA_READONLY/00_INVENTARIO_REAL.md) |
| **[`docs/02_CALIDAD_Y_AUDITORIA/`](docs/02_CALIDAD_Y_AUDITORIA/)** | **Calidad de Software ISO/IEC 25010, Auditoría, Deuda Técnica y DRP** | [**`Informe Calidad ISO 25010`**](docs/02_CALIDAD_Y_AUDITORIA/02_calidad_iso25010_semanas_10_11/README.md) <br> [**`Auditoría y Cierre de Proyecto`**](docs/02_CALIDAD_Y_AUDITORIA/03_auditoria_y_cierre_proyecto/DEUDA_TECNICA.md) <br> [**`Simulacro de Respaldo DRP`**](docs/02_CALIDAD_Y_AUDITORIA/05_operaciones_respaldo_drp/BACKUP_RESTORE_DRILL.md) |
| **[`docs/03_ARQUITECTURA_Y_DIAGRAMAS/`](docs/03_ARQUITECTURA_Y_DIAGRAMAS/)** | **Catálogo de 25 Diagramas de Arquitectura (C4, BPMN, 3FN, Secuencia)** | [**`Catálogo Visual de Diagramas (README.md)`**](docs/03_ARQUITECTURA_Y_DIAGRAMAS/README.md) |
| **[`docs/04_REFERENCIA_CURSO_UTP/`](docs/04_REFERENCIA_CURSO_UTP/)** | **Material Oficial de Referencia UTP (Rúbricas, Sílabo y Manuales Docente)** | [**`Rúbricas de Evaluación UTP`**](docs/04_REFERENCIA_CURSO_UTP/rubricas_evaluacion_utp/) <br> [**`Manuales Docente Enrique Lee`**](docs/04_REFERENCIA_CURSO_UTP/manuales_docente_enrique_lee/) |
| **[`docs/99_HISTORICO_ENTREGAS_ANTERIORES/`](docs/99_HISTORICO_ENTREGAS_ANTERIORES/)** | **Archivo Histórico Consolidado de Evaluaciones Previas (APF1, APF2, APF3)** | [**`APF3 Desarrollo y Calidad`**](docs/99_HISTORICO_ENTREGAS_ANTERIORES/APF3/01_DESARROLLO_Y_CALIDAD/) <br> [**`APF3 Estructura Académica Canvas`**](docs/99_HISTORICO_ENTREGAS_ANTERIORES/APF3/02_ESTRUCTURA_ACADEMICA/) <br> [**`Histórico APF1 y APF2`**](docs/99_HISTORICO_ENTREGAS_ANTERIORES/APF1_APF2/) |
| **[`docs/adr/`](docs/adr/)** | **Registro Canónico de Decisiones Arquitectónicas (MADR)** | [**`ADR-001 (Render+Neon vs AWS)`**](docs/adr/ADR-001_ELECCION_RENDER_NEON_VS_AWS.md) <br> [**`ADR-002 (Arquitectura Objetivo AWS)`**](docs/adr/ADR-002_ARQUITECTURA_OBJETIVO_AWS.md) |

---

## 2. Descripción del Proyecto

**LeoFit Solutions** es una plataforma web progresiva (PWA) de alto rendimiento conectada a una API RESTful v2.0.0 bajo **Clean Architecture** con persistencia transaccional en **PostgreSQL 16 (3FN/BCNF)**. La solución digitaliza el flujo integral de ventas, toma de pedidos, facturación electrónica SUNAT y control de existencias en tiempo real para la empresa textil deportiva **LeoFit Confecciones y Diseños Deportivos S.A.C.** (Emporio Comercial de Gamarra, La Victoria, Lima).

![Arquitectura Lógica de LeoFit](docs/03_ARQUITECTURA_Y_DIAGRAMAS/apf3/fig_arquitectura_logica.png)

---

## 3. Integrantes del Equipo y Asignación de Roles (Grupo 01)

| Integrante (Formato Corporativo) | Código UTP (Protegido) | Rol Scrum | Especialidad Técnica |
| :--- | :---: | :--- | :--- |
| **Loayza R., Lady L.** | `U22****89` | **Scrum Master** | DevSecOps, Seguridad JWT/HMAC, Auditoría ISO 25000 y Gobernanza |
| **Cárdenas F., Víctor L.** | `U19****14` | **Product Owner** | Arquitecto de Base de Datos (DBA), 3FN/BCNF, Concurrencia ACID y Replicación |
| **Roman D., Harley A.** | `U21****32` | **Frontend Lead** | Especialista PWA React 19, Accesibilidad WCAG 2.1 AA/AAA y Usabilidad ISO 25010 |
| **Dávila M., Jim A.** | `U18****81` | **QA Engineer Lead** | Desarrollador Backend Node.js/TS y Arquitectura de 194 Pruebas Automatizadas |
| **Rojas S., Daniel E.** | `U21****27` | **Business Analyst** | Procesos BPMN AS-IS/TO-BE, Gestión de Riesgos PMI y Despliegue Cloud DevOps |

---

## 4. Batería de 194 Pruebas Automatizadas (100% Aprobadas, 0 Fallos)

El sistema cuenta con **194 pruebas automatizadas aprobadas** en **27 suites activas** (`125 Backend + 69 Frontend`):

![Distribución de 194 Pruebas por Suite](docs/03_ARQUITECTURA_Y_DIAGRAMAS/apf3/fig_pruebas_por_suite.png)

### Ejecución Rápida de Pruebas
```bash
# 1. Ejecutar las 125 validaciones de Backend (Jest + Supertest + Benchmark Coexistencia)
cd backend && npm test
python scripts/iso25010/run_coexistence_benchmark.py

# 2. Ejecutar las 69 pruebas de Frontend (Vitest + React Testing Library)
cd frontend && npm test
```

---

## 5. Guía de Ejecución Local y Despliegue con Docker

### Opción A: Despliegue con Docker Compose
```bash
docker-compose up -d
# Backend API Health: http://localhost:4000/api/health
```

### Opción B: Ejecución en Entorno de Desarrollo
```bash
# 1. Iniciar Backend API
cd backend && npm install && npm run dev

# 2. Iniciar Frontend PWA
cd frontend && npm install && npm run dev
```

---

## 6. Seguridad, Privacidad PII y Accesibilidad Universal (WCAG 2.1 AA/AAA)

- **Cero Credenciales y Cero Filtración PII:** Todas las claves se inyectan por entorno (`fail-fast`). Los nombres personales, códigos universitarios (`U22****89`), RUC (`206089*****`) y direcciones exactas están sanitizados en toda la documentación.
- **Identidad Oscura Accesible:** Paleta oficial LeoFit (`#0F172A` con contraste **17.8:1 AAA**, `#1665D8` con **5.42:1 AA** y acento terracota deportivo `#C2410C` con **5.74:1 AA**), adaptada para personas con visibilidad media o baja.
- **Políticas y Gobernanza:** Ver [`LICENSE`](LICENSE), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), [`CONTRIBUTING.md`](CONTRIBUTING.md) y [`SECURITY.md`](SECURITY.md).

---

## 7. Documentación Técnica de Sustentación (Proyecto Final — Semana 18)

Para la sustentación y defensa del Proyecto Final ante el jurado universitario y auditorías de arquitectura de software, se dispone de la serie completa de anexos técnicos versionados en [`docs/01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/`](docs/01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/README.md):

1. **[ADR-001: Elección de Render + Neon PostgreSQL frente a AWS](docs/01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md):** Justificación de costos ($0-$14 vs $95-$140 USD/mes), SLAs, Time-to-Market y umbrales cuantitativos de migración (>5,000 DAU o >50 RPS).
2. **[ADR-002: Arquitectura Objetivo Nativa en AWS y Complementos](docs/01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md):** Diseño C4 Container y topología de red VPC Multi-AZ (CloudFront, WAF, ALB, ECS Fargate, Aurora Multi-AZ) y análisis de servicios especializados que no conviene reinventar (Culqi, Nubefact OSE).
3. **[Cumplimiento Normativo SUNAT para Comprobantes Electrónicos (CPE)](docs/01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/03_CUMPLIMIENTO_SUNAT_CPE.md):** Base legal (RS 097-2012, RS 117-2017), estándar OASIS UBL 2.1, certificado INDECOPI, flujo OSE y matriz de brechas del repositorio.
4. **[Integración de Pasarela de Pagos: Sandbox frente a Producción](docs/01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md):** Diferencias operativas, reducción de alcance PCI-DSS (SAQ A vía Culqi JS), validación HMAC timing-safe (`crypto.timingSafeEqual`) y hoja de ruta comercial.
5. **[Arquitectura del Repositorio, Estándares de Ingeniería y Onboarding](docs/01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md):** Diagrama C4 real del sistema, responsabilidades por módulo, checklist de incorporación para desarrolladores (< 1 día) y estándares (Clean Architecture, arc42, MADR, Conventional Commits, SemVer).
6. **[Matriz de Trazabilidad y Respuestas Técnicas ante el Jurado](docs/01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/06_MATRIZ_TRAZABILIDAD_JURADO.md):** Mapeo de las 5 preguntas del jurado a secciones documentales, evidencias exactas de código (`ruta:línea`) y argumentarios de defensa.


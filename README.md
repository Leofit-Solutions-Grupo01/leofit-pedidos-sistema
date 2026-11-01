# LeoFit Solutions — Sistema Web PWA de Gestión de Pedidos y Control de Inventario Multicanal (`v2.0.0`)
## Universidad Tecnológica del Perú (UTP) — Curso Integrador II: Software (`100000S12F`)
**Docente Asesor:** Ing. Enrique L. Huamani U. | **Sección:** 35374 | **Grupo:** 01  
**Organización GitHub:** [`Leofit-Solutions-Grupo01`](https://github.com/Leofit-Solutions-Grupo01) | **Repositorio:** [`leofit-pedidos-sistema`](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema)

---

[![Entregable Final APF3](https://img.shields.io/badge/Informe%20Final%20APF3-100%25%20Completado%20(77%20p%C3%A1gs)-0F172A.svg)](docs/01_entregable_final_apf3/INFORME_FINAL_APF3_LEOFIT.docx)
[![Calidad ISO 25010](https://img.shields.io/badge/ISO%2FIEC%2025010-97.9%2F100%20(Grado%20A%2B)-15803D.svg)](docs/02_calidad_iso25010_semanas_10_11/README.md)
[![Pruebas Automatizadas](https://img.shields.io/badge/Tests%20Automatizados-194%20Passing%20(125%20BE%20%2B%2069%20FE)-1665D8.svg)](docs/04_diagramas_arquitectura_y_negocio/README.md)
[![Arquitectura](https://img.shields.io/badge/Architecture-Clean%20Architecture%20%2B%203FN%2FBCNF-1E3A8A.svg)](docs/04_diagramas_arquitectura_y_negocio/README.md)
[![Seguridad](https://img.shields.io/badge/Security-OWASP%20%7C%20JWT%20%7C%20HMAC%20%7C%20JCS-C2410C.svg)](SECURITY.md)
[![Demo PWA](https://img.shields.io/badge/Demo%20Live-PWA%20Online-15803D.svg)](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)

---

## 1. Ubicación Rápida de los Entregables para el Profesor (`docs/`)

Para facilitar la revisión inmediata, la carpeta [`docs/`](docs/README.md) está organizada numéricamente por orden de prioridad:

| Carpeta Numerada | Contenido Principal | Acceso Directo al Documento Principal |
| :--- | :--- | :--- |
| **[`docs/01_entregable_final_apf3/`](docs/01_entregable_final_apf3/)** | **Informe Final APF3 y Diapositivas de Sustentación** | [**`INFORME_FINAL_APF3_LEOFIT.docx`**](docs/01_entregable_final_apf3/INFORME_FINAL_APF3_LEOFIT.docx) · [**`.pdf`**](docs/01_entregable_final_apf3/INFORME_FINAL_APF3_LEOFIT.pdf) · [**`.md`**](docs/01_entregable_final_apf3/INFORME_FINAL_APF3_LEOFIT.md) <br> [**`APF3_LEOFIT_Presentacion.pptx`**](docs/01_entregable_final_apf3/presentacion_sustentacion/APF3_LEOFIT_Presentacion.pptx) · [**`.pdf`**](docs/01_entregable_final_apf3/presentacion_sustentacion/APF3_LEOFIT_Presentacion.pdf) |
| **[`docs/02_calidad_iso25010_semanas_10_11/`](docs/02_calidad_iso25010_semanas_10_11/)** | **Informe ISO/IEC 25010 (Sem. 10-11) y Manuales ISO 25000** | [**`INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx`**](docs/02_calidad_iso25010_semanas_10_11/INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx) · [**`.pdf`**](docs/02_calidad_iso25010_semanas_10_11/INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf) <br> [**`Manual_Calidad_ISO_25000_[Completo...].docx`**](docs/02_calidad_iso25010_semanas_10_11/Manual_Calidad_ISO_25000_Leofit_Pedidos_[Completo_Auditoria_y_ComiteTecnico].docx) <br> [**`Manual_Calidad_ISO_25000_[Ejecutivo...].docx`**](docs/02_calidad_iso25010_semanas_10_11/Manual_Calidad_ISO_25000_Leofit_Pedidos_[Ejecutivo_Gerencia_y_ProductOwner].docx) |
| **[`docs/03_auditoria_y_cierre_proyecto/`](docs/03_auditoria_y_cierre_proyecto/)** | **Dashboard Excel ISO 29119/90003, Cierre de Issues y Deuda Técnica** | [**`Plan_Auditoria_Software_LeoFit_Dashboard-Loayza-Lady.xlsx`**](docs/03_auditoria_y_cierre_proyecto/Plan_Auditoria_Software_LeoFit_Dashboard-Loayza-Lady.xlsx) · [**`DEUDA_TECNICA.md`**](docs/03_auditoria_y_cierre_proyecto/DEUDA_TECNICA.md) |
| **[`docs/04_diagramas_arquitectura_y_negocio/`](docs/04_diagramas_arquitectura_y_negocio/)** | **Catálogo de 25 Diagramas (C4, BPMN, 3FN, Secuencia, QA)** | [**`Catálogo Visual de Diagramas (README.md)`**](docs/04_diagramas_arquitectura_y_negocio/README.md) |
| **[`docs/05_operaciones_respaldo_drp/`](docs/05_operaciones_respaldo_drp/)** | **Protocolo y Simulacro de Recuperación ante Desastres (DRP)** | [**`BACKUP_RESTORE_DRILL.md`**](docs/05_operaciones_respaldo_drp/BACKUP_RESTORE_DRILL.md) |
| **[`docs/06_historial_entregas_anteriores_apf1_apf2/`](docs/06_historial_entregas_anteriores_apf1_apf2/)** | **Entregas Históricas APF1 y APF2 (Archivadas)** | [**`INFORME_FINAL_APF2_LEOFIT.docx`**](docs/06_historial_entregas_anteriores_apf1_apf2/INFORME_FINAL_APF2_LEOFIT.docx) |
| **[`docs/07_material_referencia_curso_utp/`](docs/07_material_referencia_curso_utp/)** | **Sílabo, Rúbricas UTP y Clases Teóricas (Semanas 01 a 18)** | [**`rubricas_evaluacion_utp/`**](docs/07_material_referencia_curso_utp/rubricas_evaluacion_utp/) |

---

## 2. Descripción del Proyecto

**LeoFit Solutions** es una plataforma web progresiva (PWA) de alto rendimiento conectada a una API RESTful v2.0.0 bajo **Clean Architecture** con persistencia transaccional en **PostgreSQL 16 (3FN/BCNF)**. La solución digitaliza el flujo integral de ventas, toma de pedidos, facturación electrónica SUNAT y control de existencias en tiempo real para la empresa textil deportiva **LeoFit Confecciones y Diseños Deportivos S.A.C.** (Emporio Comercial de Gamarra, La Victoria, Lima).

![Arquitectura Lógica de LeoFit](docs/04_diagramas_arquitectura_y_negocio/apf3/fig_arquitectura_logica.png)

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

![Distribución de 194 Pruebas por Suite](docs/04_diagramas_arquitectura_y_negocio/apf3/fig_pruebas_por_suite.png)

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

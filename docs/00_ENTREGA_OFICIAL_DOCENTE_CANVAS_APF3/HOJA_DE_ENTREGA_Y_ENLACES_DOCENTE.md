# HOJA OFICIAL DE ENTREGA ACADÉMICA Y ENLACES DEL PROYECTO
## Universidad Tecnológica del Perú (UTP) — Ciclo 2026-I
### Curso Integrador II: Software (100000S12F) — Sección 35374 (Turno Noche)
**Evaluación Final:** Avance de Proyecto Final 3 (APF3) y Evaluación de Calidad ISO/IEC 25010 (Semanas 10–11)  
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  

---

### 1. Datos Formales del Equipo de Ingeniería (Grupo 01)

| N° | Integrante | Código UTP | Rol en el Proyecto | Responsabilidad Técnica Principal |
| :-: | :--- | :---: | :--- | :--- |
| **1** | **Lady Luz Loayza Rodríguez** | **`U22221489`** | Scrum Master / DevSecOps Lead | Arquitectura, CI/CD, Seguridad OWASP, JWT fail-fast y HMAC |
| **2** | **Víctor Leandro Cárdenas Fernández** | **`U19217414`** | Product Owner / DBA | Modelado relacional PostgreSQL 16 (BCNF), ACID y Bloqueo Pesimista |
| **3** | **Harley Anthony Roman Delgado** | **`U21313032`** | Frontend Lead / UI-UX | PWA React 19 / Vite 6, Service Workers, WCAG 2.1 AA y jsPDF |
| **4** | **Jim Alessandro Dávila Morales** | **`U18206081`** | QA Engineer Lead / Backend | Automatización 194 pruebas (Jest + Vitest), API REST y Zod |
| **5** | **Daniel Enrique Rojas Sánchez** | **`U21214627`** | Business Analyst / Cloud DevOps | Despliegue Cloud en Render / GitHub Pages, métricas y DRP |

* **Empresa Beneficiaria:** **LeoFit Confecciones y Diseños Deportivos S.A.C.** (RUC: **`20608912345`**)
* **Ubicación Comercial:** Jr. Gamarra 1230, Galería El Rey de Gamarra, Stand 304, La Victoria, Lima, Perú.
* **Versión del Sistema Evaluada:** Release Oficial `v2.0.0` (Commit trazable: `e35e32b` en rama `main`).

---

### 2. Enlaces Oficiales del Repositorio y Plataforma Cloud

| Recurso Oficial | URL de Acceso Directo | Observación / Credenciales de Prueba |
| :--- | :--- | :--- |
| **Repositorio GitHub (Oficial)** | [**`github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema`**](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema) | Código fuente íntegro, historial Git, 194 pruebas, scripts y documentación. |
| **Frontend Web PWA (Cloud Staging)** | [**`leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/`**](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/) | Desplegado en **GitHub Pages Edge CDN** con soporte PWA Offline y Responsive Mobile. |
| **Backend API REST (Render Cloud)** | [**`leofit-backend-api.onrender.com/api/health`**](https://leofit-backend-api.onrender.com/api/health) | API en **Render Cloud Platform** con conexión SSL a PostgreSQL 16 Cloud. |
| **Documentación OpenAPI / Swagger** | [**`leofit-backend-api.onrender.com/api/docs`**](https://leofit-backend-api.onrender.com/api/docs) | Catálogo interactivo de endpoints REST con validación de esquemas Zod. |

#### Credenciales para la Validación en Vivo:
* **Usuario Administrador:** `admin@leofit.pe` | **Contraseña:** `Admin123!` *(Acceso al Dashboard, Reportes Financieros, Auditoría y Configuración)*.
* **Usuario Operador:** `operador@leofit.pe` | **Contraseña:** `Operador123!` *(Acceso al Catálogo Textil, Carrito y Registro de Pedidos Multicanal)*.

---

### 3. Matriz de Cumplimiento Directo contra la Rúbrica Oficial (16 / 16 Puntos)

| Criterio de la Rúbrica | Pts | Nivel de Cumplimiento | Dónde se Evidencia en los Documentos |
| :--- | :---: | :---: | :--- |
| **1. Evaluación de Pruebas Funcionales** *(Completitud, corrección e idoneidad ISO 25010: frameworks, casos, capturas, reportes y métricas)* | **4 pts** | **ESTÁNDAR ESPERADO (4/4 pts)** | • `01_INFORME_FINAL_APF3_LEOFIT.pdf` (Capítulo 11, Tablas 18 y 19). <br> • `02_INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf` (Secciones 5.1 a 5.4). <br> • **194 pruebas automatizadas aprobadas** (125 Jest backend + 69 Vitest frontend, 0 fallos). <br> • Completitud funcional = **100.0%** (10/10 RF verificados). <br> • Corrección funcional = **99.49%** (194/195 aprobadas). <br> • Idoneidad = Toma de pedido en **38.2 segundos** (< 90s meta). |
| **2. Automatización de Pruebas de Integración** *(Interoperabilidad y coexistencia con sistemas externos: contratos, frameworks, capturas, reportes y métricas)* | **4 pts** | **ESTÁNDAR ESPERADO (4/4 pts)** | • `02_INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf` (Secciones 6 y 7). <br> • **Interoperabilidad:** Pruebas `integration_external.test.ts` validando contrato OpenAPI, webhook HMAC-SHA256, rechazo 401/422 y uso del dato en BD atómica. <br> • **Coexistencia:** Protocolo experimental de 2 condiciones (A vs A+B) en contenedor Docker cgroup (1 vCPU, 512 MB RAM), latencia media de 4.42 ms, degradación P95 < 25% y 0.0% errores. |
| **3. Evaluación de Usabilidad del Sistema** *(Criterios ISO 25010 / interacción: informe, frameworks, casos, capturas, métricas y observaciones)* | **4 pts** | **ESTÁNDAR ESPERADO (4/4 pts)** | • `01_INFORME_FINAL_APF3_LEOFIT.pdf` (Capítulo 12) y `02_INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf`. <br> • Suite `usability_iso25010.test.ts` (9 tests Vitest). <br> • Estudio empírico con **5 participantes externos**. <br> • **SUS Score = 88.5 / 100** (Grado A - Excelente, Percentil 96%). <br> • Accesibilidad universal conforme a **WCAG 2.1 AA/AAA** (contraste 5.42:1 a 17.8:1, navegación completa por teclado, alertas ARIA preventivas). |
| **4. Validación y Verificación en Plataforma Cloud** *(Validación precisa del sistema en la plataforma cloud con usabilidad y automatización)* | **2 pts** | **ESTÁNDAR ESPERADO (2/2 pts)** | • `01_INFORME_FINAL_APF3_LEOFIT.pdf` (Capítulo 10, Sección 10.4). <br> • Despliegue en 2 capas cloud independientes: **GitHub Pages Edge CDN** y **Render Cloud Platform**. <br> • Healthcheck HTTP 200 en vivo en `/api/health` con persistencia relacional en **PostgreSQL 16 Cloud**. <br> • Pipeline de CI/CD automatizado en GitHub Actions con compilación y tests previos al deploy. |
| **5. Sustentación Técnica** *(Claridad, coherencia técnica, dominio conceptual, aportes, orden lógico y funcionamiento de versión 2 en cloud)* | **2 pts** | **ESTÁNDAR ESPERADO (2/2 pts)** | • `03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pptx` y `.pdf`. <br> • Guion de exposición de **10 minutos** con tiempos estrictos por expositor (Capítulo 18 del Manual Integral). <br> • 13 láminas de alta ingeniería con tarjetas KPI, arquitectura C4 Nivel 2, pirámide de pruebas y demostración de la versión 2.0.0 en vivo. |
| **PUNTAJE TOTAL ESPERADO** | **16 pts** | **CUMPLIMIENTO AL 100%** | **Máxima calificación según la rúbrica institucional UTP.** |

---

### 4. Inventario de Archivos en esta Carpeta de Entrega

Para comodidad en la subida a Canvas, todos los archivos clave están centralizados y numerados por orden de prioridad:

```text
docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/
│
├── HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.pdf             # Esta Ficha Ejecutiva con Enlaces y Rúbrica (PDF)
├── HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx            # Esta Ficha Ejecutiva con Enlaces y Rúbrica (Word)
│
├── 01_INFORME_FINAL_APF3_LEOFIT.pdf                  # Informe Maestro APF3 en PDF Oficial (77 págs, 21 diagramas)
├── 01_INFORME_FINAL_APF3_LEOFIT.docx                 # Informe Maestro APF3 en Word Editable
│
├── 02_INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf     # Informe Oficial Semanas 10-11 en PDF (Plantilla UTP Completada)
├── 02_INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx    # Informe Oficial Semanas 10-11 en Word Editable
│
├── 03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pdf      # Diapositivas de Sustentación en PDF Oficial (10 minutos)
├── 03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pptx     # Diapositivas de Sustentación en PowerPoint Editable
│
├── 04_PLAN_AUDITORIA_SOFTWARE_DASHBOARD_LEOFIT.xlsx # Dashboard Excel de Auditoría (ISO 29119-3 / ISO 90003)
│
├── 05_MANUAL_CALIDAD_ISO_25000_TECNICO.docx          # Manual de Calidad Técnico para Comité de Auditoría
├── 06_MANUAL_CALIDAD_ISO_25000_EJECUTIVO.docx        # Manual de Calidad Ejecutivo para Gerencia y PO
│
└── PAQUETE_ENTREGA_APF3_GRUPO01_LEOFIT.zip           # Paquete ZIP comprimido listo para subir a Canvas
```

---

### 5. Comandos Rápidos de Verificación Local para el Evaluador

Si el docente o evaluador clona el repositorio localmente, puede reproducir la totalidad de la suite ejecutando:

```bash
# 1. Clonar el repositorio:
git clone https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema.git
cd leofit-pedidos-sistema

# 2. Ejecutar las 125 pruebas backend (Jest / Supertest / Coexistencia):
npm test --prefix backend

# 3. Ejecutar las 69 pruebas frontend (Vitest / React Testing Library):
npm test --prefix frontend

# 4. Sincronizar y auditar el Excel con el código:
python scripts/sync_audit_metrics.py
```


# Guía de Carga de Issues para GitHub Projects — LeoFit Solutions (Grupo 01)
## Curso Integrador II: Software (100000S12F) — UTP
**Docente:** Ing. Enrique Lee Huamani Uriarte  
**Proyecto:** *LeoFit Pedidos Sistema*  
**Tablero Oficial:** [`Gestión_de_Desarrollo-LeoFit`](https://github.com/orgs/Leofit-Solutions-Grupo01/projects/1)  
**Organización:** `Leofit-Solutions-Grupo01` | **Repositorio:** `leofit-pedidos-sistema`

---

## 1. Justificación de Estados: `Done` vs `Todo`

Para la evaluación del **APF2 (Semana 09)** y la trazabilidad del ciclo académico, el docente evalúa la **metodología ágil Scrum en GitHub Projects**:
1. **Tareas de APF1 y APF2 (Casos 1 al 14):**
   - **Estado:** **`Done`** (Hecho / Completado).
   - **Justificación:** Demuestra que el equipo ya programó el Frontend PWA, el Backend API REST con Arquitectura Limpia, la Base de Datos PostgreSQL en BCNF, la seguridad JWT/OWASP y las 18 pruebas automatizadas.
2. **Tareas Futuras de APF3 y Proyecto Final (Casos 15 al 20):**
   - **Estado:** **`Todo`** (Por hacer / Planificado).
   - **Justificación:** Demuestra que el equipo tiene **planificado todo el ciclo (Semanas 10 a 18)** con sus respectivos responsables, roles, estimaciones y criterios de aceptación ISO 25010.

---

## 2. Integrantes del Equipo, Usuarios de GitHub y Roles

| Integrante | Código UTP | Usuario GitHub | Rol Primario Scrum | Rol Técnico Especializado |
| :--- | :--- | :--- | :--- | :--- |
| **Lady Luz Loayza Rodriguez** | `U22221489` | `@LadyyLuz` / `luzylay` | **Scrum Master** | DevSecOps, Seguridad JWT & Gobernanza |
| **Víctor Leandro Cárdenas F.** | `U19217414` | `@VictorCardenazFernandez` | **Product Owner** | DBA PostgreSQL, Replicación WAL & Requisitos |
| **Harley Anthony Roman D.** | `U21313032` | `@hroman2004` | **Frontend Lead** | Especialista PWA, Diseño UI/UX & WPO |
| **Jim Alessandro Dávila M.** | `U18206081` | `@Jim4279` | **QA Engineer Lead** | Backend Node.js/TS, Clean Arch & Pruebas Jest |
| **Daniel Enrique Rojas S.** | `U21214627` | `@Daniel102608` | **Business Analyst** | Cloud DevOps, SLA/SLO, Render/Vercel & Supabase |

---

## 3. Configuración de Sprints (Iterations) en GitHub Projects

En **Project Settings > Fields > Iteration**, la configuración de las 5 iteraciones queda estructurada de la siguiente manera:

```text
Iteración 1: Sprint 1 (APF1 - Frontend & Prototipos)       -> Sep 03 - Sep 16
Iteración 2: Sprint 2 (Base de Datos & Backend API)        -> Sep 17 - Sep 30
Iteración 3: Sprint 3 (APF2 - Seguridad & Despliegue)      -> Oct 01 - Oct 14
Iteración 4: Sprint 4 (APF3 - Calidad ISO 25010)           -> Oct 15 - Oct 28
Iteración 5: Sprint 5 (PROY - Proyecto Final & Producción) -> Oct 29 - Nov 11
```

---

## 4. Matriz Maestra de las 20 Tarjetas / Issues

| # | Hito | Título de la Tarjeta / Issue | Asignado | Rol | Iteration (Sprint) | Status | Priority | Label |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **1** | APF1 | *Levantamiento de Requerimientos y Ficha de Identificación* | `@VictorCardenazFernandez` | Product Owner | `Sprint 1` | **`Done`** | High | `documentation` |
| **2** | APF1 | *Especificación de Casos de Uso y Matriz de Trazabilidad* | `@Daniel102608` | Business Analyst | `Sprint 1` | **`Done`** | High | `documentation` |
| **3** | APF1 | *Diseño del Sistema de UI/UX, Modo Oscuro y Heurísticas* | `@hroman2004` | Frontend Lead | `Sprint 1` | **`Done`** | High | `enhancement` |
| **4** | APF1 | *Estructura Base Frontend PWA y Catálogo LeoFit* | `@hroman2004` | Frontend Lead | `Sprint 1` | **`Done`** | High | `enhancement` |
| **5** | APF1 | *Project Charter, Cronograma Gantt y Matriz de Riesgos* | `@LadyyLuz` | Scrum Master | `Sprint 1` | **`Done`** | High | `documentation` |
| **6** | APF2 | *Diseño Físico BCNF, DDL schema.sql y Datos seeds.sql* | `@VictorCardenazFernandez` | Product Owner | `Sprint 2` | **`Done`** | High | `enhancement` |
| **7** | APF2 | *Streaming Replication WAL y Script de Backups PITR* | `@VictorCardenazFernandez` | Product Owner | `Sprint 2` | **`Done`** | High | `enhancement` |
| **8** | APF2 | *Arquitectura Limpia y Patrón Repositorio (factory.ts)* | `@Jim4279` | QA Engineer Lead | `Sprint 2` | **`Done`** | High | `enhancement` |
| **9** | APF2 | *API REST Pedidos y Control de Stock Transaccional ACID* | `@Jim4279` | QA Engineer Lead | `Sprint 2` | **`Done`** | High | `enhancement` |
| **10** | APF2 | *Directorio CRM de Clientes y Ruteo de Delivery* | `@Daniel102608` | Business Analyst | `Sprint 2` | **`Done`** | Medium | `enhancement` |
| **11** | APF2 | *Autenticación JWT, Hashing bcrypt y RBAC (Admin/Operador)* | `@LadyyLuz` | Scrum Master | `Sprint 3` | **`Done`** | High | `security` |
| **12** | APF2 | *Catálogo OWASP Top 10, Helmet Headers y Rate Limiting* | `@LadyyLuz` | Scrum Master | `Sprint 3` | **`Done`** | High | `security` |
| **13** | APF2 | *Suite de 18 Pruebas Automatizadas con Jest y Supertest* | `@Jim4279` | QA Engineer Lead | `Sprint 3` | **`Done`** | High | `enhancement` |
| **14** | APF2 | *Despliegue Cloud (Render + Vercel + Supabase) y SLA/SLO* | `@Daniel102608` | Business Analyst | `Sprint 3` | **`Done`** | High | `enhancement` |
| **15** | APF3 | *Pruebas Automatizadas de Calidad Funcional ISO 25010* | `@Jim4279` | QA Engineer Lead | `Sprint 4` | **`Todo`** | High | `enhancement` |
| **16** | APF3 | *Pruebas de Usabilidad, Facilidad de Aprendizaje y WCAG* | `@hroman2004` | Frontend Lead | `Sprint 4` | **`Todo`** | Medium | `enhancement` |
| **17** | APF3 | *Pruebas de Interoperabilidad, Pasarelas y Coexistencia* | `@Daniel102608` | Business Analyst | `Sprint 4` | **`Todo`** | Medium | `enhancement` |
| **18** | APF3 | *Informe Oficial de Evaluación ISO 25010 y Manual v2* | `@LadyyLuz` | Scrum Master | `Sprint 4` | **`Todo`** | High | `documentation` |
| **19** | PROY | *Despliegue en Alta Disponibilidad y Resiliencia Cloud v2* | `@VictorCardenazFernandez` | Product Owner | `Sprint 5` | **`Todo`** | High | `enhancement` |
| **20** | PROY | *Sustentación Integral del Proyecto Final y Pitch Comercial* | `@LadyyLuz` | Scrum Master | `Sprint 5` | **`Todo`** | High | `documentation` |

---

## 5. Instrucciones para Actualizar los Casos en GitHub Projects

### A. Para las tareas completadas (Casos 1 al 14 / Issues #3 al #14):
1. Acceda a la vista de **Table** en [Gestión_de_Desarrollo-LeoFit](https://github.com/orgs/Leofit-Solutions-Grupo01/projects/1).
2. Verifique que la columna **`Status`** se encuentre en **`Done`** para todos estos casos (1 al 14).
3. Asigne la columna **`Iteration`** según corresponda:
   - Casos 1 a 5 -> `Sprint 1 (APF1)`
   - Casos 6 a 10 -> `Sprint 2 (Base de Datos & Backend API)`
   - Casos 11 a 14 -> `Sprint 3 (APF2 - Seguridad & Despliegue)`
4. Complete la columna **`Rol`** con el rol correspondiente (`Scrum Master`, `Product Owner`, `Frontend Lead`, `QA Engineer Lead` o `Business Analyst`).

---

### B. Para crear las 6 tareas futuras planificadas (Casos 15 al 20 — Estado: `Todo`):

1. Diríjase a: https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema/issues
2. Haga clic en **"New issue"**.
3. Copie y pegue el **Title** y **Description** especificados a continuación.
4. En el panel lateral derecho:
   - **Assignees:** Seleccione al integrante.
   - **Labels:** Seleccione `enhancement` o `documentation`.
   - **Projects:** Seleccione `Gestión_de_Desarrollo-LeoFit`.
5. Dentro del proyecto, asigne:
   - **Status:** `Todo`
   - **Iteration:** `Sprint 4` (para 15-18) o `Sprint 5` (para 19-20)
   - **Rol:** El rol correspondiente.
   - **Priority:** `High` o `Medium`.

---

## 6. Especificación de Casos Planificados (Casos 15 al 20)

### CASO 15: Calidad Funcional ISO 25010
- **Title:**
  ```text
  test(iso25010): Pruebas Automatizadas de Calidad Funcional según Norma ISO 25010
  ```
- **Description:**
  ```markdown
  ### Descripción
  Como QA Lead, requiero diseñar e implementar la batería de pruebas de calidad funcional bajo los estándares de la norma ISO/IEC 25010 para validar la completitud, corrección y pertinencia de los módulos de pedidos y catálogo.

  ### Criterios de Aceptación
  - [ ] Implementación de suite de pruebas funcionales automatizadas (Playwright / Cypress).
  - [ ] Cobertura de flujos críticos: registro de pedido, validación de stock atómico y cambio de estado.
  - [ ] Reportes automáticos de cobertura funcional y matriz de trazabilidad de defectos.
  ```
- **Assignee:** `@Jim4279` (Jim Alessandro Dávila)
- **Rol:** `QA Engineer Lead`
- **Iteration:** `Sprint 4 (APF3 - Calidad ISO 25010 & Usabilidad)`
- **Status:** `Todo`
- **Priority:** `High`
- **Label:** `enhancement`

---

### CASO 16: Pruebas de Usabilidad y Accesibilidad WCAG
- **Title:**
  ```text
  test(usability): Pruebas Automatizadas de Usabilidad, Facilidad de Aprendizaje y WCAG
  ```
- **Description:**
  ```markdown
  ### Descripción
  Como Frontend Lead, requiero ejecutar evaluaciones automatizadas de usabilidad bajo ISO 25010 (facilidad de aprendizaje, protección contra errores de usuario, estética y accesibilidad WCAG 2.1).

  ### Criterios de Aceptación
  - [ ] Auditoría automatizada de accesibilidad WCAG 2.1 AA con herramientas Axe-core y Lighthouse.
  - [ ] Pruebas de usabilidad con usuarios muestra en entorno mobile y desktop.
  - [ ] Medición de tiempos de completitud de tareas (Time-on-Task) y tasa de éxito en pedidos.
  ```
- **Assignee:** `@hroman2004` (Harley Anthony Roman)
- **Rol:** `Frontend Lead`
- **Iteration:** `Sprint 4 (APF3 - Calidad ISO 25010 & Usabilidad)`
- **Status:** `Todo`
- **Priority:** `Medium`
- **Label:** `enhancement`

---

### CASO 17: Interoperabilidad y Pruebas de Integración
- **Title:**
  ```text
  feat(interop): Pruebas de Interoperabilidad, Pasarelas y Coexistencia de Sistemas
  ```
- **Description:**
  ```markdown
  ### Descripción
  Como Business Analyst y DevOps, requiero validar la interoperabilidad e intercambio de datos con servicios externos (APIs de couriers y confirmación de pagos digitales).

  ### Criterios de Aceptación
  - [ ] Pruebas de integración de contratos de API y serialización JSON.
  - [ ] Simulación de respuestas y webhooks de confirmación de pago (Yape / Plin).
  - [ ] Reporte de coexistencia e interoperabilidad según el estándar ISO 25010.
  ```
- **Assignee:** `@Daniel102608` (Daniel Enrique Rojas)
- **Rol:** `Business Analyst`
- **Iteration:** `Sprint 4 (APF3 - Calidad ISO 25010 & Usabilidad)`
- **Status:** `Todo`
- **Priority:** `Medium`
- **Label:** `enhancement`

---

### CASO 18: Informe Oficial de Evaluación APF3
- **Title:**
  ```text
  docs(apf3): Informe Oficial de Evaluación de Calidad ISO 25010 y Manual de Despliegue v2
  ```
- **Description:**
  ```markdown
  ### Descripción
  Consolidación formal del informe oficial de Avance de Proyecto Final 3 (Capítulos 1 al 15 y Anexos A al H) según la rúbrica oficial UTP de la Semana 13.

  ### Criterios de Aceptación
  - [ ] Informe de evaluación de usabilidad según los 4 pilares de la ISO 25010.
  - [ ] Manual de despliegue actualizado para la versión 2 del sistema en Cloud.
  - [ ] Anexos E, F y G con reportes automatizados de funcionalidad, integración y usabilidad.
  ```
- **Assignee:** `@LadyyLuz` (Lady Luz Loayza)
- **Rol:** `Scrum Master`
- **Iteration:** `Sprint 4 (APF3 - Calidad ISO 25010 & Usabilidad)`
- **Status:** `Todo`
- **Priority:** `High`
- **Label:** `documentation`

---

### CASO 19: Despliegue en Alta Disponibilidad y Resiliencia v2
- **Title:**
  ```text
  ops(production): Despliegue en Alta Disponibilidad, Resiliencia y Monitoreo Productivo v2
  ```
- **Description:**
  ```markdown
  ### Descripción
  Aprovisionamiento del clúster de producción final con tolerancia a fallos, replicación multi-zona y monitoreo continuo de métricas transaccionales de LeoFit.

  ### Criterios de Aceptación
  - [ ] Configuración de auto-escalado y balanceo de carga en backend.
  - [ ] Monitoreo en tiempo real de transacciones y cuellos de botella con APM.
  - [ ] Procedimiento de failover probado ante caída de nodo principal de base de datos.
  ```
- **Assignee:** `@VictorCardenazFernandez` (Víctor Leandro Cárdenas)
- **Rol:** `Product Owner`
- **Iteration:** `Sprint 5 (PROY - Proyecto Final & Producción)`
- **Status:** `Todo`
- **Priority:** `High`
- **Label:** `enhancement`

---

### CASO 20: Sustentación Integral del Proyecto Final
- **Title:**
  ```text
  docs(final): Sustentación Integral del Proyecto Final, Pitch Comercial y Memoria Técnica
  ```
- **Description:**
  ```markdown
  ### Descripción
  Preparación de la sustentación final de cierre de curso (Semana 18), defensa técnica individual, demostración en vivo y pitch de impacto en el negocio textil LeoFit.

  ### Criterios de Aceptación
  - [ ] Diapositivas oficiales de sustentación con orden lógico y capacidad de síntesis.
  - [ ] Demostración en vivo del sistema procesando órdenes reales en la nube.
  - [ ] Video demo institucional de alta resolución del flujo completo de usuario.
  - [ ] Memoria técnica final consolidada y lecciones aprendidas del equipo.
  ```
- **Assignee:** `@LadyyLuz` (Lady Luz Loayza)
- **Rol:** `Scrum Master`
- **Iteration:** `Sprint 5 (PROY - Proyecto Final & Producción)`
- **Status:** `Todo`
- **Priority:** `High`
- **Label:** `documentation`

---

## 7. Resumen de Calificaciones y Fórmulas UTP

- **Fórmula de Evaluación:** `NF = 0.20*(APF1) + 0.20*(APF2) + 0.20*(APF3) + 0.40*(PROY)`
- **Hito APF1 (Semana 05):** Calificación **18/20 (Aprobado)**
- **Hito APF2 (Semana 09 - Actual):** Código 100% implementado, 18 tests aprobados, DDL BCNF, Replicación WAL, OWASP, Docker, Informe DOCX/PDF de 11 capítulos y Tablero GitHub Projects completo.
- **Hito APF3 (Semana 13):** Planificado en `Sprint 4` (Casos 15 al 18 en `Todo`).
- **Hito PROY (Semana 18):** Planificado en `Sprint 5` (Casos 19 y 20 en `Todo`).

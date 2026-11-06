# Directorio Maestro de Documentación — LeoFit Solutions (`v2.0.0`)
## Universidad Tecnológica del Perú (UTP) — Ciclo 2026-I
### Curso Integrador II: Software (100000S12F) — Sección 35374 (Turno Noche)
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  
**Equipo de Ingeniería (Grupo 01):**
* **Lady Luz Loayza Rodríguez** (`U22221489`) — Scrum Master / DevSecOps Lead
* **Víctor Leandro Cárdenas Fernández** (`U19217414`) — Product Owner / DBA
* **Harley Anthony Roman Delgado** (`U21313032`) — Frontend Lead / UI-UX
* **Jim Alessandro Dávila Morales** (`U18206081`) — QA Engineer Lead / Backend
* **Daniel Enrique Rojas Sánchez** (`U21214627`) — Business Analyst / Cloud DevOps

---

> [!NOTE]
> **Nota de Evaluación:** El material del Proyecto Final (Semana 18) se encuentra fuera de este repositorio por política de evaluación. La documentación visible en este repositorio corresponde a la entrega evaluada de **Avance de Proyecto Final 3 (APF3)**, calidad ISO/IEC 25010, catálogo de diagramas y material de referencia institucional.

---

## Estructura de Documentación

Para facilitar la revisión por parte del tribunal evaluador y respetar el estándar de gobernanza documental, el repositorio organiza toda la evidencia en los siguientes módulos temáticos ordenados por ciclo de vida:

```text
docs/
├── 01_ENTREGA_OFICIAL_APF3/            [ENTREGA OFICIAL EVALUADA - APF3]
│   ├── README.md                      (Guía de entrega oficial APF3)
│   ├── 00_ENTREGA_OFICIAL_CANVAS/     (Paquete oficial entregado en Canvas para APF3)
│   ├── 01_DESARROLLO_Y_CALIDAD/       (Informe maestro APF3 de 77 páginas y enlaces)
│   └── 02_ESTRUCTURA_ACADEMICA/       (Estructura de 7 carpetas según rúbrica UTP)
│
├── 02_CALIDAD_Y_AUDITORIA/            [CALIDAD E INGENIERÍA]
│   ├── 02_calidad_iso25010_semanas_10_11/ (Informe de Calidad ISO 25010 y Coexistencia)
│   ├── 03_auditoria_y_cierre_proyecto/    (Dashboard Excel ISO 29119 y Deuda Técnica)
│   └── 05_operaciones_respaldo_drp/       (Protocolo de Continuidad y Simulacro DRP)
│
├── 03_ARQUITECTURA_Y_DIAGRAMAS/       [MODELADO VISUAL]
│   └── README.md                      (Catálogo de 25+ Diagramas C4, BPMN, 3FN y Secuencia)
│
├── 04_REFERENCIA_CURSO_UTP/           [REFERENCIA ACADÉMICA]
│   ├── manuales_docente_enrique_lee/  (Manuales de cátedra del docente asesor)
│   ├── rubricas_evaluacion_utp/       (Rúbricas institucionales de evaluación)
│   ├── silabo_y_plantillas_utp/       (Sílabo oficial y plantillas universitarias)
│   └── clases_teoricas_semanas_01_a_18/ (Material de clases semanales)
│
├── adr/                               [ESTÁNDAR MADR CANÓNICO]
│   ├── ADR-001_ELECCION_RENDER_NEON_VS_AWS.md (Decisión Render+Neon vs AWS)
│   └── ADR-002_ARQUITECTURA_OBJETIVO_AWS.md   (Arquitectura Objetivo AWS y Complementos)
│
└── 99_HISTORICO_ENTREGAS_ANTERIORES/  [HISTÓRICO ARCHIVADO]
    └── APF1_APF2/                     (Entregas históricas iniciales archivadas)
```

---

## 1. Orden de Lectura Recomendado para el Evaluador

1. **Paso 1 (Entrega Principal APF3):** Iniciar en [**`01_ENTREGA_OFICIAL_APF3/`**](./01_ENTREGA_OFICIAL_APF3/README.md), donde se encuentra el Informe Maestro APF3 de 77 páginas, las diapositivas de sustentación y los accesos al sistema desplegado en vivo.
2. **Paso 2 (Auditoría de Calidad ISO 25010):** Consultar [**`02_CALIDAD_Y_AUDITORIA/`**](./02_CALIDAD_Y_AUDITORIA/) para auditar los resultados de las pruebas automatizadas (190 tests aprobados), coexistencia experimental Docker y plan de mitigación de deuda técnica.
3. **Paso 3 (Modelado y Diagramación):** Inspeccionar el catálogo gráfico de arquitectura en [**`03_ARQUITECTURA_Y_DIAGRAMAS/`**](./03_ARQUITECTURA_Y_DIAGRAMAS/README.md) con 25 diagramas técnicos (C4 Model, BPMN, modelo entidad-relación 3FN/BCNF).
4. **Paso 4 (Decisiones Arquitectónicas):** Revisar las decisiones de infraestructura en [**`adr/`**](./adr/) documentadas bajo formato MADR (ADR-001 y ADR-002).
5. **Paso 5 (Material de Referencia):** Consultar [**`04_REFERENCIA_CURSO_UTP/`**](./04_REFERENCIA_CURSO_UTP/) para contrastar contra el sílabo y las rúbricas institucionales UTP.
6. **Paso 6 (Histórico de Entregas Previas):** Para cotejar el avance continuo del proyecto frente a evaluaciones previas, consultar [**`99_HISTORICO_ENTREGAS_ANTERIORES/`**](./99_HISTORICO_ENTREGAS_ANTERIORES/).

---

## 2. Matriz Resumen de Navegación Rápida

| Módulo / Bucket | Contenido Principal | Acceso Directo |
| :--- | :--- | :--- |
| **01. Entrega Oficial APF3** | Informe Maestro (77 págs), Diapositivas, Paquete Canvas y Estructura Académica. | [**`01_ENTREGA_OFICIAL_APF3/`**](./01_ENTREGA_OFICIAL_APF3/README.md) |
| **02. Calidad y Auditoría** | Evaluación ISO 25010 (SUS 88.5/100, WCAG 2.1), Coexistencia Docker y Protocolo DRP. | [**`02_CALIDAD_Y_AUDITORIA/`**](./02_CALIDAD_Y_AUDITORIA/) |
| **03. Arquitectura y Diagramas** | Catálogo oficial de 25+ diagramas BPMN AS-IS/TO-BE, C4 Nivel 2 y 3FN. | [**`03_ARQUITECTURA_Y_DIAGRAMAS/`**](./03_ARQUITECTURA_Y_DIAGRAMAS/README.md) |
| **04. Referencia Curso UTP** | Manuales del docente Enrique Lee, rúbricas de evaluación institucional y sílabo. | [**`04_REFERENCIA_CURSO_UTP/`**](./04_REFERENCIA_CURSO_UTP/) |
| **ADR Canónico** | Registros de Decisiones Arquitectónicas según estándar MADR. | [**`adr/`**](./adr/) |
| **99. Histórico Consolidado** | Archivo completo de entregables previos (APF1 y APF2). | [**`99_HISTORICO_ENTREGAS_ANTERIORES/`**](./99_HISTORICO_ENTREGAS_ANTERIORES/) |

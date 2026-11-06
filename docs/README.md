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

## Estructura de Documentación en 5 Buckets + Histórico Consolidado

Para facilitar la revisión por parte del tribunal evaluador y respetar el estándar de gobernanza documental, el repositorio organiza toda la evidencia en 5 módulos temáticos ordenados por ciclo de vida:

```text
docs/
├── 01_PROYECTO_FINAL_SEMANA_18/       [BUCKET 1: VIGENTE - EVALUACIÓN FINAL]
│   ├── README.md                      (Guía de evaluación, alcance e inclusiones)
│   ├── 00_HOJA_DE_ENTREGA...md        (Ficha oficial con credenciales y URLs cloud)
│   ├── 01_ANEXOS_TECNICOS/            (Los 6 Anexos Técnicos de Sustentación)
│   ├── 02_ENTREGABLES_UTP/            (Formatos compilados Word, PPTX y Excel)
│   └── 03_AUDITORIA_READONLY/         (Inventario real del código fuente)
│
├── 02_CALIDAD_Y_AUDITORIA/            [BUCKET 2: CALIDAD E INGENIERÍA]
│   ├── 02_calidad_iso25010_semanas_10_11/ (Informe de Calidad ISO 25010 y Coexistencia)
│   ├── 03_auditoria_y_cierre_proyecto/    (Dashboard Excel ISO 29119 y Deuda Técnica)
│   └── 05_operaciones_respaldo_drp/       (Protocolo de Continuidad y Simulacro DRP)
│
├── 03_ARQUITECTURA_Y_DIAGRAMAS/       [BUCKET 3: MODELADO VISUAL]
│   └── README.md                      (Catálogo de 25+ Diagramas C4, BPMN, 3FN y Secuencia)
│
├── 04_REFERENCIA_CURSO_UTP/           [BUCKET 4: REFERENCIA ACADÉMICA]
│   ├── manuales_docente_enrique_lee/  (Manuales de cátedra del docente asesor)
│   ├── rubricas_evaluacion_utp/       (Rúbricas institucionales de evaluación)
│   ├── silabo_y_plantillas_utp/       (Sílabo oficial y plantillas universitarias)
│   └── clases_teoricas_semanas_01_a_18/ (Material de clases semanales)
│
├── adr/                               [ESTÁNDAR MADR CANÓNICO]
│   ├── ADR-001_ELECCION_RENDER_NEON_VS_AWS.md
│   └── ADR-002_ARQUITECTURA_OBJETIVO_AWS.md
│
└── 99_HISTORICO_ENTREGAS_ANTERIORES/  [BUCKET 5: HISTÓRICO CONSOLIDADO]
    ├── APF3/
    │   ├── 00_ENTREGA_OFICIAL_CANVAS/ (Paquete oficial entregado en Canvas para APF3)
    │   ├── 01_DESARROLLO_Y_CALIDAD/   (Informe maestro APF3 de 77 páginas)
    │   └── 02_ESTRUCTURA_ACADEMICA/   (Estructura de 7 carpetas según pág. 35)
    └── APF1_APF2/                     (Entregas históricas iniciales archivadas)
```

---

## 1. Orden de Lectura Recomendado para el Jurado Evaluador

1. **Paso 1 (Evaluación Inmediata):** Iniciar en [**`01_PROYECTO_FINAL_SEMANA_18/`**](./01_PROYECTO_FINAL_SEMANA_18/README.md), donde se encuentra la Ficha Oficial de Entrega con los accesos directos al sistema en vivo (Render API y GitHub Pages PWA).
2. **Paso 2 (Defensa de Arquitectura):** Revisar los 6 anexos en [**`01_ANEXOS_TECNICOS/`**](./01_PROYECTO_FINAL_SEMANA_18/01_ANEXOS_TECNICOS/README.md) para verificar las respuestas a las preguntas del jurado (Render vs AWS, SUNAT UBL 2.1, pasarela Culqi y C4 Model).
3. **Paso 3 (Revisión de Formatos Office):** Descargar los documentos de sustentación desde [**`02_ENTREGABLES_UTP/`**](./01_PROYECTO_FINAL_SEMANA_18/02_ENTREGABLES_UTP/) (`01_DOCX`, `02_PPTX` de 20 láminas con notas y `03_XLSX` de auditoría).
4. **Paso 4 (Auditoría de Calidad):** Consultar [**`02_CALIDAD_Y_AUDITORIA/`**](./02_CALIDAD_Y_AUDITORIA/) para auditar los resultados de las 190 pruebas automatizadas y la evaluación ISO/IEC 25010.
5. **Paso 5 (Modelado y Diagramación):** Inspeccionar el catálogo gráfico de arquitectura en [**`03_ARQUITECTURA_Y_DIAGRAMAS/`**](./03_ARQUITECTURA_Y_DIAGRAMAS/README.md).
6. **Paso 6 (Trazabilidad Histórica):** Para cotejar el avance continuo del proyecto frente a entregables previos, consultar [**`99_HISTORICO_ENTREGAS_ANTERIORES/`**](./99_HISTORICO_ENTREGAS_ANTERIORES/).

---

## 2. Matriz Resumen de Navegación Rápida

| Módulo / Bucket | Contenido Principal | Acceso Directo |
| :--- | :--- | :--- |
| **01. Proyecto Final (Semana 18)** | Hoja de Entrega, 6 Anexos Técnicos, Paquete Office y Auditoría Read-Only. | [**`01_PROYECTO_FINAL_SEMANA_18/`**](./01_PROYECTO_FINAL_SEMANA_18/README.md) |
| **02. Calidad y Auditoría** | Evaluación ISO 25010 (SUS 88.5/100, WCAG 2.1), Coexistencia Docker y Protocolo DRP. | [**`02_CALIDAD_Y_AUDITORIA/`**](./02_CALIDAD_Y_AUDITORIA/) |
| **03. Arquitectura y Diagramas** | Catálogo oficial de 25+ diagramas BPMN AS-IS/TO-BE, C4 Nivel 2 y 3FN. | [**`03_ARQUITECTURA_Y_DIAGRAMAS/`**](./03_ARQUITECTURA_Y_DIAGRAMAS/README.md) |
| **04. Referencia Curso UTP** | Manuales del docente Enrique Lee, rúbricas de evaluación institucional y sílabo. | [**`04_REFERENCIA_CURSO_UTP/`**](./04_REFERENCIA_CURSO_UTP/) |
| **ADR Canónico** | Registros de Decisiones Arquitectónicas según estándar MADR. | [**`adr/`**](./adr/) |
| **99. Histórico Consolidado** | Archivo completo de entregables previos (APF1, APF2 y APF3 Canvas). | [**`99_HISTORICO_ENTREGAS_ANTERIORES/`**](./99_HISTORICO_ENTREGAS_ANTERIORES/) |

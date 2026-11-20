# Directorio Maestro de Documentación — LeoFit Solutions (`v2.4.0`)
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

> [!IMPORTANT]
> **Acceso Inmediato para el Docente Evaluador:**  
> Consulte el documento [**`00_INDICE_MAESTRO_ENTREGABLES_DOCENTE.md`**](00_INDICE_MAESTRO_ENTREGABLES_DOCENTE.md) para acceder directamente a cada informe, presentación, rúbrica y evidencia del curso.

---

## Estructura Consolidada de la Documentación

La documentación de este repositorio organiza toda la evidencia acumulativa del ciclo en los siguientes módulos temáticos ordenados cronológicamente:

```text
docs/
├── 00_INDICE_MAESTRO_ENTREGABLES_DOCENTE.md   [ÍNDICE EJECUTIVO PARA EL PROFESOR]
├── INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.docx  [INFORME ACUMULATIVO WORD OFICIAL]
├── INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.md    [MEMORIA TÉCNICA MARKDOWN]
├── 03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx [PRESENTACIÓN OFICIAL 25 SLIDES]
├── 03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.html [VISOR WEB INTERACTIVO]
├── 03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.md   [GUION Y TRANSCRIPCIÓN PPTX]
│
├── Guia_Libro_Semanas_14_15_Curso_Integrador_II_UTP.pdf     [MATERIAL DOCENTE LEE]
├── PPT_Breve_Semanas_14_15_Curso_Integrador_II_UTP.pdf      [MATERIAL DOCENTE LEE]
├── Plantilla_Informe_Continuacion_S14_S15_UTP.docx          [PLANTILLA OFICIAL UTP]
│
├── 01_ENTREGA_OFICIAL_APF3/            [ENTREGA OFICIAL EVALUADA - APF3]
│   ├── README.md                      (Guía de entrega oficial APF3)
│   ├── 00_ENTREGA_OFICIAL_CANVAS/     (Paquete oficial entregado en Canvas para APF3)
│   ├── 01_DESARROLLO_Y_CALIDAD/       (Informe maestro APF3 de 77 páginas y enlaces)
│   └── 02_ESTRUCTURA_ACADEMICA/       (Estructura de 7 carpetas según rúbrica UTP)
│
├── 02_CALIDAD_Y_AUDITORIA/            [CALIDAD E INGENIERÍA]
│   ├── 01_plan_de_pruebas_iso29119/    (Plan Maestro de Pruebas ISO/IEC/IEEE 29119-3/4)
│   ├── 02_calidad_iso25010_semanas_10_11/ (Informe de Calidad ISO 25010 y Coexistencia)
│   ├── 03_auditoria_y_cierre_proyecto/    (Dashboard Excel ISO 29119 y Deuda Técnica)
│   └── 05_operaciones_respaldo_drp/       (Protocolo de Continuidad y Simulacro DRP)
│
├── 03_ARQUITECTURA_Y_DIAGRAMAS/       [CATÁLOGO DE 25 DIAGRAMAS DE INGENIERÍA]
│   ├── apf3/                          (Diagramas compilados en alta resolución PNG)
│   └── README.md                      (Catálogo visual documentado con C4 y BPMN)
│
├── 04_REFERENCIA_CURSO_UTP/           [MATERIAL INSTITUCIONAL UTP]
│   ├── rubricas_evaluacion_utp/       (Rúbricas oficiales APF1, APF2 y APF3)
│   ├── manuales_docente_enrique_lee/  (Libros y manuales ISO 25010 del docente)
│   └── silabo_y_plantillas_utp/       (Sílabo oficial y plantillas)
│
├── adr/                               [DECISIONES ARQUITECTÓNICAS (MADR)]
│   ├── ADR-001_ELECCION_RENDER_NEON_VS_AWS.md
│   └── ADR-002_ARQUITECTURA_OBJETIVO_AWS.md
│
└── 99_HISTORICO_ENTREGAS_ANTERIORES/  [ARCHIVO HISTÓRICO]
    └── APF1_APF2/                     (Informes y presentaciones de APF1 y APF2)
```

---

## Resumen de Hitos y Entregables Principales

| Hito | Documento Principal | Descripción de Contenido |
| :--- | :--- | :--- |
| **Sustentación Final (Semana 18)** | [**`03_PRESENTACION_OFICIAL...pptx`**](03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx) <br> [**`Visor Web HTML`**](03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.html) | Deck de 25 diapositivas ejecutivas con notas de orador completas, tablas dinámicas y paleta accesible WCAG AAA. |
| **Continuación Semanas 14 y 15 (Unidad 4)** | [**`INFORME_CONTINUACION...docx`**](INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.docx) <br> [**`Memoria Markdown`**](INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.md) | Evaluación bajo ISO/IEC 25010: Rendimiento (k6 p50/p95), Flexibilidad (Adaptabilidad/Escalabilidad), Mantenibilidad (TDD) y Confiabilidad (HA vs HPC). |
| **Avance Final APF3** | [**`INFORME_FINAL_APF3...docx`**](01_ENTREGA_OFICIAL_APF3/01_DESARROLLO_Y_CALIDAD/INFORME_FINAL_APF3_LEOFIT.docx) | Memoria técnica de 77 páginas con adecuación funcional 100%, compatibilidad Docker, usabilidad SUS 88.5/100 y DRP RTO 3.2s. |
| **Decisiones de Arquitectura** | [**`ADR-001`**](adr/ADR-001_ELECCION_RENDER_NEON_VS_AWS.md) <br> [**`ADR-002`**](adr/ADR-002_ARQUITECTURA_OBJETIVO_AWS.md) | Justificación de Render+Neon vs AWS y maquetación de arquitectura objetivo VPC Multi-AZ en AWS. |

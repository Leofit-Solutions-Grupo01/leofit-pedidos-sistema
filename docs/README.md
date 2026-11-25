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
> Todos los entregables oficiales de la **Entrega Final y Sustentación del Proyecto (Semana 18)** se encuentran centralizados en [**`01_ENTREGA_FINAL_PROYECTO_SEMANA_18/`**](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/).  
> También puede consultar el índice rápido en [**`00_INDICE_MAESTRO_ENTREGABLES_DOCENTE.md`**](00_INDICE_MAESTRO_ENTREGABLES_DOCENTE.md).

---

## Estructura Consolidada de la Documentación

La documentación de este repositorio organiza toda la evidencia técnica acumulativa del ciclo de forma limpia, modular y jerárquica:

```text
docs/
├── 00_INDICE_MAESTRO_ENTREGABLES_DOCENTE.md       [ÍNDICE EJECUTIVO PARA EL PROFESOR]
├── README.md                                      [ESTE DIRECTORIO MAESTRO]
│
├── 01_ENTREGA_FINAL_PROYECTO_SEMANA_18/           [PAQUETE OFICIAL DE ENTREGA FINAL Y SUSTENTACIÓN]
│   ├── README.md                                  (Guía de evaluación del paquete final)
│   ├── 00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx  (Carátula oficial, credenciales y checklist)
│   ├── 00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.pdf   (Versión PDF lista para impresión/revisión)
│   ├── 00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.md    (Versión Markdown auditable)
│   ├── 01_INFORME_FINAL_LEOFIT.docx               (Informe General Final completo del proyecto en APA 7)
│   ├── 01_INFORME_FINAL_LEOFIT.pdf                (Versión PDF oficial del Informe General)
│   ├── 02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx (Informe Acumulativo S14-S15 en APA 7)
│   ├── 02_INFORME_CONTINUACION_S14_S15_LEOFIT.pdf (Versión PDF oficial del Informe S14-S15)
│   ├── 02_INFORME_CONTINUACION_S14_S15_LEOFIT.md  (Memoria técnica en Markdown)
│   ├── 03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx (Presentación ejecutiva de 25 diapositivas)
│   ├── 03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pdf  (Presentación en formato PDF de alta resolución)
│   ├── 03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.md   (Guion y estructura de diapositivas)
│   ├── 03_VISOR_WEB_PRESENTACION_SUSTENTACION.html (Visor web interactivo responsive)
│   ├── 04_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx (Dashboard Excel con 7 hojas)
│   ├── 04_COMPENDIO_TECNICO_CALIDAD_TESTING_Y_CRIPTOGRAFIA.md (Compendio S21-S29 y Cripto SSL/TLS)
│   ├── graficos/                                  (6 gráficos científicos de calidad a 300 DPI)
│   └── anexos_tecnicos/                           (7 anexos de respuestas técnicas al jurado)
│
├── 02_CALIDAD_Y_AUDITORIA/                        [EVIDENCIAS DE CALIDAD Y PRUEBAS]
│   ├── 01_plan_de_pruebas_iso29119/               (Plan Maestro de Pruebas ISO/IEC/IEEE 29119-3/4)
│   ├── 02_calidad_iso25010_semanas_10_11/         (Informe de Calidad ISO 25010 y Coexistencia)
│   ├── 03_auditoria_y_cierre_proyecto/            (Checklist de auditoría y actas de cierre)
│   ├── 05_operaciones_respaldo_drp/               (Protocolo de Continuidad y Simulacro DRP)
│   ├── METRICAS_SESION_28_UTP/                    (Métricas de Rendimiento y Evidencia Sesión 28)
│   └── README.md                                  (Índice de marcos de calidad y estándares)
│
├── 03_ARQUITECTURA_Y_DIAGRAMAS/                   [CATÁLOGO DE 25 DIAGRAMAS DE INGENIERÍA]
│   ├── apf3/                                      (Diagramas compilados en alta resolución PNG)
│   └── README.md                                  (Catálogo visual documentado con C4 y BPMN)
│
├── 04_REFERENCIA_CURSO_UTP/                       [MATERIAL INSTITUCIONAL UTP]
│   ├── clases_teoricas_semanas_01_a_18/           (Diapositivas teóricas de las semanas 1 a 18)
│   ├── manuales_docente_enrique_lee/              (Libros, manuales y PPTs del docente Lee Huamani)
│   ├── rubricas_evaluacion_utp/                   (Rúbricas oficiales APF1, APF2 y APF3)
│   └── silabo_y_plantillas_utp/                   (Sílabo oficial y plantillas institucionales)
│
├── adr/                                           [DECISIONES ARQUITECTÓNICAS (MADR)]
│   ├── ADR-001_ELECCION_RENDER_NEON_VS_AWS.md
│   └── ADR-002_ARQUITECTURA_OBJETIVO_AWS.md
│
└── 99_HISTORICO_ENTREGAS_ANTERIORES/              [ARCHIVO HISTÓRICO DE ENTREGAS]
    ├── APF1_APF2/                                 (Informes y presentaciones de APF1 y APF2)
    └── APF3/                                      (Paquete completo del Avance Final 3)
```

---

## Resumen de Hitos y Entregables Principales

| Hito | Documento Principal | Descripción de Contenido |
| :--- | :--- | :--- |
| **Entrega Final y Sustentación (Semana 18)** | [**`01_INFORME_FINAL_LEOFIT`**](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/01_INFORME_FINAL_LEOFIT.docx) ([PDF](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/01_INFORME_FINAL_LEOFIT.pdf)) <br> [**`02_INFORME_CONTINUACION_S14_S15_LEOFIT`**](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx) ([PDF](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/02_INFORME_CONTINUACION_S14_S15_LEOFIT.pdf)) <br> [**`03_PRESENTACION_OFICIAL_SUSTENTACION`**](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx) ([PDF](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pdf) · [HTML](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/03_VISOR_WEB_PRESENTACION_SUSTENTACION.html)) <br> [**`Carpeta Oficial S18`**](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/) | Paquete completo y definitivo del proyecto: memoria acumulativa integral, informe de continuación de calidad S14-S15, presentación de 25 diapositivas ejecutivas con notas de orador, y libro de auditoría Excel con 7 hojas. |
| **Calidad ISO 25010 (Unidad 4)** | [**`02_INFORME_CONTINUACION_S14_S15_LEOFIT`**](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx) ([PDF](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/02_INFORME_CONTINUACION_S14_S15_LEOFIT.pdf)) <br> [**`Carpeta Oficial S18`**](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/) | Evaluación bajo ISO/IEC 9126 (partes 1-4, fórmulas $X=1-A/B$, $X=A/B$) e ISO/IEC 25010:2023: Rendimiento SRE (k6 p50/p95/p99), Flexibilidad (Circuit Breaker/Bulkhead/Auto-scaling), Mantenibilidad (McCabe 1-3, 194 tests) y Confiabilidad (HA vs HPC). |
| **Histórico Avance APF3** | [**`APF3/`**](99_HISTORICO_ENTREGAS_ANTERIORES/APF3/) | Memoria técnica de 77 páginas con adecuación funcional 100%, compatibilidad Docker, usabilidad SUS 88.5/100 y DRP RTO 3.2s. |
| **Decisiones de Arquitectura** | [**`ADR-001`**](adr/ADR-001_ELECCION_RENDER_NEON_VS_AWS.md) <br> [**`ADR-002`**](adr/ADR-002_ARQUITECTURA_OBJETIVO_AWS.md) | Justificación de Render+Neon vs AWS y maquetación de arquitectura objetivo VPC Multi-AZ en AWS. |

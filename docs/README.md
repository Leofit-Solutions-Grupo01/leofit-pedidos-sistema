# Directorio Maestro de Documentación — LeoFit Solutions (`v2.0.0`)
## Curso Integrador II: Software (100000S12F) — Ciclo 2026-I — UTP
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  
**Equipo de Ingeniería (Grupo 01):**
* **Lady Luz Loayza Rodríguez** (`U22221489`) — Scrum Master / DevSecOps Lead
* **Víctor Leandro Cárdenas Fernández** (`U19217414`) — Product Owner / DBA
* **Harley Anthony Roman Delgado** (`U21313032`) — Frontend Lead / UI-UX
* **Jim Alessandro Dávila Morales** (`U18206081`) — QA Engineer Lead / Backend
* **Daniel Enrique Rojas Sánchez** (`U21214627`) — Business Analyst / Cloud DevOps

---

## 1. Entregas Oficiales para Evaluación Docente (Canvas UTP)

Las siguientes carpetas contienen los paquetes consolidados listos para calificación institucional:

| Carpeta Oficial | Propósito y Contenido Principal | Acceso Directo |
| :--- | :--- | :--- |
| [**`00_ENTREGA_OFICIAL_PROYECTO_FINAL_SEMANA_18/`**](./00_ENTREGA_OFICIAL_PROYECTO_FINAL_SEMANA_18/) | **ENTREGA FINAL (PROY - SEMANA 18)**: Ficha oficial de sustentación, enlaces cloud, credenciales y paquete completo en `entregables_utp/` (`01_DOCX`, `02_PPTX`, `03_XLSX`). | [**`00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.md`**](./00_ENTREGA_OFICIAL_PROYECTO_FINAL_SEMANA_18/00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.md) <br> [**`entregables_utp/`**](./00_ENTREGA_OFICIAL_PROYECTO_FINAL_SEMANA_18/entregables_utp/) |
| [**`00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/`**](./00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/) | **ENTREGA HISTORICA (APF3)**: Paquete oficial evaluado para Canvas con informe, presentación, dashboard Excel y archivos empaquetados. | [**`00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx`**](./00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx) <br> [**`PAQUETE_ENTREGA_APF3_GRUPO01_LEOFIT.zip`**](./00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/PAQUETE_ENTREGA_APF3_GRUPO01_LEOFIT.zip) |
| [**`APF3_GRUPO_01/`**](./APF3_GRUPO_01/) | **Estructura Recomendada del Manual Docente (Pág. 35)**: Organizado en 7 subcarpetas académicas (`01_informe` a `07_anexos`). | [**`01_informe/`**](./APF3_GRUPO_01/01_informe/) |

---

## 2. Anexos Técnicos de Arquitectura y Sustentación (Proyecto Final)

Documentación técnica de nivel profesional y trazabilidad estricta al código fuente (`ruta:línea`) para responder a las preguntas críticas del jurado:

| Carpeta / Anexo | Título y Propósito | Pregunta del Jurado que Resuelve |
| :--- | :--- | :--- |
| [**`05_ANEXOS_TECNICOS_PROYECTO_FINAL/`**](./05_ANEXOS_TECNICOS_PROYECTO_FINAL/) | **Índice Maestro de Anexos Técnicos**: Compendio general y matriz de trazabilidad integral. | [**`README.md`**](./05_ANEXOS_TECNICOS_PROYECTO_FINAL/README.md) |
| [**`01_ADR-001...md`**](./05_ANEXOS_TECNICOS_PROYECTO_FINAL/01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md) | **Elección de Render + Neon PostgreSQL vs AWS**: Criterios de costo ($0-$14 vs $95-$140), Time-to-Market y umbrales de migración (>50 RPS / >5,000 DAU). | **Pregunta 1:** ¿Por qué Render+Neon y no AWS? |
| [**`02_ADR-002...md`**](./05_ANEXOS_TECNICOS_PROYECTO_FINAL/02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md) | **Arquitectura Objetivo Nativa en AWS**: C4 Contenedores, VPC Multi-AZ, ECS Fargate, Aurora y justificación de complementos no-AWS (Culqi, Nubefact OSE). | **Pregunta 2:** Maquetación 100% AWS y complementos. |
| [**`03_CUMPLIMIENTO_SUNAT_CPE.md`**](./05_ANEXOS_TECNICOS_PROYECTO_FINAL/03_CUMPLIMIENTO_SUNAT_CPE.md) | **Cumplimiento Normativo SUNAT para CPE**: UBL 2.1, certificado INDECOPI, flujo OSE, desglose 18% IGV y gap analysis del repositorio. | **Pregunta 3:** Cumplimiento normativo SUNAT. |
| [**`04_INTEGRACION_PAGOS...md`**](./05_ANEXOS_TECNICOS_PROYECTO_FINAL/04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md) | **Pasarela de Pagos Sandbox vs Producción**: Flujo con Culqi JS, reducción de alcance PCI-DSS (SAQ A), webhooks HMAC timing-safe y hoja de ruta comercial. | **Pregunta 4:** ¿Pagos reales o simulados y limitantes? |
| [**`05_ARQUITECTURA_REPO...md`**](./05_ANEXOS_TECNICOS_PROYECTO_FINAL/05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md) | **Arquitectura del Repositorio y Estándares**: Diagrama C4 real del sistema, Clean Architecture, estándares (arc42, MADR, SemVer) y onboarding < 1 día. | **Pregunta 5:** Estructura, comprensión y escalabilidad. |
| [**`06_MATRIZ_TRAZABILIDAD...md`**](./05_ANEXOS_TECNICOS_PROYECTO_FINAL/06_MATRIZ_TRAZABILIDAD_JURADO.md) | **Matriz Maestra de Trazabilidad**: Mapeo pregunta -> documento -> sección -> línea de código (`ruta:línea`) -> argumentario de defensa. | Matriz de síntesis integral para la defensa. |
| [**`adr/`**](./adr/) | **Registro Canónico de ADRs**: Decisiones arquitectónicas bajo estándar abierto MADR. | [**`ADR-001`**](./adr/ADR-001_ELECCION_RENDER_NEON_VS_AWS.md) · [**`ADR-002`**](./adr/ADR-002_ARQUITECTURA_OBJETIVO_AWS.md) |
| [**`_auditoria/`**](./_auditoria/) | **Auditoría Técnica Read-Only**: Inventario real del código fuente línea a línea. | [**`00_INVENTARIO_REAL.md`**](./_auditoria/00_INVENTARIO_REAL.md) |

---

## 3. Carpetas de Desarrollo, Ingeniería y Soporte (Numeradas del 01 al 07)

| # | Carpeta | Contenido Técnico | Documento Clave |
| :-: | :--- | :--- | :--- |
| **01** | [**`01_entregable_final_apf3/`**](./01_entregable_final_apf3/) | Informe Maestro APF3 (77 págs, 15 capítulos), fuentes Markdown y presentaciones auxiliares. | [**`INFORME_FINAL_APF3_LEOFIT.docx`**](./01_entregable_final_apf3/INFORME_FINAL_APF3_LEOFIT.docx) |
| **02** | [**`02_calidad_iso25010_semanas_10_11/`**](./02_calidad_iso25010_semanas_10_11/) | Informe de Calidad ISO 25010, manuales de calidad y datos crudos de coexistencia en Docker. | [**`INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx`**](./02_calidad_iso25010_semanas_10_11/INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx) |
| **03** | [**`03_auditoria_y_cierre_proyecto/`**](./03_auditoria_y_cierre_proyecto/) | Dashboard Excel de Auditoría (ISO 29119/90003), análisis de requisitos y registro de deuda técnica. | [**`Plan_Auditoria_Software_LeoFit_Dashboard-Loayza-Lady.xlsx`**](./03_auditoria_y_cierre_proyecto/Plan_Auditoria_Software_LeoFit_Dashboard-Loayza-Lady.xlsx) |
| **04** | [**`04_diagramas_arquitectura_y_negocio/`**](./04_diagramas_arquitectura_y_negocio/) | 25+ Diagramas Oficiales: BPMN AS-IS/TO-BE, C4 Nivel 2, 3FN/BCNF, Gantt, Kanban y flujos RBAC. | [**`Catálogo de Diagramas (README.md)`**](./04_diagramas_arquitectura_y_negocio/README.md) |
| **05** | [**`05_operaciones_respaldo_drp/`**](./05_operaciones_respaldo_drp/) | Protocolo de Continuidad y Simulacro de Recuperación ante Desastres (DRP, RTO 3.2s, RPO 0). | [**`BACKUP_RESTORE_DRILL.md`**](./05_operaciones_respaldo_drp/BACKUP_RESTORE_DRILL.md) |
| **06** | [**`06_historial_entregas_anteriores_apf1_apf2/`**](./06_historial_entregas_anteriores_apf1_apf2/) | Historial de entregas académicas pasadas (APF1 y APF2) archivadas para trazabilidad. | [**`INFORME_FINAL_APF2_LEOFIT.docx`**](./06_historial_entregas_anteriores_apf1_apf2/INFORME_FINAL_APF2_LEOFIT.docx) |
| **07** | [**`07_material_referencia_curso_utp/`**](./07_material_referencia_curso_utp/) | Material de cátedra UTP: Diapositivas semanales (Sem 01 a 18), rúbricas oficiales, sílabo y manuales del docente asesor. | [**`manuales_docente_enrique_lee/`**](./07_material_referencia_curso_utp/manuales_docente_enrique_lee/) <br> [**`rubricas_evaluacion_utp/`**](./07_material_referencia_curso_utp/rubricas_evaluacion_utp/) |

---

## 4. Cadena de Construcción de Entregables (build_all.ps1)

Para compilar y exportar automáticamente todos los documentos técnicos de Markdown hacia formatos oficiales de Microsoft Office (`.docx`, `.pptx`, `.xlsx`), se dispone del script maestro:

```powershell
# Ejecutar desde PowerShell en la raíz del proyecto
pwsh docs/00_ENTREGA_OFICIAL_PROYECTO_FINAL_SEMANA_18/entregables_utp/scripts/build_all.ps1
```

Este comando verifica dependencias (`pandoc`, `mmdc`, librerías Python), compila diagramas Mermaid a PNG en alta resolución, genera los 9 archivos Word, la presentación de 20 diapositivas con notas de orador y el libro Excel de auditoría, certificando cero errores y cero emojis.

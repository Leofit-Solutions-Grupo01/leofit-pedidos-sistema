# GUÍA Y MAPA DE ENTREGABLES ACADÉMICOS PARA EL DOCENTE EVALUADOR
## Curso Integrador II: Software (100000S12F) — Ciclo 2026-I
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  
**Equipo de Ingeniería (Grupo 01):** Lady Loayza, Víctor Cárdenas, Harley Roman, Jim Dávila, Daniel Rojas  
**Organización y Repositorio:** [`Leofit-Solutions-Grupo01/leofit-pedidos-sistema`](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema)  

---

Estimado docente Ing. Enrique Lee Huamani, este documento consolida el índice unificado, directo y actualizado de todos los entregables académicos y técnicos desarrollados para la **Entrega Final y Sustentación del Proyecto (Semana 18)**, organizados para facilitar la revisión, auditoría y calificación según las rúbricas institucionales de la UTP.

---

## 1. Paquete Oficial de Entrega Final y Sustentación (Semana 18)

Todos los entregables principales que conforman la evaluación final del proyecto se encuentran organizados y disponibles en la carpeta principal [`docs/01_ENTREGA_FINAL_PROYECTO_SEMANA_18/`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/):

| N° | Entregable Oficial | Formato | Enlace Directo | Descripción y Métricas Clave |
| :-: | :--- | :---: | :--- | :--- |
| **00** | **Hoja Oficial de Entrega y Enlaces** | DOCX / MD | [`00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx)<br>[`00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.md`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.md) | Carátula formal de entrega con datos de integrantes, roles, enlaces cloud activos, credenciales y checklist de verificación. |
| **01** | **Informe General Final del Proyecto** | DOCX | [`01_INFORME_FINAL_LEOFIT.docx`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/01_INFORME_FINAL_LEOFIT.docx) | **Memoria técnica final completa** (19 capítulos, 703 párrafos, 35 tablas). Incluye antecedentes, metodología, arquitectura, base de datos BCNF, API REST, y absorción completa de la evaluación formal bajo **ISO/IEC 25010:2023** e **ISO 9126** de semanas 10 y 11. |
| **02** | **Informe de Continuación Semanas 14-15** | DOCX / MD | [`02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx)<br>[`02_INFORME_CONTINUACION_S14_S15_LEOFIT.md`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/02_INFORME_CONTINUACION_S14_S15_LEOFIT.md) | Informe acumulativo bajo la plantilla oficial del docente (`Plantilla_Informe_Continuacion_S14_S15_UTP`). Evalúa Rendimiento k6 ($p95 < 700\text{ ms}$), Flexibilidad (Adaptabilidad y Escalabilidad) y Mantenibilidad (Modularidad, Reusabilidad, Modificabilidad, Testabilidad). |
| **03** | **Presentación Oficial de Sustentación** | PPTX / HTML | [`03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx)<br>[`03_VISOR_WEB_PRESENTACION_SUSTENTACION.html`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/03_VISOR_WEB_PRESENTACION_SUSTENTACION.html) | Presentación ejecutiva de **25 diapositivas** widescreen 16:9 con diseño corporativo Navy/Cobalt/Terracotta WCAG AAA, 6 gráficos científicos de 300 DPI y notas de orador completas, más visor HTML interactivo. |
| **04** | **Plan de Auditoría, Calidad y Trazabilidad** | XLSX | [`04_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/04_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx) | Dashboard integral en Excel con **7 pestañas**: Matriz de Trazabilidad Jurado, Inventario Servicios Cloud, Auditoría de Código ISO 25010, Gap Analysis SUNAT CPE, Dimensionamiento, Estándares/Leyes y Compatibilidad/Migración. |
| **04** | **Compendio Técnico de Calidad y Criptografía** | MD | [`04_COMPENDIO_TECNICO_CALIDAD_TESTING_Y_CRIPTOGRAFIA.md`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/04_COMPENDIO_TECNICO_CALIDAD_TESTING_Y_CRIPTOGRAFIA.md) | Compendio maestro de ingeniería que sintetiza las Sesiones 21 a 29 (ISO 9126 calidad interna/externa/uso, ISO 25000, ISO 29119 con 3 documentos de gestión y 7 dinámicos) y formalización criptográfica SSL/TLS (Polanía Tovar, 2024). |
| **05** | **Galería de Gráficos Científicos** | PNG | [`graficos/`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/graficos/) | 6 gráficos a 300 DPI: Radar ISO 25010:2023, Percentiles k6, Bandas de Latencia Temporal, Curva de Saturación CPU vs TPS, Treemap McCabe y Cobertura de Código. |
| **06** | **Anexos Técnicos de Sustentación** | MD | [`anexos_tecnicos/`](01_ENTREGA_FINAL_PROYECTO_SEMANA_18/anexos_tecnicos/) | 6 anexos técnicos con respuestas de arquitectura y código ante las preguntas del jurado (ADR-001, ADR-002, SUNAT CPE, Pasarela de Pagos, Arquitectura Repo, Matriz de Trazabilidad). |

---

## 2. Evidencias de Calidad, Auditoría y Pruebas (`02_CALIDAD_Y_AUDITORIA/`)

Documentación técnica de soporte para profundizar en los marcos normativos aplicados:

| Carpeta / Documento | Enlace Directo | Contenido Técnico Principal |
| :--- | :--- | :--- |
| **Plan de Pruebas ISO 29119** | [`01_plan_de_pruebas_iso29119/`](02_CALIDAD_Y_AUDITORIA/01_plan_de_pruebas_iso29119/) | Especificación formal de los 3 documentos de gestión y 7 documentos dinámicos bajo ISO/IEC/IEEE 29119. |
| **Calidad ISO 25010 (Semanas 10-11)** | [`02_calidad_iso25010_semanas_10_11/`](02_CALIDAD_Y_AUDITORIA/02_calidad_iso25010_semanas_10_11/) | Evaluación de adecuación funcional, eficiencia de desempeño y usabilidad del primer corte de calidad. |
| **Auditoría y Cierre de Proyecto** | [`03_auditoria_y_cierre_proyecto/`](02_CALIDAD_Y_AUDITORIA/03_auditoria_y_cierre_proyecto/) | Checklists de auditoría de código, inventario técnico y actas de cierre formal. |
| **Operaciones, Respaldo y DRP** | [`05_operaciones_respaldo_drp/`](02_CALIDAD_Y_AUDITORIA/05_operaciones_respaldo_drp/) | Simulacro de recuperación ante desastres (RPO = 5 min, RTO = 15 min), respaldos pg_dump y contingencia. |
| **Métricas Sesión 28 UTP** | [`METRICAS_SESION_28_UTP/`](02_CALIDAD_Y_AUDITORIA/METRICAS_SESION_28_UTP/) | Fórmulas matemáticas de calidad ISO 9126 aplicadas: $X = 1 - (A/B)$ para adecuación funcional y suficiencia de pruebas. |

---

## 3. Catálogo de Arquitectura y Diagramas (`03_ARQUITECTURA_Y_DIAGRAMAS/`)

Colección de 25 diagramas técnicos formalizados bajo estándares internacionales:

- **Modelo C4 (Niveles 1 y 2):** Contexto del sistema y Contenedores en alta definición.
- **Modelado de Procesos BPMN 2.0:** Flujos AS-IS (manual, 5 min/pedido) vs. TO-BE (automatizado, sub-segundo).
- **Modelo de Base de Datos Relacional:** Diagrama ER en Tercera Forma Normal (3NF / BCNF) para PostgreSQL 16.
- **Diagramas de Secuencia UML:** Flujo transaccional con bloqueo pesimista (`SELECT FOR UPDATE`) para evitar sobreventa.
- **Registro Canónico de Decisiones (ADR):** Ubicado en [`docs/adr/`](adr/) bajo el estándar MADR.

---

## 4. Referencia del Curso y Material Docente (`04_REFERENCIA_CURSO_UTP/`)

Material didáctico y guías institucionales proporcionadas por el docente Ing. Enrique Lee Huamani:

- [`manuales_docente_enrique_lee/Guia_Libro_Semanas_14_15_Curso_Integrador_II_UTP.pdf`](04_REFERENCIA_CURSO_UTP/manuales_docente_enrique_lee/Guia_Libro_Semanas_14_15_Curso_Integrador_II_UTP.pdf): Guía de referencia de calidad de software y estándares de sustentación.
- [`manuales_docente_enrique_lee/PPT_Breve_Semanas_14_15_Curso_Integrador_II_UTP.pdf`](04_REFERENCIA_CURSO_UTP/manuales_docente_enrique_lee/PPT_Breve_Semanas_14_15_Curso_Integrador_II_UTP.pdf): Diapositivas guía para las Semanas 14 y 15.
- [`silabo_y_plantillas_utp/Silabo_Curso_Integrador_II.pdf`](04_REFERENCIA_CURSO_UTP/silabo_y_plantillas_utp/Silabo_Curso_Integrador_II.pdf): Sílabo oficial del curso 100000S12F.

---

## 5. Histórico de Entregas Anteriores (`99_HISTORICO_ENTREGAS_ANTERIORES/`)

Para fines de trazabilidad y auditoría de la evolución del proyecto durante el ciclo 2026-I:

- [`APF1_APF2/`](99_HISTORICO_ENTREGAS_ANTERIORES/APF1_APF2/): Informes y presentaciones de los dos primeros avances evaluados.
- [`APF3/`](99_HISTORICO_ENTREGAS_ANTERIORES/APF3/): Paquete completo del Avance de Proyecto Final 3 (memoria técnica de 77 páginas, pruebas Docker y usabilidad SUS 88.5).

---

## 6. Despliegues en Vivo y Acceso al Sistema

- **Frontend PWA (Cliente):** `https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/`
- **Backend API REST Health Check:** `https://leofit-backend-api.onrender.com/api/health`
- **Documentación Swagger OpenAPI:** `https://leofit-backend-api.onrender.com/api/docs`

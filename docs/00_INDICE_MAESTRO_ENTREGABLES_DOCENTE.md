# GUÍA Y MAPA DE ENTREGABLES ACADÉMICOS PARA EL DOCENTE EVALUADOR
## Curso Integrador II: Software (100000S12F) — Ciclo 2026-I
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  
**Equipo de Ingeniería (Grupo 01):** Lady Loayza, Víctor Cárdenas, Harley Roman, Jim Dávila, Daniel Rojas  
**Organización y Repositorio:** [`Leofit-Solutions-Grupo01/leofit-pedidos-sistema`](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema)

---

Estimado docente Ing. Enrique Lee Huamani, este documento consolida el índice unificado y directo de todos los entregables académicos y técnicos desarrollados a lo largo del ciclo, organizados para facilitar la revisión y calificación según las rúbricas institucionales de la UTP.

---

## 1. Entregables de la Unidad 4: Semanas 14 y 15 (Calidad de Software ISO/IEC 25010:2023)

En cumplimiento de lo expuesto en las sesiones teóricas y en los 3 documentos proporcionados (`Guía Libro`, `PPT Breve` y `Plantilla Editable`):

| Documento / Evidencia | Ubicación en el Repositorio | Descripción y Aportes Clave |
| :--- | :--- | :--- |
| **Informe Acumulativo Oficial (DOCX)** | [`docs/02_CALIDAD_Y_AUDITORIA/04_calidad_iso25010_semanas_14_15/INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.docx`](02_CALIDAD_Y_AUDITORIA/04_calidad_iso25010_semanas_14_15/INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.docx) | Informe acumulativo completo (APF1 + APF2 + APF3 + Unidad 4). Contiene 522 líneas compiladas, 14 tablas completas, tabla de contenidos dinámica y estilos formales UTP. |
| **Memoria Técnica Markdown (MD)** | [`docs/02_CALIDAD_Y_AUDITORIA/04_calidad_iso25010_semanas_14_15/INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.md`](02_CALIDAD_Y_AUDITORIA/04_calidad_iso25010_semanas_14_15/INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.md) | Versión técnica auditable en texto plano con código, fragmentos de prueba, consultas SQL, logs de k6 y justificaciones de arquitectura. |
| **Resultados de Rendimiento (k6)** | Ver Sección 5.1 del Informe | Ensayos de Ramp-up, Steady-state (30 min), Spike (35 VU) y Soak (4 horas). Medición de percentiles ($p50=120\text{ ms}$, $p95=280/480\text{ ms}$, $p99=720\text{ ms}$), 4 señales SRE y optimización B-Tree (-64.2% costo). |
| **Demostración de Flexibilidad** | Ver Sección 5.2 del Informe | **ISO/IEC 25010:2023 — Flexibility — Adaptability / Scalability**. Adaptabilidad multi-entorno (Local, Render, AWS ECS) con Factor III Twelve-Factor App. Patrones de resiliencia: Circuit Breaker, Bulkhead, Retry con Jitter y Rate Limiting. |
| **Demostración de Mantenibilidad** | Ver Sección 5.3 del Informe | Clean Architecture con regla estricta de dependencias (Dominio <- Aplicación <- Infraestructura). Reusabilidad DRY, modificabilidad con blast radius de 2 archivos (CHG-01), complejidad ciclomática de 1 a 3 y TDD con 194 tests (100% OK). |
| **Material Docente Utilizado** | [`docs/04_REFERENCIA_CURSO_UTP/manuales_docente_enrique_lee/Guia_Libro_Semanas_14_15_Curso_Integrador_II_UTP.pdf`](04_REFERENCIA_CURSO_UTP/manuales_docente_enrique_lee/Guia_Libro_Semanas_14_15_Curso_Integrador_II_UTP.pdf)<br>[`docs/04_REFERENCIA_CURSO_UTP/manuales_docente_enrique_lee/PPT_Breve_Semanas_14_15_Curso_Integrador_II_UTP.pdf`](04_REFERENCIA_CURSO_UTP/manuales_docente_enrique_lee/PPT_Breve_Semanas_14_15_Curso_Integrador_II_UTP.pdf)<br>[`docs/04_REFERENCIA_CURSO_UTP/silabo_y_plantillas_utp/Plantilla_Informe_Continuacion_S14_S15_UTP.docx`](04_REFERENCIA_CURSO_UTP/silabo_y_plantillas_utp/Plantilla_Informe_Continuacion_S14_S15_UTP.docx) | Material didáctico oficial entregado por el docente para la Unidad 4. |

---

## 2. Presentación Oficial de Sustentación Final (Semana 18)

La sustentación final del proyecto cuenta con material audiovisual y notas de orador de alto nivel de ingeniería:

| Recurso de Presentación | Enlace Directo | Características |
| :--- | :--- | :--- |
| **Presentación PowerPoint (.pptx)** | [`docs/05_SUSTENTACION_PROYECTO_FINAL_SEMANA_18/03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx`](05_SUSTENTACION_PROYECTO_FINAL_SEMANA_18/03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx) | Widescreen 16:9, **25 diapositivas ejecutivas**, tablas dinámicas nativas, paleta institucional Navy/Cobalt/Terracotta WCAG AAA y notas de orador en el 100% de las láminas. |
| **Visor Web Interactivo (.html)** | [`docs/05_SUSTENTACION_PROYECTO_FINAL_SEMANA_18/03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.html`](05_SUSTENTACION_PROYECTO_FINAL_SEMANA_18/03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.html) | Visor responsive que permite visualizar las 25 diapositivas en el navegador con navegación por teclado ($\leftarrow/\rightarrow$) y panel de notas (tecla `N`). |
| **Transcripción y Guion (.md)** | [`docs/05_SUSTENTACION_PROYECTO_FINAL_SEMANA_18/03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.md`](05_SUSTENTACION_PROYECTO_FINAL_SEMANA_18/03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.md) | Guion textual estructurado con todas las tablas, textos y notas para el ensayo del equipo. |

---

## 3. Entregables Anteriores (Trazabilidad Acumulativa)

| Hito Académico | Ubicación | Contenido Principal |
| :--- | :--- | :--- |
| **Avance de Proyecto Final 3 (APF3)** | [`docs/01_ENTREGA_OFICIAL_APF3/`](01_ENTREGA_OFICIAL_APF3/) | Memoria técnica de 77 páginas, evaluación de adecuación funcional 100%, compatibilidad Docker y usabilidad SUS 88.5/100. |
| **Calidad ISO 25010 y Auditoría** | [`docs/02_CALIDAD_Y_AUDITORIA/`](02_CALIDAD_Y_AUDITORIA/) | Plan de pruebas ISO 29119, matriz de deuda técnica y simulacros de recuperación ante desastres (DRP). |
| **Catálogo de Diagramas** | [`docs/03_ARQUITECTURA_Y_DIAGRAMAS/`](03_ARQUITECTURA_Y_DIAGRAMAS/) | 25 diagramas de ingeniería (C4 Nivel 1 y 2, BPMN AS-IS/TO-BE, modelo relacional BCNF, diagramas de secuencia). |
| **Decisiones de Arquitectura (ADR)** | [`docs/adr/`](adr/) | ADR-001 (Render+Neon vs AWS) y ADR-002 (Arquitectura Objetivo Cloud AWS). |
| **Histórico APF1 y APF2** | [`docs/99_HISTORICO_ENTREGAS_ANTERIORES/`](99_HISTORICO_ENTREGAS_ANTERIORES/) | Informes y presentaciones de los primeros dos avances del curso. |

---

## 4. Despliegues en Vivo y Acceso al Sistema

- **Frontend PWA (Cliente):** `https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/`
- **Backend API REST Health Check:** `https://leofit-backend-api.onrender.com/api/health`
- **Documentación Swagger OpenAPI:** `https://leofit-backend-api.onrender.com/api/docs`

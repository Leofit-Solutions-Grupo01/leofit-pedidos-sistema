# Directorio Maestro de Documentación — LeoFit Solutions
## Curso Integrador II: Software (100000S12F) — Ciclo 2026-I — UTP
**Docente Asesor:** Ing. Enrique Lee Huamani Uriarte  
**Grupo 01:** *LeoFit Pedidos Sistema*

---

## Estructura Oficial de Documentación

Toda la documentación técnica y académica del proyecto se encuentra organizada bajo estándares de ingeniería de software, arquitectura limpia y normas de redacción formal:

```text
docs/
├── README.md                                 # Portal Maestro de Documentación (Visualización en GitHub)
│
├── gestion_academica/                        # Gestión Institucional y Académica UTP
│   ├── entregas/                             # Informes Finales Oficiales Compilados
│   │   ├── INFORME_FINAL_APF3_LEOFIT.pdf     # Entregable Oficial Definitivo APF3 (Formato Libro, 77 páginas)
│   │   ├── INFORME_FINAL_APF3_LEOFIT.docx    # Documento Maestro Editable en Microsoft Word (7.14 MB)
│   │   ├── INFORME_FINAL_APF3_LEOFIT.md      # Versión Markdown completa y trazable
│   │   ├── INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf   # Informe Calidad ISO/IEC 25010 (24 páginas)
│   │   ├── INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx  # Documento Editable ISO/IEC 25010 (68 KB)
│   │   ├── INFORME_FINAL_APF2_LEOFIT.pdf     # Entregable Oficial Previo APF2 (Histórico)
│   │   ├── INFORME_FINAL_APF2_LEOFIT.docx    # Documento Editable APF2
│   │   ├── INFORME_FINAL_APF2_LEOFIT.html    # Versión Web HTML APF2
│   │   ├── INFORME_FINAL_APF2_LEOFIT.md      # Versión Markdown APF2
│   │   └── style.css                         # Hoja de estilos de exportación HTML
│   ├── presentaciones/                       # Diapositivas de Sustentación Final
│   │   ├── APF3_LEOFIT_Presentacion.pdf      # Presentación unificada definitiva de sustentación
│   │   ├── APF3_LEOFIT_Presentacion.pptx     # Presentación PowerPoint editable
│   │   ├── APF3_LEOFIT_Presentacion.html     # Versión web interactiva (Marp)
│   │   ├── APF3_LEOFIT_Presentacion.md       # Fuente Marp con guion y tiempos por expositor
│   │   ├── GRUP01-Curso_Integrador_II_Software.pptx  # Presentación entregada en APF2
│   │   └── assets/                           # Diagramas vectoriales y capturas de soporte para diapositivas
│   ├── plantillas/                           # Plantillas oficiales UTP
│   │   └── UTP_Plantilla_Informe_ISO25010_Semanas10_11.docx # Formato institucional base
│   ├── diapositivas/                         # Diapositivas de clases teóricas (Semanas 01 a 18)
│   ├── rubricas/                             # Rúbricas e indicaciones oficiales de evaluación UTP (APF1, APF2, APF3)
│   ├── evaluaciones/                         # Retroalimentación docente y control de deuda técnica
│   │   ├── Retroalimentacion_APF1_Calificacion.txt # Calificación y feedback docente APF1
│   │   └── DEUDA_TECNICA.md                  # Backlog de mejora continua y mitigación a mediano plazo
│   └── recursos/                             # Sílabo oficial del curso y fichas de mapeo de empresa
│
├── diagramas/                                # Modelos Oficiales de Arquitectura, UML y Procesos
│   ├── README.md                             # Catálogo formal de diagramas técnicos
│   ├── apf3/                                 # Figuras técnicas de alta resolución para el Informe APF3
│   │   ├── fig_arquitectura_logica.png       # Arquitectura en 3 capas
│   │   ├── fig_repositorio_factory.png       # Patrón Repository y desacoplamiento
│   │   ├── fig_secuencia_pedido.png          # Secuencia atómica transaccional
│   │   ├── fig_estados_pedido.png            # Máquina de estados del pedido
│   │   ├── fig_estrategia_pruebas.png        # Pirámide de pruebas automatizadas
│   │   ├── fig_pruebas_por_suite.png         # Distribución de 187 pruebas por suite
│   │   ├── fig_cobertura_modulos.png         # Métricas de cobertura de código
│   │   ├── fig_despliegue.png                # Topología de nube (GitHub Pages + Render)
│   │   └── fig_cicd.png                      # Pipeline CI/CD en GitHub Actions
│   ├── 01_BPMN_AS-IS.png                     # Diagrama de Procesos Actual (BPMN AS-IS)
│   ├── 01_BPMN_TO-BE.png                     # Diagrama de Procesos Propuesto (BPMN TO-BE)
│   ├── 02_Mapa_Riesgos.png                   # Matriz 5x5 de Gestión de Riesgos PMI
│   ├── 06_Lean_Canvas.png                    # Lienzo de Modelo de Negocio (Lean Canvas)
│   ├── 07_Cronograma_Gantt.png               # Cronograma de ejecución del proyecto
│   ├── 08_Tablero_Kanban.png                 # Tablero Kanban y Límites WIP
│   ├── 09_Wireframes_Baja_Fidelidad.png      # Prototipado y Wireframes Mobile-First
│   ├── 10_User_Flow_Navegacion.png           # Flujo de Navegación del Usuario
│   ├── 11_Arquitectura_C4_Model.png          # Modelo de Contenedores C4 Nivel 2
│   ├── 12_Modelo_Logico_BD.png               # DER Lógico Relacional (Crow's Foot)
│   ├── 13_Modelo_Fisico_BD.png               # Diagrama Físico de Base de Datos (PostgreSQL 16)
│   └── 14_Diagrama_DB.png                    # Esquema general de base de datos
│
├── auditoria_cierre/                         # Evidencias de Cierre de Requisitos y Capturas UI
│   ├── analisis_teorico_requisitos.docx / .md # Análisis teórico de requisitos funcionales
│   ├── justificaciones_cierre_issues.docx / .md # Justificación formal de cierre de issues GitHub
│   ├── revision_tareas_pendientes.docx / .md   # Trazabilidad de backlog resuelto
│   └── [fig_1 a fig_15, fig_analytics]       # Capturas de auditoría de módulos operativos en producción
│
└── operaciones/                              # Procedimientos Operativos y Runbooks de Soporte
    └── BACKUP_RESTORE_DRILL.md               # Protocolo de Simulacro de Respaldo y Recuperación (RPO/RTO)
```

---

## Entregables Principales del Proyecto

| Hito / Documento | Estado | Formato PDF | Formato Word | Versión Markdown |
| :--- | :---: | :---: | :---: | :---: |
| **INFORME FINAL APF3 (Definitivo)** | **Aprobado / Entregable Final** | [`INFORME_FINAL_APF3_LEOFIT.pdf`](./gestion_academica/entregas/INFORME_FINAL_APF3_LEOFIT.pdf) (77 págs) | [`INFORME_FINAL_APF3_LEOFIT.docx`](./gestion_academica/entregas/INFORME_FINAL_APF3_LEOFIT.docx) | [`INFORME_FINAL_APF3_LEOFIT.md`](./gestion_academica/entregas/INFORME_FINAL_APF3_LEOFIT.md) |
| **INFORME ISO/IEC 25010 (Semanas 10-11)** | **Completado / Evaluado** | [`INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf`](./gestion_academica/entregas/INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf) (24 págs) | [`INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx`](./gestion_academica/entregas/INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx) | — |
| **INFORME FINAL APF2** | **Histórico** | [`INFORME_FINAL_APF2_LEOFIT.pdf`](./gestion_academica/entregas/INFORME_FINAL_APF2_LEOFIT.pdf) | [`INFORME_FINAL_APF2_LEOFIT.docx`](./gestion_academica/entregas/INFORME_FINAL_APF2_LEOFIT.docx) | [`INFORME_FINAL_APF2_LEOFIT.md`](./gestion_academica/entregas/INFORME_FINAL_APF2_LEOFIT.md) |
| **SUSTENTACIÓN APF3** | **Definitivo** | [`APF3_LEOFIT_Presentacion.pdf`](./gestion_academica/presentaciones/APF3_LEOFIT_Presentacion.pdf) | [`APF3_LEOFIT_Presentacion.pptx`](./gestion_academica/presentaciones/APF3_LEOFIT_Presentacion.pptx) | [`APF3_LEOFIT_Presentacion.md`](./gestion_academica/presentaciones/APF3_LEOFIT_Presentacion.md) |

---

## Enlaces a Entornos de Producción y Código

* **Repositorio GitHub:** [https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema)
* **Frontend Web (PWA):** [https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)
* **Backend API REST (Health):** [https://leofit-backend-api.onrender.com/api/health](https://leofit-backend-api.onrender.com/api/health)

# 🖼️ Directorio de Diagramas Generados (Legacy & Matplotlib)

Este directorio almacena los gráficos y diagramas de negocio, procesos y planificación del proyecto LeoFit Solutions.

> **⚠️ Nota de Arquitectura (Importante para Evaluadores)**
> 
> Durante la evolución del proyecto, la arquitectura documental se dividió en dos áreas:
> 1. **`/diagrams/` (Este directorio):** Contiene los gráficos de negocio generados programáticamente vía Python (Matplotlib/Graphviz). Incluye el Lean Canvas, Gantt, Kanban, Wireframes y flujos BPMN.
> 2. **`/docs/diagramas/`:** Contiene la **nueva generación de diagramas HD vectoriales** (Mermaid.js) específicos para la Arquitectura de Software (Frontend, PWA, Backend, C4 Model).

## Estructura de Archivos

* `01_BPMN_*`: Diagramas de procesos de negocio (AS-IS y TO-BE).
* `02_Mapa_Riesgos.png`: Matriz de riesgos del proyecto.
* `06_Lean_Canvas.png`: Modelo de negocio.
* `07_Cronograma_Gantt.png`: Planificación temporal (Sprints).
* `08_Tablero_Kanban.png`: Flujo de trabajo ágil.
* `09_Wireframes_*`: Diseños de baja fidelidad.
* `11_Arquitectura_C4_Model.png` *(Deprecated)*: Ver `/docs/diagramas/` para la versión C4 actualizada.
* `12_` / `13_` / `14_`: Modelos lógicos y físicos de la Base de Datos.

**Seguridad y Privacidad:** Todos los diagramas de esta carpeta han sido auditados y generados programáticamente. Ninguna imagen contiene direcciones IP reales, credenciales ni información de identificación personal (PII) de los desarrolladores.

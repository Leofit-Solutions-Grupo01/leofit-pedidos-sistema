# Suite de Scripts y Automatización — LeoFit Solutions
## Curso Integrador II: Software (100000S12F) — Ciclo 2026-I — UTP

Este directorio contiene las herramientas de automatización, generación documental, maquetación editorial, renderizado de diagramas de ingeniería y ejecución de pruebas de carga para el proyecto LeoFit.

---

### Catálogo de Herramientas

| Script | Propósito y Función | Salida Generada |
| :--- | :--- | :--- |
| **`generate_apf3_complete_package.py`** | **Generador Maestro APF3**: Construye el informe final definitivo en formato libro (76 páginas) y ejecuta la exportación automatizada a PDF. | `docs/gestion_academica/entregas/INFORME_FINAL_APF3_LEOFIT.docx` y `.pdf` |
| **`apf3_book_engine.py`** | **Motor de Maquetación Editorial**: API de abstracción de `python-docx` para estilos formales tipo libro, índices de figuras/tablas (TOC/LOF/LOT), encabezados con `STYLEREF` y numeración diferenciada. | Módulo auxiliar importado por el generador maestro |
| **`export_docx_to_pdf_word_com.py`** | **Compilador PDF Word COM**: Automatiza la exportación de documentos Word a PDF mediante la API COM de Microsoft Word en Windows, garantizando fidelidad tipográfica, campos actualizados y resolución gráfica. | `.pdf` de alta fidelidad |
| **`generate_apf2_complete_package.py`** | **Generador Histórico APF2**: Genera el entregable oficial previo APF2 bajo formato APA 7ma Edición (mantenido para soporte de revisión docente). | `docs/gestion_academica/entregas/INFORME_FINAL_APF2_LEOFIT.docx` |
| **`generate_apf3_figures.py`** | **Renderizador de Métricas APF3**: Genera las 9 figuras analíticas de cobertura de código, suites de prueba, arquitectura de despliegue, secuencias y máquinas de estados. | `docs/diagramas/apf3/*.png` |
| **`generate_bpmn_tobe.py`** | **Diagramador BPMN 2.0 TO-BE**: Genera el diagrama de procesos optimizado en alta resolución (300 DPI). | `docs/diagramas/01_BPMN_TO-BE.png` |
| **`generate_risk_map.py`** | **Matriz de Riesgos 5x5**: Genera el mapa de calor y catálogo de riesgos formal según estándares PMI. | `docs/diagramas/02_Mapa_Riesgos.png` |
| **`generate_user_flow.py`** | **Diagrama de Flujo de Usuario**: Renderiza el User Flow UX de navegación e interacción multicanal. | `docs/diagramas/10_User_Flow_Navegacion.png` |
| **`generate_c4_diagram.py`** | **Arquitectura C4 Nivel 2**: Renderiza el modelo de contenedores de software según IEEE 1471 / ISO 42010. | `docs/diagramas/11_Arquitectura_C4_Model.png` |
| **`generate_leofit_db_models_bw.py`** | **Modelos de Base de Datos CAD**: Genera los esquemas Lógico (DER Crow's Foot) y Físico Relacional (DDL SQL) en alta resolución. | `docs/diagramas/12_Modelo_Logico_BD.png` y `13_Modelo_Fisico_BD.png` |
| **`convert_md_to_professional_docx.py`** | **Conversor Utilitario Markdown a DOCX**: Herramienta CLI para transformar cualquier Markdown a Word con estilos tipográficos, tablas y formateo inline. | `[archivo].docx` |
| **`k6_workload.js`** | **Suite de Pruebas de Estrés K6**: Carga concurrente (50 VUs, 6 min) para evaluar aislamiento de transacciones ACID y latencias p95 en PostgreSQL. | Métricas de rendimiento y stdout K6 |

---

### Instrucciones de Ejecución

#### Generar el Libro Oficial APF3 (DOCX y PDF):
```powershell
python scripts/generate_apf3_complete_package.py
```

#### Regenerar Figuras Analíticas de APF3:
```powershell
python scripts/generate_apf3_figures.py
```

#### Regenerar Diagramas del Proyecto:
```powershell
python scripts/generate_bpmn_tobe.py
python scripts/generate_risk_map.py
python scripts/generate_user_flow.py
python scripts/generate_c4_diagram.py
python scripts/generate_leofit_db_models_bw.py
```

#### Ejecutar Pruebas de Carga con K6:
```bash
k6 run --env ISOLATION_LEVEL=SERIALIZABLE --env BASE_URL=http://localhost:3000 --vus 50 --duration 6m scripts/k6_workload.js
```

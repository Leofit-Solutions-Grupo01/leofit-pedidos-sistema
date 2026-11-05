# Suite de Scripts y Automatización de Ingeniería — LeoFit Solutions
## Curso Integrador II: Software (100000S12F) — Ciclo 2026-I — UTP
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  
**Equipo de Ingeniería (Grupo 01):**
* Lady Luz Loayza R. (Scrum Master / DevSecOps)
* Víctor L. Cárdenas F. (Product Owner / DBA)
* Harley A. Roman D. (Frontend Lead / UI-UX)
* Jim A. Dávila M. (QA Engineer Lead / Backend)
* Daniel E. Rojas S. (Business Analyst / Cloud DevOps)

---

## Estructura Organizada del Directorio `scripts/`

```text
scripts/
│
├── build_apf3_grupo_xx_structure.py  # Ensamblador de la estructura APF3_GRUPO_01 (Cap. 14 Pág. 35 del manual)
├── export_and_render_slides.py       # Compilador PowerPoint COM a PDF y renderizador de diapositivas a PNG
├── export_docx_to_pdf_word_com.py    # Compilador Word COM de informes a PDF de alta resolución
├── sync_audit_metrics.py             # Sincronizador en vivo entre código fuente (194 tests) y Excel
├── k6_workload.js                    # Script de prueba de carga concurrente y estrés con k6
├── take_screenshots.py               # Automatización headless de capturas de pantalla de la PWA
├── validate_reference_urls.py        # Validador de salud HTTP de referencias bibliográficas
│
├── generators/                       # Generadores algorítmicos de diagramas, mockups y modelos de ingeniería
│   ├── generate_05_erd_bd.py         # Generador del Diagrama Entidad-Relación BCNF
│   ├── generate_15_rbac_flow.py      # Generador de flujos RBAC Admin vs Operador
│   ├── generate_c4_diagram.py        # Generador de Arquitectura C4 Nivel 2
│   ├── generate_bpmn_tobe.py         # Generador de Procesos BPMN 2.0 TO-BE
│   ├── generate_risk_map.py          # Generador de Mapa de Riesgos y Heatmap
│   ├── generate_user_flow.py         # Generador de Flujo de Navegación UX
│   ├── apf3_book_engine.py           # Motor de estilos tipográficos formales tipo libro para Word
│   ├── generate_apf3_complete_package.py # Compilador maestro de la memoria técnica de 77 páginas
│   └── ...                           # Generadores complementarios de figuras y presentaciones
│
├── iso25010/                         # Módulo del arnés experimental de coexistencia e ISO 25010
│   ├── run_coexistence_benchmark.py  # Arnés de prueba de coexistencia bajo Docker cgroups
│   ├── service_b_reportes.js         # Microservicio colocual de carga para contención de recursos
│   └── generate_coexistence_charts.py # Graficador de curvas de latencia y percentil P95
│
└── maintenance_archive/              # Archivo histórico de utilitarios de mantenimiento y auditorías previas
    ├── audit_all_slides_visuals.py
    ├── beautify_presentation_styles.py
    ├── find_and_remove_emojis.py
    ├── restore_indentation_and_clean_emojis.py
    └── ...                           # Scripts de inspección y saneamiento ejecutados
```

---

## Comandos Rápidos de Uso Frecuente:

```bash
# 1. Sincronizar el Dashboard Excel con los tests en vivo:
python scripts/sync_audit_metrics.py

# 2. Generar el paquete de estructura recomendada por el docente (APF3_GRUPO_01):
python scripts/build_apf3_grupo_xx_structure.py

# 3. Exportar la presentación PowerPoint a PDF y verificar diapositivas:
python scripts/export_and_render_slides.py

# 4. Ejecutar la prueba de estrés de concurrencia:
k6 run scripts/k6_workload.js
```

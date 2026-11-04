# Suite de Scripts y Automatización de Ingeniería — LeoFit Solutions
## Curso Integrador II: Software (100000S12F) — Ciclo 2026-I — UTP
**Docente Asesor:** Ing. Enrique Lee Huamani Uriarte  
**Equipo:** Lady Luz Loayza R. (SM), Víctor L. Cárdenas F. (PO), Harley A. Roman D. (Front), Jim A. Dávila M. (QA), Daniel E. Rojas S. (DevOps)

---

### ¿Por qué es fundamental esta sección `scripts/`?

La carpeta `scripts/` constituye el **núcleo de reproducibilidad, trazabilidad y automatización de ingeniería de software** del proyecto LeoFit, alineada estrictamente con los estándares **ISO/IEC/IEEE 29119-3**, **ISO/IEC 25010:2023** e **ISO/IEC/IEEE 90003:2018**:

1. **Evidencia Científica y Experimental:** Ningún diagrama, gráfico de métricas o benchmark fue elaborado de forma estática o manual. Cada figura arquitectónica, curva de latencia P95 y prueba de carga se genera algorítmicamente a partir de modelos matemáticos y telemetría real.
2. **Sincronización Bidireccional en Vivo:** El script `sync_audit_metrics.py` audita dinámicamente el código fuente (backend TypeScript + frontend Vitest) y actualiza el Dashboard Excel con las 195 pruebas y 613 aserciones en tiempo real.
3. **Generación Documental Determinista:** Los generadores maestros compilan los informes oficiales Word (`.docx`), presentaciones (`.pptx`) y exportan a PDF mediante Microsoft Office COM con fidelidad tipográfica profesional y estilo editorial formal tipo libro.
4. **Arnés de Coexistencia ISO 25010:** Contiene el Servicio B (`service_b_reportes.js`) y el benchmark experimental de coexistencia bajo contención de recursos en Docker (`run_coexistence_benchmark.py`).

---

### Catálogo Completo de Herramientas de Automatización

#### 1. Auditoría, Sincronización y Métricas de Calidad
| Script | Propósito y Función | Salida / Artefacto |
| :--- | :--- | :--- |
| **`sync_audit_metrics.py`** | **Auditor y Sincronizador Maestro**: Escanea las 27 suites de prueba (17 backend + 10 frontend) y sincroniza los datos con el Plan de Auditoría Excel. | `docs/03_auditoria_y_cierre_proyecto/Plan_Auditoria_Software_LeoFit_Dashboard-Loayza-Lady.xlsx` |
| **`validate_reference_urls.py`** | **Validador de Referencias APA 7ma**: Audita el estado HTTP y la resolución de enlaces bibliográficos citados en los informes. | Reporte stdout de integridad de citas |
| **`take_screenshots.py`** | **Capturador Headless**: Levanta el build de producción y captura pantallas full-page para auditoría visual. | Evidencias de auditoría visual |

#### 2. Entregables de Calidad ISO/IEC 25010 (Semanas 10–11)
| Script | Propósito y Función | Salida / Artefacto |
| :--- | :--- | :--- |
| **`populate_iso25010_report.py`** | **Poblador del Informe ISO 25010**: Estructura la plantilla oficial UTP con las 31 tablas, catálogos RF, casos PF/PI/PC y métricas reales. | `docs/02_calidad_iso25010_semanas_10_11/INFORME_ISO25010_SEMANAS_10_11_LEOFIT.docx` |
| **`enrich_iso25010_report.py`** | **Enriquecedor Visual y Técnico**: Aplica estilo tipográfico UTP, bordes corporativos, firmas digitales y tablas de trazabilidad. | Versión enriquecida con metadatos completos |
| **`harmonize_iso_references.py`** | **Homologador Normativo**: Inserta las citas de ISO/IEC 25010:2023, ISO/IEC 25023:2016 e ISO/IEC/IEEE 29119. | Sección de Referencias en DOCX |

#### 3. Arnés de Coexistencia Experimental (`scripts/iso25010/`)
| Script | Propósito y Función | Salida / Artefacto |
| :--- | :--- | :--- |
| **`iso25010/run_coexistence_benchmark.py`** | **Arnés Experimental de Coexistencia**: Ejecuta el protocolo de 2 condiciones (A vs A+B) midiendo latencia media, P95 y uso de CPU/RAM. | `coexistence_raw.csv` y `coexistence_summary.json` |
| **`iso25010/service_b_reportes.js`** | **Servicio B Colocual**: Microservicio consumidor intensivo de CPU/memoria para simular contención en cgroups compartidos. | Microservicio en Node.js |
| **`iso25010/generate_coexistence_charts.py`** | **Graficador de Benchmarks**: Renderiza las curvas analíticas de degradación relativa y percentil P95 (300 DPI). | `fig_coexistencia_latencias.png` y `fig_coexistencia_p95.png` |
| **`iso25010/update_quality_manuals_a11y.py`** | **Armonizador de Accesibilidad**: Sincroniza manuales técnicos con contrastes WCAG 2.1 AA/AAA. | Manuales de Calidad Técnico y Ejecutivo |

#### 4. Generación Editorial del Informe Final APF3
| Script | Propósito y Función | Salida / Artefacto |
| :--- | :--- | :--- |
| **`generate_apf3_complete_package.py`** | **Generador Maestro APF3**: Compila la memoria técnica completa (77 páginas, 21 diagramas) con estilos de libro de ingeniería. | `docs/01_entregable_final_apf3/INFORME_FINAL_APF3_LEOFIT.docx` y `.pdf` |
| **`apf3_book_engine.py`** | **Motor de Maquetación Editorial**: Módulo de bajo nivel de `python-docx` para estilos formales, TOC/LOF/LOT y encabezados `STYLEREF`. | Motor auxiliar importable |
| **`export_docx_to_pdf_word_com.py`** | **Compilador PDF Word COM**: Automatiza la exportación de Word a PDF mediante API COM nativa de Windows. | Archivos `.pdf` oficiales de alta fidelidad |
| **`generate_apf2_complete_package.py`** | **Generador Histórico APF2**: Mantiene el archivo histórico del hito intermedio APF2 para auditoría docente. | `docs/06_historial_entregas_anteriores_apf1_apf2/INFORME_FINAL_APF2_LEOFIT.docx` |

#### 5. Presentaciones de Sustentación
| Script | Propósito y Función | Salida / Artefacto |
| :--- | :--- | :--- |
| **`generate_apf3_presentation.py`** | **Compilador de Presentación Maestra**: Genera las diapositivas de sustentación de 10 minutos con guion y tiempos por expositor. | `docs/01_entregable_final_apf3/presentacion_sustentacion/APF3_LEOFIT_Presentacion.*` |
| **`generate_apf3_pptx.py`** | **Generador PPTX Directo**: Construye la baraja PowerPoint con tarjetas KPI, esquema de colores corporativo y tablas formateadas. | Archivo `.pptx` editable |

#### 6. Renderizado de Diagramas de Negocio y Arquitectura
| Script | Propósito y Función | Salida / Artefacto |
| :--- | :--- | :--- |
| **`generate_apf3_figures.py`** | **Renderizador de Figuras Analíticas**: Genera las 9 figuras de pirámide de pruebas, cobertura, despliegue y secuencias. | `docs/04_diagramas_arquitectura_y_negocio/apf3/*.png` |
| **`generate_bpmn_tobe.py`** | **Diagramador BPMN 2.0 TO-BE**: Genera el flujo operacional optimizado de pedidos textiles (300 DPI). | `01_BPMN_TO-BE.png` |
| **`generate_risk_map.py`** | **Matriz de Riesgos PMI 5x5**: Genera el mapa de calor de severidad vs. probabilidad de riesgos operacionales. | `02_Mapa_Riesgos.png` |
| **`generate_user_flow.py`** | **User Flow UI/UX**: Renderiza el diagrama de interacción de usuario en la PWA responsiva. | `10_User_Flow_Navegacion.png` |
| **`generate_c4_diagram.py`** | **Arquitectura C4 Nivel 2**: Renderiza el modelo de contenedores de software bajo IEEE 1471 / ISO 42010. | `11_Arquitectura_C4_Model.png` |
| **`generate_leofit_db_models_bw.py`** | **Modelos Lógico y Físico de BD**: Genera los diagramas DER Crow's Foot y relacional de las 12 tablas BCNF. | `12_Modelo_Logico_BD.png` y `13_Modelo_Fisico_BD.png` |
| **`generate_05_erd_bd.py`** | **Diagrama ERD Detallado**: Renderiza las 22 tablas y vistas operacionales de auditoría. | `05_ERD_Detallado.png` |
| **`generate_15_rbac_flow.py`** | **Flujo RBAC**: Renderiza la matriz visual de autorización ADMIN vs. OPERATOR. | `15_RBAC_Flow.png` |
| **`generate_accessible_split_diagrams.py`** | **Diagramas en Alta Accesibilidad**: Versiones de alto contraste y tipografía 18pt a 28pt para personas con baja visibilidad. | Diagramas de alta legibilidad |

#### 7. Pruebas de Carga de Base de Datos
| Script | Propósito y Función | Salida / Artefacto |
| :--- | :--- | :--- |
| **`k6_workload.js`** | **Pruebas de Estrés K6**: Simulación de 50 usuarios concurrentes durante 6 minutos evaluando transacciones ACID en PostgreSQL. | Métricas de rendimiento y latencia P95 |

---

### Instrucciones de Uso Rápido

#### 1. Sincronizar el Plan de Auditoría con el Código Actual:
```bash
python scripts/sync_audit_metrics.py
```

#### 2. Re-generar los Informes Oficiales en Word y PDF:
```bash
python scripts/generate_apf3_complete_package.py
```

#### 3. Re-generar las Diapositivas de Sustentación (PPTX y PDF):
```bash
python scripts/generate_apf3_presentation.py
```

#### 4. Ejecutar el Benchmark de Coexistencia ISO 25010:
```bash
python scripts/iso25010/run_coexistence_benchmark.py
```

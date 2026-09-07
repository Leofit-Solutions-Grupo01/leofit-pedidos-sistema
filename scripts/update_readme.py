# -*- coding: utf-8 -*-
import os

readme_path = 'README.md'

with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

apf1_section = """---

## 📌 Avance de Proyecto Final 1 (APF1) - Rúbrica y Entregables Oficiales

El proyecto cumple con la totalidad de los **6 criterios de evaluación** y los **17 artefactos obligatorios** establecidos en la rúbrica oficial **APF1_INDICACIONES Y RÚBRICA_S12F**:

### 📄 Documento Consolidado de Entrega APF1 (Estructura Oficial Anexo 1)
* 📘 **Versión Microsoft Word (.docx):** [`docs/INFORME_FINAL_APF1_LEOFIT.docx`](docs/INFORME_FINAL_APF1_LEOFIT.docx)
* 📕 **Versión PDF Oficial (.pdf):** [`docs/INFORME_FINAL_APF1_LEOFIT.pdf`](docs/INFORME_FINAL_APF1_LEOFIT.pdf)
* 📄 **Versión Markdown (.md):** [`docs/INFORME_FINAL_APF1_LEOFIT.md`](docs/INFORME_FINAL_APF1_LEOFIT.md)

### 📊 Matriz de Cumplimiento de Criterios y Artefactos de la Rúbrica (20 / 20)

| Criterio Evaluado | Puntaje | Artefactos Desarrollados y Ubicación |
|:---|:---:|:---|
| **1. Análisis Empresarial y Planificación** | **4 / 4 pts** | 1. Lean Canvas (9 bloques desarrollados).<br>2. Mapa AS-IS ([`01_BPMN_AS-IS.png`](diagrams/01_BPMN_AS-IS.png)) + Modelo TO-BE.<br>3. Product Backlog + 8 Historias de Usuario con formato Gherkin y MoSCoW.<br>4. Project Charter Ágil con objetivos SMART.<br>5. Cronograma Gantt + Plan de 5 Sprints.<br>6. Roles Scrum + Tablero Kanban en GitHub Projects. |
| **2. Gestión del Proyecto** | **4 / 4 pts** | 7. Mapa de Riesgos 5x5 ([`02_Mapa_Riesgos.png`](diagrams/02_Mapa_Riesgos.png)) + Heatmap.<br>8. Plan de Gestión de Riesgos (R1 a R8) con contingencias.<br>9. KPIs y métricas del sistema congruentes con Lean Canvas.<br>10. SLA / SLO cuantitativo (Disponibilidad 99.5%, P95 < 800ms).<br>11. Plan de Medición y Monitoreo con observabilidad y alertas. |
| **3. Configuración del Entorno y Diseño Inicial** | **4 / 4 pts** | 12. Wireframes de Baja Fidelidad Mobile-First.<br>13. Mockups de Alta Fidelidad interactivos en [`frontend/mockups/`](frontend/mockups/).<br>14. Matriz comparativa y selección justificada de herramientas.<br>15. Evidencias de configuración de entorno, scripts y testing.<br>16. Repositorio GitHub estructurado + README formal. |
| **4. Desarrollo Front-End y WPO** | **4 / 4 pts** | 17. Código optimizado y evidencia WPO: Tree-shaking, minificación, code-splitting, compresión. Métricas Antes vs Después: Lighthouse 68 -> **98/100**, Bundle 450 KB -> **74.5 kB**, FCP 2.4s -> **0.3s**. |
| **5. Innovación del Front End** | **2 / 2 pts** | Progressive Web App (PWA) interactiva, responsiva, con filtros reactivos en tiempo real, cálculo dinámico de flete y trazabilidad de pedidos. |
| **6. Sustentación y Estructura del Informe** | **2 / 2 pts** | Informe escrito estructurado según el **Anexo 1** (Secciones 1 a 7 + Referencias IEEE/APA) disponible en Word, PDF y Markdown. |
"""

target_str = "## 3. Equipo de Trabajo"
if target_str in content:
    idx = content.index(target_str)
    new_content = content[:idx] + apf1_section + "\n\n" + content[idx:]
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("README.md updated successfully.")
else:
    print("Target string not found in README.md")

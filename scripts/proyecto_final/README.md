# Cadena de Herramientas y Scripts de Sustentación del Proyecto Final
## Sistema de Gestión de Pedidos Multicanal — LeoFit Solutions (Ciclo 2026-I)

Este directorio contiene las herramientas de automatización para compilar la documentación ofimática oficial del Proyecto Final (Semana 18) y exportar los entregables oficiales para su presentación y subida a la plataforma académica UTP+ Class / Canvas.

---

## 1. Estructura de Entregables Oficiales

Los documentos finales se gestionan en dos ubicaciones complementarias:

1. **Documentación Oficial Versionada:**  
   `docs/01_ENTREGA_FINAL_PROYECTO_SEMANA_18/`  
   Contiene el paquete maestro oficial para el docente y el repositorio (Word, Markdown, Presentación PPTX, Visor Web HTML, Libro Excel de auditoría, compendio técnico y anexos).

2. **Carpeta Exclusiva de Subida a UTP+ Class (Ignorada en Git):**  
   `_SUBIR_A_UTP_CLASS/`  
   Carpeta local generada automáticamente que contiene **exactamente 1 archivo por tipo** (sin duplicados ni redundancias), respetando la jerarquía de prioridad del docente:
   - **Prioridad 1 (Word):** `01_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.docx`
   - **Prioridad 2 (PDF):** `02_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.pdf`
   - **Prioridad 3 (Excel):** `03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx`
   - **Prioridad 4 (PowerPoint):** `04_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT_GRUPO01.pptx`

---

## 2. Catálogo de Scripts y Responsabilidades

| Script | Lenguaje / Entorno | Propósito y Responsabilidad |
| :--- | :--- | :--- |
| **`build_all.ps1`** | PowerShell (`pwsh`) | **Orquestador Maestro.** Verifica dependencias (`pandoc`, `mmdc`, librerías Python), compila el informe final acumulativo, genera la presentación PPTX, el visor web HTML, el libro Excel XLSX, exporta a `_SUBIR_A_UTP_CLASS/` y ejecuta la validación de integridad. |
| **`build_informe_s14_s15.py`** | Python 3 + Pandoc | Genera el informe final acumulativo (`01_INFORME_FINAL_PROYECTO_LEOFIT.docx` y `.md`) con portada formal, códigos de estudiantes, credenciales de acceso, URLs verificables y evaluación integral ISO 25010 / ISO 9126. |
| **`generate_sustentacion_pptx.py`** | Python 3 + python-pptx | Genera la presentación ejecutiva oficial de **20 diapositivas** en formato widescreen 16:9 con paleta institucional Navy/Blue/Accent, contraste WCAG AAA y notas de orador integradas. |
| **`generate_slides_viewer.py`** | Python 3 | Genera el visor web interactivo (`02_VISOR_WEB_PRESENTACION_SUSTENTACION.html`) para previsualizar y proyectar las diapositivas con notas de orador en cualquier navegador. |
| **`generate_audit_xlsx.py`** | Python 3 + openpyxl | Genera el libro Excel de auditoría y trazabilidad con 7 pestañas formateadas: Dashboard, Trazabilidad, Auditoría ISO 25010, Resultados Testing, Criptografía, Inventario y Equipo. |
| **`export_subir_utp_class.py`** | Python 3 | Empaqueta exclusivamente los 4 archivos sin duplicados en `_SUBIR_A_UTP_CLASS/` y genera la versión PDF fidedigna vía Word COM. |
| **`validate_deliverables.py`** | Python 3 | Verifica que todos los archivos DOCX, PPTX y XLSX se abran sin errores, confirma el conteo de diapositivas con notas, pestañas de Excel y certifica la ausencia de emojis. |

---

## 3. Instrucciones de Compilación

Para compilar y exportar todos los entregables con un único comando:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\proyecto_final\build_all.ps1
```

---

## 4. Política de Control de Versiones

> [!NOTE]
> La carpeta `_SUBIR_A_UTP_CLASS/` se encuentra expresamente en el `.gitignore` para no sobrecargar el repositorio Git con binarios duplicados. Los archivos ofimáticos oficiales maestros se preservan en `docs/01_ENTREGA_FINAL_PROYECTO_SEMANA_18/`.

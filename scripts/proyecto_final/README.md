# Cadena de Herramientas y Scripts de Sustentación del Proyecto Final
## Sistema de Gestión de Pedidos Multicanal — LeoFit Solutions (Ciclo 2026-I)

Este directorio contiene las herramientas de automatización para compilar la documentación ofimática oficial del Proyecto Final (Semana 18) y los mecanismos de exposición/ocultamiento temporal para el día de la sustentación académica.

---

## 1. Requisito de Dependencia Local

> [!IMPORTANT]
> Los scripts de generación leen la documentación de anexos y emiten sus entregables en el directorio local:  
> `_PROYECTO_FINAL_LOCAL/02_ENTREGABLES_UTP/`  
> 
> Dicho directorio se encuentra en la raíz del repositorio y está explícitamente excluido del control de versiones (`.gitignore`) para mantener la visibilidad del repositorio enfocada exclusivamente en **APF3**.

### ¿Qué hacer si `_PROYECTO_FINAL_LOCAL/` no existe?
Si usted ha clonado este repositorio en una máquina nueva y no dispone de la carpeta:
1. No intente ejecutar los scripts de compilación sin antes contar con el paquete base.
2. Solicite el respaldo comprimido oficial al equipo de ingeniería (Lady Loayza / Grupo 01) o descárguelo desde la carpeta compartida en **Google Drive / OneDrive** del equipo.
3. Descomprima el contenido en la raíz del repositorio respetando el nombre exacto: `_PROYECTO_FINAL_LOCAL/`.

---

## 2. Catálogo de Scripts y Responsabilidades

| Script | Lenguaje / Entorno | Propósito y Responsabilidad |
| :--- | :--- | :--- |
| **`build_all.ps1`** | PowerShell (`pwsh`) | **Orquestador Maestro.** Verifica dependencias del sistema (`pandoc`, `mmdc`, paquetes Python), ejecuta la exportación DOCX, genera la presentación PPTX, compila el libro XLSX y ejecuta la validación rigurosa de integridad. |
| **`export_markdown_to_docx.py`** | Python 3 + Pandoc + python-docx | Procesa los 6 anexos técnicos Markdown, compila los bloques Mermaid a imágenes PNG vectoriales mediante `mmdc` y genera 9 documentos Word normalizados con estilos corporativos LeoFit. |
| **`generate_sustentacion_pptx.py`** | Python 3 + python-pptx | Genera la presentación ejecutiva de sustentación de **20 diapositivas** en formato widescreen 16:9 con paleta institucional Navy/Blue/Accent, contraste WCAG AAA y notas de orador integradas en cada lámina. |
| **`generate_audit_xlsx.py`** | Python 3 + openpyxl | Genera el libro Excel de auditoría y trazabilidad con 4 pestañas formateadas: `Matriz_Trazabilidad_Jurado`, `Inventario_Servicios_Cloud`, `Auditoria_Codigo_ISO25010` y `Gap_Analysis_SUNAT_CPE`. |
| **`validate_deliverables.py`** | Python 3 | Verifica que todos los archivos DOCX, PPTX y XLSX se abran sin errores, confirma el conteo mínimo de párrafos, tablas, 20 diapositivas con notas de orador y certifica la ausencia de emojis residuales. |
| **`expose_semana_18.ps1`** | PowerShell (`pwsh`) | **Toggle de Publicación.** Copia `_PROYECTO_FINAL_LOCAL/` hacia `docs/01_PROYECTO_FINAL_SEMANA_18/`, ejecuta `git add -f`, crea el commit temporal de sustentación y realiza el push a `origin/main`. |
| **`hide_semana_18.ps1`** | PowerShell (`pwsh`) | **Toggle de Ocultamiento.** Desindexa `docs/01_PROYECTO_FINAL_SEMANA_18/` mediante `git rm -r --cached`, elimina la copia en `docs/`, comitea el cambio y hace push a `origin/main`, regresando el repositorio a su estado seguro de solo APF3. |

---

## 3. Instrucciones de Uso Típico

### Compilación completa de entregables ofimáticos:
```powershell
pwsh scripts/proyecto_final/build_all.ps1
# O en Windows PowerShell 5.1:
powershell -ExecutionPolicy Bypass -File scripts\proyecto_final\build_all.ps1
```

### Flujo del Día de la Sustentación:
1. **Antes de ingresar a la sala de sustentación:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\proyecto_final\expose_semana_18.ps1
   ```
2. **Al concluir la defensa y evaluación académica:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\proyecto_final\hide_semana_18.ps1
   ```

---

## 4. Política de Control de Versiones

> [!WARNING]
> Todos los artefactos generados en `_PROYECTO_FINAL_LOCAL/02_ENTREGABLES_UTP/` (`01_DOCX/`, `02_PPTX/`, `03_XLSX/`, `.cache_diagrams/`) quedan **estrictamente ignorados por Git**. Únicamente los scripts fuente de este directorio forman parte del control de versiones principal.

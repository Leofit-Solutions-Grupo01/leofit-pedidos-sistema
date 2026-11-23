# ==============================================================================
# build_all.ps1 — Orquestador Maestro de Exportación Markdown -> Office (LeoFit)
# Proyecto Final - Semana 18 | UTP Curso Integrador II
# ==============================================================================
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$baseDir = Resolve-Path "$scriptDir\..\.."
$proyectoFinalDir = Join-Path $baseDir "_PROYECTO_FINAL_LOCAL"

if (-not (Test-Path "$baseDir\_PROYECTO_FINAL_LOCAL\02_ENTREGABLES_UTP")) {
    Write-Host "[ERROR] _PROYECTO_FINAL_LOCAL/ no existe. Ver scripts/proyecto_final/README.md" -ForegroundColor Red
    exit 1
}

$entregablesDir = Join-Path $proyectoFinalDir "02_ENTREGABLES_UTP"
$htmlDir = "$entregablesDir\00_HTML"
$docxDir = "$entregablesDir\01_DOCX"
$pptxDir = "$entregablesDir\02_PPTX"
$xlsxDir = "$entregablesDir\03_XLSX"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "INICIANDO CADENA DE CONSTRUCCION Y EXPORTACION OFICIAL (SEMANA 18)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Directorio Base: $baseDir" -ForegroundColor DarkGray
Write-Host "Proyecto Final Local: $proyectoFinalDir" -ForegroundColor DarkGray
Write-Host "Entregables UTP: $entregablesDir" -ForegroundColor DarkGray
Write-Host ""

# ------------------------------------------------------------------------------
# 1. VERIFICACION DE DEPENDENCIAS
# ------------------------------------------------------------------------------
Write-Host "[1/5] Verificando dependencias del sistema..." -ForegroundColor Yellow

$pandocVer = pandoc --version | Select-Object -First 1
Write-Host "  [OK] Pandoc: $pandocVer" -ForegroundColor Green

$mmdcVer = mmdc --version | Select-Object -First 1
Write-Host "  [OK] Mermaid CLI (mmdc): $mmdcVer" -ForegroundColor Green

$pyDeps = python -c "import docx, pptx, openpyxl, pypandoc; print('OK')"
if ($pyDeps -ne "OK") {
    Write-Host "  [ERROR] Faltan librerias de Python requeridas." -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] Python Packages (docx, pptx, openpyxl, pypandoc) disponibles." -ForegroundColor Green
Write-Host ""

# ------------------------------------------------------------------------------
# 2. GENERACION DE DOCUMENTOS HTML Y DOCX
# ------------------------------------------------------------------------------
Write-Host "[2/5] Generando documentos HTML estilizados y Word (.docx) editables..." -ForegroundColor Yellow
python "$scriptDir\export_markdown_to_docx.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Fallo la exportacion a HTML y DOCX." -ForegroundColor Red
    exit 1
}
Write-Host ""

# ------------------------------------------------------------------------------
# 3. GENERACION DE PRESENTACION PPTX (MINIMO 18 SLIDES CON NOTAS)
# ------------------------------------------------------------------------------
Write-Host "[3/5] Generando presentacion ejecutiva (.pptx) de 20 slides con notas de orador..." -ForegroundColor Yellow
python "$scriptDir\generate_sustentacion_pptx.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Fallo la generacion de PPTX." -ForegroundColor Red
    exit 1
}
Write-Host ""

# ------------------------------------------------------------------------------
# 4. GENERACION DE LIBRO DE AUDITORIA Y TRAZABILIDAD XLSX
# ------------------------------------------------------------------------------
Write-Host "[4/5] Generando libro Excel (.xlsx) de auditoria y trazabilidad..." -ForegroundColor Yellow
python "$scriptDir\generate_audit_xlsx.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Fallo la generacion de XLSX." -ForegroundColor Red
    exit 1
}
Write-Host ""

# ------------------------------------------------------------------------------
# 5. GENERACION DEL INFORME ACUMULATIVO Y VISOR WEB
# ------------------------------------------------------------------------------
Write-Host "[5/7] Generando Informe Acumulativo Final y Visor Web..." -ForegroundColor Yellow
python "$scriptDir\build_informe_s14_s15.py"
python "$scriptDir\generate_slides_viewer.py"
Write-Host ""

# ------------------------------------------------------------------------------
# 6. EXPORTACION A CARPETA EXCLUSIVA UTP+ CLASS / CANVAS
# ------------------------------------------------------------------------------
Write-Host "[6/7] Exportando archivos exclusivos a _SUBIR_A_UTP_CLASS/..." -ForegroundColor Yellow
python "$scriptDir\export_subir_utp_class.py"
Write-Host ""

# ------------------------------------------------------------------------------
# 7. VALIDACION RIGUROSA DE INTEGRIDAD Y REPORTE DE TAMANOS
# ------------------------------------------------------------------------------
Write-Host "[7/7] Validando integridad de todos los archivos generados..." -ForegroundColor Yellow

python "$scriptDir\validate_deliverables.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Fallo la validacion de integridad." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "INVENTARIO DE ARCHIVOS LISTOS PARA SUBIR A UTP+ CLASS (CANVAS)" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green

$utpFiles = Get-ChildItem -Path "$baseDir\_SUBIR_A_UTP_CLASS" -File
$tableReport = @()

foreach ($f in $utpFiles) {
    $sizeKb = [math]::Round($f.Length / 1KB, 1)
    $tableReport += [PSCustomObject]@{
        "Nombre del Archivo" = $f.Name
        "Tamano (KB)"        = $sizeKb
        "Prioridad"          = if ($f.Extension -eq ".docx") { "1 - Word (Principal)" } elseif ($f.Extension -eq ".pdf") { "2 - PDF" } elseif ($f.Extension -eq ".xlsx") { "3 - Excel" } elseif ($f.Extension -eq ".pptx") { "4 - PowerPoint" } else { "Informativo" }
    }
}

$tableReport | Format-Table -AutoSize

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "PROCESO COMPLETADO EXITOSAMENTE CON CERO ERRORES Y CERO EMOJIS" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

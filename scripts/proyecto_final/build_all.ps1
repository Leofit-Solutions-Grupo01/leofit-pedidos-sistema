# ==============================================================================
# build_all.ps1 — Orquestador Maestro de Construcción y Exportación (LeoFit)
# Proyecto Final - Semana 18 | UTP Curso Integrador II
# ==============================================================================
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$baseDir = Resolve-Path "$scriptDir\..\.."
$docsDir = Join-Path $baseDir "docs\01_ENTREGA_FINAL_PROYECTO_SEMANA_18"
$utpDir = Join-Path $baseDir "_SUBIR_A_UTP_CLASS"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "INICIANDO CADENA DE CONSTRUCCION Y EXPORTACION OFICIAL (SEMANA 18)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Directorio Base: $baseDir" -ForegroundColor DarkGray
Write-Host "Docs Oficiales:  $docsDir" -ForegroundColor DarkGray
Write-Host "Subir a UTP+:    $utpDir" -ForegroundColor DarkGray
Write-Host ""

# ------------------------------------------------------------------------------
# 1. VERIFICACION DE DEPENDENCIAS
# ------------------------------------------------------------------------------
Write-Host "[1/6] Verificando dependencias del sistema..." -ForegroundColor Yellow

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
# 2. GENERACION DEL INFORME ACUMULATIVO FINAL (WORD Y MARKDOWN)
# ------------------------------------------------------------------------------
Write-Host "[2/6] Compilando Informe Acumulativo Final (.docx y .md)..." -ForegroundColor Yellow
python "$scriptDir\build_informe_s14_s15.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Fallo la compilacion del Informe Final." -ForegroundColor Red
    exit 1
}
Write-Host ""

# ------------------------------------------------------------------------------
# 3. GENERACION DE PRESENTACION PPTX Y VISOR WEB
# ------------------------------------------------------------------------------
Write-Host "[3/6] Generando presentacion ejecutiva (.pptx) y visor web (.html)..." -ForegroundColor Yellow
python "$scriptDir\generate_sustentacion_pptx.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Fallo la generacion de PPTX." -ForegroundColor Red
    exit 1
}
python "$scriptDir\generate_slides_viewer.py"
Write-Host ""

# ------------------------------------------------------------------------------
# 4. GENERACION DE LIBRO DE AUDITORIA Y TRAZABILIDAD XLSX
# ------------------------------------------------------------------------------
Write-Host "[4/6] Generando libro Excel (.xlsx) de auditoria y trazabilidad..." -ForegroundColor Yellow
python "$scriptDir\generate_audit_xlsx.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Fallo la generacion de XLSX." -ForegroundColor Red
    exit 1
}
Write-Host ""

# ------------------------------------------------------------------------------
# 5. EXPORTACION A CARPETA EXCLUSIVA UTP+ CLASS (1 ARCHIVO POR TIPO)
# ------------------------------------------------------------------------------
Write-Host "[5/6] Exportando archivos exclusivos a _SUBIR_A_UTP_CLASS/..." -ForegroundColor Yellow
python "$scriptDir\export_subir_utp_class.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Fallo la exportacion a _SUBIR_A_UTP_CLASS." -ForegroundColor Red
    exit 1
}
Write-Host ""

# ------------------------------------------------------------------------------
# 6. VALIDACION RIGUROSA DE INTEGRIDAD Y REPORTE DE TAMANOS
# ------------------------------------------------------------------------------
Write-Host "[6/6] Validando integridad de todos los archivos generados..." -ForegroundColor Yellow
python "$scriptDir\validate_deliverables.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Fallo la validacion de integridad." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "INVENTARIO DE ARCHIVOS LISTOS PARA SUBIR A UTP+ CLASS (CANVAS)" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green

$utpFiles = Get-ChildItem -Path $utpDir -File
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

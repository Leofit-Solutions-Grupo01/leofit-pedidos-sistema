# ==============================================================================
# hide_semana_18.ps1 — Oculta el Proyecto Final tras la sustentación
# ==============================================================================
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$baseDir = Resolve-Path "$scriptDir\..\.."
$targetDir = Join-Path $baseDir "docs\01_PROYECTO_FINAL_SEMANA_18"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "OCULTAR PROYECTO FINAL (SEMANA 18) TRAS SUSTENTACION" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Validar precondiciones
if (-not (Test-Path $targetDir)) {
    Write-Host "[WARN] No existe $targetDir en docs/. El Proyecto Final ya se encuentra oculto." -ForegroundColor Yellow
    exit 0
}

# Guardar commit hash actual por seguridad
$previousCommit = git rev-parse HEAD

try {
    # 2. Desindexar de Git
    Write-Host "[1/4] Desindexando docs/01_PROYECTO_FINAL_SEMANA_18 del control de versiones..." -ForegroundColor Yellow
    git rm -r --cached docs/01_PROYECTO_FINAL_SEMANA_18/

    # 3. Eliminar copia en docs/ (el original en _PROYECTO_FINAL_LOCAL se mantiene intacto)
    Write-Host "[2/4] Eliminando copia fisica en docs/..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $targetDir

    # 4. Commit
    Write-Host "[3/4] Creando commit de ocultamiento..." -ForegroundColor Yellow
    git commit -m "chore(sustentacion): oculta proyecto final tras sustentacion"

    # 5. Push
    Write-Host "[4/4] Enviando cambios a origin/main..." -ForegroundColor Yellow
    git push origin main

    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host "OCULTADO EXITOSAMENTE. EL REPOSITORIO VUELVE A MOSTRAR UNICAMENTE APF3." -ForegroundColor Green
    Write-Host "El contenido del Proyecto Final permanece intacto en _PROYECTO_FINAL_LOCAL/." -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Green
}
catch {
    Write-Host ""
    Write-Host "[ERROR] Ocurrio un fallo durante la operacion: $_" -ForegroundColor Red
    Write-Host "Restaurando estado previo del repositorio..." -ForegroundColor Yellow

    git reset --hard $previousCommit
    Write-Host "Repositorio restaurado al commit $previousCommit." -ForegroundColor Yellow
    exit 1
}


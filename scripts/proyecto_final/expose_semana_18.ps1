# ==============================================================================
# expose_semana_18.ps1 — Publica temporalmente el Proyecto Final para sustentación
# ==============================================================================
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$baseDir = Resolve-Path "$scriptDir\..\.."
$localDir = Join-Path $baseDir "_PROYECTO_FINAL_LOCAL"
$targetDir = Join-Path $baseDir "docs\01_PROYECTO_FINAL_SEMANA_18"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "EXPONER PROYECTO FINAL (SEMANA 18) PARA SUSTENTACION" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Validar precondiciones
if (-not (Test-Path "$localDir\01_ANEXOS_TECNICOS")) {
    Write-Host "[ERROR] No se encontro $localDir\01_ANEXOS_TECNICOS. Operacion abortada." -ForegroundColor Red
    exit 1
}

# Guardar commit hash actual por seguridad
$previousCommit = git rev-parse HEAD

try {
    # 2. Copiar contenido local a docs/
    Write-Host "[1/4] Copiando _PROYECTO_FINAL_LOCAL a docs/01_PROYECTO_FINAL_SEMANA_18..." -ForegroundColor Yellow
    if (Test-Path $targetDir) {
        Remove-Item -Recurse -Force $targetDir
    }
    Copy-Item -Path $localDir -Destination $targetDir -Recurse

    # 3. Forzar git add ya que esta en .gitignore
    Write-Host "[2/4] Agregando archivos forzadamente al indice de Git..." -ForegroundColor Yellow
    git add -f docs/01_PROYECTO_FINAL_SEMANA_18/

    # 4. Commit
    Write-Host "[3/4] Creando commit de exposicion temporal..." -ForegroundColor Yellow
    git commit -m "chore(sustentacion): expone temporalmente proyecto final para revision"

    # 5. Push
    Write-Host "[4/4] Enviando cambios a origin/main..." -ForegroundColor Yellow
    git push origin main

    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host "EXPUESTO SATISFACTORIAMENTE EN ORIGIN/MAIN." -ForegroundColor Green
    Write-Host "Recuerda ejecutar hide_semana_18.ps1 despues de la sustentacion." -ForegroundColor Yellow
    Write-Host "======================================================================" -ForegroundColor Green
}
catch {
    Write-Host ""
    Write-Host "[ERROR] Ocurrio un fallo durante la operacion: $_" -ForegroundColor Red
    Write-Host "Restaurando estado previo del repositorio..." -ForegroundColor Yellow

    if (Test-Path $targetDir) {
        Remove-Item -Recurse -Force $targetDir
    }
    git reset --hard $previousCommit
    Write-Host "Repositorio restaurado al commit $previousCommit." -ForegroundColor Yellow
    exit 1
}


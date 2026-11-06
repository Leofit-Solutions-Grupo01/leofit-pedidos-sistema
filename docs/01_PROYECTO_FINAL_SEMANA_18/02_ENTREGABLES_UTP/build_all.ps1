# ==============================================================================
# build_all.ps1 — Wrapper de conveniencia para invocar scripts/build_all.ps1
# ==============================================================================
$scriptPath = Join-Path $PSScriptRoot "scripts\build_all.ps1"
& $scriptPath

<#
.SYNOPSIS
  Reubica los datos de la raíz del repo a la estructura de docs/01_estructura_del_repositorio.md.
.DESCRIPTION
  - NO usa git: no hace add, mv ni commit. Solo mueve archivos con Move-Item.
  - Por defecto es un ensayo (muestra qué haría). Para aplicar: .\scripts\reordenar_repo.ps1 -Aplicar
  - No sobrescribe archivos existentes.
  Ejecutar desde la raíz del repositorio (T:\pucp\clustering-nutricion-nna).
#>
param([switch]$Aplicar)
$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $PSScriptRoot
$moves = @()

$ficha  = Join-Path $raiz 'data\raw\ficha_nominal'
$nutri  = Join-Path $raiz 'data\raw\nutricion_mensual'
$refs   = Join-Path $raiz 'data\external\referencias_oms_cenan'

# Ficha nominal v1 (raíz)
$v1 = Join-Path $raiz 'FichaNominal_consolidado_IDs.xlsx'
if (Test-Path -LiteralPath $v1) { $moves += ,@($v1, (Join-Path $ficha 'FichaNominal_consolidado_IDs_v1.xlsx')) }

# Bloque 1: ficha nominal v2
Get-ChildItem -LiteralPath $raiz -Directory -Filter 'Datos TA - Bloque 1*' | ForEach-Object {
  Get-ChildItem -LiteralPath $_.FullName -File | ForEach-Object { $moves += ,@($_.FullName, (Join-Path $ficha $_.Name)) }
}
# Bloque 2: evaluaciones mensuales (xlsx) y referencias (pdf)
Get-ChildItem -LiteralPath $raiz -Directory -Filter 'Datos TA - Bloque 2*' | ForEach-Object {
  Get-ChildItem -LiteralPath $_.FullName -File | ForEach-Object {
    if ($_.Extension -ieq '.pdf') { $dest = Join-Path $refs $_.Name } else { $dest = Join-Path $nutri $_.Name }
    $moves += ,@($_.FullName, $dest)
  }
}

foreach ($m in $moves) {
  $src, $dst = $m
  if (Test-Path -LiteralPath $dst) { Write-Warning "Ya existe, se omite: $dst"; continue }
  if ($Aplicar) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
    Move-Item -LiteralPath $src -Destination $dst
    Write-Host "MOVIDO  $src  ->  $dst"
  } else {
    Write-Host "ENSAYO  $src  ->  $dst"
  }
}

if ($Aplicar) {
  # Elimina carpetas "Datos TA - Bloque…" solo si quedaron vacías
  Get-ChildItem -LiteralPath $raiz -Directory -Filter 'Datos TA - Bloque*' | ForEach-Object {
    if (-not (Get-ChildItem -LiteralPath $_.FullName -Force)) { Remove-Item -LiteralPath $_.FullName; Write-Host "Carpeta vacía eliminada: $($_.Name)" }
  }
  Write-Host "Listo. No se hizo ningún commit."
} else {
  Write-Host "Ensayo terminado: $($moves.Count) archivo(s). Repite con -Aplicar para mover."
}

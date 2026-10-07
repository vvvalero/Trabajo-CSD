# Compila la memoria a PDF (MiKTeX + latexmk). Uso:  .\build.ps1   |   .\build.ps1 -Clean
param([switch]$Clean)
Set-Location $PSScriptRoot
if ($Clean) { latexmk -C memoria.tex; Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue; exit }
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build memoria.tex
if ($LASTEXITCODE -eq 0) { Copy-Item build\memoria.pdf memoria.pdf -Force; "OK -> $PSScriptRoot\memoria.pdf" }

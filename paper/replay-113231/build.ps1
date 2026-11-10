param(
    [string]$Tectonic = (Join-Path $PSScriptRoot '.tools/tectonic/tectonic.exe')
)
$ErrorActionPreference = 'Stop'
$Out = Join-Path $PSScriptRoot 'build'
New-Item -ItemType Directory -Force -Path $Out | Out-Null
if (-not (Test-Path -LiteralPath $Tectonic)) { throw "Tectonic executable not found: $Tectonic" }
$Tex = Join-Path $PSScriptRoot 'paper.tex'
$Log = Join-Path $Out 'tectonic.log'
& $Tectonic --keep-logs --keep-intermediates --reruns 2 --outdir $Out $Tex 2>&1 | Tee-Object -FilePath $Log
if ($LASTEXITCODE -ne 0) { throw "Tectonic failed with exit code $LASTEXITCODE" }
$Pdf = Join-Path $Out 'paper.pdf'
if (-not (Test-Path -LiteralPath $Pdf)) { throw 'Tectonic completed without producing paper.pdf' }
Get-Item $Pdf | Select-Object FullName,Length

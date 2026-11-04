$ErrorActionPreference='Stop'
$root=Split-Path -Parent $MyInvocation.MyCommand.Path
$tectonic='D:\Anaconda\envs\latex\Library\bin\tectonic.exe'
if(-not (Test-Path $tectonic)){throw "tectonic not found: $tectonic"}
$cache=Join-Path $root 'tectonic-cache'
New-Item -ItemType Directory -Force -Path $cache | Out-Null
$env:TECTONIC_CACHE_DIR=$cache
$build=Join-Path $root 'build'
New-Item -ItemType Directory -Force -Path $build | Out-Null
& $tectonic -X compile --keep-logs --outdir $build (Join-Path $root 'paper.tex')
if($LASTEXITCODE -ne 0){throw "short-paper build failed: $LASTEXITCODE"}
$stamp=Get-Date -Format o
Set-Content -Encoding utf8 (Join-Path $build 'LAST_BUILD.txt') $stamp
Write-Output "BUILT $build/paper.pdf"

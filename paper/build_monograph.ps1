$root=Split-Path -Parent $MyInvocation.MyCommand.Path
$tectonic='D:\Anaconda\envs\latex\Library\bin\tectonic.exe'
if(-not (Test-Path $tectonic)){throw "tectonic not found: $tectonic"}
$cache=Join-Path $root 'tectonic-cache'
New-Item -ItemType Directory -Force -Path $cache | Out-Null
$env:TECTONIC_CACHE_DIR=$cache
$build=Join-Path $root 'build'
New-Item -ItemType Directory -Force -Path $build | Out-Null

# structure gate first: modular main file, every \input target present, no orphan parts,
# no script writes back to a source
$ErrorActionPreference='Stop'
python (Join-Path $root 'structure_check_monograph.py')
if($LASTEXITCODE -ne 0){throw "structure check failed: $LASTEXITCODE"}

# tectonic writes its diagnostics to stderr; under $ErrorActionPreference='Stop' PowerShell turns that
# into a terminating NativeCommandError, so the compile step runs with 'Continue' and the exit code is
# checked explicitly instead.
$ErrorActionPreference='Continue'
& $tectonic -X compile --keep-logs --outdir $build (Join-Path $root 'monograph.tex') 2> (Join-Path $build 'warnings.txt') 1> $null
$en=$LASTEXITCODE
$ErrorActionPreference='Stop'
if($en -ne 0){throw "English build failed: $en"}

# artifact gate: the PDF exists and is newer than every source file
$sources=@(Get-ChildItem (Join-Path $root '*.tex')) + @(Get-ChildItem (Join-Path $root 'sections\*.tex'))
$newest=($sources | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime
$p=Join-Path $build 'monograph.pdf'
if(-not (Test-Path $p)){throw "missing artifact: monograph.pdf"}
if((Get-Item $p).LastWriteTime -lt $newest){throw "stale artifact (older than sources): monograph.pdf"}

# page-margin QC
python (Join-Path $root 'artifact_qc.py')
if($LASTEXITCODE -ne 0){throw "artifact QC failed: $LASTEXITCODE"}

Set-Content -Encoding utf8 (Join-Path $build 'LAST_BUILD_MONOGRAPH.txt') (Get-Date -Format o)
Write-Output "BUILT $build/monograph.pdf"

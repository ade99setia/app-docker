$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvDir = Join-Path $scriptDir '.venv'
$pythonExe = Join-Path $venvDir 'Scripts\python.exe'
$requirementsFile = Join-Path $scriptDir 'requirements.txt'
$envFile = Join-Path $scriptDir '.env'
$exampleEnvFile = Join-Path $scriptDir '.env.example'
$appScript = Join-Path $scriptDir 'polling_forwarder.py'

if (-not (Test-Path $venvDir)) {
    python -m venv $venvDir
}

if (-not (Test-Path $pythonExe)) {
    throw "Python virtual environment not found at $pythonExe"
}

if (-not (Test-Path $envFile) -and (Test-Path $exampleEnvFile)) {
    Copy-Item $exampleEnvFile $envFile
}

& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r $requirementsFile
& $pythonExe $appScript
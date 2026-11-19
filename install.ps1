$ErrorActionPreference = "Stop"
Write-Host "=== Epah Scholarship setup ===" -ForegroundColor Cyan
if (!(Test-Path ".\run.py") -or !(Test-Path ".\requirements.txt")) {
    throw "Open the epah_scholarship project root (the folder containing run.py and requirements.txt)."
}

$pythonLauncher = Get-Command py -ErrorAction SilentlyContinue
$selected = $null
if ($pythonLauncher) {
    foreach ($version in @("3.15", "3.14", "3.13", "3.12")) {
        & py "-$version" -c "import sys; print(sys.version)" 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) { $selected = $version; break }
    }
}
if (!$selected) {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand) {
        $versionText = & python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
        if ($versionText -in @("3.15", "3.14", "3.13", "3.12")) { $selected = "system" }
    }
}
if (!$selected) { throw "Python 3.12, 3.13, 3.14 or 3.15 was not found. Install a supported Python version and retry." }

if (Test-Path ".\.venv") {
    if (!(Test-Path ".\.venv\Scripts\python.exe")) { throw "The .venv folder is incomplete. Rename it to .venv-backup and rerun install.ps1." }
    $venvVersion = & ".\.venv\Scripts\python.exe" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    if ($venvVersion -notin @("3.15", "3.14", "3.13", "3.12")) { throw "The existing .venv uses unsupported Python $venvVersion. Rename .venv to .venv-backup and rerun." }
} else {
    if ($selected -eq "system") { & python -m venv .venv }
    else { & py "-$selected" -m venv .venv }
    if ($LASTEXITCODE -ne 0) { throw "Could not create the virtual environment." }
}

$python = ".\.venv\Scripts\python.exe"
& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed. Check your internet connection and retry." }
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed. Check your internet connection and copy the complete error if you need help." }
& $python -m pip check
if ($LASTEXITCODE -ne 0) { throw "Dependency conflicts were detected." }

if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    $bytes = New-Object byte[] 48
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($bytes)
    $secret = [Convert]::ToBase64String($bytes)
    $rng.Dispose()
    (Get-Content ".env" -Raw).Replace("replace-with-a-long-random-secret", $secret) | Set-Content ".env" -NoNewline
}
New-Item -ItemType Directory -Force -Path ".\instance", ".\uploads\public", ".\uploads\private" | Out-Null

Write-Host "Running automated tests..." -ForegroundColor Cyan
& $python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "Automated tests failed. Do not start the server until the failure is fixed." }
Write-Host "Epah Scholarship setup completed successfully." -ForegroundColor Green
Write-Host "Start the application with: .\start.ps1"

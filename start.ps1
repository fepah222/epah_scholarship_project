$ErrorActionPreference = "Stop"
if (!(Test-Path ".\run.py")) { throw "Open the epah_scholarship project root containing run.py." }
$python = ".\.venv\Scripts\python.exe"
if (!(Test-Path $python)) { throw "Environment not found. Run .\install.ps1 first." }
Write-Host "Starting Epah Scholarship at http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "Keep this terminal open. Press Ctrl+C to stop the server."
& $python .\run.py

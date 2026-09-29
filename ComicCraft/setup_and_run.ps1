$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "       ComicCraft - One Click Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Install Python 3.11+ and run this again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

Write-Host "Installing required packages..." -ForegroundColor Yellow
& $python -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env. Add your GEMINI_API_KEY, then run START_COMICRAFT.bat again." -ForegroundColor Yellow
    notepad "$PSScriptRoot\.env"
    Read-Host "After saving .env, press Enter to continue"
}

Write-Host "Starting ComicCraft..." -ForegroundColor Green
Write-Host "Open http://127.0.0.1:8000 in your browser." -ForegroundColor Green
& $python -m uvicorn app.main:app --reload

# Скрипт для запуска backend
Write-Host "Starting Backend Server..." -ForegroundColor Cyan

# Переход в директорию backend
Set-Location $PSScriptRoot\backend

# Проверка базы данных
if (-not (Test-Path kids_store.db)) {
    Write-Host "Database not found. Creating..." -ForegroundColor Yellow
    python -m scripts.init_db --clear
}

# Запуск сервера
Write-Host "`nStarting FastAPI server..." -ForegroundColor Yellow
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Gray

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


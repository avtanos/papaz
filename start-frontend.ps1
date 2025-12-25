# Скрипт для запуска frontend
Write-Host "Starting Frontend Server..." -ForegroundColor Cyan

# Переход в директорию frontend
Set-Location $PSScriptRoot\frontend

# Очистка кэша Vite
if (Test-Path node_modules\.vite) {
    Remove-Item -Recurse -Force node_modules\.vite
    Write-Host "Vite cache cleared" -ForegroundColor Green
}

# Запуск dev сервера
Write-Host "`nStarting Vite dev server..." -ForegroundColor Yellow
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Green
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Gray

npm run dev


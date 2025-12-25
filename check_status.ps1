Write-Host "Проверка статуса сервисов..." -ForegroundColor Cyan
Write-Host ""

# Проверка Backend
Write-Host "Backend (http://localhost:8000):" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing -TimeoutSec 2
    Write-Host "  ✓ Работает! Статус: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Gray
} catch {
    Write-Host "  ✗ Не запущен или недоступен" -ForegroundColor Red
    Write-Host "  Запустите: cd backend; python -m uvicorn app.main:app --reload" -ForegroundColor Gray
}

Write-Host ""

# Проверка Frontend
Write-Host "Frontend (http://localhost:3000):" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri http://localhost:3000 -UseBasicParsing -TimeoutSec 2
    Write-Host "  ✓ Работает! Статус: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Не запущен или недоступен" -ForegroundColor Red
    Write-Host "  Запустите: cd frontend; npm run dev" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Для запуска сервисов:" -ForegroundColor Cyan
Write-Host "  1. Backend:  cd backend; python -m uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "  2. Frontend: cd frontend; npm run dev" -ForegroundColor White


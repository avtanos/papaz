# Быстрое решение проблемы с интерфейсом

## Если интерфейс не отображается:

### Вариант 1: Использовать готовые скрипты

1. **Запустите Backend** (в отдельном окне PowerShell):
   ```powershell
   .\start-backend.ps1
   ```

2. **Запустите Frontend** (в другом окне PowerShell):
   ```powershell
   .\start-frontend.ps1
   ```

3. **Откройте браузер**: http://localhost:3000

### Вариант 2: Ручной запуск

1. **Остановите все процессы Node.js**:
   ```powershell
   Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
   ```

2. **Запустите Backend**:
   ```powershell
   cd D:\papaz\backend
   python -m uvicorn app.main:app --reload --port 8000
   ```

3. **В новом окне PowerShell запустите Frontend**:
   ```powershell
   cd D:\papaz\frontend
   npm run dev
   ```

4. **Откройте браузер**: http://localhost:3000

### Вариант 3: Если все еще не работает

1. **Откройте консоль браузера** (F12)
2. **Проверьте вкладку Console** на наличие ошибок
3. **Проверьте вкладку Network** - все ли файлы загружаются?

### Проверка

Выполните в PowerShell:
```powershell
# Проверка backend
Invoke-WebRequest -Uri http://localhost:8000/health

# Проверка frontend  
Invoke-WebRequest -Uri http://localhost:3000
```

Оба должны вернуть статус 200.

## Частые проблемы:

- **Белый экран**: Откройте F12 → Console, проверьте ошибки
- **"Cannot GET /"**: Frontend не запущен или запущен на другом порту
- **Ошибки загрузки**: Проверьте, что backend работает на порту 8000


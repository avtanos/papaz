# Решение проблем с интерфейсом

## Проблема: Интерфейс не отображается

### Решение 1: Перезапуск frontend

1. Остановите все процессы Node.js:
   ```powershell
   Get-Process | Where-Object {$_.ProcessName -eq "node"} | Stop-Process -Force
   ```

2. Перейдите в директорию frontend:
   ```powershell
   cd D:\papaz\frontend
   ```

3. Очистите кэш и переустановите зависимости:
   ```powershell
   Remove-Item -Recurse -Force node_modules\.vite -ErrorAction SilentlyContinue
   npm install
   ```

4. Запустите frontend:
   ```powershell
   npm run dev
   ```

5. Откройте в браузере: http://localhost:3000

### Решение 2: Проверка консоли браузера

1. Откройте http://localhost:3000 в браузере
2. Нажмите F12 для открытия DevTools
3. Перейдите на вкладку "Console"
4. Проверьте наличие ошибок (красные сообщения)

### Решение 3: Проверка портов

Убедитесь, что порты свободны:
```powershell
netstat -an | Select-String ":3000|:8000"
```

Если порты заняты, остановите процессы или измените порты в конфигурации.

### Решение 4: Проверка backend

Убедитесь, что backend работает:
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing
```

Должен вернуться статус 200.

### Решение 5: Проверка зависимостей

Убедитесь, что все зависимости установлены:
```powershell
cd D:\papaz\frontend
npm install
```

### Решение 6: Проверка TypeScript ошибок

```powershell
cd D:\papaz\frontend
npm run build
```

Если есть ошибки компиляции, исправьте их.

## Частые ошибки

### Ошибка: "Cannot find module"
**Решение**: Переустановите зависимости:
```powershell
cd D:\papaz\frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### Ошибка: "Port 3000 is already in use"
**Решение**: Остановите процесс на порту 3000 или измените порт в `vite.config.ts`

### Ошибка: "Failed to fetch" в консоли браузера
**Решение**: Убедитесь, что backend запущен на порту 8000

### Белый экран в браузере
**Решение**: 
1. Проверьте консоль браузера (F12)
2. Проверьте, что все файлы загружаются (вкладка Network в DevTools)
3. Убедитесь, что `main.tsx` и `App.tsx` существуют и корректны

## Быстрая проверка

Выполните эти команды для диагностики:

```powershell
# 1. Проверка файлов
Test-Path D:\papaz\frontend\index.html
Test-Path D:\papaz\frontend\src\main.tsx
Test-Path D:\papaz\frontend\src\App.tsx

# 2. Проверка портов
netstat -an | Select-String ":3000"

# 3. Проверка backend
Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing

# 4. Проверка frontend
Invoke-WebRequest -Uri http://localhost:3000 -UseBasicParsing
```

## Контакты для помощи

Если проблема не решена:
1. Проверьте логи в терминале, где запущен `npm run dev`
2. Проверьте консоль браузера (F12)
3. Убедитесь, что все зависимости установлены


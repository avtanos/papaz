# Настройка Railway для деплоя Backend

## Важно: Root Directory

Railway должен работать из папки `backend`. После подключения репозитория:

### Шаг 1: Подключите репозиторий

1. В Railway создайте новый проект
2. Выберите "Deploy from GitHub repo"
3. Выберите репозиторий `avtanos/papaz`

### Шаг 2: Настройте Root Directory

**КРИТИЧЕСКИ ВАЖНО:**

1. После создания сервиса, перейдите в **Settings** сервиса
2. Найдите раздел **Source**
3. Установите **Root Directory**: `backend`
4. Сохраните изменения

Без этого Railway будет искать файлы в корне репозитория и не сможет определить Python приложение.

### Шаг 3: Настройте переменные окружения

В разделе **Variables** добавьте:

```
DATABASE_URL=postgresql://... (Railway может предоставить автоматически)
CORS_ORIGINS=["https://avtanos.github.io","http://localhost:3000"]
```

Или используйте встроенную PostgreSQL базу данных Railway.

### Шаг 4: Команда запуска

Railway автоматически определит команду запуска из `Procfile` или `railway.json`:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Шаг 5: Инициализация базы данных

После успешного деплоя, подключитесь к серверу через Railway CLI или веб-консоль:

```bash
cd backend
python -m scripts.init_db --clear
```

Это создаст тестовые данные для Кыргызстана.

### Альтернатива: Использование Railway CLI

Если веб-интерфейс не позволяет установить Root Directory:

1. Установите Railway CLI: https://railway.app/cli
2. Выполните:
```bash
railway login
railway init
railway link
railway variables set RAILWAY_SERVICE_ROOT=backend
railway up
```

## Как найти URL вашего backend

### Способ 1: В веб-интерфейсе Railway

1. Откройте ваш проект в Railway
2. Выберите сервис (service) с backend
3. Перейдите на вкладку **Settings**
4. Прокрутите вниз до раздела **Networking**
5. Найдите **Public Domain** или **Generate Domain**
6. Нажмите **Generate Domain** если домен еще не создан
7. Скопируйте URL (например: `papaz-backend.railway.app`)

### Способ 2: Через вкладку Deployments

1. Откройте ваш проект
2. Перейдите на вкладку **Deployments**
3. Выберите последний успешный деплой
4. В правой панели найдите **Public URL** или **Domain**

### Способ 3: Через вкладку Variables

1. Откройте Settings → Variables
2. Найдите переменную `RAILWAY_PUBLIC_DOMAIN` (если есть)

## Проверка работы backend

После получения URL проверьте:

1. **Корневой путь**: `https://papaz-backend.railway.app/`
   - Должен вернуть: `{"message": "Система управления скидками для детского магазина"}`

2. **Health check**: `https://papaz-backend.railway.app/health`
   - Должен вернуть: `{"status": "ok"}`

3. **Документация API**: `https://papaz-backend.railway.app/api/docs`
   - Должна открыться Swagger UI с документацией всех endpoints

4. **Альтернативная документация**: `https://papaz-backend.railway.app/redoc`
   - ReDoc интерфейс

## Если видите дефолтную страницу Railway

Если вместо FastAPI приложения вы видите страницу "Home of the Railway API" с ASCII-артом поезда:

1. Проверьте логи деплоя в Railway (вкладка **Deployments** → выберите деплой → **View Logs**)
2. Убедитесь, что приложение запущено (должны быть логи uvicorn)
3. Проверьте, что используется правильный путь: `/api/...` (например: `/api/auth/login`)
4. Убедитесь, что Root Directory установлен в `backend`


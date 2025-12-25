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

## Проверка

После деплоя проверьте:
- URL сервиса (Railway предоставит его автоматически)
- Документация API: `https://your-app.railway.app/api/docs`
- Health check: `https://your-app.railway.app/health`


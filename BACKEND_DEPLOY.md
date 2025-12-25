# Деплой Backend на Railway

## Быстрый старт

### 1. Создайте аккаунт на Railway

1. Перейдите на https://railway.app
2. Войдите через GitHub
3. Нажмите "New Project"

### 2. Подключите репозиторий

1. Выберите "Deploy from GitHub repo"
2. Выберите репозиторий `avtanos/papaz`
3. **ВАЖНО**: В настройках сервиса укажите:
   - **Root Directory**: `backend`
   - Это можно сделать после создания сервиса в настройках (Settings → Source → Root Directory)

### 3. Настройте переменные окружения

В настройках проекта добавьте:

```
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-secret-key-here
```

Или используйте встроенную PostgreSQL базу данных Railway.

### 4. Настройте команду запуска

В настройках сервиса:
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 5. Получите URL backend

После деплоя Railway предоставит URL вида:
`https://your-app-name.railway.app`

### 6. Настройте CORS в backend

Убедитесь, что в `backend/app/main.py` настроен CORS для вашего frontend домена:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://avtanos.github.io",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 7. Обновите переменную окружения в GitHub

1. Перейдите в настройки репозитория: `Settings` → `Secrets and variables` → `Actions`
2. Добавьте новый секрет:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: `https://your-app-name.railway.app/api`

### 8. Перезапустите деплой frontend

После добавления секрета, перезапустите workflow в `Actions` или сделайте новый commit.

## Альтернативные варианты

### Render.com

1. Создайте новый Web Service
2. Подключите GitHub репозиторий
3. Укажите:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### PythonAnywhere

1. Загрузите код через Git
2. Настройте виртуальное окружение
3. Настройте WSGI файл
4. Обновите переменные окружения

## Проверка работы

После деплоя backend проверьте:

```bash
curl https://your-backend-url.com/api/docs
```

Должна открыться документация Swagger.

## Инициализация базы данных

После деплоя backend, подключитесь к серверу и выполните:

```bash
cd backend
python -m scripts.init_db --clear
```

Это создаст тестовые данные для Кыргызстана.


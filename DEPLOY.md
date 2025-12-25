# Деплой на GitHub Pages

Этот проект настроен для автоматического деплоя frontend на GitHub Pages.

## Настройка GitHub Pages

1. Перейдите в настройки репозитория: `Settings` → `Pages`
2. В разделе `Source` выберите:
   - **Source**: `GitHub Actions`
3. Сохраните изменения

## Автоматический деплой

После настройки, каждый push в ветку `main` автоматически запустит деплой через GitHub Actions.

Workflow файл находится в `.github/workflows/deploy.yml`

## Структура проекта

- **Frontend**: React + Vite приложение, деплоится на GitHub Pages
- **Backend**: FastAPI приложение, требует отдельного хостинга

## Backend хостинг

GitHub Pages поддерживает только статические сайты, поэтому backend нужно задеплоить отдельно:

### Варианты хостинга backend:

1. **Railway** (рекомендуется)
   - https://railway.app
   - Простой деплой из GitHub
   - Бесплатный тариф доступен

2. **Render**
   - https://render.com
   - Бесплатный тариф доступен

3. **Heroku**
   - https://heroku.com
   - Платный тариф

4. **PythonAnywhere**
   - https://www.pythonanywhere.com
   - Бесплатный тариф доступен

### После деплоя backend:

1. Получите URL вашего backend (например: `https://your-app.railway.app`)

2. Добавьте секрет в GitHub:
   - Перейдите в `Settings` → `Secrets and variables` → `Actions`
   - Нажмите `New repository secret`
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: `https://your-backend-url.com/api` (замените на ваш URL)
   - Нажмите `Add secret`

3. Перезапустите деплой frontend:
   - Перейдите в `Actions`
   - Выберите последний workflow
   - Нажмите `Re-run all jobs`

Или создайте файл `.env.production` в папке `frontend/` (но это менее безопасно):
```
VITE_API_BASE_URL=https://your-backend-url.com/api
```

## Локальная разработка

Для локальной разработки используйте:

```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## URL приложения

После деплоя приложение будет доступно по адресу:
`https://avtanos.github.io/papaz/`


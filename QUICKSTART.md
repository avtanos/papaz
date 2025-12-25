# Быстрый старт

## Предварительные требования

- Python 3.9+
- Node.js 16+
- Docker и Docker Compose
- PostgreSQL (через Docker)

## Шаги запуска

### 1. Запуск базы данных

```bash
docker-compose up -d postgres
```

### 2. Настройка и запуск Backend

```bash
cd backend

# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла (скопируйте из .env.example и настройте)
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/kids_store

# Создание миграций
alembic revision --autogenerate -m "Initial migration"

# Применение миграций
alembic upgrade head

# Инициализация тестовых данных (опционально)
python scripts/init_db.py

# Запуск сервера
uvicorn app.main:app --reload
```

Backend будет доступен на `http://localhost:8000`
API документация: `http://localhost:8000/docs`

### 3. Настройка и запуск Frontend

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev сервера
npm run dev
```

Frontend будет доступен на `http://localhost:3000`

## Тестирование системы

1. Откройте frontend: `http://localhost:3000`
2. Перейдите в раздел "Клиенты" и создайте тестового клиента
3. Перейдите в "Скидки" и создайте правило скидки
4. Перейдите в "Касса" и обработайте тестовую покупку
5. Проверьте "Аналитика" для просмотра статистики

## Примеры использования API

### Создание клиента
```bash
curl -X POST "http://localhost:8000/api/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+79991234567",
    "first_name": "Иван",
    "last_name": "Иванов",
    "email": "ivan@example.com"
  }'
```

### Обработка покупки через POS
```bash
curl -X POST "http://localhost:8000/api/pos/process-purchase?customer_id=1&store_id=1&amount=1500" \
  -H "Content-Type: application/json"
```

### Получение аналитики
```bash
curl "http://localhost:8000/api/analytics/summary?days=30"
```

## Структура проекта

- `backend/app/api/` - API endpoints
- `backend/app/models/` - Модели базы данных
- `backend/app/services/` - Бизнес-логика
- `backend/app/schemas/` - Pydantic схемы для валидации
- `frontend/src/pages/` - React страницы
- `frontend/src/services/` - API клиенты

## Дополнительная информация

См. `README.md` для подробной документации.


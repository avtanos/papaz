#!/bin/bash
# Скрипт запуска для Railway/Render

set -e  # Остановка при ошибке

# Если DATABASE_URL не установлен, используем SQLite
if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL="sqlite:///./kids_store.db"
    echo "Using SQLite database: $DATABASE_URL"
else
    echo "Using database from DATABASE_URL"
fi

# Railway автоматически устанавливает переменную $PORT
# Если PORT не установлен, используем 8000
if [ -z "$PORT" ]; then
    PORT=8000
    echo "PORT not set, using default: $PORT"
else
    echo "Using PORT from environment: $PORT"
fi

# Выводим все переменные окружения для отладки
echo "Environment variables:"
echo "  PORT=$PORT"
echo "  DATABASE_URL=$DATABASE_URL"

# Создаем директорию для данных если нужно
mkdir -p /app/data

# Запускаем приложение с логированием
# Используем явное указание порта как числа
echo "Starting uvicorn on port $PORT"
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --log-level info

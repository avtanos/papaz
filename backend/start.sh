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
PORT=${PORT:-8000}
echo "Starting server on port $PORT"

# Создаем директорию для данных если нужно
mkdir -p /app/data

# Запускаем приложение с логированием
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level info


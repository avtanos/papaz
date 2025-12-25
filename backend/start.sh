#!/bin/bash
# Скрипт запуска для Railway/Render

# Если DATABASE_URL не установлен, используем SQLite
if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL="sqlite:///./kids_store.db"
fi

# Railway автоматически устанавливает переменную $PORT
# Если PORT не установлен, используем 8000
PORT=${PORT:-8000}

# Запускаем приложение
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT


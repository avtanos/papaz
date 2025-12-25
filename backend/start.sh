#!/bin/bash
# Скрипт запуска для Railway/Render

# Если DATABASE_URL не установлен, используем SQLite
if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL="sqlite:///./kids_store.db"
fi

# Запускаем приложение
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}


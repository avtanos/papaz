#!/usr/bin/env python3
"""
Скрипт запуска для Railway/Render
Читает переменную PORT из окружения и запускает uvicorn
"""
import os
import sys

# Получаем PORT из переменной окружения
port = int(os.environ.get("PORT", 8000))

# Получаем DATABASE_URL или используем SQLite по умолчанию
database_url = os.environ.get("DATABASE_URL", "sqlite:///./kids_store.db")
os.environ["DATABASE_URL"] = database_url

print(f"Starting server on port {port}")
print(f"Database URL: {database_url}")

# Запускаем uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )


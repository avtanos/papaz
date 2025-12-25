from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./kids_store.db"  # Временно SQLite для быстрого запуска
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://avtanos.github.io",
        "https://*.github.io"
    ]
    
    # Redis (для Celery)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Email/SMS settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # SMS provider
    SMS_API_KEY: str = ""
    
    # Push notifications
    FCM_SERVER_KEY: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import customers, bonuses, discounts, pos, analytics, notifications, stores, auth

app = FastAPI(
    title="Детский магазин - Система скидок",
    description="Комплексная система управления скидками и бонусами",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(customers.router, prefix="/api/customers", tags=["Клиенты"])
app.include_router(bonuses.router, prefix="/api/bonuses", tags=["Бонусы"])
app.include_router(discounts.router, prefix="/api/discounts", tags=["Скидки"])
app.include_router(pos.router, prefix="/api/pos", tags=["Касса"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Аналитика"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Уведомления"])
app.include_router(stores.router, prefix="/api/stores", tags=["Магазины"])
app.include_router(auth.router, prefix="/api/auth", tags=["Авторизация"])


@app.get("/")
async def root():
    return {"message": "Система управления скидками для детского магазина"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


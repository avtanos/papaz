"""
Скрипт для создания тестовых кассиров
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import *
from app.services.cashier_service import CashierService
from app.schemas.auth import CashierCreate

# Супер-админ
ADMIN_DATA = {
    "username": "admin",
    "password": "admin123",
    "full_name": "Администратор системы",
    "store_id": 1,  # Привязка к первому магазину, но супер-админ может видеть все
    "is_superuser": True
}

# Тестовые кассиры для каждого магазина (Кыргызстан)
CASHIERS_DATA = [
    {"username": "cashier1", "password": "password1", "full_name": "Айбек Акматов", "store_id": 1},
    {"username": "cashier2", "password": "password2", "full_name": "Айзада Канатбекова", "store_id": 1},
    {"username": "cashier3", "password": "password3", "full_name": "Нурзат Абдуллаев", "store_id": 2},
    {"username": "cashier4", "password": "password4", "full_name": "Айгуль Омурзакова", "store_id": 2},
    {"username": "cashier5", "password": "password5", "full_name": "Эркин Бекболотов", "store_id": 3},
    {"username": "cashier6", "password": "password6", "full_name": "Жаныл Асанова", "store_id": 4},
    {"username": "cashier7", "password": "password7", "full_name": "Талгат Жумалиев", "store_id": 5},
]


def create_cashiers():
    """Создание тестовых кассиров"""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Создание супер-админа...")
        # Создаем супер-админа
        existing_admin = CashierService.get_cashier_by_username(db, ADMIN_DATA["username"])
        if existing_admin:
            # Обновляем существующего админа
            existing_admin.is_superuser = True
            existing_admin.is_active = True
            db.commit()
            print(f"  [OK] Супер-админ {ADMIN_DATA['username']} обновлен")
        else:
            try:
                admin_create = CashierCreate(
                    username=ADMIN_DATA["username"],
                    password=ADMIN_DATA["password"],
                    full_name=ADMIN_DATA["full_name"],
                    store_id=ADMIN_DATA["store_id"]
                )
                admin = CashierService.create_cashier(db, admin_create)
                # Устанавливаем флаг супер-админа
                admin.is_superuser = True
                db.commit()
                print(f"  [OK] Создан супер-админ: {admin.username}")
            except Exception as e:
                print(f"  [ERROR] Ошибка при создании супер-админа: {e}")
        
        print("\nСоздание кассиров...")
        created = 0
        
        for cashier_data in CASHIERS_DATA:
            # Проверяем, существует ли кассир
            existing = CashierService.get_cashier_by_username(db, cashier_data["username"])
            if existing:
                print(f"  Кассир {cashier_data['username']} уже существует, пропускаем")
                continue
            
            try:
                cashier_create = CashierCreate(
                    username=cashier_data["username"],
                    password=cashier_data["password"],
                    full_name=cashier_data["full_name"],
                    store_id=cashier_data["store_id"]
                )
                cashier = CashierService.create_cashier(db, cashier_create)
                print(f"  [OK] Создан кассир: {cashier.username} (Магазин ID: {cashier.store_id})")
                created += 1
            except Exception as e:
                print(f"  [ERROR] Ошибка при создании {cashier_data['username']}: {e}")
        
        print(f"\nСоздано кассиров: {created}")
        print("\nДанные для входа:")
        print("=" * 50)
        print("СУПЕР-АДМИН:")
        print(f"  Логин: {ADMIN_DATA['username']}")
        print(f"  Пароль: {ADMIN_DATA['password']}")
        print("\nКассиры:")
        for cashier_data in CASHIERS_DATA:
            print(f"  Логин: {cashier_data['username']}, Пароль: {cashier_data['password']}")
        print("=" * 50)
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_cashiers()


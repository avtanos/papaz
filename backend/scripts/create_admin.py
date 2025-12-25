"""
Скрипт для создания супер-админа
"""
from app.core.database import SessionLocal
from app.models.cashier import Cashier
from app.core.security import get_password_hash

def create_admin():
    """Создание или обновление супер-админа"""
    db = SessionLocal()
    
    try:
        admin = db.query(Cashier).filter(Cashier.username == 'admin').first()
        
        if admin:
            # Обновляем существующего админа
            admin.is_superuser = True
            admin.is_active = True
            admin.hashed_password = get_password_hash('admin123')
            admin.full_name = 'Администратор системы'
            db.commit()
            print('[OK] Супер-админ обновлен')
        else:
            # Создаем нового админа
            admin = Cashier(
                username='admin',
                hashed_password=get_password_hash('admin123'),
                full_name='Администратор системы',
                store_id=1,  # Техническая привязка, но супер-админ видит все магазины
                is_superuser=True,
                is_active=True
            )
            db.add(admin)
            db.commit()
            print('[OK] Супер-админ создан')
        
        print('\nДанные для входа:')
        print('Логин: admin')
        print('Пароль: admin123')
        
    except Exception as e:
        db.rollback()
        print(f'Ошибка: {e}')
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()


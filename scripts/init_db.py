"""
Скрипт для инициализации базы данных с тестовыми данными
"""
import random
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import *
from app.services.customer_service import CustomerService
from app.services.store_service import StoreService
from app.services.discount_service import DiscountService
from app.services.bonus_service import BonusService
from app.services.analytics_service import AnalyticsService
from app.schemas.customer import CustomerCreate, PurchaseCreate
from app.schemas.store import StoreCreate
from app.schemas.discount import DiscountCalculationRequest
from decimal import Decimal
from datetime import datetime, timedelta


# Мок-данные для клиентов (Кыргызстан)
CUSTOMERS_DATA = [
    {"phone": "+996555123456", "email": "aibek.akmatov@example.com", "first_name": "Айбек", "last_name": "Акматов"},
    {"phone": "+996555234567", "email": "aizada.kanatbekova@example.com", "first_name": "Айзада", "last_name": "Канатбекова"},
    {"phone": "+996555345678", "email": "nurzat.abdullaev@example.com", "first_name": "Нурзат", "last_name": "Абдуллаев"},
    {"phone": "+996555456789", "email": "aigul.omurzakova@example.com", "first_name": "Айгуль", "last_name": "Омурзакова"},
    {"phone": "+996555567890", "email": "erkin.bekbolotov@example.com", "first_name": "Эркин", "last_name": "Бекболотов"},
    {"phone": "+996555678901", "email": "janyl.asanova@example.com", "first_name": "Жаныл", "last_name": "Асанова"},
    {"phone": "+996555789012", "email": "talgat.zhumaliev@example.com", "first_name": "Талгат", "last_name": "Жумалиев"},
    {"phone": "+996555890123", "email": "gulnara.tynybekova@example.com", "first_name": "Гульнара", "last_name": "Тыныбекова"},
    {"phone": "+996555901234", "email": "bakyt.umarov@example.com", "first_name": "Бакыт", "last_name": "Умаров"},
    {"phone": "+996555012345", "email": "aizirek.raimkulova@example.com", "first_name": "Айзирек", "last_name": "Раймкулова"},
    {"phone": "+996555111222", "email": "nurlan.samatov@example.com", "first_name": "Нурлан", "last_name": "Саматов"},
    {"phone": "+996555222333", "email": "aigulym.berdibekova@example.com", "first_name": "Айгулым", "last_name": "Бердибекова"},
    {"phone": "+996555333444", "email": "erbol.azamatov@example.com", "first_name": "Эрбол", "last_name": "Азаматов"},
    {"phone": "+996555444555", "email": "jarkynai.kenenbaeva@example.com", "first_name": "Жаркынай", "last_name": "Кененбаева"},
    {"phone": "+996555555666", "email": "tilek.bolotbekov@example.com", "first_name": "Тилек", "last_name": "Болотбеков"},
]

# Мок-данные для магазинов (Бишкек, Кыргызстан)
STORES_DATA = [
    {"name": "Балалар дүйнөсү - Чынгыз Айтматов", "address": "г. Бишкек, пр. Чынгыза Айтматова, 30", "phone": "+996 (312) 61-23-45"},
    {"name": "Балалар дүйнөсү - Советская", "address": "г. Бишкек, ул. Советская, 96", "phone": "+996 (312) 62-34-56"},
    {"name": "Балалар дүйнөсү - ТЦ Дордой Плаза", "address": "г. Бишкек, ул. Ибраимова, 115", "phone": "+996 (312) 63-45-67"},
    {"name": "Балалар дүйнөсү - ТЦ Бишкек Парк", "address": "г. Бишкек, ул. Логвиненко, 1", "phone": "+996 (312) 64-56-78"},
    {"name": "Балалар дүйнөсү - Ошский рынок", "address": "г. Бишкек, ул. Ошская, 1", "phone": "+996 (312) 65-67-89"},
]

# Правила скидок
DISCOUNT_RULES = [
    {
        "name": "Скидка для новых клиентов",
        "description": "10% скидка для первых покупок",
        "discount_type": "percentage",
        "value": Decimal("10"),
        "min_purchase_amount": Decimal("500"),
        "is_new_customer_only": True,
        "max_uses_per_customer": 1,
    },
    {
        "name": "Скидка для постоянных клиентов",
        "description": "5% скидка при покупке от 2000₽",
        "discount_type": "percentage",
        "value": Decimal("5"),
        "min_purchase_amount": Decimal("2000"),
        "min_visits_required": 3,
        "max_discount_amount": Decimal("500"),
    },
    {
        "name": "Фиксированная скидка",
        "description": "200₽ скидка при покупке от 1500₽",
        "discount_type": "fixed_amount",
        "value": Decimal("200"),
        "min_purchase_amount": Decimal("1500"),
    },
    {
        "name": "VIP скидка",
        "description": "15% скидка для VIP клиентов",
        "discount_type": "percentage",
        "value": Decimal("15"),
        "min_purchase_amount": Decimal("3000"),
        "customer_segments": ["vip"],
        "max_discount_amount": Decimal("1000"),
    },
    {
        "name": "Скидка на день рождения",
        "description": "20% скидка в месяц дня рождения",
        "discount_type": "percentage",
        "value": Decimal("20"),
        "min_purchase_amount": Decimal("1000"),
        "max_uses_per_customer": 1,
    },
]


def create_stores(db: Session):
    """Создание магазинов"""
    stores = []
    for store_data in STORES_DATA:
        store = StoreService.create_store(db, StoreCreate(**store_data))
        stores.append(store)
    return stores


def create_customers(db: Session):
    """Создание клиентов"""
    customers = []
    for customer_data in CUSTOMERS_DATA:
        customer = CustomerService.create_customer(db, CustomerCreate(**customer_data))
        customers.append(customer)
    return customers


def create_discount_rules(db: Session):
    """Создание правил скидок"""
    rules = []
    for rule_data in DISCOUNT_RULES:
        rule = DiscountService.create_rule(db, rule_data)
        rules.append(rule)
    return rules


def create_purchase_history(db: Session, customers, stores):
    """Создание истории покупок"""
    purchases = []
    now = datetime.now()
    
    for customer in customers:
        # Количество покупок для каждого клиента (от 0 до 15)
        num_purchases = random.randint(0, 15)
        
        for i in range(num_purchases):
            # Дата покупки - случайная в последние 6 месяцев
            days_ago = random.randint(0, 180)
            purchase_date = now - timedelta(days=days_ago)
            
            # Случайная сумма покупки (от 300 до 5000)
            amount = Decimal(str(random.randint(300, 5000)))
            
            # Случайный магазин
            store = random.choice(stores)
            
            # Создаём покупку
            purchase_data = PurchaseCreate(
                customer_id=customer.id,
                store_id=store.id,
                amount=amount,
                items_count=random.randint(1, 10),
                payment_method=random.choice(["cash", "card", "online"]),
                receipt_number=f"RCP-{random.randint(1000, 9999)}",
            )
            
            purchase = CustomerService.create_purchase(db, purchase_data)
            
            # Обновляем дату покупки
            purchase.purchase_date = purchase_date
            db.flush()
            
            # Рассчитываем и применяем скидки
            try:
                discount_request = DiscountCalculationRequest(
                    customer_id=customer.id,
                    store_id=store.id,
                    amount=amount
                )
                discount_result = DiscountService.calculate_discounts(db, discount_request)
                
                if discount_result.applicable_discounts:
                    # Применяем первую доступную скидку
                    discount_info = discount_result.applicable_discounts[0]
                    DiscountService.apply_discount(
                        db,
                        discount_info["rule_id"],
                        purchase.id,
                        customer.id,
                        amount,
                        Decimal(str(discount_info["discount_amount"]))
                    )
                    purchase.discount_applied = discount_result.total_discount
                    purchase.amount = discount_result.final_amount
                
                # Начисляем бонусы
                if discount_result.bonuses_earned > 0:
                    BonusService.add_bonuses(
                        db,
                        customer.id,
                        discount_result.bonuses_earned,
                        description=f"Начислено за покупку #{purchase.id}",
                        purchase_id=purchase.id
                    )
                    purchase.bonuses_earned = discount_result.bonuses_earned
                
            except Exception as e:
                # Если ошибка при расчёте скидок, продолжаем
                pass
            
            purchases.append(purchase)
    
    db.commit()
    return purchases


def create_bonus_transactions(db: Session, customers):
    """Создание дополнительных бонусных транзакций"""
    for customer in customers:
        balance = BonusService.get_balance(db, customer.id)
        if balance and balance.current_balance > 0:
            # Иногда клиенты тратят бонусы
            if random.random() < 0.3:  # 30% вероятность
                spend_amount = min(
                    balance.current_balance,
                    Decimal(str(random.randint(50, 500)))
                )
                try:
                    BonusService.spend_bonuses(
                        db,
                        customer.id,
                        spend_amount,
                        description="Потрачено бонусов на покупку"
                    )
                except:
                    pass


def init_db(clear_existing=False):
    """Инициализация базы данных с тестовыми данными"""
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        if clear_existing:
            print("Очистка существующих данных...")
            # Удаляем данные в правильном порядке (из-за внешних ключей)
            db.query(DiscountApplication).delete()
            db.query(BonusTransaction).delete()
            db.query(PurchaseHistory).delete()
            db.query(BonusBalance).delete()
            db.query(CustomerSegment).delete()
            db.query(Customer).delete()
            db.query(DiscountRule).delete()
            db.query(Store).delete()
            db.commit()
            print("Данные очищены.")
        
        print("Создание магазинов...")
        stores = create_stores(db)
        print(f"[OK] Создано магазинов: {len(stores)}")
        
        print("Создание клиентов...")
        customers = create_customers(db)
        print(f"[OK] Создано клиентов: {len(customers)}")
        
        print("Создание правил скидок...")
        discount_rules = create_discount_rules(db)
        print(f"[OK] Создано правил скидок: {len(discount_rules)}")
        
        print("Создание истории покупок...")
        purchases = create_purchase_history(db, customers, stores)
        print(f"[OK] Создано покупок: {len(purchases)}")
        
        print("Создание бонусных транзакций...")
        create_bonus_transactions(db, customers)
        print("[OK] Бонусные транзакции созданы")
        
        print("Сегментация клиентов...")
        AnalyticsService.segment_customers(db)
        print("[OK] Сегментация выполнена")
        
        # Статистика
        total_revenue = sum(p.amount for p in purchases)
        total_customers = len(customers)
        customers_with_purchases = len(set(p.customer_id for p in purchases))
        
        print("\n" + "="*50)
        print("База данных успешно инициализирована!")
        print("="*50)
        print(f"Магазинов: {len(stores)}")
        print(f"Клиентов: {total_customers}")
        print(f"Клиентов с покупками: {customers_with_purchases}")
        print(f"Покупок: {len(purchases)}")
        print(f"Правил скидок: {len(discount_rules)}")
        print(f"Общая выручка: {total_revenue:.2f} руб.")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Ошибка при инициализации: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    clear = "--clear" in sys.argv or "-c" in sys.argv
    init_db(clear_existing=clear)

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models.customer import Customer, PurchaseHistory, CustomerStatus
from app.models.bonus import BonusBalance
from app.models.customer_history import CustomerHistory
from app.schemas.customer import CustomerCreate, CustomerUpdate, PurchaseCreate
from decimal import Decimal
import json


class CustomerService:
    @staticmethod
    def create_customer(db: Session, customer_data: CustomerCreate) -> Customer:
        customer = Customer(**customer_data.dict())
        db.add(customer)
        db.flush()
        
        # Создаём бонусный баланс для нового клиента
        bonus_balance = BonusBalance(customer_id=customer.id)
        db.add(bonus_balance)
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def get_customer(db: Session, customer_id: int) -> Customer:
        return db.query(Customer).filter(Customer.id == customer_id).first()

    @staticmethod
    def get_customer_by_phone(db: Session, phone: str) -> Customer:
        return db.query(Customer).filter(Customer.phone == phone).first()

    @staticmethod
    def update_customer(db: Session, customer_id: int, customer_data: CustomerUpdate, changed_by: int = None) -> Customer:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return None
        
        update_data = customer_data.dict(exclude_unset=True)
        changes = {}
        history_entries = []
        
        # Сохраняем старые значения и создаем записи истории
        for key, new_value in update_data.items():
            old_value = getattr(customer, key, None)
            
            # Преобразуем значения для сравнения
            if old_value is not None:
                old_value_str = str(old_value)
            else:
                old_value_str = None
                
            if new_value is not None:
                new_value_str = str(new_value)
            else:
                new_value_str = None
            
            # Если значение изменилось, сохраняем в историю
            if old_value_str != new_value_str:
                changes[key] = {"old": old_value_str, "new": new_value_str}
                
                history_entry = CustomerHistory(
                    customer_id=customer_id,
                    changed_by=changed_by,
                    change_type="update",
                    field_name=key,
                    old_value=old_value_str,
                    new_value=new_value_str,
                    changes=changes
                )
                history_entries.append(history_entry)
            
            # Обновляем значение
            setattr(customer, key, new_value)
        
        # Сохраняем все записи истории
        if history_entries:
            for entry in history_entries:
                entry.changes = changes  # Общие изменения для всех записей
                db.add(entry)
        
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def list_customers(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Customer).offset(skip).limit(limit).all()

    @staticmethod
    def create_purchase(db: Session, purchase_data: PurchaseCreate) -> PurchaseHistory:
        purchase = PurchaseHistory(**purchase_data.dict())
        db.add(purchase)
        db.flush()  # Получаем ID покупки, но не коммитим (commit будет позже)
        
        # Обновляем статистику клиента
        customer = db.query(Customer).filter(Customer.id == purchase_data.customer_id).first()
        if customer:
            customer.total_purchases += purchase_data.amount
            customer.total_visits += 1
            customer.last_visit = datetime.now()
        
        # Не делаем commit здесь, т.к. покупка будет обновлена позже
        return purchase

    @staticmethod
    def get_purchase_history(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
        return db.query(PurchaseHistory).filter(
            PurchaseHistory.customer_id == customer_id
        ).order_by(PurchaseHistory.purchase_date.desc()).offset(skip).limit(limit).all()


from sqlalchemy.orm import Session
from datetime import datetime
from app.models.cashier import Cashier
from app.core.security import verify_password, get_password_hash
from app.schemas.auth import CashierCreate


class CashierService:
    @staticmethod
    def authenticate_cashier(db: Session, username: str, password: str) -> Cashier:
        """Аутентификация кассира"""
        cashier = db.query(Cashier).filter(Cashier.username == username).first()
        if not cashier:
            return None
        if not verify_password(password, cashier.hashed_password):
            return None
        if not cashier.is_active:
            return None
        
        # Обновляем время последнего входа
        cashier.last_login = datetime.now()
        db.commit()
        
        return cashier

    @staticmethod
    def create_cashier(db: Session, cashier_data: CashierCreate) -> Cashier:
        """Создание нового кассира"""
        # Проверяем, существует ли пользователь
        existing = db.query(Cashier).filter(Cashier.username == cashier_data.username).first()
        if existing:
            raise ValueError("Cashier with this username already exists")
        
        cashier = Cashier(
            username=cashier_data.username,
            email=cashier_data.email,
            hashed_password=get_password_hash(cashier_data.password),
            full_name=cashier_data.full_name,
            store_id=cashier_data.store_id,
            is_superuser=False,  # По умолчанию не супер-админ
        )
        db.add(cashier)
        db.commit()
        db.refresh(cashier)
        return cashier

    @staticmethod
    def get_cashier(db: Session, cashier_id: int) -> Cashier:
        """Получение кассира по ID"""
        return db.query(Cashier).filter(Cashier.id == cashier_id).first()

    @staticmethod
    def get_cashier_by_username(db: Session, username: str) -> Cashier:
        """Получение кассира по username"""
        return db.query(Cashier).filter(Cashier.username == username).first()


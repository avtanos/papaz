from sqlalchemy.orm import Session
from datetime import datetime
from app.models.bonus import BonusBalance, BonusTransaction, BonusTransactionType
from app.models.customer import Customer
from app.schemas.bonus import BonusTransactionCreate
from decimal import Decimal


class BonusService:
    @staticmethod
    def get_balance(db: Session, customer_id: int) -> BonusBalance:
        return db.query(BonusBalance).filter(BonusBalance.customer_id == customer_id).first()

    @staticmethod
    def add_bonuses(db: Session, customer_id: int, amount: Decimal, description: str = None, purchase_id: int = None) -> BonusTransaction:
        balance = db.query(BonusBalance).filter(BonusBalance.customer_id == customer_id).first()
        if not balance:
            balance = BonusBalance(customer_id=customer_id)
            db.add(balance)
            db.flush()
        
        balance_before = balance.current_balance
        balance.current_balance += amount
        balance.total_earned += amount
        balance.last_updated = datetime.now()
        
        transaction = BonusTransaction(
            balance_id=balance.id,
            customer_id=customer_id,
            transaction_type=BonusTransactionType.EARNED,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance.current_balance,
            purchase_id=purchase_id,
            description=description or f"Начислено {amount} баллов"
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def spend_bonuses(db: Session, customer_id: int, amount: Decimal, description: str = None, purchase_id: int = None) -> BonusTransaction:
        balance = db.query(BonusBalance).filter(BonusBalance.customer_id == customer_id).first()
        if not balance or balance.current_balance < amount:
            raise ValueError("Недостаточно баллов")
        
        balance_before = balance.current_balance
        balance.current_balance -= amount
        balance.total_spent += amount
        balance.last_updated = datetime.now()
        
        transaction = BonusTransaction(
            balance_id=balance.id,
            customer_id=customer_id,
            transaction_type=BonusTransactionType.SPENT,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance.current_balance,
            purchase_id=purchase_id,
            description=description or f"Списано {amount} баллов"
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def calculate_bonuses(purchase_amount: Decimal, bonus_rate: Decimal = Decimal("0.01")) -> Decimal:
        """Расчёт бонусов: по умолчанию 1% от суммы покупки"""
        return (purchase_amount * bonus_rate).quantize(Decimal("0.01"))

    @staticmethod
    def get_transactions(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
        return db.query(BonusTransaction).filter(
            BonusTransaction.customer_id == customer_id
        ).order_by(BonusTransaction.transaction_date.desc()).offset(skip).limit(limit).all()


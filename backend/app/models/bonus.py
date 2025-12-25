from sqlalchemy import Column, Integer, Numeric, DateTime, String, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class BonusTransactionType(str, enum.Enum):
    EARNED = "earned"
    SPENT = "spent"
    EXPIRED = "expired"
    ADJUSTMENT = "adjustment"


class BonusBalance(Base):
    __tablename__ = "bonus_balances"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), unique=True, nullable=False)
    current_balance = Column(Numeric(10, 2), default=0)
    total_earned = Column(Numeric(10, 2), default=0)
    total_spent = Column(Numeric(10, 2), default=0)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="bonus_balance")
    transactions = relationship("BonusTransaction", back_populates="balance")


class BonusTransaction(Base):
    __tablename__ = "bonus_transactions"

    id = Column(Integer, primary_key=True, index=True)
    balance_id = Column(Integer, ForeignKey("bonus_balances.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    transaction_type = Column(Enum(BonusTransactionType), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    balance_before = Column(Numeric(10, 2), nullable=False)
    balance_after = Column(Numeric(10, 2), nullable=False)
    transaction_date = Column(DateTime, server_default=func.now())
    purchase_id = Column(Integer, ForeignKey("purchase_history.id"), nullable=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    balance = relationship("BonusBalance", back_populates="transactions")


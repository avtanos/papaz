from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class CustomerStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    VIP = "vip"


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    birth_date = Column(DateTime, nullable=True)
    status = Column(Enum(CustomerStatus), default=CustomerStatus.ACTIVE)
    registration_date = Column(DateTime, server_default=func.now())
    last_visit = Column(DateTime, nullable=True)
    total_purchases = Column(Numeric(10, 2), default=0)
    total_visits = Column(Integer, default=0)
    preferred_store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)
    
    # Relationships
    purchases = relationship("PurchaseHistory", back_populates="customer")
    bonus_balance = relationship("BonusBalance", back_populates="customer", uselist=False)
    segments = relationship("CustomerSegment", back_populates="customer")
    history = relationship("CustomerHistory", back_populates="customer", order_by="desc(CustomerHistory.changed_at)")


class PurchaseHistory(Base):
    __tablename__ = "purchase_history"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    purchase_date = Column(DateTime, server_default=func.now())
    amount = Column(Numeric(10, 2), nullable=False)
    items_count = Column(Integer, default=0)
    discount_applied = Column(Numeric(10, 2), default=0)
    bonuses_used = Column(Numeric(10, 2), default=0)
    bonuses_earned = Column(Numeric(10, 2), default=0)
    payment_method = Column(String(50), nullable=True)
    receipt_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    customer = relationship("Customer", back_populates="purchases")
    store = relationship("Store", back_populates="purchases")
    discount_applications = relationship("DiscountApplication", back_populates="purchase")


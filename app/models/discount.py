from sqlalchemy import Column, Integer, Numeric, DateTime, String, ForeignKey, Boolean, Text, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class DiscountType(str, enum.Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    BONUS_MULTIPLIER = "bonus_multiplier"


class DiscountRuleStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


class DiscountRule(Base):
    __tablename__ = "discount_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    discount_type = Column(Enum(DiscountType), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)  # процент или фиксированная сумма
    status = Column(Enum(DiscountRuleStatus), default=DiscountRuleStatus.ACTIVE)
    
    # Условия применения
    min_purchase_amount = Column(Numeric(10, 2), nullable=True)
    max_discount_amount = Column(Numeric(10, 2), nullable=True)
    applicable_categories = Column(JSON, nullable=True)  # список категорий товаров
    applicable_stores = Column(JSON, nullable=True)  # список ID магазинов
    
    # Ограничения
    max_uses_per_customer = Column(Integer, nullable=True)
    max_total_uses = Column(Integer, nullable=True)
    current_uses = Column(Integer, default=0)
    
    # Временные ограничения
    valid_from = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)
    
    # Сегментация
    customer_segments = Column(JSON, nullable=True)  # список сегментов клиентов
    is_new_customer_only = Column(Boolean, default=False)
    min_visits_required = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    applications = relationship("DiscountApplication", back_populates="rule")


class DiscountApplication(Base):
    __tablename__ = "discount_applications"

    id = Column(Integer, primary_key=True, index=True)
    discount_rule_id = Column(Integer, ForeignKey("discount_rules.id"), nullable=False)
    purchase_id = Column(Integer, ForeignKey("purchase_history.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    applied_at = Column(DateTime, server_default=func.now())
    discount_amount = Column(Numeric(10, 2), nullable=False)
    original_amount = Column(Numeric(10, 2), nullable=False)
    final_amount = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    rule = relationship("DiscountRule", back_populates="applications")
    purchase = relationship("PurchaseHistory", back_populates="discount_applications")


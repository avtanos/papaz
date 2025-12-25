from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    segment_name = Column(String(100), nullable=False)  # new, regular, vip, churned
    assigned_at = Column(DateTime, server_default=func.now())
    criteria = Column(JSON, nullable=True)  # критерии сегментации
    
    # Relationships
    customer = relationship("Customer", back_populates="segments")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    discount_rule_id = Column(Integer, ForeignKey("discount_rules.id"), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    target_segments = Column(JSON, nullable=True)
    total_budget = Column(Numeric(10, 2), nullable=True)
    spent_budget = Column(Numeric(10, 2), default=0)
    total_reach = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(String(50), default="active")


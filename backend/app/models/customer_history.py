from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class CustomerHistory(Base):
    """История изменений данных клиента"""
    __tablename__ = "customer_history"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    changed_by = Column(Integer, ForeignKey("cashiers.id"), nullable=True)  # Кто изменил
    change_type = Column(String(50), nullable=False)  # 'update', 'create', 'delete'
    field_name = Column(String(100), nullable=True)  # Какое поле изменилось
    old_value = Column(Text, nullable=True)  # Старое значение
    new_value = Column(Text, nullable=True)  # Новое значение
    changes = Column(JSON, nullable=True)  # JSON со всеми изменениями
    notes = Column(Text, nullable=True)  # Примечания
    changed_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    customer = relationship("Customer", back_populates="history")
    changed_by_cashier = relationship("Cashier", foreign_keys=[changed_by])


from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from decimal import Decimal


class CustomerBase(BaseModel):
    phone: str
    email: Optional[EmailStr] = None
    first_name: str
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    preferred_store_id: Optional[int] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    preferred_store_id: Optional[int] = None


class CustomerResponse(CustomerBase):
    id: int
    status: str
    registration_date: datetime
    last_visit: Optional[datetime]
    total_purchases: Decimal
    total_visits: int

    class Config:
        from_attributes = True


class PurchaseCreate(BaseModel):
    customer_id: int
    store_id: int
    amount: Decimal
    items_count: int = 0
    payment_method: Optional[str] = None
    receipt_number: Optional[str] = None
    notes: Optional[str] = None


class PurchaseResponse(BaseModel):
    id: int
    customer_id: int
    store_id: int
    purchase_date: datetime
    amount: Decimal
    items_count: int
    discount_applied: Decimal
    bonuses_used: Decimal
    bonuses_earned: Decimal
    payment_method: Optional[str]
    receipt_number: Optional[str]

    class Config:
        from_attributes = True


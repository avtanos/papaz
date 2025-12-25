from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any


class DiscountRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    discount_type: str
    value: Decimal
    min_purchase_amount: Optional[Decimal] = None
    max_discount_amount: Optional[Decimal] = None
    applicable_categories: Optional[List[str]] = None
    applicable_stores: Optional[List[int]] = None
    max_uses_per_customer: Optional[int] = None
    max_total_uses: Optional[int] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    customer_segments: Optional[List[str]] = None
    is_new_customer_only: bool = False
    min_visits_required: Optional[int] = None


class DiscountRuleCreate(DiscountRuleBase):
    pass


class DiscountRuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    value: Optional[Decimal] = None
    min_purchase_amount: Optional[Decimal] = None
    max_discount_amount: Optional[Decimal] = None
    applicable_categories: Optional[List[str]] = None
    applicable_stores: Optional[List[int]] = None
    max_uses_per_customer: Optional[int] = None
    max_total_uses: Optional[int] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    customer_segments: Optional[List[str]] = None
    is_new_customer_only: Optional[bool] = None
    min_visits_required: Optional[int] = None


class DiscountRuleResponse(DiscountRuleBase):
    id: int
    status: str
    current_uses: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DiscountApplicationResponse(BaseModel):
    id: int
    discount_rule_id: int
    purchase_id: int
    customer_id: int
    applied_at: datetime
    discount_amount: Decimal
    original_amount: Decimal
    final_amount: Decimal

    class Config:
        from_attributes = True


class DiscountCalculationRequest(BaseModel):
    customer_id: int
    store_id: int
    amount: Decimal
    items: Optional[List[Dict[str, Any]]] = None  # список товаров с категориями


class DiscountCalculationResponse(BaseModel):
    applicable_discounts: List[Dict[str, Any]]
    total_discount: Decimal
    final_amount: Decimal
    bonuses_earned: Decimal


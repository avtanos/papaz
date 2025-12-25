from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional


class BonusBalanceResponse(BaseModel):
    id: int
    customer_id: int
    current_balance: Decimal
    total_earned: Decimal
    total_spent: Decimal
    last_updated: datetime

    class Config:
        from_attributes = True


class BonusTransactionCreate(BaseModel):
    customer_id: int
    transaction_type: str
    amount: Decimal
    description: Optional[str] = None
    purchase_id: Optional[int] = None


class BonusTransactionResponse(BaseModel):
    id: int
    balance_id: int
    customer_id: int
    transaction_type: str
    amount: Decimal
    balance_before: Decimal
    balance_after: Decimal
    transaction_date: datetime
    purchase_id: Optional[int]
    description: Optional[str]

    class Config:
        from_attributes = True


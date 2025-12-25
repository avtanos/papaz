from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StoreBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class StoreCreate(StoreBase):
    pass


class StoreUpdate(StoreBase):
    is_active: Optional[bool] = None


class StoreResponse(StoreBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


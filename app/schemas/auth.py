from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class CashierLogin(BaseModel):
    username: str
    password: str


class CashierCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str
    full_name: str
    store_id: int


class CashierResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    full_name: str
    store_id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class CashierProfile(BaseModel):
    id: int
    username: str
    email: Optional[str]
    full_name: str
    store_id: int
    store_name: str
    is_active: bool
    is_superuser: bool = False

    class Config:
        from_attributes = True


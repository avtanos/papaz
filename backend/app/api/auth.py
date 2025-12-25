from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.dependencies import get_current_cashier
from app.services.cashier_service import CashierService
from app.schemas.auth import Token, CashierResponse, CashierProfile, CashierCreate
from app.models.cashier import Cashier

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Авторизация кассира"""
    cashier = CashierService.authenticate_cashier(db, form_data.username, form_data.password)
    if not cashier:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": cashier.username, "cashier_id": cashier.id, "store_id": cashier.store_id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=CashierProfile)
def read_cashier_me(current_cashier: Cashier = Depends(get_current_cashier), db: Session = Depends(get_db)):
    """Получение информации о текущем кассире"""
    store = current_cashier.store
    return {
        "id": current_cashier.id,
        "username": current_cashier.username,
        "email": current_cashier.email,
        "full_name": current_cashier.full_name,
        "store_id": current_cashier.store_id,
        "store_name": store.name if store else "",
        "is_active": current_cashier.is_active,
        "is_superuser": current_cashier.is_superuser,
    }


@router.post("/register", response_model=CashierResponse)
def register(cashier_data: CashierCreate, db: Session = Depends(get_db)):
    """Регистрация нового кассира (только для суперпользователей)"""
    try:
        cashier = CashierService.create_cashier(db, cashier_data)
        return cashier
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


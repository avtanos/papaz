from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from app.core.database import get_db
from app.schemas.bonus import BonusBalanceResponse, BonusTransactionResponse, BonusTransactionCreate
from app.services.bonus_service import BonusService

router = APIRouter()


@router.get("/{customer_id}/balance", response_model=BonusBalanceResponse)
def get_balance(customer_id: int, db: Session = Depends(get_db)):
    balance = BonusService.get_balance(db, customer_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Баланс не найден")
    return balance


@router.post("/{customer_id}/earn")
def earn_bonuses(
    customer_id: int,
    amount: Decimal,
    description: str = None,
    purchase_id: int = None,
    db: Session = Depends(get_db)
):
    transaction = BonusService.add_bonuses(db, customer_id, amount, description, purchase_id)
    return {"message": "Бонусы начислены", "transaction": transaction}


@router.post("/{customer_id}/spend")
def spend_bonuses(
    customer_id: int,
    amount: Decimal,
    description: str = None,
    purchase_id: int = None,
    db: Session = Depends(get_db)
):
    try:
        transaction = BonusService.spend_bonuses(db, customer_id, amount, description, purchase_id)
        return {"message": "Бонусы списаны", "transaction": transaction}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{customer_id}/transactions", response_model=List[BonusTransactionResponse])
def get_transactions(customer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return BonusService.get_transactions(db, customer_id, skip, limit)


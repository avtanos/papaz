from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_active_cashier
from app.schemas.store import StoreCreate, StoreResponse, StoreUpdate
from app.services.store_service import StoreService
from app.models.cashier import Cashier

router = APIRouter()


@router.post("/", response_model=StoreResponse)
def create_store(
    store: StoreCreate, 
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """Создание магазина (только для супер-админа)"""
    if not current_cashier.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only super-admin can create stores"
        )
    return StoreService.create_store(db, store)


@router.get("/")
def list_stores(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """Список магазинов с пагинацией (супер-админ видит все, кассир - только свой)"""
    from app.models.store import Store
    from sqlalchemy import func
    
    if current_cashier.is_superuser:
        total = db.query(func.count(Store.id)).scalar()
        stores = StoreService.list_stores(db, skip, limit)
        return {
            "items": stores,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    else:
        # Кассир видит только свой магазин
        store = StoreService.get_store(db, current_cashier.store_id)
        return {
            "items": [store] if store else [],
            "total": 1 if store else 0,
            "skip": 0,
            "limit": 1
        }


@router.get("/{store_id}", response_model=StoreResponse)
def get_store(
    store_id: int, 
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """Получение магазина (кассир может видеть только свой магазин)"""
    store = StoreService.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    
    # Кассир может видеть только свой магазин (кроме супер-админа)
    if not current_cashier.is_superuser and store_id != current_cashier.store_id:
        raise HTTPException(
            status_code=403,
            detail="You can only view your own store"
        )
    
    return store


@router.put("/{store_id}", response_model=StoreResponse)
def update_store(
    store_id: int,
    store: StoreUpdate,
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """Обновление магазина (только для супер-админа)"""
    if not current_cashier.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only super-admin can update stores"
        )
    
    updated = StoreService.update_store(db, store_id, store)
    if not updated:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    return updated


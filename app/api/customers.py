from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_active_cashier
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, PurchaseCreate, PurchaseResponse
from app.services.customer_service import CustomerService
from app.models.cashier import Cashier

router = APIRouter()


@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли клиент с таким телефоном
    existing = CustomerService.get_customer_by_phone(db, customer.phone)
    if existing:
        raise HTTPException(status_code=400, detail="Клиент с таким телефоном уже существует")
    
    return CustomerService.create_customer(db, customer)


@router.get("/")
def list_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """Список клиентов с пагинацией (для супер-админа - все клиенты, для кассира - только клиенты его магазина)"""
    from app.models.customer import PurchaseHistory, Customer
    from sqlalchemy import func
    
    # Если супер-админ - показываем всех клиентов
    if current_cashier.is_superuser:
        total = db.query(func.count(Customer.id)).scalar()
        customers = CustomerService.list_customers(db, skip, limit)
        return {
            "items": customers,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    
    # Для обычного кассира - фильтруем по магазину
    store_customer_ids = db.query(PurchaseHistory.customer_id).filter(
        PurchaseHistory.store_id == current_cashier.store_id
    ).distinct().all()
    store_customer_ids = [cid[0] for cid in store_customer_ids]
    
    # Получаем общее количество клиентов магазина
    total = db.query(func.count(Customer.id)).filter(
        Customer.id.in_(store_customer_ids)
    ).scalar() if store_customer_ids else 0
    
    # Получаем клиентов с пагинацией
    if store_customer_ids:
        customers = db.query(Customer).filter(
            Customer.id.in_(store_customer_ids)
        ).offset(skip).limit(limit).all()
    else:
        customers = []
    
    return {
        "items": customers,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerService.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return customer


@router.get("/phone/{phone}", response_model=CustomerResponse)
def get_customer_by_phone(phone: str, db: Session = Depends(get_db)):
    customer = CustomerService.get_customer_by_phone(db, phone)
    if not customer:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return customer


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int, 
    customer: CustomerUpdate, 
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """Обновление данных клиента с сохранением истории изменений"""
    updated = CustomerService.update_customer(db, customer_id, customer, current_cashier.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return updated


@router.get("/{customer_id}/history")
def get_customer_history(
    customer_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """Получение истории изменений клиента с пагинацией"""
    from app.models.customer_history import CustomerHistory
    from app.models.cashier import Cashier
    from sqlalchemy import func
    
    # Получаем общее количество записей истории
    total = db.query(func.count(CustomerHistory.id)).filter(
        CustomerHistory.customer_id == customer_id
    ).scalar()
    
    history = db.query(CustomerHistory).filter(
        CustomerHistory.customer_id == customer_id
    ).order_by(CustomerHistory.changed_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for h in history:
        cashier_name = None
        if h.changed_by:
            cashier = db.query(Cashier).filter(Cashier.id == h.changed_by).first()
            cashier_name = cashier.full_name if cashier else None
        
        result.append({
            "id": h.id,
            "changed_at": h.changed_at.isoformat(),
            "changed_by": cashier_name,
            "change_type": h.change_type,
            "field_name": h.field_name,
            "old_value": h.old_value,
            "new_value": h.new_value,
            "changes": h.changes,
            "notes": h.notes
        })
    
    return {
        "items": result,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/purchases", response_model=PurchaseResponse)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    return CustomerService.create_purchase(db, purchase)


@router.get("/{customer_id}/purchases")
def get_purchase_history(customer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получение истории покупок с информацией о магазине"""
    from app.models.store import Store
    
    purchases = CustomerService.get_purchase_history(db, customer_id, skip, limit)
    
    result = []
    for purchase in purchases:
        store = db.query(Store).filter(Store.id == purchase.store_id).first()
        purchase_dict = {
            "id": purchase.id,
            "customer_id": purchase.customer_id,
            "store_id": purchase.store_id,
            "store_name": store.name if store else f"Магазин #{purchase.store_id}",
            "purchase_date": purchase.purchase_date.isoformat(),
            "amount": float(purchase.amount),
            "items_count": purchase.items_count,
            "discount_applied": float(purchase.discount_applied),
            "bonuses_used": float(purchase.bonuses_used),
            "bonuses_earned": float(purchase.bonuses_earned),
            "payment_method": purchase.payment_method,
            "receipt_number": purchase.receipt_number,
        }
        result.append(purchase_dict)
    
    return result


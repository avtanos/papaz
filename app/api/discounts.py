from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.discount import (
    DiscountRuleCreate, DiscountRuleUpdate, DiscountRuleResponse,
    DiscountCalculationRequest, DiscountCalculationResponse,
    DiscountApplicationResponse
)
from app.services.discount_service import DiscountService
from app.models.discount import DiscountRule

router = APIRouter()


@router.post("/rules", response_model=DiscountRuleResponse)
def create_discount_rule(rule: DiscountRuleCreate, db: Session = Depends(get_db)):
    return DiscountService.create_rule(db, rule.dict())


@router.get("/rules")
def list_discount_rules(
    store_id: int = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    from sqlalchemy import func
    
    query = db.query(DiscountRule)
    if store_id:
        query = query.filter(
            (DiscountRule.applicable_stores.contains([store_id])) | 
            (DiscountRule.applicable_stores == None)
        )
    
    total = query.count()
    rules = query.offset(skip).limit(limit).all()
    
    return {
        "items": rules,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/rules/{rule_id}", response_model=DiscountRuleResponse)
def get_discount_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(DiscountRule).filter(DiscountRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Правило скидки не найдено")
    return rule


@router.put("/rules/{rule_id}", response_model=DiscountRuleResponse)
def update_discount_rule(rule_id: int, rule: DiscountRuleUpdate, db: Session = Depends(get_db)):
    db_rule = db.query(DiscountRule).filter(DiscountRule.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Правило скидки не найдено")
    
    update_data = rule.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_rule, key, value)
    
    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.post("/calculate", response_model=DiscountCalculationResponse)
def calculate_discounts(request: DiscountCalculationRequest, db: Session = Depends(get_db)):
    try:
        return DiscountService.calculate_discounts(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/applications", response_model=List[DiscountApplicationResponse])
def list_discount_applications(customer_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    from app.models.discount import DiscountApplication
    query = db.query(DiscountApplication)
    if customer_id:
        query = query.filter(DiscountApplication.customer_id == customer_id)
    return query.order_by(DiscountApplication.applied_at.desc()).offset(skip).limit(limit).all()


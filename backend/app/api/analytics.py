from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_active_cashier
from app.schemas.analytics import AnalyticsRequest, AnalyticsResponse, CustomerSegmentResponse
from app.services.analytics_service import AnalyticsService
from app.models.cashier import Cashier
from datetime import datetime, timedelta
from typing import List

router = APIRouter()


@router.post("/", response_model=AnalyticsResponse)
def get_analytics(
    request: AnalyticsRequest,
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """Аналитика (для супер-админа - все магазины, для кассира - только его магазин)"""
    # Если не супер-админ, ограничиваем аналитику магазином кассира
    if not current_cashier.is_superuser:
        if request.store_ids is None:
            request.store_ids = [current_cashier.store_id]
        elif current_cashier.store_id not in request.store_ids:
            request.store_ids = [current_cashier.store_id]
    
    return AnalyticsService.get_analytics(db, request)


@router.get("/segments", response_model=List[CustomerSegmentResponse])
def get_customer_segments(customer_id: int = None, db: Session = Depends(get_db)):
    from app.models.analytics import CustomerSegment
    query = db.query(CustomerSegment)
    if customer_id:
        query = query.filter(CustomerSegment.customer_id == customer_id)
    return query.all()


@router.post("/segments/update")
def update_segments(db: Session = Depends(get_db)):
    """Обновить сегментацию всех клиентов"""
    AnalyticsService.segment_customers(db)
    return {"message": "Сегментация обновлена"}


@router.get("/summary")
def get_summary(
    days: int = 30,
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """Краткая сводка за последние N дней (для супер-админа - все магазины, для кассира - только его магазин)"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    request = AnalyticsRequest(
        start_date=start_date,
        end_date=end_date,
        store_ids=None if current_cashier.is_superuser else [current_cashier.store_id]
    )
    return AnalyticsService.get_analytics(db, request)


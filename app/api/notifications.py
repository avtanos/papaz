from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.services.notification_service import NotificationService
from app.models.notification import Notification

router = APIRouter()


@router.post("/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    return NotificationService.create_notification(db, notification)


@router.post("/{notification_id}/send")
def send_notification(notification_id: int, db: Session = Depends(get_db)):
    NotificationService.send_notification(db, notification_id)
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    return {"message": "Уведомление отправлено", "status": notification.status}


@router.get("/", response_model=List[NotificationResponse])
def list_notifications(customer_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(Notification)
    if customer_id:
        query = query.filter(Notification.customer_id == customer_id)
    return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    return notification


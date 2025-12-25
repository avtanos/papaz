from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationBase(BaseModel):
    customer_id: Optional[int] = None
    notification_type: str
    subject: Optional[str] = None
    message: str
    extra_data: Optional[str] = None


class NotificationCreate(NotificationBase):
    pass


class NotificationResponse(NotificationBase):
    id: int
    status: str
    sent_at: Optional[datetime]
    created_at: datetime
    error_message: Optional[str]

    class Config:
        from_attributes = True


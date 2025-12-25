from sqlalchemy.orm import Session
from datetime import datetime
from app.models.notification import Notification, NotificationType, NotificationStatus
from app.models.customer import Customer
from app.schemas.notification import NotificationCreate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class NotificationService:
    @staticmethod
    def create_notification(db: Session, notification_data: NotificationCreate) -> Notification:
        notification = Notification(**notification_data.dict())
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def send_notification(db: Session, notification_id: int):
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return
        
        try:
            if notification.notification_type == NotificationType.EMAIL:
                NotificationService._send_email(notification)
            elif notification.notification_type == NotificationType.SMS:
                NotificationService._send_sms(notification)
            elif notification.notification_type == NotificationType.PUSH:
                NotificationService._send_push(notification)
            
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.now()
        except Exception as e:
            notification.status = NotificationStatus.FAILED
            notification.error_message = str(e)
        
        db.commit()

    @staticmethod
    def _send_email(notification: Notification):
        # Заглушка для отправки email
        # В реальном проекте здесь будет интеграция с SMTP
        customer = None
        if notification.customer_id:
            # Получаем email клиента из БД
            pass
        
        # Пример отправки через SMTP
        # msg = MIMEMultipart()
        # msg['From'] = settings.SMTP_USER
        # msg['To'] = customer.email
        # msg['Subject'] = notification.subject
        # msg.attach(MIMEText(notification.message, 'plain'))
        # 
        # server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        # server.starttls()
        # server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        # server.send_message(msg)
        # server.quit()
        pass

    @staticmethod
    def _send_sms(notification: Notification):
        # Заглушка для отправки SMS
        # В реальном проекте здесь будет интеграция с SMS провайдером
        pass

    @staticmethod
    def _send_push(notification: Notification):
        # Заглушка для отправки Push уведомлений
        # В реальном проекте здесь будет интеграция с FCM
        pass

    @staticmethod
    def send_bonus_notification(db: Session, customer_id: int, bonus_amount: float):
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return
        
        notification = Notification(
            customer_id=customer_id,
            notification_type=NotificationType.SMS,
            subject="Начислены бонусы",
            message=f"Вам начислено {bonus_amount} бонусных баллов! Спасибо за покупку!"
        )
        db.add(notification)
        db.commit()
        
        # Отправляем асинхронно
        NotificationService.send_notification(db, notification.id)


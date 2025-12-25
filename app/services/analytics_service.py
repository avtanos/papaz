from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, List
from app.models.customer import Customer, PurchaseHistory
from app.models.bonus import BonusTransaction, BonusTransactionType
from app.models.discount import DiscountApplication
from app.models.analytics import CustomerSegment
from app.schemas.analytics import AnalyticsRequest, AnalyticsResponse


class AnalyticsService:
    @staticmethod
    def segment_customers(db: Session):
        """Автоматическая сегментация клиентов"""
        customers = db.query(Customer).all()
        
        for customer in customers:
            # Удаляем старые сегменты
            db.query(CustomerSegment).filter(CustomerSegment.customer_id == customer.id).delete()
            
            # Определяем сегмент
            segment_name = AnalyticsService._determine_segment(customer)
            
            segment = CustomerSegment(
                customer_id=customer.id,
                segment_name=segment_name,
                criteria={
                    "total_visits": customer.total_visits,
                    "total_purchases": float(customer.total_purchases),
                    "last_visit": customer.last_visit.isoformat() if customer.last_visit else None
                }
            )
            db.add(segment)
        
        db.commit()

    @staticmethod
    def _determine_segment(customer: Customer) -> str:
        if customer.total_visits == 0:
            return "new"
        elif customer.total_visits == 1:
            return "one_time"
        elif customer.total_visits >= 10 and customer.total_purchases >= Decimal("10000"):
            return "vip"
        elif customer.total_visits >= 5:
            return "regular"
        else:
            return "occasional"

    @staticmethod
    def get_analytics(db: Session, request: AnalyticsRequest) -> AnalyticsResponse:
        # Базовые фильтры
        purchase_query = db.query(PurchaseHistory).filter(
            and_(
                PurchaseHistory.purchase_date >= request.start_date,
                PurchaseHistory.purchase_date <= request.end_date
            )
        )
        
        if request.store_ids:
            purchase_query = purchase_query.filter(PurchaseHistory.store_id.in_(request.store_ids))
        
        purchases = purchase_query.all()
        
        # Статистика
        total_revenue = sum(p.amount for p in purchases)
        total_discounts = sum(p.discount_applied for p in purchases)
        
        # Бонусы
        bonus_earned = db.query(func.sum(BonusTransaction.amount)).filter(
            and_(
                BonusTransaction.transaction_type == BonusTransactionType.EARNED,
                BonusTransaction.transaction_date >= request.start_date,
                BonusTransaction.transaction_date <= request.end_date
            )
        ).scalar() or Decimal("0")
        
        bonus_spent = db.query(func.sum(BonusTransaction.amount)).filter(
            and_(
                BonusTransaction.transaction_type == BonusTransactionType.SPENT,
                BonusTransaction.transaction_date >= request.start_date,
                BonusTransaction.transaction_date <= request.end_date
            )
        ).scalar() or Decimal("0")
        
        # Клиенты
        customer_ids = list(set(p.customer_id for p in purchases))
        customer_count = len(customer_ids)
        average_purchase = total_revenue / len(purchases) if purchases else Decimal("0")
        
        # Сегментация
        segment_stats = {}
        if request.segment_names:
            for segment_name in request.segment_names:
                segment_customers = db.query(CustomerSegment).filter(
                    CustomerSegment.segment_name == segment_name
                ).all()
                segment_customer_ids = [s.customer_id for s in segment_customers]
                segment_purchases = [p for p in purchases if p.customer_id in segment_customer_ids]
                segment_stats[segment_name] = {
                    "customer_count": len(segment_customer_ids),
                    "total_revenue": sum(p.amount for p in segment_purchases),
                    "average_purchase": sum(p.amount for p in segment_purchases) / len(segment_purchases) if segment_purchases else 0
                }
        
        # Эффективность скидок
        discount_applications = db.query(DiscountApplication).filter(
            and_(
                DiscountApplication.applied_at >= request.start_date,
                DiscountApplication.applied_at <= request.end_date
            )
        ).all()
        
        discount_effectiveness = []
        discount_groups = {}
        for app in discount_applications:
            rule_id = app.discount_rule_id
            if rule_id not in discount_groups:
                discount_groups[rule_id] = {
                    "rule_id": rule_id,
                    "applications_count": 0,
                    "total_discount": Decimal("0"),
                    "total_revenue": Decimal("0")
                }
            discount_groups[rule_id]["applications_count"] += 1
            discount_groups[rule_id]["total_discount"] += app.discount_amount
            discount_groups[rule_id]["total_revenue"] += app.final_amount
        
        discount_effectiveness = list(discount_groups.values())
        
        return AnalyticsResponse(
            total_revenue=total_revenue,
            total_discounts=total_discounts,
            total_bonuses_issued=bonus_earned,
            total_bonuses_spent=bonus_spent,
            customer_count=customer_count,
            average_purchase=average_purchase,
            segment_statistics=segment_stats,
            discount_effectiveness=discount_effectiveness
        )


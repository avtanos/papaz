from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any
from app.models.discount import DiscountRule, DiscountApplication, DiscountType, DiscountRuleStatus
from app.models.customer import Customer, CustomerStatus
from app.schemas.discount import DiscountCalculationRequest, DiscountCalculationResponse
from app.services.bonus_service import BonusService


class DiscountService:
    @staticmethod
    def create_rule(db: Session, rule_data: dict) -> DiscountRule:
        rule = DiscountRule(**rule_data)
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule

    @staticmethod
    def get_active_rules(db: Session, store_id: int = None) -> List[DiscountRule]:
        query = db.query(DiscountRule).filter(DiscountRule.status == DiscountRuleStatus.ACTIVE)
        
        now = datetime.now()
        query = query.filter(
            or_(
                DiscountRule.valid_from.is_(None),
                DiscountRule.valid_from <= now
            )
        ).filter(
            or_(
                DiscountRule.valid_until.is_(None),
                DiscountRule.valid_until >= now
            )
        )
        
        if store_id:
            query = query.filter(
                or_(
                    DiscountRule.applicable_stores.is_(None),
                    DiscountRule.applicable_stores.contains([store_id])
                )
            )
        
        return query.all()

    @staticmethod
    def calculate_discounts(
        db: Session,
        request: DiscountCalculationRequest
    ) -> DiscountCalculationResponse:
        customer = db.query(Customer).filter(Customer.id == request.customer_id).first()
        if not customer:
            raise ValueError("Клиент не найден")
        
        active_rules = DiscountService.get_active_rules(db, request.store_id)
        applicable_discounts = []
        total_discount = Decimal("0")
        
        for rule in active_rules:
            if not DiscountService._is_rule_applicable(db, rule, customer, request):
                continue
            
            discount_amount = DiscountService._calculate_discount_amount(rule, request.amount)
            if discount_amount > 0:
                applicable_discounts.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "discount_type": rule.discount_type,
                    "discount_amount": float(discount_amount)
                })
                total_discount += discount_amount
        
        # Ограничение максимальной скидки
        final_amount = request.amount - total_discount
        if final_amount < 0:
            final_amount = Decimal("0")
            total_discount = request.amount
        
        # Расчёт бонусов
        bonuses_earned = BonusService.calculate_bonuses(final_amount)
        
        return DiscountCalculationResponse(
            applicable_discounts=applicable_discounts,
            total_discount=total_discount,
            final_amount=final_amount,
            bonuses_earned=bonuses_earned
        )

    @staticmethod
    def _is_rule_applicable(db: Session, rule: DiscountRule, customer: Customer, request: DiscountCalculationRequest) -> bool:
        # Проверка минимальной суммы покупки
        if rule.min_purchase_amount and request.amount < rule.min_purchase_amount:
            return False
        
        # Проверка для новых клиентов
        if rule.is_new_customer_only and customer.total_visits > 1:
            return False
        
        # Проверка минимального количества визитов
        if rule.min_visits_required and customer.total_visits < rule.min_visits_required:
            return False
        
        # Проверка максимального использования на клиента
        if rule.max_uses_per_customer:
            uses_count = db.query(DiscountApplication).filter(
                and_(
                    DiscountApplication.discount_rule_id == rule.id,
                    DiscountApplication.customer_id == customer.id
                )
            ).count()
            if uses_count >= rule.max_uses_per_customer:
                return False
        
        # Проверка максимального общего использования
        if rule.max_total_uses and rule.current_uses >= rule.max_total_uses:
            return False
        
        return True

    @staticmethod
    def _calculate_discount_amount(rule: DiscountRule, purchase_amount: Decimal) -> Decimal:
        if rule.discount_type == DiscountType.PERCENTAGE:
            discount = purchase_amount * (rule.value / Decimal("100"))
        elif rule.discount_type == DiscountType.FIXED_AMOUNT:
            discount = rule.value
        else:
            discount = Decimal("0")
        
        # Ограничение максимальной скидки
        if rule.max_discount_amount and discount > rule.max_discount_amount:
            discount = rule.max_discount_amount
        
        # Скидка не может быть больше суммы покупки
        if discount > purchase_amount:
            discount = purchase_amount
        
        return discount.quantize(Decimal("0.01"))

    @staticmethod
    def apply_discount(
        db: Session,
        discount_rule_id: int,
        purchase_id: int,
        customer_id: int,
        original_amount: Decimal,
        discount_amount: Decimal
    ) -> DiscountApplication:
        application = DiscountApplication(
            discount_rule_id=discount_rule_id,
            purchase_id=purchase_id,
            customer_id=customer_id,
            original_amount=original_amount,
            discount_amount=discount_amount,
            final_amount=original_amount - discount_amount
        )
        
        # Обновляем счётчик использования
        rule = db.query(DiscountRule).filter(DiscountRule.id == discount_rule_id).first()
        if rule:
            rule.current_uses += 1
        
        db.add(application)
        db.commit()
        db.refresh(application)
        return application


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from app.core.database import get_db
from app.core.dependencies import get_current_active_cashier
from app.schemas.customer import PurchaseCreate, PurchaseResponse
from app.services.customer_service import CustomerService
from app.services.discount_service import DiscountService
from app.services.bonus_service import BonusService
from app.services.notification_service import NotificationService
from app.schemas.discount import DiscountCalculationRequest
from app.models.cashier import Cashier

router = APIRouter()


@router.post("/process-purchase", response_model=PurchaseResponse)
def process_purchase(
    customer_id: int,
    store_id: int,
    amount: Decimal,
    items_count: int = 0,
    bonuses_to_use: Decimal = Decimal("0"),
    payment_method: str = None,
    receipt_number: str = None,
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """
    Обработка покупки через кассу (POS)
    Интегрирует все модули: скидки, бонусы, уведомления
    """
    # Проверяем, что кассир обрабатывает покупку в своем магазине (кроме супер-админа)
    if not current_cashier.is_superuser and store_id != current_cashier.store_id:
        raise HTTPException(
            status_code=403,
            detail="You can only process purchases for your store"
        )
    
    # 1. Рассчитываем скидки
    discount_request = DiscountCalculationRequest(
        customer_id=customer_id,
        store_id=store_id,
        amount=amount
    )
    discount_result = DiscountService.calculate_discounts(db, discount_request)
    
    # 2. Применяем бонусы (если указаны)
    final_amount = discount_result.final_amount
    bonuses_used = Decimal("0")
    
    if bonuses_to_use > 0:
        try:
            BonusService.spend_bonuses(
                db, customer_id, bonuses_to_use,
                description=f"Использовано при покупке на сумму {amount}",
                purchase_id=None  # будет обновлено после создания покупки
            )
            bonuses_used = bonuses_to_use
            final_amount = max(Decimal("0"), final_amount - bonuses_to_use)
        except ValueError as e:
            # Если не хватает бонусов, продолжаем без них
            pass
    
    # 3. Создаём запись о покупке (с оригинальной суммой для истории)
    purchase_data = PurchaseCreate(
        customer_id=customer_id,
        store_id=store_id,
        amount=amount,  # Оригинальная сумма
        items_count=items_count,
        payment_method=payment_method,
        receipt_number=receipt_number
    )
    purchase = CustomerService.create_purchase(db, purchase_data)
    
    # 4. Обновляем поля скидок и бонусов в покупке
    purchase.discount_applied = discount_result.total_discount
    purchase.bonuses_used = bonuses_used
    purchase.bonuses_earned = discount_result.bonuses_earned
    # Обновляем итоговую сумму с учётом скидок и бонусов
    purchase.amount = final_amount
    # Сохраняем изменения в покупке
    db.flush()  # Сохраняем изменения без commit (commit будет в конце)
    
    # 5. Применяем скидки (создаём записи DiscountApplication)
    for discount_info in discount_result.applicable_discounts:
        DiscountService.apply_discount(
            db,
            discount_info["rule_id"],
            purchase.id,
            customer_id,
            amount,
            Decimal(str(discount_info["discount_amount"]))
        )
    
    # 6. Начисляем бонусы
    if discount_result.bonuses_earned > 0:
        BonusService.add_bonuses(
            db, customer_id, discount_result.bonuses_earned,
            description=f"Начислено за покупку #{purchase.id}",
            purchase_id=purchase.id
        )
    
    # 7. Отправляем уведомление о начислении бонусов
    if discount_result.bonuses_earned > 0:
        NotificationService.send_bonus_notification(
            db, customer_id, float(discount_result.bonuses_earned)
        )
    
    db.commit()
    db.refresh(purchase)
    
    return purchase


@router.get("/customer/{customer_id}/available-discounts")
def get_available_discounts(
    customer_id: int,
    store_id: int,
    amount: Decimal,
    db: Session = Depends(get_db),
    current_cashier: Cashier = Depends(get_current_active_cashier)
):
    """Получить доступные скидки для клиента"""
    # Проверяем, что кассир запрашивает скидки для своего магазина (кроме супер-админа)
    if not current_cashier.is_superuser and store_id != current_cashier.store_id:
        raise HTTPException(
            status_code=403,
            detail="You can only view discounts for your store"
        )
    
    request = DiscountCalculationRequest(
        customer_id=customer_id,
        store_id=store_id,
        amount=amount
    )
    return DiscountService.calculate_discounts(db, request)


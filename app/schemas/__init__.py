from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, PurchaseCreate, PurchaseResponse
from app.schemas.bonus import BonusBalanceResponse, BonusTransactionResponse, BonusTransactionCreate
from app.schemas.discount import DiscountRuleCreate, DiscountRuleUpdate, DiscountRuleResponse, DiscountApplicationResponse
from app.schemas.store import StoreCreate, StoreResponse
from app.schemas.analytics import CustomerSegmentResponse, CampaignCreate, CampaignResponse
from app.schemas.notification import NotificationCreate, NotificationResponse

__all__ = [
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "PurchaseCreate",
    "PurchaseResponse",
    "BonusBalanceResponse",
    "BonusTransactionResponse",
    "BonusTransactionCreate",
    "DiscountRuleCreate",
    "DiscountRuleUpdate",
    "DiscountRuleResponse",
    "DiscountApplicationResponse",
    "StoreCreate",
    "StoreResponse",
    "CustomerSegmentResponse",
    "CampaignCreate",
    "CampaignResponse",
    "NotificationCreate",
    "NotificationResponse",
]


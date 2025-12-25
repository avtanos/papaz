from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any


class CustomerSegmentResponse(BaseModel):
    id: int
    customer_id: int
    segment_name: str
    assigned_at: datetime
    criteria: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    discount_rule_id: Optional[int] = None
    start_date: datetime
    end_date: datetime
    target_segments: Optional[List[str]] = None
    total_budget: Optional[Decimal] = None


class CampaignCreate(CampaignBase):
    pass


class CampaignResponse(CampaignBase):
    id: int
    spent_budget: Decimal
    total_reach: int
    conversions: int
    created_at: datetime
    status: str

    class Config:
        from_attributes = True


class AnalyticsRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    store_ids: Optional[List[int]] = None
    segment_names: Optional[List[str]] = None


class AnalyticsResponse(BaseModel):
    total_revenue: Decimal
    total_discounts: Decimal
    total_bonuses_issued: Decimal
    total_bonuses_spent: Decimal
    customer_count: int
    average_purchase: Decimal
    segment_statistics: Dict[str, Any]
    discount_effectiveness: List[Dict[str, Any]]


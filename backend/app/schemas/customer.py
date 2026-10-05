from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CustomerBase(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    country: str
    occupation: Optional[str] = None
    account_type: str = "Savings"
    kyc_status: str = "Verified"
    baseline_avg_amount: float = 25000.0
    baseline_monthly_volume: float = 150000.0
    risk_score: int = 15
    risk_level: str = "LOW"
    is_pep: bool = False

class CustomerResponse(CustomerBase):
    customer_id: str
    account_opened_date: datetime
    created_at: datetime
    transaction_count: Optional[int] = 0
    flagged_transaction_count: Optional[int] = 0
    total_volume: Optional[float] = 0.0

    class Config:
        from_attributes = True

class CustomerTimelineEvent(BaseModel):
    event_id: str
    timestamp: datetime
    event_type: str # Transaction, Alert, Status Change, Investigation
    title: str
    description: str
    severity: str
    reference_id: Optional[str] = None

class CustomerDetailResponse(CustomerResponse):
    timeline: List[CustomerTimelineEvent] = []
    recent_transactions: List[dict] = []
    alerts: List[dict] = []
    investigations: List[dict] = []

    class Config:
        from_attributes = True

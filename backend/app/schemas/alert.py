from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    transaction_id: str
    customer_id: str
    alert_type: str
    severity: str
    status: str = "New"
    risk_score: int
    details: Optional[str] = None

class AlertResponse(AlertBase):
    alert_id: str
    created_at: datetime
    customer_name: Optional[str] = None
    transaction_amount: Optional[float] = None
    destination_country: Optional[str] = None

    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    status: str

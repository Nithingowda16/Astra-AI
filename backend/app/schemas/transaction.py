from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from backend.app.schemas.rule_evaluation import RuleEvaluationResponse

class TransactionBase(BaseModel):
    customer_id: str
    amount: float
    currency: str = "INR"
    source_country: str = "India"
    destination_country: str
    transaction_type: str
    merchant_category: Optional[str] = None
    status: str = "Completed"

class TransactionCreate(TransactionBase):
    transaction_id: str
    timestamp: Optional[datetime] = None

class TransactionResponse(TransactionBase):
    transaction_id: str
    timestamp: datetime
    risk_score: int
    risk_level: str
    is_flagged: bool
    flagged_reason_summary: Optional[str] = None

    class Config:
        from_attributes = True

class TransactionDetailResponse(TransactionResponse):
    evaluations: List[RuleEvaluationResponse] = []
    customer_name: Optional[str] = None
    customer_risk_level: Optional[str] = None

    class Config:
        from_attributes = True

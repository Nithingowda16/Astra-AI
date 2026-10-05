from pydantic import BaseModel
from typing import Optional

class RuleEvaluationBase(BaseModel):
    rule_id: str
    rule_name: str
    score_contribution: int
    severity: str
    observed_value: Optional[str] = None
    threshold_value: Optional[str] = None
    explanation: str
    regulatory_ref: Optional[str] = None

class RuleEvaluationResponse(RuleEvaluationBase):
    evaluation_id: str
    transaction_id: str

    class Config:
        from_attributes = True

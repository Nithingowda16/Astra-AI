from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class InvestigationBase(BaseModel):
    title: str
    customer_id: str
    primary_transaction_id: Optional[str] = None
    status: str = "Open"
    priority: str = "High"
    assigned_analyst: str = "Senior Compliance Officer"
    summary: Optional[str] = None
    analyst_notes: Optional[str] = None
    findings: Optional[str] = None
    evidence_links: Optional[str] = None

class InvestigationCreate(InvestigationBase):
    pass

class InvestigationUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_analyst: Optional[str] = None
    summary: Optional[str] = None
    analyst_notes: Optional[str] = None
    findings: Optional[str] = None
    new_note: Optional[str] = None

class InvestigationResponse(InvestigationBase):
    investigation_id: str
    created_at: datetime
    updated_at: datetime
    customer_name: Optional[str] = None
    customer_risk_level: Optional[str] = None

    class Config:
        from_attributes = True

class InvestigationReport(BaseModel):
    report_id: str
    generated_at: datetime
    title: str
    investigation_id: str
    status: str
    priority: str
    assigned_analyst: str
    customer: dict
    primary_transaction: Optional[dict] = None
    related_transactions: List[dict] = []
    triggered_rules: List[dict] = []
    regulatory_citations: List[dict] = []
    findings: str
    notes_history: List[dict] = []
    compliance_recommendation: str
    disclaimer: str

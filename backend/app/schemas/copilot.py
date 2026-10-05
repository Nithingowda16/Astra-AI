from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class CopilotQueryRequest(BaseModel):
    query: str
    context_customer_id: Optional[str] = None
    context_transaction_id: Optional[str] = None

class CopilotEvidenceItem(BaseModel):
    source: str # e.g. "Demo AML Rule 04", "Transaction Record TXN-1024"
    doc_id: Optional[str] = None
    title: str
    excerpt: str
    authority: Optional[str] = None

class CopilotEntityItem(BaseModel):
    type: str # "transaction", "customer", "rule", "alert"
    id: str
    label: str
    details: Optional[Dict[str, Any]] = None

class CopilotQueryResponse(BaseModel):
    query: str
    answer: str
    data_found: bool = True
    entities: List[CopilotEntityItem] = []
    risk_indicators: List[str] = []
    supporting_evidence: List[CopilotEvidenceItem] = []
    suggested_actions: List[str] = []
    disclaimer: str = "Demo Regulatory Knowledge Base - Copilot Grounded in Synthesized Records"

from pydantic import BaseModel
from typing import Optional, List

class RegulatoryDocBase(BaseModel):
    title: str
    authority: str
    category: str
    summary: str
    full_clause: str
    monitored_scenarios: Optional[str] = None
    recommended_compliance_action: str
    disclaimer: str

class RegulatoryDocResponse(RegulatoryDocBase):
    doc_id: str

    class Config:
        from_attributes = True

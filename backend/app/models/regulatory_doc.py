from sqlalchemy import Column, String, Text
from backend.app.core.database import Base

class RegulatoryDoc(Base):
    __tablename__ = "regulatory_docs"

    doc_id = Column(String, primary_key=True, index=True) # e.g. "REG-AML-01"
    title = Column(String, nullable=False)
    authority = Column(String, default="Demo Financial Intelligence Unit")
    category = Column(String, nullable=False) # AML, High-Risk Jurisdictions, Structuring, Due Diligence, PEP
    summary = Column(Text, nullable=False)
    full_clause = Column(Text, nullable=False)
    monitored_scenarios = Column(Text, nullable=True) # JSON or structured bullet points
    recommended_compliance_action = Column(Text, nullable=False)
    disclaimer = Column(String, default="Demo Regulatory Knowledge Base - Simulated Compliance Guidance")

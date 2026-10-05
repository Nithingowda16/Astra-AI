from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from backend.app.core.database import Base

class Investigation(Base):
    __tablename__ = "investigations"

    investigation_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False, index=True)
    primary_transaction_id = Column(String, nullable=True)
    status = Column(String, default="Open") # Open, Under Review, Escalated, Resolved, False Positive
    priority = Column(String, default="High") # Low, Medium, High, Critical
    assigned_analyst = Column(String, default="Senior Compliance Officer")
    summary = Column(Text, nullable=True)
    analyst_notes = Column(Text, nullable=True) # JSON or markdown notes log
    findings = Column(Text, nullable=True) # Key findings
    evidence_links = Column(Text, nullable=True) # References to rules & txns
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="investigations")

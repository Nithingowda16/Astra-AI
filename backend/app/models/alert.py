from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from backend.app.core.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(String, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.transaction_id"), nullable=False, index=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False, index=True)
    alert_type = Column(String, nullable=False) # e.g. "Velocity Spike", "High Risk Corridor", "Smurfing Pattern"
    severity = Column(String, nullable=False, default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String, default="New") # New, Acknowledged, Investigating, Closed
    risk_score = Column(Integer, default=50)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    transaction = relationship("Transaction", back_populates="alerts")
    customer = relationship("Customer", back_populates="alerts")

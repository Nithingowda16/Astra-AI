from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from backend.app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    amount = Column(Float, nullable=False, index=True)
    currency = Column(String, default="INR")
    source_country = Column(String, default="India")
    destination_country = Column(String, nullable=False, index=True)
    transaction_type = Column(String, nullable=False) # Wire Transfer, Card, Crypto, ATM, International Transfer
    merchant_category = Column(String, nullable=True) # Luxury Goods, Casino, Real Estate, Offshore Holding, Utilities
    status = Column(String, default="Completed") # Completed, Flagged, Under Review, Blocked
    risk_score = Column(Integer, default=10, index=True)
    risk_level = Column(String, default="LOW", index=True) # LOW, MEDIUM, HIGH, CRITICAL
    is_flagged = Column(Boolean, default=False, index=True)
    flagged_reason_summary = Column(Text, nullable=True)

    customer = relationship("Customer", back_populates="transactions")
    evaluations = relationship("RuleEvaluation", back_populates="transaction", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="transaction")

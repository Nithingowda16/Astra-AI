from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
import datetime
from backend.app.core.database import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    country = Column(String, nullable=False)
    occupation = Column(String, nullable=True)
    account_type = Column(String, nullable=False, default="Savings") # Savings, Current, Corporate, Offshore
    account_opened_date = Column(DateTime, default=datetime.datetime.utcnow)
    kyc_status = Column(String, default="Verified") # Verified, Enhanced Due Diligence, Pending
    baseline_avg_amount = Column(Float, default=25000.0)
    baseline_monthly_volume = Column(Float, default=150000.0)
    risk_score = Column(Integer, default=15)
    risk_level = Column(String, default="LOW") # LOW, MEDIUM, HIGH, CRITICAL
    is_pep = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    transactions = relationship("Transaction", back_populates="customer", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="customer")
    investigations = relationship("Investigation", back_populates="customer")

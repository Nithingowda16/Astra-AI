from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class RuleEvaluation(Base):
    __tablename__ = "rule_evaluations"

    evaluation_id = Column(String, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.transaction_id"), nullable=False, index=True)
    rule_id = Column(String, nullable=False, index=True)
    rule_name = Column(String, nullable=False)
    score_contribution = Column(Integer, default=0)
    severity = Column(String, default="LOW") # LOW, MEDIUM, HIGH, CRITICAL
    observed_value = Column(String, nullable=True)
    threshold_value = Column(String, nullable=True)
    explanation = Column(Text, nullable=False)
    regulatory_ref = Column(String, nullable=True, index=True) # e.g. REG-AML-01

    transaction = relationship("Transaction", back_populates="evaluations")

from pydantic import BaseModel
from typing import List, Dict, Any
from backend.app.schemas.alert import AlertResponse

class RiskDistribution(BaseModel):
    low: int
    medium: int
    high: int
    critical: int

class TrendDataPoint(BaseModel):
    date: str
    total_volume: float
    total_count: int
    suspicious_count: int
    flagged_amount: float

class CountryRiskItem(BaseModel):
    country: str
    transaction_count: int
    high_risk_count: int
    total_volume: float

class DashboardStatsResponse(BaseModel):
    total_transactions: int
    suspicious_transactions: int
    suspicious_percentage: float
    high_risk_customers: int
    open_investigations: int
    total_monitored_volume: float
    currency: str = "INR"
    risk_distribution: RiskDistribution
    recent_alerts: List[AlertResponse]
    volume_trends: List[TrendDataPoint]
    country_risk_breakdown: List[CountryRiskItem]

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List

from backend.app.core.database import get_db
from backend.app.models.customer import Customer
from backend.app.models.transaction import Transaction
from backend.app.models.alert import Alert
from backend.app.models.investigation import Investigation
from backend.app.schemas.dashboard import DashboardStatsResponse, RiskDistribution, TrendDataPoint, CountryRiskItem
from backend.app.schemas.alert import AlertResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    # 1. Total counts
    total_txns = db.query(Transaction).count()
    suspicious_txns = db.query(Transaction).filter(Transaction.is_flagged == True).count()
    suspicious_pct = round((suspicious_txns / max(total_txns, 1)) * 100, 1)

    high_risk_customers = db.query(Customer).filter(
        (Customer.risk_level == "HIGH") | (Customer.risk_level == "CRITICAL")
    ).count()

    open_investigations = db.query(Investigation).filter(
        Investigation.status.in_(["Open", "Under Review", "Escalated"])
    ).count()

    total_monitored_volume = db.query(func.sum(Transaction.amount)).scalar() or 0.0

    # 2. Risk distribution
    low_count = db.query(Transaction).filter(Transaction.risk_level == "LOW").count()
    med_count = db.query(Transaction).filter(Transaction.risk_level == "MEDIUM").count()
    high_count = db.query(Transaction).filter(Transaction.risk_level == "HIGH").count()
    crit_count = db.query(Transaction).filter(Transaction.risk_level == "CRITICAL").count()

    risk_dist = RiskDistribution(
        low=low_count,
        medium=med_count,
        high=high_count,
        critical=crit_count
    )

    # 3. Recent priority alerts
    recent_alerts_db = db.query(Alert).order_by(Alert.created_at.desc()).limit(8).all()
    recent_alerts = []
    for a in recent_alerts_db:
        cust = db.query(Customer).filter(Customer.customer_id == a.customer_id).first()
        txn = db.query(Transaction).filter(Transaction.transaction_id == a.transaction_id).first()
        recent_alerts.append(AlertResponse(
            alert_id=a.alert_id,
            transaction_id=a.transaction_id,
            customer_id=a.customer_id,
            alert_type=a.alert_type,
            severity=a.severity,
            status=a.status,
            risk_score=a.risk_score,
            details=a.details,
            created_at=a.created_at,
            customer_name=cust.full_name if cust else "Unknown Customer",
            transaction_amount=txn.amount if txn else 0.0,
            destination_country=txn.destination_country if txn else "Unknown"
        ))

    # 4. Volume trends over time (group by day for last 14 days)
    now = datetime.utcnow()
    trends = []
    for day_offset in range(13, -1, -1):
        day_start = (now - timedelta(days=day_offset)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        day_label = day_start.strftime("%b %d")

        txns_in_day = db.query(Transaction).filter(
            Transaction.timestamp >= day_start,
            Transaction.timestamp < day_end
        ).all()

        day_total_vol = sum(t.amount for t in txns_in_day)
        day_total_count = len(txns_in_day)
        day_susp_count = sum(1 for t in txns_in_day if t.is_flagged)
        day_flagged_amt = sum(t.amount for t in txns_in_day if t.is_flagged)

        trends.append(TrendDataPoint(
            date=day_label,
            total_volume=round(day_total_vol, 2),
            total_count=day_total_count,
            suspicious_count=day_susp_count,
            flagged_amount=round(day_flagged_amt, 2)
        ))

    # 5. Country risk breakdown
    country_groups = db.query(
        Transaction.destination_country,
        func.count(Transaction.transaction_id).label("count"),
        func.sum(Transaction.amount).label("volume")
    ).group_by(Transaction.destination_country).order_by(func.count(Transaction.transaction_id).desc()).limit(6).all()

    country_breakdown = []
    for c_item in country_groups:
        c_name = c_item[0]
        c_count = c_item[1]
        c_vol = float(c_item[2] or 0.0)
        c_high_risk = db.query(Transaction).filter(
            Transaction.destination_country == c_name,
            Transaction.is_flagged == True
        ).count()

        country_breakdown.append(CountryRiskItem(
            country=c_name,
            transaction_count=c_count,
            high_risk_count=c_high_risk,
            total_volume=round(c_vol, 2)
        ))

    return DashboardStatsResponse(
        total_transactions=total_txns,
        suspicious_transactions=suspicious_txns,
        suspicious_percentage=suspicious_pct,
        high_risk_customers=high_risk_customers,
        open_investigations=open_investigations,
        total_monitored_volume=round(total_monitored_volume, 2),
        currency="INR",
        risk_distribution=risk_dist,
        recent_alerts=recent_alerts,
        volume_trends=trends,
        country_risk_breakdown=country_breakdown
    )

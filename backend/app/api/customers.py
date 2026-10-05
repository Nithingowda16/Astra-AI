from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from backend.app.core.database import get_db
from backend.app.models.customer import Customer
from backend.app.models.transaction import Transaction
from backend.app.models.alert import Alert
from backend.app.models.investigation import Investigation
from backend.app.schemas.customer import CustomerResponse, CustomerDetailResponse, CustomerTimelineEvent

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("", response_model=List[CustomerResponse])
def get_customers(
    search: Optional[str] = Query(None, description="Search by name, email, or customer ID"),
    risk_level: Optional[str] = Query(None, description="Filter by LOW, MEDIUM, HIGH, CRITICAL"),
    db: Session = Depends(get_db)
):
    query = db.query(Customer)
    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(
            (Customer.customer_id.ilike(search_fmt)) |
            (Customer.full_name.ilike(search_fmt)) |
            (Customer.email.ilike(search_fmt)) |
            (Customer.occupation.ilike(search_fmt))
        )
    if risk_level:
        query = query.filter(Customer.risk_level == risk_level.upper())

    customers = query.order_by(Customer.risk_score.desc()).all()
    results = []
    for c in customers:
        tx_count = db.query(Transaction).filter(Transaction.customer_id == c.customer_id).count()
        flagged_count = db.query(Transaction).filter(
            Transaction.customer_id == c.customer_id,
            Transaction.is_flagged == True
        ).count()
        total_vol = db.query(func.sum(Transaction.amount)).filter(
            Transaction.customer_id == c.customer_id
        ).scalar() or 0.0

        results.append(CustomerResponse(
            customer_id=c.customer_id,
            full_name=c.full_name,
            email=c.email,
            phone=c.phone,
            country=c.country,
            occupation=c.occupation,
            account_type=c.account_type,
            account_opened_date=c.account_opened_date,
            kyc_status=c.kyc_status,
            baseline_avg_amount=c.baseline_avg_amount,
            baseline_monthly_volume=c.baseline_monthly_volume,
            risk_score=c.risk_score,
            risk_level=c.risk_level,
            is_pep=c.is_pep,
            created_at=c.created_at,
            transaction_count=tx_count,
            flagged_transaction_count=flagged_count,
            total_volume=round(total_vol, 2)
        ))
    return results

@router.get("/{customer_id}", response_model=CustomerDetailResponse)
def get_customer_detail(customer_id: str, db: Session = Depends(get_db)):
    c = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found.")

    # Transactions
    txns = db.query(Transaction).filter(
        Transaction.customer_id == customer_id
    ).order_by(Transaction.timestamp.desc()).all()

    tx_count = len(txns)
    flagged_count = sum(1 for t in txns if t.is_flagged)
    total_vol = sum(t.amount for t in txns)

    # Alerts
    alerts = db.query(Alert).filter(Alert.customer_id == customer_id).order_by(Alert.created_at.desc()).all()

    # Investigations
    investigations = db.query(Investigation).filter(Investigation.customer_id == customer_id).order_by(Investigation.created_at.desc()).all()

    # Construct unified chronological timeline of suspicious and key events
    timeline_events: List[CustomerTimelineEvent] = []

    for a in alerts:
        timeline_events.append(CustomerTimelineEvent(
            event_id=a.alert_id,
            timestamp=a.created_at,
            event_type="Alert",
            title=f"Alert: {a.alert_type}",
            description=a.details or "Flagged by risk engine",
            severity=a.severity,
            reference_id=a.transaction_id
        ))

    for inv in investigations:
        timeline_events.append(CustomerTimelineEvent(
            event_id=inv.investigation_id,
            timestamp=inv.created_at,
            event_type="Investigation",
            title=f"Case Opened: {inv.title}",
            description=f"Assigned to {inv.assigned_analyst}. Status: {inv.status}",
            severity=inv.priority,
            reference_id=inv.investigation_id
        ))

    for t in txns:
        if t.is_flagged:
            timeline_events.append(CustomerTimelineEvent(
                event_id=t.transaction_id,
                timestamp=t.timestamp,
                event_type="Suspicious Transaction",
                title=f"Flagged Transfer: ₹{t.amount:,.2f} to {t.destination_country}",
                description=t.flagged_reason_summary or "Suspicious pattern detected",
                severity=t.risk_level,
                reference_id=t.transaction_id
            ))

    # Sort timeline in reverse chronological order
    timeline_events.sort(key=lambda x: x.timestamp, reverse=True)

    txn_dicts = [
        {
            "transaction_id": t.transaction_id,
            "timestamp": t.timestamp.isoformat(),
            "amount": t.amount,
            "currency": t.currency,
            "destination_country": t.destination_country,
            "transaction_type": t.transaction_type,
            "merchant_category": t.merchant_category,
            "status": t.status,
            "risk_score": t.risk_score,
            "risk_level": t.risk_level,
            "is_flagged": t.is_flagged,
            "flagged_reason_summary": t.flagged_reason_summary
        }
        for t in txns
    ]

    alert_dicts = [
        {
            "alert_id": a.alert_id,
            "transaction_id": a.transaction_id,
            "alert_type": a.alert_type,
            "severity": a.severity,
            "status": a.status,
            "risk_score": a.risk_score,
            "details": a.details,
            "created_at": a.created_at.isoformat()
        }
        for a in alerts
    ]

    inv_dicts = [
        {
            "investigation_id": inv.investigation_id,
            "title": inv.title,
            "status": inv.status,
            "priority": inv.priority,
            "assigned_analyst": inv.assigned_analyst,
            "summary": inv.summary,
            "created_at": inv.created_at.isoformat(),
            "updated_at": inv.updated_at.isoformat()
        }
        for inv in investigations
    ]

    return CustomerDetailResponse(
        customer_id=c.customer_id,
        full_name=c.full_name,
        email=c.email,
        phone=c.phone,
        country=c.country,
        occupation=c.occupation,
        account_type=c.account_type,
        account_opened_date=c.account_opened_date,
        kyc_status=c.kyc_status,
        baseline_avg_amount=c.baseline_avg_amount,
        baseline_monthly_volume=c.baseline_monthly_volume,
        risk_score=c.risk_score,
        risk_level=c.risk_level,
        is_pep=c.is_pep,
        created_at=c.created_at,
        transaction_count=tx_count,
        flagged_transaction_count=flagged_count,
        total_volume=round(total_vol, 2),
        timeline=timeline_events,
        recent_transactions=txn_dicts[:15],
        alerts=alert_dicts,
        investigations=inv_dicts
    )

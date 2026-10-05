from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.core.database import get_db
from backend.app.models.alert import Alert
from backend.app.models.transaction import Transaction
from backend.app.models.customer import Customer
from backend.app.schemas.alert import AlertResponse, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=List[AlertResponse])
def get_alerts(
    status: Optional[str] = Query(None, description="Filter by New, Acknowledged, Investigating, Closed"),
    severity: Optional[str] = Query(None, description="Filter by LOW, MEDIUM, HIGH, CRITICAL"),
    db: Session = Depends(get_db)
):
    query = db.query(Alert)
    if status:
        query = query.filter(Alert.status.ilike(status.strip()))
    if severity:
        query = query.filter(Alert.severity == severity.upper())

    alerts_db = query.order_by(Alert.created_at.desc()).all()
    results = []
    for a in alerts_db:
        cust = db.query(Customer).filter(Customer.customer_id == a.customer_id).first()
        txn = db.query(Transaction).filter(Transaction.transaction_id == a.transaction_id).first()
        results.append(AlertResponse(
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
    return results

@router.patch("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: str, update_data: AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found.")

    alert.status = update_data.status
    db.commit()
    db.refresh(alert)

    cust = db.query(Customer).filter(Customer.customer_id == alert.customer_id).first()
    txn = db.query(Transaction).filter(Transaction.transaction_id == alert.transaction_id).first()

    return AlertResponse(
        alert_id=alert.alert_id,
        transaction_id=alert.transaction_id,
        customer_id=alert.customer_id,
        alert_type=alert.alert_type,
        severity=alert.severity,
        status=alert.status,
        risk_score=alert.risk_score,
        details=alert.details,
        created_at=alert.created_at,
        customer_name=cust.full_name if cust else "Unknown",
        transaction_amount=txn.amount if txn else 0.0,
        destination_country=txn.destination_country if txn else "Unknown"
    )

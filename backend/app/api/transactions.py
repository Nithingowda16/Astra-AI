from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from typing import Optional, List
from datetime import datetime

from backend.app.core.database import get_db
from backend.app.models.transaction import Transaction
from backend.app.models.customer import Customer
from backend.app.models.rule_evaluation import RuleEvaluation
from backend.app.schemas.transaction import TransactionResponse, TransactionDetailResponse, TransactionBase
from backend.app.schemas.rule_evaluation import RuleEvaluationResponse
from backend.app.rules.risk_engine import RiskEngine

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("", response_model=List[TransactionResponse])
def get_transactions(
    search: Optional[str] = Query(None, description="Search by transaction ID, customer ID, or merchant"),
    risk_level: Optional[str] = Query(None, description="Filter by LOW, MEDIUM, HIGH, CRITICAL"),
    flagged_only: Optional[bool] = Query(None, description="Filter only flagged transactions"),
    min_amount: Optional[float] = Query(None, description="Minimum amount"),
    max_amount: Optional[float] = Query(None, description="Maximum amount"),
    destination_country: Optional[str] = Query(None, description="Filter by destination country"),
    sort_by: Optional[str] = Query("timestamp", description="Sort by timestamp, amount, or risk_score"),
    sort_order: Optional[str] = Query("desc", description="asc or desc"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)

    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Transaction.transaction_id.ilike(search_fmt),
                Transaction.customer_id.ilike(search_fmt),
                Transaction.merchant_category.ilike(search_fmt),
                Transaction.destination_country.ilike(search_fmt)
            )
        )

    if risk_level:
        query = query.filter(Transaction.risk_level == risk_level.upper())

    if flagged_only is not None:
        query = query.filter(Transaction.is_flagged == flagged_only)

    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)

    if destination_country:
        query = query.filter(Transaction.destination_country.ilike(f"%{destination_country.strip()}%"))

    # Sorting
    sort_column = Transaction.timestamp
    if sort_by == "amount":
        sort_column = Transaction.amount
    elif sort_by == "risk_score":
        sort_column = Transaction.risk_score

    if sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    return query.offset(skip).limit(limit).all()

@router.get("/{transaction_id}", response_model=TransactionDetailResponse)
def get_transaction_detail(transaction_id: str, db: Session = Depends(get_db)):
    txn = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} not found.")

    cust = db.query(Customer).filter(Customer.customer_id == txn.customer_id).first()
    evaluations_db = db.query(RuleEvaluation).filter(RuleEvaluation.transaction_id == transaction_id).all()

    eval_responses = [
        RuleEvaluationResponse(
            evaluation_id=e.evaluation_id,
            transaction_id=e.transaction_id,
            rule_id=e.rule_id,
            rule_name=e.rule_name,
            score_contribution=e.score_contribution,
            severity=e.severity,
            observed_value=e.observed_value,
            threshold_value=e.threshold_value,
            explanation=e.explanation,
            regulatory_ref=e.regulatory_ref
        )
        for e in evaluations_db
    ]

    return TransactionDetailResponse(
        transaction_id=txn.transaction_id,
        customer_id=txn.customer_id,
        timestamp=txn.timestamp,
        amount=txn.amount,
        currency=txn.currency,
        source_country=txn.source_country,
        destination_country=txn.destination_country,
        transaction_type=txn.transaction_type,
        merchant_category=txn.merchant_category,
        status=txn.status,
        risk_score=txn.risk_score,
        risk_level=txn.risk_level,
        is_flagged=txn.is_flagged,
        flagged_reason_summary=txn.flagged_reason_summary,
        evaluations=eval_responses,
        customer_name=cust.full_name if cust else "Unknown Customer",
        customer_risk_level=cust.risk_level if cust else "LOW"
    )

@router.post("/evaluate")
def evaluate_custom_transaction(txn_data: TransactionBase, db: Session = Depends(get_db)):
    """
    Live test endpoint: run any proposed transaction through the Explainable Risk Engine
    """
    cust = db.query(Customer).filter(Customer.customer_id == txn_data.customer_id).first()
    cust_dict = {
        "baseline_avg_amount": cust.baseline_avg_amount if cust else 25000.0,
        "is_pep": cust.is_pep if cust else False,
        "account_type": cust.account_type if cust else "Savings"
    }

    # Fetch recent transactions
    recent_db = db.query(Transaction).filter(
        Transaction.customer_id == txn_data.customer_id
    ).order_by(Transaction.timestamp.desc()).limit(10).all()

    recent_list = [
        {
            "transaction_id": t.transaction_id,
            "timestamp": t.timestamp,
            "amount": t.amount
        }
        for t in recent_db
    ]

    score, level, flagged, summary, rule_results = RiskEngine.evaluate_transaction(
        transaction_dict=txn_data.dict(),
        customer_dict=cust_dict,
        recent_customer_transactions=recent_list
    )

    return {
        "risk_score": score,
        "risk_level": level,
        "is_flagged": flagged,
        "summary": summary,
        "triggered_rules": [r.to_dict() for r in rule_results]
    }

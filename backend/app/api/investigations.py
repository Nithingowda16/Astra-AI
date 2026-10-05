from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from backend.app.core.database import get_db
from backend.app.models.investigation import Investigation
from backend.app.models.customer import Customer
from backend.app.models.transaction import Transaction
from backend.app.models.rule_evaluation import RuleEvaluation
from backend.app.regulatory.demo_knowledge_base import get_regulatory_rule_by_id
from backend.app.schemas.investigation import (
    InvestigationResponse,
    InvestigationCreate,
    InvestigationUpdate,
    InvestigationReport
)

router = APIRouter(prefix="/investigations", tags=["Investigations"])

@router.get("", response_model=List[InvestigationResponse])
def get_investigations(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    db: Session = Depends(get_db)
):
    query = db.query(Investigation)
    if status:
        query = query.filter(Investigation.status.ilike(status.strip()))
    if priority:
        query = query.filter(Investigation.priority.ilike(priority.strip()))

    invs = query.order_by(Investigation.updated_at.desc()).all()
    results = []
    for inv in invs:
        cust = db.query(Customer).filter(Customer.customer_id == inv.customer_id).first()
        results.append(InvestigationResponse(
            investigation_id=inv.investigation_id,
            title=inv.title,
            customer_id=inv.customer_id,
            primary_transaction_id=inv.primary_transaction_id,
            status=inv.status,
            priority=inv.priority,
            assigned_analyst=inv.assigned_analyst,
            summary=inv.summary,
            analyst_notes=inv.analyst_notes,
            findings=inv.findings,
            evidence_links=inv.evidence_links,
            created_at=inv.created_at,
            updated_at=inv.updated_at,
            customer_name=cust.full_name if cust else "Unknown Customer",
            customer_risk_level=cust.risk_level if cust else "LOW"
        ))
    return results

@router.post("", response_model=InvestigationResponse)
def create_investigation(data: InvestigationCreate, db: Session = Depends(get_db)):
    cust = db.query(Customer).filter(Customer.customer_id == data.customer_id).first()
    if not cust:
        raise HTTPException(status_code=404, detail=f"Customer {data.customer_id} does not exist.")

    inv_id = f"INV-2024-{uuid.uuid4().hex[:6].upper()}"
    now = datetime.utcnow()

    notes_init = f"• {now.strftime('%Y-%m-%d %H:%M')} - Case opened by {data.assigned_analyst}."
    if data.analyst_notes:
        notes_init += f"\n• Initial note: {data.analyst_notes}"

    inv = Investigation(
        investigation_id=inv_id,
        title=data.title,
        customer_id=data.customer_id,
        primary_transaction_id=data.primary_transaction_id,
        status=data.status or "Open",
        priority=data.priority or "High",
        assigned_analyst=data.assigned_analyst or "Senior Compliance Officer",
        summary=data.summary or f"Investigation into suspicious activity for {cust.full_name}.",
        analyst_notes=notes_init,
        findings=data.findings or "Under active evidence gathering and scrutiny.",
        evidence_links=data.evidence_links or data.primary_transaction_id or "",
        created_at=now,
        updated_at=now
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)

    return InvestigationResponse(
        investigation_id=inv.investigation_id,
        title=inv.title,
        customer_id=inv.customer_id,
        primary_transaction_id=inv.primary_transaction_id,
        status=inv.status,
        priority=inv.priority,
        assigned_analyst=inv.assigned_analyst,
        summary=inv.summary,
        analyst_notes=inv.analyst_notes,
        findings=inv.findings,
        evidence_links=inv.evidence_links,
        created_at=inv.created_at,
        updated_at=inv.updated_at,
        customer_name=cust.full_name,
        customer_risk_level=cust.risk_level
    )

@router.get("/{investigation_id}", response_model=InvestigationResponse)
def get_investigation_detail(investigation_id: str, db: Session = Depends(get_db)):
    inv = db.query(Investigation).filter(Investigation.investigation_id == investigation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail=f"Investigation {investigation_id} not found.")

    cust = db.query(Customer).filter(Customer.customer_id == inv.customer_id).first()
    return InvestigationResponse(
        investigation_id=inv.investigation_id,
        title=inv.title,
        customer_id=inv.customer_id,
        primary_transaction_id=inv.primary_transaction_id,
        status=inv.status,
        priority=inv.priority,
        assigned_analyst=inv.assigned_analyst,
        summary=inv.summary,
        analyst_notes=inv.analyst_notes,
        findings=inv.findings,
        evidence_links=inv.evidence_links,
        created_at=inv.created_at,
        updated_at=inv.updated_at,
        customer_name=cust.full_name if cust else "Unknown Customer",
        customer_risk_level=cust.risk_level if cust else "LOW"
    )

@router.patch("/{investigation_id}", response_model=InvestigationResponse)
def update_investigation(investigation_id: str, data: InvestigationUpdate, db: Session = Depends(get_db)):
    inv = db.query(Investigation).filter(Investigation.investigation_id == investigation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail=f"Investigation {investigation_id} not found.")

    now = datetime.utcnow()
    if data.status:
        inv.status = data.status
    if data.priority:
        inv.priority = data.priority
    if data.assigned_analyst:
        inv.assigned_analyst = data.assigned_analyst
    if data.summary:
        inv.summary = data.summary
    if data.findings:
        inv.findings = data.findings

    # Append new analyst note if supplied
    if data.new_note:
        timestamp_str = now.strftime('%Y-%m-%d %H:%M')
        new_entry = f"• {timestamp_str} [{inv.assigned_analyst}]: {data.new_note.strip()}"
        inv.analyst_notes = f"{inv.analyst_notes}\n{new_entry}" if inv.analyst_notes else new_entry

    inv.updated_at = now
    db.commit()
    db.refresh(inv)

    cust = db.query(Customer).filter(Customer.customer_id == inv.customer_id).first()
    return InvestigationResponse(
        investigation_id=inv.investigation_id,
        title=inv.title,
        customer_id=inv.customer_id,
        primary_transaction_id=inv.primary_transaction_id,
        status=inv.status,
        priority=inv.priority,
        assigned_analyst=inv.assigned_analyst,
        summary=inv.summary,
        analyst_notes=inv.analyst_notes,
        findings=inv.findings,
        evidence_links=inv.evidence_links,
        created_at=inv.created_at,
        updated_at=inv.updated_at,
        customer_name=cust.full_name if cust else "Unknown Customer",
        customer_risk_level=cust.risk_level if cust else "LOW"
    )

@router.get("/{investigation_id}/report", response_model=InvestigationReport)
def generate_investigation_report(investigation_id: str, db: Session = Depends(get_db)):
    inv = db.query(Investigation).filter(Investigation.investigation_id == investigation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail=f"Investigation {investigation_id} not found.")

    cust = db.query(Customer).filter(Customer.customer_id == inv.customer_id).first()
    customer_dict = {
        "customer_id": cust.customer_id if cust else "Unknown",
        "full_name": cust.full_name if cust else "Unknown",
        "email": cust.email if cust else "",
        "phone": cust.phone if cust else "",
        "country": cust.country if cust else "",
        "occupation": cust.occupation if cust else "",
        "account_type": cust.account_type if cust else "",
        "kyc_status": cust.kyc_status if cust else "",
        "baseline_avg_amount": cust.baseline_avg_amount if cust else 0.0,
        "baseline_monthly_volume": cust.baseline_monthly_volume if cust else 0.0,
        "risk_score": cust.risk_score if cust else 0,
        "risk_level": cust.risk_level if cust else "LOW",
        "is_pep": cust.is_pep if cust else False
    }

    # Primary transaction
    primary_txn_dict = None
    if inv.primary_transaction_id:
        ptxn = db.query(Transaction).filter(Transaction.transaction_id == inv.primary_transaction_id).first()
        if ptxn:
            primary_txn_dict = {
                "transaction_id": ptxn.transaction_id,
                "timestamp": ptxn.timestamp.isoformat(),
                "amount": ptxn.amount,
                "currency": ptxn.currency,
                "destination_country": ptxn.destination_country,
                "transaction_type": ptxn.transaction_type,
                "merchant_category": ptxn.merchant_category,
                "risk_score": ptxn.risk_score,
                "risk_level": ptxn.risk_level,
                "status": ptxn.status,
                "flagged_reason_summary": ptxn.flagged_reason_summary
            }

    # Related flagged transactions
    flagged_txns = db.query(Transaction).filter(
        Transaction.customer_id == inv.customer_id,
        Transaction.is_flagged == True
    ).order_by(Transaction.timestamp.desc()).all()

    related_txns = [
        {
            "transaction_id": t.transaction_id,
            "timestamp": t.timestamp.isoformat(),
            "amount": t.amount,
            "currency": t.currency,
            "destination_country": t.destination_country,
            "transaction_type": t.transaction_type,
            "risk_score": t.risk_score,
            "risk_level": t.risk_level,
            "status": t.status
        }
        for t in flagged_txns
    ]

    # Gather triggered rules across flagged transactions
    triggered_rules = []
    reg_citation_ids = set()
    for t in flagged_txns:
        evals = db.query(RuleEvaluation).filter(RuleEvaluation.transaction_id == t.transaction_id).all()
        for ev in evals:
            triggered_rules.append({
                "rule_id": ev.rule_id,
                "rule_name": ev.rule_name,
                "transaction_id": ev.transaction_id,
                "severity": ev.severity,
                "observed_value": ev.observed_value,
                "threshold_value": ev.threshold_value,
                "explanation": ev.explanation,
                "regulatory_ref": ev.regulatory_ref
            })
            if ev.regulatory_ref:
                reg_citation_ids.add(ev.regulatory_ref)

    # Collect Demo Regulatory Citations
    citations = []
    for ref_id in sorted(list(reg_citation_ids)):
        doc = get_regulatory_rule_by_id(ref_id)
        if doc:
            citations.append({
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "authority": doc["authority"],
                "summary": doc["summary"],
                "monitored_scenarios": doc.get("monitored_scenarios", ""),
                "recommended_compliance_action": doc["recommended_compliance_action"]
            })

    # Parse notes into structured items
    notes_lines = (inv.analyst_notes or "").split("\n")
    notes_history = [{"entry": line.strip()} for line in notes_lines if line.strip()]

    # Compliance recommendation based on status and risk
    if inv.status == "Escalated":
        recom = "Immediate filing of formal Suspicious Transaction Report (STR/SAR) with Demo FIU. Place temporary debit hold on outward international remittances pending documentary verification."
    elif inv.status == "Resolved":
        recom = "Source of funds and legitimate commercial documentation verified. Risk rating adjusted to normal operational monitoring."
    elif inv.status == "False Positive":
        recom = "Determined legitimate pre-cleared transactional pattern. Whitelisted specific merchant corridor with annual review."
    else:
        recom = "Maintain account under Level-2 Enhanced Scrutiny. Request source-of-wealth documentation, tax filings, and trade contracts within 48 hours."

    report_id = f"REP-{inv.investigation_id}-{datetime.utcnow().strftime('%Y%m%d%H%M')}"

    return InvestigationReport(
        report_id=report_id,
        generated_at=datetime.utcnow(),
        title=f"Compliance Investigation & Regulatory Audit: {inv.title}",
        investigation_id=inv.investigation_id,
        status=inv.status,
        priority=inv.priority,
        assigned_analyst=inv.assigned_analyst,
        customer=customer_dict,
        primary_transaction=primary_txn_dict,
        related_transactions=related_txns,
        triggered_rules=triggered_rules,
        regulatory_citations=citations,
        findings=inv.findings or "Detailed evidentiary audit conducted.",
        notes_history=notes_history,
        compliance_recommendation=recom,
        disclaimer="Demo Regulatory Knowledge Base - Formal Compliance Audit Prototype for HackSkill Demonstration"
    )

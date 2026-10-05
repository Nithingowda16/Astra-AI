from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.core.database import get_db
from backend.app.models.regulatory_doc import RegulatoryDoc
from backend.app.schemas.regulatory_doc import RegulatoryDocResponse
from backend.app.regulatory.demo_knowledge_base import get_all_regulatory_rules, get_regulatory_rule_by_id

router = APIRouter(prefix="/regulatory", tags=["Regulatory Knowledge"])

@router.get("/rules", response_model=List[RegulatoryDocResponse])
def get_regulatory_rules(
    search: Optional[str] = Query(None, description="Search regulatory rules by keyword"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    query = db.query(RegulatoryDoc)
    if category:
        query = query.filter(RegulatoryDoc.category.ilike(f"%{category.strip()}%"))
    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(
            (RegulatoryDoc.doc_id.ilike(search_fmt)) |
            (RegulatoryDoc.title.ilike(search_fmt)) |
            (RegulatoryDoc.summary.ilike(search_fmt)) |
            (RegulatoryDoc.full_clause.ilike(search_fmt))
        )

    docs = query.all()
    if not docs:
        # Fallback to in-memory list
        docs_list = get_all_regulatory_rules()
        return [
            RegulatoryDocResponse(
                doc_id=d["doc_id"],
                title=d["title"],
                authority=d["authority"],
                category=d["category"],
                summary=d["summary"],
                full_clause=d["full_clause"],
                monitored_scenarios=d.get("monitored_scenarios", ""),
                recommended_compliance_action=d["recommended_compliance_action"],
                disclaimer=d["disclaimer"]
            )
            for d in docs_list
        ]

    return [
        RegulatoryDocResponse(
            doc_id=d.doc_id,
            title=d.title,
            authority=d.authority,
            category=d.category,
            summary=d.summary,
            full_clause=d.full_clause,
            monitored_scenarios=d.monitored_scenarios,
            recommended_compliance_action=d.recommended_compliance_action,
            disclaimer=d.disclaimer
        )
        for d in docs
    ]

@router.get("/rules/{doc_id}", response_model=RegulatoryDocResponse)
def get_single_regulatory_rule(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(RegulatoryDoc).filter(RegulatoryDoc.doc_id.ilike(doc_id.strip())).first()
    if not doc:
        fallback = get_regulatory_rule_by_id(doc_id)
        if fallback:
            return RegulatoryDocResponse(
                doc_id=fallback["doc_id"],
                title=fallback["title"],
                authority=fallback["authority"],
                category=fallback["category"],
                summary=fallback["summary"],
                full_clause=fallback["full_clause"],
                monitored_scenarios=fallback.get("monitored_scenarios", ""),
                recommended_compliance_action=fallback["recommended_compliance_action"],
                disclaimer=fallback["disclaimer"]
            )
        raise HTTPException(status_code=404, detail=f"Regulatory Rule {doc_id} not found.")

    return RegulatoryDocResponse(
        doc_id=doc.doc_id,
        title=doc.title,
        authority=doc.authority,
        category=doc.category,
        summary=doc.summary,
        full_clause=doc.full_clause,
        monitored_scenarios=doc.monitored_scenarios,
        recommended_compliance_action=doc.recommended_compliance_action,
        disclaimer=doc.disclaimer
    )

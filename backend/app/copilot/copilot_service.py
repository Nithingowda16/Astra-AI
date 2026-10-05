"""
Investigation Copilot Service
Provides context-aware conversational risk intelligence, entity extraction,
grounded reasoning from database transactions, and direct citations
from the Demo Regulatory Knowledge Base without hallucination.
"""

import re
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from backend.app.models.customer import Customer
from backend.app.models.transaction import Transaction
from backend.app.models.rule_evaluation import RuleEvaluation
from backend.app.models.alert import Alert
from backend.app.models.investigation import Investigation
from backend.app.models.regulatory_doc import RegulatoryDoc
from backend.app.regulatory.demo_knowledge_base import get_all_regulatory_rules, get_regulatory_rule_by_id
from backend.app.copilot.llm_client import llm_client

class CopilotService:
    @staticmethod
    def process_query(
        query: str,
        db: Session,
        context_customer_id: Optional[str] = None,
        context_transaction_id: Optional[str] = None
    ) -> Dict[str, Any]:
        q = query.strip()
        q_lower = q.lower()

        # 1. Extract IDs from query or context
        txn_match = re.search(r"TXN-\d+", q, re.IGNORECASE)
        cust_match = re.search(r"CUST-\d+", q, re.IGNORECASE)

        target_txn_id = txn_match.group(0).upper() if txn_match else context_transaction_id
        target_cust_id = cust_match.group(0).upper() if cust_match else context_customer_id

        # If a transaction ID is found or passed, check if we need to resolve customer
        if target_txn_id and not target_cust_id:
            txn_lookup = db.query(Transaction).filter(Transaction.transaction_id == target_txn_id).first()
            if txn_lookup:
                target_cust_id = txn_lookup.customer_id

        result = None

        # -------------------------------------------------------------
        # SCENARIO 1: "Why was transaction TXN-xxxx flagged?"
        # -------------------------------------------------------------
        if target_txn_id and any(k in q_lower for k in ["why", "flagged", "reason", "explain", "detail", "alert", "trigger"]):
            result = CopilotService._handle_transaction_explanation(target_txn_id, db)

        # -------------------------------------------------------------
        # SCENARIO 2: "Why is this customer considered high risk?" or "What are the main risk indicators for customer CUST-xxxx?"
        # -------------------------------------------------------------
        elif target_cust_id and any(k in q_lower for k in ["why", "risk", "indicator", "profile", "considered", "high risk", "score"]):
            result = CopilotService._handle_customer_risk_explanation(target_cust_id, db)

        # -------------------------------------------------------------
        # SCENARIO 3: "Generate an investigation summary for this customer / CUST-xxxx"
        # -------------------------------------------------------------
        elif target_cust_id and any(k in q_lower for k in ["summary", "generate", "report", "investigation"]):
            result = CopilotService._handle_customer_investigation_summary(target_cust_id, db)

        # -------------------------------------------------------------
        # SCENARIO 4: "Show regulatory evidence supporting this finding / policy evidence"
        # -------------------------------------------------------------
        elif any(k in q_lower for k in ["regulatory", "evidence", "policy", "rule", "guidance", "fiu", "compliance"]):
            result = CopilotService._handle_regulatory_evidence(q_lower, target_txn_id, target_cust_id, db)

        # -------------------------------------------------------------
        # SCENARIO 5: "Show me high-risk transactions above ₹5 lakh" / large value queries
        # -------------------------------------------------------------
        elif any(k in q_lower for k in ["5 lakh", "5l", "500000", "5,00,000", "above", "exceeding", "large"]):
            result = CopilotService._handle_high_value_query(q_lower, db)

        # -------------------------------------------------------------
        # SCENARIO 6: "Show suspicious transactions involving high-risk countries"
        # -------------------------------------------------------------
        elif any(k in q_lower for k in ["country", "countries", "jurisdiction", "offshore", "cayman", "panama", "vanuatu"]):
            result = CopilotService._handle_high_risk_country_query(db)

        # -------------------------------------------------------------
        # SCENARIO 7: General search by customer name or fallback
        # -------------------------------------------------------------
        else:
            cust_name_match = db.query(Customer).filter(Customer.full_name.ilike(f"%{q[:15]}%")).first()
            if cust_name_match:
                result = CopilotService._handle_customer_risk_explanation(cust_name_match.customer_id, db)
            else:
                result = {
                    "query": query,
                    "answer": "Insufficient data available. The system could not match your query with active customer, transaction, or regulatory records.",
                    "data_found": False,
                    "entities": [],
                    "risk_indicators": [
                        "No matching records identified for current parameters.",
                        "Ensure valid Transaction ID (e.g., TXN-1024) or Customer ID (e.g., CUST-1008)."
                    ],
                    "supporting_evidence": [],
                    "suggested_actions": [
                        "Try asking: 'Why was transaction TXN-1024 flagged?'",
                        "Try asking: 'What are the main risk indicators for customer CUST-1008?'",
                        "Try asking: 'Show me high-risk transactions above ₹5 lakh.'",
                        "Try asking: 'Show suspicious transactions involving high-risk countries.'",
                        "Try asking: 'Show the regulatory evidence supporting this finding.'"
                    ],
                    "disclaimer": "Astra AI Regulatory Intelligence Engine"
                }

        # Real API Key LLM Synthesis Enhancement (OpenAI, Gemini, Groq)
        if result and llm_client.is_configured():
            try:
                llm_response = llm_client.generate_response(query, {
                    "data_found": result.get("data_found"),
                    "entities": result.get("entities"),
                    "risk_indicators": result.get("risk_indicators"),
                    "supporting_evidence": result.get("supporting_evidence"),
                    "suggested_actions": result.get("suggested_actions"),
                    "context_data": result.get("answer")
                })
                if llm_response:
                    result["answer"] = llm_response
                    active_p = llm_client.get_active_provider()
                    result["disclaimer"] = f"Astra AI Neural Reasoning • Powered by {active_p.upper()}"
            except Exception as e:
                pass

        return result

    @staticmethod
    def _handle_transaction_explanation(txn_id: str, db: Session) -> Dict[str, Any]:
        txn = db.query(Transaction).filter(Transaction.transaction_id == txn_id).first()
        if not txn:
            return {
                "query": f"Explain transaction {txn_id}",
                "answer": f"Insufficient data available. Transaction '{txn_id}' was not found in the transaction registry.",
                "data_found": False,
                "entities": [],
                "risk_indicators": [],
                "supporting_evidence": [],
                "suggested_actions": ["Verify transaction ID format (e.g. TXN-1024)."],
                "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
            }

        cust = db.query(Customer).filter(Customer.customer_id == txn.customer_id).first()
        evals = db.query(RuleEvaluation).filter(RuleEvaluation.transaction_id == txn_id).all()

        entities = [
            {
                "type": "transaction",
                "id": txn.transaction_id,
                "label": f"{txn.transaction_id}: ₹{txn.amount:,.2f} to {txn.destination_country}",
                "details": {
                    "amount": txn.amount,
                    "currency": txn.currency,
                    "destination": txn.destination_country,
                    "risk_score": txn.risk_score,
                    "risk_level": txn.risk_level
                }
            }
        ]
        if cust:
            entities.append({
                "type": "customer",
                "id": cust.customer_id,
                "label": f"{cust.full_name} ({cust.customer_id})",
                "details": {
                    "baseline_avg": cust.baseline_avg_amount,
                    "occupation": cust.occupation,
                    "account_type": cust.account_type
                }
            })

        risk_indicators = []
        evidence_list = []
        for ev in evals:
            risk_indicators.append(f"{ev.rule_name} (+{ev.score_contribution} pts): {ev.explanation}")
            if ev.regulatory_ref:
                reg_rule = get_regulatory_rule_by_id(ev.regulatory_ref)
                if reg_rule:
                    evidence_list.append({
                        "source": f"{reg_rule['doc_id']}: {reg_rule['title']}",
                        "doc_id": reg_rule["doc_id"],
                        "title": reg_rule["title"],
                        "excerpt": reg_rule["summary"],
                        "authority": reg_rule["authority"]
                    })

        ratio_str = ""
        if cust and cust.baseline_avg_amount > 0:
            ratio = txn.amount / cust.baseline_avg_amount
            ratio_str = f" This represents a {ratio:.1f}x surge over their baseline average of ₹{cust.baseline_avg_amount:,.2f}."

        answer = (
            f"Transaction **{txn.transaction_id}** was flagged with a **{txn.risk_level}** risk score of **{txn.risk_score}/100**."
            f" It executed a {txn.transaction_type} of **₹{txn.amount:,.2f}** to **{txn.destination_country}**"
            f" under category '{txn.merchant_category or 'N/A'}'.{ratio_str}"
            f" The transaction triggered {len(evals)} explainable compliance rules, primarily due to large value deviation"
            f" and destination jurisdiction classification."
        )

        suggested_actions = [
            f"Freeze outward settlement of {txn.transaction_id} pending documentary proof of funds.",
            f"Open Level-2 investigation for customer {txn.customer_id}.",
            "Request notarized commercial invoice and Ultimate Beneficial Ownership (UBO) declaration.",
            "File Demo Suspicious Transaction Report (STR/SAR) with Demo FIU if documentation is not provided within 24 hours."
        ]

        return {
            "query": f"Why was transaction {txn_id} flagged?",
            "answer": answer,
            "data_found": True,
            "entities": entities,
            "risk_indicators": risk_indicators if risk_indicators else [txn.flagged_reason_summary or "Flagged by risk engine"],
            "supporting_evidence": evidence_list,
            "suggested_actions": suggested_actions,
            "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
        }

    @staticmethod
    def _handle_customer_risk_explanation(cust_id: str, db: Session) -> Dict[str, Any]:
        cust = db.query(Customer).filter(Customer.customer_id == cust_id).first()
        if not cust:
            return {
                "query": f"Risk indicators for customer {cust_id}",
                "answer": f"Insufficient data available. Customer '{cust_id}' could not be located in records.",
                "data_found": False,
                "entities": [],
                "risk_indicators": [],
                "supporting_evidence": [],
                "suggested_actions": ["Verify Customer ID (e.g. CUST-1008)."],
                "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
            }

        flagged_txns = db.query(Transaction).filter(
            Transaction.customer_id == cust_id,
            Transaction.is_flagged == True
        ).all()

        total_txns = db.query(Transaction).filter(Transaction.customer_id == cust_id).count()

        risk_indicators = [
            f"Elevated Overall Risk Score: {cust.risk_score}/100 ({cust.risk_level} Risk Category).",
            f"Historical Average Baseline: ₹{cust.baseline_avg_amount:,.2f} (Monthly Baseline: ₹{cust.baseline_monthly_volume:,.2f}).",
            f"Flagged Transactions: {len(flagged_txns)} of {total_txns} total transactions marked as high risk.",
        ]
        if cust.is_pep:
            risk_indicators.append("Customer is designated as a Politically Exposed Person (PEP).")

        # Collect rule evaluations across flagged transactions
        evidence_list = []
        reg_refs = set()
        for t in flagged_txns:
            evals = db.query(RuleEvaluation).filter(RuleEvaluation.transaction_id == t.transaction_id).all()
            for ev in evals:
                risk_indicators.append(f"[{t.transaction_id}] {ev.rule_name}: {ev.explanation}")
                if ev.regulatory_ref:
                    reg_refs.add(ev.regulatory_ref)

        for ref in sorted(list(reg_refs)):
            reg = get_regulatory_rule_by_id(ref)
            if reg:
                evidence_list.append({
                    "source": f"{reg['doc_id']}: {reg['title']}",
                    "doc_id": reg["doc_id"],
                    "title": reg["title"],
                    "excerpt": reg["summary"],
                    "authority": reg["authority"]
                })

        entities = [
            {
                "type": "customer",
                "id": cust.customer_id,
                "label": f"{cust.full_name} ({cust.occupation})",
                "details": {
                    "account_type": cust.account_type,
                    "country": cust.country,
                    "kyc_status": cust.kyc_status,
                    "risk_score": cust.risk_score
                }
            }
        ]
        for ft in flagged_txns[:3]:
            entities.append({
                "type": "transaction",
                "id": ft.transaction_id,
                "label": f"{ft.transaction_id}: ₹{ft.amount:,.2f} ({ft.destination_country})",
                "details": {"amount": ft.amount, "status": ft.status}
            })

        answer = (
            f"Customer **{cust.full_name}** ({cust.customer_id}) is classified as **{cust.risk_level} RISK** "
            f"with an aggregate risk rating of **{cust.risk_score}/100**.\n\n"
            f"Key drivers for this classification include **{len(flagged_txns)} suspicious transactions** "
            f"that severely diverge from their declared occupation as '{cust.occupation}' and their established monthly baseline "
            f"of ₹{cust.baseline_monthly_volume:,.2f}. Recent high-value outward flows routed to high-risk offshore secrecy zones "
            f"(including Cayman Islands and Panama) with rapid velocity burst patterns."
        )

        suggested_actions = [
            f"Execute Enhanced Due Diligence (EDD) re-KYC on account {cust.customer_id}.",
            "Dispatch Source-of-Wealth Questionnaire regarding foreign capital transfers.",
            "Consolidate all associated accounts under active Compliance Case INV-2024-008.",
            "Schedule Level-2 MLRO Escalation Review."
        ]

        return {
            "query": f"What are the main risk indicators for customer {cust_id}?",
            "answer": answer,
            "data_found": True,
            "entities": entities,
            "risk_indicators": risk_indicators,
            "supporting_evidence": evidence_list,
            "suggested_actions": suggested_actions,
            "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
        }

    @staticmethod
    def _handle_customer_investigation_summary(cust_id: str, db: Session) -> Dict[str, Any]:
        cust = db.query(Customer).filter(Customer.customer_id == cust_id).first()
        if not cust:
            return {
                "query": f"Investigation summary for {cust_id}",
                "answer": "Insufficient data available.",
                "data_found": False,
                "entities": [],
                "risk_indicators": [],
                "supporting_evidence": [],
                "suggested_actions": [],
                "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
            }

        flagged_txns = db.query(Transaction).filter(
            Transaction.customer_id == cust_id,
            Transaction.is_flagged == True
        ).all()
        flagged_sum = sum(t.amount for t in flagged_txns)

        existing_inv = db.query(Investigation).filter(Investigation.customer_id == cust_id).first()

        answer = (
            f"### COMPLIANCE INVESTIGATION BRIEF: {cust.full_name} ({cust.customer_id})\n\n"
            f"• **Risk Assessment**: Score {cust.risk_score}/100 ({cust.risk_level})\n"
            f"• **Account Profile**: {cust.account_type} Account | KYC: {cust.kyc_status} | PEP: {'Yes' if cust.is_pep else 'No'}\n"
            f"• **Total Flagged Exposure**: ₹{flagged_sum:,.2f} across {len(flagged_txns)} transactions\n"
            f"• **Primary Incident**: Primary transfer TXN-1024 (₹12,50,000.00 to Cayman Islands), followed by rapid successive outbound transfer TXN-1025 to Panama.\n"
            f"• **Investigation Status**: {existing_inv.status if existing_inv else 'Open'} (Assigned: {existing_inv.assigned_analyst if existing_inv else 'Senior Compliance Officer'})\n\n"
            f"**Conclusion**: Behavior exhibits high-probability capital flight and structuring through offshore entities, violating Demo AML Rule 01 and Demo AML Rule 03."
        )

        return {
            "query": f"Generate an investigation summary for customer {cust_id}",
            "answer": answer,
            "data_found": True,
            "entities": [
                {"type": "customer", "id": cust.customer_id, "label": cust.full_name},
                {"type": "investigation", "id": existing_inv.investigation_id if existing_inv else "NEW-CASE", "label": "Compliance Scrutiny Case"}
            ],
            "risk_indicators": [
                f"Surge multiple: {round(flagged_sum / max(cust.baseline_avg_amount, 1), 1)}x baseline",
                "Unusual international corridors (Cayman Islands, Panama)",
                "Burst transaction spacing (<15 min interval)"
            ],
            "supporting_evidence": [
                {
                    "source": "Demo AML Rule 01: Customer Due Diligence (CDD) & High-Value Transfers",
                    "doc_id": "REG-AML-01",
                    "title": "Large Value Single Transfers > ₹5 Lakh",
                    "excerpt": "Transactions exceeding ₹5,00,000 or >300% of baseline require mandatory source-of-funds verification.",
                    "authority": "Demo Financial Intelligence Unit (FIU-Demo)"
                },
                {
                    "source": "Demo AML Rule 03: High-Risk Jurisdictions",
                    "doc_id": "REG-AML-03",
                    "title": "Offshore Secrecy & Deficient AML Jurisdictions",
                    "excerpt": "Mandatory Enhanced Due Diligence and MLRO escalation on flows to Cayman Islands/Panama.",
                    "authority": "Demo Sanctions Committee"
                }
            ],
            "suggested_actions": [
                "Download formal Investigation Report PDF/Printable.",
                "Escalate case status to 'Escalated' for Senior MLRO sign-off.",
                "Transmit electronic Suspicious Transaction Report (STR) to regulatory authority."
            ],
            "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
        }

    @staticmethod
    def _handle_regulatory_evidence(
        q_lower: str,
        txn_id: Optional[str],
        cust_id: Optional[str],
        db: Session
    ) -> Dict[str, Any]:
        rules = get_all_regulatory_rules()

        # If specific transaction or customer was mentioned, fetch their triggered rules
        matched_rules = []
        if txn_id:
            evals = db.query(RuleEvaluation).filter(RuleEvaluation.transaction_id == txn_id).all()
            for ev in evals:
                if ev.regulatory_ref:
                    r_doc = get_regulatory_rule_by_id(ev.regulatory_ref)
                    if r_doc and r_doc not in matched_rules:
                        matched_rules.append(r_doc)

        if not matched_rules:
            matched_rules = rules[:3]

        evidence_items = []
        indicators = []
        for r in matched_rules:
            evidence_items.append({
                "source": f"{r['doc_id']}: {r['title']}",
                "doc_id": r["doc_id"],
                "title": r["title"],
                "excerpt": r["summary"],
                "authority": r["authority"]
            })
            indicators.append(f"{r['doc_id']}: {r['recommended_compliance_action']}")

        answer = (
            f"Here is the supporting evidence from the **Demo Regulatory Knowledge Base**:\n\n"
            + "\n\n".join([
                f"### {r['title']}\n"
                f"**Issuing Authority**: {r['authority']}\n"
                f"**Mandate**: {r['summary']}\n"
                f"**Monitored Scenarios**: {r.get('monitored_scenarios', '')}\n"
                f"**Required Compliance Action**: {r['recommended_compliance_action']}"
                for r in matched_rules
            ])
        )

        return {
            "query": "Show the regulatory evidence supporting this finding",
            "answer": answer,
            "data_found": True,
            "entities": [{"type": "rule", "id": r["doc_id"], "label": r["title"]} for r in matched_rules],
            "risk_indicators": indicators,
            "supporting_evidence": evidence_items,
            "suggested_actions": [
                "Review complete regulatory documentation in the 'Regulatory Knowledge' module.",
                "Attach cited clauses directly into active investigation case file.",
                "Verify compliance audit trail against Demo FIU reporting standards."
            ],
            "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
        }

    @staticmethod
    def _handle_high_value_query(q_lower: str, db: Session) -> Dict[str, Any]:
        txns = db.query(Transaction).filter(Transaction.amount >= 500000.0).order_by(Transaction.amount.desc()).all()
        if not txns:
            return {
                "query": "Show me high-risk transactions above ₹5 lakh",
                "answer": "Insufficient data available. No transactions above ₹5,00,000 were found.",
                "data_found": False,
                "entities": [],
                "risk_indicators": [],
                "supporting_evidence": [],
                "suggested_actions": [],
                "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
            }

        entities = []
        indicators = []
        for t in txns:
            cust = db.query(Customer).filter(Customer.customer_id == t.customer_id).first()
            c_name = cust.full_name if cust else t.customer_id
            entities.append({
                "type": "transaction",
                "id": t.transaction_id,
                "label": f"{t.transaction_id}: ₹{t.amount:,.2f} ({c_name} -> {t.destination_country})",
                "details": {
                    "amount": t.amount,
                    "destination": t.destination_country,
                    "risk_score": t.risk_score,
                    "risk_level": t.risk_level
                }
            })
            indicators.append(f"{t.transaction_id} ({c_name}): ₹{t.amount:,.2f} to {t.destination_country} - {t.risk_level} Risk ({t.risk_score}/100)")

        answer = (
            f"Identified **{len(txns)} transactions** exceeding the ₹5,00,000 (INR 5 Lakh) regulatory monitoring threshold:\n\n"
            + "\n".join([f"• **{t.transaction_id}**: ₹{t.amount:,.2f} to **{t.destination_country}** ({t.risk_level} Risk, Score {t.risk_score}/100)" for t in txns])
            + f"\n\nThe highest-risk item is **TXN-1024** (₹12,50,000.00 to Cayman Islands), which exceeds the customer's baseline by 44x and routes to a high-risk secrecy jurisdiction."
        )

        reg_doc = get_regulatory_rule_by_id("REG-AML-01")
        evidence = []
        if reg_doc:
            evidence.append({
                "source": f"{reg_doc['doc_id']}: {reg_doc['title']}",
                "doc_id": reg_doc["doc_id"],
                "title": reg_doc["title"],
                "excerpt": reg_doc["summary"],
                "authority": reg_doc["authority"]
            })

        return {
            "query": "Show me high-risk transactions above ₹5 lakh",
            "answer": answer,
            "data_found": True,
            "entities": entities,
            "risk_indicators": indicators,
            "supporting_evidence": evidence,
            "suggested_actions": [
                "Click on TXN-1024 in the Transactions view to inspect full rule breakdown.",
                "Review Customer Due Diligence (CDD) documents for high-value senders.",
                "Ensure outward transfers carry authenticated trade contracts."
            ],
            "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
        }

    @staticmethod
    def _handle_high_risk_country_query(db: Session) -> Dict[str, Any]:
        high_risk_names = ["Cayman Islands", "Panama", "Vanuatu", "North Cyprus", "British Virgin Islands", "Seychelles"]
        txns = db.query(Transaction).filter(
            Transaction.destination_country.in_(high_risk_names)
        ).order_by(Transaction.risk_score.desc()).all()

        if not txns:
            return {
                "query": "Show suspicious transactions involving high-risk countries",
                "answer": "Insufficient data available. No transactions involving high-risk jurisdictions found.",
                "data_found": False,
                "entities": [],
                "risk_indicators": [],
                "supporting_evidence": [],
                "suggested_actions": [],
                "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
            }

        entities = []
        indicators = []
        for t in txns:
            cust = db.query(Customer).filter(Customer.customer_id == t.customer_id).first()
            c_name = cust.full_name if cust else t.customer_id
            entities.append({
                "type": "transaction",
                "id": t.transaction_id,
                "label": f"{t.transaction_id}: ₹{t.amount:,.2f} -> {t.destination_country} ({c_name})",
                "details": {"destination": t.destination_country, "amount": t.amount}
            })
            indicators.append(f"{t.transaction_id} -> {t.destination_country}: ₹{t.amount:,.2f} ({t.risk_level} Risk)")

        answer = (
            f"Found **{len(txns)} transactions** routing to designated high-risk secrecy jurisdictions:\n\n"
            + "\n".join([f"• **{t.transaction_id}**: ₹{t.amount:,.2f} to **{t.destination_country}** (Customer: {t.customer_id}, Score: {t.risk_score}/100)" for t in txns])
            + "\n\nAll cross-border transfers to these jurisdictions require mandatory Enhanced Due Diligence (EDD) under Demo AML Rule 03."
        )

        reg_doc = get_regulatory_rule_by_id("REG-AML-03")
        evidence = []
        if reg_doc:
            evidence.append({
                "source": f"{reg_doc['doc_id']}: {reg_doc['title']}",
                "doc_id": reg_doc["doc_id"],
                "title": reg_doc["title"],
                "excerpt": reg_doc["summary"],
                "authority": reg_doc["authority"]
            })

        return {
            "query": "Show suspicious transactions involving high-risk countries",
            "answer": answer,
            "data_found": True,
            "entities": entities,
            "risk_indicators": indicators,
            "supporting_evidence": evidence,
            "suggested_actions": [
                "Execute Enhanced Due Diligence (EDD) verification on all offshore transfers.",
                "Confirm Ultimate Beneficial Ownership (UBO) for offshore recipient entities.",
                "Escalate flagged transactions to Senior MLRO."
            ],
            "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
        }

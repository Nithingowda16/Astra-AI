"""
Demo Regulatory Knowledge Base
Simulated compliance guidelines clearly labeled for demonstration purposes.
"""

from typing import List, Dict, Optional

DEMO_REGULATORY_RULES = [
    {
        "doc_id": "REG-AML-01",
        "title": "Demo AML Rule 01: Customer Due Diligence (CDD) & High-Value Single Transfer Thresholds",
        "authority": "Demo Financial Intelligence Unit (FIU-Demo)",
        "category": "Customer Due Diligence & Thresholds",
        "summary": "Mandates enhanced scrutiny and mandatory source-of-funds verification for individual transactions exceeding ₹5,00,000 (or foreign currency equivalent) that deviate from established customer income profile.",
        "full_clause": (
            "Section 4.1 - Large Value Transfers: Financial institutions shall subject any outward or inward fund transfer "
            "exceeding INR 500,000 (or equivalent foreign exchange) to secondary compliance verification. Where the transfer amount "
            "exceeds 300% of the customer's historical 90-day average transaction baseline, the institution must immediately secure "
            "documentary proof of legitimate commercial rationale and beneficiary identity."
        ),
        "monitored_scenarios": "Single transfers > ₹5,00,000; sudden single spikes > 300% of customer average transaction value.",
        "recommended_compliance_action": "Freeze outbound dispatch if unverified; request audited bank statements / invoices within 24 hours; flag for suspicious transaction reporting (STR) if satisfactory explanation is not furnished.",
        "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
    },
    {
        "doc_id": "REG-AML-02",
        "title": "Demo AML Rule 02: Structuring & Smurfing Detection (Rapid Velocity Sub-Threshold Bursts)",
        "authority": "Demo AML Oversight Framework (FATF Rec 20 Alignment)",
        "category": "Structuring & Smurfing",
        "summary": "Defines detection rules for deliberate structuring where multiple transactions slightly below reporting limits (e.g. ₹50,000 or ₹1,00,000) occur within a compressed temporal window (under 60 minutes).",
        "full_clause": (
            "Section 7.3 - Prevention of Structuring / Smurfing: Any sequence of 3 or more transactions originating from "
            "or routed to the same account within a 1-hour rolling window, each sized between 80% and 99% of reporting thresholds, "
            "shall be classified as an intentional evasion indicator. Such transactions must be aggregated and evaluated as a singular high-risk event."
        ),
        "monitored_scenarios": "3+ transactions within 60 minutes between ₹45,000 - ₹49,999 or ₹90,000 - ₹99,999; rapid repetitive round-trip transfers.",
        "recommended_compliance_action": "Initiate automated velocity freeze; aggregate cumulative sum; file an immediate Priority Suspicious Activity Report (SAR) with FIU-Demo.",
        "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
    },
    {
        "doc_id": "REG-AML-03",
        "title": "Demo AML Rule 03: High-Risk Jurisdictions & Non-Cooperative Sanctioned Corridors",
        "authority": "Demo International Sanctions & Jurisdiction Committee",
        "category": "High-Risk Jurisdictions",
        "summary": "Imposes mandatory Enhanced Due Diligence (EDD) and escalation on all financial flows routing through or terminating in designated FATF-grey/black listed or offshore secrecy jurisdictions.",
        "full_clause": (
            "Section 11.2 - Enhanced Cross-Border Scrutiny: Transactions routing to or received from jurisdictions classified as "
            "Deficient AML Regimes or Secrecy Havens (including Cayman Islands, Panama, Vanuatu, North Cyprus, and designated high-risk offshore zones) "
            "require automated flag creation, beneficiary ultimate beneficial ownership (UBO) declaration, and Level-2 MLRO sign-off prior to settlement."
        ),
        "monitored_scenarios": "Transfers involving Cayman Islands, Panama, Vanuatu, North Cyprus, or unverified offshore correspondent accounts.",
        "recommended_compliance_action": "Require notarized UBO registry filings; perform sanctions screening on intermediary banks; escalate to Level-2 Compliance Lead.",
        "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
    },
    {
        "doc_id": "REG-AML-04",
        "title": "Demo AML Rule 04: Uncharacteristic Behavioral Deviation & Historical Baseline Rupture",
        "authority": "Demo Supervisory Authority on Transaction Monitoring",
        "category": "Behavioral Anomaly & Profile Mismatch",
        "summary": "Identifies account behavior that contradicts the declared KYC occupation, annual turnover, or historic activity patterns, including sudden spikes in monthly cumulative volume.",
        "full_clause": (
            "Section 8.5 - Pattern Deviation Monitoring: An anomaly score shall trigger when aggregate 7-day flow exceeds 400% of "
            "the customer's declared monthly baseline volume, or when transactions occur in merchant categories incompatible with the customer profile "
            "(e.g., retail individual routing millions into offshore shell consulting or overseas shell holding entities)."
        ),
        "monitored_scenarios": "Cumulative weekly flow > 4x monthly baseline; sudden overseas high-value wire from retail savings account.",
        "recommended_compliance_action": "Conduct immediate Customer Risk Re-rating; request re-KYC documentation and tax filings; assign case for manual investigative review.",
        "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
    },
    {
        "doc_id": "REG-AML-05",
        "title": "Demo AML Rule 05: Politically Exposed Persons (PEPs) & Special Attention Accounts",
        "authority": "Demo Anti-Corruption & Integrity Directive",
        "category": "PEP & Adverse Media",
        "summary": "Mandates continuous transactional oversight, senior executive approval, and rigorous source of wealth verification for Politically Exposed Persons and their close associates.",
        "full_clause": (
            "Section 5.8 - PEP Operational Oversight: All transactions executed by or on behalf of Politically Exposed Persons (PEPs) "
            "exceeding INR 2,00,000 must carry detailed purpose rationale. Any international wire transfer from a PEP account into private investment "
            "vehicles or non-resident entities requires formal review by the Chief Compliance Officer."
        ),
        "monitored_scenarios": "Any wire > ₹2,00,000 initiated by a PEP-flagged customer; transfers to third-party offshore trusts.",
        "recommended_compliance_action": "Obtain Senior Compliance sign-off; conduct adverse media screening check; cross-reference declared assets with public disclosures.",
        "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
    },
    {
        "doc_id": "REG-AML-06",
        "title": "Demo AML Rule 06: Shell Company Indicators, Round-Tripping & Pass-Through Layering",
        "authority": "Demo Financial Crime Enforcement Network",
        "category": "Layering & Shell Companies",
        "summary": "Detects high-turnover pass-through velocity where funds are credited and almost immediately debited to unrelated offshore counterparties with minimal retained balance.",
        "full_clause": (
            "Section 9.4 - Pass-Through / Layering Defense: Accounts exhibiting transit characteristics—wherein over 90% of incoming funds "
            "are wired out within 48 hours to non-resident commercial entities without commercial inventory or payroll footprint—must be "
            "categorized as high-probability layering."
        ),
        "monitored_scenarios": "Rapid credit-followed-by-debit transfers; offshore holding merchant categories; nominal retained account balances.",
        "recommended_compliance_action": "Issue temporary debit restraint; subpoena underlying trade contracts; submit regulatory Suspicious Activity Report (SAR).",
        "disclaimer": "Demo Regulatory Knowledge Base - Simulated Compliance Guidance"
    }
]

def get_all_regulatory_rules() -> List[Dict]:
    return DEMO_REGULATORY_RULES

def get_regulatory_rule_by_id(doc_id: str) -> Optional[Dict]:
    for rule in DEMO_REGULATORY_RULES:
        if rule["doc_id"].lower() == doc_id.lower():
            return rule
    return None

def search_regulatory_rules(query: str) -> List[Dict]:
    q = query.lower()
    matches = []
    for rule in DEMO_REGULATORY_RULES:
        if (
            q in rule["doc_id"].lower()
            or q in rule["title"].lower()
            or q in rule["category"].lower()
            or q in rule["summary"].lower()
            or q in rule["monitored_scenarios"].lower()
        ):
            matches.append(rule)
    return matches if matches else DEMO_REGULATORY_RULES[:3]

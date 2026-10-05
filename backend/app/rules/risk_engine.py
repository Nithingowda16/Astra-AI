"""
Explainable Rule-Based Fraud & Risk Detection Engine
Calculates deterministic risk scores and provides line-by-line justification
mapped directly to Demo Regulatory Knowledge Base clauses.
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import uuid

HIGH_RISK_JURISDICTIONS = {
    "cayman islands",
    "panama",
    "vanuatu",
    "north cyprus",
    "british virgin islands",
    "seychelles",
    "belize",
    "bahamas",
    "turks and caicos"
}

HIGH_RISK_CATEGORIES = {
    "casino/gambling",
    "casino",
    "offshore holding",
    "cryptocurrency mixer",
    "unregistered shell entity",
    "shell investment vehicle",
    "private wealth conduit"
}

class EvaluatedRuleResult:
    def __init__(
        self,
        rule_id: str,
        rule_name: str,
        score_contribution: int,
        severity: str,
        observed_value: str,
        threshold_value: str,
        explanation: str,
        regulatory_ref: Optional[str] = None
    ):
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.score_contribution = score_contribution
        self.severity = severity
        self.observed_value = observed_value
        self.threshold_value = threshold_value
        self.explanation = explanation
        self.regulatory_ref = regulatory_ref

    def to_dict(self) -> Dict:
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "score_contribution": self.score_contribution,
            "severity": self.severity,
            "observed_value": self.observed_value,
            "threshold_value": self.threshold_value,
            "explanation": self.explanation,
            "regulatory_ref": self.regulatory_ref,
        }

class RiskEngine:
    @staticmethod
    def evaluate_transaction(
        transaction_dict: Dict,
        customer_dict: Dict,
        recent_customer_transactions: Optional[List[Dict]] = None
    ) -> Tuple[int, str, bool, str, List[EvaluatedRuleResult]]:
        """
        Evaluates a transaction in the context of customer history and returns:
        (risk_score, risk_level, is_flagged, summary, rule_results)
        """
        recent_txns = recent_customer_transactions or []
        rule_results: List[EvaluatedRuleResult] = []

        amount = float(transaction_dict.get("amount", 0.0))
        currency = transaction_dict.get("currency", "INR")
        dest_country = str(transaction_dict.get("destination_country", "")).strip()
        txn_type = str(transaction_dict.get("transaction_type", "")).strip()
        category = str(transaction_dict.get("merchant_category", "")).strip()
        txn_time = transaction_dict.get("timestamp")
        if isinstance(txn_time, str):
            try:
                txn_time = datetime.fromisoformat(txn_time)
            except Exception:
                txn_time = datetime.utcnow()
        elif not isinstance(txn_time, datetime):
            txn_time = datetime.utcnow()

        # Customer baseline attributes
        baseline_avg = float(customer_dict.get("baseline_avg_amount", 25000.0))
        is_pep = bool(customer_dict.get("is_pep", False))

        # --- Rule 1: High Transaction Value vs Customer Baseline ---
        ratio = amount / max(baseline_avg, 1.0)
        if amount >= 500000.0 or ratio >= 5.0:
            score = 35 if ratio >= 5.0 and amount >= 500000.0 else 30
            rule_results.append(
                EvaluatedRuleResult(
                    rule_id="RULE-AMT-01",
                    rule_name="Unusually Large Transaction vs Historical Baseline",
                    score_contribution=score,
                    severity="HIGH",
                    observed_value=f"₹{amount:,.2f} ({ratio:.1f}x baseline)",
                    threshold_value=f"Threshold ₹5,00,000 or >3.0x baseline (₹{baseline_avg:,.2f})",
                    explanation=(
                        f"Transaction amount of ₹{amount:,.2f} represents a severe {ratio:.1f}x surge "
                        f"over customer historical average baseline of ₹{baseline_avg:,.2f}, surpassing large-value CDD threshold."
                    ),
                    regulatory_ref="REG-AML-01"
                )
            )
        elif ratio >= 2.5:
            rule_results.append(
                EvaluatedRuleResult(
                    rule_id="RULE-AMT-02",
                    rule_name="Moderate Baseline Deviation",
                    score_contribution=15,
                    severity="MEDIUM",
                    observed_value=f"₹{amount:,.2f} ({ratio:.1f}x baseline)",
                    threshold_value=f">2.5x baseline (₹{baseline_avg:,.2f})",
                    explanation=f"Transaction is {ratio:.1f}x above typical customer average.",
                    regulatory_ref="REG-AML-04"
                )
            )

        # --- Rule 2: High-Risk Jurisdiction / Offshore Haven ---
        if dest_country.lower() in HIGH_RISK_JURISDICTIONS:
            rule_results.append(
                EvaluatedRuleResult(
                    rule_id="RULE-GEO-01",
                    rule_name="High-Risk Offshore Secrecy Jurisdiction",
                    score_contribution=32,
                    severity="HIGH",
                    observed_value=dest_country,
                    threshold_value="FATF Grey/Blacklist & Secrecy Havens",
                    explanation=(
                        f"Destination country '{dest_country}' is categorized under High-Risk Secrecy Jurisdictions, "
                        "triggering mandatory Enhanced Due Diligence (EDD) and UBO disclosure."
                    ),
                    regulatory_ref="REG-AML-03"
                )
            )

        # --- Rule 3: Rapid Velocity / Temporal Burst ---
        # Look for transactions within 15 minutes
        short_window_txns = []
        for past_tx in recent_txns:
            if past_tx.get("transaction_id") == transaction_dict.get("transaction_id"):
                continue
            past_time = past_tx.get("timestamp")
            if isinstance(past_time, str):
                try:
                    past_time = datetime.fromisoformat(past_time)
                except Exception:
                    continue
            if isinstance(past_time, datetime):
                diff = abs((txn_time - past_time).total_seconds())
                if diff <= 900:  # 15 minutes
                    short_window_txns.append(past_tx)

        if len(short_window_txns) >= 2:
            burst_count = len(short_window_txns) + 1
            rule_results.append(
                EvaluatedRuleResult(
                    rule_id="RULE-VEL-01",
                    rule_name="High Velocity Burst (Multiple Rapid Transfers)",
                    score_contribution=26,
                    severity="HIGH",
                    observed_value=f"{burst_count} transactions in <15 mins",
                    threshold_value="Max 1 transaction per 15-minute window",
                    explanation=(
                        f"Detected {burst_count} rapid transfers executed within a 15-minute window, "
                        "exhibiting automated fund diversion or urgent layering velocity."
                    ),
                    regulatory_ref="REG-AML-02"
                )
            )
        elif len(short_window_txns) == 1:
            rule_results.append(
                EvaluatedRuleResult(
                    rule_id="RULE-VEL-02",
                    rule_name="Successive Repeated Transfer",
                    score_contribution=12,
                    severity="MEDIUM",
                    observed_value="2 transactions in <15 mins",
                    threshold_value="Standard spacing > 1 hour",
                    explanation="Multiple transfers initiated back-to-back within minutes.",
                    regulatory_ref="REG-AML-02"
                )
            )

        # --- Rule 4: Structuring / Smurfing Threshold Evasion ---
        # Amounts just below ₹50,000 (e.g. 45,000 - 49,999) or below ₹1,00,000 (90,000 - 99,999)
        if (45000.0 <= amount < 50000.0) or (90000.0 <= amount < 100000.0):
            rule_results.append(
                EvaluatedRuleResult(
                    rule_id="RULE-STR-01",
                    rule_name="Structuring / Smurfing Threshold Avoidance",
                    score_contribution=25,
                    severity="HIGH",
                    observed_value=f"₹{amount:,.2f}",
                    threshold_value="INR 50,000 or INR 1,00,000 mandatory reporting limit",
                    explanation=(
                        f"Transfer amount of ₹{amount:,.2f} is calibrated just below official mandatory "
                        "cash/wire reporting threshold, characteristic of intentional structuring."
                    ),
                    regulatory_ref="REG-AML-02"
                )
            )

        # --- Rule 5: Politically Exposed Person (PEP) Elevated Scrutiny ---
        if is_pep and amount >= 200000.0:
            rule_results.append(
                EvaluatedRuleResult(
                    rule_id="RULE-PEP-01",
                    rule_name="Politically Exposed Person (PEP) High-Value Transfer",
                    score_contribution=22,
                    severity="HIGH",
                    observed_value=f"PEP Account: ₹{amount:,.2f}",
                    threshold_value="PEP Transaction Scrutiny Threshold ₹2,00,000",
                    explanation=(
                        f"Customer is designated as a Politically Exposed Person (PEP) initiating a high-value transfer "
                        f"of ₹{amount:,.2f}, requiring documented rationale and MLRO oversight."
                    ),
                    regulatory_ref="REG-AML-05"
                )
            )

        # --- Rule 6: High-Risk Merchant Category & Layering Vehicles ---
        if category.lower() in HIGH_RISK_CATEGORIES:
            rule_results.append(
                EvaluatedRuleResult(
                    rule_id="RULE-CAT-01",
                    rule_name="High-Risk Commercial Category / Layering Vehicle",
                    score_contribution=20,
                    severity="MEDIUM",
                    observed_value=category,
                    threshold_value="Standard Commercial / Retail Category",
                    explanation=(
                        f"Beneficiary category '{category}' represents a recognized high-risk conduit for "
                        "untraced financial transfers and shell company layering."
                    ),
                    regulatory_ref="REG-AML-06"
                )
            )

        # --- Rule 7: International Wire on Domestic Retail Account ---
        if (
            customer_dict.get("account_type", "").lower() == "savings"
            and txn_type.lower() in ["international transfer", "wire transfer", "offshore wire"]
            and dest_country.lower() != "india"
            and amount >= 100000.0
        ):
            rule_results.append(
                EvaluatedRuleResult(
                    rule_id="RULE-COR-01",
                    rule_name="Uncharacteristic Cross-Border Corridor on Retail Account",
                    score_contribution=15,
                    severity="MEDIUM",
                    observed_value=f"Outward {txn_type} to {dest_country}",
                    threshold_value="Domestic Retail Profile Expectation",
                    explanation=(
                        f"Individual retail savings account routing high-value cross-border funds to {dest_country} "
                        "inconsistent with declared customer occupation and KYC profile."
                    ),
                    regulatory_ref="REG-AML-04"
                )
            )

        # Calculate Total Score
        base_score = 8
        rule_points = sum(r.score_contribution for r in rule_results)
        total_score = min(100, base_score + rule_points)

        # Determine Risk Level
        if total_score >= 85:
            risk_level = "CRITICAL"
        elif total_score >= 65:
            risk_level = "HIGH"
        elif total_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Determine Flag status: score >= 60 or at least one HIGH/CRITICAL rule
        has_high_rule = any(r.severity in ["HIGH", "CRITICAL"] for r in rule_results)
        is_flagged = (total_score >= 60) or has_high_rule

        # Concise explainable summary
        if rule_results:
            reasons = [r.explanation for r in rule_results]
            summary = " • ".join(reasons)
        else:
            summary = "Transaction parameters conform to customer historical baseline and standard low-risk indicators."

        return total_score, risk_level, is_flagged, summary, rule_results

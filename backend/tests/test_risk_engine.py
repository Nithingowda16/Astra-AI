from backend.app.rules.risk_engine import RiskEngine
from datetime import datetime, timedelta

def test_high_risk_transaction_flagged():
    customer = {
        "customer_id": "CUST-1008",
        "baseline_avg_amount": 25000.0,
        "is_pep": False,
        "account_type": "Savings",
    }

    # Simulate TXN-1024: 12.5 Lakhs to Cayman Islands
    txn = {
        "transaction_id": "TXN-1024",
        "amount": 1250000.0,
        "destination_country": "Cayman Islands",
        "transaction_type": "International Transfer",
        "merchant_category": "Offshore Holding",
        "timestamp": datetime.utcnow(),
    }

    score, level, flagged, summary, rules = RiskEngine.evaluate_transaction(
        transaction_dict=txn,
        customer_dict=customer,
        recent_customer_transactions=[]
    )

    assert score >= 75
    assert level in ["HIGH", "CRITICAL"]
    assert flagged is True
    assert len(rules) >= 3
    rule_ids = [r.rule_id for r in rules]
    assert "RULE-AMT-01" in rule_ids
    assert "RULE-GEO-01" in rule_ids
    assert "RULE-CAT-01" in rule_ids

def test_normal_transaction_low_risk():
    customer = {
        "customer_id": "CUST-1002",
        "baseline_avg_amount": 15000.0,
        "is_pep": False,
        "account_type": "Savings",
    }
    txn = {
        "transaction_id": "TXN-2001",
        "amount": 4200.0,
        "destination_country": "India",
        "transaction_type": "Card",
        "merchant_category": "Groceries",
        "timestamp": datetime.utcnow(),
    }

    score, level, flagged, summary, rules = RiskEngine.evaluate_transaction(
        transaction_dict=txn,
        customer_dict=customer,
        recent_customer_transactions=[]
    )

    assert score < 40
    assert level == "LOW"
    assert flagged is False
    assert len(rules) == 0

def test_smurfing_structuring_rule():
    customer = {
        "customer_id": "CUST-1003",
        "baseline_avg_amount": 30000.0,
        "is_pep": False,
        "account_type": "Current",
    }
    txn = {
        "transaction_id": "TXN-3001",
        "amount": 49500.0, # Just below 50,000 threshold
        "destination_country": "India",
        "transaction_type": "Wire Transfer",
        "merchant_category": "Consulting",
        "timestamp": datetime.utcnow(),
    }

    score, level, flagged, summary, rules = RiskEngine.evaluate_transaction(
        transaction_dict=txn,
        customer_dict=customer,
        recent_customer_transactions=[]
    )

    rule_ids = [r.rule_id for r in rules]
    assert "RULE-STR-01" in rule_ids
    assert flagged is True

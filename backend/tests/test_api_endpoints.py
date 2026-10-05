from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

# Obtain valid analyst token for protected endpoints
_login_res = client.post("/api/auth/login", json={
    "username_or_email": "analyst",
    "password": "UserPassword123!"
})
_token = _login_res.json()["access_token"]
client.headers = {"Authorization": f"Bearer {_token}"}

def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_dashboard_stats():
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["total_transactions"] > 0
    assert data["suspicious_transactions"] > 0
    assert "risk_distribution" in data
    assert len(data["recent_alerts"]) > 0

def test_transactions_list_and_detail():
    # List
    res = client.get("/api/transactions?risk_level=CRITICAL")
    assert res.status_code == 200
    txns = res.json()
    assert len(txns) > 0

    # Specific TXN-1024
    res_detail = client.get("/api/transactions/TXN-1024")
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert detail["transaction_id"] == "TXN-1024"
    assert detail["destination_country"] == "Cayman Islands"
    assert detail["is_flagged"] is True
    assert len(detail["evaluations"]) > 0
    assert any("RULE-AMT" in ev["rule_id"] for ev in detail["evaluations"])

def test_customer_detail_and_timeline():
    res = client.get("/api/customers/CUST-1008")
    assert res.status_code == 200
    data = res.json()
    assert data["customer_id"] == "CUST-1008"
    assert data["full_name"] == "Vikramaditya Singhania"
    assert len(data["timeline"]) > 0
    assert data["flagged_transaction_count"] > 0

def test_regulatory_rules():
    res = client.get("/api/regulatory/rules")
    assert res.status_code == 200
    rules = res.json()
    assert len(rules) >= 6
    doc_ids = [r["doc_id"] for r in rules]
    assert "REG-AML-01" in doc_ids
    assert "REG-AML-03" in doc_ids

def test_copilot_queries():
    # Query 1: Why flagged
    res = client.post("/api/copilot/query", json={"query": "Why was transaction TXN-1024 flagged?"})
    assert res.status_code == 200
    data = res.json()
    assert data["data_found"] is True
    assert "TXN-1024" in data["answer"]
    assert len(data["supporting_evidence"]) > 0

    # Query 2: High risk customer
    res2 = client.post("/api/copilot/query", json={"query": "What are the main risk indicators for customer CUST-1008?"})
    assert res2.status_code == 200
    assert res2.json()["data_found"] is True

    # Query 3: Unknown query fallback
    res3 = client.post("/api/copilot/query", json={"query": "What is the capital of Mars?"})
    assert res3.status_code == 200
    assert "Insufficient data available" in res3.json()["answer"]

def test_investigation_report():
    res = client.get("/api/investigations/INV-2024-008/report")
    assert res.status_code == 200
    data = res.json()
    assert data["investigation_id"] == "INV-2024-008"
    assert "customer" in data
    assert len(data["regulatory_citations"]) > 0
    assert "compliance_recommendation" in data

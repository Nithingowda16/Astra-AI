from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_unauthenticated_access_blocked():
    """Confirms no unauthorized access is permitted to protected compliance endpoints."""
    res_dash = client.get("/api/dashboard/stats")
    assert res_dash.status_code == 401
    assert "Authentication required" in res_dash.json()["detail"]

    res_txns = client.get("/api/transactions")
    assert res_txns.status_code == 401

    res_alerts = client.get("/api/alerts")
    assert res_alerts.status_code == 401

def test_user_analyst_login_and_access():
    """Tests Analyst login, token acquisition, data access, and admin barrier."""
    login_res = client.post("/api/auth/login", json={
        "username_or_email": "analyst",
        "password": "UserPassword123!",
        "required_role": "user"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert "access_token" in login_data
    assert login_data["user"]["role"] == "user"

    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Protected dashboard works with token
    dash_res = client.get("/api/dashboard/stats", headers=headers)
    assert dash_res.status_code == 200
    assert dash_res.json()["total_transactions"] > 0

    # Analyst cannot access admin endpoints (403 Forbidden)
    admin_res = client.get("/api/auth/admin/users", headers=headers)
    assert admin_res.status_code == 403
    assert "Administrative privileges required" in admin_res.json()["detail"]

def test_admin_login_and_privileges():
    """Tests Admin login and administrative control endpoints."""
    login_res = client.post("/api/auth/login", json={
        "username_or_email": "admin",
        "password": "AdminPassword123!",
        "required_role": "admin"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert login_data["user"]["role"] == "admin"

    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Admin can list all users
    users_res = client.get("/api/auth/admin/users", headers=headers)
    assert users_res.status_code == 200
    users = users_res.json()
    assert len(users) >= 2

    # Admin can view compliance audit logs
    audit_res = client.get("/api/auth/admin/audit", headers=headers)
    assert audit_res.status_code == 200
    assert len(audit_res.json()) > 0

def test_portal_separation_gate():
    """Tests that analyst credentials cannot be used to breach the Admin portal."""
    # Analyst tries to breach Admin portal
    breach_res = client.post("/api/auth/login", json={
        "username_or_email": "analyst",
        "password": "UserPassword123!",
        "required_role": "admin"
    })
    assert breach_res.status_code == 403
    assert "reserved for System Administrators" in breach_res.json()["detail"]

def test_user_registration_flow():
    """Tests user sign up / registration flow."""
    import uuid
    uid = uuid.uuid4().hex[:6]
    test_user = f"user_{uid}"
    test_email = f"user_{uid}@demo.in"

    reg_res = client.post("/api/auth/register", json={
        "username": test_user,
        "email": test_email,
        "full_name": "Test Investigator",
        "password": "PasswordSecure123!",
        "role": "user"
    })
    assert reg_res.status_code == 201
    data = reg_res.json()
    assert data["user"]["username"] == test_user
    assert data["user"]["role"] == "user"
    assert "access_token" in data

    # Duplicate username should be rejected
    dup_res = client.post("/api/auth/register", json={
        "username": test_user,
        "email": f"other_{uid}@demo.in",
        "full_name": "Test Investigator",
        "password": "PasswordSecure123!",
        "role": "user"
    })
    assert dup_res.status_code == 400


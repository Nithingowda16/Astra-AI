"""
Synthetic Seed Data Generator
Generates realistic compliance, customer, transaction, alert, and regulatory data.
"""

from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal, Base, engine
from backend.app.models.customer import Customer
from backend.app.models.transaction import Transaction
from backend.app.models.rule_evaluation import RuleEvaluation
from backend.app.models.alert import Alert
from backend.app.models.investigation import Investigation
from backend.app.models.regulatory_doc import RegulatoryDoc
from backend.app.models.user import User, AuditLog
from backend.app.core.security import hash_password
from backend.app.regulatory.demo_knowledge_base import DEMO_REGULATORY_RULES
from backend.app.rules.risk_engine import RiskEngine

CUSTOMERS_DATA = [
    {
        "customer_id": "CUST-1008",
        "full_name": "Vikramaditya Singhania",
        "email": "v.singhania@tradehorizon-demo.com",
        "phone": "+91 98201 44521",
        "country": "India",
        "occupation": "Import-Export Director",
        "account_type": "Savings",
        "kyc_status": "Enhanced Due Diligence",
        "baseline_avg_amount": 28000.0,
        "baseline_monthly_volume": 180000.0,
        "risk_score": 88,
        "risk_level": "HIGH",
        "is_pep": False,
        "days_ago": 420
    },
    {
        "customer_id": "CUST-1003",
        "full_name": "Devendra Patil",
        "email": "dev.patil@finconsult-demo.in",
        "phone": "+91 94451 88920",
        "country": "India",
        "occupation": "Financial Broker",
        "account_type": "Savings",
        "kyc_status": "Verified",
        "baseline_avg_amount": 35000.0,
        "baseline_monthly_volume": 150000.0,
        "risk_score": 78,
        "risk_level": "HIGH",
        "is_pep": False,
        "days_ago": 310
    },
    {
        "customer_id": "CUST-1004",
        "full_name": "Hon. Rameshwar Prasad",
        "email": "r.prasad@publicaffairs-demo.gov.in",
        "phone": "+91 98111 23001",
        "country": "India",
        "occupation": "Legislative Committee Member",
        "account_type": "Current",
        "kyc_status": "Enhanced Due Diligence",
        "baseline_avg_amount": 80000.0,
        "baseline_monthly_volume": 600000.0,
        "risk_score": 82,
        "risk_level": "HIGH",
        "is_pep": True,
        "days_ago": 600
    },
    {
        "customer_id": "CUST-1005",
        "full_name": "Global Trade Nexus LLC",
        "email": "finance@globalnexus-demo.com",
        "phone": "+91 22 6678 9000",
        "country": "India",
        "occupation": "Logistics & Cross-Border Commodity",
        "account_type": "Corporate",
        "kyc_status": "Verified",
        "baseline_avg_amount": 120000.0,
        "baseline_monthly_volume": 1500000.0,
        "risk_score": 68,
        "risk_level": "MEDIUM",
        "is_pep": False,
        "days_ago": 720
    },
    {
        "customer_id": "CUST-1001",
        "full_name": "Ananya Sharma",
        "email": "ananya.sharma@techcloud-demo.io",
        "phone": "+91 97112 34567",
        "country": "India",
        "occupation": "Lead Cloud Architect",
        "account_type": "Savings",
        "kyc_status": "Verified",
        "baseline_avg_amount": 18000.0,
        "baseline_monthly_volume": 95000.0,
        "risk_score": 12,
        "risk_level": "LOW",
        "is_pep": False,
        "days_ago": 500
    },
    {
        "customer_id": "CUST-1002",
        "full_name": "Rajesh Kumar Gupta",
        "email": "rajesh.gupta@guptatraders-demo.in",
        "phone": "+91 98223 99881",
        "country": "India",
        "occupation": "Wholesale Electronics Merchant",
        "account_type": "Current",
        "kyc_status": "Verified",
        "baseline_avg_amount": 65000.0,
        "baseline_monthly_volume": 480000.0,
        "risk_score": 24,
        "risk_level": "LOW",
        "is_pep": False,
        "days_ago": 850
    },
    {
        "customer_id": "CUST-1006",
        "full_name": "Dr. Priya Sundaram",
        "email": "dr.priya@cardiohealth-demo.org",
        "phone": "+91 98400 12345",
        "country": "India",
        "occupation": "Chief Cardiologist",
        "account_type": "Savings",
        "kyc_status": "Verified",
        "baseline_avg_amount": 32000.0,
        "baseline_monthly_volume": 180000.0,
        "risk_score": 15,
        "risk_level": "LOW",
        "is_pep": False,
        "days_ago": 620
    },
    {
        "customer_id": "CUST-1007",
        "full_name": "Apex Logistics Corridors",
        "email": "operations@apexlogistics-demo.com",
        "phone": "+91 44 2828 4400",
        "country": "India",
        "occupation": "Maritime Freight Transit",
        "account_type": "Corporate",
        "kyc_status": "Verified",
        "baseline_avg_amount": 250000.0,
        "baseline_monthly_volume": 2800000.0,
        "risk_score": 32,
        "risk_level": "LOW",
        "is_pep": False,
        "days_ago": 900
    },
    {
        "customer_id": "CUST-1009",
        "full_name": "Siddharth Verma",
        "email": "siddharth.v@retailpoint-demo.com",
        "phone": "+91 99100 88776",
        "country": "India",
        "occupation": "E-Commerce Merchant",
        "account_type": "Current",
        "kyc_status": "Verified",
        "baseline_avg_amount": 42000.0,
        "baseline_monthly_volume": 320000.0,
        "risk_score": 54,
        "risk_level": "MEDIUM",
        "is_pep": False,
        "days_ago": 350
    },
    {
        "customer_id": "CUST-1010",
        "full_name": "Kavita Mehra",
        "email": "kavita.mehra@designstudio-demo.in",
        "phone": "+91 98711 00223",
        "country": "India",
        "occupation": "Architectural Designer",
        "account_type": "Savings",
        "kyc_status": "Verified",
        "baseline_avg_amount": 29000.0,
        "baseline_monthly_volume": 140000.0,
        "risk_score": 18,
        "risk_level": "LOW",
        "is_pep": False,
        "days_ago": 410
    }
]

def seed_database(db: Session):
    print("Beginning database seeding...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # 1. Seed Demo Regulatory Knowledge Base
    if db.query(RegulatoryDoc).count() == 0:
        for reg in DEMO_REGULATORY_RULES:
            doc = RegulatoryDoc(
                doc_id=reg["doc_id"],
                title=reg["title"],
                authority=reg["authority"],
                category=reg["category"],
                summary=reg["summary"],
                full_clause=reg["full_clause"],
                monitored_scenarios=reg["monitored_scenarios"],
                recommended_compliance_action=reg["recommended_compliance_action"],
                disclaimer=reg["disclaimer"]
            )
            db.add(doc)
        db.commit()
        print(f"Seeded {len(DEMO_REGULATORY_RULES)} Demo Regulatory Documents.")

    # 2. Seed Customers
    now = datetime.utcnow()
    customers_map = {}
    for c_data in CUSTOMERS_DATA:
        existing = db.query(Customer).filter_by(customer_id=c_data["customer_id"]).first()
        if not existing:
            cust = Customer(
                customer_id=c_data["customer_id"],
                full_name=c_data["full_name"],
                email=c_data["email"],
                phone=c_data["phone"],
                country=c_data["country"],
                occupation=c_data["occupation"],
                account_type=c_data["account_type"],
                account_opened_date=now - timedelta(days=c_data["days_ago"]),
                kyc_status=c_data["kyc_status"],
                baseline_avg_amount=c_data["baseline_avg_amount"],
                baseline_monthly_volume=c_data["baseline_monthly_volume"],
                risk_score=c_data["risk_score"],
                risk_level=c_data["risk_level"],
                is_pep=c_data["is_pep"],
                created_at=now - timedelta(days=c_data["days_ago"])
            )
            db.add(cust)
            customers_map[c_data["customer_id"]] = c_data
        else:
            customers_map[c_data["customer_id"]] = c_data
    db.commit()
    print(f"Seeded {len(CUSTOMERS_DATA)} Customers.")

    # 3. Create transactions
    # Avoid duplicating if already seeded
    if db.query(Transaction).count() > 10:
        print("Database already contains transaction records. Skipping transaction seeding.")
        return

    transactions_to_add = []

    # Case A: TXN-1024 - Flagship Demo Transaction for Vikramaditya Singhania (CUST-1008)
    txn_1024_time = now - timedelta(hours=3, minutes=15)
    txn_1024 = {
        "transaction_id": "TXN-1024",
        "customer_id": "CUST-1008",
        "timestamp": txn_1024_time,
        "amount": 1250000.0,
        "currency": "INR",
        "source_country": "India",
        "destination_country": "Cayman Islands",
        "transaction_type": "International Transfer",
        "merchant_category": "Offshore Holding",
        "status": "Flagged"
    }
    transactions_to_add.append(txn_1024)

    # Follow-on rapid transaction for CUST-1008: TXN-1025
    txn_1025_time = txn_1024_time + timedelta(minutes=11)
    txn_1025 = {
        "transaction_id": "TXN-1025",
        "customer_id": "CUST-1008",
        "timestamp": txn_1025_time,
        "amount": 680000.0,
        "currency": "INR",
        "source_country": "India",
        "destination_country": "Panama",
        "transaction_type": "International Transfer",
        "merchant_category": "Offshore Holding",
        "status": "Flagged"
    }
    transactions_to_add.append(txn_1025)

    # Historic normal transactions for CUST-1008 to establish baseline
    for i, amt in enumerate([24500.0, 18900.0, 31200.0, 27400.0, 33000.0]):
        transactions_to_add.append({
            "transaction_id": f"TXN-101{i}",
            "customer_id": "CUST-1008",
            "timestamp": now - timedelta(days=20 - (i * 3), hours=random.randint(1, 10)),
            "amount": amt,
            "currency": "INR",
            "source_country": "India",
            "destination_country": "India",
            "transaction_type": "Card",
            "merchant_category": "Domestic Retail",
            "status": "Completed"
        })

    # Case B: Smurfing Cluster for Devendra Patil (CUST-1003)
    smurf_base_time = now - timedelta(hours=8)
    for idx, s_amt in enumerate([49500.0, 49200.0, 48900.0, 49800.0]):
        transactions_to_add.append({
            "transaction_id": f"TXN-103{idx+1}",
            "customer_id": "CUST-1003",
            "timestamp": smurf_base_time + timedelta(minutes=idx * 14),
            "amount": s_amt,
            "currency": "INR",
            "source_country": "India",
            "destination_country": "India",
            "transaction_type": "Wire Transfer",
            "merchant_category": "Consulting Services",
            "status": "Flagged"
        })

    # Case C: PEP High-Value Transfer for Hon. Rameshwar Prasad (CUST-1004)
    transactions_to_add.append({
        "transaction_id": "TXN-1040",
        "customer_id": "CUST-1004",
        "timestamp": now - timedelta(days=1, hours=5),
        "amount": 850000.0,
        "currency": "INR",
        "source_country": "India",
        "destination_country": "Switzerland",
        "transaction_type": "Wire Transfer",
        "merchant_category": "Private Wealth Conduit",
        "status": "Flagged"
    })

    # Case D: High-Volume Pass-Through for Global Trade Nexus (CUST-1005)
    transactions_to_add.append({
        "transaction_id": "TXN-1051",
        "customer_id": "CUST-1005",
        "timestamp": now - timedelta(days=2, hours=10),
        "amount": 1850000.0,
        "currency": "INR",
        "source_country": "India",
        "destination_country": "Vanuatu",
        "transaction_type": "International Transfer",
        "merchant_category": "Casino/Gambling",
        "status": "Flagged"
    })

    # Realistic background transactions for remaining customers across past 30 days
    retail_merchants = ["Groceries", "Cloud Services", "Electronics", "Airline Tickets", "Medical Supplies", "Office Equipment", "Utilities"]
    retail_cust_ids = ["CUST-1001", "CUST-1002", "CUST-1006", "CUST-1007", "CUST-1009", "CUST-1010"]

    txn_counter = 1100
    for day in range(30, 0, -1):
        num_day_txns = random.randint(2, 5)
        for _ in range(num_day_txns):
            cid = random.choice(retail_cust_ids)
            c_meta = customers_map.get(cid, {})
            base_amt = c_meta.get("baseline_avg_amount", 25000.0)
            amt = round(max(500.0, random.gauss(base_amt, base_amt * 0.35)), 2)
            dest = "India"
            cat = random.choice(retail_merchants)
            ttype = random.choice(["Card", "Wire Transfer", "UPI/Direct Transfer"])

            transactions_to_add.append({
                "transaction_id": f"TXN-{txn_counter}",
                "customer_id": cid,
                "timestamp": now - timedelta(days=day, hours=random.randint(0, 23), minutes=random.randint(0, 59)),
                "amount": amt,
                "currency": "INR",
                "source_country": "India",
                "destination_country": dest,
                "transaction_type": ttype,
                "merchant_category": cat,
                "status": "Completed"
            })
            txn_counter += 1

    # Sort transactions chronologically
    transactions_to_add.sort(key=lambda x: x["timestamp"])

    # Now evaluate all transactions through the RiskEngine and persist to database
    # Keep track of recent transactions per customer for velocity calculation
    customer_history = {}

    for t_data in transactions_to_add:
        cid = t_data["customer_id"]
        c_meta = customers_map.get(cid, {
            "baseline_avg_amount": 25000.0,
            "is_pep": False,
            "account_type": "Savings"
        })
        recent_txs = customer_history.get(cid, [])

        score, level, flagged, summary, rule_results = RiskEngine.evaluate_transaction(
            transaction_dict=t_data,
            customer_dict=c_meta,
            recent_customer_transactions=recent_txs
        )

        txn = Transaction(
            transaction_id=t_data["transaction_id"],
            customer_id=cid,
            timestamp=t_data["timestamp"],
            amount=t_data["amount"],
            currency=t_data["currency"],
            source_country=t_data["source_country"],
            destination_country=t_data["destination_country"],
            transaction_type=t_data["transaction_type"],
            merchant_category=t_data["merchant_category"],
            status="Flagged" if flagged else "Completed",
            risk_score=score,
            risk_level=level,
            is_flagged=flagged,
            flagged_reason_summary=summary
        )
        db.add(txn)

        # Store rule evaluations
        for r_res in rule_results:
            eval_id = f"EVAL-{t_data['transaction_id']}-{r_res.rule_id}"
            db_eval = RuleEvaluation(
                evaluation_id=eval_id,
                transaction_id=t_data["transaction_id"],
                rule_id=r_res.rule_id,
                rule_name=r_res.rule_name,
                score_contribution=r_res.score_contribution,
                severity=r_res.severity,
                observed_value=r_res.observed_value,
                threshold_value=r_res.threshold_value,
                explanation=r_res.explanation,
                regulatory_ref=r_res.regulatory_ref
            )
            db.add(db_eval)

        # If flagged, generate an Alert
        if flagged:
            alert_id = f"ALT-{t_data['transaction_id']}"
            first_rule = rule_results[0].rule_name if rule_results else "Risk Threshold Exceeded"
            alert = Alert(
                alert_id=alert_id,
                transaction_id=t_data["transaction_id"],
                customer_id=cid,
                alert_type=first_rule,
                severity=level,
                status="New",
                risk_score=score,
                details=summary,
                created_at=t_data["timestamp"]
            )
            db.add(alert)

        # Update customer history buffer
        if cid not in customer_history:
            customer_history[cid] = []
        customer_history[cid].append(t_data)

    db.commit()
    print(f"Seeded and evaluated {len(transactions_to_add)} transactions.")

    # 4. Seed Seed-Case Investigation for CUST-1008
    inv_id = "INV-2024-008"
    existing_inv = db.query(Investigation).filter_by(investigation_id=inv_id).first()
    if not existing_inv:
        sample_inv = Investigation(
            investigation_id=inv_id,
            title="High-Value Offshore Diversion Scrutiny - Singhania Corridors",
            customer_id="CUST-1008",
            primary_transaction_id="TXN-1024",
            status="Under Review",
            priority="Critical",
            assigned_analyst="Senior Compliance Officer - Priya Nair",
            summary=(
                "Account CUST-1008 executed a ₹12,50,000 transfer to Cayman Islands (TXN-1024), "
                "representing a 44x surge over historic average baseline, closely followed by a ₹6,80,000 transfer to Panama. "
                "Triggered Demo AML Rule 01 (Large Value CDD) and Demo AML Rule 03 (High-Risk Jurisdiction)."
            ),
            analyst_notes=(
                "• 2026-09-30 09:45 - Case initiated automatically upon alert generation ALT-TXN-1024.\n"
                "• 2026-09-30 10:15 - Analyst review: Beneficiary identified as Cayman Islands holding entity. No trade invoice attached.\n"
                "• 2026-09-30 11:30 - Customer relationship manager contacted for source of funds and business justification."
            ),
            findings=(
                "1. Total flagged volume: ₹19,30,000 across 2 cross-border transfers within 15 minutes.\n"
                "2. Customer occupation declared as retail import-export, but account classified as personal savings.\n"
                "3. Involves two FATF-monitored secrecy tax havens (Cayman Islands, Panama)."
            ),
            evidence_links="TXN-1024, TXN-1025, REG-AML-01, REG-AML-03",
            created_at=now - timedelta(hours=2),
            updated_at=now - timedelta(minutes=45)
        )
        db.add(sample_inv)
        db.commit()
        print("Seeded baseline investigation INV-2024-008.")

    # 5. Seed Security Accounts (Admin & Analyst)
    if db.query(User).count() == 0:
        admin_pwd, admin_salt = hash_password("AdminPassword123!")
        admin_user = User(
            username="admin",
            email="admin@compliance.ai",
            full_name="Chief Compliance Officer",
            hashed_password=admin_pwd,
            salt=admin_salt,
            role="admin",
            is_active=True,
            created_at=now - timedelta(days=30),
            last_login=now - timedelta(hours=1)
        )
        analyst_pwd, analyst_salt = hash_password("UserPassword123!")
        analyst_user = User(
            username="analyst",
            email="analyst@compliance.ai",
            full_name="Senior Risk Analyst",
            hashed_password=analyst_pwd,
            salt=analyst_salt,
            role="user",
            is_active=True,
            created_at=now - timedelta(days=20),
            last_login=now - timedelta(hours=2)
        )
        db.add(admin_user)
        db.add(analyst_user)
        
        # Initial audit log entries
        db.add(AuditLog(
            timestamp=now - timedelta(days=30),
            username="system",
            action="SYSTEM_INIT",
            role="admin",
            status="SUCCESS",
            details="Enterprise compliance security engine initialized with RBAC"
        ))
        db.add(AuditLog(
            timestamp=now - timedelta(hours=2),
            username="analyst",
            action="LOGIN",
            role="user",
            status="SUCCESS",
            details="Analyst logged in to review AML flag TXN-1024"
        ))
        db.add(AuditLog(
            timestamp=now - timedelta(hours=1),
            username="admin",
            action="LOGIN",
            role="admin",
            status="SUCCESS",
            details="Admin logged in to audit suspicious transactions"
        ))
        db.commit()
        print("Seeded baseline security users and audit logs.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

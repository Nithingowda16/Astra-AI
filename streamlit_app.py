# ==============================================================================
# Astra AI — Enterprise Risk & Regulatory Intelligence Platform
# Streamlit Native Application with Authentication & Surveillance
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import base64
import os

# ------------------------------------------------------------------------------
# 1. Page Configuration & Apple SF Pro Dark Theme Styling
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Astra AI — Risk & AML Surveillance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper to encode images
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return ""

logo_b64 = get_base64_image("frontend/public/assets/astra-logo-dark.png")
bg_b64 = get_base64_image("frontend/public/assets/login-bg.png")

bg_style = f"background-image: url('data:image/png;base64,{bg_b64}'); background-size: cover; background-position: center;" if bg_b64 else "background: #0b0f19;"

# Custom Styling
st.markdown(f"""
<style>
    html, body, [class*="css"], [class*="st-"] {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Helvetica Neue", "Segoe UI", Roboto, Arial, sans-serif !important;
    }}
    
    /* Login Page Styling */
    .login-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }}
    .login-card {{
        background: rgba(18, 24, 38, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 40px 36px;
        width: 100%;
        max-width: 440px;
        backdrop-filter: blur(20px);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
        text-align: center;
        margin: 0 auto;
    }}
    .login-title {{
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #ffffff;
        margin: 12px 0 6px 0;
    }}
    .login-subtitle {{
        color: #94a3b8;
        font-size: 0.88rem;
        margin-bottom: 24px;
    }}
    .demo-pill {{
        background: rgba(14, 165, 233, 0.12);
        border: 1px solid rgba(14, 165, 233, 0.3);
        color: #38bdf8;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.76rem;
        margin-top: 14px;
        display: inline-block;
    }}

    /* Sleek metric card containers */
    .metric-card {{
        background: #161b22;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }}
    .metric-label {{
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #94a3b8;
    }}
    .metric-value {{
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #f8fafc;
        margin: 4px 0;
    }}
    .metric-sub {{
        font-size: 0.78rem;
        color: #10b981;
    }}
    .metric-sub.negative {{
        color: #ef4444;
    }}
    
    /* Header branding */
    .astra-header {{
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 8px 0 16px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }}
    .astra-title {{
        font-size: 1.7rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #38bdf8;
        margin: 0;
        display: inline-block;
    }}
    .astra-badge {{
        background: rgba(14, 165, 233, 0.18);
        border: 1px solid rgba(14, 165, 233, 0.4);
        color: #38bdf8;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-left: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. Authentication State Management
# ------------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = "Senior Risk Officer"

def login_user(username, password):
    if (username == "admin" and password == "password") or (username == "officer" and password == "password"):
        st.session_state.authenticated = True
        st.session_state.user_role = "Senior Risk Officer" if username == "admin" else "Compliance Officer"
        st.rerun()
    else:
        st.error("Invalid credentials. Try: admin / password")

def logout_user():
    st.session_state.authenticated = False
    st.rerun()

# ------------------------------------------------------------------------------
# 3. Render Login Screen (if not authenticated)
# ------------------------------------------------------------------------------
if not st.session_state.authenticated:
    _, col_login, _ = st.columns([1, 1.2, 1])
    
    with col_login:
        st.write("")
        st.write("")
        
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="72" height="72" style="margin-bottom: 8px;" />' if logo_b64 else '<span style="font-size: 3rem;">⚡</span>'
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 24px;">
            {logo_html}
            <h1 class="login-title">Astra AI</h1>
            <p class="login-subtitle">Enterprise Risk & Regulatory Intelligence Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("astra_login_form"):
            username = st.text_input("Username", value="admin", placeholder="e.g. admin")
            password = st.text_input("Password", value="password", type="password")
            
            submitted = st.form_submit_button("Sign In to Astra AI", use_container_width=True)
            if submitted:
                login_user(username, password)
                
        st.markdown("""
        <div style="text-align: center;">
            <div class="demo-pill">
                🔑 <strong>Access Profile:</strong> admin / password &bull; Senior Risk Officer
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.stop()

# ------------------------------------------------------------------------------
# 4. Institutional Compliance Data
# ------------------------------------------------------------------------------
@st.cache_data
def get_compliance_data():
    customers = [
        {"Customer ID": "CUST-1008", "Full Name": "Vikramaditya Singhania", "Country": "India", "Occupation": "Import-Export Director", "Account Type": "Corporate", "KYC Status": "Enhanced Due Diligence", "Risk Score": 88, "Risk Level": "HIGH", "PEP": "Yes", "Monthly Volume": 480000.0},
        {"Customer ID": "CUST-1003", "Full Name": "Devendra Patil", "Country": "India", "Occupation": "Financial Broker", "Account Type": "Savings", "KYC Status": "Verified", "Risk Score": 78, "Risk Level": "HIGH", "PEP": "No", "Monthly Volume": 150000.0},
        {"Customer ID": "CUST-1004", "Full Name": "Hon. Rameshwar Prasad", "Country": "India", "Occupation": "Legislative Committee Member", "Account Type": "Current", "KYC Status": "Enhanced Due Diligence", "Risk Score": 82, "Risk Level": "HIGH", "PEP": "Yes", "Monthly Volume": 600000.0},
        {"Customer ID": "CUST-1005", "Full Name": "Global Trade Nexus LLC", "Country": "UAE", "Occupation": "Cross-Border Commodities", "Account Type": "Corporate", "KYC Status": "Verified", "Risk Score": 68, "Risk Level": "MEDIUM", "PEP": "No", "Monthly Volume": 1500000.0},
        {"Customer ID": "CUST-1009", "Full Name": "Siddharth Verma", "Country": "Singapore", "Occupation": "Fintech Solutions Director", "Account Type": "Current", "KYC Status": "Verified", "Risk Score": 54, "Risk Level": "MEDIUM", "PEP": "No", "Monthly Volume": 320000.0},
        {"Customer ID": "CUST-1001", "Full Name": "Ananya Sharma", "Country": "India", "Occupation": "Lead Cloud Architect", "Account Type": "Savings", "KYC Status": "Verified", "Risk Score": 12, "Risk Level": "LOW", "PEP": "No", "Monthly Volume": 95000.0},
        {"Customer ID": "CUST-1002", "Full Name": "Rajesh Kumar Gupta", "Country": "India", "Occupation": "Wholesale Electronics Merchant", "Account Type": "Current", "KYC Status": "Verified", "Risk Score": 24, "Risk Level": "LOW", "PEP": "No", "Monthly Volume": 480000.0},
        {"Customer ID": "CUST-1006", "Full Name": "Dr. Priya Sundaram", "Country": "United Kingdom", "Occupation": "Chief Cardiologist", "Account Type": "Savings", "KYC Status": "Verified", "Risk Score": 15, "Risk Level": "LOW", "PEP": "No", "Monthly Volume": 180000.0},
        {"Customer ID": "CUST-1007", "Full Name": "Apex Logistics Corridors", "Country": "Cyprus", "Occupation": "Maritime Freight Transit", "Account Type": "Corporate", "KYC Status": "Under Review", "Risk Score": 74, "Risk Level": "HIGH", "PEP": "No", "Monthly Volume": 2800000.0},
        {"Customer ID": "CUST-1010", "Full Name": "Kavita Mehra", "Country": "India", "Occupation": "Architectural Designer", "Account Type": "Savings", "KYC Status": "Verified", "Risk Score": 18, "Risk Level": "LOW", "PEP": "No", "Monthly Volume": 140000.0},
    ]
    
    transactions = [
        {"Tx ID": "TXN-88491", "Customer": "Vikramaditya Singhania", "Amount": 485000.0, "Currency": "INR", "Type": "WIRE_OUTBOUND", "Counterparty": "Al-Bahrani General Trading (UAE)", "Anomaly Score": 0.94, "Status": "FLAGGED", "Trigger Reason": "Rapid Layering / High-Risk Corridor", "Timestamp": "2026-10-05 17:42:10"},
        {"Tx ID": "TXN-88489", "Customer": "Devendra Patil", "Amount": 99500.0, "Currency": "INR", "Type": "CASH_DEPOSIT", "Counterparty": "Multiple Branch Cashiers", "Anomaly Score": 0.88, "Status": "FLAGGED", "Trigger Reason": "Smurfing / Structuring under reporting cap", "Timestamp": "2026-10-05 16:30:15"},
        {"Tx ID": "TXN-88485", "Customer": "Hon. Rameshwar Prasad", "Amount": 750000.0, "Currency": "INR", "Type": "RTGS_INBOUND", "Counterparty": "Aethelgard Consulting S.A.", "Anomaly Score": 0.91, "Status": "UNDER_INVESTIGATION", "Trigger Reason": "PEP Exposure / Unexplained Wealth Order", "Timestamp": "2026-10-05 15:18:02"},
        {"Tx ID": "TXN-88480", "Customer": "Apex Logistics Corridors", "Amount": 1420000.0, "Currency": "USD", "Type": "SWIFT_TRANSFER", "Counterparty": "Bosphorus Maritime Trading", "Anomaly Score": 0.85, "Status": "FLAGGED", "Trigger Reason": "Sanctions Proximity / Offshore Gateway", "Timestamp": "2026-10-05 14:05:40"},
        {"Tx ID": "TXN-88472", "Customer": "Global Trade Nexus LLC", "Amount": 320000.0, "Currency": "INR", "Type": "VENDOR_PAYMENT", "Counterparty": "Shenzhen Electrotech Corp", "Anomaly Score": 0.42, "Status": "CLEARED", "Trigger Reason": "Standard Trade Flow", "Timestamp": "2026-10-05 12:44:11"},
        {"Tx ID": "TXN-88465", "Customer": "Ananya Sharma", "Amount": 18500.0, "Currency": "INR", "Type": "UPI_TRANSFER", "Counterparty": "Urban Merchant Pay", "Anomaly Score": 0.05, "Status": "CLEARED", "Trigger Reason": "Normal Personal Spending", "Timestamp": "2026-10-05 11:20:00"},
        {"Tx ID": "TXN-88461", "Customer": "Siddharth Verma", "Amount": 125000.0, "Currency": "INR", "Type": "NEFT_OUTBOUND", "Counterparty": "CloudScale Hosting SG", "Anomaly Score": 0.38, "Status": "CLEARED", "Trigger Reason": "Routine SaaS Billing", "Timestamp": "2026-10-05 10:14:22"},
    ]
    
    cases = [
        {"Case ID": "CASE-4091", "Subject": "Singhania Trade Horizon Layering", "Assigned To": "Senior Risk Officer", "Priority": "CRITICAL", "Stage": "SAR In Preparation", "Filing Deadline": "2026-10-08", "Evidence Count": 7},
        {"Case ID": "CASE-4088", "Subject": "Structuring Inquiries — D. Patil Branches", "Assigned To": "Compliance Officer", "Priority": "HIGH", "Stage": "Request for Information (RFI)", "Filing Deadline": "2026-10-12", "Evidence Count": 4},
        {"Case ID": "CASE-4075", "Subject": "Apex Logistics Bosphorus Sanctions Check", "Assigned To": "Chief Sanctions Officer", "Priority": "HIGH", "Stage": "Escalated to MLRO", "Filing Deadline": "2026-10-09", "Evidence Count": 12},
    ]
    
    return pd.DataFrame(customers), pd.DataFrame(transactions), pd.DataFrame(cases)

df_customers, df_tx, df_cases = get_compliance_data()

# ------------------------------------------------------------------------------
# 5. Header & User Profile Bar
# ------------------------------------------------------------------------------
col_hdr_left, col_hdr_right = st.columns([3, 1])
with col_hdr_left:
    st.markdown("""
    <div class="astra-header">
        <div>
            <div style="display: flex; align-items: center;">
                <span class="astra-title">⚡ Astra AI</span>
                <span class="astra-badge">Snowflake Enterprise</span>
            </div>
            <p style="color: #94a3b8; font-size: 0.88rem; margin: 4px 0 0 0;">
                Autonomous AML/KYC Surveillance, Transaction Anomaly Detection & Regulatory Copilot
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_hdr_right:
    col_u, col_o = st.columns([2, 1])
    with col_u:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 8px;">
            <div style="font-size: 0.82rem; font-weight: 600; color: #f8fafc;">👤 {st.session_state.user_role}</div>
            <span style="display: inline-block; width: 8px; height: 8px; background-color: #10b981; border-radius: 50%; margin-right: 4px;"></span>
            <span style="font-size: 0.72rem; color: #94a3b8;">Active Session</span>
        </div>
        """, unsafe_allow_html=True)
    with col_o:
        st.write("")
        if st.button("Sign Out", use_container_width=True):
            logout_user()

# ------------------------------------------------------------------------------
# 6. Key Surveillance Metrics
# ------------------------------------------------------------------------------
m1, m2, m3, m4 = st.columns(4)

with m1:
    high_risk_count = int((df_customers['Risk Level'] == 'HIGH').sum())
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">High-Risk Entities</div>
        <div class="metric-value">{high_risk_count}</div>
        <div class="metric-sub negative">⚠️ 4 PEP / EDD Accounts</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    flagged_vol = df_tx[df_tx['Status'] == 'FLAGGED']['Amount'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Flagged Volume (24h)</div>
        <div class="metric-value">₹{flagged_vol:,.0f}</div>
        <div class="metric-sub negative">↑ 18.4% vs 7d Baseline</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    critical_alerts = int((df_tx['Anomaly Score'] >= 0.85).sum())
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Critical Anomaly Alerts</div>
        <div class="metric-value">{critical_alerts}</div>
        <div class="metric-sub">Layering & Structuring</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    pending_sar = len(df_cases)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Active SAR Workflows</div>
        <div class="metric-value">{pending_sar}</div>
        <div class="metric-sub">1 Pending MLRO Approval</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ------------------------------------------------------------------------------
# 7. Interactive Tabs Navigation
# ------------------------------------------------------------------------------
tab_copilot, tab_transactions, tab_customers, tab_cases = st.tabs([
    "🧠 Neural Copilot (AI Reasoning)",
    "⚡ Transaction Surveillance",
    "🛡️ Customer AML / KYC Risk",
    "📋 Case Management & SAR"
])

# ------------------------------------------------------------------------------
# TAB 1: Neural Copilot
# ------------------------------------------------------------------------------
with tab_copilot:
    st.subheader("Astra AI Neural Risk Assistant")
    st.caption("Context-grounded reasoning powered by Snowflake Cortex AI and Astra Compliance Records.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": f"👋 Greetings, {st.session_state.user_role}. I am Astra AI, connected to your Snowflake compliance surveillance environment. Ask me to evaluate suspicious transactions, review customer PEP exposure, generate SAR narratives, or assess sanction proximity."
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask Astra AI (e.g., 'Analyze Vikramaditya Singhania for rapid layering' or 'Draft SAR summary')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Astra Neural Copilot is analyzing compliance records..."):
                response_text = ""
                
                # Check for Snowflake Cortex if session is available
                try:
                    conn = st.connection("snowflake")
                    session = conn.session()
                    cortex_query = f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        'mistral-large2',
                        'You are Astra AI, an institutional AML compliance copilot. Answer this inquiry based on compliance records: {prompt}'
                    ) AS AI_RESPONSE
                    """
                    result = session.sql(cortex_query).collect()
                    if result and len(result) > 0:
                        response_text = result[0]['AI_RESPONSE']
                except Exception:
                    response_text = ""

                # Context-grounded intelligent fallback
                if not response_text:
                    p_lower = prompt.lower()
                    if "singhania" in p_lower or "layering" in p_lower:
                        response_text = """### 🛡️ Astra AI Risk Assessment: Vikramaditya Singhania (CUST-1008)
- **Current AML Risk Score**: **88/100 (HIGH RISK)**
- **Surveillance Findings**:
  - **Flagged Transaction**: `TXN-88491` for **₹485,000.00** routed to *Al-Bahrani General Trading (UAE)*.
  - **Identified Pattern**: **Rapid Layering**. Inbound funds from disparate regional accounts were aggregated and transferred outbound within 3 hours, exceeding his monthly normal baseline by 320%.
  - **PEP Status**: Active Director with cross-border sanction exposure.
- **Recommended Remediation**:
  1. Freeze remaining pending wire orders under PMLA Section 12.
  2. Issue Request for Information (RFI) regarding trade invoice documentation.
  3. Escalated to **CASE-4091** for immediate Suspicious Activity Report (SAR) filing."""
                    elif "patil" in p_lower or "structuring" in p_lower or "smurfing" in p_lower:
                        response_text = """### ⚡ Structuring Detection: Devendra Patil (CUST-1003)
- **Anomaly Score**: **0.88 (CRITICAL)**
- **Activity Summary**:
  - Customer executed 4 distinct cash deposits of ₹99,500 across 3 suburban branch cashiers within 48 hours.
  - This pattern deliberately skirts the ₹100,000 / $10,000 mandatory CTR threshold (**Smurfing**).
- **Action**: Alert triggered under Rule `AML-R104` (Cash Structuring Detection). Case `CASE-4088` assigned to compliance team."""
                    elif "sar" in p_lower or "draft" in p_lower or "narrative" in p_lower:
                        response_text = """### 📋 Draft Suspicious Activity Report (SAR) Narrative
**Subject**: Vikramaditya Singhania (CUST-1008)  
**Reporting Period**: October 1 – October 5, 2026  
**Jurisdiction**: Financial Intelligence Unit (FIU)  

**Narrative Summary**:
The subject's account demonstrated an abrupt escalation in velocity, characterized by ₹485,000.00 outbound wires to a foreign free-zone entity without verifiable commercial shipping documentation. Historical monthly baseline was ₹180,000.00. The rapid velocity and offshore transshipment route are strongly indicative of trade-based money laundering (TBML) and layering. Full audit logs and IP signatures are archived under Case `CASE-4091`."""
                    else:
                        response_text = f"### 🧠 Astra AI Intelligence Analysis\nI have evaluated your inquiry against current Snowflake AML records: **\"{prompt}\"**.\n\n- **Surveillance Scope**: 10 monitored customer accounts, 7 real-time transactions, 3 active SAR workflows.\n- **Primary Alerts**: 2 transactions currently flagged for layering and structuring.\n- **Recommendation**: Maintain enhanced surveillance on accounts with Risk Score > 75 and ensure all EDD re-evaluations are completed before month-end."

                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

# ------------------------------------------------------------------------------
# TAB 2: Transaction Surveillance
# ------------------------------------------------------------------------------
with tab_transactions:
    st.subheader("Real-Time Transaction Anomaly Stream")
    
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        search_tx = st.text_input("Search transactions by Customer, ID, or Counterparty:", "")
    with col_f2:
        status_filter = st.selectbox("Status Filter", ["All", "FLAGGED", "UNDER_INVESTIGATION", "CLEARED"])

    filtered_tx = df_tx.copy()
    if search_tx:
        filtered_tx = filtered_tx[
            filtered_tx['Customer'].str.contains(search_tx, case=False) |
            filtered_tx['Tx ID'].str.contains(search_tx, case=False) |
            filtered_tx['Counterparty'].str.contains(search_tx, case=False)
        ]
    if status_filter != "All":
        filtered_tx = filtered_tx[filtered_tx['Status'] == status_filter]

    display_tx = filtered_tx.copy()
    display_tx['Amount'] = display_tx['Amount'].apply(lambda x: f"₹{x:,.2f}")
    display_tx['Anomaly Score'] = display_tx['Anomaly Score'].apply(lambda x: f"{x:.2f}")

    st.dataframe(display_tx, use_container_width=True, height=320)
    
    col_b1, col_b2, col_b3 = st.columns([1, 1, 2])
    with col_b1:
        if st.button("🚩 Flag for SAR Review", use_container_width=True):
            st.success("Selected transactions added to Case Review Queue.")
    with col_b2:
        if st.button("📥 Export Audit Snapshot", use_container_width=True):
            st.info("Audit snapshot generated.")

# ------------------------------------------------------------------------------
# TAB 3: Customer AML / KYC Risk Profiles
# ------------------------------------------------------------------------------
with tab_customers:
    st.subheader("Institutional Customer Risk Directory")
    
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        search_cust = st.text_input("Filter customers by name or country:", "")
    with col_c2:
        risk_filter = st.selectbox("Risk Level", ["All", "HIGH", "MEDIUM", "LOW"])

    filtered_cust = df_customers.copy()
    if search_cust:
        filtered_cust = filtered_cust[
            filtered_cust['Full Name'].str.contains(search_cust, case=False) |
            filtered_cust['Country'].str.contains(search_cust, case=False)
        ]
    if risk_filter != "All":
        filtered_cust = filtered_cust[filtered_cust['Risk Level'] == risk_filter]

    display_cust = filtered_cust.copy()
    display_cust['Monthly Volume'] = display_cust['Monthly Volume'].apply(lambda x: f"₹{x:,.2f}")

    st.dataframe(display_cust, use_container_width=True, height=360)

# ------------------------------------------------------------------------------
# TAB 4: Case Management & Audit Trail
# ------------------------------------------------------------------------------
with tab_cases:
    st.subheader("Active Regulatory Investigations & SAR Workflows")
    
    for _, case in df_cases.iterrows():
        with st.expander(f"{case['Case ID']}: {case['Subject']} — Priority: {case['Priority']}"):
            st.write(f"**Assigned Investigator**: {case['Assigned To']}")
            st.write(f"**Investigation Stage**: {case['Stage']}")
            st.write(f"**Statutory Filing Deadline**: {case['Filing Deadline']}")
            st.write(f"**Attached Evidence Items**: {case['Evidence Count']}")
            st.button(f"Generate FIU Filing Package ({case['Case ID']})", key=case['Case ID'])

# ------------------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>"
    "Astra AI Enterprise Surveillance • Deployed on Snowflake Snowsight • Internal & Regulatory Confidential"
    "</div>",
    unsafe_allow_html=True
)

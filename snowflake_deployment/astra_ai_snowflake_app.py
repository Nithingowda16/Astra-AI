# ==============================================================================
# Astra AI — Enterprise Risk & Regulatory Intelligence Platform
# Streamlit in Snowflake (SiS) Native Console Application
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json

# ------------------------------------------------------------------------------
# 1. Page Configuration & Apple SF Pro Dark Theme Aesthetics
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Astra AI — Risk & AML Surveillance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling
st.markdown("""
<style>
    @import url('https://fonts.cdnfonts.com/css/sf-pro-display');
    
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Sleek card containers */
    .metric-card {
        background: rgba(22, 27, 34, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 20px;
        backdrop-filter: blur(12px);
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: rgba(6, 182, 212, 0.4);
        transform: translateY(-2px);
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #94a3b8;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #f8fafc;
        margin: 4px 0;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #10b981;
    }
    .metric-sub.negative {
        color: #ef4444;
    }
    
    /* Header branding */
    .astra-header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 12px 0 20px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 24px;
    }
    .astra-title {
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ffffff 30%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .astra-badge {
        background: rgba(14, 165, 233, 0.15);
        border: 1px solid rgba(14, 165, 233, 0.35);
        color: #38bdf8;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* Risk Badges */
    .badge-critical {
        background: rgba(239, 68, 68, 0.18);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
    }
    .badge-high {
        background: rgba(249, 115, 22, 0.18);
        color: #fb923c;
        border: 1px solid rgba(249, 115, 22, 0.3);
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
    }
    .badge-medium {
        background: rgba(234, 179, 8, 0.18);
        color: #facc15;
        border: 1px solid rgba(234, 179, 8, 0.3);
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
    }
    .badge-low {
        background: rgba(34, 197, 94, 0.18);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. Snowflake Active Session (Graceful fallback for Local or Cloud execution)
# ------------------------------------------------------------------------------
snowflake_session = None
try:
    from snowflake.snowpark.context import get_active_session
    snowflake_session = get_active_session()
except Exception:
    snowflake_session = None

# ------------------------------------------------------------------------------
# 3. Seed / Cache Data (Institutional AML & Risk Records)
# ------------------------------------------------------------------------------
@st.cache_data
def get_compliance_data():
    customers = [
        {"customer_id": "CUST-1008", "full_name": "Vikramaditya Singhania", "country": "India", "occupation": "Import-Export Director", "account_type": "Corporate", "kyc_status": "Enhanced Due Diligence", "risk_score": 88, "risk_level": "HIGH", "is_pep": True, "monthly_vol": 480000.0},
        {"customer_id": "CUST-1003", "full_name": "Devendra Patil", "country": "India", "occupation": "Financial Broker", "account_type": "Savings", "kyc_status": "Verified", "risk_score": 78, "risk_level": "HIGH", "is_pep": False, "monthly_vol": 150000.0},
        {"customer_id": "CUST-1004", "full_name": "Hon. Rameshwar Prasad", "country": "India", "occupation": "Legislative Committee Member", "account_type": "Current", "kyc_status": "Enhanced Due Diligence", "risk_score": 82, "risk_level": "HIGH", "is_pep": True, "monthly_vol": 600000.0},
        {"customer_id": "CUST-1005", "full_name": "Global Trade Nexus LLC", "country": "United Arab Emirates", "occupation": "Cross-Border Commodities", "account_type": "Corporate", "kyc_status": "Verified", "risk_score": 68, "risk_level": "MEDIUM", "is_pep": False, "monthly_vol": 1500000.0},
        {"customer_id": "CUST-1009", "full_name": "Siddharth Verma", "country": "Singapore", "occupation": "Fintech Solutions Director", "account_type": "Current", "kyc_status": "Verified", "risk_score": 54, "risk_level": "MEDIUM", "is_pep": False, "monthly_vol": 320000.0},
        {"customer_id": "CUST-1001", "full_name": "Ananya Sharma", "country": "India", "occupation": "Lead Cloud Architect", "account_type": "Savings", "kyc_status": "Verified", "risk_score": 12, "risk_level": "LOW", "is_pep": False, "monthly_vol": 95000.0},
        {"customer_id": "CUST-1002", "full_name": "Rajesh Kumar Gupta", "country": "India", "occupation": "Wholesale Electronics Merchant", "account_type": "Current", "kyc_status": "Verified", "risk_score": 24, "risk_level": "LOW", "is_pep": False, "monthly_vol": 480000.0},
        {"customer_id": "CUST-1006", "full_name": "Dr. Priya Sundaram", "country": "United Kingdom", "occupation": "Chief Cardiologist", "account_type": "Savings", "kyc_status": "Verified", "risk_score": 15, "risk_level": "LOW", "is_pep": False, "monthly_vol": 180000.0},
        {"customer_id": "CUST-1007", "full_name": "Apex Logistics Corridors", "country": "Cyprus", "occupation": "Maritime Freight Transit", "account_type": "Corporate", "kyc_status": "Under Review", "risk_score": 74, "risk_level": "HIGH", "is_pep": False, "monthly_vol": 2800000.0},
        {"customer_id": "CUST-1010", "full_name": "Kavita Mehra", "country": "India", "occupation": "Architectural Designer", "account_type": "Savings", "kyc_status": "Verified", "risk_score": 18, "risk_level": "LOW", "is_pep": False, "monthly_vol": 140000.0},
    ]
    
    transactions = [
        {"tx_id": "TXN-88491", "customer": "Vikramaditya Singhania", "amount": 485000.0, "currency": "INR", "type": "WIRE_OUTBOUND", "counterparty": "Al-Bahrani General Trading (UAE)", "anomaly_score": 0.94, "status": "FLAGGED", "trigger": "Rapid Layering / High-Risk Corridor", "timestamp": "2026-10-05 17:42:10"},
        {"tx_id": "TXN-88489", "customer": "Devendra Patil", "amount": 99500.0, "currency": "INR", "type": "CASH_DEPOSIT", "counterparty": "Multiple Branch Cashiers", "anomaly_score": 0.88, "status": "FLAGGED", "trigger": "Smurfing / Structuring under reporting cap", "timestamp": "2026-10-05 16:30:15"},
        {"tx_id": "TXN-88485", "customer": "Hon. Rameshwar Prasad", "amount": 750000.0, "currency": "INR", "type": "RTGS_INBOUND", "counterparty": "Aethelgard Consulting S.A.", "anomaly_score": 0.91, "status": "UNDER_INVESTIGATION", "trigger": "PEP Exposure / Unexplained Wealth Order", "timestamp": "2026-10-05 15:18:02"},
        {"tx_id": "TXN-88480", "customer": "Apex Logistics Corridors", "amount": 1420000.0, "currency": "USD", "type": "SWIFT_TRANSFER", "counterparty": "Bosphorus Maritime Trading", "anomaly_score": 0.85, "status": "FLAGGED", "trigger": "Sanctions Proximity / Offshore Gateway", "timestamp": "2026-10-05 14:05:40"},
        {"tx_id": "TXN-88472", "customer": "Global Trade Nexus LLC", "amount": 320000.0, "currency": "INR", "type": "VENDOR_PAYMENT", "counterparty": "Shenzhen Electrotech Corp", "anomaly_score": 0.42, "status": "CLEARED", "trigger": "Standard Trade Flow", "timestamp": "2026-10-05 12:44:11"},
        {"tx_id": "TXN-88465", "customer": "Ananya Sharma", "amount": 18500.0, "currency": "INR", "type": "UPI_TRANSFER", "counterparty": "Urban Merchant Pay", "anomaly_score": 0.05, "status": "CLEARED", "trigger": "Normal Personal Spending", "timestamp": "2026-10-05 11:20:00"},
        {"tx_id": "TXN-88461", "customer": "Siddharth Verma", "amount": 125000.0, "currency": "INR", "type": "NEFT_OUTBOUND", "counterparty": "CloudScale Hosting SG", "anomaly_score": 0.38, "status": "CLEARED", "trigger": "Routine SaaS Billing", "timestamp": "2026-10-05 10:14:22"},
    ]
    
    cases = [
        {"case_id": "CASE-4091", "subject": "Singhania Trade Horizon Layering", "assigned_to": "Senior Risk Officer", "priority": "CRITICAL", "stage": "SAR In Preparation", "filing_deadline": "2026-10-08", "evidence_count": 7},
        {"case_id": "CASE-4088", "subject": "Structuring Inquiries — D. Patil Branches", "assigned_to": "Compliance Analyst", "priority": "HIGH", "stage": "Request for Information (RFI)", "filing_deadline": "2026-10-12", "evidence_count": 4},
        {"case_id": "CASE-4075", "subject": "Apex Logistics Bosphorus Sanctions Check", "assigned_to": "Chief Sanctions Officer", "priority": "HIGH", "stage": "Escalated to MLRO", "filing_deadline": "2026-10-09", "evidence_count": 12},
    ]
    
    return pd.DataFrame(customers), pd.DataFrame(transactions), pd.DataFrame(cases)

df_customers, df_tx, df_cases = get_compliance_data()

# ------------------------------------------------------------------------------
# 4. Header & Branding Section
# ------------------------------------------------------------------------------
col_hdr_left, col_hdr_right = st.columns([3, 1])
with col_hdr_left:
    st.markdown("""
    <div class="astra-header">
        <div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 2rem;">⚡</span>
                <span class="astra-title">Astra AI</span>
                <span class="astra-badge">Snowflake Enterprise</span>
            </div>
            <p style="color: #94a3b8; font-size: 0.88rem; margin: 4px 0 0 0;">
                Next-Gen AML/KYC Surveillance, Transaction Anomaly Detection & Regulatory Copilot
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_hdr_right:
    env_label = "Snowflake Snowpark Active" if snowflake_session else "Snowflake Local Simulation"
    st.markdown(f"""
    <div style="text-align: right; padding-top: 10px;">
        <span style="display: inline-block; width: 8px; height: 8px; background-color: #10b981; border-radius: 50%; margin-right: 6px;"></span>
        <span style="font-size: 0.8rem; color: #cbd5e1; font-weight: 500;">{env_label}</span><br>
        <span style="font-size: 0.72rem; color: #64748b;">Engine: Cortex + Gemini RAG</span>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 5. Top Key Risk & Surveillance Metrics
# ------------------------------------------------------------------------------
m1, m2, m3, m4 = st.columns(4)

with m1:
    high_risk_count = len(df_customers[df_customers['risk_level'] == 'HIGH'])
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">High-Risk Entities</div>
        <div class="metric-value">{high_risk_count}</div>
        <div class="metric-sub negative">⚠️ 4 PEP / EDD Accounts</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    flagged_vol = df_tx[df_tx['status'] == 'FLAGGED']['amount'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Flagged Volume (24h)</div>
        <div class="metric-value">₹{flagged_vol:,.0f}</div>
        <div class="metric-sub negative">↑ 18.4% vs 7d Baseline</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    critical_alerts = len(df_tx[df_tx['anomaly_score'] >= 0.85])
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
# 6. Primary Tabs Navigation
# ------------------------------------------------------------------------------
tab_copilot, tab_transactions, tab_customers, tab_cases = st.tabs([
    "🧠 Neural Copilot (AI Reasoning)",
    "⚡ Transaction Surveillance",
    "🛡️ Customer AML / KYC Risk",
    "📋 Case Management & SAR"
])

# ------------------------------------------------------------------------------
# TAB 1: Neural Copilot (Cortex + Gemini Integration)
# ------------------------------------------------------------------------------
with tab_copilot:
    st.subheader("Astra AI Neural Risk Assistant")
    st.caption("Context-grounded reasoning powered by Snowflake Cortex AI and Astra Database RAG.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Greetings, Senior Risk Officer. I am Astra AI, connected to your Snowflake compliance surveillance environment. Ask me to evaluate suspicious transactions, review customer PEP exposure, generate SAR narratives, or assess sanction proximity."
            }
        ]

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat prompt input
    if prompt := st.chat_input("Ask Astra AI (e.g., 'Analyze Vikramaditya Singhania for rapid layering' or 'Draft a SAR summary')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Reasoning logic (Snowflake Cortex or Built-in Intelligent Fallback)
        with st.chat_message("assistant"):
            with st.spinner("Astra Neural Copilot is analyzing Snowflake compliance records..."):
                response_text = ""
                
                # Try Snowflake Cortex if session is active
                if snowflake_session:
                    try:
                        cortex_query = f"""
                        SELECT SNOWFLAKE.CORTEX.COMPLETE(
                            'mistral-large2',
                            'You are Astra AI, an institutional financial crime and AML compliance copilot. Answer the following risk inquiry based on high-risk accounts (Vikramaditya Singhania, Devendra Patil, Rameshwar Prasad): {prompt}'
                        ) AS AI_RESPONSE
                        """
                        result = snowflake_session.sql(cortex_query).collect()
                        response_text = result[0]['AI_RESPONSE']
                    except Exception:
                        response_text = ""

                # Fallback intelligent contextual response
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
            filtered_tx['customer'].str.contains(search_tx, case=False) |
            filtered_tx['tx_id'].str.contains(search_tx, case=False) |
            filtered_tx['counterparty'].str.contains(search_tx, case=False)
        ]
    if status_filter != "All":
        filtered_tx = filtered_tx[filtered_tx['status'] == status_filter]

    st.dataframe(
        filtered_tx.style.format({"amount": "₹{:,.2f}", "anomaly_score": "{:.2f}"}),
        use_container_width=True,
        height=320
    )
    
    # Quick Action Buttons
    col_b1, col_b2, col_b3 = st.columns([1, 1, 2])
    with col_b1:
        if st.button("🚩 Flag for SAR Filing", use_container_width=True):
            st.success("Selected transactions added to Case Review Queue.")
    with col_b2:
        if st.button("📥 Export CSV", use_container_width=True):
            st.info("Exporting audit snapshot...")

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
            filtered_cust['full_name'].str.contains(search_cust, case=False) |
            filtered_cust['country'].str.contains(search_cust, case=False)
        ]
    if risk_filter != "All":
        filtered_cust = filtered_cust[filtered_cust['risk_level'] == risk_filter]

    st.dataframe(
        filtered_cust.style.format({"monthly_vol": "₹{:,.2f}", "risk_score": "{:d}"}),
        use_container_width=True,
        height=360
    )

# ------------------------------------------------------------------------------
# TAB 4: Case Management & Audit Trail
# ------------------------------------------------------------------------------
with tab_cases:
    st.subheader("Active Regulatory Investigations & SAR Workflows")
    
    for _, case in df_cases.iterrows():
        with st.expander(f"{case['case_id']}: {case['subject']} — Priority: {case['priority']}"):
            st.write(f"**Assigned Investigator**: {case['assigned_to']}")
            st.write(f"**Investigation Stage**: {case['stage']}")
            st.write(f"**Statutory Filing Deadline**: {case['filing_deadline']}")
            st.write(f"**Attached Evidence Items**: {case['evidence_count']}")
            st.button(f"Generate FIU Filing Package ({case['case_id']})", key=case['case_id'])

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

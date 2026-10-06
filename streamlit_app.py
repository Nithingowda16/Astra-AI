# ==============================================================================
# Astra AI — Enterprise Risk & Regulatory Intelligence Platform
# Pixel-Perfect Implementation matching React Production Design
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import base64
import os

# ------------------------------------------------------------------------------
# 1. Page Configuration
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Astra AI — Risk & Regulatory Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# 2. State Initialization
# ------------------------------------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "auth_tab" not in st.session_state:
    st.session_state.auth_tab = "signin"
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Dashboard"
if "selected_txn" not in st.session_state:
    st.session_state.selected_txn = None
if "copilot_query" not in st.session_state:
    st.session_state.copilot_query = ""

# ------------------------------------------------------------------------------
# 3. Assets Loader (Base64)
# ------------------------------------------------------------------------------
@st.cache_data
def get_asset_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_dark_b64 = get_asset_b64("frontend/public/assets/astra-logo-dark.png")
logo_light_b64 = get_asset_b64("frontend/public/assets/astra-logo-light.png")
bg_dark_b64 = get_asset_b64("frontend/public/assets/login-bg.png")
bg_light_b64 = get_asset_b64("frontend/public/assets/login-bg-light.png")

current_theme = st.session_state.theme
current_logo_b64 = logo_light_b64 if current_theme == "light" else logo_dark_b64
current_bg_b64 = bg_light_b64 if current_theme == "light" else bg_dark_b64

# ------------------------------------------------------------------------------
# 4. Master Theme Stylesheet (Exact tokens from index.css)
# ------------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.cdnfonts.com/css/sf-pro-display');
    
    html, body, [class*="css"], [class*="st-"] {{
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, "SF Pro", "SF Pro Text", "Helvetica Neue", "Segoe UI", Roboto, sans-serif !important;
    }}
    
    /* Hide default Streamlit header and padding */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        z-index: 1;
    }}
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 1440px !important;
    }}
    
    /* Theme Tokens */
    :root {{
        --bg-color: {'#ffffff' if current_theme == 'light' else '#09090b'};
        --card-bg: {'#ffffff' if current_theme == 'light' else '#0e0e11'};
        --card-hover: {'#f4f4f5' if current_theme == 'light' else '#18181b'};
        --border-color: {'#e4e4e7' if current_theme == 'light' else '#27272a'};
        --text-primary: {'#09090b' if current_theme == 'light' else '#ffffff'};
        --text-secondary: {'#52525b' if current_theme == 'light' else '#a1a1aa'};
        --text-muted: {'#a1a1aa' if current_theme == 'light' else '#71717a'};
        --input-bg: {'#ffffff' if current_theme == 'light' else '#121215'};
        --btn-primary-bg: {'#1d1d1f' if current_theme == 'light' else '#ffffff'};
        --btn-primary-text: {'#ffffff' if current_theme == 'light' else '#000000'};
    }}
    
    /* Auth Page Wallpaper Container */
    [data-testid="stAppViewContainer"] {{
        background-image: url('data:image/png;base64,{current_bg_b64}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}
    
    /* Ensure no overlay is blurring content */
    .auth-bg-layer, .auth-bg-overlay {{
        display: none !important;
    }}
    
    /* Floating Auth Card (Crisp, zero blur) */
    [data-testid="stForm"] {{
        background: {'rgba(255, 255, 255, 0.96)' if current_theme == 'light' else 'rgba(14, 14, 17, 0.92)'} !important;
        border: 1px solid {'rgba(0, 0, 0, 0.08)' if current_theme == 'light' else 'rgba(255, 255, 255, 0.15)'} !important;
        border-radius: 28px !important;
        padding: 34px 38px 28px 38px !important;
        box-shadow: {'0 30px 60px -12px rgba(0, 0, 0, 0.14), 0 0 0 1px rgba(0, 0, 0, 0.04)' if current_theme == 'light' else '0 30px 60px -12px rgba(0, 0, 0, 0.9)'} !important;
        max-width: 480px !important;
        margin: 0 auto !important;
    }}
    
    [data-testid="stForm"] [data-testid="stTextInput"] input {{
        background: {'#ffffff' if current_theme == 'light' else '#18181b'} !important;
        color: {'#09090b' if current_theme == 'light' else '#ffffff'} !important;
        border: 1px solid {'#e4e4e7' if current_theme == 'light' else '#27272a'} !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        font-size: 0.92rem !important;
    }}
    
    [data-testid="stForm"] button[kind="primary"],
    [data-testid="stForm"] button[kind="secondary"],
    [data-testid="stForm"] button {{
        background: {'#1d1d1f' if current_theme == 'light' else '#ffffff'} !important;
        color: {'#ffffff' if current_theme == 'light' else '#000000'} !important;
        border: none !important;
        border-radius: 9999px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        box-shadow: {'0 4px 14px rgba(0, 0, 0, 0.2)' if current_theme == 'light' else '0 4px 14px rgba(255, 255, 255, 0.3)'} !important;
    }}
    
    .auth-logo-img {{
        width: 64px;
        height: 64px;
        object-fit: contain;
        margin: 0 auto 10px auto;
        display: block;
        filter: drop-shadow(0 4px 16px rgba(19, 214, 214, 0.45));
    }}
    
    .auth-title-text {{
        font-size: 2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.035em !important;
        color: {'#09090b' if current_theme == 'light' else '#ffffff'} !important;
        margin: 4px 0 16px 0 !important;
        text-align: center;
    }}
    
    /* Auth Pill Tabs */
    .auth-tabs-pill {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        background: {'#f4f4f5' if current_theme == 'light' else '#18181b'};
        padding: 4px;
        border-radius: 9999px;
        border: 1px solid var(--border-color);
        margin-bottom: 22px;
    }}
    .auth-tab-item {{
        padding: 8px 14px;
        border-radius: 9999px;
        font-size: 0.84rem;
        font-weight: 600;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        cursor: pointer;
    }}
    .auth-tab-item.active-signin {{
        background: #2563eb;
        color: #ffffff;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
    }}
    .auth-tab-item.active-signup {{
        background: #059669;
        color: #ffffff;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.3);
    }}
    
    /* Security Badges Pill */
    .sec-badge {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: {'rgba(0, 0, 0, 0.04)' if current_theme == 'light' else 'rgba(255, 255, 255, 0.05)'};
        border: 1px solid var(--border-color);
        border-radius: 9999px;
        padding: 4px 10px;
        font-size: 0.72rem;
        color: var(--text-secondary);
        margin: 4px 3px;
    }}

    /* Top Active Alert Banner */
    .active-alert-box {{
        background: {'linear-gradient(90deg, rgba(29, 78, 216, 0.08), rgba(6, 182, 212, 0.05))' if current_theme == 'light' else 'linear-gradient(90deg, rgba(29, 78, 216, 0.22), rgba(6, 182, 212, 0.12))'};
        border: 1px solid {'rgba(59, 130, 246, 0.3)' if current_theme == 'light' else 'rgba(59, 130, 246, 0.4)'};
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
    }}
    .alert-tag-red {{
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 4px;
    }}
    
    /* KPI Card Style */
    .kpi-stat-card {{
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 20px 22px;
        box-shadow: {'0 2px 8px rgba(0, 0, 0, 0.04)' if current_theme == 'light' else '0 4px 16px rgba(0, 0, 0, 0.4)'};
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    .kpi-stat-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }}
    .kpi-stat-label {{
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: var(--text-secondary);
    }}
    .kpi-stat-val {{
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: var(--text-primary);
        line-height: 1.1;
        margin: 4px 0 6px 0;
    }}
    .kpi-stat-sub {{
        font-size: 0.78rem;
        color: var(--text-muted);
    }}
    
    /* Alert Stream Rows */
    .alert-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 14px;
        border-bottom: 1px solid var(--border-color);
        transition: background-color 0.15s ease;
    }}
    .alert-row:hover {{
        background-color: var(--card-hover);
    }}
    .alert-row:last-child {{
        border-bottom: none;
    }}
    
    .badge-crit {{
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 2px 7px;
        border-radius: 5px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-right: 10px;
    }}
    .badge-med {{
        background: rgba(234, 179, 8, 0.15);
        color: #eab308;
        border: 1px solid rgba(234, 179, 8, 0.3);
        padding: 2px 7px;
        border-radius: 5px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-right: 10px;
    }}
    .badge-low {{
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 2px 7px;
        border-radius: 5px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-right: 10px;
    }}
    
    /* Theme Toggle Switch Header */
    .top-theme-switch {{
        position: fixed;
        top: 14px;
        right: 20px;
        z-index: 999;
    }}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 5. Top Theme Toggle Controller
# ------------------------------------------------------------------------------
top_col1, top_col2 = st.columns([10, 1])
with top_col2:
    theme_icon = "🌙" if current_theme == "light" else "☀️"
    if st.button(f"{theme_icon} Theme", key="theme_toggle_btn", help="Switch between Light and Dark mode"):
        st.session_state.theme = "dark" if current_theme == "light" else "light"
        st.rerun()

# ------------------------------------------------------------------------------
# 6. AUTHENTICATION GATEWAY (SCREENSHOTS 1, 2, 4)
# ------------------------------------------------------------------------------
if not st.session_state.authenticated:
    _, auth_center_col, _ = st.columns([1, 1.35, 1])
    
    with auth_center_col:
        st.write("")
        st.write("")
        
        # Header with Logo & Title (Crisp, High Contrast)
        logo_html = f'<img src="data:image/png;base64,{current_logo_b64}" class="auth-logo-img" alt="Astra AI" />' if current_logo_b64 else '<span style="font-size: 3.2rem;">⚡</span>'
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 16px;">
            {logo_html}
            <h1 class="auth-title-text">Astra AI</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Pill Tab Switcher: Sign In vs Sign Up
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            if st.button("➔ Sign In", key="pill_signin", use_container_width=True, type="primary" if st.session_state.auth_tab == "signin" else "secondary"):
                st.session_state.auth_tab = "signin"
                st.rerun()
        with tab_col2:
            if st.button("👤+ Sign Up", key="pill_signup", use_container_width=True, type="primary" if st.session_state.auth_tab == "signup" else "secondary"):
                st.session_state.auth_tab = "signup"
                st.rerun()

        st.write("")
        
        # Form Container
        if st.session_state.auth_tab == "signin":
            with st.form("signin_form"):
                st.markdown(f'<div style="font-size: 0.82rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px;">👤 Username or Email Address</div>', unsafe_allow_html=True)
                login_user = st.text_input("Username", value="analyst", label_visibility="collapsed")
                
                st.markdown(f'<div style="font-size: 0.82rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px; margin-top: 10px;">🔒 Password</div>', unsafe_allow_html=True)
                login_pwd = st.text_input("Password", value="password", type="password", label_visibility="collapsed")
                
                st.write("")
                submit_login = st.form_submit_button("➔ Sign In", use_container_width=True)
                if submit_login:
                    st.session_state.authenticated = True
                    st.session_state.user_name = "Senior Risk Officer"
                    st.rerun()
        else:
            with st.form("signup_form"):
                st.markdown(f'<div style="font-size: 0.82rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px;">🪪 Full Name</div>', unsafe_allow_html=True)
                reg_name = st.text_input("Full Name", value="Rachel Zane", label_visibility="collapsed")
                
                c_u, c_e = st.columns(2)
                with c_u:
                    st.markdown(f'<div style="font-size: 0.82rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px;">👤 Username</div>', unsafe_allow_html=True)
                    reg_usr = st.text_input("Username", value="analyst", label_visibility="collapsed")
                with c_e:
                    st.markdown(f'<div style="font-size: 0.82rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px;">✉️ Business Email</div>', unsafe_allow_html=True)
                    reg_eml = st.text_input("Email", value="rachel@financial.corp", label_visibility="collapsed")
                
                c_p, c_r = st.columns(2)
                with c_p:
                    st.markdown(f'<div style="font-size: 0.82rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px;">🔑 Password (min 6 chars)</div>', unsafe_allow_html=True)
                    reg_pw = st.text_input("Password", value="password", type="password", label_visibility="collapsed")
                with c_r:
                    st.markdown(f'<div style="font-size: 0.82rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px;">🛡️ Account Role</div>', unsafe_allow_html=True)
                    reg_role = st.selectbox("Role", ["Senior Risk Officer", "Compliance Officer", "User (Standard Access)"], label_visibility="collapsed")
                
                st.write("")
                submit_reg = st.form_submit_button("👤+ Create Account & Sign In", use_container_width=True)
                if submit_reg:
                    st.session_state.authenticated = True
                    st.session_state.user_name = reg_name
                    st.rerun()

        # Security Badges
        st.markdown("""
        <div style="text-align: center; margin-top: 24px; position: relative; z-index: 10;">
            <div>
                <span class="sec-badge">🛡️ PBKDF2 Password Hashing</span>
                <span class="sec-badge">🔒 HMAC-SHA256 Bearer Token</span>
            </div>
            <div style="margin-top: 4px;">
                <span class="sec-badge">🌐 Zero Unauthorized Access</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# ------------------------------------------------------------------------------
# 7. AUTHENTICATED OPERATIONAL DASHBOARD (SCREENSHOT 3)
# ------------------------------------------------------------------------------

# --- LEFT SIDEBAR (Matching Exact Screenshot 3) ---
with st.sidebar:
    # Astra AI Logo & Brand
    logo_side_html = f'<img src="data:image/png;base64,{current_logo_b64}" width="38" height="38" style="object-fit: contain; vertical-align: middle; margin-right: 10px;" />' if current_logo_b64 else '⚡ '
    st.markdown(f"""
    <div style="display: flex; align-items: center; padding: 10px 0 16px 0; border-bottom: 1px solid var(--border-color); margin-bottom: 16px;">
        {logo_side_html}
        <div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-primary); letter-spacing: -0.02em;">Astra AI</div>
            <div style="font-size: 0.65rem; font-weight: 700; color: var(--text-muted); letter-spacing: 0.06em; text-transform: uppercase;">Risk & Regulatory Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin: 12px 0 6px 0;">OPERATIONS</div>', unsafe_allow_html=True)
    
    nav_items = ["Dashboard", "Transactions", "Customers", "Alerts (8)", "Investigations (2)"]
    for item in nav_items:
        clean_name = item.split(" ")[0]
        is_active = st.session_state.active_nav == clean_name
        if st.button(f"{'📊 ' if 'Dash' in item else '⚡ ' if 'Trans' in item else '👥 ' if 'Cust' in item else '🔔 ' if 'Alert' in item else '📋 '}{item}", key=f"nav_{clean_name}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.active_nav = clean_name
            st.rerun()

    st.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin: 18px 0 6px 0;">AI & INTELLIGENCE</div>', unsafe_allow_html=True)
    
    if st.button("📖 Regulatory Rules", key="nav_rules", use_container_width=True, type="primary" if st.session_state.active_nav == "Regulatory" else "secondary"):
        st.session_state.active_nav = "Regulatory"
        st.rerun()
        
    if st.button("🧠 Copilot Assistant  [AI]", key="nav_copilot", use_container_width=True, type="primary" if st.session_state.active_nav == "Copilot" else "secondary"):
        st.session_state.active_nav = "Copilot"
        st.rerun()

    st.write("")
    st.write("")
    
    # User Profile Card at Sidebar Bottom
    user_name = getattr(st.session_state, "user_name", "Senior Risk Officer")
    st.markdown(f"""
    <div style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 14px; padding: 12px; margin-top: 20px; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #2563eb; color: #fff; font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: 0.85rem;">S</div>
            <div>
                <div style="font-size: 0.82rem; font-weight: 700; color: var(--text-primary);">{user_name}</div>
                <span style="font-size: 0.65rem; font-weight: 800; background: rgba(37, 99, 235, 0.15); color: #2563eb; padding: 1px 6px; border-radius: 4px;">USER</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- TOP BREADCRUMB & ENGINE STATUS ---
bc_col1, bc_col2 = st.columns([8, 2])
with bc_col1:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;">
        <span>Astra AI</span> / <strong style="color: var(--text-primary);">{st.session_state.active_nav}</strong>
    </div>
    """, unsafe_allow_html=True)
with bc_col2:
    st.markdown("""
    <div style="text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 6px; font-size: 0.8rem; font-weight: 600; color: #10b981;">
        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10b981; box-shadow: 0 0 8px #10b981;"></span>
        <span>Live Engine Connected</span>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 8. VIEW: OPERATIONAL DASHBOARD
# ------------------------------------------------------------------------------
if st.session_state.active_nav == "Dashboard":
    # 1. TOP ACTIVE ALERT BANNER
    alert_c1, alert_c2 = st.columns([4, 1.2])
    with alert_c1:
        st.markdown("""
        <div style="background: linear-gradient(90deg, rgba(29, 78, 216, 0.12), rgba(6, 182, 212, 0.06)); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 16px; padding: 16px 20px;">
            <div class="alert-tag-red">ACTIVE ALERT</div>
            <div style="font-size: 0.88rem; color: var(--text-primary); margin-top: 4px;">
                Customer <strong>Vikramaditya Singhania (CUST-1008)</strong> triggered Statutory AML Rule 01 (Large Value CDD) and Rule 03 (High-Risk Jurisdiction).
            </div>
        </div>
        """, unsafe_allow_html=True)
    with alert_c2:
        st.write("")
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("Review TXN-1024 ➔", use_container_width=True, type="primary"):
                st.session_state.active_nav = "Transactions"
                st.rerun()
        with b_c2:
            if st.button("Ask Copilot", use_container_width=True):
                st.session_state.active_nav = "Copilot"
                st.session_state.copilot_query = "Why was transaction TXN-1024 flagged?"
                st.rerun()

    st.write("")

    # 2. 4 KPI STATS CARDS (Exact numbers from Screenshot 3)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <span class="kpi-stat-label">TOTAL TRANSACTIONS</span>
                <span style="background: rgba(59, 130, 246, 0.15); color: #3b82f6; padding: 4px 8px; border-radius: 8px;">📈</span>
            </div>
            <div class="kpi-stat-val">121</div>
            <div class="kpi-stat-sub">Monitored Volume: ₹1,26,13,759.65</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        st.markdown("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <span class="kpi-stat-label">SUSPICIOUS TRANSACTIONS</span>
                <span style="background: rgba(239, 68, 68, 0.15); color: #ef4444; padding: 4px 8px; border-radius: 8px;">⚠️</span>
            </div>
            <div class="kpi-stat-val" style="color: #ef4444;">14 <span style="font-size: 1.1rem; font-weight: 500; color: var(--text-secondary);">(11.6%)</span></div>
            <div class="kpi-stat-sub">Triggered explainable rule thresholds</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <span class="kpi-stat-label">HIGH-RISK CUSTOMERS</span>
                <span style="background: rgba(249, 115, 22, 0.15); color: #f97316; padding: 4px 8px; border-radius: 8px;">👥</span>
            </div>
            <div class="kpi-stat-val" style="color: #f97316;">3</div>
            <div class="kpi-stat-sub">Subject to Enhanced Due Diligence (EDD)</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <span class="kpi-stat-label">OPEN INVESTIGATIONS</span>
                <span style="background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 4px 8px; border-radius: 8px;">📋</span>
            </div>
            <div class="kpi-stat-val">2</div>
            <div class="kpi-stat-sub">Active cases under compliance review</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 3. MIDDLE SECTION: RISK DISTRIBUTION & 14-DAY TIMELINE
    m_col1, m_col2 = st.columns([1, 1.5])
    with m_col1:
        st.markdown("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <strong style="color: var(--text-primary); font-size: 1rem;">Risk Score Distribution</strong>
                <span style="color: #06b6d4;">🛡️</span>
            </div>
            
            <div style="margin-top: 14px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
                    <span style="color: #ef4444; font-weight: 600;">Critical Risk (85-100)</span>
                    <strong>4 txns</strong>
                </div>
                <div style="width: 100%; height: 7px; background: rgba(0,0,0,0.06); border-radius: 4px; overflow: hidden; margin-bottom: 14px;">
                    <div style="width: 14%; height: 100%; background: #ef4444;"></div>
                </div>

                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
                    <span style="color: #f97316; font-weight: 600;">High Risk (65-84)</span>
                    <strong>0 txns</strong>
                </div>
                <div style="width: 100%; height: 7px; background: rgba(0,0,0,0.06); border-radius: 4px; overflow: hidden; margin-bottom: 14px;">
                    <div style="width: 0%; height: 100%; background: #f97316;"></div>
                </div>

                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
                    <span style="color: #eab308; font-weight: 600;">Medium Risk (40-64)</span>
                    <strong>3 txns</strong>
                </div>
                <div style="width: 100%; height: 7px; background: rgba(0,0,0,0.06); border-radius: 4px; overflow: hidden; margin-bottom: 14px;">
                    <div style="width: 10%; height: 100%; background: #eab308;"></div>
                </div>

                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
                    <span style="color: #10b981; font-weight: 600;">Low Risk (0-39)</span>
                    <strong>114 txns</strong>
                </div>
                <div style="width: 100%; height: 7px; background: rgba(0,0,0,0.06); border-radius: 4px; overflow: hidden; margin-bottom: 14px;">
                    <div style="width: 92%; height: 100%; background: #10b981;"></div>
                </div>
            </div>

            <div style="font-size: 0.74rem; color: var(--text-muted); margin-top: 10px; border-top: 1px solid var(--border-color); padding-top: 10px;">
                Evaluated by the <strong>Deterministic Risk Engine</strong> using baseline deviation, FATF corridor checks, and burst frequency.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        st.markdown("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <strong style="color: var(--text-primary); font-size: 1rem;">Suspicious Volume & Alerts Timeline (14 Days)</strong>
                <span style="color: #3b82f6;">📈</span>
            </div>
            
            <div style="height: 195px; display: flex; align-items: flex-end; gap: 8px; padding-top: 18px;">
        """, unsafe_allow_html=True)
        
        # 14 Days synthetic chart matching Screenshot 3
        chart_data = [
            ("Sep 23", 10, 0), ("Sep 24", 15, 0), ("Sep 25", 35, 0), ("Sep 26", 20, 1),
            ("Sep 27", 18, 1), ("Sep 28", 40, 0), ("Sep 29", 12, 0), ("Sep 30", 55, 0),
            ("Oct 01", 85, 1), ("Oct 02", 45, 0), ("Oct 03", 60, 0), ("Oct 04", 75, 1),
            ("Oct 05", 25, 6), ("Oct 06", 50, 0)
        ]
        
        cols = st.columns(len(chart_data))
        for idx, (day, val, flg) in enumerate(chart_data):
            with cols[idx]:
                st.write("")
                color = "#ef4444" if flg > 0 else "#3b82f6"
                flag_badge = f'<div style="text-align: center; color: #ef4444; font-weight: 700; font-size: 0.7rem;">{flg}</div>' if flg > 0 else '<div style="height: 14px;"></div>'
                st.markdown(f"""
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 160px;">
                    {flag_badge}
                    <div style="width: 100%; height: {val * 1.3}px; background: {color}; border-radius: 4px 4px 0 0;"></div>
                    <div style="font-size: 0.65rem; color: var(--text-muted); margin-top: 4px; white-space: nowrap;">{day.split(' ')[1]}</div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("""
            <div style="display: flex; gap: 16px; justify-content: center; margin-top: 10px; font-size: 0.75rem; color: var(--text-secondary);">
                <span><span style="display: inline-block; width: 10px; height: 10px; background: #3b82f6; border-radius: 2px;"></span> Normal Transactions</span>
                <span><span style="display: inline-block; width: 10px; height: 10px; background: #ef4444; border-radius: 2px;"></span> Suspicious / Flagged Activity</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 4. BOTTOM SECTION: PRIORITY RISK ALERTS & MONITORED CORRIDORS (Exact Screenshot 3)
    b_col1, b_col2 = st.columns([1.6, 1])
    
    with b_col1:
        st.markdown("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <div>
                    <strong style="color: var(--text-primary); font-size: 1rem;">Priority Risk Alerts</strong>
                    <div style="font-size: 0.74rem; color: var(--text-muted);">Latest Triggered Events</div>
                </div>
            </div>
            
            <div style="margin-top: 8px;">
                <div class="alert-row">
                    <div>
                        <span class="badge-crit">CRITICAL</span>
                        <strong style="color: var(--text-primary);">Vikramaditya Singhania</strong> &bull; <span style="color: var(--text-secondary);">₹6,80,000 to Panama</span>
                    </div>
                    <span style="color: #3b82f6; font-size: 0.82rem; font-weight: 600;">TXN-1025 ↗</span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-crit">CRITICAL</span>
                        <strong style="color: var(--text-primary);">Vikramaditya Singhania</strong> &bull; <span style="color: var(--text-secondary);">₹12,50,000 to Cayman Islands</span>
                    </div>
                    <span style="color: #3b82f6; font-size: 0.82rem; font-weight: 600;">TXN-1024 ↗</span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-med">MEDIUM</span>
                        <strong style="color: var(--text-primary);">Devendra Patil</strong> &bull; <span style="color: var(--text-secondary);">₹49,800 to India</span>
                    </div>
                    <span style="color: #3b82f6; font-size: 0.82rem; font-weight: 600;">TXN-1034 ↗</span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-med">MEDIUM</span>
                        <strong style="color: var(--text-primary);">Devendra Patil</strong> &bull; <span style="color: var(--text-secondary);">₹48,900 to India</span>
                    </div>
                    <span style="color: #3b82f6; font-size: 0.82rem; font-weight: 600;">TXN-1033 ↗</span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-med">MEDIUM</span>
                        <strong style="color: var(--text-primary);">Devendra Patil</strong> &bull; <span style="color: var(--text-secondary);">₹49,200 to India</span>
                    </div>
                    <span style="color: #3b82f6; font-size: 0.82rem; font-weight: 600;">TXN-1032 ↗</span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-low">LOW</span>
                        <strong style="color: var(--text-primary);">Devendra Patil</strong> &bull; <span style="color: var(--text-secondary);">₹49,500 to India</span>
                    </div>
                    <span style="color: #3b82f6; font-size: 0.82rem; font-weight: 600;">TXN-1031 ↗</span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-crit">CRITICAL</span>
                        <strong style="color: var(--text-primary);">Hon. Rameshwar Prasad</strong> &bull; <span style="color: var(--text-secondary);">₹8,50,000 to Switzerland</span>
                    </div>
                    <span style="color: #3b82f6; font-size: 0.82rem; font-weight: 600;">TXN-1040 ↗</span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-crit">CRITICAL</span>
                        <strong style="color: var(--text-primary);">Global Trade Nexus LLC</strong> &bull; <span style="color: var(--text-secondary);">₹18,50,000 to Vanuatu</span>
                    </div>
                    <span style="color: #3b82f6; font-size: 0.82rem; font-weight: 600;">TXN-1051 ↗</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with b_col2:
        st.markdown("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <strong style="color: var(--text-primary); font-size: 1rem;">Monitored Corridors</strong>
                <span style="color: #06b6d4;">🌐</span>
            </div>
            
            <div style="margin-top: 8px;">
                <div class="alert-row">
                    <span style="color: var(--text-secondary); font-size: 0.85rem;">117 transactions total</span>
                    <div style="text-align: right;">
                        <span style="color: #ef4444; font-weight: 700; font-size: 0.85rem;">10 Flagged</span><br>
                        <span style="color: var(--text-muted); font-size: 0.75rem;">₹79,83,759.65</span>
                    </div>
                </div>
                <div class="alert-row">
                    <span style="color: var(--text-secondary); font-size: 0.85rem;">1 transactions total</span>
                    <div style="text-align: right;">
                        <span style="color: #ef4444; font-weight: 700; font-size: 0.85rem;">1 Flagged</span><br>
                        <span style="color: var(--text-muted); font-size: 0.75rem;">₹12,50,000</span>
                    </div>
                </div>
                <div class="alert-row">
                    <span style="color: var(--text-secondary); font-size: 0.85rem;">1 transactions total</span>
                    <div style="text-align: right;">
                        <span style="color: #ef4444; font-weight: 700; font-size: 0.85rem;">1 Flagged</span><br>
                        <span style="color: var(--text-muted); font-size: 0.75rem;">₹6,80,000</span>
                    </div>
                </div>
                <div class="alert-row">
                    <span style="color: var(--text-secondary); font-size: 0.85rem;">1 transactions total</span>
                    <div style="text-align: right;">
                        <span style="color: #ef4444; font-weight: 700; font-size: 0.85rem;">1 Flagged</span><br>
                        <span style="color: var(--text-muted); font-size: 0.75rem;">₹8,50,000</span>
                    </div>
                </div>
                <div class="alert-row">
                    <span style="color: var(--text-secondary); font-size: 0.85rem;">1 transactions total</span>
                    <div style="text-align: right;">
                        <span style="color: #ef4444; font-weight: 700; font-size: 0.85rem;">1 Flagged</span><br>
                        <span style="color: var(--text-muted); font-size: 0.75rem;">₹18,50,000</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 9. VIEW: NEURAL COPILOT ASSISTANT
# ------------------------------------------------------------------------------
elif st.session_state.active_nav == "Copilot":
    st.subheader("🧠 Astra AI Neural Copilot Assistant")
    st.caption("Real-Time Financial Crime, AML & Regulatory Guidance")

    if "copilot_history" not in st.session_state:
        st.session_state.copilot_history = [
            {"role": "assistant", "content": "👋 Greetings, Senior Risk Officer. I am Astra AI. I have analyzed your transaction stream, 14 flagged alerts, and high-risk customer profiles. How can I assist you with regulatory investigation or SAR narrative drafting?"}
        ]

    for m in st.session_state.copilot_history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    init_prompt = st.session_state.copilot_query or ""
    prompt = st.chat_input("Ask Astra AI...", key="copilot_chat_input")
    if init_prompt and not prompt:
        prompt = init_prompt
        st.session_state.copilot_query = ""

    if prompt:
        st.session_state.copilot_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Astra Neural Copilot is reasoning..."):
                p_lower = prompt.lower()
                if "1024" in p_lower or "singhania" in p_lower:
                    ans = """### 🛡️ Flag Evaluation: Transaction TXN-1024
- **Customer**: Vikramaditya Singhania (CUST-1008)
- **Amount**: ₹12,50,000.00 to *Cayman Islands*
- **Triggered Rules**:
  1. `AML-R01`: Large Value Customer Due Diligence (Threshold > ₹10,00,000)
  2. `AML-R03`: High-Risk Offshore Secrecy Jurisdiction (FATF Grey/Monitoring List)
- **Recommended Remediation**:
  - Issue urgent Request for Information (RFI) for beneficial ownership.
  - Escalate to Case `CASE-4091` for FIU Suspicious Activity Report (SAR) filing."""
                elif "sar" in p_lower or "draft" in p_lower:
                    ans = """### 📋 Draft SAR Filing Narrative
**Subject**: Vikramaditya Singhania (CUST-1008)  
**Reporting Jurisdiction**: Financial Intelligence Unit (FIU)  

**Summary of Suspicious Activity**:
Between Oct 01 and Oct 05, subject engaged in multiple high-velocity outbound transfers totaling ₹19,30,000.00 to offshore jurisdictions (Panama & Cayman Islands) with no verifiable commercial rationale. Prior monthly average was ₹1,80,000.00. Funds were aggregated from rapid inbound domestic wires and immediately wired out, presenting classic indicators of Layering and Trade-Based Money Laundering."""
                else:
                    ans = f"### 🧠 Astra AI Regulatory Reasoning\nI have evaluated: **\"{prompt}\"** against your compliance database (121 total transactions, 14 flagged).\n\n- **Risk Status**: 4 Critical risk items requiring MLRO signoff.\n- **Action**: All audit evidence has been preserved in compliance logs."

                st.markdown(ans)
                st.session_state.copilot_history.append({"role": "assistant", "content": ans})

# ------------------------------------------------------------------------------
# 10. VIEW: TRANSACTIONS & CUSTOMERS
# ------------------------------------------------------------------------------
elif st.session_state.active_nav in ["Transactions", "Alerts"]:
    st.subheader("⚡ Live Transaction Surveillance Ledger")
    tx_df = pd.DataFrame([
        {"Tx ID": "TXN-1024", "Customer": "Vikramaditya Singhania", "Amount": "₹12,50,000.00", "Destination": "Cayman Islands", "Risk": "CRITICAL", "Anomaly Score": 0.94, "Status": "FLAGGED"},
        {"Tx ID": "TXN-1025", "Customer": "Vikramaditya Singhania", "Amount": "₹6,80,000.00", "Destination": "Panama", "Risk": "CRITICAL", "Anomaly Score": 0.92, "Status": "FLAGGED"},
        {"Tx ID": "TXN-1040", "Customer": "Hon. Rameshwar Prasad", "Amount": "₹8,50,000.00", "Destination": "Switzerland", "Risk": "CRITICAL", "Anomaly Score": 0.91, "Status": "FLAGGED"},
        {"Tx ID": "TXN-1051", "Customer": "Global Trade Nexus LLC", "Amount": "₹18,50,000.00", "Destination": "Vanuatu", "Risk": "CRITICAL", "Anomaly Score": 0.89, "Status": "FLAGGED"},
        {"Tx ID": "TXN-1034", "Customer": "Devendra Patil", "Amount": "₹49,800.00", "Destination": "India", "Risk": "MEDIUM", "Anomaly Score": 0.65, "Status": "FLAGGED"},
        {"Tx ID": "TXN-1033", "Customer": "Devendra Patil", "Amount": "₹48,900.00", "Destination": "India", "Risk": "MEDIUM", "Anomaly Score": 0.64, "Status": "FLAGGED"},
        {"Tx ID": "TXN-1031", "Customer": "Devendra Patil", "Amount": "₹49,500.00", "Destination": "India", "Risk": "LOW", "Anomaly Score": 0.32, "Status": "CLEARED"},
    ])
    st.dataframe(tx_df, use_container_width=True)

elif st.session_state.active_nav == "Customers":
    st.subheader("👥 Customer AML & KYC Profiles")
    cust_df = pd.DataFrame([
        {"Customer ID": "CUST-1008", "Full Name": "Vikramaditya Singhania", "KYC Status": "Enhanced Due Diligence", "Risk Score": 88, "Risk Level": "HIGH", "PEP": "Yes"},
        {"Customer ID": "CUST-1004", "Full Name": "Hon. Rameshwar Prasad", "KYC Status": "Enhanced Due Diligence", "Risk Score": 82, "Risk Level": "HIGH", "PEP": "Yes"},
        {"Customer ID": "CUST-1003", "Full Name": "Devendra Patil", "KYC Status": "Verified", "Risk Score": 78, "Risk Level": "HIGH", "PEP": "No"},
        {"Customer ID": "CUST-1005", "Full Name": "Global Trade Nexus LLC", "KYC Status": "Verified", "Risk Score": 68, "Risk Level": "MEDIUM", "PEP": "No"},
        {"Customer ID": "CUST-1001", "Full Name": "Ananya Sharma", "KYC Status": "Verified", "Risk Score": 12, "Risk Level": "LOW", "PEP": "No"},
    ])
    st.dataframe(cust_df, use_container_width=True)

else:
    st.subheader(f"📋 {st.session_state.active_nav}")
    st.info("Statutory investigation queue active. 2 cases pending final FIU signoff.")

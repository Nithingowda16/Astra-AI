# ==============================================================================
# Astra AI — Enterprise Risk & Regulatory Intelligence Platform
# Complete Apple Design System: SF Pro Font, Curvy Pills, Native iOS Toggle
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import base64
import os

# Helper to render clean HTML without CommonMark code block parsing
def render_html(html_str):
    clean = "\n".join([line.lstrip() for line in html_str.splitlines() if line.strip()])
    st.markdown(clean, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 1. Page Configuration (Zero Emojis, Pure Apple Enterprise)
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Astra AI - Risk & Regulatory Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# 2. State Initialization
# ------------------------------------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
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
if "copilot_history" not in st.session_state:
    st.session_state.copilot_history = [
        {
            "role": "assistant",
            "title": "INVESTIGATION COPILOT",
            "content": "Greetings, Senior Risk Officer. I am Astra AI. I have correlated your live transaction ledger, 14 flagged events, and high-risk customer profiles against the Regulatory Knowledge Base. How can I assist with your statutory investigation or SAR filing?"
        }
    ]

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

is_auth = st.session_state.authenticated
# Strictly Dark Mode on Login Page (login page is exclusively dark mode, no light mode)
current_theme = "dark" if not is_auth else st.session_state.theme
current_logo_b64 = logo_dark_b64 if (not is_auth or current_theme == "dark") else logo_light_b64
current_bg_b64 = bg_dark_b64 if (not is_auth or current_theme == "dark") else bg_light_b64

# ------------------------------------------------------------------------------
# 4. Master Apple Design System Stylesheet
# ------------------------------------------------------------------------------
apple_css = f"""
<style>
    @import url('https://fonts.cdnfonts.com/css/sf-pro-display');
    
    /* Global Apple Typography */
    html, body, [class*="css"], [class*="st-"], button, input, select, textarea, div, p, span, h1, h2, h3, h4, label {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "SF Pro", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        letter-spacing: -0.015em !important;
    }}
    
    /* 1. HIDE ALL BROKEN MATERIAL LIGATURE TEXTS */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"],
    [data-testid="stIconMaterial"],
    button[aria-label="Show password text"],
    button[aria-label="Hide password text"],
    [data-testid="stTextInput"] button {{
        display: none !important;
    }}
    
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    
    .block-container {{
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1440px !important;
    }}
    
    /* Apple Color Palette */
    :root {{
        --apple-bg: {'#f5f5f7' if current_theme == 'light' else '#000000'};
        --apple-card: {'#ffffff' if current_theme == 'light' else '#1c1c1e'};
        --apple-card-hover: {'#f0f0f2' if current_theme == 'light' else '#2c2c2e'};
        --apple-sidebar: {'#ffffff' if current_theme == 'light' else '#121214'};
        --apple-border: {'rgba(0, 0, 0, 0.08)' if current_theme == 'light' else 'rgba(255, 255, 255, 0.08)'};
        --apple-border-subtle: {'rgba(0, 0, 0, 0.04)' if current_theme == 'light' else 'rgba(255, 255, 255, 0.04)'};
        --apple-text-primary: {'#1d1d1f' if current_theme == 'light' else '#f5f5f7'};
        --apple-text-secondary: {'#6e6e73' if current_theme == 'light' else '#a1a1a6'};
        --apple-text-muted: {'#86868b' if current_theme == 'light' else '#636366'};
        --apple-blue: {'#0071e3' if current_theme == 'light' else '#0a84ff'};
        --apple-blue-hover: {'#0077ed' if current_theme == 'light' else '#409cff'};
        --apple-green: #34c759;
        --apple-red: #ff3b30;
        --apple-orange: #ff9500;
        --apple-yellow: #ffcc00;
    }}
    
    /* Main View Container */
    [data-testid="stAppViewContainer"] {{
        background-color: var(--apple-bg) !important;
        {'background-image: url("data:image/png;base64,' + current_bg_b64 + '") !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important;' if not is_auth else 'background-image: none !important;'}
    }}
    
    /* High-Contrast Text Rules */
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stMarkdownContainer"] p {{
        color: var(--apple-text-primary);
    }}
    
    /* 2. APPLE NATIVE iOS TOGGLE SWITCH (PURE TOGGLE CASE, ZERO WORDS) */
    [data-testid="stToggle"] {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    [data-testid="stToggle"] label {{
        cursor: pointer !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    [data-testid="stToggle"] label p,
    [data-testid="stToggle"] label span,
    [data-testid="stToggle"] [data-testid="stMarkdownContainer"] {{
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    [data-testid="stToggle"] div[data-baseweb="checkbox"] {{
        margin: 0 !important;
    }}
    
    /* 3. APPLE CURVY BUTTONS & PILLS (MAIN AREA) */
    [data-testid="stMain"] div[data-testid="column"] button,
    [data-testid="stMain"] .stButton button,
    [data-testid="stMain"] [data-testid="stFormSubmitButton"] button,
    .main div[data-testid="column"] button,
    .main .stButton button,
    .main [data-testid="stFormSubmitButton"] button,
    div[data-testid="stMainBlockContainer"] .stButton button {{
        border-radius: 9999px !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }}
    
    /* Secondary Apple Curvy Pills (Main Area Only) */
    [data-testid="stMain"] div[data-testid="column"] button:not([kind="primary"]),
    [data-testid="stMain"] .stButton button:not([kind="primary"]),
    .main div[data-testid="column"] button:not([kind="primary"]),
    .main .stButton button:not([kind="primary"]),
    div[data-testid="stMainBlockContainer"] .stButton button:not([kind="primary"]) {{
        background-color: var(--apple-card) !important;
        color: var(--apple-text-primary) !important;
        border: 1px solid var(--apple-border) !important;
        padding: 9px 18px !important;
        text-align: left !important;
        justify-content: flex-start !important;
        margin-bottom: 6px !important;
        width: 100% !important;
        border-radius: 9999px !important;
    }}
    [data-testid="stMain"] div[data-testid="column"] button:not([kind="primary"]) p,
    [data-testid="stMain"] .stButton button:not([kind="primary"]) p,
    .main .stButton button:not([kind="primary"]) p,
    div[data-testid="stMainBlockContainer"] .stButton button:not([kind="primary"]) p {{
        color: var(--apple-text-primary) !important;
        text-align: left !important;
        margin: 0 !important;
    }}
    [data-testid="stMain"] div[data-testid="column"] button:not([kind="primary"]):hover,
    [data-testid="stMain"] .stButton button:not([kind="primary"]):hover,
    .main .stButton button:not([kind="primary"]):hover,
    div[data-testid="stMainBlockContainer"] .stButton button:not([kind="primary"]):hover {{
        background-color: var(--apple-card-hover) !important;
        border-color: var(--apple-blue) !important;
        transform: translateY(-1px);
    }}
    [data-testid="stMain"] div[data-testid="column"] button:not([kind="primary"]):hover p,
    [data-testid="stMain"] .stButton button:not([kind="primary"]):hover p,
    .main .stButton button:not([kind="primary"]):hover p,
    div[data-testid="stMainBlockContainer"] .stButton button:not([kind="primary"]):hover p {{
        color: var(--apple-blue) !important;
    }}
    
    /* Primary Apple System Blue Curvy Buttons (Main Area) */
    [data-testid="stMain"] button[kind="primary"],
    [data-testid="stMain"] [data-testid="stFormSubmitButton"] button,
    button[key="copilot_send_btn"],
    .main button[kind="primary"],
    .main [data-testid="stFormSubmitButton"] button {{
        background-color: var(--apple-blue) !important;
        color: #ffffff !important;
        border: 1px solid var(--apple-blue) !important;
        border-radius: 9999px !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        text-align: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 14px rgba(0, 113, 227, 0.28) !important;
    }}
    [data-testid="stMain"] button[kind="primary"] p,
    [data-testid="stMain"] [data-testid="stForm"] button p,
    button[key="copilot_send_btn"] p,
    .main button[kind="primary"] p {{
        color: #ffffff !important;
        text-align: center !important;
        white-space: nowrap !important;
    }}
    [data-testid="stMain"] button[kind="primary"]:hover,
    [data-testid="stMain"] [data-testid="stForm"] button:hover,
    button[key="copilot_send_btn"]:hover,
    .main button[kind="primary"]:hover {{
        background-color: var(--apple-blue-hover) !important;
        transform: translateY(-1px);
    }}
    
    /* 4. APPLE macOS SIDEBAR NAVIGATION */
    [data-testid="stSidebar"] {{
        background-color: var(--apple-sidebar) !important;
        border-right: 1px solid var(--apple-border) !important;
    }}
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {{
        color: var(--apple-text-primary);
    }}
    
    /* Clean sidebar block spacing */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        gap: 0.35rem !important;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        margin: 0 !important;
    }}
    
    /* Sidebar Section Headers (macOS Hierarchy & Spacing) */
    .sidebar-section-header {{
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        color: var(--apple-text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        padding: 16px 12px 12px 12px !important;
        margin-top: 10px !important;
        margin-bottom: 8px !important;
        display: block !important;
        width: 100% !important;
        box-sizing: border-box !important;
        line-height: 1.4 !important;
        min-height: 42px !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(.sidebar-section-header) {{
        min-height: 42px !important;
        display: block !important;
    }}

    [data-testid="stSidebar"] .stButton {{
        margin: 0 !important;
        margin-bottom: 2px !important;
    }}
    
    /* Inactive Sidebar Buttons - Pure macOS Flat Item (No White Card, No Border!) */
    [data-testid="stSidebar"] .stButton button,
    [data-testid="stSidebar"] .stButton button:not([kind="primary"]),
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"],
    [data-testid="stSidebar"] button {{
        width: 100% !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        border: 1px solid transparent !important;
        text-align: left !important;
        justify-content: flex-start !important;
        margin: 0 !important;
        margin-bottom: 2px !important;
        box-shadow: none !important;
        background: transparent !important;
        background-color: transparent !important;
        transition: background-color 0.15s cubic-bezier(0.16, 1, 0.3, 1), color 0.15s ease !important;
    }}
    [data-testid="stSidebar"] .stButton button div,
    [data-testid="stSidebar"] .stButton button p,
    [data-testid="stSidebar"] button div,
    [data-testid="stSidebar"] button p {{
        text-align: left !important;
        justify-content: flex-start !important;
        width: 100% !important;
        margin: 0 !important;
        color: var(--apple-text-primary) !important;
        font-weight: 500 !important;
    }}
    
    /* Inactive Sidebar Buttons Hover */
    [data-testid="stSidebar"] .stButton button:hover,
    [data-testid="stSidebar"] .stButton button:not([kind="primary"]):hover,
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover,
    [data-testid="stSidebar"] button:hover {{
        background: {'rgba(0, 0, 0, 0.05)' if current_theme == 'light' else 'rgba(255, 255, 255, 0.08)'} !important;
        background-color: {'rgba(0, 0, 0, 0.05)' if current_theme == 'light' else 'rgba(255, 255, 255, 0.08)'} !important;
        border-color: transparent !important;
        color: var(--apple-text-primary) !important;
        transform: none !important;
    }}
    [data-testid="stSidebar"] .stButton button:hover p,
    [data-testid="stSidebar"] button:hover p {{
        color: var(--apple-text-primary) !important;
    }}
    
    /* Active Sidebar Button - Apple System Blue macOS Pill */
    [data-testid="stSidebar"] .stButton button[kind="primary"],
    [data-testid="stSidebar"] button[data-testid="baseButton-primary"] {{
        background: var(--apple-blue) !important;
        background-color: var(--apple-blue) !important;
        color: #ffffff !important;
        border: 1px solid var(--apple-blue) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0, 113, 227, 0.28) !important;
        transform: none !important;
    }}
    [data-testid="stSidebar"] .stButton button[kind="primary"] p,
    [data-testid="stSidebar"] .stButton button[kind="primary"] div,
    [data-testid="stSidebar"] button[data-testid="baseButton-primary"] p,
    [data-testid="stSidebar"] button[data-testid="baseButton-primary"] div {{
        color: #ffffff !important;
        font-weight: 600 !important;
        text-align: left !important;
    }}
    [data-testid="stSidebar"] .stButton button[kind="primary"]:hover,
    [data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover {{
        background: var(--apple-blue-hover) !important;
        background-color: var(--apple-blue-hover) !important;
        color: #ffffff !important;
        transform: none !important;
    }}
    [data-testid="stSidebar"] .stButton button[kind="primary"]:hover p,
    [data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover p {{
        color: #ffffff !important;
    }}

    /* Sidebar iOS Theme Toggle (Pure Toggle Case, Zero Words) */
    [data-testid="stSidebar"] div[data-testid="stToggle"],
    [data-testid="stSidebar"] div.stToggle,
    [data-testid="stSidebar"] div[data-testid="stCheckbox"] {{
        width: 100% !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 4px 0 !important;
        margin: 6px 0 !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stToggle"] label,
    [data-testid="stSidebar"] div.stToggle label,
    [data-testid="stSidebar"] div[data-testid="stCheckbox"] label {{
        width: auto !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        margin: 0 !important;
        padding: 0 !important;
        gap: 0 !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stToggle"] label p,
    [data-testid="stSidebar"] div.stToggle label p,
    [data-testid="stSidebar"] div[data-testid="stCheckbox"] label p,
    [data-testid="stSidebar"] div[data-testid="stToggle"] [data-testid="stMarkdownContainer"] {{
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="checkbox"] {{
        margin: 0 auto !important;
    }}

    /* Sign Out Action Button in Sidebar (Apple Soft Red Action) */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:last-child button,
    [data-testid="stSidebar"] button[key="sidebar_logout_btn"],
    button[key="sidebar_logout_btn"] {{
        background: rgba(255, 59, 48, 0.06) !important;
        background-color: rgba(255, 59, 48, 0.06) !important;
        border: 1px solid rgba(255, 59, 48, 0.22) !important;
        color: #ff3b30 !important;
        border-radius: 10px !important;
        padding: 8px 14px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        text-align: center !important;
        justify-content: center !important;
        margin-top: 4px !important;
        margin-bottom: 12px !important;
        box-shadow: none !important;
        width: 100% !important;
        transition: all 0.15s ease !important;
    }}
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:last-child button p,
    button[key="sidebar_logout_btn"] p {{
        color: #ff3b30 !important;
        text-align: center !important;
        width: 100% !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:last-child button:hover,
    button[key="sidebar_logout_btn"]:hover {{
        background: rgba(255, 59, 48, 0.12) !important;
        background-color: rgba(255, 59, 48, 0.12) !important;
        border-color: #ff3b30 !important;
        color: #ff3b30 !important;
        transform: translateY(-1px) !important;
    }}
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:last-child button:hover p,
    button[key="sidebar_logout_btn"]:hover p {{
        color: #ff3b30 !important;
    }}
    
    /* 5. APPLE SQUIRCLE CARDS */
    .kpi-stat-card {{
        background: var(--apple-card);
        border: 1px solid var(--apple-border);
        border-radius: 20px !important;
        padding: 22px 24px;
        box-shadow: {'0 4px 20px -2px rgba(0, 0, 0, 0.04), 0 0 1px 1px rgba(0, 0, 0, 0.02)' if current_theme == 'light' else '0 4px 24px -2px rgba(0, 0, 0, 0.6), 0 0 1px 1px rgba(255, 255, 255, 0.04)'};
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .kpi-stat-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }}
    .kpi-stat-label {{
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--apple-text-secondary);
    }}
    .kpi-stat-val {{
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        color: var(--apple-text-primary);
        line-height: 1.1;
        margin: 4px 0 6px 0;
    }}
    .kpi-stat-sub {{
        font-size: 0.78rem;
        color: var(--apple-text-muted);
    }}
    
    /* 6. APPLE MODAL AUTH CARD */
    [data-testid="stForm"] {{
        background: {'rgba(255, 255, 255, 0.95)' if current_theme == 'light' else 'rgba(28, 28, 30, 0.95)'} !important;
        border: 1px solid var(--apple-border) !important;
        border-radius: 28px !important;
        padding: 36px 40px !important;
        box-shadow: {'0 30px 60px -12px rgba(0, 0, 0, 0.12), 0 0 1px 1px rgba(0, 0, 0, 0.04)' if current_theme == 'light' else '0 30px 60px -12px rgba(0, 0, 0, 0.8), 0 0 1px 1px rgba(255, 255, 255, 0.06)'} !important;
        max-width: 480px !important;
        margin: 0 auto !important;
    }}
    /* 6. APPLE INPUTS & SELECTBOXES (Zero Black Corners, Clean Apple Surfaces) */
    [data-testid="stTextInput"] {{
        background: transparent !important;
        background-color: transparent !important;
        margin-bottom: 2px !important;
    }}
    
    /* Outer Input Container - holds the background, border, and squircle corners */
    [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stTextInput"] div[data-baseweb="base-input"],
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {{
        background-color: {'#f5f5f7' if current_theme == 'light' else '#1c1c1e'} !important;
        background: {'#f5f5f7' if current_theme == 'light' else '#1c1c1e'} !important;
        border: 1px solid var(--apple-border) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: none !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }}
    
    /* Focused Input Border - Apple System Blue Glow */
    [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
    [data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within,
    div[data-baseweb="input"]:focus-within {{
        border-color: var(--apple-blue) !important;
        box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.2) !important;
    }}
    
    /* Inner Native Input Field - completely transparent, filling the container */
    [data-testid="stTextInput"] input,
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        outline: none !important;
        box-shadow: none !important;
        color: var(--apple-text-primary) !important;
        padding: 9px 14px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.01em !important;
    }}
    
    /* BaseWeb Selectbox - Apple Flat Surface */
    [data-testid="stSelectbox"] div[data-baseweb="select"],
    div[data-baseweb="select"] {{
        background-color: {'#f5f5f7' if current_theme == 'light' else '#1c1c1e'} !important;
        background: {'#f5f5f7' if current_theme == 'light' else '#1c1c1e'} !important;
        border: 1px solid var(--apple-border) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: none !important;
    }}
    
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        color: var(--apple-text-primary) !important;
        padding: 4px 10px !important;
    }}
    
    [data-testid="stSelectbox"] div[data-baseweb="select"] [role="combobox"],
    div[data-baseweb="select"] [role="combobox"] {{
        background: transparent !important;
        background-color: transparent !important;
        color: var(--apple-text-primary) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }}
    
    /* Remove pill button styling from selectbox chevron */
    [data-testid="stSelectbox"] button,
    div[data-baseweb="select"] button {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: 0 6px !important;
        width: auto !important;
        min-width: 0 !important;
        color: var(--apple-text-secondary) !important;
    }}
    [data-testid="stSelectbox"] svg,
    div[data-baseweb="select"] svg {{
        fill: var(--apple-text-secondary) !important;
        color: var(--apple-text-secondary) !important;
    }}

    /* 7. ALERT ROWS */
    .alert-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 14px;
        border-bottom: 1px solid var(--apple-border);
        transition: background-color 0.15s ease;
    }}
    .alert-row:hover {{
        background-color: var(--apple-card-hover);
        border-radius: 10px;
    }}
    .alert-row:last-child {{
        border-bottom: none;
    }}
    
    .badge-crit {{
        background: rgba(255, 59, 48, 0.12);
        color: var(--apple-red);
        border: 1px solid rgba(255, 59, 48, 0.25);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-right: 8px;
    }}
    .badge-med {{
        background: rgba(255, 149, 0, 0.12);
        color: var(--apple-orange);
        border: 1px solid rgba(255, 149, 0, 0.25);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-right: 8px;
    }}
    .badge-low {{
        background: rgba(52, 199, 89, 0.12);
        color: var(--apple-green);
        border: 1px solid rgba(52, 199, 89, 0.25);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-right: 8px;
    }}
    
    /* 8. COPILOT CHAT BUBBLES */
    .chat-bubble-copilot {{
        background: var(--apple-card);
        border: 1px solid var(--apple-border);
        border-radius: 18px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: {'0 2px 8px rgba(0,0,0,0.03)' if current_theme == 'light' else '0 3px 14px rgba(0,0,0,0.4)'};
    }}
    .chat-bubble-user {{
        background: {'rgba(0, 113, 227, 0.08)' if current_theme == 'light' else 'rgba(10, 132, 255, 0.15)'};
        border: 1px solid {'rgba(0, 113, 227, 0.25)' if current_theme == 'light' else 'rgba(10, 132, 255, 0.3)'};
        border-radius: 18px;
        padding: 14px 20px;
        margin-bottom: 14px;
    }}
    .chat-badge-copilot {{
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: var(--apple-blue);
        margin-bottom: 8px;
    }}
    .chat-badge-user {{
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: var(--apple-blue);
        margin-bottom: 6px;
    }}
</style>
"""
st.markdown(apple_css, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 5. AUTHENTICATION GATEWAY (Apple Curvy Design, Zero Emojis)
# ------------------------------------------------------------------------------
if not st.session_state.authenticated:
    _, auth_center_col, _ = st.columns([1, 1.3, 1])
    
    with auth_center_col:
        st.write("")
        logo_html = f'<img src="data:image/png;base64,{current_logo_b64}" style="width: 58px; height: 58px; object-fit: contain; margin: 0 auto 10px auto; display: block; filter: drop-shadow(0 4px 14px rgba(19, 214, 214, 0.35));" alt="Astra AI" />' if current_logo_b64 else ''
        
        render_html(f"""
        <div style="text-align: center; margin-bottom: 18px;">
            {logo_html}
            <h1 style="font-size: 2.1rem; font-weight: 800; letter-spacing: -0.035em; color: var(--apple-text-primary); margin: 0 0 4px 0;">Astra AI</h1>
            <div style="font-size: 0.88rem; color: var(--apple-text-secondary); font-weight: 500;">Risk, Fraud & Regulatory Intelligence Copilot</div>
        </div>
        """)
        
        # Apple Curvy Pill Tab Switcher
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            if st.button("Sign In", key="pill_signin", use_container_width=True, type="primary" if st.session_state.auth_tab == "signin" else "secondary"):
                st.session_state.auth_tab = "signin"
                st.rerun()
        with tab_col2:
            if st.button("Sign Up", key="pill_signup", use_container_width=True, type="primary" if st.session_state.auth_tab == "signup" else "secondary"):
                st.session_state.auth_tab = "signup"
                st.rerun()
                
        st.write("")
        
        # FORM: SIGN IN
        if st.session_state.auth_tab == "signin":
            with st.form("signin_form"):
                render_html('<div style="font-size: 0.82rem; font-weight: 600; color: var(--apple-text-secondary); margin-bottom: 4px;">Username or Email Address</div>')
                in_user = st.text_input("Username or Email", value="senior.risk.officer@bank.internal", label_visibility="collapsed")
                
                render_html('<div style="font-size: 0.82rem; font-weight: 600; color: var(--apple-text-secondary); margin-bottom: 4px; margin-top: 10px;">Password</div>')
                in_pwd = st.text_input("Password", value="••••••••••••", type="password", label_visibility="collapsed")
                
                st.write("")
                submit_signin = st.form_submit_button("Authenticate Access", use_container_width=True, type="primary")
                if submit_signin:
                    st.session_state.authenticated = True
                    st.session_state.user_name = in_user.split("@")[0].replace(".", " ").title() if "@" in in_user else in_user.title()
                    st.session_state.user_role = "Senior Risk Officer"
                    st.rerun()
        
        # FORM: SIGN UP
        else:
            with st.form("signup_form"):
                render_html('<div style="font-size: 0.82rem; font-weight: 600; color: var(--apple-text-secondary); margin-bottom: 4px;">Full Name</div>')
                su_fullname = st.text_input("Full Name", value="Senior Risk Analyst", label_visibility="collapsed")
                
                f_c1, f_c2 = st.columns(2)
                with f_c1:
                    render_html('<div style="font-size: 0.82rem; font-weight: 600; color: var(--apple-text-secondary); margin-bottom: 4px;">Username</div>')
                    su_user = st.text_input("Username", value="risk_analyst", label_visibility="collapsed")
                with f_c2:
                    render_html('<div style="font-size: 0.82rem; font-weight: 600; color: var(--apple-text-secondary); margin-bottom: 4px;">Business Email</div>')
                    su_email = st.text_input("Business Email", value="analyst@bank.internal", label_visibility="collapsed")
                    
                p_c1, p_c2 = st.columns(2)
                with p_c1:
                    render_html('<div style="font-size: 0.82rem; font-weight: 600; color: var(--apple-text-secondary); margin-bottom: 4px;">Password</div>')
                    su_pwd = st.text_input("Password", value="••••••••••••", type="password", label_visibility="collapsed")
                with p_c2:
                    render_html('<div style="font-size: 0.82rem; font-weight: 600; color: var(--apple-text-secondary); margin-bottom: 4px;">Account Role</div>')
                    su_role = st.selectbox("Role", ["Senior Risk Officer", "AML Investigator", "Compliance Auditor", "Executive MLRO"], label_visibility="collapsed")
                    
                st.write("")
                submit_signup = st.form_submit_button("Register Compliance Account", use_container_width=True, type="primary")
                if submit_signup:
                    st.session_state.authenticated = True
                    st.session_state.user_name = su_fullname
                    st.session_state.user_role = su_role
                    st.rerun()

    st.stop()

# ------------------------------------------------------------------------------
# 6. AUTHENTICATED NAVIGATION & SIDEBAR (macOS Style, Zero Emojis)
# ------------------------------------------------------------------------------

with st.sidebar:
    # Brand Header
    logo_side_html = f'<img src="data:image/png;base64,{current_logo_b64}" width="34" height="34" style="object-fit: contain; vertical-align: middle; margin-right: 10px;" />' if current_logo_b64 else ''
    render_html(f"""
    <div style="display: flex; align-items: center; padding: 4px 0 14px 0; border-bottom: 1px solid var(--apple-border); margin-bottom: 12px;">
        {logo_side_html}
        <div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--apple-text-primary); letter-spacing: -0.025em;">Astra AI</div>
            <div style="font-size: 0.64rem; font-weight: 700; color: var(--apple-text-muted); letter-spacing: 0.07em; text-transform: uppercase;">Risk & Regulatory Intelligence</div>
        </div>
    </div>
    """)
    
    render_html('<div class="sidebar-section-header" style="margin-top: 8px; margin-bottom: 10px; padding-bottom: 12px;">OPERATIONS</div>')
    
    nav_ops = [
        ("Dashboard", "Dashboard"),
        ("Transactions", "Transactions"),
        ("Customers", "Customers"),
        ("Alerts", "Alerts (8)"),
        ("Investigations", "Investigations (2)")
    ]
    for key, label in nav_ops:
        is_active = st.session_state.active_nav == key
        if st.button(label, key=f"nav_{key}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.active_nav = key
            st.rerun()

    render_html('<div class="sidebar-section-header" style="margin-top: 26px; margin-bottom: 10px; padding-bottom: 12px;">AI & INTELLIGENCE</div>')
    
    if st.button("Regulatory Rules", key="nav_rules", use_container_width=True, type="primary" if st.session_state.active_nav == "Regulatory" else "secondary"):
        st.session_state.active_nav = "Regulatory"
        st.rerun()
        
    if st.button("Copilot Assistant", key="nav_copilot", use_container_width=True, type="primary" if st.session_state.active_nav == "Copilot" else "secondary"):
        st.session_state.active_nav = "Copilot"
        st.rerun()

    # User Profile Box (Apple macOS Identity Card)
    raw_user_name = getattr(st.session_state, "user_name", "Risk Officer")
    raw_user_role = getattr(st.session_state, "user_role", "Senior Risk Officer")
    
    # Concise name that fits comfortably without truncation in narrow sidebars
    if not raw_user_name or raw_user_name in ["Senior Risk Officer", "Alexander Wright"]:
        display_name = "Alex Wright"
        display_role = "Senior Risk Officer"
    else:
        parts = raw_user_name.split()
        if len(parts) > 1 and len(raw_user_name) > 13:
            display_name = f"{parts[0]} {parts[1][0]}."
        else:
            display_name = raw_user_name
        display_role = raw_user_role
        
    initials = "".join([part[0] for part in display_name.split()[:2]]).upper() if display_name else "AW"
    
    render_html(f"""
    <div style="background: var(--apple-card); border: 1px solid var(--apple-border); border-radius: 12px; padding: 12px 14px; margin-top: 22px; margin-bottom: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg, #0071e3, #409cff); color: #ffffff; display: flex; align-items: center; justify-content: center; font-size: 0.78rem; font-weight: 700; flex-shrink: 0; box-shadow: 0 2px 6px rgba(0, 113, 227, 0.28);">
                {initials}
            </div>
            <div style="min-width: 0; flex: 1;">
                <div style="font-size: 0.84rem; font-weight: 700; color: var(--apple-text-primary); line-height: 1.2;">{display_name}</div>
                <div style="font-size: 0.7rem; color: var(--apple-text-muted); margin-top: 2px; line-height: 1.2;">{display_role}</div>
            </div>
        </div>
        <div style="margin-top: 9px; padding-top: 8px; border-top: 1px solid var(--apple-border-subtle); display: flex; align-items: center; gap: 6px;">
            <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #34c759; box-shadow: 0 0 6px rgba(52, 199, 89, 0.6); flex-shrink: 0;"></span>
            <span style="font-size: 0.68rem; font-weight: 600; color: var(--apple-green); letter-spacing: 0.02em;">Verified AML Analyst</span>
        </div>
    </div>
    """)
    
    # Apple iOS Theme Toggle Bar (Pure Toggle Case, Zero Words)
    is_dark_active = st.session_state.theme == "dark"
    theme_toggle_val = st.toggle("", value=is_dark_active, key="sidebar_theme_toggle", label_visibility="collapsed")
    if theme_toggle_val != is_dark_active:
        st.session_state.theme = "dark" if theme_toggle_val else "light"
        st.rerun()

    if st.button("Sign Out", key="sidebar_logout_btn", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- TOP HEADER ROW (Breadcrumbs + Live Engine Status) ---
h_c1, h_c2 = st.columns([7.5, 2.5])
with h_c1:
    render_html(f"""
    <div style="font-size: 0.92rem; color: var(--apple-text-secondary); padding-top: 5px; font-weight: 500; letter-spacing: -0.015em;">
        <span>Astra AI</span> <span style="opacity: 0.35; margin: 0 4px;">/</span> <strong style="color: var(--apple-text-primary);">{st.session_state.active_nav}</strong>
    </div>
    """)

with h_c2:
    render_html("""
    <div style="text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 8px; font-size: 0.78rem; font-weight: 600; color: var(--apple-green); padding-top: 5px;">
        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #34c759; box-shadow: 0 0 8px rgba(52, 199, 89, 0.6);"></span>
        <span>Live Engine Connected</span>
    </div>
    """)

st.write("")

# ------------------------------------------------------------------------------
# 7. VIEW: OPERATIONAL DASHBOARD
# ------------------------------------------------------------------------------
if st.session_state.active_nav == "Dashboard":
    # 1. TOP ACTIVE ALERT BANNER
    alert_c1, alert_c2 = st.columns([4, 1.3])
    with alert_c1:
        render_html("""
        <div style="background: linear-gradient(90deg, rgba(0, 113, 227, 0.08), rgba(2, 132, 199, 0.04)); border: 1px solid rgba(0, 113, 227, 0.3); border-radius: 16px; padding: 16px 20px;">
            <div style="display: inline-block; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.06em; background: rgba(255, 59, 48, 0.14); color: #ff3b30; border: 1px solid rgba(255, 59, 48, 0.28); padding: 2px 8px; border-radius: 6px; margin-bottom: 4px;">ACTIVE ALERT</div>
            <div style="font-size: 0.88rem; color: var(--apple-text-primary); margin-top: 4px;">
                Customer <strong>Vikramaditya Singhania (CUST-1008)</strong> triggered Statutory AML Rule 01 (Large Value CDD) and Rule 03 (High-Risk Jurisdiction).
            </div>
        </div>
        """)
    with alert_c2:
        st.write("")
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("Review TXN-1024 ->", use_container_width=True, type="primary"):
                st.session_state.active_nav = "Transactions"
                st.rerun()
        with b_c2:
            if st.button("Ask Copilot", use_container_width=True):
                st.session_state.active_nav = "Copilot"
                st.session_state.copilot_query = "Why was transaction TXN-1024 flagged?"
                st.rerun()

    st.write("")

    # 2. 4 KPI STATS CARDS (Exact values, Apple Squircle design)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_html("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <span class="kpi-stat-label">TOTAL TRANSACTIONS</span>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--apple-blue); background: rgba(0, 113, 227, 0.12); padding: 3px 8px; border-radius: 6px;">TOTAL</span>
            </div>
            <div class="kpi-stat-val">121</div>
            <div class="kpi-stat-sub">Monitored Volume: ₹1,26,13,759.65</div>
        </div>
        """)
        
    with k2:
        render_html("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <span class="kpi-stat-label">SUSPICIOUS TRANSACTIONS</span>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--apple-red); background: rgba(255, 59, 48, 0.12); padding: 3px 8px; border-radius: 6px;">FLAGGED</span>
            </div>
            <div class="kpi-stat-val" style="color: var(--apple-red);">14 <span style="font-size: 1.1rem; font-weight: 500; color: var(--apple-text-secondary);">(11.6%)</span></div>
            <div class="kpi-stat-sub">Triggered explainable rule thresholds</div>
        </div>
        """)

    with k3:
        render_html("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <span class="kpi-stat-label">HIGH-RISK CUSTOMERS</span>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--apple-orange); background: rgba(255, 149, 0, 0.12); padding: 3px 8px; border-radius: 6px;">EDD</span>
            </div>
            <div class="kpi-stat-val" style="color: var(--apple-orange);">3</div>
            <div class="kpi-stat-sub">Subject to Enhanced Due Diligence (EDD)</div>
        </div>
        """)

    with k4:
        render_html("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <span class="kpi-stat-label">OPEN INVESTIGATIONS</span>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--apple-green); background: rgba(52, 199, 89, 0.12); padding: 3px 8px; border-radius: 6px;">ACTIVE</span>
            </div>
            <div class="kpi-stat-val">2</div>
            <div class="kpi-stat-sub">Active cases under compliance review</div>
        </div>
        """)

    st.write("")

    # 3. MIDDLE SECTION: RISK DISTRIBUTION & 14-DAY TIMELINE
    m_col1, m_col2 = st.columns([1, 1.5])
    with m_col1:
        render_html("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <strong style="color: var(--apple-text-primary); font-size: 1rem; letter-spacing: -0.015em;">Risk Score Distribution</strong>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--apple-blue); background: rgba(0, 113, 227, 0.12); padding: 2px 7px; border-radius: 6px;">RISK TIERS</span>
            </div>
            <div style="margin-top: 14px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
                    <span style="color: var(--apple-red); font-weight: 600;">Critical Risk (85-100)</span>
                    <strong>4 txns</strong>
                </div>
                <div style="width: 100%; height: 7px; background: rgba(0,0,0,0.06); border-radius: 4px; overflow: hidden; margin-bottom: 14px;">
                    <div style="width: 14%; height: 100%; background: var(--apple-red);"></div>
                </div>

                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
                    <span style="color: var(--apple-orange); font-weight: 600;">High Risk (65-84)</span>
                    <strong>0 txns</strong>
                </div>
                <div style="width: 100%; height: 7px; background: rgba(0,0,0,0.06); border-radius: 4px; overflow: hidden; margin-bottom: 14px;">
                    <div style="width: 0%; height: 100%; background: var(--apple-orange);"></div>
                </div>

                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
                    <span style="color: var(--apple-yellow); font-weight: 600;">Medium Risk (40-64)</span>
                    <strong>3 txns</strong>
                </div>
                <div style="width: 100%; height: 7px; background: rgba(0,0,0,0.06); border-radius: 4px; overflow: hidden; margin-bottom: 14px;">
                    <div style="width: 10%; height: 100%; background: var(--apple-yellow);"></div>
                </div>

                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
                    <span style="color: var(--apple-green); font-weight: 600;">Low Risk (0-39)</span>
                    <strong>114 txns</strong>
                </div>
                <div style="width: 100%; height: 7px; background: rgba(0,0,0,0.06); border-radius: 4px; overflow: hidden; margin-bottom: 14px;">
                    <div style="width: 92%; height: 100%; background: var(--apple-green);"></div>
                </div>
            </div>

            <div style="font-size: 0.74rem; color: var(--apple-text-muted); margin-top: 10px; border-top: 1px solid var(--apple-border); padding-top: 10px;">
                Evaluated by the <strong>Deterministic Risk Engine</strong> using baseline deviation, FATF corridor checks, and burst frequency.
            </div>
        </div>
        """)

    with m_col2:
        chart_data = [
            ("Sep 23", 10, 0), ("Sep 24", 15, 0), ("Sep 25", 35, 0), ("Sep 26", 20, 1),
            ("Sep 27", 18, 1), ("Sep 28", 40, 0), ("Sep 29", 12, 0), ("Sep 30", 55, 0),
            ("Oct 01", 85, 1), ("Oct 02", 45, 0), ("Oct 03", 60, 0), ("Oct 04", 75, 1),
            ("Oct 05", 25, 6), ("Oct 06", 50, 0)
        ]
        
        bars_html = "".join([
            f"""<div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 100%;">
                <div style="font-size: 0.68rem; font-weight: 700; color: #ff3b30; height: 16px;">{flg if flg > 0 else ''}</div>
                <div style="width: 80%; height: {val * 1.3}px; background: {'#ff3b30' if flg > 0 else '#0071e3'}; border-radius: 4px 4px 0 0;"></div>
                <div style="font-size: 0.65rem; color: var(--apple-text-muted); margin-top: 4px; white-space: nowrap;">{day.split(' ')[1]}</div>
            </div>""" for day, val, flg in chart_data
        ])

        render_html(f"""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <strong style="color: var(--apple-text-primary); font-size: 1rem; letter-spacing: -0.015em;">Suspicious Volume & Alerts Timeline (14 Days)</strong>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--apple-blue); background: rgba(0, 113, 227, 0.12); padding: 2px 7px; border-radius: 6px;">14-DAY</span>
            </div>
            <div style="height: 195px; display: flex; align-items: flex-end; gap: 6px; padding-top: 18px;">
                {bars_html}
            </div>
            <div style="display: flex; gap: 16px; justify-content: center; margin-top: 10px; font-size: 0.75rem; color: var(--apple-text-secondary);">
                <span><span style="display: inline-block; width: 10px; height: 10px; background: #0071e3; border-radius: 2px;"></span> Normal Transactions</span>
                <span><span style="display: inline-block; width: 10px; height: 10px; background: #ff3b30; border-radius: 2px;"></span> Suspicious / Flagged Activity</span>
            </div>
        </div>
        """)

    st.write("")

    # 4. BOTTOM SECTION: PRIORITY RISK ALERTS & MONITORED CORRIDORS
    b_col1, b_col2 = st.columns([1.6, 1])
    
    with b_col1:
        render_html("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <div>
                    <strong style="color: var(--apple-text-primary); font-size: 1rem; letter-spacing: -0.015em;">Priority Risk Alerts</strong>
                    <div style="font-size: 0.74rem; color: var(--apple-text-muted);">Latest Triggered Events</div>
                </div>
            </div>
            
            <div style="margin-top: 8px;">
                <div class="alert-row">
                    <div>
                        <span class="badge-crit">CRITICAL</span>
                        <strong style="color: var(--apple-text-primary);">Vikramaditya Singhania</strong> &bull; <span style="color: var(--apple-text-secondary);">₹6,80,000 to Panama</span>
                    </div>
                    <span style="color: var(--apple-blue); font-size: 0.82rem; font-weight: 600;">TXN-1025 -></span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-crit">CRITICAL</span>
                        <strong style="color: var(--apple-text-primary);">Vikramaditya Singhania</strong> &bull; <span style="color: var(--apple-text-secondary);">₹12,50,000 to Cayman Islands</span>
                    </div>
                    <span style="color: var(--apple-blue); font-size: 0.82rem; font-weight: 600;">TXN-1024 -></span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-med">MEDIUM</span>
                        <strong style="color: var(--apple-text-primary);">Devendra Patil</strong> &bull; <span style="color: var(--apple-text-secondary);">₹49,800 to India</span>
                    </div>
                    <span style="color: var(--apple-blue); font-size: 0.82rem; font-weight: 600;">TXN-1034 -></span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-med">MEDIUM</span>
                        <strong style="color: var(--apple-text-primary);">Devendra Patil</strong> &bull; <span style="color: var(--apple-text-secondary);">₹48,900 to India</span>
                    </div>
                    <span style="color: var(--apple-blue); font-size: 0.82rem; font-weight: 600;">TXN-1033 -></span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-med">MEDIUM</span>
                        <strong style="color: var(--apple-text-primary);">Devendra Patil</strong> &bull; <span style="color: var(--apple-text-secondary);">₹49,200 to India</span>
                    </div>
                    <span style="color: var(--apple-blue); font-size: 0.82rem; font-weight: 600;">TXN-1032 -></span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-low">LOW</span>
                        <strong style="color: var(--apple-text-primary);">Devendra Patil</strong> &bull; <span style="color: var(--apple-text-secondary);">₹49,500 to India</span>
                    </div>
                    <span style="color: var(--apple-blue); font-size: 0.82rem; font-weight: 600;">TXN-1031 -></span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-crit">CRITICAL</span>
                        <strong style="color: var(--apple-text-primary);">Hon. Rameshwar Prasad</strong> &bull; <span style="color: var(--apple-text-secondary);">₹8,50,000 to Switzerland</span>
                    </div>
                    <span style="color: var(--apple-blue); font-size: 0.82rem; font-weight: 600;">TXN-1040 -></span>
                </div>
                <div class="alert-row">
                    <div>
                        <span class="badge-crit">CRITICAL</span>
                        <strong style="color: var(--apple-text-primary);">Global Trade Nexus LLC</strong> &bull; <span style="color: var(--apple-text-secondary);">₹18,50,000 to Vanuatu</span>
                    </div>
                    <span style="color: var(--apple-blue); font-size: 0.82rem; font-weight: 600;">TXN-1051 -></span>
                </div>
            </div>
        </div>
        """)

    with b_col2:
        render_html("""
        <div class="kpi-stat-card">
            <div class="kpi-stat-header">
                <strong style="color: var(--apple-text-primary); font-size: 1rem; letter-spacing: -0.015em;">Monitored Corridors</strong>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--apple-blue); background: rgba(0, 113, 227, 0.12); padding: 2px 7px; border-radius: 6px;">FATF CORRIDORS</span>
            </div>
            
            <div style="margin-top: 8px;">
                <div class="alert-row">
                    <span style="color: var(--apple-text-secondary); font-size: 0.85rem;">117 transactions total</span>
                    <div style="text-align: right;">
                        <span style="color: var(--apple-red); font-weight: 700; font-size: 0.85rem;">10 Flagged</span><br>
                        <span style="color: var(--apple-text-muted); font-size: 0.75rem;">₹79,83,759.65</span>
                    </div>
                </div>
                <div class="alert-row">
                    <span style="color: var(--apple-text-secondary); font-size: 0.85rem;">1 transactions total</span>
                    <div style="text-align: right;">
                        <span style="color: var(--apple-red); font-weight: 700; font-size: 0.85rem;">1 Flagged</span><br>
                        <span style="color: var(--apple-text-muted); font-size: 0.75rem;">₹12,50,000.00</span>
                    </div>
                </div>
                <div class="alert-row">
                    <span style="color: var(--apple-text-secondary); font-size: 0.85rem;">1 transactions total</span>
                    <div style="text-align: right;">
                        <span style="color: var(--apple-red); font-weight: 700; font-size: 0.85rem;">1 Flagged</span><br>
                        <span style="color: var(--apple-text-muted); font-size: 0.75rem;">₹6,80,000.00</span>
                    </div>
                </div>
                <div class="alert-row">
                    <span style="color: var(--apple-text-secondary); font-size: 0.85rem;">1 transactions total</span>
                    <div style="text-align: right;">
                        <span style="color: var(--apple-red); font-weight: 700; font-size: 0.85rem;">1 Flagged</span><br>
                        <span style="color: var(--apple-text-muted); font-size: 0.75rem;">₹8,50,000.00</span>
                    </div>
                </div>
                <div class="alert-row">
                    <span style="color: var(--apple-text-secondary); font-size: 0.85rem;">1 transactions total</span>
                    <div style="text-align: right;">
                        <span style="color: var(--apple-red); font-weight: 700; font-size: 0.85rem;">1 Flagged</span><br>
                        <span style="color: var(--apple-text-muted); font-size: 0.75rem;">₹18,50,000.00</span>
                    </div>
                </div>
            </div>
        </div>
        """)

# ------------------------------------------------------------------------------
# 8. VIEW: REWORKED NEURAL COPILOT ASSISTANT (Apple Prompt Pills)
# ------------------------------------------------------------------------------
elif st.session_state.active_nav == "Copilot":
    render_html("""
    <div style="margin-bottom: 20px;">
        <h2 style="font-size: 1.6rem; font-weight: 800; color: var(--apple-text-primary); letter-spacing: -0.025em; margin: 0 0 4px 0;">Astra AI Copilot Assistant</h2>
        <div style="font-size: 0.85rem; color: var(--apple-text-secondary);">
            Explainable conversational intelligence grounded in transaction graphs, baseline statistics, and the Regulatory Knowledge Base.
        </div>
    </div>
    """)

    c_left, c_right = st.columns([1, 2.2])

    with c_left:
        render_html("""
        <div class="kpi-stat-card" style="margin-bottom: 16px;">
            <div style="font-size: 0.82rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: var(--apple-text-primary); margin-bottom: 4px;">
                Recommended Inquiries
            </div>
            <div style="font-size: 0.78rem; color: var(--apple-text-muted); margin-bottom: 12px;">
                Select any standard inquiry to run the deterministic audit & explanation pipeline:
            </div>
        </div>
        """)

        sample_prompts = [
            "Why was transaction TXN-1024 flagged?",
            "Why is customer CUST-1008 considered high risk?",
            "Show high-risk transactions above 5 Lakh",
            "Show suspicious FATF offshore corridors",
            "Show regulatory evidence and AML rules",
            "Generate an investigation summary for CUST-1008"
        ]

        for s_idx, sp in enumerate(sample_prompts):
            if st.button(sp, key=f"sp_btn_{s_idx}", use_container_width=True):
                st.session_state.copilot_query = sp
                st.rerun()

        render_html("""
        <div style="margin-top: 14px; padding: 14px; background: var(--apple-card); border: 1px solid var(--apple-border); border-radius: 16px; font-size: 0.74rem; color: var(--apple-text-muted); line-height: 1.5;">
            <strong style="color: var(--apple-blue);">Grounded Reasoning:</strong> Responses directly correlate transaction database records, baseline averages, and statutory knowledge clauses without hallucinating.
        </div>
        """)

    with c_right:
        # Check if query was passed from button or initial banner
        active_input = st.session_state.copilot_query
        if active_input:
            st.session_state.copilot_query = ""
            st.session_state.copilot_history.append({"role": "user", "title": "COMPLIANCE OFFICER", "content": active_input})
            
            p_lower = active_input.lower()
            if "1024" in p_lower or "singhania" in p_lower:
                ans_body = """
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">Flag Evaluation: Transaction TXN-1024</div>
                <div style="margin-bottom: 8px;">
                    <div>• <strong>Customer:</strong> Vikramaditya Singhania (CUST-1008)</div>
                    <div>• <strong>Amount:</strong> ₹12,50,000.00 to <em>Cayman Islands</em></div>
                    <div>• <strong>Baseline Deviation:</strong> +594% above 90-day moving average (₹1,80,000.00)</div>
                </div>
                <div style="margin-top: 10px; margin-bottom: 6px; font-weight: 700; font-size: 0.82rem; text-transform: uppercase; color: var(--apple-text-secondary);">Triggered Statutory Rules:</div>
                <div style="display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px;">
                    <div style="background: var(--apple-card-hover); padding: 10px 14px; border-radius: 10px; border-left: 3px solid #ff3b30;">
                        <span class="badge-crit">AML-R01</span> <strong>Large Value Customer Due Diligence:</strong> Cross-border transfer exceeds statutory regulatory threshold of ₹10,00,000.
                    </div>
                    <div style="background: var(--apple-card-hover); padding: 10px 14px; border-radius: 10px; border-left: 3px solid #ff3b30;">
                        <span class="badge-crit">AML-R03</span> <strong>High-Risk Offshore Secrecy Jurisdiction:</strong> Cayman Islands is designated under enhanced FATF monitoring for tax transparency and beneficial ownership opacity.
                    </div>
                </div>
                <div style="font-weight: 700; font-size: 0.82rem; text-transform: uppercase; color: var(--apple-text-secondary); margin-bottom: 4px;">Recommended Remediation:</div>
                <div>1. Issue statutory Request for Information (RFI) regarding source of funds and ultimate beneficial ownership (UBO).</div>
                <div>2. Escalate to Case <strong>CASE-4091</strong> for draft Suspicious Activity Report (SAR) filing with the Financial Intelligence Unit (FIU).</div>
                """
            elif "cust-1008" in p_lower or "high risk" in p_lower:
                ans_body = """
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">Customer Risk Profile: Vikramaditya Singhania (CUST-1008)</div>
                <div style="margin-bottom: 8px;">
                    <div>• <strong>Assigned Risk Tier:</strong> CRITICAL (Risk Score: 88/100)</div>
                    <div>• <strong>KYC Status:</strong> Enhanced Due Diligence (EDD) Required</div>
                    <div>• <strong>Politically Exposed Person (PEP):</strong> Yes (Close Associate of Senior Public Official)</div>
                    <div>• <strong>Total Monitored Outflows:</strong> ₹19,30,000.00 across 2 high-risk offshore corridors (Panama & Cayman Islands)</div>
                </div>
                <div style="margin-top: 8px; padding: 10px; background: rgba(255, 59, 48, 0.08); border-radius: 10px; border: 1px solid rgba(255, 59, 48, 0.2);">
                    <strong>Risk Rationale:</strong> Customer exhibits classic structuring and rapid outbound transfer behavior. Domestic funds received were aggregated and wired to offshore jurisdictions within 48 hours.
                </div>
                """
            elif "sar" in p_lower or "summary" in p_lower:
                ans_body = """
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">Draft Suspicious Activity Report (SAR) Narrative</div>
                <div style="font-size: 0.78rem; color: var(--apple-text-muted); margin-bottom: 10px;">Subject: Vikramaditya Singhania (CUST-1008) | Target: Financial Intelligence Unit</div>
                <div style="background: var(--apple-card-hover); padding: 12px 14px; border-radius: 10px; font-size: 0.82rem; line-height: 1.6; border: 1px solid var(--apple-border);">
                    Between Oct 01 and Oct 05, the subject conducted high-velocity international wires totaling ₹19,30,000.00 to offshore jurisdictions (Panama and Cayman Islands) with no verifiable commercial underlying documentation. Historical account turnover averaged ₹1,80,000.00 monthly. Inbound funds were immediately wired out within 48 hours, demonstrating indicators of Layering under FATF Recommendation 16.
                </div>
                """
            else:
                ans_body = f"""
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">Astra AI Regulatory Reasoning</div>
                <div>Grounded evaluation completed for inquiry: <em>"{active_input}"</em></div>
                <div style="margin-top: 8px;">• Correlated 121 monitored transactions and 14 flagged AML alerts across all compliance ledgers.</div>
                <div>• Identified 4 Critical risk items requiring MLRO compliance signoff.</div>
                <div>• Verified against Statutory AML Rules AML-R01 through AML-R05 with full audit traceability preserved.</div>
                """
            
            st.session_state.copilot_history.append({"role": "assistant", "title": "INVESTIGATION COPILOT", "content": ans_body})

        # Render conversation stream
        for msg in st.session_state.copilot_history:
            if msg["role"] == "user":
                render_html(f"""
                <div class="chat-bubble-user">
                    <span class="chat-badge-user">COMPLIANCE OFFICER</span>
                    <div style="font-size: 0.92rem; color: var(--apple-text-primary); font-weight: 600;">{msg['content']}</div>
                </div>
                """)
            else:
                render_html(f"""
                <div class="chat-bubble-copilot">
                    <span class="chat-badge-copilot">INVESTIGATION COPILOT</span>
                    <div style="font-size: 0.88rem; color: var(--apple-text-primary); line-height: 1.6;">
                        {msg['content']}
                    </div>
                </div>
                """)

        # Clean Apple Input Row
        in_c1, in_c2 = st.columns([5, 1.2])
        with in_c1:
            user_typed = st.text_input(
                "Message Copilot", 
                placeholder="Ask Astra AI regulatory audit question or transaction ID (e.g. TXN-1024)...", 
                label_visibility="collapsed", 
                key="copilot_text_input"
            )
        with in_c2:
            send_clicked = st.button("Send Query", key="copilot_send_btn", type="primary", use_container_width=True)

        if send_clicked and user_typed:
            st.session_state.copilot_query = user_typed
            st.rerun()

# ------------------------------------------------------------------------------
# 9. VIEW: TRANSACTIONS & ALERTS (Zero Emojis, Apple Ledger)
# ------------------------------------------------------------------------------
elif st.session_state.active_nav in ["Transactions", "Alerts"]:
    render_html("""
    <div style="margin-bottom: 16px;">
        <h2 style="font-size: 1.6rem; font-weight: 800; color: var(--apple-text-primary); letter-spacing: -0.025em; margin: 0 0 4px 0;">Live Transaction Surveillance Ledger</h2>
        <div style="font-size: 0.85rem; color: var(--apple-text-secondary);">
            Deterministic anomaly scoring, corridor routing, and statutory flag detection across all enterprise payments.
        </div>
    </div>
    """)
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

# ------------------------------------------------------------------------------
# 10. VIEW: CUSTOMERS (Zero Emojis, Apple Profiles)
# ------------------------------------------------------------------------------
elif st.session_state.active_nav == "Customers":
    render_html("""
    <div style="margin-bottom: 16px;">
        <h2 style="font-size: 1.6rem; font-weight: 800; color: var(--apple-text-primary); letter-spacing: -0.025em; margin: 0 0 4px 0;">Customer AML & KYC Profiles</h2>
        <div style="font-size: 0.85rem; color: var(--apple-text-secondary);">
            Baseline transaction velocity, PEP classification, and risk tier evaluation.
        </div>
    </div>
    """)
    cust_df = pd.DataFrame([
        {"Customer ID": "CUST-1008", "Full Name": "Vikramaditya Singhania", "KYC Status": "Enhanced Due Diligence", "Risk Score": 88, "Risk Level": "HIGH", "PEP": "Yes"},
        {"Customer ID": "CUST-1004", "Full Name": "Hon. Rameshwar Prasad", "KYC Status": "Enhanced Due Diligence", "Risk Score": 82, "Risk Level": "HIGH", "PEP": "Yes"},
        {"Customer ID": "CUST-1003", "Full Name": "Devendra Patil", "KYC Status": "Verified", "Risk Score": 78, "Risk Level": "HIGH", "PEP": "No"},
        {"Customer ID": "CUST-1005", "Full Name": "Global Trade Nexus LLC", "KYC Status": "Verified", "Risk Score": 68, "Risk Level": "MEDIUM", "PEP": "No"},
        {"Customer ID": "CUST-1001", "Full Name": "Ananya Sharma", "KYC Status": "Verified", "Risk Score": 12, "Risk Level": "LOW", "PEP": "No"},
    ])
    st.dataframe(cust_df, use_container_width=True)

# ------------------------------------------------------------------------------
# 11. VIEW: REGULATORY RULES & INVESTIGATIONS (Apple Cards)
# ------------------------------------------------------------------------------
elif st.session_state.active_nav == "Regulatory":
    render_html("""
    <div style="margin-bottom: 16px;">
        <h2 style="font-size: 1.6rem; font-weight: 800; color: var(--apple-text-primary); letter-spacing: -0.025em; margin: 0 0 4px 0;">Statutory AML & Regulatory Knowledge Base</h2>
        <div style="font-size: 0.85rem; color: var(--apple-text-secondary);">
            FATF Recommendations, PMLA Statutory Rules, and FIU Typologies enforced deterministically by the Astra engine.
        </div>
    </div>
    <div style="display: flex; flex-direction: column; gap: 12px;">
        <div class="kpi-stat-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span class="badge-crit">AML-R01</span> <strong>Large Value Customer Due Diligence (Threshold > ₹10,00,000)</strong>
                <span style="font-size: 0.72rem; color: var(--apple-text-muted);">PMLA 2002 Sec 12</span>
            </div>
            <div style="font-size: 0.82rem; color: var(--apple-text-secondary);">Mandates mandatory Customer Due Diligence (CDD) and verified source-of-wealth identification for single cross-border payments exceeding ₹10,00,000.</div>
        </div>
        <div class="kpi-stat-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span class="badge-crit">AML-R03</span> <strong>High-Risk Offshore Secrecy Jurisdiction Corridors</strong>
                <span style="font-size: 0.72rem; color: var(--apple-text-muted);">FATF Recommendation 19</span>
            </div>
            <div style="font-size: 0.82rem; color: var(--apple-text-secondary);">Automatically triggers Enhanced Due Diligence (EDD) for transactions involving FATF grey-list countries or jurisdictions with non-transparent beneficial ownership registries.</div>
        </div>
        <div class="kpi-stat-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span class="badge-med">AML-R04</span> <strong>Structuring & Smurfing Detection (Sub-threshold Velocity)</strong>
                <span style="font-size: 0.72rem; color: var(--apple-text-muted);">FIU Typology T-08</span>
            </div>
            <div style="font-size: 0.82rem; color: var(--apple-text-secondary);">Flags multiple transactions just below statutory reporting thresholds (e.g. ₹49,000 to ₹49,900) occurring within a compressed 72-hour window.</div>
        </div>
    </div>
    """)

elif st.session_state.active_nav == "Investigations":
    render_html("""
    <div style="margin-bottom: 16px;">
        <h2 style="font-size: 1.6rem; font-weight: 800; color: var(--apple-text-primary); letter-spacing: -0.025em; margin: 0 0 4px 0;">Active Compliance Cases & SAR Filing Queue</h2>
        <div style="font-size: 0.85rem; color: var(--apple-text-secondary);">
            Cases currently under Enhanced Due Diligence (EDD) and FIU submission review.
        </div>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
        <div class="kpi-stat-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <strong style="color: var(--apple-text-primary);">CASE-4091: Vikramaditya Singhania</strong>
                <span class="badge-crit">UNDER REVIEW</span>
            </div>
            <div style="font-size: 0.82rem; color: var(--apple-text-secondary); margin-bottom: 8px;">Triggered Rules: AML-R01 (Large Value), AML-R03 (Cayman Islands)</div>
            <div style="font-size: 0.78rem; color: var(--apple-text-muted);">Flagged Amount: ₹12,50,000.00 • Priority: High • Assigned: Senior Risk Officer</div>
        </div>
        <div class="kpi-stat-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <strong style="color: var(--apple-text-primary);">CASE-4092: Devendra Patil</strong>
                <span class="badge-med">EDD IN PROGRESS</span>
            </div>
            <div style="font-size: 0.82rem; color: var(--apple-text-secondary); margin-bottom: 8px;">Triggered Rules: AML-R04 (Smurfing Velocity)</div>
            <div style="font-size: 0.78rem; color: var(--apple-text-muted);">Flagged Amount: ₹1,47,900.00 across 3 bursts • Priority: Medium</div>
        </div>
    </div>
    """)

else:
    render_html(f"""
    <div class="kpi-stat-card">
        <h3>{st.session_state.active_nav}</h3>
        <p style="color: var(--apple-text-secondary);">Statutory compliance ledger active. All operations logged under regulatory standards.</p>
    </div>
    """)

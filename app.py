import base64
import os
import textwrap
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FactoryOps | Predictive Maintenance",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

REQUEST_TIMEOUT = 8


@st.cache_data
def get_login_bg_base64() -> str:
    paths = [
        r"C:\Users\Premalatha N K\.gemini\antigravity-ide\brain\89070437-1b21-4396-843d-e0abfeeccbd6\.user_uploaded\media_1788361798787.png",
        os.path.join(
            os.path.dirname(__file__),
            "assets",
            "login_bg.png",
        ),
    ]
    for bg_path in paths:
        if os.path.exists(bg_path):
            with open(bg_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    return ""


# ============================================================
# LOGIN CREDENTIALS
# ============================================================

ADMIN_USERNAME = os.getenv(
    "STREAMLIT_ADMIN_USERNAME",
    "admin",
)

ADMIN_PASSWORD = os.getenv(
    "STREAMLIT_ADMIN_PASSWORD",
    "admin123",
)

USER_USERNAME = os.getenv(
    "STREAMLIT_USER_USERNAME",
    "user",
)

USER_PASSWORD = os.getenv(
    "STREAMLIT_USER_PASSWORD",
    "user123",
)


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ============================================================
# HTML RENDER HELPER
# ============================================================


def render_html(content: str):
    st.html(textwrap.dedent(content).strip())


# ============================================================
# GLOBAL STYLING
# ============================================================

render_html(
    """
    <style>

        /* ==================================================
           GLOBAL APP
           ================================================== */

        html {
            scroll-behavior: smooth;
            scroll-padding-top: 25px;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 10%,
                    rgba(59, 130, 246, 0.13),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 85%,
                    rgba(14, 165, 233, 0.10),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #eef4ff 0%,
                    #f7f9fc 48%,
                    #edf5fb 100%
                );
        }


        /* ==================================================
           REMOVE DEFAULT STREAMLIT SPACING
           ================================================== */

        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
        }

        [data-testid="stVerticalBlock"] {
            gap: 0.55rem;
        }


        /* ==================================================
           OFFICIAL TOP NAVIGATION
           ================================================== */

        [data-testid="stSidebar"] {
            display: none;
        }

        .factory-topbar {
            position: sticky;
            top: 0;
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.85rem 1.2rem;
            margin: -1.2rem 0 1.2rem 0;
            background: rgba(7, 24, 52, 0.94);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 0 0 16px 16px;
            box-shadow: 0 10px 30px rgba(7,24,52,0.16);
        }

        .factory-topbar-brand {
            color: #ffffff;
            font-size: 1.35rem;
            font-weight: 850;
            letter-spacing: -0.03em;
            white-space: nowrap;
        }

        .factory-topbar-sub {
            color: #bfdbfe;
            font-size: 0.86rem;
            margin-left: 0.35rem;
        }

        .factory-nav-note {
            color: #cbd5e1;
            font-size: 0.9rem;
        }

        .factory-nav-links {
            display: flex;
            align-items: center;
            gap: 0.35rem;
            flex-wrap: wrap;
            margin-top: 0.6rem;
        }

        .factory-nav-links a {
            color: #dbeafe !important;
            text-decoration: none !important;
            font-size: 0.9rem;
            font-weight: 650;
            padding: 0.42rem 0.65rem;
            border-radius: 8px;
            border: 1px solid transparent;
            transition: 0.2s ease;
        }

        .factory-nav-links a:hover {
            color: #ffffff !important;
            background: rgba(255,255,255,0.10);
            border-color: rgba(255,255,255,0.12);
        }


        /* ==================================================
           RESPONSIVE PRODUCTION LOGIN EXPERIENCE (FactoryOps)
           ================================================== */

        /* Hide Streamlit default header, footer & padding */
        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        #MainMenu,
        footer {
            display: none !important;
            visibility: hidden !important;
        }

        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
        }

        .stApp {
            overflow-x: hidden !important;
        }

        .login-backdrop-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #020614;
            z-index: 9990;
            pointer-events: none;
        }

        /* Split Screen Container - Rigid 50/50 Side-by-Side */
        [class*="st-key-login_frame"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            transform: none !important;
            z-index: 9999 !important;
            width: 100vw !important;
            height: 100vh !important;
            min-height: 100vh !important;
            margin: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            overflow: hidden !important;
            background: #020614 !important;
            padding: 0 !important;
        }

        [class*="st-key-login_frame"] [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            width: 100vw !important;
            height: 100vh !important;
            min-height: 100vh !important;
            gap: 0 !important;
            margin: 0 !important;
            align-items: stretch !important;
        }

        /* Left Industrial Background Column - 50vw */
        [class*="st-key-login_frame"] [data-testid="stColumn"]:nth-of-type(1) {
            padding: 0 !important;
            height: 100vh !important;
            min-height: 100vh !important;
            flex: 1 1 50% !important;
            width: 50vw !important;
            min-width: 50vw !important;
            max-width: 50vw !important;
            position: relative !important;
            overflow: hidden !important;
        }

        .login-hero-container {
            width: 100%;
            height: 100% !important;
            min-height: 100vh !important;
            background-size: cover !important;
            background-position: left center !important;
            background-repeat: no-repeat !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: flex-end !important;
            padding: clamp(2.5rem, 5vw, 5rem) !important;
            box-sizing: border-box !important;
            position: relative;
        }

        .login-hero-content-box {
            position: relative;
            z-index: 2;
            max-width: 540px;
        }

        .hero-title-brand {
            color: #ffffff;
            font-size: clamp(2.8rem, 4.2vw, 4.8rem);
            font-weight: 850;
            letter-spacing: -0.045em;
            line-height: 1.05;
            margin-bottom: 0.5rem;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
        }

        .hero-tagline-text {
            color: #dbeafe;
            font-size: clamp(1.05rem, 1.35vw, 1.4rem);
            font-weight: 400;
            margin-bottom: 0.8rem;
            line-height: 1.3;
        }

        .hero-divider-bar {
            width: 48px;
            height: 2.5px;
            background: #2563eb;
            margin-bottom: 1.5rem;
            border-radius: 2px;
            box-shadow: 0 0 10px rgba(37, 99, 235, 0.8);
        }

        /* Right Panel - Equal 50vw Width, Perfectly Centered */
        [class*="st-key-login_frame"] [data-testid="stColumn"]:nth-of-type(2) {
            padding: 0 !important;
            height: 100vh !important;
            min-height: 100vh !important;
            flex: 1 1 50% !important;
            width: 50vw !important;
            min-width: 50vw !important;
            max-width: 50vw !important;
            background: linear-gradient(160deg, #020817 0%, #051538 55%, #072254 100%) !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }

        [class*="st-key-login_frame"] [data-testid="stColumn"]:nth-of-type(2) > div[data-testid="stVerticalBlock"] {
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 2rem !important;
            box-sizing: border-box !important;
            margin: 0 !important;
        }

        /* Seamless Centered Login Form Block (Matches User Reference Image 1) */
        [class*="st-key-login_form_side"] {
            width: 100% !important;
            max-width: 440px !important;
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            box-shadow: none !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            box-sizing: border-box !important;
            margin: auto !important;
        }

        .login-form-eyebrow {
            color: #3b82f6;
            font-size: 0.95rem;
            font-weight: 500;
            margin-bottom: 0.35rem;
            text-align: left !important;
            width: 100% !important;
        }

        .login-form-heading {
            color: #ffffff;
            font-size: 2.6rem;
            font-weight: 750;
            letter-spacing: -0.03em;
            margin-bottom: 0.4rem;
            line-height: 1.1;
            text-align: left !important;
            width: 100% !important;
        }

        .login-form-subtitle {
            color: #94a3b8;
            font-size: 0.98rem;
            margin-bottom: 2rem;
            text-align: left !important;
            width: 100% !important;
        }

        /* Portal Radio Buttons - Clean Blue Radio Selection (Image 1) */
        [class*="st-key-login_portal"] {
            margin-bottom: 1.8rem !important;
            width: 100% !important;
            display: flex !important;
            justify-content: flex-start !important;
        }

        [class*="st-key-login_portal"] [data-testid="stRadio"] > label {
            display: none !important;
        }

        [class*="st-key-login_portal"] div[role="radiogroup"] {
            display: flex !important;
            flex-direction: row !important;
            justify-content: flex-start !important;
            gap: 2.5rem !important;
            width: 100% !important;
        }

        [class*="st-key-login_portal"] div[role="radiogroup"] label {
            display: flex !important;
            align-items: center !important;
            gap: 0.65rem !important;
            color: #ffffff !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            cursor: pointer !important;
        }

        [class*="st-key-login_portal"] div[role="radiogroup"] label p {
            color: #ffffff !important;
            font-size: 1rem !important;
        }

        /* Radio outer ring */
        div[data-testid="stRadio"] [role="radiogroup"] label > div > div:nth-child(1),
        div[data-testid="stRadio"] [role="radiogroup"] input:checked ~ div:nth-of-type(1),
        [class*="st-key-login_portal"] div[role="radiogroup"] [data-baseweb="radio"] div {
            border-color: #3b82f6 !important;
            background-color: transparent !important;
        }

        /* Radio active inner dot - Pure Blue (#2563eb) overriding red inline style */
        div[data-testid="stRadio"] div[class*="etak9228"],
        div[data-testid="stRadio"] [role="radiogroup"] input:checked ~ div:nth-of-type(2),
        div[data-testid="stRadio"] [role="radiogroup"] label > div > div:nth-of-type(2),
        div[data-testid="stRadio"] [role="radiogroup"] div[style*="255, 75, 75"] {
            background-color: #2563eb !important;
            background: #2563eb !important;
            border-color: #2563eb !important;
        }

        /* Form Controls & Inputs */
        div[data-testid="stForm"] {
            border: 0 !important;
            padding: 0 !important;
            background: transparent !important;
            width: 100% !important;
        }

        div[data-testid="stForm"] [data-testid="stTextInput"] {
            margin-bottom: 1.4rem !important;
            width: 100% !important;
        }

        div[data-testid="stForm"] [data-testid="stTextInput"] label,
        div[data-testid="stForm"] [data-testid="stTextInput"] label p {
            color: #cbd5e1 !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
            margin-bottom: 0.45rem !important;
            text-align: left !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }

        /* Textbox Input Container - Distinct Visible Electric Blue Border (Image 1) */
        div[data-testid="stTextInput"] div[data-baseweb="input"] {
            background-color: rgba(6, 18, 48, 0.75) !important;
            background: rgba(6, 18, 48, 0.75) !important;
            border: 1.5px solid #2563eb !important;
            border-radius: 12px !important;
            box-shadow: none !important;
            height: 50px !important;
            min-height: 50px !important;
            box-sizing: border-box !important;
            transition: all 0.2s ease !important;
            overflow: hidden !important;
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"]:hover {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.35) !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: #60a5fa !important;
            box-shadow: 0 0 16px rgba(96, 165, 250, 0.5) !important;
        }

        /* Inner wrappers transparent to reveal dark navy container fill */
        div[data-testid="stTextInput"] div[data-baseweb="input"] div,
        div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
            border: none !important;
            border-color: transparent !important;
            background-color: transparent !important;
            background: transparent !important;
            box-shadow: none !important;
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            align-items: center !important;
        }

        div[data-testid="stTextInput"] input {
            background-color: transparent !important;
            background: transparent !important;
            color: #ffffff !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            font-size: 0.98rem !important;
            height: 48px !important;
            min-height: 48px !important;
            width: 100% !important;
            padding-right: 14px !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #8ca3c5 !important;
            opacity: 0.9 !important;
        }

        /* Username Input - Left User SVG Icon (Image 1) */
        div[data-testid="stTextInput"] input[aria-label="Username"] {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%233b82f6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: 14px center !important;
            padding-left: 44px !important;
        }

        /* Password Input - Left Lock SVG Icon (Image 1) */
        div[data-testid="stTextInput"] input[aria-label="Password"] {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%233b82f6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='18' height='11' x='3' y='11' rx='2' ry='2'/%3E%3Cpath d='M7 11V7a5 5 0 0 1 10 0v4'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: 14px center !important;
            padding-left: 44px !important;
        }

        /* Password Eye Toggle Icon */
        [data-testid="stTextInput"] button {
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            color: #60a5fa !important;
            background: transparent !important;
            background-color: transparent !important;
            margin-right: 8px !important;
        }

        [data-testid="stTextInput"] button svg,
        [data-testid="stTextInput"] button path {
            fill: none !important;
            stroke: #60a5fa !important;
            color: #60a5fa !important;
        }

        /* Sign In Button - Crisp Pill matching Image 1 */
        div[data-testid="stFormSubmitButton"] {
            width: 100% !important;
            margin-top: 1rem !important;
        }

        div[data-testid="stFormSubmitButton"] button,
        button[data-testid="stBaseButton-primaryFormSubmit"] {
            width: 100% !important;
            height: 50px !important;
            min-height: 50px !important;
            background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%) !important;
            background-color: #2563eb !important;
            border: none !important;
            outline: none !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.45) !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            margin: 0 !important;
            transition: all 0.2s ease !important;
        }

        div[data-testid="stFormSubmitButton"] button:hover,
        button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
            background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%) !important;
            background-color: #3b82f6 !important;
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.65) !important;
            transform: translateY(-1px) !important;
        }

        div[data-testid="stFormSubmitButton"] button *,
        button[data-testid="stBaseButton-primaryFormSubmit"] * {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            color: #ffffff !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            display: inline-block !important;
            width: auto !important;
            height: auto !important;
            line-height: 1 !important;
        }

        /* Tablet & Mobile Media Queries */
        @media (max-width: 900px) {
            [class*="st-key-login_frame"] > [data-testid="stHorizontalBlock"] {
                flex-direction: column !important;
            }
            [class*="st-key-login_frame"] [data-testid="stColumn"]:nth-of-type(1) {
                min-height: 280px !important;
                height: 35vh !important;
                flex: none !important;
            }
            .login-hero-container {
                min-height: 280px !important;
                height: 35vh !important;
                padding: 1.5rem 2rem !important;
            }
            [class*="st-key-login_frame"] [data-testid="stColumn"]:nth-of-type(2) {
                min-height: auto !important;
                padding: 2rem 1.2rem !important;
                flex: none !important;
            }
            [class*="st-key-login_form_side"] {
                width: 100% !important;
                max-width: 100% !important;
                padding: 2rem 1.5rem !important;
            }
        }


        /* ==================================================
           SCROLL SECTIONS
           ================================================== */

        .factory-section {
            position: relative;
            width: 100%;
            padding: 2rem 2rem 2.5rem 2rem;
            margin: 0 0 1rem 0;
            border-radius: 22px;
            border: 1px solid rgba(226,232,240,0.9);
            background: rgba(255,255,255,0.82);
            box-shadow: 0 5px 20px rgba(15,23,42,0.07);
            scroll-margin-top: 25px;
        }

        .factory-section::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            border-radius: 22px 0 0 22px;
            background: linear-gradient(180deg, #2563eb, #0ea5e9);
        }

        .section-header {
            margin-bottom: 1rem;
        }

        .section-kicker {
            color: #2563eb;
            font-size: 0.82rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 0.35rem;
        }

        .section-main-title {
            color: #0f172a;
            font-size: 2.25rem;
            font-weight: 850;
            letter-spacing: -0.045em;
            line-height: 1.1;
        }

        /* DESCRIPTION REMOVED */


        /* ==================================================
           SECTION DIVIDERS
           ================================================== */

        .section-divider {
            height: 1px;
            width: 100%;
            margin: 0.4rem 0 1.3rem 0;
            background:
                linear-gradient(
                    90deg,
                    transparent,
                    #cbd5e1,
                    transparent
                );
        }


        /* ==================================================
           METRIC CARDS
           ================================================== */

        .metric-card {
            background: rgba(255,255,255,0.94);
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1rem 1.1rem;
            min-height: 115px;
            box-shadow:
                0 4px 14px rgba(15,23,42,0.05);
        }

        .metric-label {
            color: #64748b;
            font-size: 0.95rem;
            font-weight: 600;
        }

        .metric-value {
            color: #111827;
            font-size: 1.9rem;
            font-weight: 800;
            margin-top: 0.35rem;
        }

        .metric-note {
            color: #94a3b8;
            font-size: 0.75rem;
            margin-top: 0.25rem;
        }


        /* ==================================================
           SECTION TITLES
           ================================================== */

        .section-title {
            font-size: 1.5rem;
            font-weight: 800;
            color: #1e293b;
            margin: 1.3rem 0 0.7rem 0;
        }


        /* ==================================================
           HEALTH OVERVIEW
           ================================================== */

        .health-card {
            background: rgba(255,255,255,0.96);
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow:
                0 8px 24px rgba(15,23,42,0.06);
        }

        .health-chart-title {
            text-align: center;
            font-size: 1rem;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 0.2rem;
        }

        .health-chart-subtitle {
            text-align: center;
            color: #64748b;
            font-size: 0.78rem;
            margin-bottom: 1rem;
        }

        .health-overview-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2.5rem;
            flex-wrap: wrap;
        }


        /* ==================================================
           DONUT
           ================================================== */

        .donut-chart {
            width: 220px;
            height: 220px;
            margin: 0 auto;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            flex-shrink: 0;
            box-shadow:
                0 8px 20px rgba(15,23,42,0.10);
        }

        .donut-center {
            width: 128px;
            height: 128px;
            background: #ffffff;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow:
                0 0 0 1px #eef2f7,
                0 4px 12px rgba(15,23,42,0.06);
        }

        .donut-number {
            font-size: 2rem;
            font-weight: 800;
            color: #111827;
            line-height: 1;
        }

        .donut-text {
            font-size: 0.75rem;
            color: #64748b;
            margin-top: 0.35rem;
            font-weight: 600;
        }


        /* ==================================================
           HEALTH SUMMARY
           ================================================== */

        .health-legend {
            margin-top: 0.5rem;
        }

        .legend-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.85rem 0;
            border-bottom: 1px solid #f1f5f9;
        }

        .legend-row:last-child {
            border-bottom: none;
        }

        .legend-left {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            font-weight: 600;
            color: #334155;
        }

        .legend-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            flex-shrink: 0;
        }

        .legend-value {
            font-weight: 800;
            color: #111827;
        }

        .legend-percentage {
            font-size: 0.75rem;
            color: #64748b;
            margin-left: 0.4rem;
        }


        /* ==================================================
           FACTORY DATA TABLE
           ================================================== */

        .factory-table-wrapper {
            width: 100%;
            overflow-x: auto;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            background: #ffffff;
            box-shadow:
                0 4px 14px rgba(15,23,42,0.04);
        }

        .factory-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }

        .factory-table th {
            text-align: left !important;
            padding: 12px 16px;
            background: #f8fafc;
            color: #334155;
            font-weight: 700;
            border-bottom: 1px solid #e2e8f0;
            white-space: nowrap;
        }

        .factory-table td {
            text-align: left !important;
            padding: 11px 16px;
            color: #111827;
            border-bottom: 1px solid #f1f5f9;
            white-space: nowrap;
        }

        .factory-table tbody tr:last-child td {
            border-bottom: none;
        }

        .factory-table tbody tr:hover {
            background: #f8fafc;
        }


        /* ==================================================
           GENERAL BUTTONS
           ================================================== */

        .stButton > button {
            border-radius: 9px;
            font-weight: 600;
        }


        /* ==================================================
           FOOTER
           ================================================== */

        .footer-note {
            color: #94a3b8 !important;
            font-size: 0.75rem;
            text-align: center;
            margin-top: 1.5rem;
        }


        /* ==================================================
           HIDE STREAMLIT DECORATIONS
           ================================================== */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }


        /* ==================================================
           MOBILE
           ================================================== */

        @media (max-width: 768px) {

            .factory-section {
                padding: 1.2rem 1rem 1.5rem 1rem;
                border-radius: 16px;
            }

            .section-main-title {
                font-size: 1.55rem;
            }

            .login-shell {
                height: 100dvh;
                min-height: 0;
                padding: 1rem;
                align-items: center;
                inset: 8px;
            }

            .login-hero-copy {
                padding: 1.35rem;
            }

            .login-hero-feature {
                display: none;
            }

            .login-shell::before {
                display: none;
            }

            [class*="st-key-login-card"] {
                width: auto;
                max-width: none;
                height: auto;
                min-height: auto;
                top: auto;
                right: 8px;
                bottom: 8px;
                left: 8px;
                margin: 0;
                padding: 1.25rem;
                border-radius: 22px;
                background: rgba(11,25,48,0.82);
            }
        }

    </style>
    """
)


# ============================================================
# SCROLL-SPY JAVASCRIPT
# ============================================================


def inject_scroll_spy():
    return


# ============================================================
# API HELPERS
# ============================================================


def api_request(
    method: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> Any:

    url = f"{API_BASE_URL}{path}"

    response = requests.request(
        method=method,
        url=url,
        params=params,
        json=json,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    if not response.content:
        return None

    return response.json()


def api_get(
    path: str,
    params: Optional[Dict[str, Any]] = None,
) -> Any:

    return api_request(
        "GET",
        path,
        params=params,
    )


def extract_list(
    payload: Any,
) -> List[Dict[str, Any]]:

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):

        for key in (
            "items",
            "data",
            "results",
            "machines",
            "sensors",
            "predictions",
            "maintenance",
            "incidents",
        ):

            value = payload.get(key)

            if isinstance(value, list):
                return value

    return []


def safe_get(
    path: str,
    params: Optional[Dict[str, Any]] = None,
):

    try:

        return (
            api_get(
                path,
                params=params,
            ),
            None,
        )

    except requests.exceptions.ConnectionError:

        return (
            None,
            f"Cannot connect to backend at {API_BASE_URL}.",
        )

    except requests.exceptions.Timeout:

        return (
            None,
            "Backend request timed out.",
        )

    except requests.exceptions.HTTPError as exc:

        status = exc.response.status_code if exc.response is not None else "unknown"

        detail = ""

        try:
            detail = exc.response.json()
        except Exception:
            pass

        return (
            None,
            f"API returned HTTP {status}: {detail}",
        )

    except Exception as exc:

        return (
            None,
            str(exc),
        )


def fetch_first(
    paths: List[str],
):

    errors = []

    for path in paths:

        data, error = safe_get(path)

        if error is None:
            return data, None

        errors.append(f"{path}: {error}")

    return (
        None,
        " | ".join(errors),
    )


# ============================================================
# FORMATTERS
# ============================================================


def fmt_number(
    value: Any,
    digits: int = 2,
) -> str:

    if value is None or value == "":
        return "—"

    try:
        return f"{float(value):.{digits}f}"

    except Exception:
        return str(value)


def metric_card(
    label: str,
    value: Any,
    note: str = "",
):

    render_html(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                {label}
            </div>

            <div class="metric-value">
                {value}
            </div>

            <div class="metric-note">
                {note}
            </div>
        </div>
        """
    )


def normalize_dataframe(
    rows: List[Dict[str, Any]],
) -> pd.DataFrame:

    if not rows:
        return pd.DataFrame()

    return pd.json_normalize(rows)


# ============================================================
# TABLE DISPLAY HELPER
# ============================================================


def display_table(
    df: pd.DataFrame,
    units: Optional[Dict[str, str]] = None,
):
    if df.empty:
        st.info("No data available.")
        return

    units = units or {}
    display_df = df.copy()

    for column, unit in units.items():
        if column in display_df.columns:
            display_df[column] = display_df[column].apply(
                lambda value: "—" if pd.isna(value) else f"{value} {unit}"
            )

    styled_df = display_df.style
    numeric_columns = display_df.select_dtypes(include="number").columns
    text_columns = display_df.select_dtypes(exclude="number").columns

    if len(numeric_columns):
        styled_df = styled_df.set_properties(
            subset=list(numeric_columns),
            **{"text-align": "right"},
        )

    if len(text_columns):
        styled_df = styled_df.set_properties(
            subset=list(text_columns),
            **{"text-align": "left"},
        )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=min(520, 90 + 36 * len(display_df)),
    )


# ============================================================
# SECTION WRAPPERS
# ============================================================


def section_start(
    section_id: str,
    number: str,
    title: str,
    description: str = "",
):

    render_html(
        f"""
        <section
            id="{section_id}"
            class="factory-section"
        >

            <div class="section-header">

                <div class="section-kicker">
                    Section {number}
                </div>

                <div class="section-main-title">
                    {title}
                </div>

            </div>
        """
    )


def section_end():

    render_html(
        """
        </section>
        """
    )


def top_navigation(pages: List[str]):
    links = " ".join(
        f'<a href="#factory-{page.lower().replace(" ", "-")}">{page}</a>'
        for page in pages
    )

    render_html(
        f"""
        <div class="factory-topbar">
            <div style="width:100%;">
                <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;">
                    <div>
                        <span class="factory-topbar-brand">FactoryOps</span>
                        <span class="factory-topbar-sub">Smart Factory Intelligence</span>
                    </div>
                    <div class="factory-nav-note">Predictive Maintenance Platform</div>
                </div>
                <div class="factory-nav-links">
                    {links}
                </div>
            </div>
        </div>
        """
    )

    c1, c2, c3 = st.columns([1, 1, 8])
    with c1:
        if st.button("Refresh", use_container_width=True, key="top_refresh"):
            st.rerun()
    with c2:
        if st.button("Logout", use_container_width=True, key="top_logout"):
            st.session_state.clear()
            st.rerun()


# ============================================================
# LOGIN PAGE
# ============================================================


def login_page():
    bg_base64 = get_login_bg_base64()

    render_html('<div class="login-backdrop-overlay"></div>')

    with st.container(key="login_frame"):
        col1, col2 = st.columns([1, 1], gap="small")

        with col1:
            render_html(
                f"""
                <div class="login-hero-container" style="background-image: url('data:image/png;base64,{bg_base64}');">
                    <div class="login-hero-content-box">
                        <div class="hero-title-brand">FactoryOps</div>
                        <div class="hero-tagline-text">Smart Operations. Stronger Tomorrow.</div>
                        <div class="hero-divider-bar"></div>
                    </div>
                </div>
                """
            )

        with col2:
            render_html(
                """
                <script>
                (() => {
                    function applyMockupTheme() {
                        document.querySelectorAll('[data-testid="stTextInput"] div[data-baseweb="input"]').forEach(el => {
                            el.style.setProperty('background-color', 'rgba(6, 18, 48, 0.75)', 'important');
                            el.style.setProperty('border', '1.5px solid #2563eb', 'important');
                            el.style.setProperty('border-radius', '12px', 'important');
                        });
                        document.querySelectorAll('[data-testid="stTextInput"] div[data-baseweb="input"] div, [data-testid="stTextInput"] div[data-baseweb="base-input"]').forEach(el => {
                            el.style.setProperty('background-color', 'transparent', 'important');
                            el.style.setProperty('border', 'none', 'important');
                        });
                        document.querySelectorAll('[data-testid="stTextInput"] input').forEach(el => {
                            el.style.setProperty('background-color', 'transparent', 'important');
                            el.style.setProperty('color', '#ffffff', 'important');
                        });
                        document.querySelectorAll('[data-testid="stRadio"] [role="radiogroup"] input:checked').forEach(radio => {
                            const container = radio.closest('label');
                            if (container) {
                                const dots = container.querySelectorAll('div > div');
                                if (dots.length > 1) {
                                    dots[1].style.setProperty('background-color', '#2563eb', 'important');
                                }
                            }
                        });
                    }
                    applyMockupTheme();
                    setInterval(applyMockupTheme, 250);
                })();
                </script>
                """
            )

            with st.container(key="login_form_side"):
                render_html(
                    """
                    <div class="login-form-eyebrow">Login to your account!</div>
                    <div class="login-form-heading">Welcome Back!</div>
                    <div class="login-form-subtitle">Please enter your details to continue</div>
                    """
                )

                portal = st.radio(
                    "Portal",
                    ["User Portal", "Admin Portal"],
                    horizontal=True,
                    label_visibility="collapsed",
                    key="login_portal",
                )

                with st.form("login_form", clear_on_submit=False):
                    username = st.text_input(
                        "Username",
                        placeholder="Enter your username",
                        key="login_username",
                    )
                    password = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Enter your password",
                        key="login_password",
                    )
                    submitted = st.form_submit_button(
                        "Sign In",
                        use_container_width=True,
                        type="primary",
                    )

    if submitted:
        valid_admin = (
            portal == "Admin Portal"
            and username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        )
        valid_user = (
            portal == "User Portal"
            and username == USER_USERNAME
            and password == USER_PASSWORD
        )

        if valid_admin or valid_user:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = "admin" if valid_admin else "user"
            st.session_state.page = "Dashboard"
            st.rerun()
        else:
            st.error("Invalid username or password for the selected portal.")


# ============================================================
# DASHBOARD
# ============================================================


def dashboard_page():

    section_start(
        "factory-dashboard",
        "01",
        "Factory Dashboard",
    )

    dashboard, error = safe_get("/dashboard/summary")

    if error:

        st.error(error)

        st.info("Start the backend first, then refresh this page.")

        section_end()
        return

    if not isinstance(
        dashboard,
        dict,
    ):

        st.error("Dashboard API returned an unexpected response.")

        section_end()
        return

    cols = st.columns(5)

    with cols[0]:

        metric_card(
            "Factory Status",
            dashboard.get(
                "factory_status",
                "—",
            ),
        )

    with cols[1]:

        metric_card(
            "Total Machines",
            dashboard.get(
                "total_machines",
                0,
            ),
        )

    with cols[2]:

        metric_card(
            "Healthy",
            dashboard.get(
                "healthy_machines",
                0,
            ),
        )

    with cols[3]:

        metric_card(
            "Warning",
            dashboard.get(
                "warning_machines",
                0,
            ),
        )

    with cols[4]:

        metric_card(
            "Critical",
            dashboard.get(
                "critical_machines",
                0,
            ),
        )

    cols = st.columns(5)

    with cols[0]:

        metric_card(
            "Average Health",
            f"{fmt_number(dashboard.get('average_health_score'), 1)}%",
        )

    with cols[1]:

        metric_card(
            "Availability",
            dashboard.get(
                "machine_availability",
                "—",
            ),
        )

    with cols[2]:

        metric_card(
            "Active Alerts",
            dashboard.get(
                "active_alerts",
                0,
            ),
        )

    with cols[3]:

        metric_card(
            "Maintenance Due",
            dashboard.get(
                "maintenance_due",
                0,
            ),
        )

    with cols[4]:

        metric_card(
            "High Failure Risk",
            dashboard.get(
                "high_failure_risk",
                0,
            ),
        )

    render_html(
        """
        <div class="section-title">
            Health Overview
        </div>
        """
    )

    healthy = int(
        dashboard.get(
            "healthy_machines",
            0,
        )
        or 0
    )

    warning = int(
        dashboard.get(
            "warning_machines",
            0,
        )
        or 0
    )

    critical = int(
        dashboard.get(
            "critical_machines",
            0,
        )
        or 0
    )

    total_health = healthy + warning + critical

    healthy_percent = healthy / total_health * 100 if total_health else 0
    warning_percent = warning / total_health * 100 if total_health else 0
    critical_percent = critical / total_health * 100 if total_health else 0

    if total_health > 0:
        health_data = pd.DataFrame(
            {
                "Status": ["Healthy", "Warning", "Critical"],
                "Machines": [healthy, warning, critical],
            }
        )

        chart_col, summary_col = st.columns([1.35, 1], gap="large")

        with chart_col:
            render_html(
                """
                <div class="health-card">
                    <div class="health-chart-title">
                        Machine Health Overview
                    </div>
                    <div class="health-chart-subtitle">
                        Distribution of current machine health status
                    </div>
                """
            )

            chart = {
                "mark": {"type": "arc", "innerRadius": 58},
                "encoding": {
                    "theta": {"field": "Machines", "type": "quantitative"},
                    "color": {
                        "field": "Status",
                        "type": "nominal",
                        "scale": {
                            "domain": ["Healthy", "Warning", "Critical"],
                            "range": ["#16a34a", "#f59e0b", "#dc2626"],
                        },
                        "legend": {"title": None, "orient": "bottom"},
                    },
                    "tooltip": [
                        {"field": "Status", "type": "nominal"},
                        {"field": "Machines", "type": "quantitative"},
                    ],
                },
                "width": "container",
                "height": 300,
            }

            st.vega_lite_chart(
                health_data,
                chart,
                use_container_width=True,
            )
            render_html("</div>")

        with summary_col:
            render_html(
                f"""
                <div class="health-card">
                    <div class="health-chart-title">
                        Health Summary
                    </div>
                    <div class="health-legend">
                        <div class="legend-row">
                            <div class="legend-left">
                                <div class="legend-dot" style="background:#16a34a;"></div>
                                Healthy
                            </div>
                            <div class="legend-value">
                                {healthy}
                                <span class="legend-percentage">({healthy_percent:.1f}%)</span>
                            </div>
                        </div>
                        <div class="legend-row">
                            <div class="legend-left">
                                <div class="legend-dot" style="background:#f59e0b;"></div>
                                Warning
                            </div>
                            <div class="legend-value">
                                {warning}
                                <span class="legend-percentage">({warning_percent:.1f}%)</span>
                            </div>
                        </div>
                        <div class="legend-row">
                            <div class="legend-left">
                                <div class="legend-dot" style="background:#dc2626;"></div>
                                Critical
                            </div>
                            <div class="legend-value">
                                {critical}
                                <span class="legend-percentage">({critical_percent:.1f}%)</span>
                            </div>
                        </div>
                    </div>
                </div>
                """
            )
    else:
        st.info("No machine health data is currently available.")

    render_html(
        """
        <div class="section-title">
            Quick Actions
        </div>
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button(
            "View Machines",
            use_container_width=True,
            key="quick_machines",
        ):

            st.session_state.page = "Machines"
            st.rerun()

    with c2:

        if st.button(
            "View Predictions",
            use_container_width=True,
            key="quick_predictions",
        ):

            st.session_state.page = "Predictions"
            st.rerun()

    with c3:

        if st.button(
            "View Incidents",
            use_container_width=True,
            key="quick_incidents",
        ):

            st.session_state.page = "Incidents"
            st.rerun()

    section_end()


# ============================================================
# MACHINES
# ============================================================


def machines_page():

    section_start(
        "factory-machines",
        "02",
        "Machines",
    )

    data, error = fetch_first(
        [
            "/machines",
            "/machine",
        ]
    )

    if error:

        st.error(error)
        section_end()
        return

    rows = extract_list(data)

    if not rows:

        st.warning("No machines returned by the API.")

        section_end()
        return

    df = normalize_dataframe(rows)

    search = st.text_input(
        "Search machine",
        placeholder="Machine code or name",
        key="machines_search",
    )

    if search:

        mask = (
            df.astype(str)
            .apply(
                lambda col: col.str.contains(
                    search,
                    case=False,
                    na=False,
                )
            )
            .any(axis=1)
        )

        df = df[mask]

    display_table(df)

    st.caption(f"{len(df)} machine(s) shown.")

    section_end()


# ============================================================
# SENSORS
# ============================================================


def sensors_page():

    section_start(
        "factory-sensors",
        "03",
        "Sensor Monitoring",
    )

    machine_id = st.number_input(
        "Machine ID",
        min_value=1,
        value=100,
        step=1,
        key="sensor_machine_id",
    )

    data, error = fetch_first(
        [
            f"/sensors/machine/{machine_id}",
            f"/sensors?machine_id={machine_id}",
        ]
    )

    if error:

        data, error = fetch_first(
            [
                "/sensors",
                "/sensor",
            ]
        )

    if error:

        st.error(error)
        section_end()
        return

    rows = extract_list(data)

    if not rows:

        st.warning("No sensor readings found.")

        section_end()
        return

    df = normalize_dataframe(rows)

    numeric_cols = [
        column
        for column in [
            "temperature",
            "vibration",
            "pressure",
            "humidity",
            "voltage",
            "current",
        ]
        if column in df.columns
    ]

    units = {
        "temperature": "Celsius (°C)",
        "vibration": "millimeters per second (mm/s)",
        "pressure": "bar",
        "humidity": "percent (%)",
        "voltage": "volts (V)",
        "current": "amperes (A)",
    }

    if numeric_cols:

        render_html(
            """
            <div class="section-title">
                Latest Reading
            </div>
            """
        )

        latest = df.iloc[0]

        cols = st.columns(
            min(
                len(numeric_cols),
                6,
            )
        )

        for column, sensor_name in zip(
            cols,
            numeric_cols,
        ):

            with column:

                unit = units.get(
                    sensor_name,
                    "",
                )

                value = fmt_number(latest[sensor_name])

                metric_card(
                    sensor_name.replace(
                        "_",
                        " ",
                    ).title(),
                    f"{value} {unit}",
                )

    render_html(
        """
        <div class="section-title">
            Sensor Data
        </div>
        """
    )

    display_table(df, units=units)

    section_end()


# ============================================================
# PREDICTIONS
# ============================================================


def predictions_page():

    section_start(
        "factory-predictions",
        "04",
        "Failure Predictions",
    )

    data, error = fetch_first(
        [
            "/predictions",
            "/prediction",
        ]
    )

    if error:

        st.error(error)
        section_end()
        return

    rows = extract_list(data)

    if not rows:

        st.warning("No predictions returned by the API.")

        section_end()
        return

    df = normalize_dataframe(rows)

    if "risk_level" in df.columns:

        risk_filter = st.selectbox(
            "Risk Level",
            options=["High", "Medium", "Low"],
            index=None,
            placeholder="Select risk level",
            key="prediction_risk_filter",
        )

        if risk_filter:
            df = df[df["risk_level"].astype(str).str.lower().eq(risk_filter.lower())]

    if "health_score" in df.columns:

        df["health_score"] = pd.to_numeric(
            df["health_score"],
            errors="coerce",
        )

    if "failure_probability" in df.columns:

        df["failure_probability"] = pd.to_numeric(
            df["failure_probability"],
            errors="coerce",
        )

    c1, c2, c3 = st.columns(3)

    with c1:

        high_count = (
            int((df["risk_level"].astype(str).str.lower() == "high").sum())
            if "risk_level" in df.columns
            else 0
        )

        metric_card(
            "High Risk",
            high_count,
        )

    with c2:

        avg_health = df["health_score"].mean() if "health_score" in df.columns else 0

        metric_card(
            "Average Health",
            f"{avg_health:.1f}%",
        )

    with c3:

        avg_probability = (
            df["failure_probability"].mean()
            if "failure_probability" in df.columns
            else 0
        )

        metric_card(
            "Avg Failure Probability",
            f"{avg_probability:.1f}%",
        )

    preferred = [
        "machine_id",
        "health_score",
        "failure_probability",
        "risk_level",
        "predicted_failure",
        "estimated_failure_days",
        "confidence_score",
    ]

    visible = [column for column in preferred if column in df.columns]

    display_df = df[visible] if visible else df

    display_table(display_df)

    section_end()


# ============================================================
# RISK ANALYSIS
# ============================================================


def risk_page():
    section_start(
        "factory-risk-analysis",
        "05",
        "Risk Analysis",
    )

    data, error = fetch_first(["/predictions", "/prediction"])

    if error:
        st.error(error)
        section_end()
        return

    rows = extract_list(data)
    if not rows:
        st.info("No prediction data is currently available.")
        section_end()
        return

    df = normalize_dataframe(rows)

    if "risk_level" not in df.columns:
        st.info("Risk level is not available in the prediction response.")
        section_end()
        return

    selected = st.selectbox(
        "Risk Level",
        ["High", "Medium", "Low"],
        index=None,
        placeholder="Select risk level",
        key="risk_analysis_filter",
    )

    if selected:
        df = df[df["risk_level"].astype(str).str.lower().eq(selected.lower())]

    display_table(df)
    st.caption(f"{len(df)} risk record(s) shown.")

    section_end()


# ============================================================
# MAINTENANCE
# ============================================================


def maintenance_page():

    section_start(
        "factory-maintenance",
        "06",
        "Maintenance",
    )

    data, error = fetch_first(
        [
            "/maintenance",
            "/maintenances",
        ]
    )

    if error:

        st.error(error)
        section_end()
        return

    rows = extract_list(data)

    if rows:

        df = normalize_dataframe(rows)

        display_table(df)

        st.caption(f"{len(df)} maintenance record(s) shown.")

    else:

        st.info("No maintenance records are currently available.")

    render_html(
        """
        <div class="section-title">
            Maintenance Recommendation
        </div>
        """
    )

    machine_id = st.number_input(
        "Machine ID for recommendation",
        min_value=1,
        value=1,
        step=1,
        key="maintenance_machine_id",
    )

    if st.button(
        "Get Recommendation",
        type="primary",
        key="get_maintenance_recommendation",
    ):

        prediction_data, prediction_error = fetch_first(
            [
                f"/predictions/machine/{machine_id}",
                f"/predictions/{machine_id}",
            ]
        )

        if prediction_error:

            st.error(prediction_error)

            section_end()
            return

        prediction_rows = extract_list(prediction_data)

        prediction = (
            prediction_rows[0]
            if prediction_rows
            else (
                prediction_data
                if isinstance(
                    prediction_data,
                    dict,
                )
                else None
            )
        )

        if not prediction:

            st.warning("No prediction found for this machine.")

            section_end()
            return

        st.json(prediction)

    section_end()


# ============================================================
# INCIDENTS
# ============================================================


def incidents_page():

    section_start(
        "factory-incidents",
        "07",
        "Incidents & Alerts",
    )

    data, error = fetch_first(
        [
            "/incidents",
            "/incident",
        ]
    )

    if error:

        st.error(error)
        section_end()
        return

    rows = extract_list(data)

    if not rows:

        st.info("No incidents returned by the API.")

        section_end()
        return

    df = normalize_dataframe(rows)

    st.metric(
        "Total Incidents",
        len(df),
    )

    if "status" in df.columns:

        statuses = sorted(df["status"].dropna().astype(str).unique())

        selected = st.multiselect(
            "Filter by Status",
            statuses,
            default=statuses,
            key="incident_status_filter",
        )

        df = df[df["status"].astype(str).isin(selected)]

    display_table(df)

    section_end()


# ============================================================
# HELP
# ============================================================


def help_page():

    section_start(
        "factory-help",
        "08",
        "Help & Support",
    )

    render_html(
        """
        <div class="section-title">
            Using FactoryOps
        </div>
        """
    )

    st.write(
        """
        **Dashboard** provides an overview of factory operations,
        machine health and active alerts.

        **Machines** displays your available machine inventory.

        **Sensors** allows you to monitor machine sensor readings
        with their respective SI units.

        **Predictions** displays failure probabilities and risk levels.

        **Maintenance** provides maintenance records and recommendations.

        **Incidents** helps you monitor operational incidents and alerts.
        """
    )

    render_html(
        """
        <div class="section-title">
            Need assistance?
        </div>
        """
    )

    st.info(
        "Use the navigation above to move between operational areas. "
        "If a page cannot load data, make sure the FastAPI service is running "
        "and then select Refresh."
    )

    with st.expander("What does each area do?"):
        st.write(
            "- Dashboard: factory health and key operational indicators.\n"
            "- Machines: machine inventory and search.\n"
            "- Sensors: latest telemetry with measurement units.\n"
            "- Predictions: failure probability and risk levels.\n"
            "- Risk Analysis: filter machines by High, Medium or Low risk.\n"
            "- Maintenance: maintenance history and recommendations.\n"
            "- Incidents: operational incidents and alerts."
        )

    with st.expander("User vs Admin Portal"):
        st.write(
            "Both portals use Streamlit session state for access control. "
            "The selected role is stored only for the current Streamlit session."
        )

    section_end()


# ============================================================
# MAIN APPLICATION
# ============================================================


def main():

    if not st.session_state.authenticated:
        login_page()
        return

    pages = [
        "Dashboard",
        "Machines",
        "Sensors",
        "Predictions",
        "Risk Analysis",
        "Maintenance",
        "Incidents",
        "Help",
    ]

    top_navigation(pages)

    # ========================================================
    # CONTINUOUS SCROLLING WORKSPACE
    # ========================================================

    dashboard_page()

    machines_page()

    sensors_page()

    predictions_page()

    risk_page()

    maintenance_page()

    incidents_page()

    help_page()

    # ========================================================
    # SCROLL SPY
    # ========================================================

    inject_scroll_spy()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()

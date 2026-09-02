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
    initial_sidebar_state="expanded",
)

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

REQUEST_TIMEOUT = 8


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
           SIDEBAR
           ================================================== */

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #0f172a 0%,
                    #111827 50%,
                    #172033 100%
                );

            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }

        .brand {
            font-size: 1.55rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            margin-bottom: 0.15rem;
            padding-top: 0.3rem;
        }

        .brand-sub {
            color: #94a3b8 !important;
            font-size: 0.76rem;
            margin-bottom: 1.2rem;
        }


        /* ==================================================
           SIDEBAR BUTTONS
           ================================================== */

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;

            background: rgba(255,255,255,0.08) !important;

            color: #f8fafc !important;

            border: 1px solid rgba(255,255,255,0.16) !important;

            border-radius: 10px !important;

            font-weight: 650 !important;

            min-height: 42px;

            transition:
                background 0.2s ease,
                border-color 0.2s ease,
                transform 0.15s ease;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255,255,255,0.15) !important;

            border-color: rgba(255,255,255,0.28) !important;

            color: #ffffff !important;

            transform: translateY(-1px);
        }

        [data-testid="stSidebar"] .stButton > button:active {
            background: rgba(255,255,255,0.20) !important;
        }

        [data-testid="stSidebar"] .stButton > button p {
            color: #f8fafc !important;
            font-weight: 650 !important;
        }


        /* ==================================================
           LOGIN PAGE
           ================================================== */

        .login-left {
            padding: 3rem;
            border-radius: 24px;
            background:
                linear-gradient(
                    135deg,
                    rgba(30, 64, 175, 0.94),
                    rgba(14, 116, 144, 0.90)
                );
            box-shadow:
                0 20px 45px rgba(15, 23, 42, 0.16);
            min-height: 440px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .login-brand {
            color: white;
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -0.05em;
            margin-bottom: 0.8rem;
        }

        .login-brand-icon {
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
        }

        .login-description {
            color: rgba(255,255,255,0.88);
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }

        .login-feature {
            color: rgba(255,255,255,0.9);
            font-size: 0.9rem;
            line-height: 1.9;
        }

        .login-card {
            background: rgba(255,255,255,0.96);
            border-radius: 20px;
            padding: 2rem;
            min-height: 190px;
            box-shadow:
                0 15px 35px rgba(15,23,42,0.10);
            border: 1px solid #e2e8f0;
            margin-bottom: 1rem;
        }

        .login-heading {
            color: #111827;
            font-size: 1.8rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        .portal-label {
            color: #64748b;
            font-size: 0.9rem;
        }


        /* ==================================================
           LOGIN FORM
           ================================================== */

        [data-testid="stForm"] {
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            padding: 0.75rem !important;
            background: rgba(255,255,255,0.20) !important;
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
            background: rgba(255,255,255,0.42);
            box-shadow:
                0 5px 20px rgba(15,23,42,0.035);
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
            background:
                linear-gradient(
                    180deg,
                    #2563eb,
                    #0ea5e9
                );
        }

        .section-header {
            margin-bottom: 1rem;
        }

        .section-kicker {
            color: #2563eb;
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 0.35rem;
        }

        .section-main-title {
            color: #0f172a;
            font-size: 2rem;
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
            font-size: 0.82rem;
            font-weight: 600;
        }

        .metric-value {
            color: #111827;
            font-size: 1.65rem;
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
            font-size: 1.25rem;
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
            text-align: right !important;
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

            .login-left {
                padding: 2rem;
                min-height: auto;
            }

            .login-brand {
                font-size: 2.3rem;
            }
        }

    </style>
    """
)


# ============================================================
# SCROLL-SPY JAVASCRIPT
# ============================================================

def inject_scroll_spy():

    render_html(
        """
        <script>

        (function() {

            const sectionNames = [
                "Dashboard",
                "Machines",
                "Sensors",
                "Predictions",
                "Maintenance",
                "Incidents",
                "Help"
            ];

            const sectionIds = [
                "factory-dashboard",
                "factory-machines",
                "factory-sensors",
                "factory-predictions",
                "factory-maintenance",
                "factory-incidents",
                "factory-help"
            ];


            function findSection(name) {

                const id = "factory-" +
                    name.toLowerCase();

                return document.getElementById(id);
            }


            function updateSidebar() {

                let activeIndex = 0;

                let bestDistance = Infinity;

                sectionIds.forEach(
                    function(id, index) {

                        const section =
                            document.getElementById(id);

                        if (!section) {
                            return;
                        }

                        const rect =
                            section.getBoundingClientRect();

                        const distance =
                            Math.abs(rect.top - 130);

                        if (
                            rect.top <= 180 &&
                            distance < bestDistance
                        ) {

                            bestDistance = distance;
                            activeIndex = index;
                        }

                    }
                );


                const sidebar =
                    document.querySelector(
                        '[data-testid="stSidebar"]'
                    );

                if (!sidebar) {
                    return;
                }


                const radios =
                    sidebar.querySelectorAll(
                        'input[type="radio"]'
                    );


                if (
                    radios.length >=
                    sectionNames.length
                ) {

                    const target =
                        radios[activeIndex];

                    if (
                        target &&
                        !target.checked
                    ) {

                        target.click();
                    }
                }

            }


            function scrollToSection(name) {

                const section =
                    findSection(name);

                if (!section) {
                    return;
                }

                section.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }


            let ticking = false;

            window.addEventListener(
                "scroll",
                function() {

                    if (!ticking) {

                        window.requestAnimationFrame(
                            function() {

                                updateSidebar();

                                ticking = false;

                            }
                        );

                        ticking = true;
                    }

                },
                { passive: true }
            );


            document.addEventListener(
                "click",
                function(event) {

                    const target =
                        event.target.closest(
                            '[data-testid="stSidebar"] label'
                        );

                    if (!target) {
                        return;
                    }


                    const text =
                        target.innerText.trim();

                    const index =
                        sectionNames.indexOf(text);

                    if (index !== -1) {

                        setTimeout(
                            function() {

                                scrollToSection(
                                    sectionNames[index]
                                );

                            },
                            150
                        );

                    }

                }
            );


            setTimeout(
                updateSidebar,
                1000
            );

        })();

        </script>
        """
    )


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

        return api_get(
            path,
            params=params,
        ), None

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

        status = (
            exc.response.status_code
            if exc.response is not None
            else "unknown"
        )

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

        errors.append(
            f"{path}: {error}"
        )

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
):

    if df.empty:

        st.info(
            "No data available."
        )

        return

    html = """
    <div class="factory-table-wrapper">

        <table class="factory-table">

            <thead>

                <tr>
    """

    for column in df.columns:

        header = (
            str(column)
            .replace(
                "_",
                " ",
            )
            .title()
        )

        html += f"""
                    <th>
                        {header}
                    </th>
        """

    html += """
                </tr>

            </thead>

            <tbody>
    """

    for _, row in df.iterrows():

        html += """
                <tr>
        """

        for value in row:

            if pd.isna(value):

                display_value = "—"

            else:

                display_value = str(value)

            html += f"""
                    <td>
                        {display_value}
                    </td>
            """

        html += """
                </tr>
        """

    html += """
            </tbody>

        </table>

    </div>
    """

    render_html(html)


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


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    left_column, right_column = st.columns(
        [1.05, 1],
        gap="large",
    )


    with left_column:

        render_html(
            """
            <div class="login-left">

                <div class="login-brand-icon">
                    🏭
                </div>

                <div class="login-brand">
                    FactoryOps
                </div>

                <div class="login-description">
                    Intelligent predictive maintenance and
                    factory operations management in one platform.
                </div>

                <div class="login-feature">
                    Monitor machines<br>
                    Track sensor performance<br>
                    Predict equipment failures<br>
                    Manage maintenance and incidents
                </div>

            </div>
            """
        )


    with right_column:

        render_html(
            """
            <div class="login-card">

                <div class="login-heading">
                    Welcome Back
                </div>

                <div class="portal-label">
                    Sign in to access FactoryOps
                </div>

            </div>
            """
        )


        portal = st.radio(
            "Portal",
            [
                "User Portal",
                "Admin Portal",
            ],
            horizontal=True,
            label_visibility="collapsed",
        )


        st.write("")


        with st.form(
            "login_form",
            clear_on_submit=False,
        ):

            username = st.text_input(
                "Username",
                placeholder="Enter username",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password",
            )

            submitted = st.form_submit_button(
                "Sign In",
                use_container_width=True,
                type="primary",
            )


            if submitted:

                if (
                    portal == "Admin Portal"
                    and username == ADMIN_USERNAME
                    and password == ADMIN_PASSWORD
                ):

                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.role = "admin"

                    st.rerun()


                elif (
                    portal == "User Portal"
                    and username == USER_USERNAME
                    and password == USER_PASSWORD
                ):

                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.role = "user"

                    st.rerun()


                else:

                    st.error(
                        "Invalid username or password for the selected portal."
                    )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_page():

    section_start(
        "factory-dashboard",
        "01",
        "Factory Dashboard",
    )


    dashboard, error = safe_get(
        "/dashboard/summary"
    )


    if error:

        st.error(error)

        st.info(
            "Start the backend first, then refresh this page."
        )

        section_end()
        return


    if not isinstance(
        dashboard,
        dict,
    ):

        st.error(
            "Dashboard API returned an unexpected response."
        )

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
            f"{fmt_number(
                dashboard.get(
                    "average_health_score"
                ),
                1,
            )}%",
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
        ) or 0
    )

    warning = int(
        dashboard.get(
            "warning_machines",
            0,
        ) or 0
    )

    critical = int(
        dashboard.get(
            "critical_machines",
            0,
        ) or 0
    )


    total_health = (
        healthy
        + warning
        + critical
    )


    if total_health > 0:

        healthy_percent = (
            healthy
            / total_health
        ) * 100

        warning_percent = (
            warning
            / total_health
        ) * 100

        critical_percent = (
            critical
            / total_health
        ) * 100


        healthy_end = round(
            healthy_percent,
            2,
        )

        warning_end = round(
            healthy_percent
            + warning_percent,
            2,
        )


        chart_col, summary_col = st.columns(
            [1.2, 1],
            gap="large",
        )


        with chart_col:

            render_html(
                f"""
                <div class="health-card">

                    <div class="health-chart-title">
                        Machine Health Distribution
                    </div>

                    <div class="health-chart-subtitle">
                        Current machine status across the factory
                    </div>

                    <div class="health-overview-wrapper">

                        <div
                            class="donut-chart"
                            style="
                                background:
                                conic-gradient(
                                    from -90deg,
                                    #22c55e 0% {healthy_end}%,
                                    #f59e0b {healthy_end}% {warning_end}%,
                                    #ef4444 {warning_end}% 100%
                                );
                            "
                        >

                            <div class="donut-center">

                                <div class="donut-number">
                                    {total_health}
                                </div>

                                <div class="donut-text">
                                    Total Machines
                                </div>

                            </div>

                        </div>

                    </div>

                </div>
                """
            )


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

                                <div
                                    class="legend-dot"
                                    style="background:#22c55e;"
                                ></div>

                                Healthy

                            </div>

                            <div class="legend-value">

                                {healthy}

                                <span class="legend-percentage">
                                    ({healthy_percent:.1f}%)
                                </span>

                            </div>

                        </div>


                        <div class="legend-row">

                            <div class="legend-left">

                                <div
                                    class="legend-dot"
                                    style="background:#f59e0b;"
                                ></div>

                                Warning

                            </div>

                            <div class="legend-value">

                                {warning}

                                <span class="legend-percentage">
                                    ({warning_percent:.1f}%)
                                </span>

                            </div>

                        </div>


                        <div class="legend-row">

                            <div class="legend-left">

                                <div
                                    class="legend-dot"
                                    style="background:#ef4444;"
                                ></div>

                                Critical

                            </div>

                            <div class="legend-value">

                                {critical}

                                <span class="legend-percentage">
                                    ({critical_percent:.1f}%)
                                </span>

                            </div>

                        </div>

                    </div>

                </div>
                """
            )


    else:

        st.info(
            "No machine health data is currently available."
        )


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

        st.warning(
            "No machines returned by the API."
        )

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


    st.caption(
        f"{len(df)} machine(s) shown."
    )


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

        st.warning(
            "No sensor readings found."
        )

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
        "temperature": "°C",
        "vibration": "mm/s",
        "pressure": "bar",
        "humidity": "%",
        "voltage": "V",
        "current": "A",
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

                value = fmt_number(
                    latest[sensor_name]
                )


                metric_card(
                    sensor_name
                    .replace(
                        "_",
                        " ",
                    )
                    .title(),
                    f"{value} {unit}",
                )


    render_html(
        """
        <div class="section-title">
            Sensor Data
        </div>
        """
    )


    display_table(df)


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

        st.warning(
            "No predictions returned by the API."
        )

        section_end()
        return


    df = normalize_dataframe(rows)


    if "risk_level" in df.columns:

        risk_options = sorted(
            df["risk_level"]
            .dropna()
            .astype(str)
            .unique()
        )


        risk_filter = st.multiselect(
            "Risk Level",
            options=risk_options,
            default=risk_options,
            key="prediction_risk_filter",
        )


        df = df[
            df["risk_level"]
            .astype(str)
            .isin(risk_filter)
        ]


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
            int(
                (
                    df["risk_level"]
                    .astype(str)
                    .str.lower()
                    == "high"
                ).sum()
            )
            if "risk_level" in df.columns
            else 0
        )


        metric_card(
            "High Risk",
            high_count,
        )


    with c2:

        avg_health = (
            df["health_score"].mean()
            if "health_score" in df.columns
            else 0
        )


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


    visible = [
        column
        for column in preferred
        if column in df.columns
    ]


    display_df = (
        df[visible]
        if visible
        else df
    )


    display_table(display_df)


    section_end()


# ============================================================
# MAINTENANCE
# ============================================================

def maintenance_page():

    section_start(
        "factory-maintenance",
        "05",
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

        st.caption(
            f"{len(df)} maintenance record(s) shown."
        )


    else:

        st.info(
            "No maintenance records are currently available."
        )


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

            st.error(
                prediction_error
            )

            section_end()
            return


        prediction_rows = extract_list(
            prediction_data
        )


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

            st.warning(
                "No prediction found for this machine."
            )

            section_end()
            return


        st.json(
            prediction
        )


    section_end()


# ============================================================
# INCIDENTS
# ============================================================

def incidents_page():

    section_start(
        "factory-incidents",
        "06",
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

        st.info(
            "No incidents returned by the API."
        )

        section_end()
        return


    df = normalize_dataframe(rows)


    st.metric(
        "Total Incidents",
        len(df),
    )


    if "status" in df.columns:

        statuses = sorted(
            df["status"]
            .dropna()
            .astype(str)
            .unique()
        )


        selected = st.multiselect(
            "Filter by Status",
            statuses,
            default=statuses,
            key="incident_status_filter",
        )


        df = df[
            df["status"]
            .astype(str)
            .isin(selected)
        ]


    display_table(df)


    section_end()


# ============================================================
# HELP
# ============================================================

def help_page():

    section_start(
        "factory-help",
        "07",
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
            Backend Connection
        </div>
        """
    )


    st.write(
        "The application retrieves operational data from the connected FastAPI backend."
    )


    if st.button(
        "Test Backend Connection",
        type="primary",
        key="test_backend",
    ):

        data, error = safe_get(
            "/dashboard/summary"
        )


        if error:

            st.error(error)

        else:

            st.success(
                "Backend connection is working."
            )


    section_end()


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    # ========================================================
    # LOGIN
    # ========================================================

    if not st.session_state.authenticated:

        login_page()

        return


    # ========================================================
    # PAGES
    # ========================================================

    pages = [
        "Dashboard",
        "Machines",
        "Sensors",
        "Predictions",
        "Maintenance",
        "Incidents",
        "Help",
    ]


    current_page = st.session_state.get(
        "page",
        "Dashboard",
    )


    if current_page not in pages:

        current_page = "Dashboard"


    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        render_html(
            """
            <div class="brand">
                🏭 FactoryOps
            </div>
            """
        )


        render_html(
            """
            <div class="brand-sub">
                Predictive Maintenance Platform
            </div>
            """
        )


        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        page = st.radio(
            "Navigation",
            pages,
            index=pages.index(
                current_page
            ),
            label_visibility="collapsed",
        )


        st.session_state.page = page


        st.divider()


        # ----------------------------------------------------
        # REFRESH
        # ----------------------------------------------------

        if st.button(
            "Refresh Data",
            use_container_width=True,
            key="sidebar_refresh",
        ):

            st.rerun()


        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        if st.button(
            "Logout",
            use_container_width=True,
            key="sidebar_logout",
        ):

            st.session_state.clear()

            st.rerun()


        render_html(
            """
            <div class="footer-note">
                FactoryOps
            </div>
            """
        )


    # ========================================================
    # CONTINUOUS SCROLLING WORKSPACE
    # ========================================================

    dashboard_page()

    machines_page()

    sensors_page()

    predictions_page()

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

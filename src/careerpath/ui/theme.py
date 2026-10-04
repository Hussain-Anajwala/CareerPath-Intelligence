"""UI theme and custom CSS injection module for CareerPath Intelligence.

Provides a polished, high-contrast, professional design system aligning with the
Stitch UI/UX visual hierarchy, typography, colors, status badges, and tables,
while preserving 100% backend data fidelity.
"""

import streamlit as st


def inject_theme():
    """Injects Stitch-aligned design system CSS for layout, sidebar, typography, controls, and tables."""
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />

        <style>
        /* Base Typography & Color Palette */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #131B2E;
        }

        /* Streamlit Main Container Spacing */
        .main .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 3.5rem !important;
            max-width: 1240px !important;
        }

        /* Headings Hierarchy */
        h1 {
            font-family: 'Inter', sans-serif !important;
            font-size: 2.1rem !important;
            font-weight: 700 !important;
            color: #131B2E !important;
            margin-bottom: 0.4rem !important;
            letter-spacing: -0.025em !important;
        }
        h2 {
            font-family: 'Inter', sans-serif !important;
            font-size: 1.4rem !important;
            font-weight: 600 !important;
            color: #131B2E !important;
            margin-top: 1.4rem !important;
            margin-bottom: 0.7rem !important;
            letter-spacing: -0.015em !important;
        }
        h3 {
            font-family: 'Inter', sans-serif !important;
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            color: #1E293B !important;
            margin-top: 1.2rem !important;
            margin-bottom: 0.5rem !important;
        }
        h4 {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.98rem !important;
            font-weight: 600 !important;
            color: #444653 !important;
            margin-top: 0.8rem !important;
            margin-bottom: 0.4rem !important;
        }

        /* Monospace font utility class */
        .font-mono, .code-sm {
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FAF8FF !important;
            border-right: 1px solid #E2E7FF !important;
        }

        [data-testid="stSidebarNav"] {
            padding-top: 0.5rem !important;
        }

        [data-testid="stSidebarNav"] ul {
            gap: 0.25rem !important;
        }

        /* Sidebar Nav Links */
        [data-testid="stSidebarNav"] li div a {
            padding: 0.6rem 0.85rem !important;
            border-radius: 8px !important;
            background-color: transparent !important;
            transition: all 0.15s ease-in-out !important;
        }

        [data-testid="stSidebarNav"] li div a span {
            color: #444653 !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
        }

        [data-testid="stSidebarNav"] li div a:hover {
            background-color: #F2F3FF !important;
        }

        [data-testid="stSidebarNav"] li div a:hover span {
            color: #131B2E !important;
        }

        /* Sidebar Active Nav Link */
        [data-testid="stSidebarNav"] li div a[aria-current="page"] {
            background-color: #1E40AF !important;
            border-left: 3px solid #00288E !important;
            box-shadow: 0 1px 3px rgba(30, 64, 175, 0.2) !important;
        }

        [data-testid="stSidebarNav"] li div a[aria-current="page"] span {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        /* Primary & Secondary Buttons */
        div.stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            padding: 0.55rem 1.25rem !important;
            transition: all 0.15s ease-in-out !important;
            border: 1px solid #CBD5E1 !important;
            background-color: #FFFFFF !important;
            color: #131B2E !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.04) !important;
        }

        div.stButton > button:hover {
            background-color: #F8FAFC !important;
            border-color: #94A3B8 !important;
            color: #131B2E !important;
            transform: translateY(-1px);
        }

        div.stButton > button[kind="primary"] {
            background-color: #1E40AF !important;
            border-color: #1E40AF !important;
            color: #FFFFFF !important;
            box-shadow: 0 1px 3px 0 rgba(30, 64, 175, 0.25) !important;
        }

        div.stButton > button[kind="primary"]:hover {
            background-color: #1E3A8A !important;
            border-color: #1E3A8A !important;
            color: #FFFFFF !important;
        }

        /* Metric Cards */
        [data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px !important;
            padding: 1.0rem 1.2rem !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04) !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            color: #64748B !important;
            letter-spacing: 0.04em !important;
        }

        [data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 1.45rem !important;
            font-weight: 700 !important;
            color: #131B2E !important;
        }

        /* Custom Sliders */
        [data-baseweb="slider"] [role="slider"] {
            background-color: #1E40AF !important;
            border: 2px solid #FFFFFF !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.25) !important;
            width: 18px !important;
            height: 18px !important;
        }

        /* Stitch Product Cards */
        .stitch-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.03);
            transition: box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out;
        }

        .stitch-card:hover {
            border-color: #CBD5E1;
            box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.06);
        }

        .stitch-hero {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 1.75rem 2.0rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.03);
        }

        /* Skill Badges */
        .skill-tag {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            font-size: 0.84rem;
            font-weight: 500;
            margin-right: 0.4rem;
            margin-bottom: 0.5rem;
        }
        .skill-matched {
            background-color: #F0FDF4;
            color: #166534;
            border: 1px solid #DCFCE7;
        }
        .skill-partial {
            background-color: #FFFBEB;
            color: #92400E;
            border: 1px solid #FEF3C7;
        }
        .skill-missing {
            background-color: #F8FAFC;
            color: #475569;
            border: 1px solid #E2E8F0;
        }

        /* Step Card */
        .step-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.2rem;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }

        .step-number {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            font-weight: 700;
            color: #1E40AF;
            letter-spacing: 0.05em;
        }

        /* Sidebar Brand Header */
        .sidebar-brand {
            padding: 0.6rem 0.8rem 1rem 0.8rem;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 0.8rem;
        }
        .sidebar-brand-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #131B2E;
            letter-spacing: -0.01em;
        }
        .sidebar-brand-sub {
            font-size: 0.78rem;
            font-weight: 500;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-top: 2px;
        }

        /* Custom Data Tables */
        .product-table-container {
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 0.8rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }

        .product-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            text-align: left;
        }

        .product-table th {
            background-color: #F8FAFC;
            color: #475569;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 10px 16px;
            border-bottom: 1px solid #E2E8F0;
        }

        .product-table td {
            padding: 12px 16px;
            color: #131B2E;
            border-bottom: 1px solid #F1F5F9;
        }

        .product-table tr:last-child td {
            border-bottom: none;
        }

        .product-table tr:nth-child(even) {
            background-color: #FAFAFA;
        }

        .shift-badge-up {
            background-color: #F0FDF4;
            color: #166534;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.82rem;
            font-family: 'JetBrains Mono', monospace;
        }

        .shift-badge-down {
            background-color: #FEF2F2;
            color: #991B1B;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.82rem;
            font-family: 'JetBrains Mono', monospace;
        }

        .shift-badge-same {
            background-color: #F8FAFC;
            color: #64748B;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.82rem;
            font-family: 'JetBrains Mono', monospace;
        }

        /* Section Divider */
        hr {
            margin: 1.8rem 0 !important;
            border: 0 !important;
            height: 1px !important;
            background-color: #E2E8F0 !important;
        }

        /* Consolidated Product Footer */
        .product-footer {
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #E2E8F0;
            font-size: 0.82rem;
            color: #64748B;
            text-align: center;
        }
        .product-footer strong {
            color: #334155;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_sidebar_brand():
    """Renders clean, professional Stitch-aligned sidebar brand header."""
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">🎓 CareerPath</div>
            <div class="sidebar-brand-sub">INTELLIGENCE</div>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Evidence-Based Decision Support</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def inject_footer():
    """Renders a single consolidated disclaimer and platform copyright footer."""
    st.markdown(
        """
        <div class="product-footer">
            <strong>CareerPath Intelligence</strong> &bull; Evidence-based career decision-support using ESCO v1.2 taxonomy standards.
            <br>
            <span style="font-size: 0.78rem; color: #94A3B8;">Recommendations provide decision-support guidance and hypothetical scenario exploration, not deterministic guarantees of employment.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

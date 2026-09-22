"""UI theme and custom CSS injection module for CareerPath Intelligence.

Provides a polished, high-contrast, professional design system with custom
styled sliders, buttons, metric cards, data tables, and consolidated footers.
"""

import streamlit as st


def inject_theme():
    """Injects high-contrast, professional custom CSS for layout, sidebar, typography, controls, and tables."""
    st.markdown(
        """
        <style>
        /* Base Typography & Background */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #0F172A;
        }

        /* Streamlit Main Container Spacing */
        .main .block-container {
            padding-top: 1.8rem !important;
            padding-bottom: 3.5rem !important;
            max-width: 1200px !important;
        }

        /* Headings Hierarchy & Breathing Room */
        h1 {
            font-size: 2.1rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
            margin-bottom: 0.4rem !important;
            letter-spacing: -0.02em !important;
        }
        h2 {
            font-size: 1.4rem !important;
            font-weight: 600 !important;
            color: #0F172A !important;
            margin-top: 1.5rem !important;
            margin-bottom: 0.8rem !important;
        }
        h3 {
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            color: #1E293B !important;
            margin-top: 1.2rem !important;
            margin-bottom: 0.5rem !important;
        }
        h4 {
            font-size: 0.98rem !important;
            font-weight: 600 !important;
            color: #334155 !important;
            margin-top: 0.8rem !important;
            margin-bottom: 0.4rem !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #F8FAFC !important;
            border-right: 1px solid #E2E8F0 !important;
        }

        [data-testid="stSidebarNav"] {
            padding-top: 0.5rem !important;
        }

        [data-testid="stSidebarNav"] ul {
            gap: 0.25rem !important;
        }

        /* Sidebar Inactive Nav Item */
        [data-testid="stSidebarNav"] li div a {
            padding: 0.6rem 0.85rem !important;
            border-radius: 6px !important;
            background-color: transparent !important;
            transition: all 0.15s ease-in-out !important;
        }

        [data-testid="stSidebarNav"] li div a span {
            color: #334155 !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
        }

        [data-testid="stSidebarNav"] li div a:hover {
            background-color: #F1F5F9 !important;
        }

        [data-testid="stSidebarNav"] li div a:hover span {
            color: #0F172A !important;
        }

        /* Sidebar Active Nav Item */
        [data-testid="stSidebarNav"] li div a[aria-current="page"] {
            background-color: #EFF6FF !important;
            border-left: 3px solid #2563EB !important;
        }

        [data-testid="stSidebarNav"] li div a[aria-current="page"] span {
            color: #1E40AF !important;
            font-weight: 600 !important;
        }

        /* Custom Button Styling */
        div.stButton > button {
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            padding: 0.5rem 1.2rem !important;
            transition: all 0.15s ease-in-out !important;
            border: 1px solid #CBD5E1 !important;
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.04) !important;
        }

        div.stButton > button:hover {
            background-color: #F8FAFC !important;
            border-color: #94A3B8 !important;
            color: #0F172A !important;
            transform: translateY(-1px);
        }

        div.stButton > button[kind="primary"] {
            background-color: #2563EB !important;
            border-color: #2563EB !important;
            color: #FFFFFF !important;
            box-shadow: 0 1px 3px 0 rgba(37, 99, 235, 0.2) !important;
        }

        div.stButton > button[kind="primary"]:hover {
            background-color: #1D4ED8 !important;
            border-color: #1D4ED8 !important;
            color: #FFFFFF !important;
        }

        /* Custom Metric / Stat Card Styling */
        [data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 8px !important;
            padding: 1.0rem 1.2rem !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04) !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            color: #64748B !important;
            letter-spacing: 0.04em !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
        }

        /* Custom Slider Styling */
        [data-baseweb="slider"] [role="slider"] {
            background-color: #2563EB !important;
            border: 2px solid #FFFFFF !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.25) !important;
            width: 18px !important;
            height: 18px !important;
        }

        /* Custom Product Cards with Subtle Depth */
        .product-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 1.25rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.02);
            transition: box-shadow 0.2s ease-in-out;
        }

        .product-card:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.02);
        }

        /* Clean Skill Tags */
        .skill-tag {
            display: inline-block;
            padding: 0.3rem 0.7rem;
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

        /* Sidebar Brand Header */
        .sidebar-brand {
            padding: 0.5rem 0.8rem 1rem 0.8rem;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 0.6rem;
        }
        .sidebar-brand-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.01em;
        }
        .sidebar-brand-sub {
            font-size: 0.8rem;
            color: #64748B;
        }

        /* Custom Product Data Tables */
        .product-table-container {
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            overflow: hidden;
            margin-top: 0.8rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }

        .product-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
            text-align: left;
        }

        .product-table th {
            background-color: #F8FAFC;
            color: #475569;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 10px 16px;
            border-bottom: 1px solid #E2E8F0;
        }

        .product-table td {
            padding: 12px 16px;
            color: #0F172A;
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
        }

        .shift-badge-down {
            background-color: #FEF2F2;
            color: #991B1B;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.82rem;
        }

        .shift-badge-same {
            background-color: #F8FAFC;
            color: #64748B;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.82rem;
        }

        /* Styled Section Divider */
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
    """Renders clean, professional sidebar brand header."""
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">🎓 CareerPath</div>
            <div class="sidebar-brand-sub">Career Decision-Support Platform</div>
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
            <span style="font-size: 0.78rem; color: #94A3B8;">Recommendations are decision-support guidance, not deterministic guarantees of employment.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

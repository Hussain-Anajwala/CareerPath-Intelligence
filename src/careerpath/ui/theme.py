"""UI theme and custom CSS injection module for CareerPath Intelligence.

Provides a clean, professional, technical design system avoiding flashy gradients,
excessive emojis, or generic AI startup landing page templates.
"""

import streamlit as st


def inject_theme():
    """Injects professional custom CSS for typography, layout, borders, and cards."""
    st.markdown(
        """
        <style>
        /* Typography */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #1E293B;
        }

        /* Headers */
        h1 {
            font-size: 2.1rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: -0.02em;
        }
        h2 {
            font-size: 1.4rem !important;
            font-weight: 600 !important;
            color: #1E293B !important;
            margin-top: 1.2rem !important;
            margin-bottom: 0.5rem !important;
        }
        h3 {
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            color: #334155 !important;
            margin-top: 1rem !important;
            margin-bottom: 0.4rem !important;
        }
        h4 {
            font-size: 1.0rem !important;
            font-weight: 600 !important;
            color: #475569 !important;
        }

        /* Cards and Container Boxes */
        .system-card {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .metric-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0F172A;
        }

        /* Status Pills */
        .status-badge {
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .status-online {
            background-color: #F0FDF4;
            color: #166534;
            border: 1px solid #BBF7D0;
        }
        .status-fallback {
            background-color: #EFF6FF;
            color: #1E40AF;
            border: 1px solid #BFDBFE;
        }

        /* Sidebar Adjustments */
        [data-testid="stSidebar"] {
            background-color: #F8FAFC;
            border-right: 1px solid #E2E8F0;
        }

        /* Clean Divider */
        hr {
            margin: 1.2rem 0 !important;
            border-color: #E2E8F0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

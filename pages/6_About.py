"""Page 6 — About CareerPath Intelligence & Responsible Use.

Responsible ML guidelines, system metadata, open-source licensing, and decision-support disclaimers.
"""

import streamlit as st
from careerpath.ui.theme import inject_theme

st.set_page_config(page_title="About — CareerPath", page_icon="ℹ️", layout="wide")

inject_theme()

st.title("About")
st.markdown(
    "CareerPath Intelligence is an open-source, portfolio-grade Machine Learning & Skill Taxonomy Decision-Support Platform."
)

st.subheader("Responsible AI & Ethical Guidance Principles")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        #### What CareerPath Intelligence IS:
        - **Decision Support**: Tool for exploring alignment between student profiles and career paths.
        - **Skill Gap Inspector**: Explainable skill-gap analysis backed by European standard ESCO v1.2 taxonomy.
        - **Scenario Simulation**: Counterfactual What-If simulator to explore the impact of skill acquisition.
        - **Open Source**: Reproducible ML engineering project.
        """
    )

with col2:
    st.markdown(
        """
        #### What CareerPath Intelligence IS NOT:
        - **Not an Employment Guarantee**: Does not provide deterministic career predictions.
        - **Not a Hiring Automation Tool**: Not designed for employer screening or recruitment automation.
        - **Not a Psychological Assessment**: Does not evaluate personal or emotional traits.
        - **Not a Counselor Replacement**: Does not replace professional human career counselors.
        """
    )

st.markdown("---")
st.subheader("System Metadata & Open-Source Architecture")

st.markdown(
    """
    - **Repository**: `Hussain-Anajwala/CareerPath-Intelligence`
    - **Backend API**: FastAPI Service Layer (`/health`, `/api/v1/recommend`, `/api/v1/skill-gap`, `/api/v1/what-if`)
    - **UI Layer**: Multi-Page Streamlit Application (`app.py`, `pages/`)
    - **ML Framework**: CatBoost + LightGBM + XGBoost + Scikit-Learn
    - **Taxonomy Framework**: ESCO Taxonomy v1.2 + SentenceTransformers + FAISS Vector Index
    - **License**: MIT License (Code & Architecture)
    - **Dataset Protection**: Raw dataset `student_career_data.csv` protected under `.gitignore` (`UNVERIFIED` license status).
    """
)

st.markdown("---")
st.caption("© 2026 CareerPath Intelligence. Built for open-source reproducible machine learning excellence.")

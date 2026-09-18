"""Page 6 — About CareerPath Intelligence & Responsible Use.

Responsible ML guidelines, system metadata, open-source licensing, and decision-support disclaimers.
"""

import streamlit as st

st.set_page_config(page_title="About — CareerPath", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About CareerPath Intelligence")
st.markdown(
    "CareerPath Intelligence is an open-source, portfolio-grade Machine Learning & Skill Taxonomy Decision-Support Platform."
)

st.subheader("🛡️ Responsible AI & Ethical Guidance Principles")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        #### What CareerPath Intelligence IS:
        - ✅ A decision-support tool for exploring alignment between student profiles and career paths.
        - ✅ An explainable skill-gap inspector backed by European standard ESCO v1.2 taxonomy.
        - ✅ A counterfactual What-If simulator to explore the impact of skill acquisition.
        - ✅ An open-source, reproducible ML engineering project.
        """
    )

with col2:
    st.markdown(
        """
        #### What CareerPath Intelligence IS NOT:
        - ❌ An employment guarantee or deterministic career predictor.
        - ❌ A hiring or recruitment automation tool.
        - ❌ An evaluation of psychological, emotional, or personal traits.
        - ❌ A replacement for professional career counselors.
        """
    )

st.markdown("---")
st.subheader("⚙️ System Metadata & Open-Source Architecture")

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

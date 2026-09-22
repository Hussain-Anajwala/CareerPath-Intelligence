"""Page 4 — About & Methodology.

Comprehensive secondary reference page detailing system purpose, workflow architecture,
empirical validation metrics, responsible use principles, and technical implementation.
"""

import streamlit as st
from careerpath.ui.theme import inject_theme, inject_sidebar_brand, inject_footer

# Page Configuration
st.set_page_config(page_title="About & Methodology — CareerPath", page_icon="ℹ️", layout="wide")

# Inject Clean Design System & Sidebar Brand
inject_theme()
inject_sidebar_brand()

st.title("About & Methodology")
st.markdown(
    "CareerPath Intelligence is an explainable career decision-support platform that helps "
    "students explore career alignment, skill gaps and possible skill-improvement scenarios."
)

st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Section 1: About the Platform
# -----------------------------------------------------------------------------
st.subheader("About")
st.markdown(
    """
    CareerPath Intelligence addresses the challenge students face when evaluating how their current 
    technical competencies translate into real-world career paths. By combining supervised 
    machine learning trained on empirical student profile data with the standardized European 
    ESCO v1.2 skill taxonomy, the platform offers explainable alignment insights and actionable next steps.
    """
)

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 2: How It Works
# -----------------------------------------------------------------------------
st.subheader("How It Works")

st.markdown(
    """
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.2rem; text-align: center; font-weight: 600; color: #334155; font-size: 0.92rem; line-height: 2.0;">
        Student Profile &nbsp; ➔ &nbsp; 
        Feature Preprocessing &nbsp; ➔ &nbsp; 
        CatBoost Ranking &nbsp; ➔ &nbsp; 
        Career Recommendations &nbsp; ➔ &nbsp; 
        ESCO Skill Evidence &nbsp; ➔ &nbsp; 
        Skill Alignment & Gaps &nbsp; ➔ &nbsp; 
        What-If Simulation
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Section 3: Empirical Validation & Model Performance (Stat-Card Grid)
# -----------------------------------------------------------------------------
st.subheader("Model Validation")

st.markdown("##### Dataset & Evaluation Setup")
st.markdown(
    "• **Dataset:** N = 6,901 student profiles &nbsp;|&nbsp; "
    "• **Training Split:** 5,520 samples (80%) &nbsp;|&nbsp; "
    "• **Holdout Test Split:** 1,381 samples (20%) &nbsp;|&nbsp; "
    "• **Selected Model:** **CatBoost Classifier**"
)

st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)

st.markdown("##### Holdout Evaluation Metrics (N = 1,381)")
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric("Top-1 Accuracy", "7.60%", help="Exact top recommendation accuracy")
    st.metric("Macro F1 Score", "0.0744", help="Unweighted average macro F1 across career classes")
with m_col2:
    st.metric("Top-3 Accuracy", "25.42%", help="Target career present within top 3 recommendations")
    st.metric("Log Loss", "2.5151", help="Multiclass cross-entropy loss")
with m_col3:
    st.metric("Top-5 Accuracy", "43.01%", help="Target career present within top 5 recommendations")
    st.metric("Brier Score", "0.9221", help="Multiclass quadratic probability calibration error")

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 4: Responsible Use Principles
# -----------------------------------------------------------------------------
st.subheader("Responsible Use & Limitations")

resp_col1, resp_col2 = st.columns(2)

with resp_col1:
    st.markdown("##### System Intent & Scope")
    st.markdown("• **Decision Support:** Designed for student self-assessment and career exploration.")
    st.markdown("• **Explainable Evidence:** Uses standard ESCO skills to make recommendations transparent.")
    st.markdown("• **Scenario Testing:** Allows exploring hypothetical skill development pathways.")

with resp_col2:
    st.markdown("##### Clear Boundaries & Non-Goals")
    st.markdown("• **Not an Employment Guarantee:** Recommendations reflect model patterns, not employment outcomes.")
    st.markdown("• **Not a Hiring Tool:** Not intended for employer recruitment or candidate filtering.")
    st.markdown("• **Not a Psychological Assessment:** Evaluates technical evidence, not personal traits.")
    st.markdown("• **Not a Counselor Replacement:** Complements human career guidance.")

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 5: Technical Details
# -----------------------------------------------------------------------------
st.subheader("Technical Architecture")

t_col1, t_col2 = st.columns(2)

with t_col1:
    st.markdown("• **Web Interface:** Multi-page Streamlit application (`app.py`, `pages/`)")
    st.markdown("• **Service Layer:** FastAPI application (`src/careerpath/api/app.py`)")
    st.markdown("• **ML Engine:** CatBoost classifier with scikit-learn preprocessing")

with t_col2:
    st.markdown("• **Taxonomy Standard:** ESCO v1.2 occupation and skill hierarchy")
    st.markdown("• **Vector Search:** FAISS (`IndexFlatIP`) with Sentence Transformers (`all-MiniLM-L6-v2`)")
    st.markdown("• **Data Persistence:** SQLite database via SQLAlchemy ORM")

# Single Consolidated Footer
inject_footer()

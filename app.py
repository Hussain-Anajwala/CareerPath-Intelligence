"""CareerPath Intelligence — Main Landing Dashboard.

Presents the career intelligence platform, active system status, guided workflow
navigation across assessment, recommendations, skill gap inspection, and What-If simulation.
"""

import os
import streamlit as st
from careerpath.ui.client import ServiceClient
from careerpath.ui.theme import inject_theme

# Page Configuration
st.set_page_config(
    page_title="CareerPath Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Clean Design System
inject_theme()

# Sidebar Configuration
st.sidebar.title("System Configuration")
api_url_input = st.sidebar.text_input(
    "API Service URL (`CAREERPATH_API_URL`)",
    value=os.getenv("CAREERPATH_API_URL", "http://127.0.0.1:8000"),
    help="FastAPI server endpoint URL. If offline, the application seamlessly uses the local engine fallback.",
)

client = ServiceClient(api_url=api_url_input)

# Check API Server Status
is_online, status_msg = client.check_api_health()
if is_online:
    st.sidebar.success(f"Status: {status_msg}")
else:
    st.sidebar.info(f"Status: {status_msg}")

# Initialize Session State Profile if absent
if "student_profile" not in st.session_state:
    st.session_state["student_profile"] = {
        "Database Fundamentals": 7.5,
        "Computer Networks": 6.0,
        "Software Engineering": 8.0,
        "Cyber Security": 5.0,
        "Coding Skills": 8.5,
        "Web Development": 7.0,
        "Software Testing": 6.5,
        "Technical Support": 4.0,
        "certifications": "Python Certified Associate",
        "interested_subjects": "Software Development, Cloud Systems",
    }

st.sidebar.markdown("---")
st.sidebar.subheader("Active Profile")
st.sidebar.caption("Predefined Demo Profile Loaded")
active_prof = st.session_state["student_profile"]
st.sidebar.caption(f"Coding Skills: **{active_prof.get('Coding Skills', 5.0)}/10**")
st.sidebar.caption(f"Software Engineering: **{active_prof.get('Software Engineering', 5.0)}/10**")
st.sidebar.caption(f"Cyber Security: **{active_prof.get('Cyber Security', 5.0)}/10**")

# Main Header Section
st.title("CareerPath Intelligence")
st.markdown(
    "Explainable career decision-support platform using supervised ML ranking, "
    "ESCO skill taxonomy, and scenario simulation."
)

st.markdown("---")

# System Metadata Bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("ML Model", "CatBoost", help="Gradient boosted multi-class classifier")
with col2:
    st.metric("Taxonomy", "ESCO v1.2", help="European Skills, Competencies and Occupations standard")
with col3:
    st.metric("Vector Search", "FAISS + SBERT", help="Local 384d SBERT embeddings + inner-product index")
with col4:
    st.metric("System Mode", "ML Ranking + ESCO Evidence", help="Production config α = 1.0")

st.markdown("---")

# Guided Workflow Cards Section
st.subheader("Guided Intelligence Workflow")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("#### 1. Profile Assessment")
    st.caption("Submit or adjust technical skill evidence (0-10 scale), academic scores, and domain interests.")
    if st.button("Go to Profile Assessment ➔", key="btn_prof", use_container_width=True):
        st.switch_page("pages/1_Profile_Assessment.py")

with c2:
    st.markdown("#### 2. Career Explorer")
    st.caption("Inspect ranked career recommendations with ML alignment scores and ESCO evidence breakdowns.")
    if st.button("Explore Recommendations ➔", key="btn_rec", use_container_width=True):
        st.switch_page("pages/2_Career_Explorer.py")

with c3:
    st.markdown("#### 3. Skill Gap Inspector")
    st.caption("Pinpoint exact matched, partial, and missing required skills for any target career path.")
    if st.button("Inspect Skill Gaps ➔", key="btn_gap", use_container_width=True):
        st.switch_page("pages/3_Skill_Gap.py")

with c4:
    st.markdown("#### 4. What-If Simulation")
    st.caption("Simulate counterfactual skill acquisition to observe before-vs-after ranking deltas.")
    if st.button("Launch What-If Lab ➔", key="btn_whatif", use_container_width=True):
        st.switch_page("pages/4_What_If_Lab.py")

st.markdown("---")

# Quick Baseline Overview Preview
st.subheader("Quick Recommendation Preview")
with st.spinner("Generating career intelligence preview..."):
    recs = client.get_recommendations(st.session_state["student_profile"], top_k=3, alpha=1.0)

if recs:
    p_cols = st.columns(len(recs))
    for idx, r in enumerate(recs):
        with p_cols[idx]:
            st.markdown(f"**#{idx+1} {r['career_role']}**")
            st.caption(f"ESCO Title: {r['esco_occupation_title']}")
            st.metric("Alignment Score", f"{r['final_score']:.3f}")
            st.markdown(f"• **ML Signal:** `{r['normalized_ml_score']:.3f}`")
            st.markdown(f"• **ESCO Alignment:** `{r['esco_score']:.3f}`")
            st.caption(f"Matched Skills: {len(r['matched_skills'])} | Missing Gaps: {len(r['missing_skills'])}")

st.markdown("---")
st.info(
    "**Decision-Support Notice**: CareerPath Intelligence provides evidence-based career alignment analysis. "
    "It does not predict guaranteed employment or substitute for professional academic counseling."
)

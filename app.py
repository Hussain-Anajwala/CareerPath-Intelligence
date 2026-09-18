"""CareerPath Intelligence — Streamlit Main Application & Executive Dashboard.

Main landing page presenting the career intelligence platform, active system status,
and workflow navigation across assessment, recommendations, skill gap, and What-If simulation.
"""

import os
import streamlit as st
from careerpath.ui.client import ServiceClient

# Page Configuration
st.set_page_config(
    page_title="CareerPath Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling Injection for Portfolio Aesthetics
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.15rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    .card {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1F2937;
    }
    .badge-success {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-info {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_dict_only=False if False else True,
)

# Sidebar Configuration
st.sidebar.title("⚙️ System Config")
api_url_input = st.sidebar.text_input(
    "API Service URL (`CAREERPATH_API_URL`)",
    value=os.getenv("CAREERPATH_API_URL", "http://127.0.0.1:8000"),
    help="FastAPI server endpoint URL. If offline, the application seamlessly uses the local engine fallback.",
)

client = ServiceClient(api_url=api_url_input)

# Check API Server Status
is_online, status_msg = client.check_api_health()
if is_online:
    st.sidebar.success(f"🟢 {status_msg}")
else:
    st.sidebar.info(f"🔵 {status_msg}")

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
st.sidebar.subheader("👤 Active Profile")
active_prof = st.session_state["student_profile"]
st.sidebar.caption(f"Coding Skills: **{active_prof.get('Coding Skills', 5.0)}/10**")
st.sidebar.caption(f"Software Engineering: **{active_prof.get('Software Engineering', 5.0)}/10**")
st.sidebar.caption(f"Cyber Security: **{active_prof.get('Cyber Security', 5.0)}/10**")

# Header Section
st.markdown('<div class="main-header">CareerPath Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Explainable career recommendations powered by profile evidence, machine learning, and structured ESCO skill taxonomy.</div>',
    unsafe_allow_html=True,
)

# Call to Action Banner
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("ML Signal Model", "CatBoost", delta="Selected Top-K")
with col2:
    st.metric("Taxonomy Standard", "ESCO v1.2", delta="3,039 Occupations")
with col3:
    st.metric("Semantic Index", "FAISS + SBERT", delta="all-MiniLM-L6-v2")
with col4:
    st.metric("System Mode", "Hybrid ML + ESCO", delta="Zero-Cost Local")

st.markdown("---")

# Workflow Cards Section
st.subheader("🎯 Guided Career Intelligence Workflow")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        ### 1. Assess Profile
        Submit or adjust academic scores, technical skill evidence (0–10 scale), and domain interests.
        """,
    )
    if st.button("Go to Profile Assessment ➔", key="btn_prof"):
        st.switch_page("pages/1_Profile_Assessment.py")

with c2:
    st.markdown(
        """
        ### 2. Explore Careers
        Inspect ranked career recommendations with ML alignment scores and ESCO evidence breakdowns.
        """,
    )
    if st.button("Explore Recommendations ➔", key="btn_rec"):
        st.switch_page("pages/2_Career_Explorer.py")

with c3:
    st.markdown(
        """
        ### 3. Skill Gap Analysis
        Pinpoint exact matched, partial, and missing required skills for any target career path.
        """,
    )
    if st.button("Inspect Skill Gaps ➔", key="btn_gap"):
        st.switch_page("pages/3_Skill_Gap.py")

with c4:
    st.markdown(
        """
        ### 4. What-If Simulator
        Simulate counterfactual skill acquisition to observe before-vs-after ranking deltas.
        """,
    )
    if st.button("Launch What-If Lab ➔", key="btn_whatif"):
        st.switch_page("pages/4_What_If_Lab.py")

st.markdown("---")

# Quick Baseline Overview Preview
st.subheader("⚡ Quick Recommendation Preview")
with st.spinner("Generating career intelligence preview..."):
    recs = client.get_recommendations(st.session_state["student_profile"], top_k=3, alpha=0.5)

if recs:
    p_cols = st.columns(len(recs))
    for idx, r in enumerate(recs):
        with p_cols[idx]:
            st.markdown(f"#### #{idx+1} {r['career_role']}")
            st.caption(f"ESCO Title: {r['esco_occupation_title']}")
            st.metric("Final Alignment Score", f"{r['final_score']:.3f}")
            st.markdown(f"**ML Signal:** {r['normalized_ml_score']:.3f}")
            st.markdown(f"**ESCO Alignment:** {r['esco_score']:.3f}")
            st.caption(f"Matched Skills: {len(r['matched_skills'])} / Missing: {len(r['missing_skills'])}")

st.markdown("---")
st.info(
    "💡 **Responsible Use Disclaimer**: CareerPath Intelligence provides decision-support alignment recommendations based on profile evidence and model signals. It does NOT predict guaranteed employment or real-world career outcomes."
)

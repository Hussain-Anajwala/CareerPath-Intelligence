"""CareerPath Intelligence — Product Overview.

Presents a clear, professional entry point explaining the system capabilities,
current student profile status, top career path options, and direct navigation.
"""

import streamlit as st
from careerpath.ui.client import ServiceClient
from careerpath.ui.theme import inject_theme, inject_sidebar_brand, inject_footer

# Page Configuration
st.set_page_config(
    page_title="CareerPath Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Clean Design System & Sidebar Brand
inject_theme()
inject_sidebar_brand()

# Initialize Client in Background
client = ServiceClient()

# Default Demo Profile Initialization
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

prof = st.session_state["student_profile"]

# Main Product Hero Header
st.title("CareerPath Intelligence")
st.markdown(
    "Understand which career paths align with your current skills and discover what you can improve next."
)

st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

# Primary Actions
col_b1, col_b2, _ = st.columns([1, 1, 2])
with col_b1:
    if st.button("Review Your Profile", type="primary", use_container_width=True):
        st.switch_page("pages/1_Profile_Assessment.py")
with col_b2:
    if st.button("Explore Careers", use_container_width=True):
        st.switch_page("pages/2_Career_Explorer.py")

st.markdown("---")

# Section 1: Your Profile Summary
st.subheader("Your Profile Summary")

# Extract Top Skills
skill_ratings = [
    (k, v) for k, v in prof.items() if isinstance(v, (int, float))
]
top_skills = sorted(skill_ratings, key=lambda x: x[1], reverse=True)[:3]
top_skills_formatted = ", ".join([f"{k} ({v:g}/10)" for k, v in top_skills])

cert_text = prof.get("certifications", "")
interest_text = prof.get("interested_subjects", "Software Development")

p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    st.markdown(
        """
        <div class="product-card" style="margin-bottom: 0;">
            <div style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; color: #64748B; letter-spacing: 0.05em;">Assessment Status</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin-top: 4px;">Profile Ready</div>
            <div style="font-size: 0.85rem; color: #475569; margin-top: 2px;">8 technical skill areas assessed</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p_col2:
    st.markdown(
        f"""
        <div class="product-card" style="margin-bottom: 0;">
            <div style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; color: #64748B; letter-spacing: 0.05em;">Demonstrated Strengths</div>
            <div style="font-size: 1.0rem; font-weight: 700; color: #0F172A; margin-top: 4px; line-height: 1.3;">{top_skills_formatted}</div>
            <div style="font-size: 0.85rem; color: #475569; margin-top: 2px;">Highest rated competencies</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p_col3:
    st.markdown(
        f"""
        <div class="product-card" style="margin-bottom: 0;">
            <div style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; color: #64748B; letter-spacing: 0.05em;">Stated Interests</div>
            <div style="font-size: 1.0rem; font-weight: 700; color: #0F172A; margin-top: 4px;">{interest_text or 'Not specified'}</div>
            <div style="font-size: 0.85rem; color: #475569; margin-top: 2px;">Target domain preferences</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Section 2: Top Career Alignment Options
st.subheader("Your Top Career Options")

try:
    recs = client.get_recommendations(prof, top_k=3, alpha=1.0)
except Exception:
    recs = []

if recs:
    for idx, r in enumerate(recs):
        rank = idx + 1
        role = r["career_role"]
        matched = r.get("matched_skills", [])
        partial = r.get("partial_matches", [])
        missing = r.get("missing_skills", [])
        total_req = len(matched) + len(partial) + len(missing)

        alignment_tier = (
            "Strong current alignment"
            if rank == 1
            else ("Good current alignment" if rank == 2 else "Moderate current alignment")
        )

        match_summary = (
            f"{len(matched)} of {total_req} required skills matched"
            if total_req > 0
            else f"{len(matched)} skills matched"
        )

        st.markdown(
            f"""
            <div class="product-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span style="font-size: 1.15rem; font-weight: 700; color: #0F172A;">#{rank} &nbsp; {role}</span>
                        <span style="margin-left: 10px; font-size: 0.82rem; font-weight: 600; color: #1E40AF; background-color: #EFF6FF; border: 1px solid #DBEAFE; padding: 3px 8px; border-radius: 4px;">{alignment_tier}</span>
                    </div>
                    <div style="font-size: 0.9rem; font-weight: 600; color: #334155;">
                        {match_summary}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("Complete your profile assessment to explore top career recommendations.")

# Single Consolidated Footer
inject_footer()

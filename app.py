"""CareerPath Intelligence — Product Overview.

Presents a Stitch-aligned entry point explaining system capabilities,
current student profile status, 4-step guided discovery flow, top career options,
and direct navigation CTAs.
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

# Inject Design System & Sidebar Brand
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

# System Notice Badge
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 1rem;">
        <div style="display: inline-flex; align-items: center; gap: 8px; padding: 4px 14px; border-radius: 9999px; background-color: #F2F3FF; color: #444653; font-size: 0.8rem; font-weight: 500;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background-color: #00563A;"></span>
            <span>Evidence-based mapping using ESCO v1.2 taxonomy</span>
            <span style="color: #94A3B8;">&bull;</span>
            <span style="color: #64748B;">Decision-support only (not a hiring guarantee)</span>
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #64748B;">
            ESCO Framework Aligned v1.2
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Main Hero Header
st.markdown(
    """
    <div class="stitch-hero">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; color: #1E40AF; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;">
            Algorithmic Pathways &bull; Career Decision Engine
        </div>
        <h1 style="margin-top: 0.2rem; margin-bottom: 0.6rem;">Find career paths that fit the skills you have today.</h1>
        <p style="font-size: 1.05rem; color: #444653; max-width: 800px; line-height: 1.6; margin-bottom: 1.2rem;">
            Explore your current career alignment, understand your skill gaps, and see how hypothetical skill changes can affect your recommendation ranking.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Primary Navigation CTAs
col_b1, col_b2, _ = st.columns([1.2, 1.2, 2])
with col_b1:
    if st.button("Start My Assessment ➔", type="primary", use_container_width=True):
        st.switch_page("pages/1_Profile_Assessment.py")
with col_b2:
    if st.button("Explore Career Paths", use_container_width=True):
        st.switch_page("pages/2_Career_Explorer.py")

st.markdown("---")

# 4-Step Guided Student Journey
st.subheader("Structured Pathway Discovery")
st.caption("Four-step methodology for evidence-based career self-assessment.")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(
        """
        <div class="step-card">
            <div>
                <div class="step-number">STEP 01</div>
                <div style="font-size: 1.0rem; font-weight: 700; color: #131B2E; margin-top: 6px; margin-bottom: 4px;">Build your profile</div>
                <div style="font-size: 0.84rem; color: #444653; line-height: 1.45;">Rate 8 technical skill areas (0–10 scale) and record academic background.</div>
            </div>
            <div style="margin-top: 12px; font-size: 0.76rem; font-weight: 600; color: #166534; background-color: #F0FDF4; border: 1px solid #DCFCE7; padding: 2px 8px; border-radius: 4px; display: inline-block;">
                Status: Complete
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with s2:
    st.markdown(
        """
        <div class="step-card">
            <div>
                <div class="step-number" style="color: #64748B;">STEP 02</div>
                <div style="font-size: 1.0rem; font-weight: 700; color: #131B2E; margin-top: 6px; margin-bottom: 4px;">Explore career paths</div>
                <div style="font-size: 0.84rem; color: #444653; line-height: 1.45;">Inspect machine learning-ranked occupations matched to your skill matrix.</div>
            </div>
            <div style="margin-top: 12px; font-size: 0.76rem; font-weight: 600; color: #1E40AF; background-color: #EFF6FF; border: 1px solid #DBEAFE; padding: 2px 8px; border-radius: 4px; display: inline-block;">
                Ranked: Top 5 Roles
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with s3:
    st.markdown(
        """
        <div class="step-card">
            <div>
                <div class="step-number" style="color: #64748B;">STEP 03</div>
                <div style="font-size: 1.0rem; font-weight: 700; color: #131B2E; margin-top: 6px; margin-bottom: 4px;">Understand skill gaps</div>
                <div style="font-size: 0.84rem; color: #444653; line-height: 1.45;">Break down matched vs. missing competencies with ESCO taxonomy mapping.</div>
            </div>
            <div style="margin-top: 12px; font-size: 0.76rem; font-weight: 600; color: #475569; background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 2px 8px; border-radius: 4px; display: inline-block;">
                Detailed Breakdown
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with s4:
    st.markdown(
        """
        <div class="step-card">
            <div>
                <div class="step-number" style="color: #64748B;">STEP 04</div>
                <div style="font-size: 1.0rem; font-weight: 700; color: #131B2E; margin-top: 6px; margin-bottom: 4px;">Run What-If scenarios</div>
                <div style="font-size: 0.84rem; color: #444653; line-height: 1.45;">Simulate hypothetical skill level upgrades and observe shifts in role alignment.</div>
            </div>
            <div style="margin-top: 12px; font-size: 0.76rem; font-weight: 600; color: #475569; background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 2px 8px; border-radius: 4px; display: inline-block;">
                Interactive Sandbox
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Section: Profile Summary & Top Careers Split Layout
p_col1, p_col2 = st.columns([1, 1.8])

with p_col1:
    st.subheader("Your Profile Summary")
    
    skill_ratings = [
        (k, v) for k, v in prof.items() if isinstance(v, (int, float))
    ]
    top_skills = sorted(skill_ratings, key=lambda x: x[1], reverse=True)[:3]
    top_skills_formatted = ", ".join([f"{k} ({v:g}/10)" for k, v in top_skills])

    cert_text = prof.get("certifications", "")
    interest_text = prof.get("interested_subjects", "Software Development")

    st.markdown(
        f"""
        <div class="stitch-card">
            <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.04em;">Assessment Status</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #131B2E; margin-top: 4px;">Profile Ready</div>
            <div style="font-size: 0.84rem; color: #444653; margin-top: 2px;">8 technical skill areas assessed</div>
            <hr style="margin: 0.8rem 0 !important;">
            <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.04em;">Demonstrated Strengths</div>
            <div style="font-size: 0.96rem; font-weight: 600; color: #1E40AF; margin-top: 4px; line-height: 1.4;">{top_skills_formatted}</div>
            <hr style="margin: 0.8rem 0 !important;">
            <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.04em;">Stated Interests</div>
            <div style="font-size: 0.92rem; font-weight: 600; color: #131B2E; margin-top: 4px;">{interest_text or 'Not specified'}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p_col2:
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
                "Strong alignment"
                if rank == 1
                else ("Good alignment" if rank == 2 else "Moderate alignment")
            )

            match_summary = (
                f"{len(matched)} of {total_req} skills matched"
                if total_req > 0
                else f"{len(matched)} skills matched"
            )

            st.markdown(
                f"""
                <div class="stitch-card" style="padding: 1.0rem 1.25rem; margin-bottom: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #1E40AF;">#{rank}</span>
                            <span style="font-size: 1.08rem; font-weight: 700; color: #131B2E; margin-left: 6px;">{role}</span>
                            <span style="margin-left: 10px; font-size: 0.78rem; font-weight: 600; color: #1E40AF; background-color: #F2F3FF; border: 1px solid #DBE1FF; padding: 2px 8px; border-radius: 4px;">{alignment_tier}</span>
                        </div>
                        <div style="font-size: 0.86rem; font-weight: 600; color: #444653;">
                            {match_summary}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Complete your profile assessment to explore top career recommendations.")

# Footer
inject_footer()

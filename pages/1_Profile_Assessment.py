"""Page 1 — Profile Assessment.

Structured product form for entering technical skill evidence, academic performance,
certifications, and domain interests.
"""

import streamlit as st
from careerpath.ui.theme import inject_theme, inject_sidebar_brand, inject_footer

# Page Configuration
st.set_page_config(page_title="Profile Assessment — CareerPath", page_icon="📝", layout="wide")

# Inject Clean Design System & Sidebar Brand
inject_theme()
inject_sidebar_brand()

st.title("Profile Assessment")
st.markdown(
    "Tell us about your current technical experience, academic performance and interests."
)

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

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

prof = st.session_state["student_profile"]

with st.form("profile_assessment_form"):
    st.subheader("Technical Skills")
    st.caption(
        "Self-assessed evidence scale: **0** = no demonstrated evidence &nbsp;|&nbsp; "
        "**5** = competent project evidence &nbsp;|&nbsp; **10** = advanced evidence"
    )

    col1, col2 = st.columns(2)

    with col1:
        coding = st.slider("Coding Skills", 0.0, 10.0, float(prof.get("Coding Skills", 5.0)), 0.5)
        sw_eng = st.slider("Software Engineering", 0.0, 10.0, float(prof.get("Software Engineering", 5.0)), 0.5)
        db_fund = st.slider("Database Fundamentals", 0.0, 10.0, float(prof.get("Database Fundamentals", 5.0)), 0.5)
        web_dev = st.slider("Web Development", 0.0, 10.0, float(prof.get("Web Development", 5.0)), 0.5)

    with col2:
        networks = st.slider("Computer Networks", 0.0, 10.0, float(prof.get("Computer Networks", 5.0)), 0.5)
        cyber = st.slider("Cyber Security", 0.0, 10.0, float(prof.get("Cyber Security", 5.0)), 0.5)
        testing = st.slider("Software Testing", 0.0, 10.0, float(prof.get("Software Testing", 5.0)), 0.5)
        tech_supp = st.slider("Technical Support", 0.0, 10.0, float(prof.get("Technical Support", 5.0)), 0.5)

    st.markdown("---")
    st.subheader("Academic & Interest Information")

    c_col1, c_col2 = st.columns(2)
    with c_col1:
        certs = st.text_input(
            "Certifications",
            value=prof.get("certifications", ""),
            placeholder="e.g., Python Certified Associate, AWS Certified",
        )
    with c_col2:
        subjects = st.text_input(
            "Interested Subjects & Domains",
            value=prof.get("interested_subjects", ""),
            placeholder="e.g., Software Development, Cloud Systems",
        )

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Save Profile & View Careers", type="primary", use_container_width=True)

if submitted:
    updated_profile = {
        "Database Fundamentals": db_fund,
        "Computer Networks": networks,
        "Software Engineering": sw_eng,
        "Cyber Security": cyber,
        "Coding Skills": coding,
        "Web Development": web_dev,
        "Software Testing": testing,
        "Technical Support": tech_supp,
        "certifications": certs,
        "interested_subjects": subjects,
    }
    st.session_state["student_profile"] = updated_profile
    st.success("Profile saved successfully.")
    st.switch_page("pages/2_Career_Explorer.py")

# Section: Profile Review (Human-Readable Summary)
st.markdown("---")
st.subheader("Profile Review")

cur_p = st.session_state["student_profile"]

rev_col1, rev_col2 = st.columns(2)

with rev_col1:
    st.markdown("##### Technical Skill Evidence")
    skill_items = [
        ("Coding Skills", cur_p.get("Coding Skills", 0.0)),
        ("Software Engineering", cur_p.get("Software Engineering", 0.0)),
        ("Database Fundamentals", cur_p.get("Database Fundamentals", 0.0)),
        ("Web Development", cur_p.get("Web Development", 0.0)),
        ("Computer Networks", cur_p.get("Computer Networks", 0.0)),
        ("Cyber Security", cur_p.get("Cyber Security", 0.0)),
        ("Software Testing", cur_p.get("Software Testing", 0.0)),
        ("Technical Support", cur_p.get("Technical Support", 0.0)),
    ]
    for name, val in skill_items:
        st.markdown(f"• **{name}:** `{val:g} / 10`")

with rev_col2:
    st.markdown("##### Background & Interests")
    st.markdown(f"• **Certifications:** {cur_p.get('certifications') or 'None specified'}")
    st.markdown(f"• **Interested Domains:** {cur_p.get('interested_subjects') or 'None specified'}")

# Single Consolidated Footer
inject_footer()

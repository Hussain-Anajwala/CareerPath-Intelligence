"""Page 1 — Profile Assessment.

Structured form to input student academic performance, technical skill evidence (0-10 scale),
interests, and certifications.
"""

import streamlit as st
from careerpath.ui.client import ServiceClient
from careerpath.ui.theme import inject_theme

st.set_page_config(page_title="Profile Assessment — CareerPath", page_icon="📝", layout="wide")

inject_theme()

st.title("Profile Assessment")
st.markdown(
    "Provide evidence of technical skills, academic performance, and domain interests. "
    "All ratings follow a standard 0–10 evidence scale."
)

if "student_profile" not in st.session_state:
    st.session_state["student_profile"] = {
        "Database Fundamentals": 5.0,
        "Computer Networks": 5.0,
        "Software Engineering": 5.0,
        "Cyber Security": 5.0,
        "Coding Skills": 5.0,
        "Web Development": 5.0,
        "Software Testing": 5.0,
        "Technical Support": 5.0,
        "certifications": "",
        "interested_subjects": "",
    }

prof = st.session_state["student_profile"]

with st.form("profile_form"):
    st.subheader("Technical Skill Evidence (0–10 Scale)")
    st.caption(
        "Scale Guidance: **0** = No demonstrated evidence | **5** = Competent project evidence | **10** = Advanced mastery"
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
    st.subheader("Certifications & Domain Interests")
    c_col1, c_col2 = st.columns(2)

    with c_col1:
        certs = st.text_input(
            "Certifications (comma-separated)",
            value=prof.get("certifications", ""),
            help="Example: AWS Certified Cloud Practitioner, Python Institute PCEP",
        )
    with c_col2:
        subjects = st.text_input(
            "Interested Subjects / Domains",
            value=prof.get("interested_subjects", ""),
            help="Example: Cloud Computing, Machine Learning, Network Security",
        )

    submitted = st.form_submit_button("Save Profile & Update Recommendations", use_container_width=True)

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
    st.success("Student profile successfully updated!")

st.markdown("---")
st.subheader("Active Profile Summary")
st.json(st.session_state["student_profile"])

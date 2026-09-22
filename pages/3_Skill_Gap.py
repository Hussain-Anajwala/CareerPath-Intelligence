"""Page 3 — Target Skill Gap Inspector.

Analyzes required ESCO skills for any target career path and categorizes student profile
evidence into Matched, Partial, and Missing skills with visual indicators.
"""

import os
import streamlit as st
import pandas as pd
from careerpath.ui.client import ServiceClient
from careerpath.ui.theme import inject_theme

st.set_page_config(page_title="Skill Gap Inspector — CareerPath", page_icon="🎯", layout="wide")

inject_theme()

st.title("Skill Gap Inspector")
st.markdown(
    "Pinpoint exact skill proficiencies and evidence gaps for any target career role. "
    "Required skills are extracted from the ESCO v1.2 occupation taxonomy standard."
)

api_url = os.getenv("CAREERPATH_API_URL", "http://127.0.0.1:8000")
client = ServiceClient(api_url=api_url)

if "student_profile" not in st.session_state:
    st.warning("No student profile found. Please complete Profile Assessment first.")
    if st.button("Go to Profile Assessment ➔"):
        st.switch_page("pages/1_Profile_Assessment.py")
    st.stop()

profile = st.session_state["student_profile"]

# Career Selection Dropdown
supported_careers = [
    "Database Administrator",
    "Network Security Engineer",
    "Software Developer",
    "Cyber Security Specialist",
    "Web Developer",
    "Software Quality Assurance Engineer",
    "Technical Support Engineer",
    "Systems Analyst",
    "Data API Engineer",
]

default_target = st.session_state.get("target_career", "Software Developer")
if default_target not in supported_careers:
    supported_careers.insert(0, default_target)

target_career = st.selectbox("Select Target Career Role", supported_careers, index=supported_careers.index(default_target))

st.markdown("---")

with st.spinner(f"Evaluating ESCO skill gap analysis for '{target_career}'..."):
    try:
        gap_res = client.get_skill_gap(profile, target_career)
    except Exception as e:
        st.error(f"Error conducting skill gap analysis: {e}")
        st.stop()

st.subheader(f"Skill Alignment Analysis: {target_career}")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Required ESCO Skills", gap_res["total_required_skills"])
with c2:
    st.metric("Skill Coverage Score", f"{gap_res['coverage_score']:.3f}", f"{gap_res['coverage_score']*100:.1f}%")
with c3:
    st.metric("Average Skill Similarity", f"{gap_res['average_similarity']:.3f}")

st.markdown("---")

matched = gap_res["matched_skills"]
partial = gap_res["partial_matches"]
missing = gap_res["missing_skills"]

# Visual Coverage Progress Bar
col_chart, col_details = st.columns([1, 1])

with col_chart:
    st.markdown("#### Skill Gap Composition")
    status_df = pd.DataFrame(
        [
            {"Status": "Matched Skills", "Count": len(matched)},
            {"Status": "Partial Matches", "Count": len(partial)},
            {"Status": "Missing Evidence", "Count": len(missing)},
        ]
    )
    st.bar_chart(status_df.set_index("Status"))

with col_details:
    st.markdown("#### Summary Status")
    st.markdown(f"• **{len(matched)}** Matched Skills (High evidence in profile)")
    st.markdown(f"• **{len(partial)}** Partial Matches (Moderate evidence in profile)")
    st.markdown(f"• **{len(missing)}** Missing Evidence (No matching evidence in profile)")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Matched Skills", "Partial Matches", "Missing Evidence"])

with tab1:
    if matched:
        for m in matched:
            st.markdown(f"• **{m['skill']}** (Semantic Similarity: `{m['similarity']:.2f}`) — Matched via *{m['evidence']}*")
    else:
        st.info("No strong matched skills found for this profile.")

with tab2:
    if partial:
        for p in partial:
            st.markdown(f"• **{p['skill']}** (Semantic Similarity: `{p['similarity']:.2f}`) — Partial evidence in *{p['evidence']}*")
    else:
        st.info("No partial skill matches.")

with tab3:
    if missing:
        for ms in missing:
            st.markdown(f"• **{ms['skill']}** — No matching evidence found in supplied profile attributes.")
    else:
        st.success("Complete skill coverage! No missing skill gaps detected.")

st.markdown("---")
st.caption(
    "Note: Wording 'Missing Evidence' means no matching skill rating or certification text was present in the profile. "
    "It does not imply personal deficit."
)

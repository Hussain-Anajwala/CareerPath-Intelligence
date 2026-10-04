"""Page 2 — Career Explorer.

Split-screen layout presenting ranked career pathway options on the left and selected
career details, ESCO skill alignment badges, development actions, and progressive disclosure
technical details on the right.
"""

import streamlit as st
from careerpath.ui.client import ServiceClient
from careerpath.ui.theme import inject_theme, inject_sidebar_brand, inject_footer

# Page Configuration
st.set_page_config(page_title="Career Explorer — CareerPath", page_icon="🔍", layout="wide")

# Inject Design System & Sidebar Brand
inject_theme()
inject_sidebar_brand()

client = ServiceClient()

st.title("Career Explorer")
st.markdown("Explore ranked career path options and ESCO skill alignments for your current profile.")

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

# Guard against missing profile
if "student_profile" not in st.session_state:
    st.warning("Your career profile is not ready yet. Please complete your profile assessment first.")
    if st.button("Complete Profile Assessment", type="primary"):
        st.switch_page("pages/1_Profile_Assessment.py")
    st.stop()

profile = st.session_state["student_profile"]

# Sidebar Settings
with st.sidebar:
    st.markdown("---")
    st.markdown("### Exploration Settings")
    top_k_select = st.slider("Recommendations to display", 3, 10, 5)
    
    if "exploratory_alpha" not in st.session_state:
        st.session_state["exploratory_alpha"] = 1.0

alpha = st.session_state.get("exploratory_alpha", 1.0)

try:
    recs = client.get_recommendations(profile, top_k=top_k_select, alpha=alpha)
except Exception:
    st.error("Unable to load recommendations. Please verify backend service availability.")
    recs = []

if not recs:
    st.info("No recommendations generated. Complete your profile to explore career paths.")
    st.stop()

# -----------------------------------------------------------------------------
# Split-Screen Layout: Left = Ranked Pathways, Right = Selected Career Detail
# -----------------------------------------------------------------------------
rec_roles = [r["career_role"] for r in recs]

# Check target career selection
default_selected_index = 0
if "target_career" in st.session_state and st.session_state["target_career"] in rec_roles:
    default_selected_index = rec_roles.index(st.session_state["target_career"])

left_col, right_col = st.columns([1, 1.6])

with left_col:
    st.subheader("Ranked Career Pathways")
    
    selected_role = st.radio(
        "Select a career path to inspect detail:",
        options=rec_roles,
        index=default_selected_index,
        label_visibility="collapsed",
    )
    
    selected_rec = next((r for r in recs if r["career_role"] == selected_role), recs[0])

    for idx, r in enumerate(recs):
        role_name = r["career_role"]
        matched_count = len(r.get("matched_skills", []))
        total_req = matched_count + len(r.get("partial_matches", [])) + len(r.get("missing_skills", []))
        is_active = (role_name == selected_rec["career_role"])
        
        border_color = "#1E40AF" if is_active else "#E2E8F0"
        bg_color = "#F2F3FF" if is_active else "#FFFFFF"
        active_indicator = "🔹 " if is_active else ""
        
        st.markdown(
            f"""
            <div style="background-color: {bg_color}; border: 1.5px solid {border_color}; border-radius: 10px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #1E40AF;">#{idx + 1} RANKED</span>
                    <span style="font-size: 0.8rem; font-weight: 600; color: #475569;">{matched_count}/{total_req} skills matched</span>
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #131B2E; margin-top: 4px;">{active_indicator}{role_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with right_col:
    role_title = selected_rec["career_role"]
    esco_title = selected_rec["esco_occupation_title"]
    matched = selected_rec.get("matched_skills", [])
    partial = selected_rec.get("partial_matches", [])
    missing = selected_rec.get("missing_skills", [])
    total_skills = len(matched) + len(partial) + len(missing)

    st.subheader(f"Career Alignment: {role_title}")
    st.markdown(f"Mapped ESCO Occupation Standard: **{esco_title}**")

    # 1. Why This Career Matches
    st.markdown("#### Why This Career Matches")
    if matched:
        top_matched_names = ", ".join([m["skill"] for m in matched[:3]])
        st.markdown(
            f"Your profile demonstrates strong proficiency in **{top_matched_names}**, "
            f"which forms the essential evidence foundation for a {role_title}."
        )
    else:
        st.markdown(f"Your profile has foundational technical overlap with the core requirements for {role_title}.")

    st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)

    # 2. Skill Alignment & Coverage
    st.markdown("#### Skill Alignment & Coverage")
    if total_skills > 0:
        st.markdown(f"**{len(matched)} of {total_skills} required skills matched**")
    
    b_col1, b_col2, b_col3 = st.columns(3)

    with b_col1:
        st.markdown("##### Matched Skills")
        if matched:
            for m in matched:
                st.markdown(
                    f"""<div class="skill-tag skill-matched">✓ {m['skill']}</div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No full skill matches.")

    with b_col2:
        st.markdown("##### Partial Matches")
        if partial:
            for p in partial:
                st.markdown(
                    f"""<div class="skill-tag skill-partial">~ {p['skill']}</div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No partial matches.")

    with b_col3:
        st.markdown("##### Missing Skills")
        if missing:
            for ms in missing:
                st.markdown(
                    f"""<div class="skill-tag skill-missing">+ {ms['skill']}</div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.caption("Complete skill coverage!")

    st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)

    # 3. Next Areas to Develop
    st.markdown("#### Next Areas to Develop")
    if missing:
        gaps_list = ", ".join([ms["skill"] for ms in missing[:3]])
        st.markdown(f"To strengthen your alignment for **{role_title}**, focus next on developing: **{gaps_list}**.")
    elif partial:
        part_list = ", ".join([p["skill"] for p in partial[:3]])
        st.markdown(f"To solidify your alignment for **{role_title}**, deepen your practical evidence in: **{part_list}**.")
    else:
        st.success("Complete coverage! Your profile addresses all required skills for this career path.")

    # Action to What-If Lab
    st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)
    if st.button(f"Simulate Improving Skills in What-If Lab ➔"):
        st.session_state["target_career"] = role_title
        st.switch_page("pages/3_What_If.py")

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 3: Technical Progressive Disclosure Expander
# -----------------------------------------------------------------------------
with st.expander("How this recommendation is calculated", expanded=False):
    st.markdown("#### Technical Model & Taxonomy Details")
    st.caption(
        "Internal evidence breakdown combining supervised ML classification ranking with "
        "ESCO v1.2 taxonomy vector similarity."
    )

    d_col1, d_col2, d_col3, d_col4 = st.columns(4)
    with d_col1:
        st.metric("Composite Score", f"{selected_rec['final_score']:.3f}")
    with d_col2:
        st.metric("ML Model Score", f"{selected_rec['normalized_ml_score']:.3f}")
    with d_col3:
        st.metric("ESCO Skill Score", f"{selected_rec['esco_score']:.3f}")
    with d_col4:
        st.metric("Raw ML Probability", f"{selected_rec['raw_ml_probability']:.4f}", help="Internal model output. This is not a probability of employment.")

    st.markdown(f"• **ESCO Occupation URI:** `{selected_rec['esco_occupation_uri']}`")

    st.markdown("---")
    st.markdown("##### Exploratory Fusion Control")
    new_alpha = st.slider(
        "Exploratory fusion weight (α)",
        min_value=0.0,
        max_value=1.0,
        value=float(st.session_state.get("exploratory_alpha", 1.0)),
        step=0.1,
        help="Production recommendations use the validated ML ranking configuration (α = 1.0). This control is provided for exploratory comparison.",
    )
    if new_alpha != st.session_state.get("exploratory_alpha", 1.0):
        st.session_state["exploratory_alpha"] = new_alpha
        st.rerun()

# Single Consolidated Footer
inject_footer()

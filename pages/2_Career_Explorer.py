"""Page 2 — Career Explorer.

The primary product interface for exploring ranked career path recommendations,
understanding career alignment rationale, inspecting integrated skill coverage/gaps,
and discovering recommended skill development areas.
"""

import streamlit as st
from careerpath.ui.client import ServiceClient
from careerpath.ui.theme import inject_theme, inject_sidebar_brand, inject_footer

# Page Configuration
st.set_page_config(page_title="Career Explorer — CareerPath", page_icon="🔍", layout="wide")

# Inject Clean Design System & Sidebar Brand
inject_theme()
inject_sidebar_brand()

client = ServiceClient()

st.title("Career Explorer")
st.markdown("Career paths for your current profile.")

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

# Guard against missing profile
if "student_profile" not in st.session_state:
    st.warning("Your career profile is not ready yet. Please complete your profile assessment first.")
    if st.button("Complete Profile Assessment", type="primary"):
        st.switch_page("pages/1_Profile_Assessment.py")
    st.stop()

profile = st.session_state["student_profile"]

# Advanced/Exploratory Settings (Progressive Disclosure)
with st.sidebar:
    st.markdown("---")
    st.markdown("### Exploration Settings")
    top_k_select = st.slider("Recommendations to display", 3, 10, 5)
    
    # Store alpha in session state (default 1.0)
    if "exploratory_alpha" not in st.session_state:
        st.session_state["exploratory_alpha"] = 1.0

alpha = st.session_state.get("exploratory_alpha", 1.0)

try:
    recs = client.get_recommendations(profile, top_k=top_k_select, alpha=alpha)
except Exception as e:
    st.error("Unable to load recommendations. Please verify backend service availability.")
    recs = []

if not recs:
    st.info("No recommendations generated. Complete your profile to explore career paths.")
    st.stop()

# -----------------------------------------------------------------------------
# Section 1: Ranked Recommendation List
# -----------------------------------------------------------------------------
st.subheader("Top Recommended Career Paths")

# Create list of roles for user selection
rec_roles = [r["career_role"] for r in recs]

# Check if target_career pre-selected from session state or default to rank 1
default_selected_index = 0
if "target_career" in st.session_state and st.session_state["target_career"] in rec_roles:
    default_selected_index = rec_roles.index(st.session_state["target_career"])

selected_role = st.radio(
    "Select a career path to explore detail & skill alignment:",
    options=rec_roles,
    index=default_selected_index,
    horizontal=True,
    label_visibility="collapsed",
)

# Find selected recommendation record
selected_rec = next((r for r in recs if r["career_role"] == selected_role), recs[0])

# Summary Cards for Recommendations List
card_cols = st.columns(min(len(recs), 5))
for idx, r in enumerate(recs[:5]):
    role_name = r["career_role"]
    matched_count = len(r.get("matched_skills", []))
    total_req = matched_count + len(r.get("partial_matches", [])) + len(r.get("missing_skills", []))
    
    is_active = (role_name == selected_rec["career_role"])
    card_border = "#2563EB" if is_active else "#E2E8F0"
    card_bg = "#EFF6FF" if is_active else "#FFFFFF"
    
    with card_cols[idx]:
        st.markdown(
            f"""
            <div style="background-color: {card_bg}; border: 1.5px solid {card_border}; border-radius: 8px; padding: 0.9rem; height: 100%;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #2563EB;">#{idx + 1} RANKED</div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{role_name}</div>
                <div style="font-size: 0.82rem; color: #475569; margin-top: 4px;">{matched_count}/{total_req} skills matched</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 2: Selected Career Detailed Breakdown
# -----------------------------------------------------------------------------
role_title = selected_rec["career_role"]
esco_title = selected_rec["esco_occupation_title"]
matched = selected_rec.get("matched_skills", [])
partial = selected_rec.get("partial_matches", [])
missing = selected_rec.get("missing_skills", [])
total_skills = len(matched) + len(partial) + len(missing)

st.subheader(f"Career Alignment: {role_title}")
st.markdown(f"Your profile demonstrates strong alignment with the standard **{esco_title}** career path.")

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

# 2.1 Why This Career
st.markdown("#### Why This Career Matches")
if matched:
    top_matched_names = ", ".join([m["skill"] for m in matched[:3]])
    st.markdown(
        f"Your profile demonstrates strong proficiency in **{top_matched_names}**, "
        f"which forms the essential foundation for a {role_title}."
    )
else:
    st.markdown(f"Your profile has foundational technical overlap with the core requirements for {role_title}.")

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

# 2.2 Skill Alignment (Integrated Skill Gap)
st.markdown("#### Skill Alignment & Coverage")

if total_skills > 0:
    st.markdown(f"**{len(matched)} of {total_skills} required skills matched**")
else:
    st.markdown("Skill alignment evaluated against ESCO taxonomy standards.")

align_col1, align_col2, align_col3 = st.columns(3)

with align_col1:
    st.markdown("##### Matched Skills")
    if matched:
        for m in matched:
            st.markdown(
                f"""<div class="skill-tag skill-matched">✓ {m['skill']}</div>""",
                unsafe_allow_html=True,
            )
    else:
        st.caption("No full skill matches identified yet.")

with align_col2:
    st.markdown("##### Partial Matches")
    if partial:
        for p in partial:
            st.markdown(
                f"""<div class="skill-tag skill-partial">~ {p['skill']}</div>""",
                unsafe_allow_html=True,
            )
    else:
        st.caption("No partial matches.")

with align_col3:
    st.markdown("##### Missing Skills")
    if missing:
        for ms in missing:
            st.markdown(
                f"""<div class="skill-tag skill-missing">+ {ms['skill']}</div>""",
                unsafe_allow_html=True,
            )
    else:
        st.caption("Complete skill coverage!")

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

# 2.3 Next Areas to Develop
st.markdown("#### Next Areas to Develop")
if missing:
    gaps_list = ", ".join([ms["skill"] for ms in missing[:3]])
    st.markdown(f"To strengthen your alignment for **{role_title}**, focus next on developing: **{gaps_list}**.")
elif partial:
    part_list = ", ".join([p["skill"] for p in partial[:3]])
    st.markdown(f"To solidify your alignment for **{role_title}**, deepen your practical evidence in: **{part_list}**.")
else:
    st.success("Complete coverage! Your profile addresses all required skills for this career path.")

# Quick action to What-If simulation
st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)
if st.button(f"Simulate Improving Skills for {role_title} in What-If Lab ➔"):
    st.session_state["target_career"] = role_title
    st.switch_page("pages/3_What_If.py")

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 3: Progressive Disclosure — Recommendation Details
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
        st.metric("Raw ML Probability", f"{selected_rec['raw_ml_probability']:.4f}")

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

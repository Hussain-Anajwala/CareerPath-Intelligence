"""Page 2 — Career Explorer.

Displays top career recommendations, decomposable score breakdowns, ESCO occupation mappings,
skill coverage ratios, matched skills, partial matches, and missing skill evidence.
"""

import os
import streamlit as st
from careerpath.ui.client import ServiceClient
from careerpath.ui.theme import inject_theme

st.set_page_config(page_title="Career Explorer — CareerPath", page_icon="🔍", layout="wide")

inject_theme()

st.title("Career Explorer")
st.markdown(
    "Explore ranked career path recommendations tailored to your profile evidence. "
    "Every recommendation decomposes into machine learning model signals and ESCO taxonomy skill alignment."
)

api_url = os.getenv("CAREERPATH_API_URL", "http://127.0.0.1:8000")
client = ServiceClient(api_url=api_url)

if "student_profile" not in st.session_state:
    st.warning("No student profile found. Please complete Profile Assessment first.")
    if st.button("Go to Profile Assessment ➔"):
        st.switch_page("pages/1_Profile_Assessment.py")
    st.stop()

profile = st.session_state["student_profile"]

# Controls
col_ctrl1, col_ctrl2 = st.columns([1, 2])
with col_ctrl1:
    top_k = st.slider("Top Recommendations (K)", min_value=1, max_value=10, value=5)
with col_ctrl2:
    alpha = st.slider(
        "Exploratory Fusion Weight α",
        min_value=0.0,
        max_value=1.0,
        value=1.0,
        step=0.1,
        help="Production configuration: α = 1.0 (Supervised ML ranking + ESCO explainability evidence). Adjust α to explore alternative hybrid scoring combinations (α = 0.0 is ESCO-only skill alignment).",
    )

st.markdown("---")

with st.spinner("Calculating career recommendations..."):
    recs = client.get_recommendations(profile, top_k=top_k, alpha=alpha)

if not recs:
    st.error("Failed to generate career recommendations. Please verify system dependencies.")
    st.stop()

st.subheader(f"Top {len(recs)} Recommended Career Paths")

for idx, rec in enumerate(recs):
    rank = idx + 1
    role_title = rec["career_role"]
    esco_title = rec["esco_occupation_title"]
    final_score = rec["final_score"]
    ml_score = rec["normalized_ml_score"]
    esco_score = rec["esco_score"]
    raw_ml = rec["raw_ml_probability"]

    matched = rec["matched_skills"]
    partial = rec["partial_matches"]
    missing = rec["missing_skills"]
    total_req = len(matched) + len(partial) + len(missing)

    with st.expander(f"#{rank} — {role_title} (Score: {final_score:.3f})", expanded=(rank == 1)):
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Composite Score", f"{final_score:.3f}")
        with m_col2:
            st.metric("ML Model Score", f"{ml_score:.3f}", help=f"Raw CatBoost probability: {raw_ml:.4f}")
        with m_col3:
            st.metric("ESCO Skill Score", f"{esco_score:.3f}")
        with m_col4:
            coverage_pct = (len(matched) / total_req * 100) if total_req > 0 else 0
            st.metric("Skill Coverage", f"{len(matched)} / {total_req}", f"{coverage_pct:.0f}%")

        st.caption(f"ESCO Occupation Mapping: **{esco_title}** (`{rec['esco_occupation_uri']}`)")

        st.markdown("#### Decomposable Evidence Breakdown")
        ev_col1, ev_col2 = st.columns(2)

        with ev_col1:
            st.markdown("##### Matched Skill Evidence")
            if matched:
                for m in matched:
                    st.markdown(f"• **{m['skill']}** (Similarity: `{m['similarity']:.2f}`) — *{m['evidence']}*")
            else:
                st.caption("No strong skill matches found.")

            if partial:
                st.markdown("##### Partial Skill Evidence")
                for p in partial:
                    st.markdown(f"• **{p['skill']}** (Similarity: `{p['similarity']:.2f}`) — *{p['evidence']}*")

        with ev_col2:
            st.markdown("##### Missing Skill Evidence")
            if missing:
                for ms in missing:
                    st.markdown(f"• **{ms['skill']}** (Similarity: `{ms['similarity']:.2f}`)")
            else:
                st.caption("No missing skill gaps detected!")

        st.markdown("---")
        if st.button(f"Inspect Skill Gap for {role_title} ➔", key=f"btn_gap_{idx}"):
            st.session_state["target_career"] = role_title
            st.switch_page("pages/3_Skill_Gap.py")

st.markdown("---")
st.info(
    "**Score Interpretation**: Scores reflect relative model alignment and ESCO skill similarity on a [0, 1] scale. "
    "They represent decision-support evidence rather than deterministic probabilities of employment."
)

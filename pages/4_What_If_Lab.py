"""Page 4 — Interactive What-If Simulation Lab.

Flagship UI feature allowing users to simulate hypothetical skill acquisition, observe
before-vs-after career ranking deltas, score shifts, and reduced skill gaps.
"""

import os
import streamlit as st
import pandas as pd
from careerpath.ui.client import ServiceClient

st.set_page_config(page_title="What-If Lab — CareerPath", page_icon="🧪", layout="wide")

st.title("🧪 Interactive What-If Simulation Lab")
st.markdown(
    "Simulate counterfactual skill acquisition scenarios to observe how improving specific technical skills "
    "affects your model career recommendations, rank shifts, and resolved skill gaps."
)

api_url = os.getenv("CAREERPATH_API_URL", "http://127.0.0.1:8000")
client = ServiceClient(api_url=api_url)

if "student_profile" not in st.session_state:
    st.warning("⚠️ No student profile found. Please complete Profile Assessment first.")
    if st.button("Go to Profile Assessment ➔"):
        st.switch_page("pages/1_Profile_Assessment.py")
    st.stop()

baseline_profile = st.session_state["student_profile"]

st.subheader("⚙️ Scenario Builder: Select Skills to Improve")
st.caption("Adjust the sliders below to simulate acquiring or boosting specific skill evidence levels.")

skills_to_modify = {}
col1, col2 = st.columns(2)

skill_keys = [
    "Database Fundamentals",
    "Computer Networks",
    "Software Engineering",
    "Cyber Security",
    "Coding Skills",
    "Web Development",
    "Software Testing",
    "Technical Support",
]

with col1:
    for s in skill_keys[:4]:
        curr_val = float(baseline_profile.get(s, 5.0))
        new_val = st.slider(f"Simulate '{s}'", 0.0, 10.0, curr_val, 0.5, key=f"sim_{s}")
        if new_val != curr_val:
            skills_to_modify[s] = new_val

with col2:
    for s in skill_keys[4:]:
        curr_val = float(baseline_profile.get(s, 5.0))
        new_val = st.slider(f"Simulate '{s}'", 0.0, 10.0, curr_val, 0.5, key=f"sim_{s}")
        if new_val != curr_val:
            skills_to_modify[s] = new_val

st.markdown("---")

run_sim = st.button("🚀 Run Counterfactual What-If Simulation", use_container_width=True)

if run_sim or "last_sim_res" in st.session_state:
    if run_sim:
        if not skills_to_modify:
            st.info("ℹ️ No skill sliders were adjusted. Modifying 'Cyber Security' to 9.0 as a default example scenario.")
            skills_to_modify["Cyber Security"] = 9.0

        with st.spinner("Running What-If simulation engine across model & ESCO pipeline..."):
            sim_res = client.simulate_what_if(baseline_profile, skills_to_modify, top_k=5)
            st.session_state["last_sim_res"] = sim_res
    else:
        sim_res = st.session_state["last_sim_res"]

    st.subheader("📊 Simulation Results: Before vs After")

    # High level metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Baseline #1 Recommendation", sim_res["baseline_top_recommendation"])
    with m2:
        st.metric(
            "Scenario #1 Recommendation",
            sim_res["scenario_top_recommendation"],
            delta="Changed" if sim_res["baseline_top_recommendation"] != sim_res["scenario_top_recommendation"] else "Unchanged",
        )
    with m3:
        st.metric("Simulated Skills Modified", len(sim_res["skills_modified"]))

    st.markdown("#### 🔄 Career Ranking Shift Table")

    rank_changes = sim_res["rank_changes"]
    table_rows = []
    for rc in rank_changes:
        base_r = f"#{rc['baseline_rank']}" if rc['baseline_rank'] is not None else "N/A"
        scen_r = f"#{rc['scenario_rank']}" if rc['scenario_rank'] is not None else "N/A"
        r_delta = rc['rank_delta']
        if r_delta > 0:
            delta_str = f"⬆️ +{r_delta}"
        elif r_delta < 0:
            delta_str = f"⬇️ {r_delta}"
        else:
            delta_str = "➡️ 0"

        table_rows.append(
            {
                "Career Path": rc["career_role"],
                "Baseline Rank": base_r,
                "Scenario Rank": scen_r,
                "Rank Shift": delta_str,
                "Baseline Score": f"{rc['baseline_score']:.3f}",
                "Scenario Score": f"{rc['scenario_score']:.3f}",
                "Score Delta": f"{rc['score_delta']:+.3f}",
            }
        )

    df_ranks = pd.DataFrame(table_rows)
    st.dataframe(df_ranks, use_container_width=True)

    st.markdown("---")
    st.markdown("#### ✨ Resolved Skill Gaps & Improved Alignments")
    reduced_gaps = sim_res.get("reduced_skill_gaps", [])
    if reduced_gaps:
        for rg in reduced_gaps:
            st.success(
                f"🎉 **{rg['career_role']}**: Increasing **{rg['skill']}** resolved skill gap for "
                f"*{rg['esco_skill_label']}* (Similarity: `{rg['new_similarity']:.2f}`)"
            )
    else:
        st.info("No new ESCO skill gaps were newly resolved in this scenario, but model scores were updated.")

st.markdown("---")
st.info(
    "💡 **What-If Language & Scientific Disclaimer**: 'Simulated impact' demonstrates how changing profile inputs affects model ranking outputs. "
    "It demonstrates pipeline counterfactual logic and does NOT guarantee causal real-world outcome or employment."
)

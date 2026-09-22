"""Page 3 — What-If Simulation.

Interactive counterfactual scenario builder allowing users to simulate skill improvements,
observe career recommendation rank shifts, and inspect resolved skill gaps.
"""

import streamlit as st
from careerpath.ui.client import ServiceClient
from careerpath.ui.theme import inject_theme, inject_sidebar_brand, inject_footer

# Page Configuration
st.set_page_config(page_title="What-If Simulation — CareerPath", page_icon="🧪", layout="wide")

# Inject Clean Design System & Sidebar Brand
inject_theme()
inject_sidebar_brand()

client = ServiceClient()

st.title("What-If")
st.markdown(
    "See how improving specific skills could change your current career recommendations."
)

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

# Guard against missing profile
if "student_profile" not in st.session_state:
    st.warning("Your career profile is not ready yet. Please complete your profile assessment first.")
    if st.button("Complete Profile Assessment", type="primary"):
        st.switch_page("pages/1_Profile_Assessment.py")
    st.stop()

baseline_profile = st.session_state["student_profile"]

# Scenario Builder Form
st.subheader("Scenario Builder")
st.caption("Adjust skill ratings below to simulate acquiring or strengthening specific technical evidence.")

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

skills_to_modify = {}
col1, col2 = st.columns(2)

with col1:
    for s in skill_keys[:4]:
        curr_val = float(baseline_profile.get(s, 5.0))
        new_val = st.slider(
            f"{s} (Current: {curr_val:g})",
            0.0,
            10.0,
            curr_val,
            0.5,
            key=f"sim_{s}",
        )
        if new_val != curr_val:
            skills_to_modify[s] = new_val

with col2:
    for s in skill_keys[4:]:
        curr_val = float(baseline_profile.get(s, 5.0))
        new_val = st.slider(
            f"{s} (Current: {curr_val:g})",
            0.0,
            10.0,
            curr_val,
            0.5,
            key=f"sim_{s}",
        )
        if new_val != curr_val:
            skills_to_modify[s] = new_val

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

run_sim = st.button("Run Simulation", type="primary", use_container_width=True)

if run_sim or "last_sim_res" in st.session_state:
    if run_sim:
        if not skills_to_modify:
            st.info("No skill sliders were modified. Simulating an increase in 'Cyber Security' to 9.0 as a sample scenario.")
            skills_to_modify["Cyber Security"] = 9.0

        with st.spinner("Calculating simulated career recommendations..."):
            sim_res = client.simulate_what_if(baseline_profile, skills_to_modify, top_k=5)
            st.session_state["last_sim_res"] = sim_res
    else:
        sim_res = st.session_state["last_sim_res"]

    st.markdown("---")
    st.subheader("Simulation Results")

    # High Level Summary Cards
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f"""
            <div class="product-card" style="margin-bottom: 0;">
                <div style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; color: #64748B;">Current Top Path</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin-top: 4px;">{sim_res['baseline_top_recommendation']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        is_changed = (sim_res["baseline_top_recommendation"] != sim_res["scenario_top_recommendation"])
        badge_text = "Rank Shifted" if is_changed else "Same Top Path"
        st.markdown(
            f"""
            <div class="product-card" style="margin-bottom: 0;">
                <div style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; color: #64748B;">Simulated Top Path ({badge_text})</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #1E40AF; margin-top: 4px;">{sim_res['scenario_top_recommendation']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="product-card" style="margin-bottom: 0;">
                <div style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; color: #64748B;">Skills Simulated</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin-top: 4px;">{len(sim_res['skills_modified'])} area(s) updated</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    st.markdown("#### Career Ranking Shifts")

    rank_changes = sim_res["rank_changes"]
    
    # Styled Product Data Table HTML
    table_html = """
    <div class="product-table-container">
    <table class="product-table">
        <thead>
            <tr>
                <th>Career Path</th>
                <th>Previous Rank</th>
                <th>New Rank</th>
                <th>Rank Shift</th>
                <th>Previous Score</th>
                <th>New Score</th>
                <th>Score Delta</th>
            </tr>
        </thead>
        <tbody>
    """
    for rc in rank_changes:
        base_r = f"#{rc['baseline_rank']}" if rc['baseline_rank'] is not None else "—"
        scen_r = f"#{rc['scenario_rank']}" if rc['scenario_rank'] is not None else "—"
        r_delta = rc['rank_delta']

        if r_delta > 0:
            shift_badge = f'<span class="shift-badge-up">▲ +{r_delta}</span>'
        elif r_delta < 0:
            shift_badge = f'<span class="shift-badge-down">▼ {r_delta}</span>'
        else:
            shift_badge = '<span class="shift-badge-same">=</span>'

        table_html += f"""
        <tr>
            <td><strong>{rc['career_role']}</strong></td>
            <td>{base_r}</td>
            <td>{scen_r}</td>
            <td>{shift_badge}</td>
            <td>{rc['baseline_score']:.3f}</td>
            <td>{rc['scenario_score']:.3f}</td>
            <td><code>{rc['score_delta']:+.3f}</code></td>
        </tr>
        """
    table_html += """
        </tbody>
    </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)

    # Skills Addressed
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("#### Skills Addressed & Resolved Gaps")
    reduced_gaps = sim_res.get("reduced_skill_gaps", [])
    if reduced_gaps:
        for rg in reduced_gaps:
            st.markdown(
                f"• **{rg['career_role']}:** Increasing **{rg['skill']}** resolved skill gap for "
                f"*{rg['esco_skill_label']}* (Similarity: `{rg['new_similarity']:.2f}`)"
            )
    else:
        st.markdown("Model scores were updated for all career paths based on the simulated profile input.")

# Single Consolidated Footer
inject_footer()

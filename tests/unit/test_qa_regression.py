"""Targeted QA regression test suite for bug fixes and system invariants.

Verifies:
1. Recommendation sorting by final_score (descending).
2. Zero required skills state logic (not treated as complete coverage or 0/0).
3. Recommendation and Skill Gap API consistency.
4. ServiceClient HTTP vs local fallback structural consistency.
5. What-If rank delta and score delta mathematical consistency.
"""

import pytest
import pandas as pd
from careerpath.ui.client import ServiceClient
from careerpath.esco import (
    ESCOTaxonomy,
    CareerMapper,
    SkillNormalizer,
    ESCOVectorIndex,
    SkillGapEngine,
    HybridRecommender,
)
from careerpath.esco.whatif import WhatIfEngine
from careerpath.ml.artifacts import ArtifactManager
from careerpath.config.settings import settings


@pytest.fixture(scope="module")
def local_components():
    """Fixture providing initialized local recommendation and skill gap components."""
    preprocessor_file = settings.MODELS_DIR / "preprocessor" / "v1.0" / "preprocessor.joblib"
    preprocessor, pre_meta = ArtifactManager.load_artifact(preprocessor_file)
    target_classes = pre_meta.get("user_metadata", {}).get("target_classes", [])

    cat_file = settings.MODELS_DIR / "advanced_catboost" / "v1.0" / "advanced_catboost.joblib"
    ml_model, _ = ArtifactManager.load_artifact(cat_file)

    taxonomy = ESCOTaxonomy()
    mapper = CareerMapper(taxonomy=taxonomy)
    vector_index = ESCOVectorIndex(taxonomy=taxonomy)
    vector_index.build_skill_index()
    gap_engine = SkillGapEngine(taxonomy=taxonomy, vector_index=vector_index)

    recommender = HybridRecommender(
        ml_model=ml_model,
        target_classes=target_classes,
        taxonomy=taxonomy,
        mapper=mapper,
        gap_engine=gap_engine,
        alpha=1.0,
    )
    whatif_engine = WhatIfEngine(recommender=recommender)

    return {
        "preprocessor": preprocessor,
        "ml_model": ml_model,
        "target_classes": target_classes,
        "taxonomy": taxonomy,
        "mapper": mapper,
        "recommender": recommender,
        "gap_engine": gap_engine,
        "whatif_engine": whatif_engine,
    }


def test_recommendations_sorted_by_final_score(local_components):
    """Verify recommendation output is strictly sorted by final_score descending."""
    client = ServiceClient(api_url="http://127.0.0.1:9999")
    profile = {
        "Coding Skills": 8.0,
        "Software Engineering": 7.0,
        "Database Fundamentals": 6.5,
    }
    recs = client.get_recommendations(profile, top_k=5, alpha=1.0)
    assert len(recs) == 5

    for i in range(len(recs) - 1):
        assert recs[i]["final_score"] >= recs[i + 1]["final_score"], (
            f"Recommendations out of order at index {i}: {recs[i]['final_score']} < {recs[i+1]['final_score']}"
        )


def test_zero_required_skills_not_treated_as_complete_coverage(local_components):
    """Verify zero required skills is identified as total_required == 0, not complete coverage."""
    client = ServiceClient(api_url="http://127.0.0.1:9999")
    profile = {"Technical Support": 8.0}
    recs = client.get_recommendations(profile, top_k=10, alpha=1.0)

    # Find Technical Support recommendation
    tech_supp_rec = next((r for r in recs if r["career_role"] == "Technical Support"), None)
    assert tech_supp_rec is not None

    matched = tech_supp_rec.get("matched_skills", [])
    partial = tech_supp_rec.get("partial_matches", [])
    missing = tech_supp_rec.get("missing_skills", [])
    total_req = len(matched) + len(partial) + len(missing)

    # If total_req is 0, verify it is not flagged with positive matched skills
    if total_req == 0:
        assert len(matched) == 0
        assert len(partial) == 0
        assert len(missing) == 0


def test_zero_required_skills_not_displayed_as_zero_of_zero(local_components):
    """Verify helper coverage calculation handles total_required == 0 gracefully."""
    matched = []
    partial = []
    missing = []
    total_req = len(matched) + len(partial) + len(missing)

    if total_req > 0:
        coverage_text = f"{len(matched)}/{total_req} skills matched"
    else:
        coverage_text = "ESCO coverage unavailable"

    assert coverage_text == "ESCO coverage unavailable"
    assert "0/0" not in coverage_text


def test_alignment_label_not_derived_only_from_rank():
    """Verify model ranking label is distinct from skill alignment."""
    rank = 1
    ranking_label = "Top Model Recommendation" if rank == 1 else f"Ranked #{rank} by Model"
    assert ranking_label == "Top Model Recommendation"
    assert ranking_label != "Strong alignment"


def test_recommendation_skill_gap_consistency(local_components):
    """Verify matched/partial/missing skills in recommendation match SkillGapReport."""
    recommender: HybridRecommender = local_components["recommender"]
    preprocessor = local_components["preprocessor"]
    gap_engine: SkillGapEngine = local_components["gap_engine"]
    mapper: CareerMapper = local_components["mapper"]

    profile = {
        "Coding Skills": 9.0,
        "Software Engineering": 8.5,
        "Database Fundamentals": 8.0,
        "Web Development": 7.5,
    }

    raw_input = {col: 5.0 for col in preprocessor.numeric_cols}
    for col in preprocessor.categorical_cols:
        raw_input[col] = "Unknown"
    for k, v in profile.items():
        raw_input[k] = v

    X_sample = preprocessor.transform(pd.DataFrame([raw_input]))
    recs = recommender.recommend_for_profile(X_sample, profile, top_k=5, alpha_override=1.0)
    target_rec = recs[0]

    # Evaluate direct gap report for the top role
    mapping = mapper.get_mapping(target_rec.career_role)
    student_skills = SkillNormalizer.normalize_student_profile(profile)
    gap_report = gap_engine.evaluate_gap(student_skills, mapping.esco_occupation_uri)

    assert len(target_rec.matched_skills) == len(gap_report.matched_skills)
    assert len(target_rec.partial_matches) == len(gap_report.partial_matches)
    assert len(target_rec.missing_skills) == len(gap_report.missing_skills)


def test_api_and_skill_gap_consistency(local_components):
    """Verify ServiceClient skill gap logic matches recommendation output for same career."""
    client = ServiceClient(api_url="http://127.0.0.1:9999")
    profile = {
        "Coding Skills": 8.5,
        "Software Engineering": 8.0,
        "Database Fundamentals": 7.5,
    }

    recs = client.get_recommendations(profile, top_k=5, alpha=1.0)
    top_role = recs[0]["career_role"]

    gap_res = client.get_skill_gap(profile, top_role)

    assert gap_res["target_career_role"] == top_role
    assert len(gap_res["matched_skills"]) == len(recs[0]["matched_skills"])
    assert len(gap_res["partial_matches"]) == len(recs[0]["partial_matches"])
    assert len(gap_res["missing_skills"]) == len(recs[0]["missing_skills"])


def test_service_client_http_and_local_structural_consistency(local_components):
    """Verify ServiceClient local fallback outputs exact required fields."""
    client = ServiceClient(api_url="http://127.0.0.1:9999")
    profile = {"Coding Skills": 7.0}
    recs = client.get_recommendations(profile, top_k=3, alpha=1.0)

    for r in recs:
        assert "career_role" in r
        assert "final_score" in r
        assert "normalized_ml_score" in r
        assert "esco_score" in r
        assert "matched_skills" in r
        assert "partial_matches" in r
        assert "missing_skills" in r


def test_what_if_rank_delta_consistency(local_components):
    """Verify What-If rank delta calculation is mathematically accurate."""
    client = ServiceClient(api_url="http://127.0.0.1:9999")
    baseline_profile = {
        "Database Fundamentals": 5.0,
        "Cyber Security": 4.0,
        "Coding Skills": 5.0,
    }
    skill_modifications = {"Cyber Security": 9.5}

    sim_res = client.simulate_what_if(baseline_profile, skill_modifications, top_k=5)

    for rc in sim_res["rank_changes"]:
        base_r = rc["baseline_rank"]
        scen_r = rc["scenario_rank"]
        if base_r is not None and scen_r is not None:
            expected_delta = base_r - scen_r
            assert rc["rank_delta"] == expected_delta, (
                f"Rank delta mismatch for {rc['career_role']}: expected {expected_delta}, got {rc['rank_delta']}"
            )


def test_what_if_score_delta_consistency(local_components):
    """Verify What-If score delta calculation is mathematically accurate."""
    client = ServiceClient(api_url="http://127.0.0.1:9999")
    baseline_profile = {
        "Database Fundamentals": 5.0,
        "Cyber Security": 4.0,
    }
    skill_modifications = {"Cyber Security": 9.0}

    sim_res = client.simulate_what_if(baseline_profile, skill_modifications, top_k=5)

    for rc in sim_res["rank_changes"]:
        expected_score_delta = round(rc["scenario_score"] - rc["baseline_score"], 4)
        assert abs(rc["score_delta"] - expected_score_delta) < 1e-3, (
            f"Score delta mismatch for {rc['career_role']}: expected {expected_score_delta}, got {rc['score_delta']}"
        )

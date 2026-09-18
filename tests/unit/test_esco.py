"""Unit tests for Phase 5 ESCO integration, semantic skill matching, and hybrid recommender."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from careerpath.esco.taxonomy import ESCOTaxonomy, ESCOOccupation, ESCOSkill
from careerpath.esco.mapping import CareerMapper, CareerMappingEntry
from careerpath.esco.normalization import SkillNormalizer, DemonstratedSkill
from careerpath.esco.embeddings import ESCOVectorIndex
from careerpath.esco.gap_engine import SkillGapEngine, SkillGapReport
from careerpath.esco.hybrid_recommender import HybridRecommender
from xgboost import XGBClassifier


@pytest.fixture
def sample_taxonomy():
    return ESCOTaxonomy()


def test_esco_taxonomy_loading(sample_taxonomy):
    assert len(sample_taxonomy.occupations) == 12
    assert len(sample_taxonomy.skills) >= 14

    occ = sample_taxonomy.get_occupation_by_uri("http://data.europa.eu/esco/occupation/204cfdd8-e4b7-4581-912f-98bcbd87884d")
    assert occ is not None
    assert occ.preferred_label == "Network Security Engineer"

    skills = sample_taxonomy.get_occupation_skills(occ.uri)
    assert len(skills) > 0


def test_career_mapper(sample_taxonomy):
    mapper = CareerMapper(taxonomy=sample_taxonomy)
    mapping = mapper.get_mapping("Network Security Engineer")

    assert mapping is not None
    assert mapping.mapping_status == "EXACT"
    assert mapping.confidence_score == 1.0
    assert mapping.esco_occupation_uri.startswith("http://data.europa.eu/esco/")

    all_mappings = mapper.get_all_mappings()
    assert len(all_mappings) == 12


def test_skill_normalizer():
    profile = {
        "Database Fundamentals": 8.0,
        "Computer Networks": 9.0,
        "Cyber Security": 7.5,
        "certifications": "rdbms certification",
    }
    skills = SkillNormalizer.normalize_student_profile(profile)

    assert len(skills) >= 3
    skill_labels = [sk.skill_label for sk in skills]
    assert "Database Management" in skill_labels
    assert "Network Security" in skill_labels


def test_vector_index_build_and_search(sample_taxonomy, tmp_path):
    vindex = ESCOVectorIndex(taxonomy=sample_taxonomy)
    vindex.build_skill_index()
    assert vindex.is_built is True

    res = vindex.search_skills("cyber security", top_k=3)
    assert len(res) == 3
    assert "skill_label" in res[0]
    assert "similarity_score" in res[0]
    assert res[0]["similarity_score"] > 0.0

    # Save and load index
    vindex.save_index(target_dir=tmp_path)
    new_index = ESCOVectorIndex(taxonomy=sample_taxonomy)
    new_index.load_index(target_dir=tmp_path)
    assert new_index.is_built is True


def test_skill_gap_engine(sample_taxonomy):
    vindex = ESCOVectorIndex(taxonomy=sample_taxonomy)
    vindex.build_skill_index()

    gap_engine = SkillGapEngine(taxonomy=sample_taxonomy, vector_index=vindex)
    student_skills = [
        DemonstratedSkill("Computer Networks", "Network Security", 0.9, "rating"),
        DemonstratedSkill("Cyber Security", "Information Security", 0.8, "rating"),
    ]

    occ_uri = "http://data.europa.eu/esco/occupation/204cfdd8-e4b7-4581-912f-98bcbd87884d"
    report = gap_engine.evaluate_gap(student_skills, occ_uri)

    assert report.total_required_skills > 0
    assert isinstance(report.coverage_score, float)
    assert len(report.matched_skills) + len(report.partial_matches) + len(report.missing_skills) == report.total_required_skills


def test_hybrid_recommender(sample_taxonomy):
    target_classes = ["Network Security Engineer", "Software Developer", "Database Administrator"]
    np.random.seed(42)

    X_train = pd.DataFrame(np.random.randn(50, 5), columns=[f"f_{i}" for i in range(5)])
    y_train = np.random.randint(0, 3, size=50)

    model = XGBClassifier(n_estimators=5, random_state=42, eval_metric="mlogloss")
    model.fit(X_train, y_train)

    vindex = ESCOVectorIndex(taxonomy=sample_taxonomy)
    vindex.build_skill_index()

    recommender = HybridRecommender(
        ml_model=model,
        target_classes=target_classes,
        taxonomy=sample_taxonomy,
        alpha=0.6,
    )

    profile = {"Database Fundamentals": 9.0, "Computer Networks": 8.5}
    X_sample = X_train.iloc[[0]]

    recs = recommender.recommend_for_profile(X_sample, profile, top_k=3)
    assert len(recs) == 3
    rec = recs[0]

    assert hasattr(rec, "career_role")
    assert hasattr(rec, "final_score")
    assert hasattr(rec, "raw_ml_probability")
    assert hasattr(rec, "normalized_ml_score")
    assert hasattr(rec, "esco_score")
    assert hasattr(rec, "matched_skills")
    assert rec.final_score >= 0.0

    # Verify mathematical reconstruction of final_score = alpha * norm_ml + (1 - alpha) * esco
    expected_score = round(0.6 * rec.normalized_ml_score + 0.4 * rec.esco_score, 4)
    assert rec.final_score == expected_score

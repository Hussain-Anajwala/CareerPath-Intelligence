"""Unit tests for Phase 6 What-If skill simulation engine."""

import pytest
import numpy as np
import pandas as pd

from careerpath.esco.taxonomy import ESCOTaxonomy
from careerpath.esco.hybrid_recommender import HybridRecommender
from careerpath.esco.whatif import WhatIfEngine, WhatIfSimulationResult
from xgboost import XGBClassifier


def test_whatif_simulation():
    taxonomy = ESCOTaxonomy()
    target_classes = ["Network Security Engineer", "Software Developer", "Database Administrator"]
    np.random.seed(42)

    X_train = pd.DataFrame(np.random.randn(50, 5), columns=[f"f_{i}" for i in range(5)])
    y_train = np.random.randint(0, 3, size=50)

    model = XGBClassifier(n_estimators=5, random_state=42, eval_metric="mlogloss")
    model.fit(X_train, y_train)

    recommender = HybridRecommender(ml_model=model, target_classes=target_classes, taxonomy=taxonomy)
    whatif_engine = WhatIfEngine(recommender=recommender)

    baseline_profile = {"Database Fundamentals": 5.0, "Computer Networks": 5.0}
    skill_modifications = {"Database Fundamentals": 9.5, "Cyber Security": 9.0}

    res = whatif_engine.simulate_skill_acquisition(
        X_sample=X_train.iloc[[0]],
        baseline_profile=baseline_profile,
        skill_modifications=skill_modifications,
        top_k=3,
    )

    assert isinstance(res, WhatIfSimulationResult)
    assert res.skills_modified == skill_modifications
    assert len(res.baseline_recommendations) == 3
    assert len(res.scenario_recommendations) == 3
    assert len(res.rank_changes) == 3

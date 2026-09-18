"""Unit tests for Phase 4 advanced ML models (XGBoost, LightGBM, CatBoost)."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from careerpath.ml.advanced import (
    AdvancedTrainer,
    calculate_calibration_metrics,
    measure_inference_latency,
    extract_feature_importances,
)
from careerpath.ml.evaluator import ModelEvaluator
from careerpath.ml.artifacts import ArtifactManager
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier


@pytest.fixture
def sample_multiclass_data():
    """Generates synthetic multiclass dataset for fast unit testing."""
    np.random.seed(42)
    n_samples = 200
    n_features = 10
    n_classes = 4

    X = pd.DataFrame(
        np.random.randn(n_samples, n_features),
        columns=[f"feat_{i}" for i in range(n_features)],
    )
    y = np.random.randint(0, n_classes, size=n_samples)

    X_train, X_test = X.iloc[:150], X.iloc[150:]
    y_train, y_test = y[:150], y[150:]

    return X_train, y_train, X_test, y_test


def test_get_model_factories():
    factories = AdvancedTrainer.get_model_factories(random_state=42)
    expected_keys = [
        "dummy_most_frequent",
        "logistic_regression",
        "random_forest",
        "xgboost",
        "lightgbm",
        "catboost",
    ]
    for key in expected_keys:
        assert key in factories
        factory, hparams = factories[key]
        assert callable(factory)
        assert isinstance(hparams, dict)


def test_xgb_lgb_catboost_fit_eval(sample_multiclass_data):
    X_train, y_train, X_test, y_test = sample_multiclass_data

    # Test XGBoost
    xgb_model = XGBClassifier(n_estimators=10, max_depth=3, random_state=42, eval_metric="mlogloss")
    xgb_model.fit(X_train, y_train)
    xgb_eval = ModelEvaluator.evaluate_classifier(xgb_model, X_test, y_test)

    assert "accuracy" in xgb_eval
    assert "top_1_accuracy" in xgb_eval
    assert xgb_eval["top_1_accuracy"] == xgb_eval["accuracy"]

    # Test LightGBM
    lgb_model = LGBMClassifier(n_estimators=10, max_depth=3, random_state=42, verbose=-1)
    lgb_model.fit(X_train, y_train)
    lgb_eval = ModelEvaluator.evaluate_classifier(lgb_model, X_test, y_test)

    assert "accuracy" in lgb_eval
    assert "top_1_accuracy" in lgb_eval
    assert lgb_eval["top_1_accuracy"] == lgb_eval["accuracy"]

    # Test CatBoost
    cat_model = CatBoostClassifier(iterations=10, depth=3, random_seed=42, verbose=0)
    cat_model.fit(X_train, y_train)
    cat_eval = ModelEvaluator.evaluate_classifier(cat_model, X_test, y_test)

    assert "accuracy" in cat_eval
    assert "top_1_accuracy" in cat_eval
    assert cat_eval["top_1_accuracy"] == cat_eval["accuracy"]


def test_calibration_metrics(sample_multiclass_data):
    X_train, y_train, X_test, y_test = sample_multiclass_data
    model = XGBClassifier(n_estimators=10, max_depth=3, random_state=42, eval_metric="mlogloss")
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)
    cal_metrics = calculate_calibration_metrics(y_test, y_prob)

    assert "log_loss" in cal_metrics
    assert "brier_score" in cal_metrics
    assert cal_metrics["log_loss"] >= 0
    assert cal_metrics["brier_score"] >= 0


def test_inference_latency(sample_multiclass_data):
    X_train, y_train, X_test, y_test = sample_multiclass_data
    model = XGBClassifier(n_estimators=10, max_depth=3, random_state=42, eval_metric="mlogloss")
    model.fit(X_train, y_train)

    latency = measure_inference_latency(model, X_test, n_runs=5)

    assert "single_sample_latency_ms" in latency
    assert "batch_total_latency_ms" in latency
    assert "batch_per_sample_latency_ms" in latency
    assert latency["single_sample_latency_ms"] >= 0


def test_extract_feature_importances(sample_multiclass_data):
    X_train, y_train, X_test, y_test = sample_multiclass_data
    feature_names = list(X_train.columns)

    model = XGBClassifier(n_estimators=10, max_depth=3, random_state=42, eval_metric="mlogloss")
    model.fit(X_train, y_train)

    importances = extract_feature_importances(model, feature_names, top_n=5)
    assert len(importances) == 5
    assert "feature" in importances[0]
    assert "importance" in importances[0]


def test_advanced_artifact_save_load(sample_multiclass_data, tmp_path):
    X_train, y_train, X_test, y_test = sample_multiclass_data
    model = XGBClassifier(n_estimators=10, max_depth=3, random_state=42, eval_metric="mlogloss")
    model.fit(X_train, y_train)

    artifact_dir = tmp_path / "advanced_xgboost" / "v1.0"
    artifact_file = ArtifactManager.save_artifact(
        model,
        artifact_name="advanced_xgboost",
        version="v1.0",
        target_dir=artifact_dir,
        metadata={"model_name": "xgboost"},
    )

    loaded_model, loaded_meta = ArtifactManager.load_artifact(artifact_file)
    assert loaded_meta["artifact_name"] == "advanced_xgboost"

    preds_orig = model.predict(X_test)
    preds_loaded = loaded_model.predict(X_test)
    np.testing.assert_array_equal(preds_orig, preds_loaded)

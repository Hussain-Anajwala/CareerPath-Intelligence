"""Unit tests for baseline ML models, cross-validation, Top-K evaluation, and model artifacts."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from careerpath.ml.evaluator import ModelEvaluator
from careerpath.ml.baseline import BaselineTrainer
from careerpath.ml.artifacts import ArtifactManager
from sklearn.dummy import DummyClassifier


@pytest.fixture
def synthetic_classification_data():
    """Fixture providing synthetic features and target labels for baseline testing."""
    np.random.seed(42)
    X = pd.DataFrame(
        {
            "f1": np.random.randn(100),
            "f2": np.random.randn(100),
            "f3": np.random.choice([0, 1], 100),
        }
    )
    y = np.random.choice([0, 1, 2], 100)
    return X, y


def test_top_k_accuracy():
    """Test Top-K accuracy calculation on known probability matrix."""
    y_true = np.array([0, 1, 2])
    # Class 0: highest prob on 0; Class 1: highest on 2, second on 1; Class 2: highest on 2
    y_prob = np.array(
        [
            [0.8, 0.1, 0.1],  # Top 1 correct for 0
            [0.1, 0.3, 0.6],  # Top 1 is 2, Top 2 includes 1
            [0.0, 0.1, 0.9],  # Top 1 correct for 2
        ]
    )

    top_1 = ModelEvaluator.calculate_top_k_accuracy(y_prob, y_true, k=1)
    top_2 = ModelEvaluator.calculate_top_k_accuracy(y_prob, y_true, k=2)

    assert round(top_1, 2) == round(2 / 3, 2)
    assert round(top_2, 2) == 1.0


def test_evaluate_classifier(synthetic_classification_data):
    """Test full classifier evaluation suite."""
    X, y = synthetic_classification_data
    model = DummyClassifier(strategy="most_frequent")
    model.fit(X, y)

    metrics = ModelEvaluator.evaluate_classifier(
        model, X, y, class_names=["Role A", "Role B", "Role C"]
    )
    assert "accuracy" in metrics
    assert "macro_f1" in metrics
    assert "confusion_matrix" in metrics
    assert "top_1_accuracy" in metrics
    assert metrics["top_1_accuracy"] == metrics["accuracy"]


def test_cross_validate_model(synthetic_classification_data):
    """Test Stratified K-Fold cross validation execution."""
    X, y = synthetic_classification_data
    factory = lambda: DummyClassifier(strategy="most_frequent")

    cv_results = BaselineTrainer.cross_validate_model(
        factory, X, y, n_splits=3, random_state=42
    )

    assert "cv_accuracy_mean" in cv_results
    assert "cv_macro_f1_mean" in cv_results
    assert cv_results["cv_accuracy_mean"] > 0.0


def test_run_all_baselines(tmp_path, synthetic_classification_data):
    """Test baseline trainer execution across all baseline models using temporary artifact directory."""
    X, y = synthetic_classification_data
    X_tr, X_te = X.iloc[:80], X.iloc[80:]
    y_tr, y_te = y[:80], y[80:]

    results = BaselineTrainer.run_all_baselines(
        X_train=X_tr,
        y_train=y_tr,
        X_test=X_te,
        y_test=y_te,
        class_names=["Class 0", "Class 1", "Class 2"],
        n_splits=2,
        random_state=42,
        save_artifacts=True,
        target_base_dir=tmp_path,
    )

    assert "dummy_most_frequent" in results
    assert "logistic_regression" in results
    assert "random_forest" in results

    lr_res = results["logistic_regression"]
    assert "cv_metrics" in lr_res
    assert "test_metrics" in lr_res
    assert Path(lr_res["artifact_path"]).exists()

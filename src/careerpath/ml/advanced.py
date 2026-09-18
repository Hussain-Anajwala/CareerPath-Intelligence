"""Advanced tree-based ML experimentation framework (XGBoost, LightGBM, CatBoost)."""

import time
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np
import pandas as pd

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import log_loss

from careerpath.config.logging import logger
from careerpath.ml.evaluator import ModelEvaluator
from careerpath.ml.artifacts import ArtifactManager


def calculate_calibration_metrics(y_true: np.ndarray, y_prob: np.ndarray) -> Dict[str, float]:
    """Calculates log-loss and multiclass Brier score.
    
    Multiclass Brier Score definition:
        Brier = (1 / N) * sum_{i=1}^N sum_{k=1}^K (y_{i,k} - p_{i,k})^2
    where y_{i,k} is the one-hot encoded true class indicator and p_{i,k} is predicted probability for class k.
    """
    classes = np.unique(y_true)
    # Log loss calculation
    try:
        loss = float(log_loss(y_true, y_prob, labels=classes))
    except Exception:
        loss = float("nan")

    # Multiclass Brier score calculation
    N, K = y_prob.shape
    one_hot_y = np.zeros((N, K))
    for i, label in enumerate(y_true):
        if label < K:
            one_hot_y[i, label] = 1.0

    brier = float(np.mean(np.sum((one_hot_y - y_prob) ** 2, axis=1)))

    return {
        "log_loss": round(loss, 4),
        "brier_score": round(brier, 4),
    }


def measure_inference_latency(
    model: Any, X_test: pd.DataFrame, n_runs: int = 50
) -> Dict[str, float]:
    """Measures single-profile and batch inference latency in milliseconds."""
    single_sample = X_test.iloc[[0]]

    # Warmup
    _ = model.predict(single_sample)
    _ = model.predict(X_test)

    # Single profile latency
    start_single = time.perf_counter()
    for _ in range(n_runs):
        _ = model.predict(single_sample)
    end_single = time.perf_counter()
    single_latency_ms = ((end_single - start_single) / n_runs) * 1000.0

    # Batch latency (total test set)
    start_batch = time.perf_counter()
    for _ in range(n_runs):
        _ = model.predict(X_test)
    end_batch = time.perf_counter()
    batch_latency_ms = ((end_batch - start_batch) / n_runs) * 1000.0

    per_sample_batch_ms = batch_latency_ms / len(X_test)

    return {
        "single_sample_latency_ms": round(single_latency_ms, 4),
        "batch_total_latency_ms": round(batch_latency_ms, 4),
        "batch_per_sample_latency_ms": round(per_sample_batch_ms, 4),
    }


def extract_feature_importances(
    model: Any, feature_names: List[str], top_n: int = 15
) -> List[Dict[str, Any]]:
    """Extracts top feature importances for tree-based models or linear models."""
    importances = None
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.mean(np.abs(model.coef_), axis=0)

    if importances is None or len(importances) != len(feature_names):
        return []

    total = np.sum(importances)
    norm_importances = importances / total if total > 0 else importances

    indices = np.argsort(norm_importances)[::-1][:top_n]
    result = [
        {
            "feature": feature_names[i],
            "importance": round(float(norm_importances[i]), 4),
            "raw_score": round(float(importances[i]), 6),
        }
        for i in indices
    ]
    return result


class AdvancedTrainer:
    """Trainer and cross-validation framework for advanced ML models."""

    @staticmethod
    def get_model_factories(random_state: int = 42) -> Dict[str, Tuple[Callable[[], Any], Dict[str, Any]]]:
        """Returns model factory functions and hyperparameter metadata."""
        factories = {
            "dummy_most_frequent": (
                lambda: DummyClassifier(strategy="most_frequent"),
                {"strategy": "most_frequent"},
            ),
            "logistic_regression": (
                lambda: LogisticRegression(max_iter=1000, random_state=random_state),
                {"max_iter": 1000, "random_state": random_state},
            ),
            "random_forest": (
                lambda: RandomForestClassifier(
                    n_estimators=100, random_state=random_state, n_jobs=-1
                ),
                {"n_estimators": 100, "random_state": random_state, "n_jobs": -1},
            ),
            "xgboost": (
                lambda: XGBClassifier(
                    n_estimators=100,
                    max_depth=5,
                    learning_rate=0.1,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    min_child_weight=1,
                    random_state=random_state,
                    n_jobs=-1,
                    eval_metric="mlogloss",
                ),
                {
                    "n_estimators": 100,
                    "max_depth": 5,
                    "learning_rate": 0.1,
                    "subsample": 0.8,
                    "colsample_bytree": 0.8,
                    "min_child_weight": 1,
                    "random_state": random_state,
                    "n_jobs": -1,
                    "eval_metric": "mlogloss",
                },
            ),
            "lightgbm": (
                lambda: LGBMClassifier(
                    n_estimators=100,
                    learning_rate=0.1,
                    num_leaves=31,
                    max_depth=-1,
                    min_child_samples=20,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    random_state=random_state,
                    n_jobs=-1,
                    verbose=-1,
                ),
                {
                    "n_estimators": 100,
                    "learning_rate": 0.1,
                    "num_leaves": 31,
                    "max_depth": -1,
                    "min_child_samples": 20,
                    "subsample": 0.8,
                    "colsample_bytree": 0.8,
                    "random_state": random_state,
                    "n_jobs": -1,
                    "verbose": -1,
                },
            ),
            "catboost": (
                lambda: CatBoostClassifier(
                    iterations=100,
                    depth=6,
                    learning_rate=0.1,
                    loss_function="MultiClass",
                    random_seed=random_state,
                    verbose=0,
                    thread_count=-1,
                ),
                {
                    "iterations": 100,
                    "depth": 6,
                    "learning_rate": 0.1,
                    "loss_function": "MultiClass",
                    "random_seed": random_state,
                    "verbose": 0,
                    "thread_count": -1,
                },
            ),
        }
        return factories

    @classmethod
    def cross_validate_model(
        cls,
        model_factory: Callable[[], Any],
        X_train: pd.DataFrame,
        y_train: np.ndarray,
        n_splits: int = 5,
        random_state: int = 42,
    ) -> Dict[str, Any]:
        """Runs Stratified K-Fold cross validation on training data ONLY."""
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

        accs, macro_f1s, weighted_f1s = [], [], []
        top_1_accs, top_3_accs, top_5_accs = [], [], []

        for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train)):
            X_tr, y_tr = X_train.iloc[train_idx], y_train[train_idx]
            X_val, y_val = X_train.iloc[val_idx], y_train[val_idx]

            model = model_factory()
            model.fit(X_tr, y_tr)

            eval_res = ModelEvaluator.evaluate_classifier(model, X_val, y_val)
            accs.append(eval_res["accuracy"])
            macro_f1s.append(eval_res["macro_f1"])
            weighted_f1s.append(eval_res["weighted_f1"])

            if "top_1_accuracy" in eval_res:
                top_1_accs.append(eval_res["top_1_accuracy"])
            if "top_3_accuracy" in eval_res:
                top_3_accs.append(eval_res["top_3_accuracy"])
            if "top_5_accuracy" in eval_res:
                top_5_accs.append(eval_res["top_5_accuracy"])

        cv_results = {
            "cv_accuracy_mean": round(float(np.mean(accs)), 4),
            "cv_accuracy_std": round(float(np.std(accs)), 4),
            "cv_macro_f1_mean": round(float(np.mean(macro_f1s)), 4),
            "cv_macro_f1_std": round(float(np.std(macro_f1s)), 4),
            "cv_weighted_f1_mean": round(float(np.mean(weighted_f1s)), 4),
        }

        if top_1_accs:
            cv_results["cv_top_1_mean"] = round(float(np.mean(top_1_accs)), 4)
        if top_3_accs:
            cv_results["cv_top_3_mean"] = round(float(np.mean(top_3_accs)), 4)
        if top_5_accs:
            cv_results["cv_top_5_mean"] = round(float(np.mean(top_5_accs)), 4)

        return cv_results

    @classmethod
    def run_all_advanced_experiments(
        cls,
        X_train: pd.DataFrame,
        y_train: np.ndarray,
        X_test: pd.DataFrame,
        y_test: np.ndarray,
        class_names: Optional[List[str]] = None,
        n_splits: int = 5,
        random_state: int = 42,
        save_artifacts: bool = True,
        target_base_dir: Optional[Path] = None,
        dataset_sha256: str = "cd9b2d1ce8d1d582f1e472a7dcb2724f687e22ac5932d5760eac95c53d281d62",
    ) -> Dict[str, Dict[str, Any]]:
        """Trains, cross-validates, and evaluates all baseline + advanced ML models."""
        factories = cls.get_model_factories(random_state=random_state)
        feature_names = list(X_train.columns)

        results = {}

        for name, (factory, hparams) in factories.items():
            logger.info(f"Running advanced experiment for model: {name}")

            # 1. Stratified 5-Fold Cross Validation on Train Data
            cv_res = cls.cross_validate_model(
                factory, X_train, y_train, n_splits=n_splits, random_state=random_state
            )

            # 2. Fit Full Model on Train Split
            model = factory()
            model.fit(X_train, y_train)

            # 3. Evaluate Holdout Test Set
            test_res = ModelEvaluator.evaluate_classifier(
                model, X_test, y_test, class_names=class_names
            )

            # 4. Compute Calibration Metrics
            calibration_metrics = {}
            if hasattr(model, "predict_proba"):
                try:
                    y_prob = model.predict_proba(X_test)
                    calibration_metrics = calculate_calibration_metrics(y_test, y_prob)
                except Exception as e:
                    logger.warning(f"Calibration metric calculation failed for {name}: {e}")

            # 5. Measure Inference Latency
            latency_metrics = measure_inference_latency(model, X_test)

            # 6. Feature Importances
            top_features = extract_feature_importances(model, feature_names, top_n=15)

            # 7. Artifact Serialization
            artifact_file_str = ""
            if save_artifacts:
                category = "baseline" if "dummy" in name or name in ["logistic_regression", "random_forest"] else "advanced"
                artifact_name = f"{category}_{name}"
                artifact_dir = (
                    (target_base_dir / artifact_name / "v1.0")
                    if target_base_dir
                    else None
                )

                metadata = {
                    "model_name": name,
                    "dataset_sha256": dataset_sha256,
                    "hyperparameters": hparams,
                    "cv_metrics": cv_res,
                    "test_metrics": test_res,
                    "calibration_metrics": calibration_metrics,
                    "latency_metrics": latency_metrics,
                    "num_train_samples": len(X_train),
                    "num_features": X_train.shape[1],
                }

                artifact_file = ArtifactManager.save_artifact(
                    model,
                    artifact_name=artifact_name,
                    version="v1.0",
                    target_dir=artifact_dir,
                    metadata=metadata,
                )
                artifact_file_str = str(artifact_file)

            results[name] = {
                "model": model,
                "hyperparameters": hparams,
                "cv_metrics": cv_res,
                "test_metrics": test_res,
                "calibration_metrics": calibration_metrics,
                "latency_metrics": latency_metrics,
                "top_features": top_features,
                "artifact_path": artifact_file_str,
            }

            logger.info(
                f"[{name}] CV Macro F1: {cv_res['cv_macro_f1_mean']} | Test Acc: {test_res['accuracy']} | Test Macro F1: {test_res['macro_f1']} | Top-3: {test_res.get('top_3_accuracy', 'N/A')}"
            )

        return results

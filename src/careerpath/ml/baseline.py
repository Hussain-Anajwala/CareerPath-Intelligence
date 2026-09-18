"""Baseline machine learning experimentation framework."""

from typing import Dict, Any, List, Tuple, Optional
from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold

from careerpath.config.logging import logger
from careerpath.ml.evaluator import ModelEvaluator
from careerpath.ml.artifacts import ArtifactManager


class BaselineTrainer:
    """Trainer and cross-validation framework for baseline ML models."""

    @staticmethod
    def cross_validate_model(
        model_factory,
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
    def run_all_baselines(
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
    ) -> Dict[str, Dict[str, Any]]:
        """Trains and evaluates Dummy, Logistic Regression, and Random Forest baselines."""
        baseline_configs = {
            "dummy_most_frequent": lambda: DummyClassifier(strategy="most_frequent"),
            "logistic_regression": lambda: LogisticRegression(
                max_iter=1000, random_state=random_state
            ),
            "random_forest": lambda: RandomForestClassifier(
                n_estimators=100, random_state=random_state, n_jobs=-1
            ),
        }

        results = {}

        for name, factory in baseline_configs.items():
            logger.info(f"Running baseline experiment: {name}")

            # 1. Stratified Cross-Validation on Train Split
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

            # 4. Save Model Artifact if requested
            artifact_file_str = ""
            if save_artifacts:
                artifact_dir = (
                    (target_base_dir / f"baseline_{name}" / "v1.0")
                    if target_base_dir
                    else None
                )
                artifact_file = ArtifactManager.save_artifact(
                    model,
                    artifact_name=f"baseline_{name}",
                    version="v1.0",
                    target_dir=artifact_dir,
                    metadata={
                        "cv_metrics": cv_res,
                        "test_metrics": test_res,
                        "num_train_samples": len(X_train),
                        "num_features": X_train.shape[1],
                    },
                )
                artifact_file_str = str(artifact_file)

            results[name] = {
                "model": model,
                "cv_metrics": cv_res,
                "test_metrics": test_res,
                "artifact_path": artifact_file_str,
            }

            logger.info(
                f"[{name}] CV Macro F1: {cv_res['cv_macro_f1_mean']} | Test Accuracy: {test_res['accuracy']} | Test Macro F1: {test_res['macro_f1']}"
            )

        return results

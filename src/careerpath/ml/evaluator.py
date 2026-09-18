"""Comprehensive evaluation metrics and Top-K ranking accuracy calculator."""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from sklearn.dummy import DummyClassifier


class ModelEvaluator:
    """Evaluates multi-class classification and ranking performance metrics."""

    @staticmethod
    def calculate_top_k_accuracy(
        y_prob: np.ndarray,
        y_true: np.ndarray,
        k: int,
        classes: Optional[np.ndarray] = None,
    ) -> float:
        """Calculates Top-K hit rate / accuracy given predicted class probabilities."""
        if k <= 0:
            raise ValueError("k must be greater than 0.")

        num_samples = len(y_true)
        if num_samples == 0:
            return 0.0

        if k == 1:
            # For k=1, use argmax (matching scikit-learn model.predict behavior)
            top_1_indices = np.argmax(y_prob, axis=1)
            if classes is not None:
                top_1_preds = classes[top_1_indices]
            else:
                top_1_preds = top_1_indices
            return float(np.mean(top_1_preds == y_true))

        # For k > 1, sort probability column indices descending and check if true class is in top k
        top_k_col_indices = np.argsort(y_prob, axis=1)[:, -k:]

        if classes is not None:
            top_k_predicted_classes = classes[top_k_col_indices]
        else:
            top_k_predicted_classes = top_k_col_indices

        hits = [
            y_true[i] in top_k_predicted_classes[i] for i in range(num_samples)
        ]
        return float(np.mean(hits))

    @classmethod
    def evaluate_classifier(
        cls,
        model: Any,
        X: pd.DataFrame,
        y_true: np.ndarray,
        class_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Calculates full classification evaluation suite."""
        y_pred = model.predict(X)

        acc = float(accuracy_score(y_true, y_pred))
        macro_prec = float(
            precision_score(y_true, y_pred, average="macro", zero_division=0)
        )
        macro_rec = float(
            recall_score(y_true, y_pred, average="macro", zero_division=0)
        )
        macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
        weighted_f1 = float(
            f1_score(y_true, y_pred, average="weighted", zero_division=0)
        )

        cm = confusion_matrix(y_true, y_pred).tolist()

        metrics: Dict[str, Any] = {
            "accuracy": round(acc, 4),
            "macro_precision": round(macro_prec, 4),
            "macro_recall": round(macro_rec, 4),
            "macro_f1": round(macro_f1, 4),
            "weighted_f1": round(weighted_f1, 4),
            "confusion_matrix": cm,
        }

        # Calculate Top-K metrics if probabilities are available
        is_dummy = isinstance(model, DummyClassifier)
        if hasattr(model, "predict_proba"):
            try:
                y_prob = model.predict_proba(X)
                classes = getattr(model, "classes_", None)

                # Enforce exact identity between top_1_accuracy and accuracy_score
                metrics["top_1_accuracy"] = round(acc, 4)

                # For DummyClassifier, Top-3 and Top-5 ranking metrics are not semantically meaningful
                # because tied zero probabilities produce arbitrary ordering.
                if not is_dummy:
                    num_classes = y_prob.shape[1]
                    if num_classes >= 3:
                        metrics["top_3_accuracy"] = round(
                            cls.calculate_top_k_accuracy(
                                y_prob, y_true, k=3, classes=classes
                            ),
                            4,
                        )
                    if num_classes >= 5:
                        metrics["top_5_accuracy"] = round(
                            cls.calculate_top_k_accuracy(
                                y_prob, y_true, k=5, classes=classes
                            ),
                            4,
                        )
            except Exception:
                pass

        if class_names:
            report_dict = classification_report(
                y_true,
                y_pred,
                target_names=class_names,
                output_dict=True,
                zero_division=0,
            )
            metrics["per_class_report"] = report_dict

        return metrics

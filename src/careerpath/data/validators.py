"""Automated dataset validation, audit, and quality inspection suite."""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

from careerpath.data.schemas import (
    DatasetSchemaConfig,
    ValidationResult,
    LeakageAuditResult,
)
from careerpath.config.logging import logger


class DataValidator:
    """Suite for auditing dataset quality, integrity, leakage, and schema compatibility."""

    @staticmethod
    def validate_schema(
        df: pd.DataFrame, config: DatasetSchemaConfig
    ) -> ValidationResult:
        """Validates dataframe schema against expected requirements."""
        errors: List[str] = []
        warnings: List[str] = []

        total_rows, total_columns = df.shape

        if total_rows < config.min_rows:
            errors.append(
                f"Dataset row count ({total_rows}) is below minimum requirement ({config.min_rows})."
            )

        missing_cols = [col for col in config.required_columns if col not in df.columns]
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")

        if config.target_column and config.target_column not in df.columns:
            errors.append(f"Target column '{config.target_column}' not found in dataset.")

        duplicate_count = int(df.duplicated().sum())
        if duplicate_count > 0:
            warnings.append(f"Found {duplicate_count} exact duplicate rows.")

        missing_summary = (df.isnull().mean() * 100).round(2).to_dict()

        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            total_rows=total_rows,
            total_columns=total_columns,
            missing_columns=missing_cols,
            duplicate_rows=duplicate_count,
            missing_value_summary=missing_summary,
            errors=errors,
            warnings=warnings,
        )

    @staticmethod
    def audit_target(df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """Audits target column distribution, missingness, and class balance."""
        if target_column not in df.columns:
            return {"error": f"Target column '{target_column}' not in DataFrame."}

        target = df[target_column]
        missing_count = int(target.isnull().sum())
        missing_pct = float((missing_count / len(df)) * 100)

        value_counts = target.value_counts(dropna=False).to_dict()
        unique_classes = int(target.nunique(dropna=True))

        if unique_classes > 0 and len(target.dropna()) > 0:
            counts = target.value_counts(dropna=True)
            max_count = int(counts.max())
            min_count = int(counts.min())
            imbalance_ratio = round(max_count / max(min_count, 1), 2)
        else:
            imbalance_ratio = 1.0

        if imbalance_ratio > 10.0:
            balance_status = "Highly Imbalanced"
        elif imbalance_ratio > 3.0:
            balance_status = "Moderately Imbalanced"
        else:
            balance_status = "Healthy Balance"

        return {
            "target_column": target_column,
            "total_samples": len(df),
            "missing_count": missing_count,
            "missing_percentage": round(missing_pct, 2),
            "unique_classes": unique_classes,
            "value_counts": value_counts,
            "imbalance_ratio": imbalance_ratio,
            "balance_status": balance_status,
        }

    @staticmethod
    def audit_leakage(
        df: pd.DataFrame,
        target_column: Optional[str] = None,
        suspicious_keywords: Optional[List[str]] = None,
    ) -> LeakageAuditResult:
        """Audits features for potential target leakage or post-outcome information."""
        if suspicious_keywords is None:
            suspicious_keywords = [
                "target",
                "hired",
                "outcome",
                "label",
                "salary_after",
                "placement_status",
                "accepted_job",
                "employment_id",
            ]

        suspicious_cols: List[str] = []
        findings: List[Dict[str, str]] = []

        for col in df.columns:
            col_lower = col.lower()
            if target_column and col == target_column:
                continue

            for kw in suspicious_keywords:
                if kw in col_lower:
                    suspicious_cols.append(col)
                    findings.append(
                        {
                            "column": col,
                            "reason": f"Column name contains suspicious keyword '{kw}'.",
                            "recommendation": "Inspect feature source to ensure it is available prior to recommendation.",
                        }
                    )
                    break

            # Check if column is a 1-to-1 duplicate or mirror of target column
            if target_column and target_column in df.columns:
                if df[col].nunique() == df[target_column].nunique():
                    crosstab = pd.crosstab(df[col], df[target_column])
                    if (crosstab.values > 0).sum(axis=1).max() == 1:
                        if col not in suspicious_cols:
                            suspicious_cols.append(col)
                        findings.append(
                            {
                                "column": col,
                                "reason": f"Column '{col}' exhibits 1-to-1 mapping with target '{target_column}'.",
                                "recommendation": "Remove feature to prevent trivial target leakage.",
                            }
                        )

        is_leakage = len(suspicious_cols) > 0

        return LeakageAuditResult(
            is_leakage_detected=is_leakage,
            suspicious_columns=suspicious_cols,
            findings=findings,
        )

    @staticmethod
    def detect_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> Dict[str, Any]:
        """Detects exact duplicate rows or duplicate IDs."""
        total_rows = len(df)
        duplicate_rows = int(df.duplicated(subset=subset).sum())

        return {
            "total_rows": total_rows,
            "duplicate_count": duplicate_rows,
            "duplicate_percentage": round((duplicate_rows / max(total_rows, 1)) * 100, 2),
            "subset_checked": subset or "all_columns",
        }

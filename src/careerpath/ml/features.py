"""Deterministic, leakage-safe feature engineering module for student career data."""

from typing import List, Optional
import pandas as pd
import numpy as np


class FeatureExtractor:
    """Computes derived domain features from raw student profile inputs cleanly."""

    def __init__(
        self,
        rating_cols: Optional[List[str]] = None,
        hackathon_col: str = "hackathons",
    ):
        self.rating_cols = rating_cols or [
            "Logical quotient rating",
            "coding skills rating",
            "public speaking points",
        ]
        self.hackathon_col = hackathon_col

    def fit(self, df: pd.DataFrame, y: Optional[pd.Series] = None) -> "FeatureExtractor":
        """Fits extractor parameters if needed (stateless for deterministic feature engineering)."""
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforms input DataFrame by adding derived features."""
        df_out = df.copy()

        # 1. Rating Aggregates
        valid_rating_cols = [c for c in self.rating_cols if c in df_out.columns]
        if valid_rating_cols:
            df_out["technical_rating_sum"] = df_out[valid_rating_cols].sum(axis=1)
            df_out["technical_rating_mean"] = df_out[valid_rating_cols].mean(axis=1).round(4)

        # 2. Problem Solving Index
        if "Logical quotient rating" in df_out.columns and self.hackathon_col in df_out.columns:
            df_out["problem_solving_index"] = (
                df_out["Logical quotient rating"] * (df_out[self.hackathon_col] + 1)
            )

        return df_out

    def fit_transform(self, df: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """Fits extractor and transforms DataFrame."""
        return self.fit(df, y).transform(df)

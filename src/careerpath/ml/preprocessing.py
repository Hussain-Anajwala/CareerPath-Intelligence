"""Leakage-safe student profile preprocessing pipeline using scikit-learn standard transformers."""

from typing import List, Optional, Dict, Any, Union
import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder

from careerpath.config.logging import logger
from careerpath.data.schemas import RAW_NUMERIC_COLS, RAW_CATEGORICAL_COLS


class StudentProfilePreprocessor(BaseEstimator, TransformerMixin):
    """Scikit-learn compatible preprocessor that fits scalers, imputers, and encoders strictly on train data."""

    def __init__(
        self,
        numeric_cols: Optional[List[str]] = None,
        categorical_cols: Optional[List[str]] = None,
        scale_numeric: bool = True,
        handle_unknown: str = "ignore",
    ):
        self.numeric_cols = numeric_cols if numeric_cols is not None else RAW_NUMERIC_COLS
        self.categorical_cols = (
            categorical_cols if categorical_cols is not None else RAW_CATEGORICAL_COLS
        )
        self.scale_numeric = scale_numeric
        self.handle_unknown = handle_unknown

        self.column_transformer_: Optional[ColumnTransformer] = None
        self.label_encoder_: Optional[LabelEncoder] = None
        self.is_fitted_: bool = False
        self.feature_names_out_: List[str] = []

    def fit(
        self, X: pd.DataFrame, y: Optional[Union[pd.Series, np.ndarray, List]] = None
    ) -> "StudentProfilePreprocessor":
        """Fits imputers, scalers, and encoders ONLY on training DataFrame X and optional target y."""
        X_df = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X)

        # Identify actual columns present in input DataFrame
        num_cols = [c for c in self.numeric_cols if c in X_df.columns]
        cat_cols = [c for c in self.categorical_cols if c in X_df.columns]

        transformers = []

        if num_cols:
            num_steps = [("imputer", SimpleImputer(strategy="median"))]
            if self.scale_numeric:
                num_steps.append(("scaler", StandardScaler()))

            num_pipeline = Pipeline(steps=num_steps)
            transformers.append(("numeric", num_pipeline, num_cols))

        if cat_cols:
            cat_steps = [
                ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
                (
                    "onehot",
                    OneHotEncoder(
                        handle_unknown=self.handle_unknown,
                        sparse_output=False,
                    ),
                ),
            ]
            cat_pipeline = Pipeline(steps=cat_steps)
            transformers.append(("categorical", cat_pipeline, cat_cols))

        if transformers:
            self.column_transformer_ = ColumnTransformer(
                transformers=transformers, remainder="drop"
            )
            self.column_transformer_.fit(X_df)

            # Reconstruct output feature names
            feature_names = []
            if num_cols:
                feature_names.extend(num_cols)
            if cat_cols:
                cat_encoder = (
                    self.column_transformer_.named_transformers_["categorical"]
                    .named_steps["onehot"]
                )
                encoded_cats = list(cat_encoder.get_feature_names_out(cat_cols))
                feature_names.extend(encoded_cats)
            self.feature_names_out_ = feature_names

        if y is not None:
            self.label_encoder_ = LabelEncoder()
            self.label_encoder_.fit(y)

        self.is_fitted_ = True
        logger.info(
            f"Preprocessor successfully fitted on {len(X_df)} samples. Output features: {len(self.feature_names_out_)}"
        )
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transforms input DataFrame X using learned parameters without modifying preprocessor state."""
        if not self.is_fitted_:
            raise RuntimeError(
                "StudentProfilePreprocessor is not fitted. Call 'fit' before 'transform'."
            )

        X_df = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X)

        if self.column_transformer_ is None:
            return X_df

        transformed_array = self.column_transformer_.transform(X_df)
        return pd.DataFrame(
            transformed_array,
            columns=self.feature_names_out_,
            index=X_df.index,
        )

    def fit_transform(
        self, X: pd.DataFrame, y: Optional[Union[pd.Series, np.ndarray, List]] = None
    ) -> pd.DataFrame:
        """Fits on X (and y) and returns transformed DataFrame."""
        return self.fit(X, y).transform(X)

    def transform_target(self, y: Union[pd.Series, np.ndarray, List]) -> np.ndarray:
        """Transforms target labels using fitted LabelEncoder."""
        if self.label_encoder_ is None:
            raise RuntimeError("LabelEncoder is not fitted.")
        return self.label_encoder_.transform(y)

    def inverse_transform_target(self, y_encoded: np.ndarray) -> np.ndarray:
        """Inverts target transformation back to original labels."""
        if self.label_encoder_ is None:
            raise RuntimeError("LabelEncoder is not fitted.")
        return self.label_encoder_.inverse_transform(y_encoded)

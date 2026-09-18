"""Reproducible, leakage-safe dataset splitting utilities."""

from typing import Tuple, Optional, Dict, Any
import pandas as pd
from sklearn.model_selection import train_test_split

from careerpath.config.logging import logger


class DatasetSplitter:
    """Utility for reproducible train/test and train/val/test splits."""

    @staticmethod
    def split(
        df: pd.DataFrame,
        target_column: Optional[str] = None,
        test_size: float = 0.2,
        val_size: float = 0.0,
        random_state: int = 42,
        stratify: bool = True,
    ) -> Dict[str, pd.DataFrame]:
        """Splits input DataFrame into train, optional val, and test partitions."""
        if test_size <= 0 or test_size >= 1:
            raise ValueError("test_size must be strictly between 0 and 1.")

        if val_size < 0 or (test_size + val_size) >= 1:
            raise ValueError("test_size + val_size must be less than 1.")

        stratify_target = None
        if stratify and target_column and target_column in df.columns:
            target_counts = df[target_column].value_counts()
            if (target_counts >= 2).all():
                stratify_target = df[target_column]
            else:
                logger.warning(
                    "Stratification disabled: Some target classes have fewer than 2 samples."
                )

        if val_size == 0.0:
            train_df, test_df = train_test_split(
                df,
                test_size=test_size,
                random_state=random_state,
                stratify=stratify_target,
            )
            logger.info(
                f"Dataset split complete: Train ({len(train_df)} rows), Test ({len(test_df)} rows)."
            )
            return {"train": train_df, "test": test_df}
        else:
            # First split off test set
            temp_df, test_df = train_test_split(
                df,
                test_size=test_size,
                random_state=random_state,
                stratify=stratify_target,
            )
            # Adjust val_size relative to remaining temp_df
            relative_val_size = val_size / (1.0 - test_size)
            temp_stratify = (
                temp_df[target_column]
                if (stratify_target is not None and (temp_df[target_column].value_counts() >= 2).all())
                else None
            )

            train_df, val_df = train_test_split(
                temp_df,
                test_size=relative_val_size,
                random_state=random_state,
                stratify=temp_stratify,
            )

            logger.info(
                f"Dataset split complete: Train ({len(train_df)}), Val ({len(val_df)}), Test ({len(test_df)})."
            )
            return {"train": train_df, "val": val_df, "test": test_df}

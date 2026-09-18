"""Unit and leakage-regression tests for data pipeline, splitting, feature engineering, and artifact serialization."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from careerpath.ml.features import FeatureExtractor
from careerpath.ml.splitting import DatasetSplitter
from careerpath.ml.preprocessing import StudentProfilePreprocessor
from careerpath.ml.artifacts import ArtifactManager


@pytest.fixture
def synthetic_pipeline_dataframe():
    """Fixture providing a synthetic dataset for testing pipeline mechanics."""
    np.random.seed(42)
    return pd.DataFrame(
        {
            "student_id": [f"S{i:03d}" for i in range(1, 51)],
            "Logical quotient rating": np.random.randint(1, 10, 50),
            "hackathons": np.random.randint(0, 7, 50),
            "academic_score": np.random.uniform(5.0, 10.0, 50).round(2),
            "python_skill": np.random.choice([np.nan, 2.0, 5.0, 8.0, 10.0], 50),
            "sql_skill": np.random.choice([1.0, 4.0, 7.0, 9.0], 50),
            "education_level": np.random.choice(
                ["Undergraduate", "Postgraduate", np.nan], 50
            ),
            "analytics_interest": np.random.choice([0, 1], 50),
            "career_role": np.random.choice(
                ["Data Analyst", "Software Engineer", "Data Scientist"], 50
            ),
        }
    )


def test_feature_extractor_deterministic(synthetic_pipeline_dataframe):
    """Test feature extractor generates expected derived academic and skill metrics."""
    extractor = FeatureExtractor(
        rating_cols=["academic_score", "python_skill", "sql_skill"],
        hackathon_col="analytics_interest",
    )
    df_transformed = extractor.fit_transform(synthetic_pipeline_dataframe)

    assert "technical_rating_sum" in df_transformed.columns
    assert "technical_rating_mean" in df_transformed.columns
    assert "problem_solving_index" in df_transformed.columns
    assert len(df_transformed) == 50


def test_dataset_splitter_reproducible(synthetic_pipeline_dataframe):
    """Test dataset splitter divides data reproducibly with stratification."""
    splits = DatasetSplitter.split(
        synthetic_pipeline_dataframe,
        target_column="career_role",
        test_size=0.2,
        random_state=42,
    )
    assert len(splits["train"]) == 40
    assert len(splits["test"]) == 10

    # Repeat split and verify identity
    splits2 = DatasetSplitter.split(
        synthetic_pipeline_dataframe,
        target_column="career_role",
        test_size=0.2,
        random_state=42,
    )
    pd.testing.assert_frame_equal(splits["train"], splits2["train"])


def test_preprocessor_fit_transform(synthetic_pipeline_dataframe):
    """Test fitting preprocessor on train split and transforming."""
    splits = DatasetSplitter.split(
        synthetic_pipeline_dataframe,
        target_column="career_role",
        test_size=0.2,
        random_state=42,
    )
    train_df = splits["train"]

    preprocessor = StudentProfilePreprocessor(
        numeric_cols=["academic_score", "python_skill", "sql_skill"],
        categorical_cols=["education_level"],
        scale_numeric=True,
    )
    X_train_proc = preprocessor.fit_transform(train_df, y=train_df["career_role"])

    assert preprocessor.is_fitted_ is True
    assert X_train_proc.isnull().sum().sum() == 0
    assert len(X_train_proc) == 40


def test_leakage_prevention_regression(synthetic_pipeline_dataframe):
    """Regression test ensuring test set transformation does NOT mutate fitted training state."""
    splits = DatasetSplitter.split(
        synthetic_pipeline_dataframe,
        target_column="career_role",
        test_size=0.2,
        random_state=42,
    )
    train_df, test_df = splits["train"], splits["test"]

    preprocessor = StudentProfilePreprocessor(
        numeric_cols=["academic_score", "python_skill"],
        categorical_cols=["education_level"],
    )
    preprocessor.fit(train_df)

    # Snapshot fitted parameters prior to transforming test set
    num_imputer_fitted_medians = preprocessor.column_transformer_.named_transformers_[
        "numeric"
    ].named_steps["imputer"].statistics_.copy()

    # Transform holdout test set
    _ = preprocessor.transform(test_df)

    # Verify fitted medians remained completely unchanged
    np.testing.assert_array_equal(
        num_imputer_fitted_medians,
        preprocessor.column_transformer_.named_transformers_["numeric"]
        .named_steps["imputer"]
        .statistics_,
    )


def test_artifact_manager_save_and_load_checksum(tmp_path, synthetic_pipeline_dataframe):
    """Test saving and loading fitted preprocessor artifact with SHA-256 validation."""
    preprocessor = StudentProfilePreprocessor(
        numeric_cols=["academic_score", "python_skill"],
        categorical_cols=["education_level"],
    )
    preprocessor.fit(synthetic_pipeline_dataframe)

    artifact_dir = tmp_path / "models"
    artifact_file = ArtifactManager.save_artifact(
        preprocessor,
        artifact_name="test_preprocessor",
        version="v1.0",
        target_dir=artifact_dir,
    )

    loaded_preprocessor, metadata = ArtifactManager.load_artifact(artifact_file)
    assert loaded_preprocessor.is_fitted_ is True
    assert metadata["artifact_name"] == "test_preprocessor"
    assert "sha256_checksum" in metadata

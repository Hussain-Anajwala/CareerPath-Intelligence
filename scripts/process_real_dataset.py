"""Script to process real raw dataset, apply feature engineering, execute train/test split, and save artifacts."""

import sys
sys.path.insert(0, 'src')

from pathlib import Path
import pandas as pd
import joblib

from careerpath.config.logging import logger
from careerpath.config.settings import settings
from careerpath.data.loaders import DataLoader
from careerpath.data.validators import DataValidator
from careerpath.data.schemas import DatasetSchemaConfig, RAW_TARGET_COL
from careerpath.ml.splitting import DatasetSplitter
from careerpath.ml.features import FeatureExtractor
from careerpath.ml.preprocessing import StudentProfilePreprocessor
from careerpath.ml.artifacts import ArtifactManager


def main():
    logger.info("Starting Phase 2 data pipeline on real dataset student_career_data.csv...")

    raw_file = settings.RAW_DATA_DIR / "student_career_data.csv"
    if not raw_file.exists():
        raise FileNotFoundError(f"Raw dataset not found at {raw_file}")

    # 1. Load Data
    df, sha256 = DataLoader.load_tabular_data(raw_file)

    # 2. Schema & Validation Gate
    schema_config = DatasetSchemaConfig()
    val_result = DataValidator.validate_schema(df, schema_config)
    if not val_result.is_valid:
        raise ValueError(f"Schema validation failed: {val_result.errors}")

    leakage_result = DataValidator.audit_leakage(df, target_column=RAW_TARGET_COL)
    if leakage_result.is_leakage_detected:
        logger.warning(f"Target leakage detected: {leakage_result.suspicious_columns}")

    # 3. Feature Engineering
    feature_extractor = FeatureExtractor()
    df_engineered = feature_extractor.fit_transform(df)

    # 4. Train / Test Split (80/20 Stratified)
    splits = DatasetSplitter.split(
        df_engineered,
        target_column=RAW_TARGET_COL,
        test_size=0.2,
        random_state=42,
        stratify=True,
    )
    train_df = splits["train"]
    test_df = splits["test"]

    X_train = train_df.drop(columns=[RAW_TARGET_COL])
    y_train = train_df[RAW_TARGET_COL]

    X_test = test_df.drop(columns=[RAW_TARGET_COL])
    y_test = test_df[RAW_TARGET_COL]

    # 5. Preprocessing (Fit on Train ONLY)
    preprocessor = StudentProfilePreprocessor(scale_numeric=True)
    X_train_proc = preprocessor.fit_transform(X_train, y=y_train)
    X_test_proc = preprocessor.transform(X_test)

    y_train_enc = preprocessor.transform_target(y_train)
    y_test_enc = preprocessor.transform_target(y_test)

    # 6. Save Processed Datasets
    processed_dir = settings.PROCESSED_DATA_DIR
    processed_dir.mkdir(parents=True, exist_ok=True)

    X_train_proc.to_csv(processed_dir / "X_train.csv", index=False)
    X_test_proc.to_csv(processed_dir / "X_test.csv", index=False)
    pd.Series(y_train_enc, name="target").to_csv(processed_dir / "y_train.csv", index=False)
    pd.Series(y_test_enc, name="target").to_csv(processed_dir / "y_test.csv", index=False)

    # 7. Save Pipeline & Preprocessor Artifact
    ArtifactManager.save_artifact(
        preprocessor,
        artifact_name="preprocessor",
        version="v1.0",
        metadata={
            "raw_dataset_sha256": sha256,
            "train_samples": len(X_train_proc),
            "test_samples": len(X_test_proc),
            "num_features": X_train_proc.shape[1],
            "target_classes": preprocessor.label_encoder_.classes_.tolist(),
        },
    )

    logger.info("Successfully completed Phase 2 pipeline execution!")
    logger.info(f"Processed features: {X_train_proc.shape[1]}")
    logger.info(f"Train samples: {len(X_train_proc)}, Test samples: {len(X_test_proc)}")


if __name__ == "__main__":
    main()

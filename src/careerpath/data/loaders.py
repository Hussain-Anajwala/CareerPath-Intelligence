"""Data loading utilities with integrity verification."""

import hashlib
from pathlib import Path
from typing import Tuple, Optional
import pandas as pd

from careerpath.config.logging import logger
from careerpath.config.settings import settings


class DataLoader:
    """Safe dataset loading utility with SHA-256 verification."""

    @staticmethod
    def calculate_sha256(file_path: Path) -> str:
        """Calculates SHA-256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @classmethod
    def load_tabular_data(
        cls, file_path: Path, expected_sha256: Optional[str] = None
    ) -> Tuple[pd.DataFrame, str]:
        """Loads CSV/Parquet dataset and returns (DataFrame, SHA256)."""
        if not file_path.exists():
            raise FileNotFoundError(f"Dataset file not found at: {file_path}")

        actual_sha256 = cls.calculate_sha256(file_path)

        if expected_sha256 and actual_sha256 != expected_sha256:
            raise ValueError(
                f"SHA-256 mismatch for {file_path}. Expected {expected_sha256}, got {actual_sha256}."
            )

        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            df = pd.read_csv(file_path)
        elif suffix in [".parquet", ".pq"]:
            df = pd.read_parquet(file_path)
        elif suffix == ".json":
            df = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format '{suffix}'. Expected CSV, Parquet, or JSON.")

        logger.info(
            f"Successfully loaded dataset from {file_path.name} ({len(df)} rows, {len(df.columns)} cols). SHA256: {actual_sha256[:8]}..."
        )

        return df, actual_sha256

    @classmethod
    def load_raw_student_dataset(cls) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """Attempts to load the raw student career dataset from data/raw/."""
        raw_dir = settings.RAW_DATA_DIR
        candidate_files = list(raw_dir.glob("*.csv")) + list(raw_dir.glob("*.parquet"))

        if not candidate_files:
            logger.warning(f"No raw dataset files found in {raw_dir}")
            return None, None

        primary_file = candidate_files[0]
        return cls.load_tabular_data(primary_file)

"""Unit tests for dataset validation, schema checking, and target leakage auditing."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from careerpath.data.schemas import (
    StudentProfileInput,
    DatasetSchemaConfig,
    ValidationResult,
    LeakageAuditResult,
)
from careerpath.data.validators import DataValidator
from careerpath.data.loaders import DataLoader


@pytest.fixture
def sample_student_dataframe():
    """Fixture providing a mock student profile dataset for testing."""
    np.random.seed(42)
    return pd.DataFrame(
        {
            "student_id": [f"S{i:03d}" for i in range(1, 21)],
            "academic_score": np.random.uniform(6.0, 9.5, 20).round(2),
            "python_skill": np.random.randint(1, 10, 20),
            "sql_skill": np.random.randint(1, 10, 20),
            "analytics_interest": np.random.choice([0, 1], 20),
            "career_role": np.random.choice(
                ["Data Analyst", "Software Engineer", "Data Scientist"], 20
            ),
        }
    )


def test_student_profile_input_valid():
    """Test Pydantic student profile validation with valid values."""
    profile = StudentProfileInput(
        academic_score=8.5,
        skills=["Python", "SQL"],
        interests=["analytics"],
    )
    assert profile.academic_score == 8.5
    assert "Python" in profile.skills


def test_student_profile_input_invalid_score():
    """Test Pydantic student profile validation with out-of-range academic score."""
    with pytest.raises(ValueError, match="academic_score must be between"):
        StudentProfileInput(academic_score=150.0)


def test_data_validator_schema_valid(sample_student_dataframe):
    """Test dataset schema validation on valid DataFrame."""
    config = DatasetSchemaConfig(
        required_columns=["student_id", "academic_score", "python_skill"],
        target_column="career_role",
        min_rows=5,
    )
    result = DataValidator.validate_schema(sample_student_dataframe, config)
    assert result.is_valid is True
    assert len(result.missing_columns) == 0
    assert result.total_rows == 20
    assert result.total_columns == 6


def test_data_validator_schema_missing_column(sample_student_dataframe):
    """Test dataset schema validation when required column is missing."""
    config = DatasetSchemaConfig(
        required_columns=["non_existent_column"],
        min_rows=5,
    )
    result = DataValidator.validate_schema(sample_student_dataframe, config)
    assert result.is_valid is False
    assert "non_existent_column" in result.missing_columns


def test_data_validator_target_audit(sample_student_dataframe):
    """Test target audit calculation."""
    audit = DataValidator.audit_target(sample_student_dataframe, "career_role")
    assert audit["target_column"] == "career_role"
    assert audit["total_samples"] == 20
    assert audit["unique_classes"] == 3
    assert audit["missing_count"] == 0


def test_data_validator_leakage_audit(sample_student_dataframe):
    """Test target leakage detection."""
    # Add a suspicious target-derived column
    df = sample_student_dataframe.copy()
    df["hired_career_label"] = df["career_role"]

    result = DataValidator.audit_leakage(df, target_column="career_role")
    assert result.is_leakage_detected is True
    assert "hired_career_label" in result.suspicious_columns


def test_data_validator_duplicate_detection(sample_student_dataframe):
    """Test exact duplicate row detection."""
    df = sample_student_dataframe.copy()
    # Duplicate first row
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    res = DataValidator.detect_duplicates(df)
    assert res["duplicate_count"] == 1
    assert res["total_rows"] == 21


def test_data_loader_sha256(tmp_path):
    """Test data loader SHA-256 calculation."""
    test_file = tmp_path / "test.csv"
    test_file.write_text("a,b,c\n1,2,3\n")

    sha256 = DataLoader.calculate_sha256(test_file)
    assert isinstance(sha256, str)
    assert len(sha256) == 64

    df, loaded_sha256 = DataLoader.load_tabular_data(test_file)
    assert len(df) == 1
    assert loaded_sha256 == sha256

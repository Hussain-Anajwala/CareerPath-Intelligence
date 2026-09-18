"""Data schemas and Pydantic validation models reconciled with real dataset."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


RAW_NUMERIC_COLS = [
    "Logical quotient rating",
    "hackathons",
    "coding skills rating",
    "public speaking points",
]

RAW_CATEGORICAL_COLS = [
    "self-learning capability?",
    "Extra-courses did",
    "certifications",
    "workshops",
    "reading and writing skills",
    "memory capability score",
    "Interested subjects",
    "interested career area ",
    "Type of company want to settle in?",
    "Taken inputs from seniors or elders",
    "Interested Type of Books",
    "Management or Technical",
    "hard/smart worker",
    "worked in teams ever?",
    "Introvert",
]

RAW_TARGET_COL = "Suggested Job Role"


class StudentProfileInput(BaseModel):
    """Pydantic model for validating student profile inputs."""

    academic_score: Optional[float] = Field(
        default=None,
        description="Academic score or CGPA (0.0 to 100.0 or 0.0 to 10.0)",
    )
    education_level: Optional[str] = Field(
        default="undergraduate",
        description="Current education level",
    )
    skills: List[str] = Field(
        default_factory=list,
        description="List of self-reported user skills",
    )
    interests: List[str] = Field(
        default_factory=list,
        description="List of domain interests or preferences",
    )
    preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional non-sensitive user preferences",
    )

    @field_validator("academic_score")
    @classmethod
    def validate_academic_score(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and (v < 0.0 or v > 100.0):
            raise ValueError("academic_score must be between 0.0 and 100.0")
        return v


class DatasetSchemaConfig(BaseModel):
    """Configuration defining expected tabular dataset schema."""

    required_columns: List[str] = Field(
        default_factory=lambda: RAW_NUMERIC_COLS + RAW_CATEGORICAL_COLS
    )
    numeric_columns: List[str] = Field(default_factory=lambda: RAW_NUMERIC_COLS)
    categorical_columns: List[str] = Field(default_factory=lambda: RAW_CATEGORICAL_COLS)
    target_column: Optional[str] = Field(default=RAW_TARGET_COL)
    min_rows: int = Field(default=10)


class ValidationResult(BaseModel):
    """Outcome of dataset validation."""

    is_valid: bool
    total_rows: int = 0
    total_columns: int = 0
    missing_columns: List[str] = Field(default_factory=list)
    duplicate_rows: int = 0
    missing_value_summary: Dict[str, float] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class LeakageAuditResult(BaseModel):
    """Outcome of target leakage audit."""

    is_leakage_detected: bool
    suspicious_columns: List[str] = Field(default_factory=list)
    findings: List[Dict[str, str]] = Field(default_factory=list)

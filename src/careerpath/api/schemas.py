"""Pydantic v2 schemas for FastAPI service layer requests and responses."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """Health check endpoint response schema."""

    status: str = "ok"
    version: str = "1.0.0"
    model_loaded: bool = True
    esco_loaded: bool = True


class StudentProfileSchema(BaseModel):
    """Raw student profile attributes schema."""

    model_config = ConfigDict(populate_by_name=True)

    database_fundamentals: float = Field(default=5.0, ge=0.0, le=10.0, alias="Database Fundamentals")
    computer_networks: float = Field(default=5.0, ge=0.0, le=10.0, alias="Computer Networks")
    software_engineering: float = Field(default=5.0, ge=0.0, le=10.0, alias="Software Engineering")
    cyber_security: float = Field(default=5.0, ge=0.0, le=10.0, alias="Cyber Security")
    coding_skills: float = Field(default=5.0, ge=0.0, le=10.0, alias="Coding Skills")
    web_development: float = Field(default=5.0, ge=0.0, le=10.0, alias="Web Development")
    software_testing: float = Field(default=5.0, ge=0.0, le=10.0, alias="Software Testing")
    technical_support: float = Field(default=5.0, ge=0.0, le=10.0, alias="Technical Support")
    certifications: Optional[str] = Field(default="", description="Comma-separated or text certifications")
    interested_subjects: Optional[str] = Field(default="", description="Interested subjects or domain areas")


class RecommendRequest(BaseModel):
    """Request payload for career recommendations."""

    profile: StudentProfileSchema
    top_k: int = Field(default=5, ge=1, le=12)
    alpha: float = Field(default=0.5, ge=0.0, le=1.0, description="Fusion weight (ML vs ESCO)")


class CareerRecommendationSchema(BaseModel):
    """Decomposable career recommendation output schema."""

    career_role: str
    esco_occupation_uri: str
    esco_occupation_title: str
    final_score: float
    raw_ml_probability: float
    normalized_ml_score: float
    esco_score: float
    alpha: float
    matched_skills: List[Dict[str, Any]]
    partial_matches: List[Dict[str, Any]]
    missing_skills: List[Dict[str, Any]]


class RecommendResponse(BaseModel):
    """Response payload for career recommendations."""

    recommendations: List[CareerRecommendationSchema]
    num_recommendations: int
    execution_time_ms: float


class SkillGapRequest(BaseModel):
    """Request payload for target career skill gap analysis."""

    profile: StudentProfileSchema
    target_career_role: str = Field(..., json_schema_extra={"example": "Network Security Engineer"})


class SkillGapResponse(BaseModel):
    """Response payload for skill gap analysis."""

    target_career_role: str
    esco_occupation_uri: str
    total_required_skills: int
    coverage_score: float
    average_similarity: float
    matched_skills: List[Dict[str, Any]]
    partial_matches: List[Dict[str, Any]]
    missing_skills: List[Dict[str, Any]]


class WhatIfRequest(BaseModel):
    """Request payload for counterfactual skill acquisition simulation."""

    profile: StudentProfileSchema
    skill_modifications: Dict[str, float] = Field(
        ...,
        json_schema_extra={"example": {"Database Fundamentals": 9.5, "Cyber Security": 9.0}},
        description="Modified skill ratings to simulate",
    )
    top_k: int = Field(default=5, ge=1, le=12)


class WhatIfResponse(BaseModel):
    """Response payload for What-If simulation."""

    skills_modified: Dict[str, float]
    baseline_top_recommendation: str
    scenario_top_recommendation: str
    baseline_recommendations: List[CareerRecommendationSchema]
    scenario_recommendations: List[CareerRecommendationSchema]
    rank_changes: List[Dict[str, Any]]
    reduced_skill_gaps: List[Dict[str, Any]]

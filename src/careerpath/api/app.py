"""FastAPI application providing production REST endpoints for recommendations, skill gap analysis, and What-If simulations."""

import time
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from careerpath.config.logging import logger
from careerpath.config.settings import settings
from careerpath.ml.artifacts import ArtifactManager
from careerpath.esco import (
    ESCOTaxonomy,
    CareerMapper,
    SkillNormalizer,
    ESCOVectorIndex,
    SkillGapEngine,
    HybridRecommender,
)
from careerpath.esco.whatif import WhatIfEngine
from careerpath.api.schemas import (
    HealthResponse,
    RecommendRequest,
    RecommendResponse,
    CareerRecommendationSchema,
    SkillGapRequest,
    SkillGapResponse,
    WhatIfRequest,
    WhatIfResponse,
)

# Global singleton components loaded during startup
app_state: Dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan manager loading preprocessors, models, and ESCO vector index once on startup."""
    logger.info("Initializing CareerPath Intelligence API Service Layer...")

    try:
        # 1. Load Preprocessor
        preprocessor_file = settings.MODELS_DIR / "preprocessor" / "v1.0" / "preprocessor.joblib"
        preprocessor, pre_meta = ArtifactManager.load_artifact(preprocessor_file)
        target_classes = pre_meta.get("user_metadata", {}).get("target_classes", [])
        feature_names = pre_meta.get("user_metadata", {}).get("feature_names", [])

        # 2. Load ML Candidate Model (CatBoost or Random Forest)
        cat_file = settings.MODELS_DIR / "advanced_catboost" / "v1.0" / "advanced_catboost.joblib"
        if cat_file.exists():
            ml_model, _ = ArtifactManager.load_artifact(cat_file)
        else:
            rf_file = settings.MODELS_DIR / "baseline_random_forest" / "v1.0" / "baseline_random_forest.joblib"
            ml_model, _ = ArtifactManager.load_artifact(rf_file)

        # 3. Load ESCO Taxonomy & Vector Index
        taxonomy = ESCOTaxonomy()
        mapper = CareerMapper(taxonomy=taxonomy)
        vector_index = ESCOVectorIndex(taxonomy=taxonomy)
        vector_index.build_skill_index()

        gap_engine = SkillGapEngine(taxonomy=taxonomy, vector_index=vector_index)
        recommender = HybridRecommender(
            ml_model=ml_model,
            target_classes=target_classes,
            taxonomy=taxonomy,
            mapper=mapper,
            gap_engine=gap_engine,
            alpha=0.5,
        )
        whatif_engine = WhatIfEngine(recommender=recommender)

        app_state["preprocessor"] = preprocessor
        app_state["ml_model"] = ml_model
        app_state["target_classes"] = target_classes
        app_state["feature_names"] = feature_names
        app_state["taxonomy"] = taxonomy
        app_state["mapper"] = mapper
        app_state["recommender"] = recommender
        app_state["whatif_engine"] = whatif_engine
        app_state["gap_engine"] = gap_engine
        app_state["is_ready"] = True

        logger.info("CareerPath Intelligence API dependencies successfully loaded and ready.")
    except Exception as e:
        logger.error(f"Failed to initialize API dependencies: {e}")
        app_state["is_ready"] = False

    yield

    logger.info("Shutting down CareerPath Intelligence API Service...")
    app_state.clear()


app = FastAPI(
    title="CareerPath Intelligence API",
    description="Explainable ML Career Decision Support & Skill-Gap Analysis Platform REST API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Enable CORS for local web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Handles Pydantic payload validation errors with 422 Unprocessable Entity."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Request payload validation failed", "errors": exc.errors()},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handles explicit HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catches unhandled internal server exceptions safely without leaking tracebacks."""
    logger.error(f"Unhandled internal server error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred while processing the request."},
    )


def _convert_profile_to_feature_sample(profile_dict: Dict[str, Any]) -> pd.DataFrame:
    """Helper converting raw profile dictionary to 1-row DataFrame aligned with trained preprocessor."""
    feature_names = app_state.get("feature_names", [])

    # Map raw numeric features
    raw_input = {
        "Database Fundamentals": float(profile_dict.get("Database Fundamentals", 5.0)),
        "Computer Networks": float(profile_dict.get("Computer Networks", 5.0)),
        "Software Engineering": float(profile_dict.get("Software Engineering", 5.0)),
        "Cyber Security": float(profile_dict.get("Cyber Security", 5.0)),
        "Coding Skills": float(profile_dict.get("Coding Skills", 5.0)),
        "Web Development": float(profile_dict.get("Web Development", 5.0)),
        "Software Testing": float(profile_dict.get("Software Testing", 5.0)),
        "Technical Support": float(profile_dict.get("Technical Support", 5.0)),
    }

    # Transform raw input using fitted preprocessor if available
    preprocessor = app_state.get("preprocessor")
    if preprocessor and hasattr(preprocessor, "transform"):
        input_df = pd.DataFrame([raw_input])
        for col in preprocessor.numeric_cols:
            if col not in input_df.columns:
                input_df[col] = 5.0
        for col in preprocessor.categorical_cols:
            if col not in input_df.columns:
                input_df[col] = "Unknown"
        return preprocessor.transform(input_df)

    # Fallback to constructing zero-filled DataFrame with feature_names
    sample_data = {col: 0.0 for col in feature_names}
    for col, val in raw_input.items():
        if col in sample_data:
            sample_data[col] = val
    return pd.DataFrame([sample_data])


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint confirming API service status and dependency loading."""
    is_ready = app_state.get("is_ready", False)
    if not is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API services are initializing or encountered startup errors.",
        )
    return HealthResponse(
        status="ok",
        version="1.0.0",
        model_loaded=bool(app_state.get("ml_model")),
        esco_loaded=bool(app_state.get("taxonomy")),
    )


@app.post("/api/v1/recommend", response_model=RecommendResponse, tags=["Recommendations"])
async def generate_career_recommendations(payload: RecommendRequest):
    """Generates ranked hybrid career recommendations with complete evidence breakdown."""
    if not app_state.get("is_ready"):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="API not ready.")

    start_t = time.perf_counter()
    profile_dict = payload.profile.model_dump(by_alias=True)

    X_sample = _convert_profile_to_feature_sample(profile_dict)
    recommender: HybridRecommender = app_state["recommender"]

    recs = recommender.recommend_for_profile(
        X_sample=X_sample,
        profile_dict=profile_dict,
        top_k=payload.top_k,
        alpha_override=payload.alpha,
    )

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    rec_schemas = [
        CareerRecommendationSchema(
            career_role=r.career_role,
            esco_occupation_uri=r.esco_occupation_uri,
            esco_occupation_title=r.esco_occupation_title,
            final_score=r.final_score,
            raw_ml_probability=r.raw_ml_probability,
            normalized_ml_score=r.normalized_ml_score,
            esco_score=r.esco_score,
            alpha=r.alpha,
            matched_skills=r.matched_skills,
            partial_matches=r.partial_matches,
            missing_skills=r.missing_skills,
        )
        for r in recs
    ]

    return RecommendResponse(
        recommendations=rec_schemas,
        num_recommendations=len(rec_schemas),
        execution_time_ms=round(elapsed_ms, 2),
    )


@app.post("/api/v1/skill-gap", response_model=SkillGapResponse, tags=["Skill Gap Analysis"])
async def evaluate_target_skill_gap(payload: SkillGapRequest):
    """Evaluates skill gap analysis for a specific target career role."""
    if not app_state.get("is_ready"):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="API not ready.")

    mapper: CareerMapper = app_state["mapper"]
    gap_engine: SkillGapEngine = app_state["gap_engine"]

    mapping = mapper.get_mapping(payload.target_career_role)
    if not mapping or mapping.mapping_status == "UNRESOLVED":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target career role '{payload.target_career_role}' could not be resolved to an ESCO occupation.",
        )

    profile_dict = payload.profile.model_dump(by_alias=True)
    student_skills = SkillNormalizer.normalize_student_profile(profile_dict)

    gap_report = gap_engine.evaluate_gap(student_skills, mapping.esco_occupation_uri)

    matched = [
        {"skill": m.required_skill_label, "similarity": m.similarity_score, "evidence": m.evidence_source}
        for m in gap_report.matched_skills
    ]
    partial = [
        {"skill": m.required_skill_label, "similarity": m.similarity_score, "evidence": m.evidence_source}
        for m in gap_report.partial_matches
    ]
    missing = [
        {"skill": m.required_skill_label, "similarity": m.similarity_score}
        for m in gap_report.missing_skills
    ]

    return SkillGapResponse(
        target_career_role=payload.target_career_role,
        esco_occupation_uri=mapping.esco_occupation_uri,
        total_required_skills=gap_report.total_required_skills,
        coverage_score=gap_report.coverage_score,
        average_similarity=gap_report.average_similarity,
        matched_skills=matched,
        partial_matches=partial,
        missing_skills=missing,
    )


@app.post("/api/v1/what-if", response_model=WhatIfResponse, tags=["What-If Simulation"])
async def simulate_what_if_scenario(payload: WhatIfRequest):
    """Simulates counterfactual skill acquisition and compares baseline vs scenario recommendations."""
    if not app_state.get("is_ready"):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="API not ready.")

    whatif_engine: WhatIfEngine = app_state["whatif_engine"]
    profile_dict = payload.profile.model_dump(by_alias=True)
    X_sample = _convert_profile_to_feature_sample(profile_dict)

    sim_res = whatif_engine.simulate_skill_acquisition(
        X_sample=X_sample,
        baseline_profile=profile_dict,
        skill_modifications=payload.skill_modifications,
        top_k=payload.top_k,
    )

    base_schemas = [
        CareerRecommendationSchema(
            career_role=r.career_role,
            esco_occupation_uri=r.esco_occupation_uri,
            esco_occupation_title=r.esco_occupation_title,
            final_score=r.final_score,
            raw_ml_probability=r.raw_ml_probability,
            normalized_ml_score=r.normalized_ml_score,
            esco_score=r.esco_score,
            alpha=r.alpha,
            matched_skills=r.matched_skills,
            partial_matches=r.partial_matches,
            missing_skills=r.missing_skills,
        )
        for r in sim_res.baseline_recommendations
    ]

    scen_schemas = [
        CareerRecommendationSchema(
            career_role=r.career_role,
            esco_occupation_uri=r.esco_occupation_uri,
            esco_occupation_title=r.esco_occupation_title,
            final_score=r.final_score,
            raw_ml_probability=r.raw_ml_probability,
            normalized_ml_score=r.normalized_ml_score,
            esco_score=r.esco_score,
            alpha=r.alpha,
            matched_skills=r.matched_skills,
            partial_matches=r.partial_matches,
            missing_skills=r.missing_skills,
        )
        for r in sim_res.scenario_recommendations
    ]

    rank_change_dicts = [
        {
            "career_role": rc.career_role,
            "baseline_rank": rc.baseline_rank,
            "scenario_rank": rc.scenario_rank,
            "rank_delta": rc.rank_delta,
            "baseline_score": rc.baseline_score,
            "scenario_score": rc.scenario_score,
            "score_delta": rc.score_delta,
        }
        for rc in sim_res.rank_changes[: payload.top_k]
    ]

    return WhatIfResponse(
        skills_modified=sim_res.skills_modified,
        baseline_top_recommendation=base_schemas[0].career_role if base_schemas else "N/A",
        scenario_top_recommendation=scen_schemas[0].career_role if scen_schemas else "N/A",
        baseline_recommendations=base_schemas,
        scenario_recommendations=scen_schemas,
        rank_changes=rank_change_dicts,
        reduced_skill_gaps=sim_res.reduced_skill_gaps,
    )

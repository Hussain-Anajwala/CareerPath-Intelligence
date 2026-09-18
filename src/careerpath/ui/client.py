"""UI API Client for CareerPath Intelligence.

Supports HTTP requests to FastAPI service layer with fallback to direct Python backend
service layer if API is offline or standalone local execution is preferred.
"""

import os
import requests
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple

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

DEFAULT_API_URL = os.getenv("CAREERPATH_API_URL", "http://127.0.0.1:8000")


class ServiceClient:
    """Unified client for UI -> Backend communications."""

    def __init__(self, api_url: str = DEFAULT_API_URL):
        self.api_url = api_url.rstrip("/")
        self._local_backend: Optional[Dict[str, Any]] = None

    def check_api_health(self) -> Tuple[bool, str]:
        """Check if HTTP API server is online and ready."""
        try:
            resp = requests.get(f"{self.api_url}/health", timeout=1.5)
            if resp.status_code == 200:
                data = resp.json()
                return True, f"FastAPI Connected ({data.get('version', '1.0.0')})"
            return False, f"API returned status {resp.status_code}"
        except Exception as e:
            return False, "FastAPI Offline (Fallback to Local Engine)"

    def _ensure_local_backend(self):
        """Lazy-loads local python components as fallback when HTTP API server is unreachable."""
        if self._local_backend is not None:
            return

        logger.info("Initializing local Python backend engine fallback for UI...")
        try:
            preprocessor_file = settings.MODELS_DIR / "preprocessor" / "v1.0" / "preprocessor.joblib"
            preprocessor, pre_meta = ArtifactManager.load_artifact(preprocessor_file)
            target_classes = pre_meta.get("user_metadata", {}).get("target_classes", [])
            feature_names = pre_meta.get("user_metadata", {}).get("feature_names", [])

            cat_file = settings.MODELS_DIR / "advanced_catboost" / "v1.0" / "advanced_catboost.joblib"
            if cat_file.exists():
                ml_model, _ = ArtifactManager.load_artifact(cat_file)
            else:
                rf_file = settings.MODELS_DIR / "baseline_random_forest" / "v1.0" / "baseline_random_forest.joblib"
                ml_model, _ = ArtifactManager.load_artifact(rf_file)

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

            self._local_backend = {
                "preprocessor": preprocessor,
                "ml_model": ml_model,
                "target_classes": target_classes,
                "feature_names": feature_names,
                "taxonomy": taxonomy,
                "mapper": mapper,
                "recommender": recommender,
                "whatif_engine": whatif_engine,
                "gap_engine": gap_engine,
            }
            logger.info("Local Python backend engine successfully initialized for UI.")
        except Exception as e:
            logger.error(f"Failed to initialize local backend engine: {e}")
            raise RuntimeError(f"Could not initialize fallback engine: {e}")

    def _convert_profile_to_feature_sample(self, profile_dict: Dict[str, Any]) -> pd.DataFrame:
        """Helper converting raw profile to preprocessed DataFrame."""
        self._ensure_local_backend()
        feature_names = self._local_backend.get("feature_names", [])
        preprocessor = self._local_backend.get("preprocessor")

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

        if preprocessor and hasattr(preprocessor, "transform"):
            input_df = pd.DataFrame([raw_input])
            for col in preprocessor.numeric_cols:
                if col not in input_df.columns:
                    input_df[col] = 5.0
            for col in preprocessor.categorical_cols:
                if col not in input_df.columns:
                    input_df[col] = "Unknown"
            return preprocessor.transform(input_df)

        sample_data = {col: 0.0 for col in feature_names}
        for col, val in raw_input.items():
            if col in sample_data:
                sample_data[col] = val
        return pd.DataFrame([sample_data])

    def get_recommendations(
        self, profile_dict: Dict[str, Any], top_k: int = 5, alpha: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Fetch career recommendations via HTTP API or local engine fallback."""
        payload = {
            "profile": profile_dict,
            "top_k": top_k,
            "alpha": alpha,
        }
        try:
            resp = requests.post(f"{self.api_url}/api/v1/recommend", json=payload, timeout=5.0)
            if resp.status_code == 200:
                return resp.json().get("recommendations", [])
        except Exception:
            pass

        # Fallback to local engine
        self._ensure_local_backend()
        recommender: HybridRecommender = self._local_backend["recommender"]
        X_sample = self._convert_profile_to_feature_sample(profile_dict)
        recs = recommender.recommend_for_profile(
            X_sample=X_sample,
            profile_dict=profile_dict,
            top_k=top_k,
            alpha_override=alpha,
        )
        return [
            {
                "career_role": r.career_role,
                "esco_occupation_uri": r.esco_occupation_uri,
                "esco_occupation_title": r.esco_occupation_title,
                "final_score": r.final_score,
                "raw_ml_probability": r.raw_ml_probability,
                "normalized_ml_score": r.normalized_ml_score,
                "esco_score": r.esco_score,
                "alpha": r.alpha,
                "matched_skills": r.matched_skills,
                "partial_matches": r.partial_matches,
                "missing_skills": r.missing_skills,
            }
            for r in recs
        ]

    def get_skill_gap(self, profile_dict: Dict[str, Any], target_career_role: str) -> Dict[str, Any]:
        """Fetch skill gap analysis via HTTP API or local engine fallback."""
        payload = {
            "profile": profile_dict,
            "target_career_role": target_career_role,
        }
        try:
            resp = requests.post(f"{self.api_url}/api/v1/skill-gap", json=payload, timeout=5.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        # Fallback to local engine
        self._ensure_local_backend()
        mapper: CareerMapper = self._local_backend["mapper"]
        gap_engine: SkillGapEngine = self._local_backend["gap_engine"]

        mapping = mapper.get_mapping(target_career_role)
        if not mapping or mapping.mapping_status == "UNRESOLVED":
            raise ValueError(f"Target career role '{target_career_role}' could not be resolved to ESCO occupation.")

        student_skills = SkillNormalizer.normalize_student_profile(profile_dict)
        gap_report = gap_engine.evaluate_gap(student_skills, mapping.esco_occupation_uri)

        return {
            "target_career_role": target_career_role,
            "esco_occupation_uri": mapping.esco_occupation_uri,
            "total_required_skills": gap_report.total_required_skills,
            "coverage_score": gap_report.coverage_score,
            "average_similarity": gap_report.average_similarity,
            "matched_skills": [
                {"skill": m.required_skill_label, "similarity": m.similarity_score, "evidence": m.evidence_source}
                for m in gap_report.matched_skills
            ],
            "partial_matches": [
                {"skill": m.required_skill_label, "similarity": m.similarity_score, "evidence": m.evidence_source}
                for m in gap_report.partial_matches
            ],
            "missing_skills": [
                {"skill": m.required_skill_label, "similarity": m.similarity_score}
                for m in gap_report.missing_skills
            ],
        }

    def simulate_what_if(
        self, profile_dict: Dict[str, Any], skill_modifications: Dict[str, float], top_k: int = 5
    ) -> Dict[str, Any]:
        """Run What-If simulation via HTTP API or local engine fallback."""
        payload = {
            "profile": profile_dict,
            "skill_modifications": skill_modifications,
            "top_k": top_k,
        }
        try:
            resp = requests.post(f"{self.api_url}/api/v1/what-if", json=payload, timeout=5.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        # Fallback to local engine
        self._ensure_local_backend()
        whatif_engine: WhatIfEngine = self._local_backend["whatif_engine"]
        X_sample = self._convert_profile_to_feature_sample(profile_dict)

        sim_res = whatif_engine.simulate_skill_acquisition(
            X_sample=X_sample,
            baseline_profile=profile_dict,
            skill_modifications=skill_modifications,
            top_k=top_k,
        )

        def _format_recs(recs):
            return [
                {
                    "career_role": r.career_role,
                    "esco_occupation_uri": r.esco_occupation_uri,
                    "esco_occupation_title": r.esco_occupation_title,
                    "final_score": r.final_score,
                    "raw_ml_probability": r.raw_ml_probability,
                    "normalized_ml_score": r.normalized_ml_score,
                    "esco_score": r.esco_score,
                    "alpha": r.alpha,
                    "matched_skills": r.matched_skills,
                    "partial_matches": r.partial_matches,
                    "missing_skills": r.missing_skills,
                }
                for r in recs
            ]

        base_recs = _format_recs(sim_res.baseline_recommendations)
        scen_recs = _format_recs(sim_res.scenario_recommendations)

        return {
            "skills_modified": sim_res.skills_modified,
            "baseline_top_recommendation": base_recs[0]["career_role"] if base_recs else "N/A",
            "scenario_top_recommendation": scen_recs[0]["career_role"] if scen_recs else "N/A",
            "baseline_recommendations": base_recs,
            "scenario_recommendations": scen_recs,
            "rank_changes": [
                {
                    "career_role": rc.career_role,
                    "baseline_rank": rc.baseline_rank,
                    "scenario_rank": rc.scenario_rank,
                    "rank_delta": rc.rank_delta,
                    "baseline_score": rc.baseline_score,
                    "scenario_score": rc.scenario_score,
                    "score_delta": rc.score_delta,
                }
                for rc in sim_res.rank_changes[:top_k]
            ],
            "reduced_skill_gaps": sim_res.reduced_skill_gaps,
        }

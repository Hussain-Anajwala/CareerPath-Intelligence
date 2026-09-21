"""Hybrid recommendation engine fusing normalized supervised ML probabilities and ESCO skill gap scores."""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd

from careerpath.config.logging import logger
from careerpath.esco.taxonomy import ESCOTaxonomy
from careerpath.esco.mapping import CareerMapper
from careerpath.esco.normalization import SkillNormalizer, DemonstratedSkill
from careerpath.esco.gap_engine import SkillGapEngine, SkillGapReport


@dataclass
class CareerRecommendation:
    """Decomposable explainable career recommendation output."""

    career_role: str
    esco_occupation_uri: str
    esco_occupation_title: str
    final_score: float
    raw_ml_probability: float
    normalized_ml_score: float
    esco_score: float
    alpha: float
    skill_gap_report: Dict[str, Any]
    matched_skills: List[Dict[str, Any]] = field(default_factory=list)
    partial_matches: List[Dict[str, Any]] = field(default_factory=list)
    missing_skills: List[Dict[str, Any]] = field(default_factory=list)


class HybridRecommender:
    """Fuses normalized supervised ML class probabilities with taxonomy-backed ESCO skill scores.
    
    Formula:
        P_ML_norm(k) = P_ML(k) / max_j(P_ML(j))
        S_final(k) = alpha * P_ML_norm(k) + (1 - alpha) * S_ESCO(k)
    """

    def __init__(
        self,
        ml_model: Any,
        target_classes: List[str],
        taxonomy: Optional[ESCOTaxonomy] = None,
        mapper: Optional[CareerMapper] = None,
        gap_engine: Optional[SkillGapEngine] = None,
        alpha: float = 1.0,
    ):
        self.ml_model = ml_model
        self.target_classes = target_classes
        self.taxonomy = taxonomy or ESCOTaxonomy()
        self.mapper = mapper or CareerMapper(taxonomy=self.taxonomy)
        self.gap_engine = gap_engine or SkillGapEngine(taxonomy=self.taxonomy)
        self.alpha = alpha

    def calculate_esco_score(self, gap_report: SkillGapReport) -> float:
        """Computes composite ESCO alignment score from skill coverage and similarity."""
        if gap_report.total_required_skills == 0:
            return 0.0
        return round(0.6 * gap_report.coverage_score + 0.4 * gap_report.average_similarity, 4)

    def recommend_for_profile(
        self,
        X_sample: pd.DataFrame,
        profile_dict: Dict[str, Any],
        top_k: int = 5,
        alpha_override: Optional[float] = None,
    ) -> List[CareerRecommendation]:
        """Generates ranked hybrid career recommendations with complete evidence breakdown."""
        eff_alpha = alpha_override if alpha_override is not None else self.alpha

        if hasattr(self.ml_model, "predict_proba"):
            raw_ml_probs = self.ml_model.predict_proba(X_sample)[0]
        else:
            raw_ml_probs = np.ones(len(self.target_classes)) / len(self.target_classes)

        # Normalize ML probabilities to [0.0, 1.0] scale relative to max class probability
        max_p = np.max(raw_ml_probs) if np.max(raw_ml_probs) > 0 else 1.0
        norm_ml_scores = raw_ml_probs / max_p

        student_skills = SkillNormalizer.normalize_student_profile(profile_dict)

        recommendations: List[CareerRecommendation] = []

        for i, class_name in enumerate(self.target_classes):
            raw_p = float(raw_ml_probs[i]) if i < len(raw_ml_probs) else 0.0
            norm_p = float(norm_ml_scores[i]) if i < len(norm_ml_scores) else 0.0

            mapping_entry = self.mapper.get_mapping(class_name)
            esco_uri = mapping_entry.esco_occupation_uri if mapping_entry else ""

            esco_score = 0.0
            gap_dict = {}
            matched_dicts = []
            partial_dicts = []
            missing_dicts = []

            if esco_uri:
                gap_report = self.gap_engine.evaluate_gap(student_skills, esco_uri)
                esco_score = self.calculate_esco_score(gap_report)

                gap_dict = {
                    "total_required": gap_report.total_required_skills,
                    "coverage_score": gap_report.coverage_score,
                    "average_similarity": gap_report.average_similarity,
                }

                matched_dicts = [
                    {
                        "skill": m.required_skill_label,
                        "similarity": m.similarity_score,
                        "evidence": m.evidence_source,
                    }
                    for m in gap_report.matched_skills
                ]
                partial_dicts = [
                    {
                        "skill": m.required_skill_label,
                        "similarity": m.similarity_score,
                        "evidence": m.evidence_source,
                    }
                    for m in gap_report.partial_matches
                ]
                missing_dicts = [
                    {
                        "skill": m.required_skill_label,
                        "similarity": m.similarity_score,
                    }
                    for m in gap_report.missing_skills
                ]

            final_score = round(eff_alpha * norm_p + (1.0 - eff_alpha) * esco_score, 4)

            recommendations.append(
                CareerRecommendation(
                    career_role=class_name,
                    esco_occupation_uri=esco_uri,
                    esco_occupation_title=mapping_entry.esco_preferred_label if mapping_entry else class_name,
                    final_score=final_score,
                    raw_ml_probability=round(raw_p, 4),
                    normalized_ml_score=round(norm_p, 4),
                    esco_score=esco_score,
                    alpha=eff_alpha,
                    skill_gap_report=gap_dict,
                    matched_skills=matched_dicts,
                    partial_matches=partial_dicts,
                    missing_skills=missing_dicts,
                )
            )

        recommendations.sort(key=lambda rec: rec.final_score, reverse=True)
        return recommendations[:top_k]

    def run_ablation_study(
        self,
        X_eval: pd.DataFrame,
        eval_profiles: List[Dict[str, Any]],
        y_eval: np.ndarray,
        alphas: List[float] = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    ) -> pd.DataFrame:
        """Executes fast ablation study across fusion weights alpha on a validation set."""
        num_samples = len(X_eval)
        if hasattr(self.ml_model, "predict_proba"):
            all_raw_p = self.ml_model.predict_proba(X_eval)
        else:
            all_raw_p = np.ones((num_samples, len(self.target_classes))) / len(self.target_classes)

        # Precalculate normalized ML scores (each row scaled by its max probability)
        all_norm_p = np.zeros_like(all_raw_p)
        for idx in range(num_samples):
            max_p = np.max(all_raw_p[idx])
            if max_p > 0:
                all_norm_p[idx] = all_raw_p[idx] / max_p
            else:
                all_norm_p[idx] = all_raw_p[idx]

        # Precompute ESCO scores ONCE for all samples and classes
        esco_scores_matrix = np.zeros((num_samples, len(self.target_classes)))
        for idx in range(num_samples):
            prof = eval_profiles[idx] if idx < len(eval_profiles) else {}
            student_skills = SkillNormalizer.normalize_student_profile(prof)

            for c_idx, class_name in enumerate(self.target_classes):
                mapping_entry = self.mapper.get_mapping(class_name)
                esco_uri = mapping_entry.esco_occupation_uri if mapping_entry else ""
                if esco_uri:
                    gap_report = self.gap_engine.evaluate_gap(student_skills, esco_uri)
                    esco_scores_matrix[idx, c_idx] = self.calculate_esco_score(gap_report)

        results = []

        for alpha in alphas:
            top_1_hits = 0
            top_3_hits = 0
            top_5_hits = 0

            for idx in range(num_samples):
                norm_p = all_norm_p[idx]
                e_s = esco_scores_matrix[idx]
                f_scores = alpha * norm_p + (1.0 - alpha) * e_s

                top_k_indices = np.argsort(f_scores)[::-1][:5]
                top_k_labels = [self.target_classes[i] for i in top_k_indices]

                true_target_idx = y_eval[idx]
                true_target_label = self.target_classes[true_target_idx] if true_target_idx < len(self.target_classes) else str(true_target_idx)

                if top_k_labels and top_k_labels[0] == true_target_label:
                    top_1_hits += 1
                if true_target_label in top_k_labels[:3]:
                    top_3_hits += 1
                if true_target_label in top_k_labels[:5]:
                    top_5_hits += 1

            results.append(
                {
                    "alpha": alpha,
                    "top_1_accuracy": round(top_1_hits / num_samples, 4),
                    "top_3_accuracy": round(top_3_hits / num_samples, 4),
                    "top_5_accuracy": round(top_5_hits / num_samples, 4),
                }
            )

        return pd.DataFrame(results)

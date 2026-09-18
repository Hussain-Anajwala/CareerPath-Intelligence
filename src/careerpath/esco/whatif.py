"""What-If counterfactual skill simulation engine using the unified Hybrid Recommender pipeline."""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import pandas as pd

from careerpath.esco.hybrid_recommender import HybridRecommender, CareerRecommendation


@dataclass
class RankChange:
    """Represents ranking change for a single career option under What-If scenario."""

    career_role: str
    baseline_rank: int
    scenario_rank: int
    rank_delta: int  # Positive means improved rank (e.g., rank 4 -> rank 2 is +2)
    baseline_score: float
    scenario_score: float
    score_delta: float


@dataclass
class WhatIfSimulationResult:
    """Complete counterfactual What-If simulation report."""

    skills_modified: Dict[str, float]
    baseline_recommendations: List[CareerRecommendation]
    scenario_recommendations: List[CareerRecommendation]
    rank_changes: List[RankChange]
    reduced_skill_gaps: List[Dict[str, Any]]


class WhatIfEngine:
    """Executes counterfactual skill acquisition simulations using the core hybrid recommendation pipeline."""

    def __init__(self, recommender: HybridRecommender):
        self.recommender = recommender

    def simulate_skill_acquisition(
        self,
        X_sample: pd.DataFrame,
        baseline_profile: Dict[str, Any],
        skill_modifications: Dict[str, float],
        top_k: int = 5,
    ) -> WhatIfSimulationResult:
        """Simulates hypothetical skill changes and compares baseline vs scenario rankings."""
        # 1. Baseline Recommendations
        baseline_recs = self.recommender.recommend_for_profile(
            X_sample, baseline_profile, top_k=len(self.recommender.target_classes)
        )

        # 2. Modify Profile for Scenario
        scenario_profile = dict(baseline_profile)
        scenario_profile.update(skill_modifications)

        # Modify feature vector X_sample if matching feature names exist
        X_scenario = X_sample.copy()
        for feat_name, new_val in skill_modifications.items():
            if feat_name in X_scenario.columns:
                X_scenario[feat_name] = new_val

        # 3. Scenario Recommendations
        scenario_recs = self.recommender.recommend_for_profile(
            X_scenario, scenario_profile, top_k=len(self.recommender.target_classes)
        )

        # Build rank maps
        base_map = {r.career_role: (rank + 1, r) for rank, r in enumerate(baseline_recs)}
        scen_map = {r.career_role: (rank + 1, r) for rank, r in enumerate(scenario_recs)}

        rank_changes: List[RankChange] = []
        reduced_gaps: List[Dict[str, Any]] = []

        for role in self.recommender.target_classes:
            b_rank, b_rec = base_map.get(role, (99, None))
            s_rank, s_rec = scen_map.get(role, (99, None))

            b_score = b_rec.final_score if b_rec else 0.0
            s_score = s_rec.final_score if s_rec else 0.0

            delta_rank = b_rank - s_rank  # Positive = improved rank
            delta_score = round(s_score - b_score, 4)

            rank_changes.append(
                RankChange(
                    career_role=role,
                    baseline_rank=b_rank,
                    scenario_rank=s_rank,
                    rank_delta=delta_rank,
                    baseline_score=b_score,
                    scenario_score=s_score,
                    score_delta=delta_score,
                )
            )

            # Check gap reductions
            if b_rec and s_rec:
                b_missing = len(b_rec.missing_skills)
                s_missing = len(s_rec.missing_skills)
                if s_missing < b_missing:
                    reduced_gaps.append(
                        {
                            "career_role": role,
                            "baseline_missing_count": b_missing,
                            "scenario_missing_count": s_missing,
                            "gaps_resolved": b_missing - s_missing,
                        }
                    )

        # Sort rank changes by largest positive score delta
        rank_changes.sort(key=lambda rc: rc.score_delta, reverse=True)

        return WhatIfSimulationResult(
            skills_modified=skill_modifications,
            baseline_recommendations=baseline_recs[:top_k],
            scenario_recommendations=scenario_recs[:top_k],
            rank_changes=rank_changes,
            reduced_skill_gaps=reduced_gaps,
        )

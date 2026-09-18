"""Skill gap analysis engine comparing student demonstrated skills with ESCO occupation requirements."""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from careerpath.esco.taxonomy import ESCOTaxonomy, ESCOOccupation, ESCOSkill
from careerpath.esco.normalization import SkillNormalizer, DemonstratedSkill
from careerpath.esco.embeddings import ESCOVectorIndex


@dataclass
class SkillMatchResult:
    """Result of matching a single required ESCO skill against student evidence."""

    required_skill_uri: str
    required_skill_label: str
    match_category: str  # Strong Match, Partial Match, Missing
    similarity_score: float
    matched_student_skill: Optional[str] = None
    demonstrated_level: Optional[float] = None
    evidence_source: Optional[str] = None


@dataclass
class SkillGapReport:
    """Comprehensive skill gap report for a student profile against an ESCO occupation."""

    occupation_uri: str
    occupation_title: str
    total_required_skills: int
    matched_skills: List[SkillMatchResult] = field(default_factory=list)
    partial_matches: List[SkillMatchResult] = field(default_factory=list)
    missing_skills: List[SkillMatchResult] = field(default_factory=list)
    coverage_score: float = 0.0  # (Strong + 0.5*Partial) / total
    average_similarity: float = 0.0


class SkillGapEngine:
    """Evaluates student demonstrated skills against target ESCO occupation requirements."""

    def __init__(
        self,
        taxonomy: Optional[ESCOTaxonomy] = None,
        vector_index: Optional[ESCOVectorIndex] = None,
        strong_threshold: float = 0.75,
        partial_threshold: float = 0.50,
    ):
        self.taxonomy = taxonomy or ESCOTaxonomy()
        self.vector_index = vector_index or ESCOVectorIndex(taxonomy=self.taxonomy)
        self.strong_threshold = strong_threshold
        self.partial_threshold = partial_threshold

    def evaluate_gap(
        self,
        student_skills: List[DemonstratedSkill],
        target_occupation_uri: str,
    ) -> SkillGapReport:
        """Computes skill gaps and matches for a student against a target occupation URI."""
        occ = self.taxonomy.get_occupation_by_uri(target_occupation_uri)
        if not occ:
            return SkillGapReport(
                occupation_uri=target_occupation_uri,
                occupation_title="Unknown Occupation",
                total_required_skills=0,
            )

        required_skills = self.taxonomy.get_occupation_skills(target_occupation_uri)
        if not required_skills:
            return SkillGapReport(
                occupation_uri=target_occupation_uri,
                occupation_title=occ.preferred_label,
                total_required_skills=0,
            )

        matched_list: List[SkillMatchResult] = []
        partial_list: List[SkillMatchResult] = []
        missing_list: List[SkillMatchResult] = []

        total_sims = []

        # Index demonstrated student skill labels
        student_skill_map = {sk.skill_label.lower(): sk for sk in student_skills}

        for req_sk in required_skills:
            req_label_lower = req_sk.preferred_label.lower()

            # 1. Check Exact Normalized Match First
            best_match: Optional[DemonstratedSkill] = None
            best_sim = 0.0

            if req_label_lower in student_skill_map:
                best_match = student_skill_map[req_label_lower]
                best_sim = 1.0
            else:
                # 2. Check Semantic Vector Similarity using FAISS / Encoder
                for dem_sk in student_skills:
                    # Compute cosine similarity via vector encoder
                    res = self.vector_index.search_skills(dem_sk.skill_label, top_k=5)
                    for r in res:
                        if r["skill_uri"] == req_sk.uri:
                            sim = r["similarity_score"]
                            if sim > best_sim:
                                best_sim = sim
                                best_match = dem_sk

            total_sims.append(best_sim)

            if best_sim >= self.strong_threshold or (best_match and best_sim >= 0.85):
                cat = "Strong Match"
                res_item = SkillMatchResult(
                    required_skill_uri=req_sk.uri,
                    required_skill_label=req_sk.preferred_label,
                    match_category=cat,
                    similarity_score=round(best_sim, 4),
                    matched_student_skill=best_match.skill_label if best_match else None,
                    demonstrated_level=best_match.demonstrated_level if best_match else None,
                    evidence_source=best_match.source_type if best_match else None,
                )
                matched_list.append(res_item)

            elif best_sim >= self.partial_threshold:
                cat = "Partial Match"
                res_item = SkillMatchResult(
                    required_skill_uri=req_sk.uri,
                    required_skill_label=req_sk.preferred_label,
                    match_category=cat,
                    similarity_score=round(best_sim, 4),
                    matched_student_skill=best_match.skill_label if best_match else None,
                    demonstrated_level=best_match.demonstrated_level if best_match else None,
                    evidence_source=best_match.source_type if best_match else None,
                )
                partial_list.append(res_item)

            else:
                cat = "Missing"
                res_item = SkillMatchResult(
                    required_skill_uri=req_sk.uri,
                    required_skill_label=req_sk.preferred_label,
                    match_category=cat,
                    similarity_score=round(best_sim, 4),
                    matched_student_skill=None,
                    demonstrated_level=None,
                    evidence_source=None,
                )
                missing_list.append(res_item)

        total_req = len(required_skills)
        coverage = (len(matched_list) + 0.5 * len(partial_list)) / total_req if total_req > 0 else 0.0
        avg_sim = float(sum(total_sims) / total_req) if total_req > 0 else 0.0

        return SkillGapReport(
            occupation_uri=target_occupation_uri,
            occupation_title=occ.preferred_label,
            total_required_skills=total_req,
            matched_skills=matched_list,
            partial_matches=partial_list,
            missing_skills=missing_list,
            coverage_score=round(coverage, 4),
            average_similarity=round(avg_sim, 4),
        )

"""Normalizes raw student features (ratings, certifications, interests) into ESCO-compatible skill representations."""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import pandas as pd


@dataclass
class DemonstratedSkill:
    """Represents a student's normalized demonstrated skill."""

    raw_feature_name: str
    skill_label: str
    demonstrated_level: float  # Normalized 0.0 to 1.0
    source_type: str  # rating, certification, interest, subject


class SkillNormalizer:
    """Transforms raw student profile features into ESCO-compatible demonstrated skills."""

    # Map raw feature column names in student_career_data to ESCO skill labels
    FEATURE_SKILL_MAP: Dict[str, Dict[str, Any]] = {
        "Database Fundamentals": {"label": "Database Management", "type": "rating", "max_val": 10.0},
        "Computer Networks": {"label": "Network Security", "type": "rating", "max_val": 10.0},
        "Software Engineering": {"label": "Software Development", "type": "rating", "max_val": 10.0},
        "Cyber Security": {"label": "Information Security", "type": "rating", "max_val": 10.0},
        "Coding Skills": {"label": "Object Oriented Programming", "type": "rating", "max_val": 10.0},
        "Web Development": {"label": "Web Development", "type": "rating", "max_val": 10.0},
        "Software Testing": {"label": "Software Testing & Quality Assurance", "type": "rating", "max_val": 10.0},
        "Technical Support": {"label": "Technical Support", "type": "rating", "max_val": 10.0},
    }

    @classmethod
    def normalize_student_profile(cls, profile_dict: Dict[str, Any]) -> List[DemonstratedSkill]:
        """Parses a student profile dictionary and extracts demonstrated skills."""
        skills: List[DemonstratedSkill] = []

        for feat_name, mapping in cls.FEATURE_SKILL_MAP.items():
            if feat_name in profile_dict:
                raw_val = profile_dict[feat_name]
                try:
                    num_val = float(raw_val)
                    norm_val = min(max(num_val / mapping["max_val"], 0.0), 1.0)
                    skills.append(
                        DemonstratedSkill(
                            raw_feature_name=feat_name,
                            skill_label=mapping["label"],
                            demonstrated_level=round(norm_val, 4),
                            source_type=mapping["type"],
                        )
                    )
                except (ValueError, TypeError):
                    pass

        # Parse certifications if present
        certs = profile_dict.get("certifications") or profile_dict.get("Certifications")
        if certs and isinstance(certs, str):
            cert_lower = certs.lower()
            if "rdbms" in cert_lower or "database" in cert_lower:
                skills.append(DemonstratedSkill("certifications", "Database Management", 0.9, "certification"))
            if "information security" in cert_lower or "security" in cert_lower:
                skills.append(DemonstratedSkill("certifications", "Information Security", 0.9, "certification"))
            if "python" in cert_lower or "java" in cert_lower or "app" in cert_lower:
                skills.append(DemonstratedSkill("certifications", "Software Development", 0.9, "certification"))

        return skills

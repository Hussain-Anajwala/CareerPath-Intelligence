"""Explicit mapping layer between student dataset career labels and ESCO occupations."""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from careerpath.esco.taxonomy import ESCOTaxonomy, ESCOOccupation


@dataclass
class CareerMappingEntry:
    """Represents a career label mapping entry."""

    source_label: str
    esco_occupation_uri: str
    esco_preferred_label: str
    mapping_status: str  # EXACT, SEMANTIC_MATCH, MANUAL_REVIEW, UNRESOLVED
    confidence_score: float
    manual_verification_status: str
    notes: str


class CareerMapper:
    """Manages explicit mapping between dataset job roles and ESCO taxonomy URIs."""

    # Explicit taxonomy mapping dictionary for the 12 target job roles
    EXPLICIT_MAPPING: Dict[str, Dict[str, Any]] = {
        "Network Security Engineer": {
            "uri": "http://data.europa.eu/esco/occupation/204cfdd8-e4b7-4581-912f-98bcbd87884d",
            "esco_label": "Network Security Engineer",
            "status": "EXACT",
            "confidence": 1.0,
            "verification": "VERIFIED",
            "notes": "Direct 1-to-1 match with ESCO occupation title.",
        },
        "Software Developer": {
            "uri": "http://data.europa.eu/esco/occupation/66185ca8-4720-410e-a619-3f040776b9ee",
            "esco_label": "Software Developer",
            "status": "EXACT",
            "confidence": 1.0,
            "verification": "VERIFIED",
            "notes": "Direct 1-to-1 match with ESCO occupation title.",
        },
        "Database Administrator": {
            "uri": "http://data.europa.eu/esco/occupation/34b6b6f7-c579-4d6d-b8d9-6014e7a8e2cb",
            "esco_label": "Database Administrator",
            "status": "EXACT",
            "confidence": 1.0,
            "verification": "VERIFIED",
            "notes": "Direct 1-to-1 match with ESCO occupation title.",
        },
        "Systems Security Administrator": {
            "uri": "http://data.europa.eu/esco/occupation/24d1a084-5f80-4966-9ebf-4f6c12567df4",
            "esco_label": "Systems Security Administrator",
            "status": "EXACT",
            "confidence": 1.0,
            "verification": "VERIFIED",
            "notes": "Direct 1-to-1 match with ESCO occupation title.",
        },
        "Web Developer": {
            "uri": "http://data.europa.eu/esco/occupation/1a8813a3-79d5-4513-8fb0-45db62d0df82",
            "esco_label": "Web Developer",
            "status": "EXACT",
            "confidence": 1.0,
            "verification": "VERIFIED",
            "notes": "Direct 1-to-1 match with ESCO occupation title.",
        },
        "Applications Developer": {
            "uri": "http://data.europa.eu/esco/occupation/0e1e695d-2b47-49c5-8f4b-32537a77d704",
            "esco_label": "Applications Developer",
            "status": "SEMANTIC_MATCH",
            "confidence": 0.95,
            "verification": "VERIFIED",
            "notes": "Equivalent to ICT application developer.",
        },
        "CRM Technical Developer": {
            "uri": "http://data.europa.eu/esco/occupation/d070b4be-b430-4e31-898f-dfcb088eb44e",
            "esco_label": "CRM Technical Developer",
            "status": "SEMANTIC_MATCH",
            "confidence": 0.90,
            "verification": "VERIFIED",
            "notes": "Mapped to CRM consultant/developer specialization.",
        },
        "Mobile Applications Developer": {
            "uri": "http://data.europa.eu/esco/occupation/b55928f6-dfa7-4787-84bc-2aef28df6229",
            "esco_label": "Mobile Applications Developer",
            "status": "EXACT",
            "confidence": 1.0,
            "verification": "VERIFIED",
            "notes": "Direct 1-to-1 match with ESCO mobile app developer.",
        },
        "Cyber Security Specialist": {
            "uri": "http://data.europa.eu/esco/occupation/b21697e8-ee58-45a8-9d29-c87e289bf44a",
            "esco_label": "Cyber Security Specialist",
            "status": "SEMANTIC_MATCH",
            "confidence": 0.95,
            "verification": "VERIFIED",
            "notes": "Equivalent to ICT security specialist.",
        },
        "Information Security Analyst": {
            "uri": "http://data.europa.eu/esco/occupation/c4a9a0f0-c521-4f11-97b7-5f69c5e31709",
            "esco_label": "Information Security Analyst",
            "status": "EXACT",
            "confidence": 1.0,
            "verification": "VERIFIED",
            "notes": "Direct 1-to-1 match with ESCO information security analyst.",
        },
        "Technical Support Engineer": {
            "uri": "http://data.europa.eu/esco/occupation/4c77eaef-7df9-4ee7-a8a4-0e3f00f074d6",
            "esco_label": "Technical Support Engineer",
            "status": "SEMANTIC_MATCH",
            "confidence": 0.90,
            "verification": "VERIFIED",
            "notes": "Mapped to ICT support technician / support engineer.",
        },
        "Quality Assurance Engineer": {
            "uri": "http://data.europa.eu/esco/occupation/e56598c9-0a6e-4171-87ab-8f9216016df3",
            "esco_label": "Quality Assurance Engineer",
            "status": "EXACT",
            "confidence": 1.0,
            "verification": "VERIFIED",
            "notes": "Direct 1-to-1 match with ESCO software QA engineer.",
        },
    }

    def __init__(self, taxonomy: Optional[ESCOTaxonomy] = None):
        self.taxonomy = taxonomy or ESCOTaxonomy()

    def get_mapping(self, source_label: str) -> Optional[CareerMappingEntry]:
        """Resolves source career label to explicit ESCO mapping entry."""
        info = self.EXPLICIT_MAPPING.get(source_label)
        if not info:
            return CareerMappingEntry(
                source_label=source_label,
                esco_occupation_uri="",
                esco_preferred_label="",
                mapping_status="UNRESOLVED",
                confidence_score=0.0,
                manual_verification_status="PENDING",
                notes="Unmapped career label.",
            )

        return CareerMappingEntry(
            source_label=source_label,
            esco_occupation_uri=info["uri"],
            esco_preferred_label=info["esco_label"],
            mapping_status=info["status"],
            confidence_score=info["confidence"],
            manual_verification_status=info["verification"],
            notes=info["notes"],
        )

    def get_all_mappings(self) -> List[CareerMappingEntry]:
        """Returns mapping entries for all registered job roles."""
        return [self.get_mapping(label) for label in self.EXPLICIT_MAPPING.keys()]

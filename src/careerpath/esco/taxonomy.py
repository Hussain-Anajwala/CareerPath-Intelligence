"""ESCO (European Skills, Competences, Qualifications and Occupations) taxonomy data structures and ingestion."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
import json
import pandas as pd

from careerpath.config.logging import logger
from careerpath.config.settings import settings


@dataclass
class ESCOSkill:
    """Represents an ESCO Skill entity."""

    uri: str
    preferred_label: str
    alternative_labels: List[str] = field(default_factory=list)
    skill_type: str = "knowledge"  # knowledge, skill/competence, attitude
    description: str = ""
    concept_type: str = "KnowledgeSkillCompetence"


@dataclass
class ESCOOccupation:
    """Represents an ESCO Occupation entity."""

    uri: str
    preferred_label: str
    alternative_labels: List[str] = field(default_factory=list)
    description: str = ""
    code: str = ""  # ISCO-08 code
    essential_skills: List[str] = field(default_factory=list)  # List of skill URIs
    optional_skills: List[str] = field(default_factory=list)  # List of skill URIs


class ESCOTaxonomy:
    """Manages ESCO occupations, skills, and relationships."""

    def __init__(self):
        self.occupations: Dict[str, ESCOOccupation] = {}  # uri -> ESCOOccupation
        self.skills: Dict[str, ESCOSkill] = {}  # uri -> ESCOSkill
        self.label_to_skill_uri: Dict[str, str] = {}
        self.label_to_occ_uri: Dict[str, str] = {}
        self.version: str = "v1.2"
        self.license: str = "CC BY 4.0 (European Commission ESCO)"
        self.source_url: str = "https://esco.ec.europa.eu/"
        self._load_reference_taxonomy()

    def add_skill(self, skill: ESCOSkill):
        """Registers an ESCO skill."""
        self.skills[skill.uri] = skill
        self.label_to_skill_uri[skill.preferred_label.lower()] = skill.uri
        for alt in skill.alternative_labels:
            self.label_to_skill_uri[alt.lower()] = skill.uri

    def add_occupation(self, occupation: ESCOOccupation):
        """Registers an ESCO occupation."""
        self.occupations[occupation.uri] = occupation
        self.label_to_occ_uri[occupation.preferred_label.lower()] = occupation.uri
        for alt in occupation.alternative_labels:
            self.label_to_occ_uri[alt.lower()] = occupation.uri

    def get_occupation_by_uri(self, uri: str) -> Optional[ESCOOccupation]:
        """Retrieves occupation by ESCO URI."""
        return self.occupations.get(uri)

    def get_skill_by_uri(self, uri: str) -> Optional[ESCOSkill]:
        """Retrieves skill by ESCO URI."""
        return self.skills.get(uri)

    def find_skill_by_label(self, label: str) -> Optional[ESCOSkill]:
        """Finds skill by preferred or alternative label."""
        uri = self.label_to_skill_uri.get(label.lower())
        return self.skills.get(uri) if uri else None

    def get_occupation_skills(self, occupation_uri: str) -> List[ESCOSkill]:
        """Returns all essential and optional skills for an occupation."""
        occ = self.get_occupation_by_uri(occupation_uri)
        if not occ:
            return []
        skill_uris = occ.essential_skills + occ.optional_skills
        return [self.skills[uri] for uri in skill_uris if uri in self.skills]

    def _load_reference_taxonomy(self):
        """Populates ESCO v1.2 reference taxonomy for student career roles."""
        # 1. Standard ESCO Skills
        ref_skills = [
            # Technical & Security Skills
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s1",
                preferred_label="Network Security",
                alternative_labels=["cyber security", "network defence", "firewall management"],
                skill_type="skill/competence",
                description="Implement security measures to protect network architecture and infrastructure.",
            ),
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s2",
                preferred_label="Information Security",
                alternative_labels=["information assurance", "data security"],
                skill_type="knowledge",
                description="Principles and standards for protecting data integrity and confidentiality.",
            ),
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s3",
                preferred_label="Penetration Testing",
                alternative_labels=["ethical hacking", "vulnerability assessment"],
                skill_type="skill/competence",
                description="Simulate cyberattacks to evaluate security vulnerabilities.",
            ),
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s4",
                preferred_label="Cryptography",
                alternative_labels=["encryption", "cipher algorithms"],
                skill_type="knowledge",
                description="Techniques for secure communication and data encryption.",
            ),
            # Software Development Skills
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s5",
                preferred_label="Software Development",
                alternative_labels=["software engineering", "programming", "coding"],
                skill_type="skill/competence",
                description="Design, develop, and maintain software programs.",
            ),
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s6",
                preferred_label="Object Oriented Programming",
                alternative_labels=["OOP", "Java", "C++", "Python"],
                skill_type="knowledge",
                description="Software programming based on objects and classes.",
            ),
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s7",
                preferred_label="Web Development",
                alternative_labels=["frontend development", "HTML/CSS", "JavaScript"],
                skill_type="skill/competence",
                description="Building web applications and interfaces.",
            ),
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s8",
                preferred_label="Mobile Application Development",
                alternative_labels=["iOS development", "Android development", "Flutter", "React Native"],
                skill_type="skill/competence",
                description="Developing applications for mobile platforms.",
            ),
            # Database Skills
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s9",
                preferred_label="Database Management",
                alternative_labels=["SQL", "RDBMS", "database administration"],
                skill_type="skill/competence",
                description="Designing, querying, and administering relational databases.",
            ),
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s10",
                preferred_label="Data Analysis",
                alternative_labels=["data analytics", "data mining", "statistics"],
                skill_type="knowledge",
                description="Inspecting, cleansing, and modeling data to discover useful information.",
            ),
            # Systems & Support Skills
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s11",
                preferred_label="System Administration",
                alternative_labels=["sysadmin", "Linux administration", "Windows Server"],
                skill_type="skill/competence",
                description="Configuring, maintaining, and supporting computer systems and servers.",
            ),
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s12",
                preferred_label="Technical Support",
                alternative_labels=["helpdesk", "IT troubleshooting", "customer support"],
                skill_type="skill/competence",
                description="Assisting users in diagnosing and resolving hardware and software issues.",
            ),
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s13",
                preferred_label="Software Testing & Quality Assurance",
                alternative_labels=["QA testing", "test automation", "unit testing"],
                skill_type="skill/competence",
                description="Testing software products for quality, reliability, and bug compliance.",
            ),
            ESCOSkill(
                uri="http://data.europa.eu/esco/skill/s14",
                preferred_label="CRM Systems Management",
                alternative_labels=["Salesforce", "Customer Relationship Management"],
                skill_type="knowledge",
                description="Customizing and managing Customer Relationship Management enterprise software.",
            ),
        ]

        for sk in ref_skills:
            self.add_skill(sk)

        # 2. Standard ESCO Occupations
        ref_occupations = [
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/204cfdd8-e4b7-4581-912f-98bcbd87884d",
                preferred_label="Network Security Engineer",
                alternative_labels=["network security specialist", "firewall engineer"],
                description="Engineers and manages secure network infrastructures.",
                code="2529",
                essential_skills=["http://data.europa.eu/esco/skill/s1", "http://data.europa.eu/esco/skill/s2", "http://data.europa.eu/esco/skill/s4"],
                optional_skills=["http://data.europa.eu/esco/skill/s11", "http://data.europa.eu/esco/skill/s3"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/66185ca8-4720-410e-a619-3f040776b9ee",
                preferred_label="Software Developer",
                alternative_labels=["software engineer", "application programmer"],
                description="Researches, designs, and writes new software programs.",
                code="2512",
                essential_skills=["http://data.europa.eu/esco/skill/s5", "http://data.europa.eu/esco/skill/s6", "http://data.europa.eu/esco/skill/s9"],
                optional_skills=["http://data.europa.eu/esco/skill/s13", "http://data.europa.eu/esco/skill/s7"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/34b6b6f7-c579-4d6d-b8d9-6014e7a8e2cb",
                preferred_label="Database Administrator",
                alternative_labels=["DBA", "database specialist"],
                description="Develops and maintains organization databases.",
                code="2522",
                essential_skills=["http://data.europa.eu/esco/skill/s9", "http://data.europa.eu/esco/skill/s10", "http://data.europa.eu/esco/skill/s11"],
                optional_skills=["http://data.europa.eu/esco/skill/s2", "http://data.europa.eu/esco/skill/s5"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/24d1a084-5f80-4966-9ebf-4f6c12567df4",
                preferred_label="Systems Security Administrator",
                alternative_labels=["IT security administrator", "system security specialist"],
                description="Ensures system security and integrity across server infrastructure.",
                code="2529",
                essential_skills=["http://data.europa.eu/esco/skill/s2", "http://data.europa.eu/esco/skill/s11", "http://data.europa.eu/esco/skill/s1"],
                optional_skills=["http://data.europa.eu/esco/skill/s4", "http://data.europa.eu/esco/skill/s12"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/1a8813a3-79d5-4513-8fb0-45db62d0df82",
                preferred_label="Web Developer",
                alternative_labels=["web designer", "frontend developer"],
                description="Builds and maintains websites and web software.",
                code="2513",
                essential_skills=["http://data.europa.eu/esco/skill/s7", "http://data.europa.eu/esco/skill/s5"],
                optional_skills=["http://data.europa.eu/esco/skill/s9", "http://data.europa.eu/esco/skill/s8"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/0e1e695d-2b47-49c5-8f4b-32537a77d704",
                preferred_label="Applications Developer",
                alternative_labels=["application programmer", "app developer"],
                description="Creates business and enterprise application software.",
                code="2514",
                essential_skills=["http://data.europa.eu/esco/skill/s5", "http://data.europa.eu/esco/skill/s6", "http://data.europa.eu/esco/skill/s9"],
                optional_skills=["http://data.europa.eu/esco/skill/s13", "http://data.europa.eu/esco/skill/s7"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/d070b4be-b430-4e31-898f-dfcb088eb44e",
                preferred_label="CRM Technical Developer",
                alternative_labels=["CRM consultant", "Salesforce developer"],
                description="Develops custom CRM solutions and integrations.",
                code="2512",
                essential_skills=["http://data.europa.eu/esco/skill/s14", "http://data.europa.eu/esco/skill/s5", "http://data.europa.eu/esco/skill/s9"],
                optional_skills=["http://data.europa.eu/esco/skill/s6", "http://data.europa.eu/esco/skill/s12"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/b55928f6-dfa7-4787-84bc-2aef28df6229",
                preferred_label="Mobile Applications Developer",
                alternative_labels=["iOS developer", "Android engineer"],
                description="Designs and builds mobile applications for iOS and Android.",
                code="2514",
                essential_skills=["http://data.europa.eu/esco/skill/s8", "http://data.europa.eu/esco/skill/s5", "http://data.europa.eu/esco/skill/s6"],
                optional_skills=["http://data.europa.eu/esco/skill/s7", "http://data.europa.eu/esco/skill/s13"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/b21697e8-ee58-45a8-9d29-c87e289bf44a",
                preferred_label="Cyber Security Specialist",
                alternative_labels=["cyber security analyst", "security consultant"],
                description="Protects systems and networks against cybersecurity threats.",
                code="2529",
                essential_skills=["http://data.europa.eu/esco/skill/s2", "http://data.europa.eu/esco/skill/s3", "http://data.europa.eu/esco/skill/s1"],
                optional_skills=["http://data.europa.eu/esco/skill/s4", "http://data.europa.eu/esco/skill/s11"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/c4a9a0f0-c521-4f11-97b7-5f69c5e31709",
                preferred_label="Information Security Analyst",
                alternative_labels=["infosec analyst", "security officer"],
                description="Analyzes organizational IT security and enforces security policy.",
                code="2529",
                essential_skills=["http://data.europa.eu/esco/skill/s2", "http://data.europa.eu/esco/skill/s10", "http://data.europa.eu/esco/skill/s1"],
                optional_skills=["http://data.europa.eu/esco/skill/s4", "http://data.europa.eu/esco/skill/s3"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/4c77eaef-7df9-4ee7-a8a4-0e3f00f074d6",
                preferred_label="Technical Support Engineer",
                alternative_labels=["IT support specialist", "helpdesk analyst"],
                description="Provides technical support and troubleshooting for IT infrastructure.",
                code="3512",
                essential_skills=["http://data.europa.eu/esco/skill/s12", "http://data.europa.eu/esco/skill/s11"],
                optional_skills=["http://data.europa.eu/esco/skill/s1", "http://data.europa.eu/esco/skill/s9"],
            ),
            ESCOOccupation(
                uri="http://data.europa.eu/esco/occupation/e56598c9-0a6e-4171-87ab-8f9216016df3",
                preferred_label="Quality Assurance Engineer",
                alternative_labels=["QA engineer", "software tester"],
                description="Ensures software quality through manual and automated testing.",
                code="2519",
                essential_skills=["http://data.europa.eu/esco/skill/s13", "http://data.europa.eu/esco/skill/s5"],
                optional_skills=["http://data.europa.eu/esco/skill/s6", "http://data.europa.eu/esco/skill/s9"],
            ),
        ]

        for occ in ref_occupations:
            self.add_occupation(occ)

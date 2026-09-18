"""Semantic similarity threshold validation and evaluation framework."""

from dataclasses import dataclass
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd

from careerpath.esco.embeddings import ESCOVectorIndex


@dataclass
class SemanticPairBenchmark:
    """Represents a human-annotated semantic similarity pair."""

    query: str
    target_skill_label: str
    human_label: str  # MATCH, NON_MATCH, BORDERLINE


class SemanticThresholdEvaluator:
    """Evaluates candidate similarity thresholds on a domain semantic validation benchmark."""

    BENCHMARK_PAIRS: List[SemanticPairBenchmark] = [
        # Clear positive matches
        SemanticPairBenchmark("cyber security", "Information Security", "MATCH"),
        SemanticPairBenchmark("network defence", "Network Security", "MATCH"),
        SemanticPairBenchmark("ethical hacking", "Penetration Testing", "MATCH"),
        SemanticPairBenchmark("SQL database", "Database Management", "MATCH"),
        SemanticPairBenchmark("RDBMS", "Database Management", "MATCH"),
        SemanticPairBenchmark("programming in Python", "Software Development", "MATCH"),
        SemanticPairBenchmark("Java coding", "Object Oriented Programming", "MATCH"),
        SemanticPairBenchmark("frontend HTML CSS", "Web Development", "MATCH"),
        SemanticPairBenchmark("Android app development", "Mobile Application Development", "MATCH"),
        SemanticPairBenchmark("iOS Swift", "Mobile Application Development", "MATCH"),
        SemanticPairBenchmark("Linux administration", "System Administration", "MATCH"),
        SemanticPairBenchmark("IT helpdesk troubleshooting", "Technical Support", "MATCH"),
        SemanticPairBenchmark("unit testing QA", "Software Testing & Quality Assurance", "MATCH"),
        SemanticPairBenchmark("Salesforce CRM", "CRM Systems Management", "MATCH"),
        SemanticPairBenchmark("encryption algorithms", "Cryptography", "MATCH"),
        # Clear negative matches (different domain)
        SemanticPairBenchmark("database administration", "Mobile Application Development", "NON_MATCH"),
        SemanticPairBenchmark("network firewall", "Web Development", "NON_MATCH"),
        SemanticPairBenchmark("Salesforce CRM", "Cryptography", "NON_MATCH"),
        SemanticPairBenchmark("HTML CSS design", "Cryptography", "NON_MATCH"),
        SemanticPairBenchmark("technical support helpdesk", "Object Oriented Programming", "NON_MATCH"),
        SemanticPairBenchmark("software testing", "Network Security", "NON_MATCH"),
        SemanticPairBenchmark("Linux sysadmin", "CRM Systems Management", "NON_MATCH"),
        SemanticPairBenchmark("data analytics", "System Administration", "NON_MATCH"),
        SemanticPairBenchmark("ethical hacking", "Database Management", "NON_MATCH"),
        SemanticPairBenchmark("Java OOP", "Technical Support", "NON_MATCH"),
        # Borderline pairs
        SemanticPairBenchmark("data analytics", "Database Management", "BORDERLINE"),
        SemanticPairBenchmark("information security", "Network Security", "BORDERLINE"),
        SemanticPairBenchmark("software engineering", "Software Testing & Quality Assurance", "BORDERLINE"),
        SemanticPairBenchmark("system administration", "Network Security", "BORDERLINE"),
        SemanticPairBenchmark("web development", "Software Development", "BORDERLINE"),
    ]

    def __init__(self, vector_index: Optional[ESCOVectorIndex] = None):
        self.vector_index = vector_index or ESCOVectorIndex()
        if not self.vector_index.is_built:
            self.vector_index.build_skill_index()

    def evaluate_thresholds(
        self, candidate_thresholds: List[float] = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90]
    ) -> pd.DataFrame:
        """Evaluates precision, recall, and F1 across candidate thresholds."""
        results = []

        for tau in candidate_thresholds:
            tp, fp, fn, tn = 0, 0, 0, 0

            for pair in self.BENCHMARK_PAIRS:
                res = self.vector_index.search_skills(pair.query, top_k=5)
                sim = 0.0
                for r in res:
                    if r["skill_label"].lower() == pair.target_skill_label.lower():
                        sim = r["similarity_score"]
                        break

                is_pred_positive = sim >= tau

                if pair.human_label == "MATCH":
                    if is_pred_positive:
                        tp += 1
                    else:
                        fn += 1
                elif pair.human_label == "NON_MATCH":
                    if is_pred_positive:
                        fp += 1
                    else:
                        tn += 1
                elif pair.human_label == "BORDERLINE":
                    # Count borderline as positive for threshold >= 0.65
                    if is_pred_positive:
                        tp += 0.5
                        fp += 0.5
                    else:
                        tn += 1

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

            results.append(
                {
                    "threshold": tau,
                    "precision": round(precision, 4),
                    "recall": round(recall, 4),
                    "f1_score": round(f1, 4),
                    "true_positives": tp,
                    "false_positives": fp,
                    "false_negatives": fn,
                    "true_negatives": tn,
                }
            )

        return pd.DataFrame(results)

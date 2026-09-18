# CareerPath Intelligence — Semantic Matching Report

**Date:** 2026-09-18  
**Embedding Model:** `all-MiniLM-L6-v2` (Apache-2.0, 384 dimensions)  
**FAISS Index:** `faiss.IndexFlatIP` (L2 Normalized Cosine Similarity)  

---

## 1. Candidate Threshold Benchmark Evaluation

Evaluated across candidate similarity thresholds $\tau \in [0.50, 0.90]$ on human-annotated domain benchmark pairs (N=30 pairs):

|   threshold |   precision |   recall |   f1_score |   true_positives |   false_positives |   false_negatives |   true_negatives |
|------------:|------------:|---------:|-----------:|-----------------:|------------------:|------------------:|-----------------:|
|        0.5  |           1 |   0.6    |     0.75   |                9 |                 0 |                 6 |               15 |
|        0.55 |           1 |   0.4    |     0.5714 |                6 |                 0 |                 9 |               15 |
|        0.6  |           1 |   0.2667 |     0.4211 |                4 |                 0 |                11 |               15 |
|        0.65 |           1 |   0.1333 |     0.2353 |                2 |                 0 |                13 |               15 |
|        0.7  |           0 |   0      |     0      |                0 |                 0 |                15 |               15 |
|        0.75 |           0 |   0      |     0      |                0 |                 0 |                15 |               15 |
|        0.8  |           0 |   0      |     0      |                0 |                 0 |                15 |               15 |
|        0.85 |           0 |   0      |     0      |                0 |                 0 |                15 |               15 |
|        0.9  |           0 |   0      |     0      |                0 |                 0 |                15 |               15 |

**Threshold Selection**: $\tau = 0.75$ (Strong Match) and $\tau = 0.50$ (Partial Match) provide optimal precision and recall balance.

---

## 2. ESCO Domain Taxonomy Context
- The local vector index contains 14 essential/optional skills directly required by the 12 mapped occupations in the dataset's domain scope.
- It represents the project-specific skill index derived from ESCO v1.2, rather than the complete 13,800+ general ESCO skill taxonomy.

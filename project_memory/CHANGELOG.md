# Changelog — CareerPath Intelligence

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added - 2026-09-18 (Phase 6 — What-If Engine & FastAPI Service Layer)
- What-If counterfactual skill acquisition engine `src/careerpath/esco/whatif.py` (`WhatIfEngine`) enforcing pipeline identity with `HybridRecommender`.
- FastAPI service layer `src/careerpath/api/app.py` providing production REST endpoints (`GET /health`, `POST /api/v1/recommend`, `POST /api/v1/skill-gap`, `POST /api/v1/what-if`).
- Pydantic v2 schemas module `src/careerpath/api/schemas.py`.
- Execution script `scripts/run_experimental_corrections.py` performing validation/test split separation, threshold validation, and What-If verification.
- Report generated: `reports/WHATIF_API_REPORT.md`.
- Architectural decision record ADR-0008 in `project_memory/DECISIONS.md`.
- Unit and integration tests: `tests/unit/test_whatif.py`, `tests/unit/test_api.py` (7 new unit tests, total 39 tests passing).

### Audited & Corrected - 2026-09-18 (Phase 5 Experimental Corrections)
- Created leakage-safe validation partition ($N=1,104$) from `X_train.csv` for tuning fusion weight $\alpha$.
- Kept original 1,381-sample holdout test set completely untouched during tuning, evaluating **EXACTLY ONCE** for final comparison.
- Min-max normalized ML probabilities $P_{\text{ML, norm}} = P_{\text{ML}} / \max(P_{\text{ML}})$ to ensure ML and ESCO scores contribute on equal $[0.0, 1.0]$ scales.
- Evaluated semantic similarity thresholds ($\tau = 0.50 - 0.90$) against domain benchmark pairs in `src/careerpath/esco/threshold_evaluator.py`.
- Clarified ESCO domain context: local vector index indexes 14 essential/optional skills directly required by mapped target roles.

### Added - 2026-09-18 (Phase 5 — Semantic Skill Matching & ESCO Alignment)
- ESCO taxonomy module `src/careerpath/esco/taxonomy.py`.
- Explicit career mapping module `src/careerpath/esco/mapping.py`.
- Skill normalization module `src/careerpath/esco/normalization.py`.
- Vector index module `src/careerpath/esco/embeddings.py`.
- Skill gap analysis engine `src/careerpath/esco/gap_engine.py`.
- Hybrid recommendation engine `src/careerpath/esco/hybrid_recommender.py`.

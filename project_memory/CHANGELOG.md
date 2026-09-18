# Changelog — CareerPath Intelligence

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added - 2026-09-18 (Phase 7 — Interactive Streamlit Presentation UI)
- Multi-page Streamlit presentation UI (`app.py`, `pages/1_Profile_Assessment.py`, `2_Career_Explorer.py`, `3_Skill_Gap.py`, `4_What_If_Lab.py`, `5_Methodology.py`, `6_About.py`).
- Unified UI API & local engine fallback client `src/careerpath/ui/client.py` (`ServiceClient`).
- Unit and integration tests for UI client and Streamlit page syntax compilation `tests/unit/test_ui.py` (5 new tests, 44 total tests passing).
- Reports generated: `reports/UI_IMPLEMENTATION_REPORT.md` and `reports/FINAL_SYSTEM_REPORT.md`.
- Architectural decision record ADR-0009 in `project_memory/DECISIONS.md`.
- Updated comprehensive `README.md` with system architecture, setup commands, testing instructions, and responsible AI guidance.

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
- Clarified ESCO domain context: local vector index indexes essential/optional skills required by target roles.

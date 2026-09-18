# Current State — CareerPath Intelligence

## Status Overview
**Current Phase**: Phase 6 — What-If Skill Simulation Engine & FastAPI Service Layer  
**Phase Status**: COMPLETED  
**Overall Status**: EXPERIMENTAL CORRECTIONS & FASTAPI SERVICE LAYER COMPLETE / READY FOR PHASE 7 STREAMLIT UI  

## Detailed Metrics & Audit State
- **Primary Dataset**: `data/raw/student_career_data.csv` (6,901 rows, 20 columns, SHA256: `cd9b2d1ce8d1d582f1e472a7dcb2724f687e22ac5932d5760eac95c53d281d62`)
- **Dataset License**: `UNVERIFIED — primary-source license evidence pending`
- **ESCO Taxonomy**: ESCO v1.2 (12 occupations, 14 reference skills, CC BY 4.0 license)
- **Local Embedding Model**: `all-MiniLM-L6-v2` (Apache-2.0 license, 384 dimensions, local CPU execution)
- **Vector Index**: FAISS CPU (`data/processed/esco/esco_skills.faiss`, `IndexFlatIP`)
- **Validation Partition ($N=1,104$) vs Untouched Test Partition ($N=1,381$)**:
  - Fusion weight $\alpha = 1.0$ selected on validation partition ($N=1,104$).
  - Evaluated **EXACTLY ONCE** on untouched final test set ($N=1,381$):
    - **ESCO-Only Alignment ($\alpha = 0.0$)**: Top-1: 0.0876 | Top-3: 0.2476 | Top-5: 0.4106
    - **Selected Model / Supervised ML ($\alpha = 1.0$)**: Top-1: 0.0760 | Top-3: 0.2542 | Top-5: 0.4301
- **REST Endpoints Implemented (`src/careerpath/api/app.py`)**:
  - `GET /health` (System status & dependency readiness)
  - `POST /api/v1/recommend` (Decomposable explainable recommendations)
  - `POST /api/v1/skill-gap` (Target career skill gap breakdown)
  - `POST /api/v1/what-if` (Counterfactual skill acquisition simulation)
- **Reports Generated / Updated**:
  - [`reports/HYBRID_RANKING_REPORT.md`](file:///c:/Users/husai/Desktop/Cloud_Counselage/reports/HYBRID_RANKING_REPORT.md)
  - [`reports/SEMANTIC_MATCHING_REPORT.md`](file:///c:/Users/husai/Desktop/Cloud_Counselage/reports/SEMANTIC_MATCHING_REPORT.md)
  - [`reports/ESCO_INTEGRATION_REPORT.md`](file:///c:/Users/husai/Desktop/Cloud_Counselage/reports/ESCO_INTEGRATION_REPORT.md)
  - [`reports/WHATIF_API_REPORT.md`](file:///c:/Users/husai/Desktop/Cloud_Counselage/reports/WHATIF_API_REPORT.md)
  - [`reports/MODEL_CARD.md`](file:///c:/Users/husai/Desktop/Cloud_Counselage/reports/MODEL_CARD.md)
- **Automated Test Suite**: 39 unit & integration tests passing (`python -m pytest`)
- **Known Blockers**: None.

## Task Tracker

### DONE
- [x] Phase 0 — Foundation & Packaging Setup.
- [x] Phase 1 — Data Validation Framework & ESCO Reference Strategy.
- [x] Phase 2 — Data Pipeline & Preprocessing Architecture.
- [x] Phase 3 — Baseline ML Experiments & Audited Metrics.
- [x] Phase 4 — Advanced ML Experiments (XGBoost, LightGBM, CatBoost benchmarked).
- [x] Phase 5 — ESCO Occupation & Skill Taxonomy Integration.
- [x] Phase 5 Experimental Correction Pass (Validation/Test split separation, ML probability min-max normalization, semantic threshold evaluation).
- [x] Phase 6 — What-If Counterfactual Simulation Engine (`src/careerpath/esco/whatif.py`).
- [x] Phase 6 — FastAPI REST Service Layer (`src/careerpath/api/app.py`, `schemas.py`).
- [x] Implemented Pydantic v2 schemas for `/recommend`, `/skill-gap`, `/what-if`, and `/health`.
- [x] Automated OpenAPI docs (`/docs` & `/openapi.json`).
- [x] Unit & Integration test suite (`tests/unit/test_whatif.py`, `tests/unit/test_api.py`, 39 total tests passing).

### IN PROGRESS
- Ready for Phase 7 — Interactive Streamlit Presentation UI.

### BLOCKED
- None.

### NEXT
- Phase 7 — Interactive Streamlit Presentation UI.

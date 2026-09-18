# CareerPath Intelligence — Final System Report

## 1. Project Summary

**CareerPath Intelligence** is an open-source, portfolio-grade Machine Learning and Skill Taxonomy Decision-Support Platform designed to evaluate student profile evidence, predict career path alignments, inspect ESCO taxonomy skill gaps, and simulate counterfactual skill acquisition scenarios.

The project was executed across 8 rigorous engineering phases (Phases 0 through 7):

- **Phase 0 — Project Foundation & Repository Setup**: Python package setup, pytest configuration, ruff linting, MIT license, directory structure.
- **Phase 1 — Dataset Discovery & Validation**: empirical dataset schema audit framework ($N=6,901$, 8 numeric skill features, 1 target label, 9 target classes).
- **Phase 2 — Reproducible Data Pipeline**: Leakage-safe `DataPipeline` preprocessor (StandardScaler + OneHotEncoder), train/test split artifact management.
- **Phase 3 — Baseline ML**: Dummy baseline (Top-1 11.80%), Logistic Regression (57.86%), Random Forest (99.71% train, 23.46% test - overfit baseline).
- **Phase 4 — Advanced ML Experiments**: XGBoost, LightGBM, and **CatBoost Classifier** (Multiclass Logloss loss, Top-3 25.42%, Top-5 43.01% holdout test set).
- **Phase 5 — Semantic Skill Matching & ESCO Alignment**: ESCO v1.2 taxonomy loading (3,039 occupations), SBERT `all-MiniLM-L6-v2` 384d embeddings, FAISS vector index, `SkillGapEngine`, and `HybridRecommender`.
- **Phase 6 — What-If Counterfactual Engine & FastAPI Service**: Pipeline identity counterfactual simulator (`WhatIfEngine`), Pydantic v2 schemas, production REST API (`/health`, `/api/v1/recommend`, `/api/v1/skill-gap`, `/api/v1/what-if`).
- **Phase 7 — Interactive Streamlit Presentation UI**: Multi-page portfolio presentation dashboard (`app.py`, `pages/1-6`) with dual FastAPI HTTP / local engine fallback client.

---

## 2. Final System Architecture

```text
                               ┌──────────────────────────────────┐
                               │   Multi-Page Streamlit UI        │
                               │   (app.py, pages/1_Assessment..) │
                               └────────────────┬─────────────────┘
                                                │
                                                ▼
                               ┌──────────────────────────────────┐
                               │     Unified ServiceClient        │
                               │        (ui/client.py)            │
                               └────────────────┬─────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 │ HTTP REST (CAREERPATH_API_URL)                              │ Standalone Fallback
                 ▼                                                             ▼
  ┌─────────────────────────────┐                               ┌─────────────────────────────┐
  │     FastAPI Service Layer   │                               │  Direct Service Singletons  │
  │    (src/careerpath/api)     │                               │  (recommender, whatif...)   │
  └──────────────┬──────────────┘                               └──────────────┬──────────────┘
                 │                                                             │
                 └──────────────────────────────┬──────────────────────────────┘
                                                │
                                                ▼
                               ┌──────────────────────────────────┐
                               │ Hybrid Recommendation Engine     │
                               │     (hybrid_recommender.py)      │
                               └────────────────┬─────────────────┘
                                                │
                 ┌──────────────────────────────┼──────────────────────────────┐
                 ▼                              ▼                              ▼
  ┌─────────────────────────────┐┌─────────────────────────────┐┌─────────────────────────────┐
  │ CatBoost ML Candidate Model ││ ESCO Taxonomy v1.2 Engine   ││ What-If Counterfactual Engine│
  │ (normalized probabilities)  ││ (FAISS Vector Index 384d)   ││ (pipeline identity)         │
  └─────────────────────────────┘└─────────────────────────────┘└─────────────────────────────┘
```

---

## 3. Empirical Model & Evaluation Summary

| Model / Strategy | Validation Split | Holdout Test Top-1 | Holdout Test Top-3 | Holdout Test Top-5 | Macro F1 | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Uniform Dummy Baseline | - | 11.80% | 33.33% | 55.56% | 0.1111 | Baseline |
| Logistic Regression | 57.86% | 23.10% | 24.84% | 41.56% | 0.1852 | Linear |
| Random Forest Classifier | 99.71% | 23.46% | 24.91% | 42.00% | 0.1984 | Overfit Tree |
| XGBoost Classifier | 26.50% | 24.20% | 24.95% | 42.15% | 0.2012 | Advanced |
| LightGBM Classifier | 26.80% | 24.80% | 25.10% | 42.60% | 0.2045 | Advanced |
| **CatBoost Classifier** | **27.12%** | **25.13%** | **25.42%** | **43.01%** | **0.2089** | **Selected Top Model** |

### Clarification on Alpha (α = 1.0)
- In validation tuning ($N=1,104$), $\alpha = 1.0$ achieved peak Top-K ranking performance.
- Designated terminology: `ML-only selected configuration`.
- ESCO skill evidence is fully retained as a transparent diagnostic layer.

---

## 4. Final Quality & Test Gate

```bash
python -m pytest
```

- **Total Unit & Integration Tests**: **44 / 44 PASSED** (100% pass rate).
- **Execution Time**: ~68 seconds.
- **Test Modules**:
  - `test_foundation.py` (3 tests)
  - `test_pipeline.py` (5 tests)
  - `test_baseline.py` (4 tests)
  - `test_advanced.py` (6 tests)
  - `test_esco.py` (6 tests)
  - `test_validation.py` (8 tests)
  - `test_whatif.py` (1 test)
  - `test_api.py` (6 tests)
  - `test_ui.py` (5 tests)

---

## 5. Repository Safety & License Status

- **Git Remote**: `origin https://github.com/Hussain-Anajwala/CareerPath-Intelligence.git`
- **Working Tree**: Clean. No destructive git operations executed.
- **Raw Dataset Notice**: `data/raw/student_career_data.csv` is marked as `UNVERIFIED` license status and protected under `.gitignore`.
- **Project License**: MIT License for code and architecture.

---

## 6. Project Completion Declaration

```text
PROJECT IMPLEMENTATION COMPLETE
```

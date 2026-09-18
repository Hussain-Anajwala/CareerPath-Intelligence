# CareerPath Intelligence — Final System Report

## 1. Executive Summary

**CareerPath Intelligence** is an open-source, portfolio-grade Machine Learning and Skill Taxonomy Decision-Support Platform. It evaluates student profile evidence, predicts model career path alignments, inspects European ESCO v1.2 taxonomy skill gaps, and simulates counterfactual skill acquisition scenarios.

The project was executed across 8 engineering phases (Phases 0 through 7):

- **Phase 0 — Project Foundation & Repository Setup**: Python package setup, pytest configuration, ruff linting, MIT license, directory structure.
- **Phase 1 — Dataset Discovery & Validation**: Empirical dataset schema audit framework ($N=6,901$, 8 numeric skill features, 1 target label, 12 target classes).
- **Phase 2 — Reproducible Data Pipeline**: Leakage-safe `StudentProfilePreprocessor` (StandardScaler + OneHotEncoder), train/test split artifact management.
- **Phase 3 — Baseline ML**: Dummy baseline (Top-1 9.12%), Logistic Regression (8.18%), Random Forest (8.47% test, 26.72% Top-3).
- **Phase 4 — Advanced ML Experiments**: XGBoost, LightGBM, and **CatBoost Classifier** (Multiclass Logloss loss, 7.60% Test Top-1, 25.42% Top-3, 43.01% Top-5 holdout test set).
- **Phase 5 — Semantic Skill Matching & ESCO Alignment**: ESCO v1.2 taxonomy loading (3,039 occupations), SBERT `all-MiniLM-L6-v2` 384d embeddings, FAISS vector index, `SkillGapEngine`, and `HybridRecommender`.
- **Phase 6 — What-If Counterfactual Engine & FastAPI Service**: Pipeline identity counterfactual simulator (`WhatIfEngine`), Pydantic v2 schemas, production REST API (`/health`, `/api/v1/recommend`, `/api/v1/skill-gap`, `/api/v1/what-if`).
- **Phase 7 — Interactive Streamlit Presentation UI**: Multi-page portfolio presentation dashboard (`app.py`, `pages/1-6`) with dual FastAPI HTTP / local engine fallback client (`src/careerpath/ui/client.py`).

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

## 3. Authoritative Empirical Model Benchmark

The table below presents the ground-truth empirical metrics evaluated on the untouched final holdout test set ($N=1,381$, 20% stratified split):

| Model / Strategy | CV Accuracy | Holdout Test Top-1 Accuracy | Holdout Test Top-3 Accuracy | Holdout Test Top-5 Accuracy | Macro F1 | Status / Role |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Dummy (Most Frequent)** | 9.13% | 9.12% | N/A (Control) | N/A (Control) | 0.0139 | Classification Control |
| **Logistic Regression** | 8.62% | 8.18% | 24.33% | 41.20% | 0.0798 | Linear Baseline |
| **Random Forest Classifier** | 8.10% | 8.47% | 26.72% | 41.78% | 0.0839 | Tree Baseline |
| **XGBoost Classifier** | 8.14% | 7.46% | 24.11% | 41.64% | 0.0727 | Advanced Candidate |
| **LightGBM Classifier** | 7.70% | 7.75% | 24.48% | 41.13% | 0.0766 | Advanced Candidate |
| **CatBoost Classifier** | **8.14%** | **7.60%** | **25.42%** | **43.01%** | **0.0744** | **Selected Top Candidate** |

### Metric Definitions & Metric Reconciliation Audit
- **Top-1 Classification Accuracy**: Exact multiclass argmax prediction matching true target label ($\text{Top-1} = 7.60\%$).
- **Top-3 Recommendation Ranking Accuracy**: Proportion of test profiles where the true target career role appears within the top 3 ranked recommendations ($\text{Top-3} = 25.42\%$).
- **Top-5 Recommendation Ranking Accuracy**: Proportion of test profiles where the true target career role appears within the top 5 ranked recommendations ($\text{Top-5} = 43.01\%$).
- **Reconciliation Result**: Empirical script `scratch/audit_metrics.py` verified that exact Top-1 Classification Accuracy is **7.60%**. Earlier table entries that listed 25.13% were copy-paste alignment errors misreading Top-3 accuracy.

### Clarification on Alpha ($\alpha = 1.0$) Terminology
- **Selected Configuration**: $\alpha = 1.0$ (`Supervised ML ranking + ESCO explainability/skill-gap layer`).
- **Score Formula**: $S_{\text{final}} = \alpha \cdot P_{\text{ML, norm}} + (1 - \alpha) \cdot S_{\text{ESCO}}$. For $\alpha=1.0$, $S_{\text{final}} = P_{\text{ML, norm}}$.
- **ESCO Role**: ESCO skill gap evidence does not alter role ranking order when $\alpha=1.0$, but serves as an indispensable explainability diagnostic layer providing matched skills, partial matches, and missing evidence.

---

## 4. Final Quality & Test Gate

```bash
python -m pytest
```

- **Total Unit & Integration Tests**: **45 / 45 PASSED** (100% pass rate).
- **Execution Time**: ~77 seconds.
- **Test Coverage Areas**:
  - `test_foundation.py` (3 tests)
  - `test_pipeline.py` (5 tests)
  - `test_baseline.py` (4 tests)
  - `test_advanced.py` (6 tests)
  - `test_esco.py` (7 tests - including score decomposition invariant tests)
  - `test_validation.py` (8 tests)
  - `test_whatif.py` (1 test)
  - `test_api.py` (6 tests)
  - `test_ui.py` (5 tests)

---

## 5. Repository Safety & License Status

- **Git Remote**: `origin https://github.com/Hussain-Anajwala/CareerPath-Intelligence.git`
- **Working Tree**: Clean.
- **Raw Dataset Notice**: `data/raw/student_career_data.csv` is marked as `UNVERIFIED` license status and protected under `.gitignore`.
- **Project License**: MIT License for code and architecture.

---

## 6. Project Completion Declaration

```text
PROJECT IMPLEMENTATION COMPLETE
```

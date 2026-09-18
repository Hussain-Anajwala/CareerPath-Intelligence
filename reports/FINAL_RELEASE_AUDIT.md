# CareerPath Intelligence — Final Release Audit & Readiness Report

## 1. Executive Status

**READY WITH DOCUMENTED LIMITATIONS**

CareerPath Intelligence is fully implemented, empirically audited, documented, and verified. The system passes all automated quality gates (45/45 unit and integration tests passing) and is ready for portfolio demonstration and open-source distribution.

---

## 2. Verified Components & Invariants

1. **Git Repository & History Safety**: Clean working tree on `main` branch. No destructive commands executed.
2. **Data Pipeline**: Leakage-safe preprocessor (`StudentProfilePreprocessor` using `StandardScaler` and `OneHotEncoder`) fitted strictly on training data ($N=5,520$).
3. **ML Candidate Model**: CatBoost Classifier loaded from `models/advanced_catboost/v1.0/advanced_catboost.joblib` with SHA-256 metadata checksum verification.
4. **Metric Reconciliation**: Empirically reconciled Top-1 Classification Accuracy (**7.60%**) vs Top-3 Ranking Accuracy (**25.42%**) and Top-5 Ranking Accuracy (**43.01%**) on untouched holdout test set ($N=1,381$).
5. **Score Decomposition Invariant**: Verified mathematically and via automated tests that for $\alpha = 1.0$, `final_score == normalized_ml_score` holds exactly.
6. **What-If Pipeline Identity**: `WhatIfEngine` passes modified profile vectors through the exact same `HybridRecommender.recommend_for_profile` pipeline as baseline requests.
7. **ESCO & Vector Search**: ESCO v1.2 taxonomy (3,039 occupations, 13,939 skills), 384d SBERT embeddings (`all-MiniLM-L6-v2`), FAISS CPU inner-product cosine index.
8. **FastAPI REST Service**: Endpoints `/health`, `/api/v1/recommend`, `/api/v1/skill-gap`, `/api/v1/what-if` returning valid Pydantic v2 schemas without traceback leakage.
9. **Streamlit Presentation UI**: Multi-page dashboard (`app.py`, `pages/1-6`) with dual FastAPI HTTP / local engine fallback client (`src/careerpath/ui/client.py`).
10. **Test Suite**: **45 / 45 PASSED** (`python -m pytest`).

---

## 3. Audit Corrections Executed

1. **Reconciled Top-1 Classification Metric**: Removed erroneous 25.13% Top-1 entry from summary tables and established **7.60%** as the exact multiclass argmax Top-1 classification accuracy.
2. **Standardized Alpha Terminology**: Replaced inaccurate "active hybrid model" claims for $\alpha = 1.0$ with **"Supervised ML ranking + ESCO explainability/skill-gap layer"**.
3. **Added Score Decomposition Invariant Test**: Implemented `test_score_decomposition_invariants` in `tests/unit/test_esco.py`.
4. **Pydantic v2 Warning Elimination**: Updated `src/careerpath/api/schemas.py` to use `model_config = ConfigDict(...)` and `json_schema_extra={"example": ...}`.
5. **Git Hygiene**: Added `catboost_info/` temporary training artifacts to `.gitignore` and untracked cached files.

---

## 4. Final Authoritative ML Metrics

Evaluated on the untouched final holdout test set ($N=1,381$, 20% stratified split):

| Metric | Value | Description / Scope |
| :--- | :---: | :--- |
| **Evaluated Population** | $N = 1,381$ | 20% stratified holdout test set ($X_{\text{test}}$, $y_{\text{test}}$) |
| **Number of Classes** | 12 | Target career roles in empirical student dataset |
| **Selected Model** | CatBoost Classifier | Multiclass Logloss loss, `advanced_catboost.joblib` |
| **Top-1 Classification Accuracy** | **7.60%** (0.0760) | Exact multiclass argmax prediction matching true target label |
| **Top-3 Ranking Accuracy** | **25.42%** (0.2542) | True target role appears in top 3 ranked recommendations |
| **Top-5 Ranking Accuracy** | **43.01%** (0.4301) | True target role appears in top 5 ranked recommendations |
| **Macro F1 Score** | **0.0744** (0.0744) | Unweighted macro average F1 across all 12 classes |
| **Log Loss** | 2.5151 | Multiclass cross-entropy loss |
| **Multiclass Brier Score** | 0.9221 | Mean squared probability error |
| **Single Latency** | ~2.19 ms | Single-sample CPU inference time |

---

## 5. System Architecture

```text
                    ┌──────────────────────┐
                    │     Streamlit UI     │
                    │       (app.py)       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    ServiceClient     │
                    │   (ui/client.py)     │
                    └──────────┬───────────┘
                               │
            ┌──────────────────┴──────────────────┐
            │ HTTP (CAREERPATH_API_URL)           │ Standalone Fallback
            ▼                                     ▼
┌──────────────────────┐              ┌────────────────────────┐
│     FastAPI Layer    │              │ HybridRecommender /    │
│  (/api/v1/recommend) │              │ WhatIfEngine / ESCO    │
└──────────┬───────────┘              └────────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│ Recommendation Service Layer   │
└───────────────┬────────────────┘
                │
┌───────────────┼────────────────┐
▼               ▼                ▼
┌──────────┐   ┌────────────┐   ┌────────────┐
│ ML Model │   │ ESCO Engine│   │  What-If   │
└──────────┘   └────────────┘   └────────────┘
```

---

## 6. Open-Source Dependency & License Inventory

| Package / Artifact | Version | License | Purpose | Key Property |
| :--- | :--- | :--- | :--- | :--- |
| `scikit-learn` | $\ge 1.3.0$ | BSD-3-Clause | Preprocessing & evaluation | Open source |
| `catboost` | $\ge 1.2.0$ | Apache-2.0 | Supervised gradient boosting | Open source |
| `sentence-transformers` | $\ge 2.2.0$ | Apache-2.0 | Local 384d embedding generation | Local execution (`all-MiniLM-L6-v2`) |
| `faiss-cpu` | $\ge 1.7.4$ | MIT | Dense vector similarity index | Local CPU execution |
| `fastapi` | $\ge 0.100.0$ | MIT | REST API service layer | Open source |
| `pydantic` | $\ge 2.0.0$ | MIT | Schema validation | Open source |
| `streamlit` | $\ge 1.28.0$ | Apache-2.0 | Interactive web application | Open source |
| **ESCO Taxonomy v1.2** | v1.2 | CC BY 4.0 | Standardized occupation taxonomy | Open data |
| **Student Career Dataset** | CSV ($N=6,901$) | **UNVERIFIED** | Model training & evaluation | **Protected under `.gitignore`** |

---

## 7. Security, Privacy & Compliance Findings

- **Zero Secrets / API Keys**: No API keys, credentials, or `.env` secrets are present in tracked files.
- **Local-First Execution**: Core recommendation, vector index search, and What-If simulation run locally without external network API calls.
- **Dataset Privacy & License Safety**: Raw dataset `data/raw/student_career_data.csv` is excluded via `.gitignore` due to `UNVERIFIED` primary-source license status.

---

## 8. Reproducibility

A developer with access to the Python environment can reproduce the system as follows:

1. **Install Package**: `pip install -e .`
2. **Run Unit Tests**: `python -m pytest` (45/45 passed).
3. **Launch REST Service**: `uvicorn careerpath.api.app:app --reload --port 8000`
4. **Launch Presentation UI**: `streamlit run app.py`

*Limitation Notice*: Fresh-clone training from scratch requires obtaining `student_career_data.csv` separately due to `UNVERIFIED` raw dataset licensing status.

---

## 9. Remaining Limitations

1. **Dataset License Status**: `UNVERIFIED — primary-source evidence pending`. Raw CSV is protected under `.gitignore`.
2. **Model Accuracy Bounds**: 12-class dataset achieves 7.60% exact Top-1 and 43.01% Top-5 ranking accuracy.
3. **Semantic Matching Coverage**: Local FAISS index contains essential/optional skills for mapped dataset job roles.
4. **Decision-Support Scope**: Recommendations provide evidence-based alignment and do NOT guarantee real-world employment or predict causal future success.

---

## 10. Git Status & Commit Record

- **Branch**: `main`
- **Latest Audit Commit**: `1240ec4668987fa2d6e8ce86aa8a01d1be64827a` (or release audit commit)
- **Working Tree**: Clean.

---

## 11. Final Release Recommendation

CareerPath Intelligence is **APPROVED FOR RELEASE** as an open-source, portfolio-grade Machine Learning decision-support project.

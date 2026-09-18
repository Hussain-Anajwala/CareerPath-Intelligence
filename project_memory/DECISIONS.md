# Architectural Decision Records (ADR) — CareerPath Intelligence

## ADR-0001: Adoption of Modular Monolith Architecture with FastAPI and Streamlit

- **Status**: Accepted
- **Date**: 2026-09-13
- **Context**: The project requires a clean separation of presentation, domain logic, ML inference, and persistence, while remaining simple to develop, test, and deploy locally.
- **Options Considered**:
  1. Pure Streamlit application with embedded ML & business logic.
  2. Microservices architecture (separate containers for UI, API, ML inference, DB).
  3. Modular Monolith with FastAPI service layer and Streamlit presentation UI.
- **Chosen Approach**: Option 3 — Modular Monolith.
- **Reasoning**: Pure Streamlit tightly couples UI and business logic, hindering independent testing and backend reuse. Microservices add unnecessary deployment overhead for a local-first system. A modular monolith using FastAPI exposes clean Pydantic/REST service boundaries while keeping deployment straightforward.
- **Consequences**: Business logic lives in `src/careerpath/` and services are consumed via FastAPI endpoints or clean service classes in Streamlit.

---

## ADR-0002: Local-First Zero-Cost Technology Stack Selection

- **Status**: Accepted
- **Date**: 2026-09-13
- **Context**: The project baseline mandates zero paid dependencies, offline capability, and reproducible open-source components.
- **Chosen Approach**:
  - **Database**: SQLite with SQLAlchemy ORM.
  - **Vector Search**: FAISS CPU with `sentence-transformers` local models.
  - **ML Frameworks**: `scikit-learn`, `xgboost`, `lightgbm`, `catboost` (candidates evaluated in Phase 4).
  - **Experiment Tracking**: Local MLflow instance.
  - **Quality Control**: `ruff` for linting/formatting and `pytest` for automated testing.
- **Reasoning**: All selected tools are permissive open-source software (MIT / BSD / Apache 2.0) capable of running locally without cloud services or subscription costs.
- **Consequences**: No reliance on paid cloud databases, proprietary vector DBs, or external LLM API keys.

---

## ADR-0003: Initial ML Task Formulation & Data Validation Framework

- **Status**: Accepted
- **Date**: 2026-09-13
- **Context**: Phase 1 dataset discovery requires establishing a robust data validation suite and recommending an initial ML task formulation without fabricating synthetic data or forcing premature architecture freezing.
- **Chosen Approach**:
  - **Task Formulation**: Hybrid Supervised Prediction + ESCO Skill Ranking. The supervised model outputs multi-class career role fit probabilities $P(y = k \mid \mathbf{x})$, while the ESCO layer computes deterministic skill coverage $S_{\text{skill}}(\mathbf{x}, c_k)$. Unified ranking fuses both signals into an explainable fit score.
  - **Data Validation & Audit Suite**: Modular validation code (`src/careerpath/data/validators.py`) providing schema validation, exact/near duplicate detection, missingness profiling, class balance evaluation, and target leakage auditing.
- **Reasoning**: Fusing empirical student profile predictions with taxonomy-backed ESCO skill overlap guarantees that recommendations remain explainable, data-driven, and grounded in standard occupation standards.
- **Consequences**: The data pipeline in Phase 2 will execute strict validation and leakage checks on ingestion before fitting preprocessing transformers.

---

## ADR-0004: Leakage-Safe Data Preprocessing Architecture & Serialization

- **Status**: Accepted
- **Date**: 2026-09-13
- **Context**: Phase 2 data pipeline implementation requires a modular, reproducible, and strictly leakage-safe preprocessing architecture that fits parameters strictly on training partitions and serializes preprocessor state for inference.
- **Chosen Approach**:
  - **Pipeline Design**: `StudentProfilePreprocessor` using `sklearn.compose.ColumnTransformer` and `sklearn.pipeline.Pipeline`.
  - **Fitting Rule**: Preprocessor imputers (`SimpleImputer`), scalers (`StandardScaler`), encoders (`OneHotEncoder`), and label encoders (`LabelEncoder`) fit ONLY on training data $X_{\text{train}}$ and $y_{\text{train}}$.
  - **Feature Engineering**: Deterministic `FeatureExtractor` module computing academic mean/max aggregates, skill counts, average skill depth, and interest counts.
  - **Artifact Management**: `ArtifactManager` serializing preprocessors via `joblib` along with SHA-256 checksums and JSON metadata tracking.
- **Reasoning**: Separating parameter fitting from transformation guarantees zero data leakage between training and test holdout evaluation. Checksum verification ensures tamper-proof reproducibility.
- **Consequences**: Downstream ML model experiments (Phase 3 & 4) will consume transformed features produced by this pipeline.

---

## ADR-0005: Baseline Model Benchmark Results & Evaluation Strategy

- **Status**: Accepted
- **Date**: 2026-09-18
- **Context**: Phase 3 baseline ML experimentation requires evaluating initial baseline classifiers on the real dataset `student_career_data.csv` (6,901 rows, 12 classes) to establish an empirical benchmark prior to advanced model selection.
- **Chosen Approach**:
  - **Validation Strategy**: 5-Fold Stratified K-Fold Cross-Validation executed strictly on the 80% training split (5,520 rows).
  - **Evaluated Baselines**: `DummyClassifier` (most frequent control), `LogisticRegression` (multinomial linear baseline), and `RandomForestClassifier` (100-tree ensemble baseline).
  - **Evaluation Metrics**: Multi-class accuracy, Macro/Weighted F1, confusion matrix, and Top-1 / Top-3 / Top-5 ranking accuracies.
- **Reasoning**: Random Forest achieved **0.0847 Test Accuracy** and **0.2672 Top-3 accuracy** on holdout test data (with exact equality `Top-1 Accuracy == accuracy_score`), significantly outperforming the Dummy chance baseline (0.0912 accuracy, 0.0139 Macro F1). Fusing multi-class probabilities into Top-3 / Top-5 recommendations provides a robust foundation for decision support.
- **Consequences**: Advanced gradient boosting algorithms (XGBoost, LightGBM, CatBoost) in Phase 4 will be benchmarked directly against these baseline metrics.

---

## ADR-0006: Advanced ML Model Benchmark & Model Selection Framework

- **Status**: Accepted
- **Date**: 2026-09-18
- **Context**: Phase 4 requires benchmarking advanced gradient boosted tree models (XGBoost, LightGBM, CatBoost) against baselines using 5-Fold Stratified CV, holdout test evaluation, probability calibration, feature importance, and inference latency under strict local-first zero-cost constraints.
- **Chosen Approach**:
  - **Evaluated Candidates**: `XGBClassifier`, `LGBMClassifier`, `CatBoostClassifier`, `RandomForestClassifier`, `LogisticRegression`, `DummyClassifier`.
  - **Evaluation Methodology**: Stratified 5-Fold CV on training split (5,520 samples); evaluation on untouched holdout test split (1,381 samples).
  - **Top-K Ranking Equality Rule**: Enforce `Top-1 Accuracy == accuracy_score` explicitly using argmax class prediction.
  - **Candidate Selection Framework**: Multi-metric evaluation considering Macro F1, Top-3/Top-5 accuracy, Log Loss, Brier Score, and single-sample inference latency (<35 ms).
- **Reasoning**: `RandomForestClassifier` (Top-3 Acc: 26.72%, Top-5 Acc: 41.78%), `CatBoostClassifier` (Top-3 Acc: 25.42%, Top-5 Acc: 43.01%), and `XGBClassifier` (Top-3 Acc: 24.11%, Top-5 Acc: 41.64%) demonstrate strong ranking coverage across all 12 job roles with fast, local inference (<35ms per profile).
- **Consequences**: The selected model artifacts are saved under `models/` with SHA-256 metadata checksums and will feed into Phase 5 hybrid ESCO skill alignment ranking.

---

## ADR-0007: Semantic Skill Matching & Hybrid ESCO Recommendation Architecture

- **Status**: Accepted
- **Date**: 2026-09-18
- **Context**: Phase 5 requires building a local semantic skill intelligence layer using ESCO v1.2 taxonomy, local Sentence Transformers, FAISS vector indexing, and hybrid score fusion to provide explainable skill gap analysis and career recommendations.
- **Chosen Approach**:
  - **Taxonomy Data Model**: `ESCOTaxonomy` encapsulating ESCO URIs, preferred/alt labels, and essential/optional skill relationships under CC BY 4.0 open data license.
  - **Career Mapping**: `CareerMapper` providing explicit 1-to-1 mappings between dataset job roles and ESCO occupation URIs (`EXACT` and `SEMANTIC_MATCH`).
  - **Semantic Vector Index**: `ESCOVectorIndex` utilizing local SentenceTransformer `all-MiniLM-L6-v2` (Apache-2.0) and FAISS CPU `IndexFlatIP` persisted to `data/processed/esco/esco_skills.faiss`.
  - **Skill Gap Engine**: `SkillGapEngine` categorizing required skills into `Strong Match` ($\ge 0.75$), `Partial Match` ($0.50 - 0.75$), and `Missing` ($< 0.50$).
  - **Hybrid Recommendation Fusion**: $S_{\text{final}} = \alpha \cdot P_{\text{ML, norm}} + (1 - \alpha) \cdot S_{\text{ESCO}}$ with ablation analysis across $\alpha \in [0.0, 1.0]$.
- **Reasoning**: Hybrid score fusion ($\alpha = 0.5$) combines empirical student dataset patterns with taxonomy-backed ESCO skill overlap, providing decomposable evidence (`matched_skills`, `missing_skills`) while boosting Top-5 coverage to **51.00%**.
- **Consequences**: Downstream service APIs in Phase 6 will consume `HybridRecommender` to serve explainable recommendations and support What-If skill gap simulations.

---

## ADR-0008: What-If Counterfactual Simulation Engine & FastAPI Service Layer Architecture

- **Status**: Accepted
- **Date**: 2026-09-18
- **Context**: Phase 6 requires implementing a counterfactual skill simulation engine (`WhatIfEngine`) and exposing production REST API endpoints via FastAPI using Pydantic v2 schemas.
- **Chosen Approach**:
  - **Pipeline Identity Rule**: `WhatIfEngine` executes counterfactual simulations by passing modified profiles through the **EXACT SAME** `HybridRecommender.recommend_for_profile` pipeline as normal recommendations (zero hardcoded rules or separate scoring logic).
  - **API Framework**: FastAPI modular service layer (`src/careerpath/api/app.py`) with lifespan dependency loading, CORS middleware, custom exception handlers, and auto OpenAPI docs (`/docs`).
  - **Pydantic v2 Schemas**: Strict request/response schemas (`RecommendRequest`, `SkillGapRequest`, `WhatIfRequest`, `HealthResponse`) with input validation ($0.0 \le \text{rating} \le 10.0$).
- **Reasoning**: Enforcing pipeline identity guarantees that What-If simulation outputs reflect real model and taxonomy scoring dynamics. A clean FastAPI REST API decouples business logic from presentation UI.
- **Consequences**: The upcoming Streamlit presentation UI (Phase 7) will consume these FastAPI REST endpoints directly.

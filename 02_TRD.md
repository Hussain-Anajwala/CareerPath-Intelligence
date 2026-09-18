# CareerPath Intelligence — Technical Requirements & Design Document (TRD)

**Version:** 1.0-draft  
**Status:** Draft pending dataset validation  
**Architecture principle:** Local-first, modular, reproducible, explainable, zero-cost core

---

## 1. Technical Objective

Build a maintainable Python application that separates:

1. UI/presentation.
2. API/service boundaries.
3. Input validation.
4. Feature engineering.
5. ML inference.
6. Career ranking.
7. Semantic skill matching.
8. Skill-gap analysis.
9. Explainability.
10. What-If simulation.
11. Persistence.
12. Experiment tracking and model artifacts.

The architecture must allow the model to change after experimentation without requiring a redesign of the UI or persistence layer.

## 2. Architecture Decision

### 2.1 Selected shape

```text
Streamlit UI
    |
    v
FastAPI Service Layer
    |
    +--> Validation
    +--> Profile transformation
    +--> Recommendation service
    +--> Skill-gap service
    +--> What-If service
    +--> Persistence service
    |
    +-------------------------------+
    |                               |
    v                               v
ML/Recommendation Core         SQLite/SQLAlchemy
    |
    +--> Predictive Model
    +--> Career Ranker
    +--> Explainability
    +--> Semantic Skill Matcher
    +--> ESCO reference data
    +--> FAISS local index
```

Offline training/research is separate:

```text
Dataset
  -> Validation
  -> EDA
  -> Preprocessing
  -> Feature Engineering
  -> Baselines
  -> Advanced Models
  -> Cross-Validation
  -> Tuning
  -> Evaluation
  -> Error Analysis
  -> Model Selection
  -> Versioned Artifact
```

### 2.2 Why not microservices?

The internship baseline does not require microservices. They would add operational complexity without a demonstrated need. The system therefore uses a modular monolith with a clean API boundary.

### 2.3 Why FastAPI + Streamlit?

Streamlit satisfies the required interactive application scope while FastAPI provides a clean service boundary that can be tested independently and keeps model logic out of the UI layer.

## 3. Technology Stack

| Layer | Technology | Role | Status |
|---|---|---|---|
| Runtime | Python 3.11+ | Main language | Required |
| Data | pandas | Tabular data | Required |
| Numerical | NumPy | Numerical operations | Required |
| Classical ML | scikit-learn | Baselines/preprocessing/metrics | Required |
| Gradient boosting | XGBoost | Candidate model | Optional experiment |
| Gradient boosting | LightGBM | Candidate model | Optional experiment |
| Gradient boosting | CatBoost | Candidate model | Optional experiment |
| Deep learning | PyTorch | MLP experiment | Optional |
| Embeddings | sentence-transformers | Semantic matching | P1 |
| Vector search | FAISS CPU | Local similarity | P1 |
| Explainability | SHAP | Feature contributions | P0/P1 depending on selected model |
| API | FastAPI + Pydantic | Service boundary | P1 |
| UI | Streamlit | Web application | P0 |
| Persistence | SQLite + SQLAlchemy | Local database | P1 |
| Experiment tracking | MLflow | Local experiment tracking | P1 |
| Testing | pytest | Automated tests | P0 |
| Quality | Ruff | Lint/format | P1 |
| CI | GitHub Actions | Checks | P1 |
| Packaging | pyproject.toml | Environment/build metadata | P0 |

## 4. Open-Source and Zero-Cost Policy

### 4.1 Hard rule

The core product shall run without:

- Paid API keys.
- Paid model inference endpoints.
- Mandatory hosted databases.
- Mandatory cloud object storage.
- Managed vector databases.
- Proprietary runtime dependencies.

### 4.2 License baseline

The currently checked project licenses support the chosen core stack. scikit-learn is distributed under the BSD 3-Clause license; XGBoost uses Apache 2.0; LightGBM uses MIT; CatBoost uses Apache 2.0; Sentence Transformers uses Apache 2.0; FAISS uses MIT; FastAPI uses MIT; Streamlit uses Apache 2.0; SQLAlchemy uses MIT; MLflow is Apache 2.0; SHAP is MIT; pandas is BSD 3-Clause; pytest is MIT; and Ruff is MIT. These checks should be treated as a current verification, not a perpetual guarantee. License files must be preserved/inventoried for the exact dependency versions used by the project.

### 4.3 Data license requirement

Software licensing alone does not make the project legally clean. Every dataset and pretrained model must have its own documented license/terms.

For ESCO, the European Commission states that the classification can be downloaded, used, reproduced, and reused free of charge subject to acknowledgement and conditions; adapted versions must be clearly identified. The project shall therefore include the required ESCO acknowledgement and record the exact ESCO version used.

### 4.4 Model-weight policy

A library may be open source while a specific model checkpoint has a different license. Every downloaded embedding checkpoint must be recorded in `MODEL_CARD.md` or `THIRD_PARTY_NOTICES.md` with:

- Model name.
- Source URL.
- Version/revision.
- License.
- Intended use.
- Local file hash.
- Whether it is redistributable.

### 4.5 CI license control

The repository should generate a dependency/license report in CI using a local package inspection tool. The exact tool can be selected during implementation, but the process must detect unexpected or incompatible licenses before release.

## 5. Python Project Structure

Recommended structure:

```text
careerpath-intelligence/
├── app/
│   └── streamlit_app.py
├── src/
│   └── careerpath/
│       ├── api/
│       │   ├── routes_profile.py
│       │   ├── routes_recommendation.py
│       │   ├── routes_career.py
│       │   └── routes_simulation.py
│       ├── config/
│       ├── data/
│       │   ├── loaders.py
│       │   ├── validators.py
│       │   └── schemas.py
│       ├── db/
│       │   ├── models.py
│       │   ├── session.py
│       │   └── repositories.py
│       ├── ml/
│       │   ├── preprocessing.py
│       │   ├── features.py
│       │   ├── train.py
│       │   ├── evaluate.py
│       │   └── inference.py
│       ├── recommendation/
│       │   ├── ranker.py
│       │   ├── evidence.py
│       │   ├── readiness.py
│       │   └── actions.py
│       ├── skills/
│       │   ├── normalization.py
│       │   ├── embeddings.py
│       │   ├── faiss_index.py
│       │   └── gap_engine.py
│       ├── explainability/
│       │   └── shap_explainer.py
│       └── simulation/
│           └── what_if.py
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── reference/
├── models/
├── experiments/
├── tests/
├── notebooks/
├── scripts/
├── docs/
├── project_memory/
├── artifacts/
├── pyproject.toml
├── README.md
├── LICENSE
└── THIRD_PARTY_NOTICES.md
```

## 6. ML Task Formulation

### 6.1 Decision gate

Do not hard-code the ML problem until dataset inspection confirms whether the available target and labels support:

- Multiclass classification.
- Multi-label classification.
- Ranking.
- Hybrid prediction + structured ranking.

### 6.2 Recommended product architecture

Even if the predictive model is classification, the user-facing system should convert model outputs into a ranked recommendation list.

Potential flow:

```text
Model probabilities/scores
        +
Skill alignment evidence
        +
Interest/domain evidence
        +
Validated constraints
        |
        v
Career ranking
```

The exact fusion formula shall be established through an experiment/decision record rather than invented in the UI.

## 7. Data Pipeline

```text
Source Data
  -> Schema Check
  -> Missing/duplicate checks
  -> Type/category validation
  -> Leakage checks
  -> EDA
  -> Preprocessing
  -> Feature engineering
  -> Train/validation/test split
  -> Training
  -> Evaluation
  -> Artifact generation
```

### 7.1 Leakage prevention

The preprocessing pipeline must be fit on training data only. Any target-derived feature, post-outcome field, duplicate representation of the label, or data collected after the prediction point must be treated as a potential leakage source.

### 7.2 Dataset versioning

Record:

- Source name.
- Retrieval date.
- Original filename/URL where allowed.
- Dataset version.
- Row count.
- Column count.
- Schema hash.
- File hash where practical.
- License/terms.
- Preprocessing version.

## 8. Feature Engineering

The feature pipeline should be modular and deterministic.

Candidate feature groups:

- Academic features.
- Normalized skill features.
- Interest/category features.
- User preference features.
- Skill-count/coverage features.
- Semantic skill-alignment features, if validated.

Do not add engineered features merely because they can be computed. Each feature should have a documented purpose and leakage assessment.

## 9. Model Experiment Strategy

### Baseline

Start with simple models to establish a reference point:

- Logistic Regression where appropriate.
- Decision Tree/Random Forest where appropriate.
- A simple ranking baseline if the task is ranking.

### Advanced candidates

- XGBoost.
- LightGBM.
- CatBoost.
- PyTorch MLP if justified by dataset size/task structure.

### Evaluation

Candidate metrics depend on the final task. Possible measures include:

- Accuracy.
- Precision.
- Recall.
- F1.
- ROC-AUC where meaningful.
- Confusion matrix.
- Top-k hit rate / recall.
- NDCG or other ranking measures.
- Inference latency.

No metric value may be claimed in documentation until it is measured.

## 10. Cross-Validation and Model Selection

Use an appropriate validation strategy based on the final dataset and class distribution.

Examples:

- Stratified K-fold for balanced multiclass classification.
- Group-aware split if rows are grouped by a person/source.
- Time-aware split if there is a temporal signal.

Model selection must consider more than a single score. The final decision should document:

- Performance.
- Stability across folds.
- Error patterns.
- Calibration/uncertainty considerations where relevant.
- Runtime/size.
- Explainability support.
- Maintainability.


### 10.1 Probability calibration and uncertainty

If the final task produces probabilities that are exposed to users, calibration shall be assessed on a validation set. Do not label raw model probabilities as reliable confidence without evidence. Depending on the final model/task, calibration methods may include Platt scaling or isotonic regression. If calibration is not justified, expose a qualitative strength/uncertainty label instead.

### 10.2 Error and slice analysis

Perform structured error analysis on:

- Overall performance.
- Common confusion pairs or ranking failures.
- Sparse profiles.
- Ambiguous profiles.
- Out-of-distribution-like profiles where detectable.
- Available non-sensitive dataset slices when appropriate.

Do not create sensitive attributes purely for fairness analysis.

## 11. Explainability Architecture

### 11.1 Goal

Generate evidence that helps the user understand the recommendation, not a mathematically complete explanation of every internal operation.

### 11.2 Primary approach

Use SHAP where it is technically appropriate for the selected model.

Fallbacks:

- Built-in feature importance for suitable tree models.
- Coefficient-based contributions for linear models.
- Deterministic skill-overlap evidence.

### 11.3 Explanation contract

Every recommendation response should have a structured evidence object:

```json
{
  "career_id": "career-123",
  "rank": 1,
  "score": 0.81,
  "confidence_label": "moderate",
  "evidence": [
    {"type": "feature", "name": "python_skill", "direction": "positive", "importance": 0.19},
    {"type": "skill_match", "skill": "SQL", "status": "matched"},
    {"type": "skill_gap", "skill": "statistics", "status": "missing"}
  ]
}
```

The exact response schema may be refined after the dataset and model are fixed.

## 12. Semantic Skill Matching

### 12.1 Inputs

- User skill strings.
- Canonical skill labels.
- Occupation skill descriptions.

### 12.2 Pipeline

```text
Raw Skill Text
     |
     +--> exact/controlled vocabulary match
     |
     +--> normalized text match
     |
     +--> sentence embedding
     |
     +--> FAISS similarity search
     |
     +--> threshold + validation
     |
     v
Canonical Skill
```

### 12.3 Guardrails

Semantic similarity shall not automatically equal equivalence. Use:

- Similarity thresholds.
- Optional top-k candidates.
- Abbreviation/alias rules.
- Rejection for low similarity.
- Evidence display for normalized matches.

## 13. ESCO Integration

ESCO is the preferred external occupation/skill reference from the scope baseline.

Store a normalized local subset sufficient for the project rather than making a live external request.

Recommended data concepts:

- `occupation_uri`
- `occupation_label`
- `skill_uri`
- `skill_label`
- `occupation_skill_relation`
- Optional skill type/category fields where useful.

The exact subset shall be versioned and accompanied by attribution.

## 14. Recommendation Engine

The engine consists of independent stages:

1. Validate profile.
2. Normalize skills.
3. Generate model features.
4. Obtain predictive scores.
5. Generate semantic/structured skill evidence.
6. Compute career ranking.
7. Compute skill gaps.
8. Compute readiness/alignment.
9. Build evidence.
10. Return a versioned recommendation result.

### 14.1 Recommendation object

Conceptual fields:

```text
RecommendationRun
 ├── run_id
 ├── model_version
 ├── preprocessing_version
 ├── input_snapshot
 ├── generated_at
 └── recommendations[]
       ├── career_id
       ├── rank
       ├── score
       ├── confidence
       ├── evidence[]
       ├── matched_skills[]
       └── gaps[]
```

## 15. Readiness/Alignment Engine

Readiness must be a product indicator, not an employment probability.

Possible components:

```text
Readiness/Alignment
= weighted evidence from
  profile fit
  + skill coverage
  + validated preference/interest alignment
```

Weights must be versioned and documented.

If the dataset does not support meaningful proficiency levels, readiness must not imply that the student meets a required proficiency threshold that the source data never provided.

## 16. What-If Engine

### 16.1 Principle

The What-If engine shall use the **same preprocessing, model, scoring, semantic matching, and ranking pipeline** as the normal recommendation flow.

### 16.2 Flow

```text
Original Profile
      |
      +--> Baseline Result
      |
Hypothetical Skill Changes
      |
      +--> Validate scenario
      +--> Apply changes in memory
      +--> Run same pipeline
      |
      +--> Scenario Result
      |
      +--> Difference Engine
             |
             +--> Rank changes
             +--> Score changes
             +--> Readiness changes
             +--> Evidence changes
```

No simulated outcome may be described as causal or guaranteed.

## 17. API Design

### 17.1 Suggested endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/profile/validate` | Validate profile |
| POST | `/api/v1/recommendations` | Generate recommendations |
| GET | `/api/v1/careers` | List supported careers |
| GET | `/api/v1/careers/{career_id}` | Career details |
| POST | `/api/v1/careers/{career_id}/skill-gap` | Calculate skill gaps |
| POST | `/api/v1/what-if` | Evaluate hypothetical profile |
| GET | `/api/v1/methodology` | Model/data metadata |
| GET | `/api/v1/health` | Service health |

Persistence endpoints are optional and should only be exposed where needed.

### 17.2 Request validation

Pydantic models shall validate:

- Required fields.
- Ranges.
- Enumerated categories.
- Skill structures.
- Scenario changes.

### 17.3 Error contract

```json
{
  "error_code": "INVALID_PROFILE",
  "message": "Some profile fields need attention.",
  "details": [
    {"field": "academic_score", "reason": "Value is outside supported range."}
  ]
}
```

## 18. Persistence

SQLite shall be the baseline local database.

SQLAlchemy shall provide ORM/repository access.

Persistence should store:

- Anonymous profile snapshots where enabled.
- Recommendation runs.
- Career recommendations.
- Skill gaps.
- What-If scenarios.
- Experiment metadata if desired.

Raw sensitive information should not be collected by default.

## 19. Model and Dataset Cards

Each selected model should have a lightweight Model Card containing:

- Model/task purpose.
- Training data/version.
- Feature groups.
- Evaluation methodology.
- Measured metrics.
- Calibration/uncertainty method if applicable.
- Known failure modes.
- Intended use.
- Prohibited/non-intended use.
- Version and checksum.

The dataset should have a Dataset Card containing:

- Source/provenance.
- License/terms.
- Retrieval date.
- Version/hash.
- Schema.
- Missing-data characteristics.
- Known limitations and representativeness concerns.

## 20. Model Artifact Packaging

Each selected model artifact should have:

```text
models/<model_name>/<version>/
    model artifact
    metadata.json
    feature_schema.json
    preprocessing_config.json
    evaluation.json
    checksum.txt
```

`metadata.json` should include:

- Model name/version.
- Training dataset version/hash.
- Code version/commit.
- Feature schema version.
- Training timestamp.
- Evaluation summary.
- Random seed where relevant.

## 21. MLflow Usage

MLflow should be self-hosted/locally run for experiment tracking.

Track:

- Parameters.
- Metrics.
- Dataset version/hash.
- Feature configuration.
- Model family.
- Artifact path.
- Decision status.

The core application must not depend on a remote MLflow server.

## 22. Testing Strategy

### Unit tests

- Feature transformations.
- Skill normalization.
- Scoring.
- Skill-gap calculations.
- Readiness formula.
- What-If differences.

### Data tests

- Required columns.
- Valid ranges.
- Duplicate detection.
- Category validity.
- Leakage checks.

### Model tests

- Artifact loading.
- Input schema compatibility.
- Deterministic inference for fixed inputs.
- Probability/score shape checks.

### API tests

- Valid payloads.
- Invalid payloads.
- Error responses.
- Version metadata.

### UI tests

Verify primary workflow manually and with lightweight automated checks where practical.

## 23. Security and Privacy

- No secrets in source control.
- Environment variables for any future optional integration.
- No unnecessary PII.
- Anonymous/local profiles preferred.
- Local database by default.
- No raw user input sent to a third-party LLM because no LLM is required.
- If optional future integrations are added, document data flow and opt-in behavior.

## 24. Performance Targets

No arbitrary production SLA is required for the internship prototype.

Development targets:

- Application startup should be practical on ordinary hardware.
- Recommendation inference should feel interactive for a single user.
- Semantic search should use a prebuilt local FAISS index.
- Models should be loaded once per application process where possible.

Actual timings shall be recorded as measured observations.

## 25. Deployment

Primary target:

```text
Developer Machine
  -> virtual environment
  -> install dependencies
  -> load data/model artifacts
  -> start FastAPI
  -> start Streamlit
```

Optional free demo deployment may be considered only after local reproducibility is proven and only if it preserves the project’s zero-cost goal.

## 26. Dependency and Supply-Chain Controls

At release:

- Pin dependency versions using a lockfile or equivalent reproducible mechanism.
- Record license inventory.
- Run vulnerability scanning where practical.
- Record external model licenses.
- Record data licenses and attribution.
- Avoid dependencies that are unused by the running core path.

## 27. Observability

For a local prototype, structured logs are sufficient.

Log:

- Application version.
- Model version.
- Recommendation request ID.
- Execution duration.
- Error code.

Do not log unnecessary personal profile values.

## 28. Architecture Invariants

1. Core recommendations do not require an external LLM.
2. Core recommendations do not require paid APIs.
3. Core persistence does not require a cloud database.
4. The same model pipeline powers standard and What-If inference.
5. Model selection follows measured experiments.
6. User-facing explanations must be evidence-linked.
7. Dataset and model versions are traceable.
8. Material architectural changes require ADR/decision-log updates.

## 29. Technical Open Decisions

Pending actual dataset:

- Exact target/task.
- Feature list.
- Final model.
- Score fusion strategy.
- Confidence approach.
- Readiness formula.
- ESCO subset.
- Exact embedding model.
- Persistence depth.


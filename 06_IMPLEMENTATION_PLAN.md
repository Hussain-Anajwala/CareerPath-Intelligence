# CareerPath Intelligence — Implementation Plan

**Version:** 1.0-draft  
**Objective:** Build a resume-worthy, evidence-backed, open-source, zero-cost career intelligence project using a disciplined ML + software engineering workflow.

---

## 1. Implementation Strategy

The project will be built in gated phases. A later phase must not silently assume that an earlier scientific decision is correct.

```text
Scope baseline
    ↓
Dataset validation gate
    ↓
PRD/TRD confirmation
    ↓
ML experiments
    ↓
Recommendation intelligence
    ↓
Backend
    ↓
UI/UX
    ↓
Integration
    ↓
Testing
    ↓
Reproducibility + license audit
    ↓
Demo + final documentation
```

## 2. Phase 0 — Repository and Agent Setup

### Objectives

Create a stable project foundation before implementing features.

### Tasks

- Initialize Git repository.
- Create Python package structure.
- Add `pyproject.toml`.
- Add formatting/linting configuration.
- Add pytest.
- Add CI workflow.
- Add project memory files.
- Add docs directory.
- Add license/third-party notice placeholders.
- Add `.gitignore`.

### Deliverables

```text
PROJECT_CONTEXT.md
CURRENT_STATE.md
INVARIANTS.md
DECISIONS.md
HANDOFF.md
CHANGELOG.md
```

### Gate

A clean clone can create the local environment and run a hello-world test suite.

## 3. Phase 1 — Dataset Validation

### Objective

Determine what the actual dataset can support.

### Tasks

1. Identify dataset files/source.
2. Inspect schema.
3. Profile target labels.
4. Analyze missing values.
5. Analyze duplicates.
6. Check category cardinality.
7. Check class imbalance.
8. Detect potential leakage.
9. Determine whether classification/ranking/hybrid is justified.
10. Document data license/terms.
11. Decide how career labels map to supported careers.

### Deliverables

```text
notebooks/01_data_profile.ipynb
reports/DATASET_AUDIT.md
experiments/dataset_manifest.json
```

### Gate

Do not freeze the model/task before this phase is complete.

## 4. Phase 2 — Data Pipeline

### Objective

Create reproducible data loading and preprocessing.

### Tasks

- Implement source loaders.
- Implement schema validation.
- Implement missing-value policy.
- Implement duplicate checks.
- Implement train/validation/test split.
- Implement preprocessing pipeline.
- Implement feature schema.
- Add leakage tests.
- Generate versioned processed data.

### Deliverables

```text
src/careerpath/data/
src/careerpath/ml/preprocessing.py
data/processed/
```

### Gate

The same input + same code/configuration produces the same processed schema.

## 5. Phase 3 — Baseline ML

### Objective

Establish a simple performance reference.

### Candidate baselines

- Logistic Regression where appropriate.
- Random Forest where appropriate.
- Simple rule/ranking baseline.

### Tasks

- Define evaluation split.
- Train baselines.
- Cross-validate where appropriate.
- Produce confusion matrix/ranking metrics.
- Record runtime.
- Inspect errors.

### Deliverables

```text
experiments/baseline/
MLFLOW local runs
reports/BASELINE_RESULTS.md
```

### Gate

There must be a measured baseline before advanced models are selected.

## 6. Phase 4 — Advanced Model Experiments

### Objective

Compare stronger models objectively.

### Candidates

- XGBoost.
- LightGBM.
- CatBoost.
- MLP/PyTorch if justified.

### Evaluation dimensions

- Predictive performance.
- Stability across validation.
- Error patterns.
- Class/rank coverage.
- Inference cost.
- Explainability.

### Deliverables

```text
experiments/model_comparison/
reports/MODEL_SELECTION.md
models/<selected-model>/
```

### Gate

The selected model must be supported by actual evidence.

## 7. Phase 5 — Career Taxonomy and Skill Normalization

### Objective

Create a reliable career/skill reference layer.

### Tasks

- Obtain documented ESCO release/version.
- Record attribution/license information.
- Extract only required occupation/skill data.
- Build canonical IDs.
- Create alias/normalization rules.
- Add exact matching.
- Add semantic matching only after testing.

### Deliverables

```text
data/reference/esco/
src/careerpath/skills/normalization.py
reports/SKILL_MATCHING_EVALUATION.md
THIRD_PARTY_NOTICES.md
```

### Gate

Semantic matching must demonstrate useful behavior on a manually reviewed test set before becoming a critical dependency.

## 8. Phase 6 — Semantic Matching + FAISS

### Objective

Add local semantic matching as a differentiator.

### Tasks

1. Select an embedding model with compatible license.
2. Download locally.
3. Record source and hash.
4. Generate career/skill embeddings.
5. Build FAISS CPU index.
6. Implement top-k search.
7. Define similarity threshold.
8. Evaluate false matches.

### Gate

Exact matches should continue to work independently. Semantic matching should be auditable.

## 9. Phase 7 — Recommendation Intelligence

### Objective

Create the core recommendation service.

### Components

- Input validation.
- Feature preparation.
- ML inference.
- Career ranking.
- Evidence generation.
- Skill-gap engine.
- Readiness/alignment.
- Development actions.

### Deliverables

```text
src/careerpath/recommendation/
src/careerpath/explainability/
src/careerpath/skills/gap_engine.py
```

### Gate

Given a fixed profile and model version, the service produces deterministic, traceable output.

## 10. Phase 8 — What-If Engine

### Objective

Implement the core differentiator without creating a second ML implementation.

### Tasks

- Clone baseline profile in memory.
- Apply supported hypothetical changes.
- Reuse same inference pipeline.
- Calculate before/after comparison.
- Calculate rank movement.
- Calculate evidence differences.
- Add interpretation disclaimer.

### Gate

A regression test must prove that the scenario path uses the same model/preprocessing versions as the baseline path.

## 11. Phase 9 — Persistence Layer

### Tasks

- Implement SQLAlchemy models.
- Create migrations.
- Create repositories.
- Add SQLite initialization.
- Save recommendation runs.
- Save skill gaps.
- Save optional What-If scenarios.

### Gate

A fresh database can be created from migrations and reference-data loading scripts.

## 12. Phase 10 — FastAPI Service

### Tasks

Implement:

```text
POST /api/v1/profile/validate
POST /api/v1/recommendations
GET  /api/v1/careers
GET  /api/v1/careers/{career_id}
POST /api/v1/careers/{career_id}/skill-gap
POST /api/v1/what-if
GET  /api/v1/methodology
GET  /api/v1/health
```

Add Pydantic schemas and error contracts.

### Gate

API tests pass for valid and invalid payloads.

## 13. Phase 11 — Streamlit UI

### Implementation order

1. Landing.
2. Profile builder.
3. Validation UI.
4. Results.
5. Career detail.
6. Skill gaps.
7. Readiness.
8. What-If Lab.
9. Methodology.
10. About/limitations.

### Gate

A first-time user can complete the full main journey without developer assistance.

## 14. Phase 12 — Integration

Connect:

```text
Streamlit
   ↓
FastAPI
   ↓
Recommendation services
   ↓
ML + skills + persistence
```

### Tests

- End-to-end happy path.
- Invalid input.
- Low-confidence result.
- Career detail.
- What-If.
- Database optional/disabled behavior.
- Missing artifact behavior.

## 15. Phase 13 — Testing and Quality

### Required test groups

```text
tests/
├── unit/
├── data/
├── ml/
├── recommendation/
├── api/
├── integration/
└── regression/
```

### Regression scenarios

Maintain a small fixed set of representative profiles:

- Strong data profile.
- Strong software profile.
- Mixed/ambiguous profile.
- Sparse profile.
- Invalid profile.

Record expected invariants rather than hard-coding unstable model scores.

## 16. Phase 14 — Reproducibility Audit

A new developer should be able to:

1. Clone repository.
2. Install pinned dependencies.
3. Obtain/load documented data.
4. Load model artifacts.
5. Start backend.
6. Start UI.
7. Run tests.
8. Reproduce documented experiment outputs.

### Deliverables

```text
README.md
SETUP.md
REPRODUCIBILITY.md
```

## 17. Phase 15 — Model Cards and Responsible-Use Review

Before release, create:

- `docs/MODEL_CARD.md`
- `docs/DATASET_CARD.md`
- `docs/RESPONSIBLE_USE.md`

The review must cover intended use, non-intended use, data provenance, limitations, measured model performance, uncertainty/calibration where applicable, and observed error/bias patterns.

## 18. Phase 16 — Open-Source / License Audit

Before release:

- [ ] All direct dependencies identified.
- [ ] Exact versions recorded.
- [ ] Licenses checked.
- [ ] Third-party notices generated.
- [ ] Dataset terms recorded.
- [ ] ESCO attribution included.
- [ ] Embedding model license recorded.
- [ ] Model weights' redistribution terms checked.
- [ ] No paid API key required by core path.
- [ ] No secret values committed.

## 19. Phase 17 — Performance and Robustness Review

Measure rather than guess:

- App startup time.
- Model loading time.
- Inference time.
- Skill matching time.
- What-If execution time.
- Peak local memory for typical test run.

These are development observations, not guaranteed production SLAs.

## 20. Phase 18 — Demo and Portfolio Packaging

### Demo story

The final demo should emphasize:

1. Student enters profile.
2. System ranks multiple careers.
3. User opens a recommended career.
4. System explains why.
5. User sees skill gaps.
6. User opens What-If.
7. User improves a skill hypothetically.
8. Ranking changes.
9. Methodology shows how the system was evaluated.

### Portfolio assets

- Architecture diagram.
- Model comparison table using measured results.
- Explainability screenshot.
- Skill-gap screenshot.
- What-If screenshot.
- Test/CI evidence.
- Reproducibility instructions.

## 21. Suggested Milestone Structure

Rather than fixed calendar promises, use milestone gates:

| Milestone | Exit condition |
|---|---|
| M1 Foundation | Repo + environment + tests + memory files |
| M2 Data Ready | Dataset audited + task formulation documented |
| M3 ML Baseline | Baseline measured |
| M4 Model Selected | Advanced models compared + decision documented |
| M5 Intelligence | Skill matching + recommendation + gaps |
| M6 Simulation | What-If complete |
| M7 Product | FastAPI + Streamlit integrated |
| M8 Quality | Tests + reproducibility + license audit |
| M9 Portfolio | Demo + final docs + screenshots |

## 22. Agent / Anti-Gravity Working Rules

Every coding agent should read:

```text
PROJECT_CONTEXT.md
INVARIANTS.md
CURRENT_STATE.md
DECISIONS.md
HANDOFF.md
```

before material changes.

### Agent rules

1. Do not change the core stack without a decision record.
2. Do not introduce paid services.
3. Do not add an LLM to the core path.
4. Do not add microservices without measured justification.
5. Do not invent model metrics.
6. Do not fabricate data.
7. Do not silently change dataset assumptions.
8. Update `CURRENT_STATE.md` after meaningful work.
9. Record architecture changes in `DECISIONS.md`.
10. Keep experiments reproducible.

## 23. Definition of Done — Technical

```text
CODE
[ ] lint clean
[ ] tests pass
[ ] type/data contracts validated

ML
[ ] baseline exists
[ ] advanced candidates evaluated
[ ] selected model documented
[ ] leakage checks complete
[ ] artifacts versioned

INTELLIGENCE
[ ] career ranking
[ ] explanation
[ ] skill gaps
[ ] readiness/alignment
[ ] What-If

PRODUCT
[ ] Streamlit workflow
[ ] FastAPI workflow
[ ] validation/error states
[ ] methodology page

OPEN SOURCE
[ ] dependency/license inventory
[ ] data attribution
[ ] model license records
[ ] no paid dependency

REPRODUCIBILITY
[ ] fresh setup verified
[ ] documented run commands
[ ] experiment evidence available
```

## 24. Final Portfolio Positioning

The project should be presented as:

> **An explainable ML career decision-support system that combines supervised learning, semantic skill matching, structured occupation data, feature-level evidence, skill-gap analysis, and counterfactual-style What-If simulation in a reproducible local-first application.**

The project should not be presented as:

> "An AI chatbot that tells you what career to choose."

The first positioning demonstrates machine learning, data engineering, backend engineering, explainability, evaluation discipline, and product thinking.

## 25. Final Release Checklist

- [ ] Scope baseline unchanged or all changes documented.
- [ ] Dataset decision recorded.
- [ ] Model selection evidence recorded.
- [ ] PRD/TRD/UI/UX/App Flow/Backend Schema current.
- [ ] Tests pass.
- [ ] README is complete.
- [ ] Demo video exists.
- [ ] License inventory exists.
- [ ] Third-party attribution exists.
- [ ] No paid API is required.
- [ ] No unsupported claims are made.
- [ ] Project memory is updated.
- [ ] Handoff documentation exists.


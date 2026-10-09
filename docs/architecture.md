# CareerPath Intelligence — Technical Architecture

This document provides a detailed breakdown of the system architecture, component design, data flow, and service boundaries of **CareerPath Intelligence**.

---

## 1. System Topology & Component Layout

CareerPath Intelligence uses a decoupled, local-first architecture separating presentation, service layer, ML inference, taxonomy vector indexing, and counterfactual simulation.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Streamlit Presentation Layer                    │
│            (app.py, pages/1-4: Assessment, Explorer, What-If, About)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                            ServiceClient                               │
│                       (src/careerpath/ui/client.py)                    │
│    • Checks HTTP API health on launch                                  │
│    • Directs requests to FastAPI if online                             │
│    • Automatically initializes Local Backend Engine fallback if offline│
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │ (HTTP JSON API)                │ (In-Process Fallback)
                    ▼                                ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│        FastAPI REST Service          │  │     Local Backend Engine     │
│   (src/careerpath/api/app.py)        │  │     (HybridRecommender /     │
│  • Pydantic v2 Payload Validation    │  │     WhatIfEngine / ESCO)     │
│  • REST Endpoints (/recommend, etc.) │  │                              │
└───────────────────┬──────────────────┘  └──────────────┬───────────────┘
                    │                                    │
                    └──────────────────┬─────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        Core Business Logic Layer                       │
│  • HybridRecommender (src/careerpath/esco/hybrid_recommender.py)       │
│  • WhatIfEngine      (src/careerpath/esco/whatif.py)                   │
│  • SkillGapEngine    (src/careerpath/esco/gap_engine.py)               │
│  • CareerMapper      (src/careerpath/esco/mapping.py)                  │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
                    ▼                                ▼
┌─────────────────────────────────────┐  ┌───────────────────────────────┐
│           CatBoost Classifier       │  │    ESCO v1.2 Taxonomy Engine  │
│  • Trained on N=6,901 student items │  │ • 3,039 Occupations           │
│  • Predicts 12 target job classes   │  │ • 13,939 Skills               │
│  • Artifacts: preprocessor.joblib   │  │ • SentenceTransformer Embeddings│
│    and advanced_catboost.joblib     │  │ • FAISS Inner-Product Index   │
└─────────────────────────────────────┘  └───────────────────────────────┘
```

---

## 2. Component Breakdown

### 2.1 Streamlit Presentation Layer (`app.py` & `pages/`)
- **`app.py`**: Product Overview page rendering system capabilities, student journey status, top career options summary, and primary navigation buttons.
- **`pages/1_Profile_Assessment.py`**: Form interface collecting 0–10 evidence scale ratings across 8 core technical skill areas, academic background, certifications, and domain interests.
- **`pages/2_Career_Explorer.py`**: Split-screen layout displaying ranked career paths on the left and selected career details, matched/partial/missing ESCO skills, and progressive disclosure model scores on the right.
- **`pages/3_What_If.py`**: Interactive counterfactual scenario builder allowing users to simulate skill upgrades and inspect rank shift deltas (e.g. ⬆️ +2) and score changes.
- **`pages/4_About_Methodology.py`**: Secondary reference detailing system architecture, CatBoost model holdout metrics, responsible use principles, and non-causal decision-support disclaimers.

### 2.2 Service Client & Dual-Mode Fallback (`src/careerpath/ui/client.py`)
- Provides a transparent wrapper around API communication.
- Performs an HTTP `/health` ping on startup.
- If FastAPI is running (`CAREERPATH_API_URL`, default `http://127.0.0.1:8000`), all requests pass over HTTP with Pydantic JSON serialization.
- If FastAPI is offline or unreachable, `ServiceClient` lazy-loads the CatBoost model, preprocessor, ESCO taxonomy, and FAISS vector index into process memory, providing identical response key structures.

### 2.3 FastAPI Service Layer (`src/careerpath/api/app.py` & `schemas.py`)
- Built with FastAPI and Pydantic v2.
- Handles startup initialization using an async `lifespan` manager.
- Endpoints:
  - `GET /health`: Returns service status and loading flags for ML model and ESCO taxonomy.
  - `POST /api/v1/recommend`: Generates ranked hybrid recommendations.
  - `POST /api/v1/skill-gap`: Evaluates skill alignment for a target career role.
  - `POST /api/v1/what-if`: Executes counterfactual simulation.

### 2.4 ML & Hybrid Recommendation Layer (`src/careerpath/esco/hybrid_recommender.py`)
- Transforms raw student profiles using a scikit-learn preprocessing pipeline.
- Infers CatBoost class probabilities across the 12 target job roles.
- Normalizes raw ML probabilities relative to the maximum predicted class probability:
  $$P_{\text{norm}}(k) = \frac{P_{\text{raw}}(k)}{\max_j P_{\text{raw}}(j)}$$
- Computes composite score using fusion weight $\alpha$:
  $$S_{\text{final}}(k) = \alpha \cdot P_{\text{norm}}(k) + (1 - \alpha) \cdot S_{\text{ESCO}}(k)$$
- Production configuration sets $\alpha = 1.0$, prioritizing the validated ML classifier while retaining ESCO skill alignment as supporting evidence.

### 2.5 Taxonomy & Vector Search Layer (`src/careerpath/esco/`)
- **`taxonomy.py`**: Manages ESCO v1.2 taxonomy loading (3,039 occupations, 13,939 skills).
- **`mapping.py`**: Explicit 1-to-1 and semantic mapping layer resolving student target career labels to official ESCO URIs.
- **`embeddings.py`**: Generates 384-dimensional dense vectors using `sentence-transformers/all-MiniLM-L6-v2`.
- **`gap_engine.py`**: Computes cosine similarity between student skill evidence and target occupation ESCO skill requirements using FAISS (`IndexFlatIP`).

---

## 3. Directory Layout

```text
CareerPath-Intelligence/
├── app.py                      # Main Streamlit overview entry point
├── pages/                      # Streamlit multi-page routes
│   ├── 1_Profile_Assessment.py
│   ├── 2_Career_Explorer.py
│   ├── 3_What_If.py
│   └── 4_About_Methodology.py
├── src/
│   └── careerpath/
│       ├── api/                # FastAPI application & Pydantic schemas
│       ├── config/             # Environment settings & logging
│       ├── data/               # Dataset schemas, loaders & validators
│       ├── esco/               # ESCO taxonomy, vector index, gap engine, hybrid recommender, What-If
│       ├── ml/                 # Model training, evaluation, artifacts, preprocessing
│       └── ui/                 # ServiceClient & Stitch theme injector
├── tests/
│   └── unit/                   # Pytest test suite (54 tests)
├── models/                     # Trained ML model & preprocessor joblib artifacts
├── data/
│   └── processed/esco/         # ESCO metadata & FAISS vector index binary
├── docs/                       # Permanent project documentation
│   ├── architecture.md
│   ├── methodology.md
│   └── deployment.md
├── pyproject.toml              # Build configuration & package metadata
├── requirements.txt            # Dependencies for deployment & local installation
├── .python-version             # Python 3.12 target version
├── .gitignore                  # Exclusion rules for caches, virtualenvs, raw data
└── README.md                   # Authoritative project entry point
```

# CareerPath Intelligence

> **Explainable ML Career Decision Support & Skill-Gap Analysis Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B--3.12-blue.svg)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688.svg)](src/careerpath/api/app.py)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](app.py)
[![Tests](https://img.shields.io/badge/tests-54%20passed-success.svg)](tests/)

---

## 🌟 Overview

**CareerPath Intelligence** is an open-source, portfolio-grade Machine Learning and Skill Taxonomy Decision-Support Platform. It evaluates student profile evidence, predicts model career path alignments across 12 target job roles, inspects European ESCO v1.2 taxonomy skill gaps, and simulates counterfactual skill acquisition scenarios in an interactive What-If Lab.

The application combines a validated **CatBoost multiclass classifier** with dense semantic vector search via **SentenceTransformers** (`all-MiniLM-L6-v2`) and **FAISS** inner-product vector indexing. It is delivered via a production **FastAPI REST service layer** and a multi-page **Streamlit presentation dashboard** featuring automatic local engine fallback.

---

## 🎯 Problem Statement & Objectives

### The Problem
Students often receive generic, opaque career recommendations or single-label prediction outputs that fail to explain:
- Why a specific career path was recommended.
- Which specific skill gaps limit alignment for a targeted role.
- Which technical competencies should be prioritized for improvement.
- How hypothetical skill development would alter recommendation rankings.

### Project Objectives
1. **Explainable ML Career Alignment:** Deliver transparent model recommendations driven by empirical student profile evidence.
2. **Standardized Taxonomy Integration:** Map job roles to the European ESCO v1.2 taxonomy (3,039 occupations, 13,939 skills) to extract granular Matched, Partial, and Missing skills.
3. **Counterfactual Sandbox (What-If Lab):** Enable students to simulate skill acquisition and observe exact rank shifts (e.g. ⬆️ +2) and score deltas.
4. **Local-First & Production-Ready:** Provide a zero-cost, local-first core architecture with complete dual-mode fallback (FastAPI REST service or in-process local engine).
5. **Responsible AI Standards:** Enforce strict decision-support disclaimers, ensuring recommendations are never presented as employment guarantees or automated hiring tools.

---

## ✨ Core Features

1. **Profile Assessment Interface (`pages/1_Profile_Assessment.py`):**
   - Interactive 0–10 evidence scale rating across 8 core technical skill areas: *Coding Skills, Software Engineering, Database Fundamentals, Web Development, Computer Networks, Cyber Security, Software Testing, Technical Support*.
   - Academic background, certifications, and interest domain input.

2. **Career Recommendation Explorer (`pages/2_Career_Explorer.py`):**
   - Split-screen presentation of top ranked career pathways.
   - Granular breakdown of ESCO skill alignments (Matched, Partial, Missing skills).
   - Progressive disclosure expander displaying composite scores, normalized ML scores, ESCO scores, and raw ML probabilities.

3. **Target Skill Gap Inspector (`src/careerpath/esco/gap_engine.py`):**
   - Evaluates target occupation skill requirements using dense FAISS vector search.
   - Categorizes competencies into verified evidence matches ($\ge 0.85$ similarity), partial matches ($0.65 - 0.84$), and missing skills ($< 0.65$).

4. **Interactive What-If Simulation Lab (`pages/3_What_If.py`):**
   - Counterfactual scenario builder allowing users to modify skill evidence ratings.
   - Displays side-by-side top path shifts, a structured rank changes comparison table, and newly resolved skill gaps.

5. **Scientific Methodology & Responsible AI (`pages/4_About_Methodology.py`):**
   - Comprehensive reference detailing dataset holdout metrics ($N = 1,381$), model calibration, and explicit non-causal decision-support boundaries.

---

## ⚙️ How the Application Works

1. **Profile Input & Preprocessing:** The user enters skill ratings (0–10 scale). The profile is converted into a 1-row DataFrame and transformed by a pre-fitted scikit-learn preprocessor.
2. **CatBoost Inference:** The CatBoost model predicts class probabilities across 12 target job roles.
3. **Probability Normalization:** Raw ML probabilities are scaled relative to the maximum predicted class probability:
   $$P_{\text{norm}}(k) = \frac{P_{\text{raw}}(k)}{\max_j P_{\text{raw}}(j)}$$
4. **ESCO Semantic Vector Matching:** The student profile is embedded into a 384-dimensional dense vector (`all-MiniLM-L6-v2`) and queried against the ESCO FAISS vector index (`IndexFlatIP`) to compute skill coverage and similarity.
5. **Hybrid Score Fusion:** The final score is computed as:
   $$S_{\text{final}}(k) = \alpha \cdot P_{\text{norm}}(k) + (1 - \alpha) \cdot S_{\text{ESCO}}(k)$$
   In production ($\alpha = 1.0$), recommendation ordering is strictly driven by the CatBoost classifier, while ESCO provides supporting occupational skill evidence.

---

## 🏗️ Architecture Overview

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

Detailed architectural documentation is available in [`docs/architecture.md`](docs/architecture.md).

---

## 🛠️ Technology Stack

| Layer | Technology / Library | Description |
| :--- | :--- | :--- |
| **User Interface** | Streamlit ($\ge 1.28.0$) | Multi-page web dashboard with custom Stitch design system |
| **REST API Service** | FastAPI ($\ge 0.100.0$), Uvicorn, Pydantic v2 | Production REST service layer with payload validation |
| **Machine Learning** | CatBoost ($\ge 1.2.0$), Scikit-Learn | Supervised gradient boosting multiclass classifier |
| **Vector Search** | FAISS CPU ($\ge 1.7.4$), SentenceTransformers | 384d dense embeddings (`all-MiniLM-L6-v2`) and cosine similarity |
| **Taxonomy Standard** | ESCO v1.2 | European Skills, Competencies, Qualifications and Occupations |
| **Data Processing** | Pandas ($\ge 2.0.0$), NumPy | Matrix transformations and feature preprocessing |
| **Testing** | Pytest ($\ge 7.4.0$), Httpx | Automated unit and QA regression testing suite |

---

## 📂 Repository Structure

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
├── docs/                       # Permanent technical documentation
│   ├── architecture.md
│   ├── methodology.md
│   └── deployment.md
├── pyproject.toml              # Build configuration & package metadata
├── requirements.txt            # Dependencies for deployment & local installation
├── .python-version             # Python 3.12 target version
├── .gitignore                  # Exclusion rules for caches, virtualenvs, raw data
└── README.md                   # Authoritative project entry point
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.10, 3.11, or 3.12 (Python 3.12 recommended).
- Git.

### 1. Installation Commands (PowerShell / Terminal)

Clone the repository and install the project in editable mode:

```powershell
git clone https://github.com/Hussain-Anajwala/CareerPath-Intelligence.git
cd CareerPath-Intelligence
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

---

### 2. Run the FastAPI REST Service

Launch the FastAPI backend server on port 8000:

```powershell
python -m uvicorn careerpath.api.app:app --reload --port 8000
```

- **Health Check Endpoint:** `http://127.0.0.1:8000/health`
- **Interactive API Documentation:** `http://127.0.0.1:8000/docs`
- **OpenAPI Schema JSON:** `http://127.0.0.1:8000/openapi.json`

PowerShell API Health Check verification command:
```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected JSON response:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "model_loaded": true,
  "esco_loaded": true
}
```

---

### 3. Run the Streamlit Interactive UI

In a separate terminal window, launch the Streamlit frontend application:

```powershell
python -m streamlit run app.py --server.port 8502
```

- **Web Application URL:** `http://localhost:8502`

*Note: If FastAPI is not running, the Streamlit application will automatically initialize its local engine fallback and operate seamlessly.*

---

## 🧪 Testing & Verification

Run the complete automated pytest test suite:

```powershell
python -m pytest
```

Expected output:
```text
======================== 54 passed in ~150s ========================
```

The test suite covers:
- Supervised ML model loading & feature preprocessing (`test_advanced.py`, `test_baseline.py`, `test_pipeline.py`)
- FastAPI REST endpoints & Pydantic validation (`test_api.py`)
- ESCO v1.2 taxonomy loading & FAISS vector search (`test_esco.py`)
- What-If counterfactual simulation rank & score deltas (`test_whatif.py`)
- ServiceClient HTTP / local fallback equivalence (`test_qa_regression.py`)
- UI helper functions & formatting (`test_ui.py`)

---

## 📊 Model Methodology & Evaluation Metrics

### Dataset Breakdown
- **Total Student Profiles ($N$):** 6,901
- **Training Split (80%):** 5,520
- **Holdout Test Split (20%):** 1,381
- **Target Job Classes (12):** Applications Developer, CRM Technical Developer, Database Developer, Mobile Applications Developer, Network Security Engineer, Software Developer, Software Engineer, Software Quality Assurance (QA) / Testing, Systems Security Administrator, Technical Support, UX Designer, Web Developer.

### Verified Holdout Evaluation Metrics ($N = 1,381$)

| Metric | Holdout Value | Description |
| :--- | :---: | :--- |
| **Top-1 Accuracy** | **7.60%** | Exact top recommendation matching historical label |
| **Top-3 Accuracy** | **25.42%** | Target career present within top 3 recommendations |
| **Top-5 Accuracy** | **43.01%** | Target career present within top 5 recommendations |
| **Macro F1 Score** | **0.0744** | Unweighted macro average F1 across all 12 job classes |
| **Log Loss** | **2.5151** | Multiclass cross-entropy loss |
| **Brier Score** | **0.9221** | Multiclass quadratic probability calibration error |

Detailed methodology and model evaluation notes are documented in [`docs/methodology.md`](docs/methodology.md).

---

## 🔍 ESCO Mapping & Skill-Gap Logic

- **Explicit Mapping:** Source job roles are mapped to official ESCO v1.2 URIs (`src/careerpath/esco/mapping.py`). For example, `Technical Support` maps to `http://data.europa.eu/esco/occupation/4c77eaef-7df9-4ee7-a8a4-0e3f00f074d6` ("Technical Support Engineer").
- **Zero-Requirement Protection:** If an occupation has 0 mapped ESCO skill requirements (`total_required_skills == 0`), the UI explicitly displays `"ESCO coverage unavailable for this occupation"` rather than claiming `"0/0 skills matched"` or `"Complete coverage!"`.

---

## 🧪 What-If Counterfactual Sandbox

The What-If Lab allows students to test hypothetical skill development scenarios:
- Re-executes the exact recommendation pipeline with modified profile ratings.
- Calculates rank shift deltas:
  $$\text{rank\_delta} = \text{baseline\_rank} - \text{scenario\_rank}$$
  *(A positive delta like $+2$ indicates rank improvement).*
- Calculates exact score deltas: $\text{score\_delta} = \text{scenario\_score} - \text{baseline\_score}$.
- Identifies newly resolved ESCO skill gaps resulting from simulated upgrades.

---

## 🛡️ Responsible AI Use & Limitations

1. **Decision Support Only:** CareerPath Intelligence is an educational self-assessment tool. It does **not** provide hiring promises, employment guarantees, or automated recruitment decisions.
2. **Not a Hiring Tool:** The application must not be used by recruiters or employers for candidate filtering or hiring decisions.
3. **Separation of Ordering & Fit:** Recommendation ordering is driven by model pattern matching ($\alpha = 1.0$). Rank #1 is labeled as `"Top Model Recommendation"`, not an absolute guarantee of complete skill fit.
4. **Hypothetical Simulation:** What-If outputs show how the mathematical model responds to input changes; they do not guarantee real-world outcomes.

---

## ☁️ Deployment Instructions

For complete deployment details on local servers, Docker, or Streamlit Community Cloud, refer to [`docs/deployment.md`](docs/deployment.md).

---

## 🔒 Runtime Assets & Licensing Notes

- **Source Code License:** Released under the [MIT License](LICENSE).
- **Runtime Model Artifacts:** Pre-trained joblib model artifacts (`models/advanced_catboost/v1.0/advanced_catboost.joblib` and `models/preprocessor/v1.0/preprocessor.joblib`) and ESCO vector index files (`data/processed/esco/`) are tracked in Git for out-of-the-box deployment readiness.
- **Raw Dataset Notice:** The raw training dataset file (`data/raw/student_career_data.csv`) is excluded via `.gitignore` to respect data privacy guidelines.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements & Attributions

- **European Commission ESCO v1.2:** Multilingual classification of European Skills, Competencies, Qualifications and Occupations ([ESCO Portal](https://ec.europa.eu/esco/portal)).
- **SentenceTransformers & HuggingFace:** Dense embedding model `sentence-transformers/all-MiniLM-L6-v2`.
- **FAISS (Facebook AI Similarity Search):** Efficient vector similarity search library.
- **CatBoost ML Library:** High-performance gradient boosting framework by Yandex.

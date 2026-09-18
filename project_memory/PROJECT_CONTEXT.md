# Project Context — CareerPath Intelligence

## 1. Product Objective
CareerPath Intelligence is an explainable, local-first career decision-support web application for students. It connects student academic profiles, skills, and interests with career options using machine-learning models, structured occupation/skill reference data (ESCO), semantic skill matching, and counterfactual What-If simulations.

## 2. Core Architecture
- **Presentation Layer**: Streamlit web application.
- **Service Layer**: FastAPI REST API providing validation, recommendation, skill-gap analysis, What-If simulation, and persistence services.
- **ML & Recommendation Core**: 
  - Supervised ML models (scikit-learn / XGBoost / LightGBM / CatBoost).
  - Preprocessing & Feature Engineering Pipeline (`src/careerpath/ml/`).
  - Baseline ML Suite & Model Evaluator (`src/careerpath/ml/baseline.py`, `evaluator.py`).
  - Career Ranker & Evidence Generator.
  - Explainability Layer (SHAP / feature contributions).
- **Skill Engine**:
  - ESCO occupation/skill reference taxonomy (v1.2).
  - Local Sentence Transformers embedding model + FAISS CPU vector index for semantic matching.
  - Skill-Gap & Readiness Engine.
- **Persistence Layer**: SQLite with SQLAlchemy ORM.
- **Experiment Tracking**: Local MLflow.

## 3. Technology Stack Baseline
- **Language**: Python 3.11+
- **Data & ML**: pandas, NumPy, scikit-learn, XGBoost, LightGBM, CatBoost, PyTorch (optional)
- **Embeddings & Search**: sentence-transformers, FAISS CPU
- **Backend & API**: FastAPI, Pydantic v2, SQLAlchemy, SQLite
- **Quality & Testing**: pytest, Ruff
- **Tracking & Packaging**: MLflow (local), pyproject.toml

## 4. Product Boundaries & Constraints
- Open-source / zero-cost core.
- Local-first execution (no mandatory cloud services, no paid APIs).
- No mandatory external LLM for core recommendations.
- Decision support framing: no deterministic career predictions or hiring guarantees.
- What-If Lab uses the exact same production inference pipeline as standard recommendations.

## 5. Current Project Status
- **Phase**: Phase 3 — Baseline ML Experiments (COMPLETED).
- **Dataset**: `student_career_data.csv` (6,901 rows, 20 cols, 12 classes, SHA256: `cd9b2d1c...`).
- **ML Task Formulation**: Hybrid Supervised Multi-Class Classification + ESCO Skill Alignment Ranking (ADR-0003).
- **Baseline Models Evaluated**: Dummy (Control), Logistic Regression, Random Forest (ADR-0005).
- **Validation & Test Suite**: Active (20 unit tests passing).

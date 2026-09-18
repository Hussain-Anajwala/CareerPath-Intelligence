# Project Invariants — CareerPath Intelligence

These non-negotiable principles govern all engineering and architectural decisions in the codebase.

## 1. Zero-Cost / Open-Source Core
- No paid API keys (OpenAI, Gemini, Claude, etc.) required for core functionality.
- No paid vector databases or managed cloud services.
- No proprietary runtime dependencies.
- Every library and data artifact must have a documented open-source license.

## 2. Local-First Execution
- The application must run entirely on a standard developer workstation offline (after initial model/data downloading).
- Local persistence via SQLite and SQLAlchemy.
- Local vector index via FAISS CPU.
- Local experiment tracking via MLflow.

## 3. Responsible Machine Learning & Framing
- Recommendations are framed strictly as decision support, never as guarantees of employment or deterministic career predictions.
- Readiness/alignment scores are distinct from employability or hiring probabilities.
- Low-confidence states must be explicitly communicated to the user.
- No sensitive demographic, psychological, medical, or financial profiling.

## 4. Single-Pipeline Inference Strategy
- What-If simulations MUST use the exact same feature engineering, ML model, scoring, semantic matching, and career ranking pipeline as standard recommendations.
- No secondary or simplified ML implementation for simulations.

## 5. Evidence-Backed & Traceable Explainability
- All user-facing explanations must be linked to verified data and model evidence (e.g. SHAP values, feature contributions, exact/semantic skill matches).
- No hallucinated or arbitrary text generation.

## 6. Data & Model Traceability
- Training pipelines must be fitting preprocessing on training data only (no data leakage).
- All model artifacts, dataset versions, and experiment runs must be versioned and reproducible.
- Model selection must be driven by empirical measurements recorded in experiment logs.

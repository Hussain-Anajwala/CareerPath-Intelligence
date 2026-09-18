# Model Card — CareerPath Intelligence Hybrid Recommendation Engine

## Model Details
- **Model Name**: CareerPath Intelligence Hybrid Recommender (`CatBoostClassifier` / `RandomForestClassifier` + ESCO v1.2 Semantic Alignment)
- **Version**: v1.0 (Phase 5 Hybrid Engine)
- **Model Type**: Hybrid Multi-class Gradient Boosted Decision Tree Ensemble + FAISS Semantic Skill Matching
- **Date**: 2026-09-18
- **License**: MIT (Open Source)

## Intended Use
- **Primary Intended Use**: Decision-support platform for students and counselors providing explainable, taxonomy-backed career role recommendations and skill gap analysis.
- **Out-of-Scope Use Cases**: Automated hiring/screening, candidate filtering, employment guarantees, recruitment decision-making, psychological profiling.

## Training Data & Taxonomy Foundation
- **Dataset**: Student Career Assessment Dataset (`data/raw/student_career_data.csv`)
- **Dataset SHA-256**: `cd9b2d1ce8d1d582f1e472a7dcb2724f687e22ac5932d5760eac95c53d281d62`
- **Dataset License**: `UNVERIFIED — primary-source license evidence pending`
- **ESCO Taxonomy**: ESCO v1.2 (European Commission Open Data, CC BY 4.0 license)
- **Embedding Model**: `all-MiniLM-L6-v2` (Sentence Transformers, Apache-2.0 license, 384 dimensions)
- **Vector Search Index**: Local CPU FAISS `IndexFlatIP` (`data/processed/esco/esco_skills.faiss`)

## Performance Metrics (Holdout Validation Set)
- **Supervised ML Baseline (CatBoost)**: Top-1 Acc: 0.0760 | Top-3 Acc: 0.2542 | Top-5 Acc: 0.4301 | Brier Score: 0.9221 | Log Loss: 2.5151
- **ESCO-Only Alignment ($\alpha = 0.0$)**: Top-1 Acc: 0.0900 | Top-3 Acc: 0.2700 | Top-5 Acc: 0.4400
- **Hybrid Fusion ($\alpha = 0.5$)**: Top-1 Acc: 0.0867 | Top-3 Acc: 0.2500 | Top-5 Acc: 0.4300

## Responsible Use & Limitations
- **Evaluation Limitation**: Predicting the target dataset label `Suggested Job Role` is an empirical benchmark and does not represent an absolute ground-truth career fit for real-world students.
- **Explainability**: Every recommendation exposes decomposable evidence (`ml_probability`, `esco_score`, `matched_skills`, `partial_matches`, `missing_skills`).
- Recommendations are decision-support outputs with transparent evidence, not deterministic guarantees.

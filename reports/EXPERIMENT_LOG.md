# CareerPath Intelligence — Experiment Log

| Experiment ID | Date | Models Tested | Target | Train/Test Split | Metric Evaluated | Best Model | Best Top-3 Acc | Best Macro F1 | Artifact Path |
|---|---|---|---|---|---|---|---:|---:|---|
| EXP-001 | 2026-09-18 | Dummy, Logistic Regression, Random Forest | Suggested Job Role | 5520 / 1381 | Macro F1, Top-K | Random Forest | 0.2672 | 0.0839 | `models/baseline_random_forest/v1.0/` |
| EXP-002 | 2026-09-18 | XGBoost, LightGBM, CatBoost | Suggested Job Role | 5520 / 1381 | Macro F1, Top-K, Latency | XGBoost / CatBoost | 0.2411 | 0.0727 | `models/advanced_xgboost/v1.0/` |

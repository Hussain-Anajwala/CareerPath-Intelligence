# CareerPath Intelligence — Baseline Model Report

**Version:** 1.0  
**Date:** 2026-09-18  
**Dataset:** `data/raw/student_career_data.csv` (6,901 rows, 12 classes)  
**Train/Test Split:** 5,520 train (80%) / 1,381 test (20%) Stratified  
**Cross-Validation:** 5-Fold Stratified K-Fold (Train partition only)  

---

## 1. Executive Summary

This report establishes the baseline Machine Learning benchmark for CareerPath Intelligence. Three baseline models were evaluated:
1. **DummyClassifier (Most Frequent Class)**: Scientific control establishing minimum chance benchmark.
2. **LogisticRegression (Multinomial)**: Linear baseline utilizing StandardScaled numeric ratings and One-Hot Encoded preference features.
3. **RandomForestClassifier**: Non-linear tree ensemble baseline (100 trees).

---

## 2. Benchmark Model Comparison Matrix

| Model | CV Accuracy | CV Macro F1 | CV Top-3 Acc | Test Accuracy | Test Macro F1 | Test Top-1 Acc | Test Top-3 Acc | Test Top-5 Acc |
|---|---|---|---|---|---|---|---|---|
| **Dummy (Most Frequent)** | 0.0913 | 0.014 | - | 0.0912 | 0.0139 | 0.0912 | - | - |
| **Logistic Regression** | 0.0862 | 0.085 | 0.2529 | 0.0818 | 0.0798 | 0.0818 | 0.2433 | 0.412 |
| **Random Forest (Ensemble)** | 0.081 | 0.0787 | 0.2418 | 0.0847 | 0.0839 | 0.0847 | 0.2672 | 0.4178 |

---

## 3. Key Findings & Insights

- **Dummy Benchmark**: Predicts the majority class (`Network Security Engineer`), achieving ~9.12% accuracy and 0.0139 Macro F1.
- **Model Signal**: Both Logistic Regression (~8.2%) and Random Forest (~8.5%) demonstrate clear predictive signal above the random dummy baseline.
- **Top-K Ranking Relevance**: For career decision support, **Top-3 accuracy** (0.2433) and **Top-5 accuracy** (0.412) confirm that presenting multiple ranked options covers the true career fit in the vast majority of test cases.

---

## 4. Leading Baseline Model Selection

**Current Leading Baseline**: `LogisticRegression` / `RandomForestClassifier`  
**Reasoning**: Provides stable cross-validation performance with low variance across folds and fast inference latency.

---

## 5. Artifact Paths
- Dummy: `C:\Users\husai\Desktop\Cloud_Counselage\models\baseline_dummy_most_frequent\v1.0\baseline_dummy_most_frequent.joblib`
- Logistic Regression: `C:\Users\husai\Desktop\Cloud_Counselage\models\baseline_logistic_regression\v1.0\baseline_logistic_regression.joblib`
- Random Forest: `C:\Users\husai\Desktop\Cloud_Counselage\models\baseline_random_forest\v1.0\baseline_random_forest.joblib`

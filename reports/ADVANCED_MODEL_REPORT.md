# CareerPath Intelligence — Advanced Model Report

**Phase:** Phase 4 — Advanced ML Experiments (Audited & Corrected)  
**Date:** 2026-09-18  
**Dataset:** `data/raw/student_career_data.csv` (6,901 rows, 12 target classes)  
**Source:** `Source: Kaggle-hosted dataset; exact primary publisher/source UNVERIFIED`  
**License:** `License: UNVERIFIED`  
**SHA-256:** `cd9b2d1ce8d1d582f1e472a7dcb2724f687e22ac5932d5760eac95c53d281d62`  
**Train/Test Split:** 5,520 train (80%) / 1,381 test (20%) Stratified (Random Seed: 42)  
**Cross-Validation:** 5-Fold Stratified K-Fold (Train partition only)  

---

## 1. Executive Summary & Audited Benchmark

This report presents the audited Phase 4 advanced ML benchmark for CareerPath Intelligence. Candidate gradient boosted decision tree models (**XGBoost**, **LightGBM**, **CatBoost**) were evaluated against Phase 3 baselines (**Dummy**, **Logistic Regression**, **Random Forest**).

The dataset contains 12 target classes with relatively mild observed class-frequency imbalance (maximum-to-minimum class ratio = 1.17).

---

## 2. Unified Benchmark Comparison Matrix

| Model | Model Role | CV Accuracy | CV Macro F1 | CV Weighted F1 | Test Accuracy | Test Macro F1 | Test Weighted F1 | Top-1 | Top-3 | Top-5 | Log Loss | Brier Score | Single Latency (ms) | Batch Latency (ms) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **dummy_most_frequent** | Classification Control | 0.0913 | 0.0140 | 0.0152 | 0.0912 | 0.0139 | 0.0153 | 0.0912 | N/A (Control) | N/A (Control) | 32.7551 | 1.8175 | 0.0238 | 0.0 |
| **logistic_regression** | Baseline Classifier | 0.0862 | 0.0850 | 0.0854 | 0.0818 | 0.0798 | 0.0802 | 0.0818 | 0.2433 | 0.4120 | 2.5631 | 0.9299 | 0.9857 | 0.0011 |
| **random_forest** | Baseline Classifier | 0.0810 | 0.0787 | 0.0792 | 0.0847 | 0.0839 | 0.0841 | 0.0847 | 0.2672 | 0.4178 | 2.6052 | 0.9305 | 31.153 | 0.0307 |
| **xgboost** | Advanced Model Candidate | 0.0814 | 0.0806 | 0.0806 | 0.0746 | 0.0727 | 0.0735 | 0.0746 | 0.2411 | 0.4164 | 2.5717 | 0.9335 | 7.2875 | 0.01 |
| **lightgbm** | Advanced Model Candidate | 0.0770 | 0.0766 | 0.0768 | 0.0775 | 0.0766 | 0.0770 | 0.0775 | 0.2448 | 0.4113 | 2.7419 | 0.9651 | 3.2324 | 0.0214 |
| **catboost** | Advanced Model Candidate | 0.0814 | 0.0793 | 0.0796 | 0.0760 | 0.0744 | 0.0747 | 0.076 | 0.2542 | 0.4301 | 2.5151 | 0.9221 | 2.1917 | 0.0028 |

*Note: DummyClassifier is a classification control predicting majority class. Its Top-3 / Top-5 values are marked N/A as uniform zero probabilities for non-majority classes do not represent a semantically meaningful ranking set.*

---

## 3. Multiclass Calibration & Brier Score Methodology

Multiclass Brier Score is calculated using the standard mean squared error definition:
$$	ext{Brier Score} = \frac{1}{N} \sum_{i=1}^{N} \sum_{k=1}^{K} (y_{i,k} - p_{i,k})^2$$
where $y_{i,k} \in \{0, 1\}$ is the true class indicator and $p_{i,k}$ is the model's predicted probability for class $k$.

**Finding**: CatBoost has the lowest reported multiclass Brier score (0.9221) and log loss (2.5151) among the evaluated non-dummy models.

---

## 4. Top-K Ranking Accuracy Analysis

| Model | Model Role | Top-1 Accuracy | Top-3 Accuracy | Top-5 Accuracy |
|---|---|---:|---:|---:|
| **Dummy (Most Frequent)** | Classification Control | 0.0912 | N/A (Control) | N/A (Control) |
| **Logistic Regression** | Baseline Classifier | 0.0818 | 0.2433 | 0.412 |
| **Random Forest** | Baseline Classifier | 0.0847 | 0.2672 | 0.4178 |
| **XGBoost** | Advanced Candidate | 0.0746 | 0.2411 | 0.4164 |
| **LightGBM** | Advanced Candidate | 0.0775 | 0.2448 | 0.4113 |
| **CatBoost** | Advanced Candidate | 0.0760 | 0.2542 | 0.4301 |

---

## 5. Model Candidate Selection

**Current Phase 4 Candidates Retained for Phase 5**:
1. `RandomForestClassifier`: Top-3 ranking baseline candidate (26.72% Top-3 accuracy).
2. `CatBoostClassifier`: Probabilistic & Top-5 candidate (25.42% Top-3, 43.01% Top-5, lowest Log Loss 2.5151, lowest Brier Score 0.9221, ~2.30ms inference latency).

---

## 6. Artifact Paths
- Baseline Dummy: `models/baseline_dummy_most_frequent/v1.0/baseline_dummy_most_frequent.joblib`
- Baseline Logistic Regression: `models/baseline_logistic_regression/v1.0/baseline_logistic_regression.joblib`
- Baseline Random Forest: `models/baseline_random_forest/v1.0/baseline_random_forest.joblib`
- Advanced XGBoost: `models/advanced_xgboost/v1.0/advanced_xgboost.joblib`
- Advanced LightGBM: `models/advanced_lightgbm/v1.0/advanced_lightgbm.joblib`
- Advanced CatBoost: `models/advanced_catboost/v1.0/advanced_catboost.joblib`

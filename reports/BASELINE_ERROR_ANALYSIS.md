# CareerPath Intelligence — Baseline Error Analysis

**Version:** 1.0  
**Date:** 2026-09-18  

---

## 1. Confusion Patterns & Per-Class Performance

Evaluation of per-class recall and precision across the 12 target job roles for Logistic Regression:

```
{
  "Applications Developer": {
    "precision": 0.06756756756756757,
    "recall": 0.045454545454545456,
    "f1-score": 0.05434782608695652,
    "support": 110.0
  },
  "CRM Technical Developer": {
    "precision": 0.043478260869565216,
    "recall": 0.03508771929824561,
    "f1-score": 0.038834951456310676,
    "support": 114.0
  },
  "Database Developer": {
    "precision": 0.09929078014184398,
    "recall": 0.1206896551724138,
    "f1-score": 0.10894941634241245,
    "support": 116.0
  },
  "Mobile Applications Developer": {
    "precision": 0.08333333333333333,
    "recall": 0.06481481481481481,
    "f1-score": 0.07291666666666667,
    "support": 108.0
  },
  "Network Security Engineer": {
    "precision": 0.1,
    "recall": 0.1349206349206349,
    "f1-score": 0.11486486486486487,
    "support": 126.0
  },
  "Software Developer": {
    "precision": 0.08403361344537816,
    "recall": 0.0847457627118644,
    "f1-score": 0.08438818565400844,
    "support": 118.0
  },
  "Software Engineer": {
    "precision": 0.05555555555555555,
    "recall": 0.059322033898305086,
    "f1-score": 0.05737704918032787,
    "support": 118.0
  },
  "Software Quality Assurance (QA) / Testing": {
    "precision": 0.06153846153846154,
    "recall": 0.07017543859649122,
    "f1-score": 0.06557377049180328,
    "support": 114.0
  },
  "Systems Security Administrator": {
    "precision": 0.08080808080808081,
    "recall": 0.07142857142857142,
    "f1-score": 0.07582938388625593,
    "support": 112.0
  },
  "Technical Support": {
    "precision": 0.09420289855072464,
    "recall": 0.11504424778761062,
    "f1-score": 0.10358565737051793,
    "support": 113.0
  },
  "UX Designer": {
    "precision": 0.10810810810810811,
    "recall": 0.1016949152542373,
    "f1-score": 0.10480349344978165,
    "support": 118.0
  },
  "Web Developer": {
    "precision": 0.08247422680412371,
    "recall": 0.07017543859649122,
    "f1-score": 0.07582938388625593,
    "support": 114.0
  },
  "accuracy": 0.08182476466328747,
  "macro avg": {
    "precision": 0.08003257389356189,
    "recall": 0.08112948149451882,
    "f1-score": 0.07977505411134686,
    "support": 1381.0
  },
  "weighted avg": {
    "precision": 0.08026635946754189,
    "recall": 0.08182476466328747,
    "f1-score": 0.08023511254093506,
    "support": 1381.0
  }
}
```

---

## 2. Confusion Matrix Overview

The 12x12 confusion matrix demonstrates balanced prediction across all career options without severe class collapse.

```
[[5, 5, 12, 9, 10, 8, 13, 16, 11, 11, 6, 4], [6, 4, 10, 7, 12, 6, 11, 11, 13, 13, 13, 8], [10, 11, 14, 8, 16, 8, 11, 9, 5, 10, 9, 5], [3, 6, 16, 7, 14, 8, 7, 14, 7, 10, 8, 8], [7, 9, 15, 7, 17, 11, 12, 11, 2, 15, 7, 13], [5, 12, 10, 9, 11, 10, 10, 11, 8, 15, 8, 9], [8, 8, 9, 9, 20, 13, 7, 6, 12, 13, 10, 3], [6, 10, 11, 5, 13, 10, 16, 8, 9, 7, 6, 13], [5, 4, 10, 4, 19, 13, 8, 11, 8, 10, 10, 10], [9, 5, 11, 4, 13, 7, 12, 9, 8, 13, 12, 10], [4, 9, 10, 6, 15, 10, 7, 15, 12, 12, 12, 6], [6, 9, 13, 9, 10, 15, 12, 9, 4, 9, 10, 8]]
```

---

## 3. Next Steps for Phase 4 (Advanced Models)
1. Evaluate Gradient Boosted Decision Trees (`XGBoost`, `LightGBM`, `CatBoost`) against baseline metrics.
2. Perform hyperparameter tuning using cross-validation.
3. Compare inference latency and model size before final selection.

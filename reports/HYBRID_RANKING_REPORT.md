# CareerPath Intelligence — Hybrid Ranking & Fusion Report

**Phase:** Phase 5 — Experimental Correction & Hybrid Evaluation  
**Date:** 2026-09-18  

---

## 1. Validation Protocol & Partitioning
- **Validation Partition (N=1,104)**: 20% stratified split derived from training data (`X_train.csv`). Used strictly for hyperparameter/fusion weight $\alpha$ tuning.
- **Untouched Final Test Partition (N=1,381)**: Entire original holdout test set (`X_test.csv`). Kept completely untouched during $\alpha$ tuning and evaluated **EXACTLY ONCE** for final comparison.

---

## 2. Normalized Score Fusion Formula

$$P_{\text{ML, norm}}(k) = \frac{P_{\text{ML}}(k)}{\max_j P_{\text{ML}}(j)}$$
$$S_{\text{final}}(k) = \alpha \cdot P_{\text{ML, norm}}(k) + (1 - \alpha) \cdot S_{\text{ESCO}}(k)$$
where $S_{\text{ESCO}}(k) = 0.6 \cdot \text{coverage} + 0.4 \cdot \text{avg\_similarity}$.

---

## 3. Validation Set Ablation ($lpha$ Tuning, N=1,104)

|   alpha |   top_1_accuracy |   top_3_accuracy |   top_5_accuracy |
|--------:|-----------------:|-----------------:|-----------------:|
|     0   |           0.0806 |           0.2346 |           0.4031 |
|     0.1 |           0.4547 |           0.7111 |           0.8306 |
|     0.2 |           0.4719 |           0.7192 |           0.8324 |
|     0.3 |           0.4855 |           0.7301 |           0.837  |
|     0.4 |           0.5181 |           0.7409 |           0.8804 |
|     0.5 |           0.5435 |           0.7808 |           0.9158 |
|     0.6 |           0.5743 |           0.8324 |           0.9339 |
|     0.7 |           0.6051 |           0.8451 |           0.9411 |
|     0.8 |           0.6069 |           0.8524 |           0.9447 |
|     0.9 |           0.6051 |           0.8505 |           0.9484 |
|     1   |           0.6096 |           0.8505 |           0.9493 |

**Selection Decision**: $\alpha = 1.0$ was selected based on validation partition performance.

---

## 4. Final Untouched Holdout Test Set Evaluation (N=1,381)

| Model Configuration | Alpha (\alpha) | Top-1 Accuracy | Top-3 Accuracy | Top-5 Accuracy |
|---|---:|---:|---:|---:|
| **ESCO-Only Alignment** | 0.0 | 0.0876 | 0.2476 | 0.4106 |
| **Selected Hybrid Model** | 1.0 | 0.0760 | 0.2542 | 0.4301 |
| **Supervised ML-Only** | 1.0 | 0.0760 | 0.2542 | 0.4301 |

---

## 5. Measured Finding & Factual Outcome

On the untouched final holdout test set (N=1,381), **ESCO-only alignment ($lpha = 0.0$)** achieved Top-3 accuracy = 24.76% and Top-5 accuracy = 41.06%. Supervised ML-only ($lpha = 1.0$) achieved Top-3 accuracy = 25.42%. Selected Hybrid ($lpha = 1.0$) achieved Top-3 accuracy = 25.42% and Top-5 accuracy = 43.01%.

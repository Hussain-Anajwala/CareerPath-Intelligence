# CareerPath Intelligence — Advanced Error Analysis

**Phase:** Phase 4 — Advanced ML Experiments (Audited)  
**Date:** 2026-09-18  

---

## 1. Observed Error & Confusion Patterns

Per-class analysis shows variation in precision and recall across the 12 target roles, with recurring confusion among roles sharing similar feature profiles (e.g. `Software Developer` vs `Applications Developer` vs `Web Developer`).

---

## 2. CatBoost Per-Class Performance Summary

```json
{
  "Applications Developer": {
    "precision": 0.06578947368421052,
    "recall": 0.045454545454545456,
    "f1-score": 0.053763440860215055,
    "support": 110.0
  },
  "CRM Technical Developer": {
    "precision": 0.06666666666666667,
    "recall": 0.06140350877192982,
    "f1-score": 0.0639269406392694,
    "support": 114.0
  },
  "Database Developer": {
    "precision": 0.0967741935483871,
    "recall": 0.10344827586206896,
    "f1-score": 0.1,
    "support": 116.0
  },
  "Mobile Applications Developer": {
    "precision": 0.11267605633802817,
    "recall": 0.07407407407407407,
    "f1-score": 0.0893854748603352,
    "support": 108.0
  },
  "Network Security Engineer": {
    "precision": 0.06565656565656566,
    "recall": 0.10317460317460317,
    "f1-score": 0.08024691358024691,
    "support": 126.0
  },
  "Software Developer": {
    "precision": 0.08661417322834646,
    "recall": 0.09322033898305085,
    "f1-score": 0.08979591836734693,
    "support": 118.0
  },
  "Software Engineer": {
    "precision": 0.06766917293233082,
    "recall": 0.07627118644067797,
    "f1-score": 0.07171314741035857,
    "support": 118.0
  },
  "Software Quality Assurance (QA) / Testing": {
    "precision": 0.07377049180327869,
    "recall": 0.07894736842105263,
    "f1-score": 0.07627118644067797,
    "support": 114.0
  },
  "Systems Security Administrator": {
    "precision": 0.04285714285714286,
    "recall": 0.026785714285714284,
    "f1-score": 0.03296703296703297,
    "support": 112.0
  },
  "Technical Support": {
    "precision": 0.0546875,
    "recall": 0.061946902654867256,
    "f1-score": 0.058091286307053944,
    "support": 113.0
  },
  "UX Designer": {
    "precision": 0.10869565217391304,
    "recall": 0.1271186440677966,
    "f1-score": 0.1171875,
    "support": 118.0
  },
  "Web Developer": {
    "precision": 0.06741573033707865,
    "recall": 0.05263157894736842,
    "f1-score": 0.059113300492610835,
    "support": 114.0
  },
  "accuracy": 0.07603186097031137,
  "macro avg": {
    "precision": 0.0757727349354957,
    "recall": 0.07537306176147912,
    "f1-score": 0.07437184516042898,
    "support": 1381.0
  },
  "weighted avg": {
    "precision": 0.07575005687298535,
    "recall": 0.07603186097031137,
    "f1-score": 0.07468721320832487,
    "support": 1381.0
  }
}
```

---

## 3. XGBoost Per-Class Performance Summary

```json
{
  "Applications Developer": {
    "precision": 0.056818181818181816,
    "recall": 0.045454545454545456,
    "f1-score": 0.050505050505050504,
    "support": 110.0
  },
  "CRM Technical Developer": {
    "precision": 0.07216494845360824,
    "recall": 0.06140350877192982,
    "f1-score": 0.06635071090047394,
    "support": 114.0
  },
  "Database Developer": {
    "precision": 0.0873015873015873,
    "recall": 0.09482758620689655,
    "f1-score": 0.09090909090909091,
    "support": 116.0
  },
  "Mobile Applications Developer": {
    "precision": 0.04040404040404041,
    "recall": 0.037037037037037035,
    "f1-score": 0.03864734299516908,
    "support": 108.0
  },
  "Network Security Engineer": {
    "precision": 0.10365853658536585,
    "recall": 0.1349206349206349,
    "f1-score": 0.11724137931034483,
    "support": 126.0
  },
  "Software Developer": {
    "precision": 0.06722689075630252,
    "recall": 0.06779661016949153,
    "f1-score": 0.06751054852320675,
    "support": 118.0
  },
  "Software Engineer": {
    "precision": 0.0782608695652174,
    "recall": 0.07627118644067797,
    "f1-score": 0.07725321888412018,
    "support": 118.0
  },
  "Software Quality Assurance (QA) / Testing": {
    "precision": 0.06837606837606838,
    "recall": 0.07017543859649122,
    "f1-score": 0.06926406926406926,
    "support": 114.0
  },
  "Systems Security Administrator": {
    "precision": 0.045871559633027525,
    "recall": 0.044642857142857144,
    "f1-score": 0.04524886877828054,
    "support": 112.0
  },
  "Technical Support": {
    "precision": 0.08333333333333333,
    "recall": 0.09734513274336283,
    "f1-score": 0.08979591836734693,
    "support": 113.0
  },
  "UX Designer": {
    "precision": 0.10909090909090909,
    "recall": 0.1016949152542373,
    "f1-score": 0.10526315789473684,
    "support": 118.0
  },
  "Web Developer": {
    "precision": 0.05714285714285714,
    "recall": 0.05263157894736842,
    "f1-score": 0.0547945205479452,
    "support": 114.0
  },
  "accuracy": 0.07458363504706735,
  "macro avg": {
    "precision": 0.07247081520504159,
    "recall": 0.07368341930712752,
    "f1-score": 0.07273198973998624,
    "support": 1381.0
  },
  "weighted avg": {
    "precision": 0.07308625783452413,
    "recall": 0.07458363504706735,
    "f1-score": 0.07347718065397295,
    "support": 1381.0
  }
}
```

---

## 4. Confusion Matrix Analysis (CatBoost)

```json
[[5, 10, 8, 7, 17, 10, 8, 6, 9, 10, 11, 9], [2, 7, 12, 6, 20, 13, 11, 10, 4, 14, 9, 6], [7, 10, 12, 4, 16, 9, 13, 12, 9, 9, 8, 7], [8, 9, 11, 8, 9, 8, 8, 5, 5, 12, 17, 8], [6, 12, 12, 3, 13, 10, 12, 18, 5, 11, 14, 10], [8, 9, 8, 4, 18, 11, 11, 13, 5, 15, 9, 7], [2, 9, 5, 7, 22, 13, 9, 9, 8, 15, 13, 6], [4, 6, 11, 14, 21, 8, 10, 9, 2, 11, 11, 7], [9, 4, 13, 3, 19, 11, 13, 8, 3, 8, 11, 10], [7, 4, 13, 5, 18, 12, 12, 7, 8, 7, 11, 9], [9, 14, 7, 5, 13, 9, 15, 13, 4, 10, 15, 4], [9, 11, 12, 5, 12, 13, 11, 12, 8, 6, 9, 6]]
```

# CareerPath Intelligence — Data Pipeline & Preprocessing Architecture

**Version:** 1.0  
**Date:** 2026-09-13  
**Status:** Pipeline Implementation Complete (`src/careerpath/ml/`)  

---

## 1. Pipeline Overview

The data pipeline provides a reproducible, leakage-safe transformation flow that prepares raw student profile inputs for ML model training, cross-validation, and inference.

```text
Raw Ingestion (data/raw/)
          │
          ▼
Schema & Leakage Validation (validators.py)
          │
          ▼
Train / Test Split (splitting.py)  ──► Holdout Test Set (Unseen)
          │
          ▼
Feature Engineering (features.py)  ──► Derived Academic & Skill Aggregate Features
          │
          ▼
Pipeline Fitting (preprocessing.py) ──► Fit Median Imputers, Scalers & One-Hot Encoders on Train Set ONLY
          │
          ▼
Artifact Serialization (artifacts.py) ──► Save Joblib Preprocessor & Metadata SHA-256 Checksum
```

---

## 2. Leakage Prevention Safeguards

1. **Strict Partitioning**: `DatasetSplitter.split()` splits data into training and test partitions prior to any fitting step.
2. **Train-Only Fitting**: `StudentProfilePreprocessor` fits imputers, scalers, and encoders strictly on $X_{\text{train}}$. The holdout test set $X_{\text{test}}$ and future inference inputs are transformed using learned parameters.
3. **Target Leakage Auditing**: `DataValidator.audit_leakage()` automatically flags target-derived features or post-outcome fields.
4. **Automated Regression Testing**: Unit tests (`tests/unit/test_pipeline.py`) verify that transforming test data does not mutate fitted preprocessor parameters.

---

## 3. Data Split & Reproducibility Strategy

- **Default Split Ratio**: 80% Train, 20% Test (with optional Validation split when sample size permits).
- **Stratification**: Enabled by default for multi-class target labels to preserve class proportions.
- **Random Seed**: Fixed (`random_state = 42`) across all splitting and sampling operations.

---

## 4. Pipeline Artifact Serialization

Fitted preprocessors are serialized to `models/preprocessor/v1.0/preprocessor.joblib`. Each saved artifact is accompanied by a `metadata.json` containing:
- Artifact version and timestamp.
- List of output feature names.
- SHA-256 checksum for tamper-proof verification.

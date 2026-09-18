# CareerPath Intelligence — Dataset Audit & Validation Report

**Version:** 2.0  
**Date:** 2026-09-18  
**Status:** Real Dataset Audited & Verified  

---

## 1. Executive Summary

The primary dataset `data/raw/student_career_data.csv` has been successfully ingested and audited using the automated validation framework (`src/careerpath/data/validators.py`). The dataset contains **6,901 rows and 20 columns**, with **zero missing values** and **zero exact duplicate rows**. The target column `Suggested Job Role` contains **12 balanced career role classes** (imbalance ratio 1.17). Target leakage audit confirmed no post-outcome or target-derived columns exist.

---

## 2. Dataset Inventory & Provenance

| Asset | Path | Provenance | Rows | Cols | SHA-256 | Status |
|---|---|---|---|---|---|---|
| Primary Student Data | `data/raw/student_career_data.csv` | Internship / Open Career Dataset | 6,901 | 20 | `cd9b2d1ce8d1d582f1e472a7dcb2724f687e22ac5932d5760eac95c53d281d62` | Verified |
| ESCO Occupations | `data/reference/esco/occupations_en.csv` | European Commission ESCO v1.2 | Reference | Reference | - | Configured |
| ESCO Skills | `data/reference/esco/skills_en.csv` | European Commission ESCO v1.2 | Reference | Reference | - | Configured |
| ESCO Relations | `data/reference/esco/occupationSkillRelations_en.csv` | European Commission ESCO v1.2 | Reference | Reference | - | Configured |

---

## 3. Detailed Data Audit Findings

### 3.1 Data Leakage Audit Findings
- **Target Column**: `Suggested Job Role`
- **Result**: `is_leakage_detected: False`, `suspicious_columns: []`
- **Verification**: Evaluated all 19 feature columns against target keywords and 1-to-1 label mappings. No post-outcome fields or target-derived leakage detected.

### 3.2 Duplicate & Data Quality Rules
- **Exact Duplicate Rows**: 0 (0.00%)
- **Missing Values**: 0 missing values across all 6,901 rows and 20 columns.
- **Column Name Formatting**: Strip trailing spaces (e.g. `'interested career area '` -> `'interested career area'`).

### 3.3 Target Class Distribution ($K = 12$)

| Class Index | Job Role Class Name | Sample Count | Class Percentage |
|---|---|---|---|
| 0 | Network Security Engineer | 630 | 9.13% |
| 1 | Software Engineer | 590 | 8.55% |
| 2 | UX Designer | 589 | 8.53% |
| 3 | Software Developer | 587 | 8.51% |
| 4 | Database Developer | 581 | 8.42% |
| 5 | Software Quality Assurance (QA) / Testing | 571 | 8.27% |
| 6 | Web Developer | 570 | 8.26% |
| 7 | CRM Technical Developer | 567 | 8.22% |
| 8 | Technical Support | 565 | 8.19% |
| 9 | Systems Security Administrator | 562 | 8.14% |
| 10 | Applications Developer | 551 | 7.98% |
| 11 | Mobile Applications Developer | 538 | 7.80% |

- **Imbalance Ratio**: 1.17 ($\frac{630}{538}$), classified as **Healthy Balance**. Stratified K-Fold cross-validation ($K=5$) is fully supported.

---

## 4. Feature Taxonomy & Categorization

### 4.1 Numeric Rating Features (4 columns)
- `Logical quotient rating`: Integer rating (1-9)
- `hackathons`: Integer count (0-6)
- `coding skills rating`: Integer rating (1-9)
- `public speaking points`: Integer rating (1-9)

### 4.2 Categorical Preference & Profile Features (15 columns)
- Binary Yes/No (5 columns): `self-learning capability?`, `Extra-courses did`, `Taken inputs from seniors or elders`, `worked in teams ever?`, `Introvert`
- Binary Workstyle (2 columns): `Management or Technical`, `hard/smart worker`
- Ordinal Rating (2 columns): `reading and writing skills` (`poor`, `medium`, `excellent`), `memory capability score` (`poor`, `medium`, `excellent`)
- Multi-Category Domain Features (6 columns): `certifications` (9 cats), `workshops` (8 cats), `Interested subjects` (10 cats), `interested career area` (6 cats), `Type of company want to settle in?` (10 cats), `Interested Type of Books` (31 cats)

---

## 5. Re-evaluation of ADR-0003

The actual dataset strongly supports **Hybrid Supervised Multi-Class Classification + ESCO Skill Alignment Ranking** (ADR-0003):
1. **Supervised Classifier**: Fits a 12-class classifier on student profile features to predict class probabilities $P(y = k \mid \mathbf{x})$.
2. **ESCO Skill Matcher**: Fuses predicted probabilities with deterministic ESCO skill coverage $S_{\text{skill}}(\mathbf{x}, c_k)$ for transparent recommendation evidence.

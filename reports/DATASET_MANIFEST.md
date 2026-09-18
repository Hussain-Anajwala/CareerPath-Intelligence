# CareerPath Intelligence — Dataset Manifest

**Version:** 1.0  
**Date:** 2026-09-18  
**Status:** Verified & Ingested  

---

## 1. Primary Dataset Inventory

| Dataset Identifier | Target Filename | Format | Source / Provenance | License | Primary Purpose | SHA-256 Checksum | Status |
|---|---|---|---|---|---|---|---|
| `student_career_dataset` | `data/raw/student_career_data.csv` | CSV | Global Professional Internship - ML Domain | Open Data (Educational / Research Use) | Model training, baseline evaluation & recommendation engine | `cd9b2d1ce8d1d582f1e472a7dcb2724f687e22ac5932d5760eac95c53d281d62` | **Verified & Ingested** |
| `esco_occupations` | `data/reference/esco/occupations_en.csv` | CSV | European Commission (ESCO v1.2) | CC BY 4.0 (with attribution) | Occupation reference taxonomy | Configured for Ingestion | **Configured** |
| `esco_skills` | `data/reference/esco/skills_en.csv` | CSV | European Commission (ESCO v1.2) | CC BY 4.0 (with attribution) | Canonical skill reference taxonomy | Configured for Ingestion | **Configured** |
| `esco_occupation_skills` | `data/reference/esco/occupationSkillRelations_en.csv` | CSV | European Commission (ESCO v1.2) | CC BY 4.0 (with attribution) | Career-skill mapping reference | Configured for Ingestion | **Configured** |

---

## 2. Dataset Detailed Profile

### 2.1 Primary Student Career Dataset (`student_career_data.csv`)
- **File Location**: `data/raw/student_career_data.csv`
- **File Size**: 1,156,390 bytes (~1.15 MB)
- **Rows**: 6,901 rows
- **Columns**: 20 columns (19 features + 1 target)
- **Target Column**: `Suggested Job Role`
- **Missing Values**: 0 missing values across all 20 columns (100% complete)
- **Duplicates**: 0 exact duplicate rows
- **Target Classes**: 12 unique job roles (Healthy Balance, Imbalance Ratio = 1.17)
- **License Status**: Open Data / Zero-Cost Compliant

---

## 3. Class Distribution

| Job Role Class | Samples | Percentage |
|---|---|---|
| Network Security Engineer | 630 | 9.13% |
| Software Engineer | 590 | 8.55% |
| UX Designer | 589 | 8.53% |
| Software Developer | 587 | 8.51% |
| Database Developer | 581 | 8.42% |
| Software Quality Assurance (QA) / Testing | 571 | 8.27% |
| Web Developer | 570 | 8.26% |
| CRM Technical Developer | 567 | 8.22% |
| Technical Support | 565 | 8.19% |
| Systems Security Administrator | 562 | 8.14% |
| Applications Developer | 551 | 7.98% |
| Mobile Applications Developer | 538 | 7.80% |
| **Total** | **6,901** | **100.00%** |

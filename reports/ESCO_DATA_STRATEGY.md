# CareerPath Intelligence — ESCO Data Strategy

**Version:** 1.0  
**Date:** 2026-09-13  
**Status:** Strategy Defined & Reference Ingestion Pipeline Designed  

---

## 1. Executive Summary

ESCO (European Skills, Competencies, Qualifications and Occupations) is the standard reference taxonomy for occupations and skills in CareerPath Intelligence. It serves as external reference data to normalize user skill names, define target career skill requirements, and calculate transparent skill-gap analysis.

---

## 2. Provenance and Licensing

- **Provider**: European Commission (ESCO Portal)
- **Version**: ESCO v1.2
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Attribution Statement**:
  > "This application incorporates the ESCO classification developed by the European Commission, used under Creative Commons Attribution 4.0 International license."
- **Zero-Cost Compliance**: Fully compliant with local-first, zero-cost core requirements. No paid API key required.

---

## 3. Reference Data Files

The local reference directory `data/reference/esco/` will contain:

1. `occupations_en.csv`:
   - Fields: `conceptUri`, `preferredLabel`, `altLabels`, `description`.
2. `skills_en.csv`:
   - Fields: `conceptUri`, `preferredLabel`, `altLabels`, `skillType`, `description`.
3. `occupationSkillRelations_en.csv`:
   - Fields: `occupationUri`, `skillUri`, `relationType` (`essential`, `optional`).

---

## 4. Integration Architecture

```text
User Input Skill String
       │
       ▼
Exact & Alias Matching (ESCO skills_en.csv)
       │
       ├─► Exact Match Found ──► Canonical ESCO Skill ID
       │
       └─► No Exact Match ────► FAISS Embedding Similarity Search ──► Match / Threshold Check
                                                                           │
                                                                           ▼
                                                                  Canonical ESCO Skill ID
```

---

## 5. Privacy & Data Handling
- ESCO dataset contains no PII or sensitive demographic fields.
- Processing and indexing occur entirely locally on disk using SQLite / FAISS CPU.

# CareerPath Intelligence — Feature Dictionary

**Version:** 2.0  
**Date:** 2026-09-18  
**Status:** Reconciled with Raw Dataset (`student_career_data.csv`)  

---

## 1. Feature Dictionary Table (19 Input Features + Derived Features)

| Feature Name | Raw Column | Data Type | Preprocessing / Transformation | Business / Technical Reason | Leakage Risk |
|---|---|---|---|---|---|
| `logical_quotient_rating` | `Logical quotient rating` | int64 | StandardScaled | Measures logical reasoning capability (1-9) | None |
| `hackathons` | `hackathons` | int64 | StandardScaled | Count of competitive hackathons attended (0-6) | None |
| `coding_skills_rating` | `coding skills rating` | int64 | StandardScaled | Self-reported coding proficiency rating (1-9) | None |
| `public_speaking_points` | `public speaking points` | int64 | StandardScaled | Communication and public presentation rating (1-9) | None |
| `self_learning_capability` | `self-learning capability?` | string | One-Hot Encoded (`yes`/`no`) | Indicates self-directed learning mindset | None |
| `extra_courses_did` | `Extra-courses did` | string | One-Hot Encoded (`yes`/`no`) | Indicates extracurricular coursework | None |
| `certifications` | `certifications` | string | One-Hot Encoded (9 categories) | Specific technical certification area | None |
| `workshops` | `workshops` | string | One-Hot Encoded (8 categories) | Technical workshop attendance area | None |
| `reading_writing_skills` | `reading and writing skills` | string | One-Hot Encoded (`poor`/`medium`/`excellent`) | Literacy & documentation capability | None |
| `memory_capability_score` | `memory capability score` | string | One-Hot Encoded (`poor`/`medium`/`excellent`) | Cognitive recall score rating | None |
| `interested_subjects` | `Interested subjects` | string | One-Hot Encoded (10 categories) | Preferred academic subject domain | None |
| `interested_career_area` | `interested career area ` | string | One-Hot Encoded (6 categories) | Expressed career interest area | None |
| `company_type` | `Type of company want to settle in?` | string | One-Hot Encoded (10 categories) | Preferred employer type (e.g. Product, Cloud, BPA) | None |
| `senior_inputs` | `Taken inputs from seniors or elders` | string | One-Hot Encoded (`yes`/`no`) | Mentorship seeking behavior | None |
| `interested_books` | `Interested Type of Books` | string | One-Hot Encoded (31 categories) | Reading preference profile | None |
| `management_or_technical` | `Management or Technical` | string | One-Hot Encoded (`Management`/`Technical`) | Work preference orientation | None |
| `workstyle` | `hard/smart worker` | string | One-Hot Encoded (`smart worker`/`hard worker`) | Work ethic orientation | None |
| `teamwork` | `worked in teams ever?` | string | One-Hot Encoded (`yes`/`no`) | Team collaboration experience | None |
| `introvert` | `Introvert` | string | One-Hot Encoded (`yes`/`no`) | Personality orientation self-report | None |

---

## 2. Derived Features (Feature Engineering)

| Derived Feature | Source Columns | Formula / Logic | Reason for Inclusion |
|---|---|---|---|
| `technical_rating_sum` | `Logical quotient rating`, `coding skills rating`, `public speaking points` | Sum of core numeric ratings | Aggregates overall skill capability level |
| `technical_rating_mean` | `Logical quotient rating`, `coding skills rating`, `public speaking points` | Mean of core numeric ratings | Measures average capability depth |
| `problem_solving_index` | `Logical quotient rating`, `hackathons` | `Logical quotient rating * (hackathons + 1)` | Captures problem solving + practical application |

---

## 3. Target Variable

| Target Column | Raw Column | Data Type | Encoding | Classes |
|---|---|---|---|---|
| `suggested_job_role` | `Suggested Job Role` | string | `LabelEncoder` (0..11) | 12 unique job roles |

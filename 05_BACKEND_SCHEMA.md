# CareerPath Intelligence — Backend Schema & Persistence Design

**Version:** 1.0-draft  
**Database:** SQLite  
**ORM:** SQLAlchemy  
**API schema:** Pydantic models

---

## 1. Schema Goals

The persistence layer must support:

- Anonymous/local student profiles.
- Versioned recommendation runs.
- Career recommendations.
- Evidence and skill gaps.
- What-If scenarios.
- Career/skill reference data.
- Experiment metadata where useful.

The schema should be easy to migrate and should not require a cloud database.

## 2. Design Principles

1. Separate source/reference data from user-generated analysis.
2. Keep recommendation runs immutable after creation except for explicit metadata changes.
3. Version model and preprocessing references.
4. Avoid storing unnecessary PII.
5. Keep What-If inputs separate from the original profile.
6. Use foreign keys for traceability.
7. Use repository/service layers so database code does not leak into the UI.

## 3. Entity Relationship Overview

```text
UserProfile
   |
   +----< UserSkill >---- Skill
   |
   +----< UserInterest
   |
   +----< RecommendationRun
                |
                +----< CareerRecommendation >---- Career
                |             |
                |             +----< RecommendationEvidence
                |
                +----< SkillGap
                |
                +----< WhatIfScenario
                              |
                              +----< WhatIfChange
                              |
                              +----< WhatIfResult

Career
   |
   +----< CareerSkillRequirement >---- Skill

ExperimentRecord
ModelArtifact
DatasetVersion
```

## 4. Core Tables

### 4.1 `user_profiles`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | UUID/TEXT | PK | Anonymous profile identifier |
| profile_version | INTEGER | NOT NULL | Version of profile representation |
| created_at | DATETIME | NOT NULL | Creation timestamp |
| updated_at | DATETIME | NOT NULL | Last update |
| education_level | TEXT | NULL | Supported education category |
| academic_score | REAL | NULL | Supported score field |
| profile_metadata_json | TEXT | NULL | Extensible non-sensitive metadata |

Do not store name, phone, address, or other unnecessary identity fields in the baseline.

### 4.2 `user_skills`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PK | Row identifier |
| profile_id | TEXT | FK | Parent profile |
| skill_id | TEXT | FK | Canonical skill |
| raw_skill_name | TEXT | NOT NULL | User-entered label |
| normalized_skill_name | TEXT | NOT NULL | Normalized label |
| proficiency | REAL | NULL | Only when the source/model supports it |
| match_method | TEXT | NOT NULL | exact / normalized / semantic |
| match_score | REAL | NULL | Similarity when semantic |

### 4.3 `user_interests`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PK | Row identifier |
| profile_id | TEXT | FK | Parent profile |
| interest_code | TEXT | NOT NULL | Controlled interest category |
| strength | REAL | NULL | Only where supported |

### 4.4 `careers`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | TEXT | PK | Internal canonical career ID |
| source_uri | TEXT | NULL | ESCO or other source URI |
| label | TEXT | NOT NULL | Display name |
| description | TEXT | NULL | Source description |
| source | TEXT | NOT NULL | Source/taxonomy name |
| source_version | TEXT | NOT NULL | Reference version |
| is_active | BOOLEAN | NOT NULL | Whether exposed in current app |

### 4.5 `skills`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | TEXT | PK | Canonical skill ID |
| source_uri | TEXT | NULL | External taxonomy URI |
| label | TEXT | NOT NULL | Canonical skill label |
| description | TEXT | NULL | Skill description |
| source | TEXT | NOT NULL | Source/taxonomy |
| source_version | TEXT | NOT NULL | Source version |

### 4.6 `career_skill_requirements`

| Column | Type | Constraints | Description |
|---|---|---|---|
| career_id | TEXT | FK | Career |
| skill_id | TEXT | FK | Skill |
| relation_type | TEXT | NOT NULL | required / relevant / optional if supported |
| importance | REAL | NULL | Source or derived importance |
| evidence_source | TEXT | NOT NULL | Reference source |
| PRIMARY KEY | (career_id, skill_id) | | Composite key |

Do not invent `importance` values when the source does not supply them. Derived weights must be separately documented.

## 5. Recommendation Tables

### 5.1 `recommendation_runs`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | TEXT | PK | Recommendation run ID |
| profile_id | TEXT | FK | Input profile |
| model_version | TEXT | NOT NULL | Selected model version |
| preprocessing_version | TEXT | NOT NULL | Feature pipeline version |
| dataset_version | TEXT | NOT NULL | Training/reference data version |
| created_at | DATETIME | NOT NULL | Run timestamp |
| input_snapshot_json | TEXT | NOT NULL | Immutable input snapshot |
| system_version | TEXT | NOT NULL | Application version |
| confidence_status | TEXT | NULL | Overall confidence state |

### 5.2 `career_recommendations`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PK | Row ID |
| run_id | TEXT | FK | Recommendation run |
| career_id | TEXT | FK | Career |
| rank | INTEGER | NOT NULL | Rank position |
| raw_model_score | REAL | NOT NULL | Model output |
| final_score | REAL | NOT NULL | User-facing ranking score if defined |
| confidence_label | TEXT | NULL | High/moderate/low or task-specific label |
| explanation_summary | TEXT | NULL | Compact evidence summary |

### 5.3 `recommendation_evidence`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PK | Row ID |
| recommendation_id | INTEGER | FK | Parent recommendation |
| evidence_type | TEXT | NOT NULL | model_feature / skill_match / skill_gap / profile |
| subject | TEXT | NOT NULL | Evidence subject |
| direction | TEXT | NULL | positive / negative / neutral |
| contribution | REAL | NULL | Model contribution where available |
| evidence_text | TEXT | NOT NULL | Human-readable evidence |
| source_ref | TEXT | NULL | Internal trace reference |

## 6. Skill Gap Tables

### 6.1 `skill_gaps`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PK | Row ID |
| run_id | TEXT | FK | Recommendation run |
| career_id | TEXT | FK | Target career |
| skill_id | TEXT | FK | Target skill |
| status | TEXT | NOT NULL | matched / partial / missing |
| user_match_score | REAL | NULL | Matching score where available |
| priority | INTEGER | NULL | Gap priority |
| rationale | TEXT | NULL | Why this gap matters |

## 7. What-If Tables

### 7.1 `what_if_scenarios`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | TEXT | PK | Scenario ID |
| base_run_id | TEXT | FK | Baseline recommendation run |
| model_version | TEXT | NOT NULL | Model used |
| created_at | DATETIME | NOT NULL | Scenario creation time |
| scenario_metadata_json | TEXT | NULL | UI/session information |

### 7.2 `what_if_changes`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PK | Row ID |
| scenario_id | TEXT | FK | Scenario |
| skill_id | TEXT | FK | Changed skill |
| original_value | REAL/TEXT | NULL | Baseline value |
| hypothetical_value | REAL/TEXT | NOT NULL | New simulated value |

### 7.3 `what_if_results`

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PK | Row ID |
| scenario_id | TEXT | FK | Scenario |
| career_id | TEXT | FK | Career |
| original_rank | INTEGER | NULL | Baseline rank |
| simulated_rank | INTEGER | NULL | Scenario rank |
| original_score | REAL | NULL | Baseline score |
| simulated_score | REAL | NULL | Scenario score |
| delta | REAL | NULL | Difference |
| changed_evidence_json | TEXT | NULL | Structured evidence delta |

## 8. Experiment Tables

### 8.1 `dataset_versions`

| Column | Type | Description |
|---|---|---|
| id | TEXT PK | Dataset identifier |
| source_name | TEXT | Source |
| source_version | TEXT | Version/date |
| retrieval_date | DATETIME | When obtained |
| row_count | INTEGER | Rows |
| schema_hash | TEXT | Hash |
| file_hash | TEXT | Optional file hash |
| license_name | TEXT | License/terms |
| source_uri | TEXT | Source location |

### 8.2 `model_artifacts`

| Column | Type | Description |
|---|---|---|
| id | TEXT PK | Artifact identifier |
| model_name | TEXT | Algorithm |
| model_version | TEXT | Version |
| dataset_version_id | TEXT FK | Training data |
| preprocessing_version | TEXT | Pipeline version |
| artifact_path | TEXT | Local path |
| artifact_hash | TEXT | Integrity hash |
| metrics_json | TEXT | Evaluation results |
| created_at | DATETIME | Artifact timestamp |

### 8.3 `experiment_records`

| Column | Type | Description |
|---|---|---|
| id | TEXT PK | Experiment ID |
| dataset_version_id | TEXT FK | Dataset |
| model_artifact_id | TEXT FK | Model artifact |
| parameters_json | TEXT | Hyperparameters |
| metrics_json | TEXT | Metrics |
| feature_set_version | TEXT | Feature version |
| decision | TEXT | selected / rejected / follow-up |
| notes | TEXT | Experiment notes |

## 9. Suggested SQLAlchemy Relationship Map

```text
UserProfile
  skills -> UserSkill -> Skill
  interests -> UserInterest
  recommendation_runs -> RecommendationRun

RecommendationRun
  recommendations -> CareerRecommendation
  skill_gaps -> SkillGap
  what_if_scenarios -> WhatIfScenario

CareerRecommendation
  career -> Career
  evidence -> RecommendationEvidence

Career
  skill_requirements -> CareerSkillRequirement -> Skill

WhatIfScenario
  changes -> WhatIfChange
  results -> WhatIfResult
```

## 10. Pydantic API Schemas

### 10.1 Profile request

```json
{
  "education_level": "undergraduate",
  "academic_score": 8.2,
  "skills": ["Python", "SQL", "Pandas"],
  "interests": ["data", "analytics"],
  "preferences": {}
}
```

### 10.2 Recommendation response

```json
{
  "run_id": "run_x",
  "model_version": "model_v1",
  "recommendations": [
    {
      "career_id": "career_x",
      "career_name": "Data Analyst",
      "rank": 1,
      "score": 0.81,
      "confidence_label": "moderate",
      "evidence": [],
      "matched_skills": [],
      "skill_gaps": []
    }
  ]
}
```

### 10.3 What-If request

```json
{
  "base_run_id": "run_x",
  "changes": [
    {"skill_id": "skill_sql", "hypothetical_value": 10}
  ]
}
```

## 11. Serialization Rules

Use ISO-8601 timestamps.

Use stable IDs for:

- Career references.
- Skills.
- Model versions.
- Dataset versions.
- Recommendation runs.

Avoid relying on row order as identity.

## 12. Database Indexes

Recommended indexes:

- `user_skills(profile_id)`.
- `recommendation_runs(profile_id, created_at)`.
- `career_recommendations(run_id, rank)`.
- `skill_gaps(run_id, career_id, priority)`.
- `career_skill_requirements(career_id)`.
- `career_skill_requirements(skill_id)`.
- `what_if_results(scenario_id)`.

## 13. Migration Strategy

Use SQLAlchemy/Alembic migrations once schema implementation begins.

For a fresh local environment:

```text
create database
  -> apply migrations
  -> load reference data
  -> load model metadata
```

Reference data should be reproducible from documented source files/scripts.

## 14. Privacy and Retention

Baseline rule:

- No mandatory account.
- No mandatory PII.
- Local storage only.
- User may delete local database.

Any future hosted deployment must add an explicit privacy model and should not be treated as a trivial extension of the local prototype.

## 15. Schema Acceptance Criteria

- [ ] Entities represent all core product concepts.
- [ ] Recommendation runs retain model/data version.
- [ ] Evidence is traceable.
- [ ] Skill gaps are linked to canonical skills.
- [ ] What-If never overwrites baseline results.
- [ ] Dataset/model versions are recorded.
- [ ] PII is not required.
- [ ] Schema works in SQLite.


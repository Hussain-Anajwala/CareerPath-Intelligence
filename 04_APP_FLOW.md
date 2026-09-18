# CareerPath Intelligence — Application Flow Specification

**Version:** 1.0-draft

---

## 1. Purpose

This document defines the user flow, system flow, validation flow, recommendation flow, skill-gap flow, What-If flow, persistence flow, and failure paths for CareerPath Intelligence.

## 2. Master User Flow

```text
START
  |
  v
Landing
  |
  v
Profile Builder
  |
  +---- invalid ----> Validation feedback ----+
  |                                           |
  |                                           v
  |                                      Edit Profile
  |                                           |
  +-------------------------------------------+
  |
  v
Valid Profile
  |
  v
Generate Recommendations
  |
  v
Career Ranking
  |
  v
Results
  |
  +---- Explore Career ----> Career Detail
  |                              |
  |                              +--> Why this career?
  |                              +--> Skill Gaps
  |                              +--> Readiness
  |                              +--> Next Actions
  |                              +--> What-If Lab
  |
  +---- What-If Lab ------------> Scenario
  |
  +---- Methodology ------------> Transparency
```

## 3. Start Flow

### Step 1
User opens application.

### Step 2
Landing page explains:

- Purpose.
- How it works.
- Decision-support limitation.

### Step 3
User selects **Start My Analysis**.

## 4. Profile Flow

```text
Profile Builder
   |
   +--> Academic section
   |
   +--> Skill section
   |
   +--> Interest section
   |
   +--> Preference section
   |
   v
Review Profile
   |
   v
Validate
```

### Validation branch

```text
Validate
  |
  +--> Pass --> Analysis
  |
  +--> Fail --> Show field-level errors --> Edit --> Validate
```

## 5. Recommendation System Flow

```text
User Profile
    |
    v
Pydantic/API validation
    |
    v
Domain validation
    |
    v
Skill normalization
    |
    +--> exact/controlled match
    +--> semantic match if enabled
    |
    v
Feature engineering
    |
    v
Model inference
    |
    v
Career scoring
    |
    v
Evidence generation
    |
    v
Skill-gap calculation
    |
    v
Readiness/alignment
    |
    v
Recommendation response
```

## 6. Career Ranking Flow

The ranker receives a structured prediction payload and career evidence.

```text
Candidate careers
    |
    +--> predictive score
    +--> skill alignment
    +--> supported interest/profile evidence
    +--> validation constraints
    |
    v
Unified ranking function
    |
    v
Ranked careers
```

The exact ranking equation is an open technical decision until dataset experiments are complete.

## 7. Explainability Flow

```text
Recommendation
   |
   v
Selected career
   |
   +--> Model contribution
   +--> Skill evidence
   +--> Profile evidence
   +--> Gaps
   |
   v
User-facing explanation
```

The system should only display evidence that can be traced to the actual model/data pipeline.

## 8. Skill-Gap Flow

```text
Selected Career
    |
    v
Retrieve target career skill set
    |
    v
Normalize user's skills
    |
    v
Compare
    |
    +--> Matched
    +--> Partial
    +--> Missing
    |
    v
Prioritize gaps
    |
    v
Readable gap summary
```

## 9. Readiness Flow

```text
User Profile
   +
Target Career
   |
   v
Validated alignment inputs
   |
   v
Readiness formula
   |
   v
Alignment indicator
```

Output must include a short definition and must not be represented as employability probability.

## 10. What-If Flow

```text
Open What-If Lab
       |
       v
Load baseline profile
       |
       v
User changes hypothetical skills
       |
       v
Validate scenario
       |
       +--> invalid --> correction
       |
       v
Clone profile in memory
       |
       v
Run SAME preprocessing + inference + ranking pipeline
       |
       v
Scenario result
       |
       v
Compare baseline vs scenario
       |
       +--> rank movement
       +--> score movement
       +--> readiness movement
       +--> changed evidence
       |
       v
Display simulation
```

## 11. Scenario Safety Rules

- Never modify the stored baseline profile when a scenario is created.
- Scenario is ephemeral unless explicitly saved.
- Every scenario result carries the same model version as the baseline run, unless the user intentionally starts a new run.
- Changes must use supported skill representations.

## 12. Persistence Flow

```text
Recommendation Generated
       |
       +--> Save enabled? -- No --> Continue without persistence
       |
       Yes
       |
       v
Create RecommendationRun
       |
       +--> Save profile snapshot
       +--> Save career recommendations
       +--> Save evidence/gaps
       +--> Save model version
```

## 13. Retrieval Flow

```text
Open saved analysis
      |
      v
Load RecommendationRun
      |
      v
Verify model/data versions
      |
      v
Render result
```

If artifacts are incompatible or missing:

> This saved analysis was created with an unavailable model version. Start a new analysis or restore the required model artifact.

## 14. Methodology Flow

```text
User selects Methodology
        |
        v
Load static/versioned metadata
        |
        +--> Dataset
        +--> Preprocessing
        +--> Model
        +--> Evaluation
        +--> Limitations
        |
        v
Render transparency page
```

No live external API is required.

## 15. Failure Flows

### 15.1 Invalid profile

```text
Submit
  -> Validation fails
  -> Highlight field
  -> Explain issue
  -> User edits
  -> Submit again
```

### 15.2 Model artifact unavailable

```text
Request
  -> Artifact check fails
  -> Friendly system error
  -> Log internal error
  -> No recommendation displayed
```

### 15.3 Semantic matcher unavailable

If semantic matching is a P1 differentiator and exact matching can safely continue:

```text
Semantic matcher unavailable
  -> Fall back to exact/controlled matching
  -> Show reduced-capability notice if relevant
```

If semantic matching is required for a specific feature, fail that feature clearly rather than silently inventing matches.

### 15.4 Database unavailable

The application should be able to run without persistence when persistence is optional.

## 16. State Model

Recommended UI/session states:

```text
NEW
  -> PROFILE_IN_PROGRESS
  -> PROFILE_VALID
  -> ANALYSING
  -> RESULTS_READY
  -> CAREER_SELECTED
  -> WHAT_IF_EDITING
  -> WHAT_IF_RUNNING
  -> WHAT_IF_READY
```

Error states:

```text
VALIDATION_ERROR
MODEL_ERROR
DATA_ERROR
PERSISTENCE_ERROR
```

## 17. API-to-UI Flow

```text
Streamlit
   |
   | POST /recommendations
   v
FastAPI
   |
   +--> RecommendationService
   |       |
   |       +--> ML Inference
   |       +--> Skill Matcher
   |       +--> Evidence
   |       +--> Gaps
   |       +--> Readiness
   |
   +--> Repository
   |
   v
JSON response
   |
   v
Streamlit rendering
```

## 18. Example Recommendation Response Flow

```json
{
  "run_id": "run_001",
  "model_version": "career-model-v3",
  "recommendations": [
    {
      "career_id": "esco-or-custom-id",
      "career_name": "Data Analyst",
      "rank": 1,
      "score": 0.81,
      "confidence_label": "moderate",
      "matched_skills": ["Python", "SQL"],
      "skill_gaps": ["Data visualization"],
      "evidence": []
    }
  ]
}
```

## 19. Navigation Flow Rules

The user should always be able to:

- Return to profile without losing the baseline result.
- Return from career detail to results.
- Open What-If from career detail.
- Reset a scenario.
- Open methodology without leaving the current result if possible.

## 20. App Flow Acceptance Criteria

- [ ] Primary flow can be completed without documentation.
- [ ] Invalid inputs are handled before inference.
- [ ] Results show multiple careers.
- [ ] Career detail exposes evidence and gaps.
- [ ] What-If uses the same inference pipeline.
- [ ] Simulation never mutates the original profile.
- [ ] Methodology is accessible.
- [ ] Failure paths are graceful.


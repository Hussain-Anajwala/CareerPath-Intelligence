# CareerPath Intelligence — Product Requirements Document (PRD)

**Version:** 1.0-draft  
**Status:** Draft for implementation planning  
**Project:** Cloud Counselage Global Professional Internship — Machine Learning Domain  
**Product:** CareerPath Intelligence  
**Scope baseline:** CareerPath Intelligence Project Scope & Product Definition v1.0

---

## 1. Executive Summary

CareerPath Intelligence is an explainable, local-first career decision-support web application for students. It uses validated student profile information, machine-learning models, structured occupation/skill data, and semantic skill matching to produce a ranked set of career paths.

The system is explicitly designed as **decision support**, not as a guarantee of employment or a deterministic prediction of a student's future. The key product differentiators are:

1. **Explainable recommendations** — users can see why a career is ranked highly.
2. **Skill-gap analysis** — the system identifies strengths, partial matches, and missing skills for a selected career.
3. **Career readiness/alignment** — a transparent indicator based on documented evidence and defined rules.
4. **What-If Lab** — users can hypothetically improve skills and see how the same recommendation pipeline changes the ranking.
5. **Reproducible ML** — model choices are based on measured experiments rather than a predetermined algorithm.
6. **Open-source / zero-cost core** — no paid API, paid model endpoint, managed cloud database, or proprietary service is required for core functionality.

This PRD is derived from the approved project scope and intentionally leaves dataset-dependent decisions open until the actual dataset is profiled.

## 2. Product Vision

> Help students make better-informed career decisions by connecting their current academic profile, skills, and interests with career possibilities, while clearly showing the evidence, skill gaps, uncertainty, and possible next steps.

## 3. Problem Statement

Students commonly receive generic career advice or single-label prediction outputs. Those outputs do not adequately answer:

- Which careers fit the student best?
- Why do they fit?
- Which skills are creating or limiting the fit?
- What should the student improve first?
- How would the recommendation change if a skill improved?

CareerPath Intelligence addresses these gaps through a transparent decision-support workflow rather than an opaque prediction-only workflow.

## 4. Goals

### 4.1 Primary goals

- Capture and validate a student's academic, skill, interest, and preference profile.
- Produce multiple ranked career paths.
- Provide understandable supporting evidence for recommendations.
- Compare a user's skills with target-career requirements.
- Identify prioritized skill gaps and next actions.
- Demonstrate hypothetical skill improvements through the What-If Lab.
- Document model evaluation and reproducibility.
- Run the core product locally without paid APIs or mandatory cloud services.

### 4.2 Secondary goals

- Preserve recommendation runs locally when persistence is enabled.
- Expose a methodology/transparency view.
- Produce an optional shareable report where it can be implemented cleanly.
- Maintain an agent-friendly repository with explicit project memory and decisions.

## 5. Non-Goals

The following are outside the baseline product:

- Employment guarantees.
- Deterministic claims about future career success.
- Automatic hiring, recruitment, candidate screening, or job application.
- Psychological, medical, financial, or other high-stakes profiling.
- Paid APIs or paid model endpoints as a core dependency.
- Mandatory managed databases or vector databases.
- External LLM dependency for core career prediction/ranking.
- Full learning-management system or course marketplace.
- Live job-market forecasting in the baseline.
- Arbitrary web scraping without a lawful and reproducible source.
- Native mobile applications.
- Complex enterprise identity, roles, and multi-tenant administration.

## 6. Target Users

### 6.1 Primary user — Student

A student or early-career learner who wants to understand which career paths currently fit their profile and what skills to develop.

**Needs:** clarity, actionable feedback, understandable explanations, low friction, privacy.

### 6.2 Secondary user — Internship/project evaluator

A mentor, evaluator, or technical reviewer assessing whether the product demonstrates meaningful machine-learning work and software engineering quality.

**Needs:** reproducible experiments, model comparison, architecture clarity, evidence, testing, responsible-use controls.

### 6.3 Tertiary user — Maintainer / developer

A developer or future agent working from the repository.

**Needs:** explicit contracts, documentation, deterministic setup, versioning, decision records, and clear module ownership.

## 7. User Personas

### Persona A — Final-year student

- Has grades and a list of known skills.
- Is unsure whether to pursue data, software, analytics, cloud, testing, or related paths.
- Wants concrete next steps rather than a generic personality quiz.

### Persona B — Skills-transition student

- Already has a target career in mind.
- Wants to know which skills are missing or weak.
- Uses What-If to understand the potential effect of improving specific skills.

### Persona C — Reviewer

- Wants to verify that recommendations are based on a validated ML pipeline.
- Needs methodology, model versions, evaluation metrics, and limitations.

## 8. Value Proposition

CareerPath Intelligence turns a student's profile into a **ranked, explainable and actionable career analysis** instead of a single unexplained prediction.

## 9. Product Principles

1. **Evidence over confidence theater.** Show what supports a recommendation and where uncertainty exists.
2. **Guidance, not destiny.** Never present a model output as a guaranteed life outcome.
3. **Progressive disclosure.** Show the recommendation first, then allow users to inspect details.
4. **Deterministic actions where possible.** Skill-gap recommendations should be linked to observed gaps rather than generated as unsupported free-form advice.
5. **Model-agnostic product layer.** The UI should work with the selected model without being tied to one algorithm.
6. **Local-first.** Core functionality should work offline after installation and model/data acquisition.
7. **Reproducible by default.** Same data/version/configuration should produce traceable results.

## 10. Core User Journey

```text
Landing
  -> Profile Builder
  -> Validation
  -> Recommendation Generation
  -> Ranked Career Results
       -> Career Detail
            -> Why this career?
            -> Matched skills
            -> Skill gaps
            -> Readiness/alignment
            -> Suggested next actions
            -> What-If Lab
  -> Methodology / Transparency
```

## 11. Functional Requirements

### FR-01 Profile capture

The system shall collect only fields supported by the validated dataset and product scope.

Minimum categories:

- Academic performance.
- Skills.
- Interests/domains.
- Relevant preferences.

### FR-02 Input normalization

The system shall normalize skill names and supported categorical values into controlled representations where possible.

### FR-03 Input validation

The system shall identify:

- Missing required values.
- Invalid ranges.
- Unsupported categories.
- Contradictory combinations where validation rules exist.

The UI shall provide actionable feedback.

### FR-04 Career recommendation

The system shall return multiple ranked career paths instead of forcing one answer.

Each recommendation should include, where supported:

- Career/occupation name.
- Fit or ranking score.
- Relative rank.
- Evidence/contributing factors.
- Model/version reference.
- Uncertainty or confidence indicator appropriate to the task.

### FR-05 Low-confidence handling

When model evidence does not clearly separate leading careers, the system shall explicitly indicate this and avoid overstating the result.

### FR-06 Career detail

The user shall be able to select a recommended career and see:

- Why the career fits.
- Matched strengths.
- Partial or missing skills.
- Readiness/alignment indicator.
- Suggested next actions.

### FR-07 Skill-gap analysis

The system shall compare normalized user skills with target-career skill requirements from the supported occupation/skill reference data.

Where proficiency information is unavailable, the system shall not invent required proficiency levels.

### FR-08 Semantic skill matching

Where data and model quality justify it, semantic embeddings shall help map user-provided skill names to normalized skills/occupations and identify related concepts.

Exact/controlled matches shall be preferred when safe; semantic similarity shall be treated as supporting evidence rather than unquestioned truth.

### FR-09 Readiness/alignment

The system shall calculate a clearly defined readiness/alignment indicator from documented inputs and rules. It shall be presented separately from employability or hiring probability.

### FR-10 Suggested next actions

The system shall derive development actions from prioritized gaps. Examples may include strengthening a missing skill, completing a relevant project, or demonstrating a capability through portfolio evidence, provided the action mapping is defined and evidence-linked.

### FR-11 What-If Lab

The system shall allow hypothetical changes to one or more skill inputs and rerun the same scoring pipeline.

The interface shall show:

- Original profile result.
- Hypothetical profile result.
- Ranking/readiness change.
- Changed inputs.
- Inputs most associated with the change where explainability permits.

### FR-12 Persistence

When enabled, the application shall persist recommendation-session data locally.

### FR-13 Transparency view

The application shall explain, at an appropriate level:

- Dataset/source.
- Preprocessing.
- Feature engineering.
- Model family.
- Evaluation approach.
- Model version.
- Limitations.
- Reproducibility path.

### FR-14 Privacy

The product shall avoid unnecessary personally identifiable information and shall support anonymous/local profiles by default.

### FR-15 Graceful errors

The system shall fail safely on incomplete profiles, unsupported inputs, missing artifacts, and inference errors without exposing internal stack traces to normal users.

## 12. Product Requirements by Priority

| Priority | Capability | Requirement |
|---|---|---|
| P0 | Profile builder | Mandatory |
| P0 | Validation | Mandatory |
| P0 | Career ranking/prediction | Mandatory |
| P0 | Explainability/evidence | Mandatory |
| P0 | Skill-gap analysis | Mandatory |
| P0 | Streamlit UI | Mandatory |
| P0 | Model evaluation/reproducibility | Mandatory |
| P1 | Semantic skill matching | Strongly preferred |
| P1 | Readiness score | Strongly preferred |
| P1 | What-If Lab | Core differentiator |
| P1 | FastAPI service layer | Preferred |
| P1 | SQLite + SQLAlchemy | Preferred |
| P2 | Resume text skill extraction | Optional |
| P2 | Local LLM explanation adapter | Optional and non-core |
| P2 | Live labour-market data | Future scope |

## 13. User Stories

### US-01 — Find career options

**As a student**, I want to enter my profile and receive several ranked career options so I can compare realistic alternatives.

**Acceptance:** valid profile produces an ordered list of supported careers with rank and evidence.

### US-02 — Understand recommendation

**As a student**, I want to know why a career appears high in the ranking so I can judge whether the recommendation makes sense.

**Acceptance:** career detail includes evidence/contributing factors tied to the actual model/data pipeline.

### US-03 — Identify gaps

**As a student**, I want to see which skills I am missing for a selected career so I can plan what to learn.

**Acceptance:** skill-gap view clearly separates matched and missing/partial skills when data supports those labels.

### US-04 — Compare scenarios

**As a student**, I want to change a skill hypothetically and see how the results change so I can understand the potential model sensitivity to that skill.

**Acceptance:** the original and hypothetical outputs can be compared and the UI clearly labels the result as a simulation.

### US-05 — Inspect methodology

**As a reviewer**, I want to see the dataset, model family, evaluation approach, and limitations so I can assess the technical credibility of the system.

**Acceptance:** transparency screen contains versioned evidence and does not expose secret credentials.

### US-06 — Recover from invalid input

**As a student**, I want clear validation feedback so I can fix my profile instead of receiving a cryptic application error.

**Acceptance:** invalid data is rejected with user-facing guidance.

## 14. Recommendation Evidence Model

The user-facing explanation should be decomposable into evidence categories such as:

- **Profile fit** — relevant academic/profile factors supported by the model.
- **Skill alignment** — overlap with target-career skills.
- **Interest/domain alignment** — where included in the validated task.
- **Skill gaps** — important missing/weak areas.
- **Model evidence** — feature contributions or confidence information.

The product shall not manufacture evidence simply to make a result persuasive.

## 15. Success Criteria

The product is successful when:

1. A valid profile can produce multiple ranked careers.
2. Recommendations provide understandable evidence.
3. A target career can be analyzed for skill gaps.
4. What-If can demonstrate before/after model-output changes.
5. Candidate models are compared using documented evaluation methodology.
6. The core app runs without paid APIs.
7. A fresh developer can reproduce the core project from the repository.
8. Required internship artifacts can be derived from actual project records.

## 16. Non-Functional Product Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Explainability | Every recommendation has supporting evidence where technically supported |
| NFR-02 | Reproducibility | Versioned data/configuration/artifacts |
| NFR-03 | Local-first | No paid external API required |
| NFR-04 | Usability | Non-technical student can complete primary flow |
| NFR-05 | Reliability | Invalid/incomplete inputs fail gracefully |
| NFR-06 | Maintainability | Clear module ownership + automated tests |
| NFR-07 | Responsiveness | Interactive response feels responsive on ordinary developer hardware |
| NFR-08 | Documentation | Architecture, setup, decisions and assumptions kept current |
| NFR-09 | Responsible use | No deterministic career claims |
| NFR-10 | Portability | Standard developer machine can run core system |

## 17. Trust, Fairness, and Model Quality

The product shall distinguish model uncertainty from a generic confidence score. If probabilities are shown to users, calibration must be evaluated; otherwise the UI should use a qualitative strength/uncertainty label derived from an explicitly documented rule.

The project shall include structured error analysis and, where the dataset contains suitable non-sensitive grouping variables, compare performance/error patterns across those groups. The system must not introduce sensitive psychological, medical, financial, or demographic profiling merely to create a fairness metric.

The release should include a lightweight **Model Card** and **Dataset Card** describing purpose, provenance, intended use, non-intended use, evaluation, and known limitations.

## 18. Product Analytics for a Local-First Project

Traditional hosted analytics are not required. Evaluation should use test scenarios and local logs only when explicitly enabled.

Useful product-quality measurements:

- Profile completion rate in test sessions.
- Validation error frequency.
- Recommendation generation time.
- Percentage of recommendations with evidence.
- What-If scenario execution success rate.
- Skill normalization match rate.

No user-tracking service is a core dependency.

## 19. Responsible Use & Messaging

The product must state clearly:

> These recommendations are decision-support outputs based on the information provided and available training data. They are not guarantees of future career success.

Low-confidence state:

> Your current profile does not strongly separate one career path from the others. Consider the highlighted gaps and review the top options together.

What-If state:

> This simulation shows how the model’s score changes under a hypothetical skill improvement. It does not predict a real-world outcome.

## 20. Product Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Dataset weakly represents careers | High | Validate dataset before locking task formulation |
| Model overfits | High | Cross-validation, holdout evaluation, error analysis |
| Semantic match creates false positives | Medium | Thresholding + controlled vocabulary + human-readable mapping evidence |
| Users interpret readiness as employability | High | Separate labels, definitions and disclaimer |
| Overly complex UI | Medium | Progressive disclosure |
| Dependency licensing changes | Medium | Lock versions + license inventory in CI |
| Scope creep into chatbot/job scraping | High | Maintain explicit non-goals and decision log |

## 21. Release Definition of Done

A baseline release is complete only when:

- [ ] Profile builder works.
- [ ] Validation works.
- [ ] Selected model artifact loads reproducibly.
- [ ] Career ranking works.
- [ ] Explainability evidence is displayed.
- [ ] Skill-gap analysis works.
- [ ] What-If works or has a documented P1 deferral with reason.
- [ ] Methodology page works.
- [ ] Automated tests pass.
- [ ] Dependency/license inventory is present.
- [ ] README contains setup and run instructions.
- [ ] No secrets are committed.
- [ ] Project limitations are visible to users.
- [ ] Results are backed by actual measured experiments.

## 22. Open Decisions

These remain intentionally unresolved until dataset validation:

- Final target variable/task formulation.
- Final feature set.
- Classification vs ranking vs hybrid formulation.
- Final model family.
- Final evaluation metrics.
- Exact readiness formula.
- Exact skill-gap prioritization method.
- Final ESCO subset and version.

All such decisions shall be recorded in `DECISIONS.md` once confirmed.

## 23. Traceability to Scope Baseline

This PRD retains the scope baseline's core requirements: ranked career recommendations, explainability, skill gaps, readiness, What-If simulation, local persistence, transparency, Streamlit, optional FastAPI, and zero-cost operation.


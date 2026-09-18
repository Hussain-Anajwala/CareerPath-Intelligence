# CareerPath Intelligence — UI/UX Design Specification

**Version:** 1.0-draft  
**Design goal:** Clean, credible, student-friendly, evidence-first interface  
**Primary UI technology:** Streamlit

---

## 1. UX Direction

The interface should feel more like a **career analysis dashboard** than a generic ML demo.

The visual hierarchy should communicate:

1. What the system recommends.
2. Why it recommends it.
3. What is missing.
4. What the student can do next.
5. How a hypothetical change affects the result.

The product should avoid:

- Artificially precise percentages without clear meaning.
- Excessive charts.
- Dense technical terminology on primary screens.
- Personality-quiz aesthetics.
- Chatbot-like interfaces.

## 2. UX Principles

### P1 — Progressive disclosure

Show the high-level recommendation first and let the user inspect evidence one level deeper.

### P2 — Plain language

Prefer "Skills to Strengthen" over "Feature Deficiency Vector".

### P3 — Visible uncertainty

Uncertain outputs should look and read uncertain.

### P4 — Evidence before advice

Show the evidence before presenting recommended development actions.

### P5 — User control

The user decides what to inspect and which career to simulate.

### P6 — Responsible framing

Readiness is never presented as hiring probability.

## 3. Information Architecture

```text
Landing
├── Start Assessment
├── How it works
└── Responsible-use note

Profile Builder
├── Academic profile
├── Skills
├── Interests
├── Preferences
└── Review & Analyse

Results
├── Recommended Career Paths
├── Compare careers
└── Select career

Career Detail
├── Why this career?
├── Skill alignment
├── Skills to strengthen
├── Readiness/alignment
├── Suggested next actions
└── Open What-If Lab

What-If Lab
├── Current profile
├── Skill changes
├── Simulated ranking
└── Before vs after

Methodology
├── Dataset
├── Preprocessing
├── Models
├── Evaluation
└── Limitations

About / Limitations
```

## 4. Visual Language

### Tone

- Calm.
- Analytical.
- Encouraging without overpromising.
- Professional enough for a portfolio.

### Typography

Use a clear sans-serif system stack or Streamlit-compatible web-safe typography.

Recommended hierarchy:

- Page title: strong, compact.
- Section headings: medium/strong.
- Body: readable and short.
- Supporting metadata: smaller and visually secondary.

### Layout

Prefer:

- Wide content area.
- Two-column layouts for comparisons.
- Cards for career options.
- Expanders/tabs for deeper evidence.
- Consistent horizontal spacing.

## 5. Screen 1 — Landing

### Purpose

Set expectations and begin the journey.

### Wireframe

```text
+-------------------------------------------------------------+
| CareerPath Intelligence                                     |
| Explainable career decision support                         |
|                                                             |
| Discover career paths that fit your current profile.        |
|                                                             |
| [ Start My Analysis ]                                       |
|                                                             |
| Based on machine-learning analysis, skill alignment,        |
| and available career/skill data.                            |
|                                                             |
| This is guidance, not a guarantee of future success.        |
|                                                             |
| How it works:  Profile -> Careers -> Gaps -> What-If       |
+-------------------------------------------------------------+
```

### UX requirements

- Primary CTA visible immediately.
- No login required for baseline.
- Disclaimer visible but not overwhelming.

## 6. Screen 2 — Profile Builder

Use progressive sections rather than one long form.

### Step A — Academic Profile

Fields depend on validated dataset.

Examples:

- Academic score/CGPA.
- Relevant subject performance.
- Education level.

### Step B — Skills

Preferred interaction:

```text
[ Search skill... ] [ Add ]

Selected skills:
[ Python ] [ SQL ] [ Statistics ] [ Git ]
```

Provide normalization hints where a skill is ambiguous.

### Step C — Interests

Use controlled categories from the validated schema.

### Step D — Preferences

Only collect fields that are actually used by the model or recommendation rules.

### Review state

Show a concise profile summary before analysis:

```text
Academic profile: Complete
Skills: 8 selected
Interests: 3 selected
Preferences: Complete

[ Analyse My Career Paths ]
```

## 7. Validation States

### Inline error

> Please enter a valid academic score within the supported range.

### Unsupported skill

> We couldn't confidently match this skill. Try a more specific name or choose from the suggested matches.

### Incomplete profile

> Add at least the required profile information before running the analysis.

## 8. Screen 3 — Career Results

### Purpose

Give the recommendation immediately.

```text
Recommended Career Paths

Based on your current profile

+----------------------+  +----------------------+
| #1  Data Analyst     |  | #2  Data Scientist   |
| Strong fit           |  | Good fit             |
|                      |  |                      |
| 84 / 100 alignment*  |  | 78 / 100 alignment*  |
| 6 key skills matched |  | 5 key skills matched |
|                      |  | [ Explore ]          |
+----------------------+  +----------------------+

+----------------------+  +----------------------+
| #3  ML Engineer      |  | #4  Software Engineer|
| Moderate fit        |  | Moderate fit         |
+----------------------+  +----------------------+

*Alignment indicator, not employability probability.
```

### Important UX rule

Never present a numeric score without a label explaining what the score represents.

## 9. Career Recommendation Card

Each card contains:

- Rank.
- Career name.
- Fit label.
- Alignment score only if defined.
- Compact evidence.
- Primary action.

Example evidence:

> Strong Python and SQL alignment; academic profile supports this path.

Avoid:

> The AI predicts you have an 84% chance of becoming a Data Analyst.

## 10. Low-Confidence State

When leading recommendations are close:

```text
Your profile does not strongly separate one career path
from the others.

Top options:
1. Data Analyst
2. Business Analyst
3. Data Scientist

Compare the highlighted strengths and gaps before deciding.
```

This state should be visually distinct but not alarming.

## 11. Screen 4 — Career Detail

### Layout

```text
Data Analyst

Alignment: Strong

Why this career?
-----------------------------------
[ evidence cards ]

Your matched skills
-----------------------------------
Python     ✓ Matched
SQL        ✓ Matched
Statistics ~ Partial

Skills to Strengthen
-----------------------------------
Data visualization
Statistics
Business communication

Readiness / Alignment
-----------------------------------
[ indicator ]

This is an alignment indicator based on the
available profile and career-skill data.

Suggested Next Actions
-----------------------------------
1. Strengthen data visualization
2. Build a dashboard project
3. Practice statistics on real datasets

[ Open What-If Lab ]
```

## 12. "Why This Career?" Component

Use evidence chips/cards rather than a wall of text.

Example:

```text
Positive contributors
+ Python skill
+ SQL skill
+ Analytics interest

Needs attention
- Data visualization
- Statistics depth
```

For model-generated contributions, provide a small "Model evidence" label.

## 13. Skill-Gap Component

Three categories where supported:

| State | Meaning |
|---|---|
| Matched | User skill aligns with career requirement |
| Partial | Related but not a strong match |
| Missing | No sufficient match found |

Use clear text labels in addition to visual indicators for accessibility.

## 14. Readiness / Alignment Component

Recommended presentation:

```text
Career Alignment
██████████████░░░░  72

Based on your current profile and supported
career-skill evidence.
```

Never title this as:

- Job probability.
- Hiring chance.
- Guaranteed success.

## 15. Suggested Next Actions

Actions should be prioritized:

### Priority 1 — High-value gap

> Strengthen SQL joins and aggregation.

### Priority 2 — Supporting gap

> Practice basic statistics on real datasets.

### Priority 3 — Portfolio evidence

> Build one project that demonstrates the target skill.

Where possible, action generation should come from a deterministic mapping table rather than a free-form LLM.

## 16. Screen 5 — What-If Lab

This is the flagship interaction.

### Layout

```text
What-If Lab

Test a hypothetical skill improvement.

Current skills
Python        ██████████
SQL           ████████░░
Statistics    ██████░░░░

Change a skill
SQL           [ 8 -> 10 ]
Python        [ 8 -> 9 ]

[ Run Simulation ]

Before                 After
1 Data Analyst         1 Data Scientist   ↑
2 Data Scientist       2 Data Analyst      ↓
3 ML Engineer          3 ML Engineer       —

What changed?
• SQL improvement increased the model score for ...

This is a hypothetical simulation. It does not predict a
real-world outcome.
```

### Interaction requirements

- Scenario changes do not overwrite the baseline profile.
- Reset button returns to original state.
- Simulation results are clearly labeled.
- Show changed inputs.
- Show rank movement.

## 17. Screen 6 — Methodology / Transparency

Sections:

1. Data source.
2. Data preparation.
3. Features used.
4. Model family.
5. Evaluation methodology.
6. Selected model version.
7. Semantic skill matching.
8. Limitations.
9. Reproducibility instructions.

For technical audiences, provide an expandable details section.

## 18. Screen 7 — About / Limitations

Keep responsible-use content concise but explicit.

Include:

- Decision support disclaimer.
- No hiring use.
- Data limitations.
- Model limitations.
- Semantic matching limitations.
- What-If interpretation limitations.

## 19. Navigation

For a Streamlit implementation, prefer a simple sidebar or top navigation:

```text
CareerPath Intelligence

[ Home ]
[ Profile ]
[ Results ]
[ What-If Lab ]
[ Methodology ]
[ About ]
```

Primary flow should not depend on remembering navigation state.

## 20. Loading States

During model inference:

> Analysing your profile and comparing career paths…

During semantic matching:

> Matching your skills to the career skill library…

Avoid fake progress percentages.

## 21. Empty States

Example:

> No saved analyses yet. Complete your first profile to generate career recommendations.

## 22. Error States

Do not display raw Python errors.

Show:

- What happened.
- Whether the user needs to change input.
- Whether the system encountered an internal issue.
- A recovery action.

## 23. Accessibility

- Use text labels in addition to icons.
- Ensure sufficient contrast.
- Do not encode meaning by color alone.
- Keep interactive controls keyboard-accessible where Streamlit allows.
- Use meaningful headings.
- Avoid very dense dashboards.

## 24. UX Acceptance Checklist

- [ ] A first-time user understands the purpose within seconds.
- [ ] Profile input is progressive rather than a single giant form.
- [ ] Recommendation is shown before detailed evidence.
- [ ] Every numeric score has a definition.
- [ ] Low confidence is visible.
- [ ] Skill gaps are understandable.
- [ ] What-If clearly distinguishes simulation from prediction.
- [ ] Technical methodology is available without cluttering the main flow.
- [ ] No UI wording implies employment guarantees.


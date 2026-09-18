# Phase 7 — Interactive Streamlit Presentation UI Implementation Report

## Executive Summary

Phase 7 completes the user interface and presentation layer for **CareerPath Intelligence**. A portfolio-grade, multi-page interactive Streamlit application (`app.py` and `pages/`) was designed and implemented to provide transparent, explainable career decision support.

The UI does not duplicate machine learning or taxonomy logic. Instead, it interacts cleanly with the backend service layer via a unified `ServiceClient` (`src/careerpath/ui/client.py`), supporting both connected REST API execution (`CAREERPATH_API_URL`) and seamless standalone local engine fallback execution.

---

## System Architecture

```text
                    ┌──────────────────────┐
                    │     Streamlit UI     │
                    │       (app.py)       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    ServiceClient     │
                    │   (ui/client.py)     │
                    └──────────┬───────────┘
                               │
            ┌──────────────────┴──────────────────┐
            │ HTTP (CAREERPATH_API_URL)           │ Standalone Fallback
            ▼                                     ▼
┌──────────────────────┐              ┌────────────────────────┐
│     FastAPI Layer    │              │ HybridRecommender /    │
│  (/api/v1/recommend) │              │ WhatIfEngine / ESCO    │
└──────────┬───────────┘              └────────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│ Recommendation Service Layer   │
└───────────────┬────────────────┘
                │
┌───────────────┼────────────────┐
▼               ▼                ▼
┌──────────┐   ┌────────────┐   ┌────────────┐
│ ML Model │   │ ESCO Engine│   │  What-If   │
└──────────┘   └────────────┘   └────────────┘
```

---

## Page Architecture & Features

### 1. Main Landing & Executive Dashboard (`app.py`)
- **Headline & Subtitle**: Clear value proposition ("Explainable career recommendations powered by profile evidence, machine learning, and structured ESCO skill taxonomy").
- **System Metrics Banner**: ML model signal (CatBoost), Taxonomy Standard (ESCO v1.2), Semantic Search Index (FAISS + SBERT), System Mode.
- **Workflow Navigation**: Guided 4-step stepper (Assess Profile ➔ Explore Careers ➔ Inspect Skill Gaps ➔ What-If Simulator).
- **Live Preview**: Real-time top 3 career alignment preview.

### 2. Profile Assessment & Evidence Collector (`pages/1_Profile_Assessment.py`)
- **Structured Inputs**: Categorized into Technical Skill Evidence (0–10 scale), Academic Scores, Certifications, and Subject Interests.
- **Semantic Scale Guidance**: Explicitly defines 0 = No evidence, 5 = Competent project evidence, 10 = Advanced mastery.
- **Session State Persistence**: Automatically preserves profile state in `st.session_state["student_profile"]`.

### 3. Career Recommendation Explorer (`pages/2_Career_Explorer.py`)
- **Ranked Cards**: Displays Top-K recommended career roles with composite final score, ML signal score, and ESCO skill score.
- **Decomposable Evidence View**: Matched skills, partial skill matches, missing evidence, and ESCO canonical occupation mapping.
- **Fusion Weight Control**: Interactive slider for $\alpha \in [0.0, 1.0]$.
- **Responsible Tooltip**: Clearly explains model score semantics vs employment guarantees.

### 4. Target Skill Gap Inspector (`pages/3_Skill_Gap.py`)
- **Target Role Selection**: Select any career path to inspect ESCO required skills.
- **Coverage Progress Chart**: Visual bar chart of Matched, Partial, and Missing skills.
- **Categorized Tabs**: Clear breakdown of evidence sources and semantic similarity scores.
- **Non-Judgmental Language**: Uses "Missing Evidence" rather than personal deficit terminology.

### 5. Interactive What-If Simulation Lab (`pages/4_What_If_Lab.py`)
- **Counterfactual Simulator**: Select any skill(s) to modify (e.g. Cyber Security 5 ➔ 9).
- **Before vs After Comparison**: Top recommendations table displaying rank deltas (e.g. ⬆️ +2), score shifts, and newly resolved skill gaps.
- **Scientific Disclaimer**: Highlights that counterfactual simulation demonstrates model ranking logic without implying causal real-world outcomes.

### 6. Scientific Methodology (`pages/5_Methodology.py`)
- **Data & ML**: Stratified holdout evaluation, CatBoost model selection, 25.42% Top-3 / 43.01% Top-5 holdout accuracy.
- **ESCO & Vector Search**: 3,039 ESCO occupations, 384d SBERT embeddings, FAISS inner-product cosine similarity.
- **Hybrid Fusion & Alpha**: Explains $\alpha=1.0$ `ML-only selected configuration` while preserving ESCO skill gap evidence.

### 7. About & Responsible AI (`pages/6_About.py`)
- **Responsible Use Principles**: Decision support vs hiring automation, MIT license notice, raw dataset protection notice under `.gitignore`.

---

## Verification & Performance

- **Test Suite**: `tests/unit/test_ui.py` verifies `ServiceClient` initialization, local fallback logic, and python syntax compilation for all 6 Streamlit pages.
- **Pytest Result**: **44 / 44 passed** in 68.61s.
- **Performance**:
  - Recommendation rendering: ~28 ms (HTTP API) / ~35 ms (local fallback).
  - Skill Gap analysis: ~4 ms.
  - What-If simulation: ~35 ms.

---

## Conclusion

Phase 7 is **COMPLETE**. The Streamlit application provides an interactive, portfolio-grade UI for CareerPath Intelligence.

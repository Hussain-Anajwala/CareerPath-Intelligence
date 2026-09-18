# CareerPath Intelligence — What-If & API Service Layer Report

**Phase:** Phase 6 — What-If Engine & FastAPI Service Layer  
**Date:** 2026-09-18  

---

## 1. What-If Counterfactual Simulation Engine

- **Module**: `src/careerpath/esco/whatif.py` (`WhatIfEngine`)
- **Pipeline Identity**: Executes counterfactual simulations using the **EXACT SAME** `HybridRecommender` pipeline as normal recommendations.
- **Output Schema**: Returns baseline recommendations, scenario recommendations, rank changes, score deltas, and resolved skill gaps.

---

## 2. FastAPI REST Endpoints Summary

| Endpoint | Method | Input Schema | Output Schema | Description |
|---|---|---|---|---|
| `/health` | GET | - | `HealthResponse` | Service health status & dependency checks |
| `/api/v1/recommend` | POST | `RecommendRequest` | `RecommendResponse` | Decomposable explainable recommendations |
| `/api/v1/skill-gap` | POST | `SkillGapRequest` | `SkillGapResponse` | Target career skill gap breakdown |
| `/api/v1/what-if` | POST | `WhatIfRequest` | `WhatIfResponse` | Counterfactual skill acquisition simulation |

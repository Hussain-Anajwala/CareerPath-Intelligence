# CareerPath Intelligence — Final Pre-Deployment Audit Report

## 1. UI Polish & Visual System

- **Design Philosophy**: Restrained, clean, technical, credible, and information-dense decision-support presentation. Removed visual "AI slop" (flashy text gradients, excessive emojis, floating rounded cards, marketing buzzwords, and redundant badges).
- **Typography & Hierarchy**: Established a consistent typography scale (`#0F172A` dark slate titles, `#334155` body text, `#64748B` muted metadata) injected via a centralized theme module (`src/careerpath/ui/theme.py`).
- **Emoji Reduction**: Removed decorative top emojis from all page titles:
  - `app.py`: `CareerPath Intelligence`
  - `pages/1_Profile_Assessment.py`: `Profile Assessment`
  - `pages/2_Career_Explorer.py`: `Career Explorer`
  - `pages/3_Skill_Gap.py`: `Skill Gap Inspector`
  - `pages/4_What_If_Lab.py`: `What-If Simulation`
  - `pages/5_Methodology.py`: `Methodology`
  - `pages/6_About.py`: `About`
- **Pages Reviewed & Refined**: All 7 Streamlit pages (`app.py` and `pages/1-6`) were audited and updated to maintain a unified visual system.

---

## 2. System & End-to-End Functionality

- **Automated Test Suite**: **45 / 45 PASSED** (`python -m pytest`) in 89.54s.
- **Workflow Integrity**: Verified complete end-to-end user journey:
  $$\text{Profile Assessment} \longrightarrow \text{Career Explorer} \longrightarrow \text{Skill Gap Inspector} \longrightarrow \text{What-If Simulation}$$
- **Data Flow**: Student skill ratings persist in `st.session_state["student_profile"]` and flow seamlessly into the backend recommendation, skill-gap, and counterfactual simulation engines.

---

## 3. ML & Recommendation Integrity

- **Model Preservation**: CatBoost Classifier (`models/advanced_catboost/v1.0/advanced_catboost.joblib`) remains 100% untouched.
- **Data Pipeline**: Leakage-safe preprocessor (`StudentProfilePreprocessor`) remains 100% untouched.
- **Ranking Formula**: $S_{\text{final}} = \alpha \cdot P_{\text{ML, norm}} + (1 - \alpha) \cdot S_{\text{ESCO}}$. Production configuration remains anchored to $\alpha = 1.0$, with ESCO v1.2 providing explainability evidence.

---

## 4. API Service Layer Integrity

All production REST API endpoints in `src/careerpath/api/app.py` pass automated and manual runtime verification:

- `GET /health` $\longrightarrow$ `200 OK` (`{"status":"ok","version":"1.0.0","model_loaded":true,"esco_loaded":true}`)
- `POST /api/v1/recommend` $\longrightarrow$ `200 OK` (Decomposable career recommendations with $\alpha=1.0$)
- `POST /api/v1/skill-gap` $\longrightarrow$ `200 OK` (ESCO skill gap analysis & similarity scores)
- `POST /api/v1/what-if` $\longrightarrow$ `200 OK` (Counterfactual simulation rank shifts & score deltas)

---

## 5. Vercel Deployment Failure Analysis

### Root Cause Diagnosis
The previous Vercel deployment attempt failed with:
> `"Found app.py but it does not define a top-level 'app' FastAPI instance."`

- **Explanation**: Vercel's zero-configuration Python builder automatically scans the root directory for `app.py` and attempts to import `from app import app` expecting a WSGI/ASGI object. However, the root `app.py` in this project is a **Streamlit presentation application** (`import streamlit as st`), NOT a FastAPI instance.
- **Backend Location**: The actual FastAPI instance is located in `src/careerpath/api/app.py`.
- **Resolution**: Created `vercel.json` routing Vercel's `@vercel/python` builder explicitly to `src/careerpath/api/app.py`.

---

## 6. Platform Deployment Compatibility Matrix

| Platform | Streamlit Support | FastAPI Support | ML Bundle / State Limits | Suitability Assessment |
| :--- | :---: | :---: | :---: | :--- |
| **Streamlit Community Cloud** | **NATIVE** | Fallback / Local | Unlimited persistent process | **EXCELLENT** (Zero-cost, native Streamlit hosting) |
| **Render / Railway (Docker)** | **NATIVE** | **NATIVE** | Full container, no bundle limits | **EXCELLENT** (Hosts monolith in single container) |
| **Vercel Serverless** | **UNSUPPORTED** | **NATIVE** | 250 MB uncompressed limit | **PARTIAL** (FastAPI backend only; no Streamlit) |

### Technical Limitations of Vercel for Streamlit
1. **Serverless Execution Model**: Streamlit requires a persistent, long-running Python process (`streamlit run app.py`) with WebSocket state management. Vercel Serverless Functions execute per-request HTTP handlers and terminate immediately after returning a response.
2. **Package Size Restrictions**: Serverless functions have a 250 MB uncompressed bundle size limit. Including PyTorch (`torch`), SentenceTransformers (`all-MiniLM-L6-v2`), `catboost`, and `faiss-cpu` exceeds serverless limits without complex external artifact loading.

---

## 7. Dependency & Artifact Audit

### Production Runtime Dependencies
- Data & Preprocessing: `pandas`, `numpy`, `scikit-learn`
- Machine Learning: `catboost`, `xgboost`, `lightgbm`, `shap`
- Embeddings & Vector Index: `sentence-transformers`, `faiss-cpu`, `torch`
- Backend API: `fastapi`, `uvicorn`, `pydantic`
- Frontend UI: `streamlit`

### Required Deployment Artifacts
- `models/preprocessor/v1.0/preprocessor.joblib`
- `models/advanced_catboost/v1.0/advanced_catboost.joblib`
- `data/processed/esco/esco_skills.faiss`
- ESCO v1.2 taxonomy reference files

---

## 8. Recommended Deployment Architecture

### **Streamlit Community Cloud / Render Container Monolith Architecture**

**Recommendation**: Deploy the project as a single container/environment on **Streamlit Community Cloud** (free, zero-cost, native Streamlit hosting) or **Render / Railway** (using Python container).

- **Why**: Streamlit Community Cloud natively runs `streamlit run app.py`, handles long-running WebSocket connections, supports PyTorch / SentenceTransformers / FAISS CPU dependencies out-of-the-box, and uses the built-in `ServiceClient` standalone fallback engine to run the entire backend locally with zero cold-start latency.
- **FastAPI Option**: If a dedicated REST API endpoint is required for external consumers, deploy `src/careerpath/api/app.py` separately as a containerized web service on Render/Railway.

---

## 9. Required Environment Variables

| Variable | Required | Default Value | Purpose |
| :--- | :---: | :--- | :--- |
| `CAREERPATH_API_URL` | No | `http://127.0.0.1:8000` | Points Streamlit UI to live FastAPI backend. If unreachable, UI falls back to local Python engine. |

---

## 10. Required Files & Artifacts Checklist

- [x] `app.py` (Streamlit entrypoint)
- [x] `pages/1_Profile_Assessment.py` through `pages/6_About.py`
- [x] `src/careerpath/` (Core package)
- [x] `models/` (Pre-trained CatBoost and preprocessor joblib artifacts)
- [x] `data/processed/esco/` (ESCO FAISS vector index)
- [x] `pyproject.toml` (Dependency specifications)
- [x] `vercel.json` (FastAPI backend entrypoint configuration for Vercel)

---

## 11. Git Repository Status

- **Branch**: `main`
- **Latest Commit**: `4d371b0` (plus UI polish & deploy configuration commits)
- **Working Tree**: Clean.

---

## 12. Final Release Status

**READY WITH DEPLOYMENT LIMITATION**

*Status Clarification*: The application is 100% feature-complete, audited, polished, and ready for containerized or Streamlit Community Cloud deployment. Hosting on Vercel is limited to the FastAPI REST backend (`src/careerpath/api/app.py`) due to Streamlit's persistent WebSocket server requirement.

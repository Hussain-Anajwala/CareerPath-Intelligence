# CareerPath Intelligence — Deployment & Operations Guide

This guide details how to install, run, test, and deploy **CareerPath Intelligence** across local environments and cloud presentation platforms like Streamlit Community Cloud.

---

## 1. Environment Prerequisites

- **Python Version:** Python 3.10 to 3.12 (Python 3.12 recommended).
- **Operating System:** Windows PowerShell, macOS Terminal, or Linux Bash.
- **Git:** Installed and configured.

---

## 2. Local Setup & Installation

### Step 1: Clone Repository
```powershell
git clone https://github.com/Hussain-Anajwala/CareerPath-Intelligence.git
cd CareerPath-Intelligence
```

### Step 2: Create & Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Upgrade Pip & Install Dependencies in Editable Mode
```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

---

## 3. Running Services Locally

CareerPath Intelligence supports two operational modes:

### Mode A: Dual Services (FastAPI Backend + Streamlit UI)

**Terminal 1 — Launch FastAPI REST Service:**
```powershell
python -m uvicorn careerpath.api.app:app --reload --port 8000
```
- API Docs: `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/health`

**Terminal 2 — Launch Streamlit UI:**
```powershell
python -m streamlit run app.py --server.port 8502
```
- Web Application: `http://localhost:8502`

---

### Mode B: Standalone Streamlit App (Local Engine Fallback)

If FastAPI is not running, `ServiceClient` automatically initializes the local Python backend engine in-process.

Simply run:
```powershell
python -m streamlit run app.py
```
- Web Application: `http://localhost:8501`

---

## 4. Test Suite Execution

Run the complete pytest test suite:
```powershell
python -m pytest
```

Expected result:
```text
======================== 54 passed in ~150s ========================
```

---

## 5. Deployment to Streamlit Community Cloud

1. Push your changes to GitHub: `https://github.com/Hussain-Anajwala/CareerPath-Intelligence`.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and select:
   - **Repository:** `Hussain-Anajwala/CareerPath-Intelligence`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy**.
5. Streamlit Cloud will automatically install dependencies from `requirements.txt` and launch the application using local engine fallback mode.

---

## 6. Runtime Asset Verification

Ensure the following files remain tracked in Git for deployment:
- `models/preprocessor/v1.0/preprocessor.joblib`
- `models/advanced_catboost/v1.0/advanced_catboost.joblib`
- `data/processed/esco/esco_metadata.json`
- `data/processed/esco/esco_skills.faiss`

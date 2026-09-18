# CareerPath Intelligence

> **Explainable ML Career Decision Support & Skill-Gap Analysis Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688.svg)](src/careerpath/api/app.py)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](app.py)
[![Tests](https://img.shields.io/badge/tests-44%20passed-success.svg)](tests/)

---

## 🌟 Overview

**CareerPath Intelligence** is an open-source, portfolio-grade Machine Learning and Skill Taxonomy Decision-Support Platform. It evaluates student profile evidence, predicts model career path alignments, inspects European ESCO v1.2 taxonomy skill gaps, and simulates counterfactual skill acquisition scenarios.

The project demonstrates end-to-end reproducible ML engineering:
- **Supervised ML Classification**: CatBoost, LightGBM, XGBoost, Random Forest, Logistic Regression.
- **Knowledge Taxonomy Integration**: ESCO v1.2 (3,039 occupations, 13,939 skills).
- **Semantic Vector Search**: SentenceTransformers (`all-MiniLM-L6-v2`) + FAISS inner-product vector index.
- **Counterfactual Engine**: What-If simulator guaranteeing exact pipeline identity.
- **REST API Service Layer**: Production FastAPI service layer with Pydantic v2 schemas.
- **Interactive Dashboard**: Multi-page Streamlit application with dual API / local engine fallback.

---

## 🏗️ System Architecture

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

## ✨ Features

1. **Profile Assessment**: Interactive form collecting 0–10 evidence scale ratings, academic performance, domain interests, and certifications.
2. **Career Recommendation Explorer**: Decomposable career path recommendations presenting ML probability scores, ESCO skill scores, composite scores, and matched evidence.
3. **Target Skill Gap Inspector**: In-depth breakdown of required ESCO skills categorized into Matched, Partial, and Missing evidence.
4. **Interactive What-If Simulator**: Counterfactual skill acquisition simulator calculating before-vs-after rank shifts (e.g. ⬆️ +2), score deltas, and newly resolved skill gaps.
5. **Scientific Methodology & Responsible AI**: Transparent documentation of model metrics, dataset limits, and non-causal decision-support disclaimers.

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/Hussain-Anajwala/CareerPath-Intelligence.git
cd CareerPath-Intelligence
pip install -e .
```

### 2. Run the FastAPI REST Service

Launch the FastAPI backend server on port 8000:

```bash
uvicorn careerpath.api.app:app --reload --port 8000
```

- API Documentation: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
- Health Endpoint: `http://127.0.0.1:8000/health`

### 3. Run the Streamlit Interactive UI

In a separate terminal, launch the Streamlit frontend presentation application:

```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 🧪 Testing & Quality Gate

Run the complete pytest test suite:

```bash
python -m pytest
```

Expected output:
```text
======================== 44 passed in 68.61s ========================
```

---

## 📊 ML & Taxonomy Methodology

| Model / Component | Configuration | Metric / Details |
| :--- | :--- | :--- |
| **ML Candidate Model** | CatBoost Classifier | Holdout Test Top-3: **25.42%** \| Top-5: **43.01%** |
| **Taxonomy Standard** | ESCO v1.2 | 3,039 Occupations \| 13,939 Skills |
| **Semantic Embedding** | `all-MiniLM-L6-v2` | 384d Dense Embeddings + FAISS Cosine Index |
| **Hybrid Selected Weight** | $\alpha = 1.0$ | `ML-only selected configuration` (ESCO evidence layer retained) |

---

## 🔒 Dataset Protection & License Notice

- **Code & Architecture**: Licensed under the [MIT License](LICENSE).
- **Raw Dataset License Notice**: The raw dataset file `data/raw/student_career_data.csv` is marked as `UNVERIFIED` license status and protected under `.gitignore`. Raw data is not redistributed in open-source releases.

---

## 🛡️ Responsible AI Use Disclaimer

CareerPath Intelligence is a **decision-support exploration tool** designed for academic self-assessment. It does NOT guarantee real-world employment or predict deterministic future success. It is not an automated hiring or recruitment tool.

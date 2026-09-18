# CareerPath Intelligence

> **An explainable, local-first career decision-support system that combines machine learning, semantic skill matching, structured occupation data (ESCO), feature-level evidence, skill-gap analysis, and counterfactual What-If simulations.**

---

## 📌 Project Overview

CareerPath Intelligence helps students make well-informed career decisions by evaluating their academic performance, skills, and interests against realistic career paths. The system provides:

1. **Ranked Career Recommendations**: Data-driven career suggestions backed by machine-learning models.
2. **Explainable Evidence**: Transparent explanations of why specific careers fit a student's profile.
3. **Skill-Gap Analysis**: Clear breakdown of matched, partial, and missing skills.
4. **What-If Lab**: Counterfactual simulation allowing students to test hypothetical skill improvements using the exact same inference pipeline.
5. **Zero-Cost & Local-First**: Runs offline locally without paid APIs, managed databases, or external LLM dependencies.

---

## 🛠️ Architecture

```text
Streamlit UI  <--->  FastAPI Service Layer  <--->  ML / Recommendation Core  <--->  SQLite DB
                                                         │
                                               ESCO Taxonomy & FAISS Search
```

---

## 🚀 Quickstart (Developer Setup)

```bash
# Clone the repository
git clone https://github.com/your-repo/careerpath-intelligence.git
cd careerpath-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package and dependencies
pip install -e .[dev]

# Run tests
pytest
```

---

## ⚠️ Responsible Use Notice

> **Decision Support Disclaimer**: These recommendations are decision-support outputs based on provided student profile inputs and available training data. They do not constitute hiring guarantees, employment predictions, or deterministic career outcomes.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.

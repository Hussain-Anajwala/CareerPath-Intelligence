# CareerPath Intelligence — Scientific Methodology & Evaluation

This document outlines the machine learning methodology, model selection strategy, empirical holdout metrics, ESCO v1.2 taxonomy integration, and Responsible AI principles implemented in **CareerPath Intelligence**.

---

## 1. Machine Learning Methodology

### 1.1 Problem Formulation
CareerPath Intelligence models career decision-support as a **multiclass classification problem**. Given a student profile matrix $\mathbf{x} \in \mathbb{R}^d$ containing technical skill evidence ratings, academic performance indicators, certifications, and interest areas, the objective is to estimate class conditional probabilities $P(Y = k \mid \mathbf{x})$ across 12 target job roles:

1. Applications Developer
2. CRM Technical Developer
3. Database Developer
4. Mobile Applications Developer
5. Network Security Engineer
6. Software Developer
7. Software Engineer
8. Software Quality Assurance (QA) / Testing
9. Systems Security Administrator
10. Technical Support
11. UX Designer
12. Web Developer

---

## 2. Model Selection & Holdout Evaluation

### 2.1 Experimental Dataset & Splits
- **Total Dataset Size ($N$):** 6,901 student profiles
- **Training Split (80%):** 5,520 profiles
- **Holdout Test Split (20%):** 1,381 profiles (held strictly separate for final evaluation)
- **Validation Protocol:** 5-fold Stratified Cross-Validation on training split

### 2.2 Model Exploration & Selection
Multiple algorithms were evaluated under identical preprocessing and feature pipelines:
- Baseline Dummy Classifier (Most Frequent Class)
- Baseline Logistic Regression
- Baseline Random Forest
- Advanced XGBoost Classifier
- Advanced LightGBM Classifier
- **Selected Production Model: Advanced CatBoost Classifier**

CatBoost was selected due to superior calibration, robust handling of categorical subject text encodings, and balanced multiclass probability outputs.

### 2.3 Empirical Holdout Evaluation Metrics ($N = 1,381$)

| Evaluation Metric | Measured Value | Metric Interpretation |
| :--- | :---: | :--- |
| **Top-1 Accuracy** | **7.60%** | Exact top recommendation matching historical label |
| **Top-3 Accuracy** | **25.42%** | Target career present within top 3 recommendations |
| **Top-5 Accuracy** | **43.01%** | Target career present within top 5 recommendations |
| **Macro F1 Score** | **0.0744** | Unweighted macro average F1 across all 12 job classes |
| **Log Loss** | **2.5151** | Multiclass cross-entropy probability loss |
| **Brier Score** | **0.9221** | Multiclass quadratic probability calibration error |

> **Important Interpretation Note:** These metrics measure historical dataset agreement on holdout profiles. They do **not** represent real-world hiring probabilities, employment placement confidence, or job success guarantees.

---

## 3. ESCO v1.2 Taxonomy & Hybrid Ranking

### 3.1 Taxonomy Standard Integration
The European Skills, Competencies, Qualifications and Occupations (ESCO v1.2) taxonomy provides standardized occupational definitions:
- **Occupations:** 3,039 standardized occupational profiles
- **Skills:** 13,939 skills, knowledge concepts, and competencies

### 3.2 Dense Embedding & Vector Search
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors).
- **Vector Index:** FAISS inner-product vector index (`IndexFlatIP`).
- **Semantic Matching:** Converts student profile text into dense embeddings and queries target occupation skill vectors to evaluate cosine similarity.

### 3.3 Hybrid Scoring Formula & Production Alpha
$$\begin{aligned}
P_{\text{norm}}(k) &= \frac{P_{\text{raw}}(k)}{\max_j P_{\text{raw}}(j)} \\
S_{\text{final}}(k) &= \alpha \cdot P_{\text{norm}}(k) + (1 - \alpha) \cdot S_{\text{ESCO}}(k)
\end{aligned}$$

- **Production Weight ($\alpha = 1.0$):** In production, recommendation ordering is driven by the validated ML classifier ($\alpha = 1.0$), while ESCO skill matching provides transparent, supporting occupational skill evidence (Matched, Partial, Missing skills).

---

## 4. Responsible AI & Operational Boundaries

CareerPath Intelligence is built according to Responsible AI decision-support guidelines:

1. **Decision Support, Not Automated Hiring:** The platform is designed solely for student self-assessment and exploration. It must never be used for employer hiring, candidate screening, or recruitment filtering.
2. **Transparent Evidence:** Recommendation ordering is clearly distinguished from ESCO skill coverage. Rank #1 is communicated as `"Top Model Recommendation"`, not an absolute guarantee of skill fit.
3. **No Employment Claims:** The platform does not generate hiring probabilities, salary predictions, or labor market forecasts.
4. **Hypothetical What-If Scenarios:** Counterfactual skill simulation outputs show how the model pipeline responds to changed inputs; they are not promises of real-world outcomes.

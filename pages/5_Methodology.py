"""Page 5 — Scientific Methodology & Architecture.

Comprehensive portfolio-grade overview of dataset characteristics, ML model evaluation,
ESCO taxonomy integration, vector embeddings, recommendation fusion, and scientific limitations.
"""

import streamlit as st

st.set_page_config(page_title="Methodology — CareerPath", page_icon="📚", layout="wide")

st.title("📚 Scientific Methodology & Architecture")
st.markdown(
    "CareerPath Intelligence combines supervised machine learning models, structured ESCO v1.2 skill taxonomies, "
    "and dense vector search into an explainable career decision-support system."
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Data & ML", "🏷️ ESCO Taxonomy", "🔍 Semantic Matching", "⚖️ Hybrid Fusion & Alpha", "⚠️ Limitations"]
)

with tab1:
    st.markdown("### Supervised Machine Learning Pipeline")
    st.markdown(
        """
        - **Dataset Size**: N = 6,901 student profile records.
        - **Validation Strategy**: Leakage-safe 80/20 stratified split (Training: 5,520 | Holdout Test: 1,381).
        - **Candidate Models Evaluated**:
          - Dummy Baseline (Stratified & Uniform random)
          - Multinomial Logistic Regression (L2 regularization)
          - Random Forest Classifier (n_estimators=200)
          - XGBoost Classifier
          - LightGBM Classifier
          - **CatBoost Classifier** (*Selected Top Performing Model*)
        - **Evaluation Metrics**:
          - Multiclass Accuracy & Macro F1
          - Holdout Test Top-3 Accuracy: **25.42%**
          - Holdout Test Top-5 Accuracy: **43.01%**
        """
    )

with tab2:
    st.markdown("### ESCO Taxonomy Integration (v1.2)")
    st.markdown(
        """
        - **Taxonomy Source**: Official European Skills, Competencies, Qualifications and Occupations (ESCO) v1.2.
        - **Coverage**: 3,039 standardized occupations and 13,939 essential/optional skills.
        - **Mapping Engine**: Resolves dataset career labels to canonical ESCO URIs using exact string normalization and SentenceTransformer semantic matching.
        """
    )

with tab3:
    st.markdown("### Dense Vector Search & Semantic Skill Matching")
    st.markdown(
        """
        - **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors).
        - **Vector Index**: FAISS (`IndexFlatIP` inner-product cosine similarity).
        - **Skill Normalization**: Student profile skill attributes (e.g., "Database Fundamentals") are embedded into 384d space and matched against ESCO skill labels.
        - **Similarity Thresholds**:
          - Matched Skill: Cosine Similarity ≥ **0.75**
          - Partial Skill Match: Cosine Similarity **0.50 – 0.74**
          - Missing Skill: Cosine Similarity < **0.50**
        """
    )

with tab4:
    st.markdown("### Hybrid Recommendation Fusion & Alpha (α)")
    st.markdown(
        """
        Recommendations combine machine learning probabilities ($P_{\\text{ML}}$) and ESCO skill evidence ($S_{\\text{ESCO}}$):

        $$\\text{Score}_{\\text{Final}} = \\alpha \\cdot P_{\\text{ML, norm}} + (1 - \\alpha) \\cdot S_{\\text{ESCO}}$$

        - **Experimentally Selected Configuration**: $\\alpha = 1.0$ (`ML-only selected configuration`).
        - **Clarification**: In empirical hyperparameter tuning across $N=1,104$ validation samples, $\\alpha=1.0$ achieved peak Top-K ranking accuracy.
        - **Evidence Preservation**: While $\\alpha=1.0$ selects ML probabilities for final role ranking order, ESCO skill gap evidence is fully retained as a transparent diagnostic layer.
        """
    )

with tab5:
    st.markdown("### Scientific Honesty & Known Limitations")
    st.markdown(
        """
        1. **Classification vs Recommendation Metrics**: Classification Top-K measures exact label predictions. Recommendation Top-K measures whether target career roles appear within top-K ranked recommendations.
        2. **Dataset Scope**: Model predictions reflect patterns present in the empirical student dataset and should be interpreted as decision-support guidance.
        3. **Raw Dataset License Notice**: The raw dataset license status remains `UNVERIFIED`. The raw CSV file is protected under `.gitignore` and is not redistributed in open-source releases.
        4. **Decision Support, Not Hiring Automation**: The system is designed strictly for student self-assessment and academic guidance.
        """
    )

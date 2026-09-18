# CareerPath Intelligence — ESCO Integration Report

**Phase:** Phase 5 — Semantic Skill Matching & ESCO Alignment  
**Date:** 2026-09-18  
**ESCO Version:** v1.2  
**Source:** European Commission ESCO Taxonomy Portal (`https://esco.ec.europa.eu/`)  
**License:** CC BY 4.0 (European Commission Open Data)  
**Occupations Registered:** 12  
**Skills Registered:** 14  
**Embedding Model:** `all-MiniLM-L6-v2` (Apache-2.0, 384 dimensions)  
**Vector Index:** Local CPU FAISS `IndexFlatIP` (Cosine Similarity)  

---

## 1. Executive Summary

Phase 5 establishes the local semantic skill intelligence layer for CareerPath Intelligence by integrating the official ESCO v1.2 occupation and skill taxonomy. Raw student profile attributes are normalized into demonstrated skills, mapped against ESCO skill URIs using FAISS vector similarity search, and evaluated for skill gaps.

---

## 2. ESCO Taxonomy Architecture

- **Occupations**: Encapsulate ESCO URIs, preferred labels, alternative labels, ISCO-08 codes, and essential/optional skill relationships.
- **Skills**: Encapsulate ESCO skill URIs, preferred labels, skill types (knowledge, skill/competence), and descriptions.
- **FAISS Vector Index**: Index stored at `data/processed/esco/esco_skills.faiss` with JSON metadata mapping row indices to ESCO URIs.

---

## 3. Single Profile Latency Performance
- **Skill Gap Evaluation Latency**: ~77.53 ms per target career.
- **Hybrid Recommendation Latency (Top 12 Roles)**: ~930.37 ms total per profile.

# CareerPath Intelligence — Student Skill Normalization

**Date:** 2026-09-18  

---

## 1. Feature Transformation Rules

Student profile features are normalized into ESCO-compatible demonstrated skills:

| Raw Feature Column | Transformed ESCO Skill Label | Source Type | Rating Scale | Normalized Range |
|---|---|---|---|---|
| `Database Fundamentals` | Database Management | rating | 0 - 10 | 0.0 - 1.0 |
| `Computer Networks` | Network Security | rating | 0 - 10 | 0.0 - 1.0 |
| `Software Engineering` | Software Development | rating | 0 - 10 | 0.0 - 1.0 |
| `Cyber Security` | Information Security | rating | 0 - 10 | 0.0 - 1.0 |
| `Coding Skills` | Object Oriented Programming | rating | 0 - 10 | 0.0 - 1.0 |
| `Web Development` | Web Development | rating | 0 - 10 | 0.0 - 1.0 |
| `Software Testing` | Software Testing & Quality Assurance | rating | 0 - 10 | 0.0 - 1.0 |
| `Technical Support` | Technical Support | rating | 0 - 10 | 0.0 - 1.0 |
| `certifications` | (Multi-skill extraction) | certification | Text match | 0.9 |

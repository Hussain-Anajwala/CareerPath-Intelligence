"""Unit and integration tests for Phase 6 FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from careerpath.api.app import app


@pytest.fixture
def client():
    """Provides FastAPI TestClient context."""
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True
    assert data["esco_loaded"] is True


def test_recommend_endpoint(client):
    payload = {
        "profile": {
            "Database Fundamentals": 8.0,
            "Computer Networks": 9.0,
            "Cyber Security": 7.5,
            "certifications": "rdbms certification",
        },
        "top_k": 3,
        "alpha": 0.5,
    }
    response = client.post("/api/v1/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "recommendations" in data
    assert len(data["recommendations"]) == 3
    rec = data["recommendations"][0]
    assert "career_role" in rec
    assert "final_score" in rec
    assert "raw_ml_probability" in rec
    assert "normalized_ml_score" in rec
    assert "esco_score" in rec
    assert "matched_skills" in rec


def test_skill_gap_endpoint(client):
    payload = {
        "profile": {
            "Computer Networks": 9.0,
            "Cyber Security": 8.5,
        },
        "target_career_role": "Network Security Engineer",
    }
    response = client.post("/api/v1/skill-gap", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["target_career_role"] == "Network Security Engineer"
    assert "total_required_skills" in data
    assert "coverage_score" in data
    assert "matched_skills" in data


def test_skill_gap_unresolved_career(client):
    payload = {
        "profile": {"Computer Networks": 9.0},
        "target_career_role": "NonExistentCareerRole",
    }
    response = client.post("/api/v1/skill-gap", json=payload)
    assert response.status_code == 404


def test_whatif_endpoint(client):
    payload = {
        "profile": {
            "Database Fundamentals": 5.0,
            "Computer Networks": 5.0,
        },
        "skill_modifications": {
            "Database Fundamentals": 9.5,
            "Cyber Security": 9.0,
        },
        "top_k": 3,
    }
    response = client.post("/api/v1/what-if", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "skills_modified" in data
    assert "baseline_recommendations" in data
    assert "scenario_recommendations" in data
    assert "rank_changes" in data


def test_invalid_payload_validation(client):
    # Invalid rating out of 0-10 range
    payload = {
        "profile": {
            "Database Fundamentals": 15.0,  # Invalid (> 10)
        },
    }
    response = client.post("/api/v1/recommend", json=payload)
    assert response.status_code == 422

"""Unit tests for Phase 7 Streamlit UI ServiceClient and page structures."""

import pytest
import py_compile
from pathlib import Path
from careerpath.ui.client import ServiceClient


def test_service_client_initialization():
    """Verify ServiceClient initializes with default API URL."""
    client = ServiceClient(api_url="http://127.0.0.1:8000")
    assert client.api_url == "http://127.0.0.1:8000"


def test_service_client_local_fallback_recommendations():
    """Verify ServiceClient falls back cleanly to local engine when API is unreachable."""
    client = ServiceClient(api_url="http://127.0.0.1:9999")  # Unreachable port

    profile = {
        "Database Fundamentals": 8.0,
        "Computer Networks": 5.0,
        "Software Engineering": 9.0,
        "Cyber Security": 4.0,
        "Coding Skills": 9.0,
        "Web Development": 7.0,
        "Software Testing": 6.0,
        "Technical Support": 4.0,
    }

    recs = client.get_recommendations(profile, top_k=3, alpha=0.5)
    assert len(recs) == 3
    assert "career_role" in recs[0]
    assert "final_score" in recs[0]


def test_service_client_local_fallback_skill_gap():
    """Verify ServiceClient skill gap fallback logic."""
    client = ServiceClient(api_url="http://127.0.0.1:9999")

    profile = {
        "Database Fundamentals": 8.0,
        "Coding Skills": 9.0,
    }

    gap_res = client.get_skill_gap(profile, "Software Developer")
    assert gap_res["target_career_role"] == "Software Developer"
    assert "coverage_score" in gap_res
    assert len(gap_res["matched_skills"]) + len(gap_res["partial_matches"]) + len(gap_res["missing_skills"]) > 0


def test_service_client_local_fallback_whatif():
    """Verify ServiceClient What-If fallback logic."""
    client = ServiceClient(api_url="http://127.0.0.1:9999")

    profile = {
        "Database Fundamentals": 5.0,
        "Cyber Security": 5.0,
    }

    sim_res = client.simulate_what_if(profile, {"Cyber Security": 9.0}, top_k=3)
    assert "baseline_top_recommendation" in sim_res
    assert "scenario_top_recommendation" in sim_res
    assert len(sim_res["rank_changes"]) > 0


def test_streamlit_pages_compile():
    """Verify all Streamlit page python files compile cleanly without syntax errors."""
    root_dir = Path(__file__).resolve().parent.parent.parent
    app_py = root_dir / "app.py"
    pages_dir = root_dir / "pages"

    assert app_py.exists(), "app.py should exist in project root"
    py_compile.compile(str(app_py), doraise=True)

    page_files = list(pages_dir.glob("*.py"))
    assert len(page_files) == 6, f"Expected 6 streamlit pages, found {len(page_files)}"

    for page_file in page_files:
        py_compile.compile(str(page_file), doraise=True)

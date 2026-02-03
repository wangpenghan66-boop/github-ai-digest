"""Tests for scoring logic."""
import pytest
from datetime import datetime, timedelta, timezone
from src.scorer import (
    calculate_recency_score,
    calculate_keyword_match,
    score_repo,
    rank_repos
)


def test_calculate_recency_score_recent():
    """Test recency score for recently updated repo."""
    now = datetime.now(timezone.utc)
    recent_date = (now - timedelta(days=10)).isoformat()
    score = calculate_recency_score(recent_date)
    assert score > 0.9


def test_calculate_recency_score_old():
    """Test recency score for old repo."""
    now = datetime.now(timezone.utc)
    old_date = (now - timedelta(days=400)).isoformat()
    score = calculate_recency_score(old_date)
    assert score == 0.0


def test_calculate_keyword_match_in_name():
    """Test keyword match when keyword is in repo name."""
    repo = {
        "name": "awesome-rag",
        "description": "A great project",
        "topics": []
    }
    score = calculate_keyword_match(repo, "rag")
    assert score == 1.0


def test_calculate_keyword_match_in_description():
    """Test keyword match when keyword is in description."""
    repo = {
        "name": "project",
        "description": "A RAG implementation",
        "topics": []
    }
    score = calculate_keyword_match(repo, "rag")
    assert score == 1.0


def test_calculate_keyword_match_no_match():
    """Test keyword match when no match found."""
    repo = {
        "name": "project",
        "description": "Something else",
        "topics": []
    }
    score = calculate_keyword_match(repo, "rag")
    assert score == 0.0


def test_score_repo():
    """Test overall repo scoring."""
    now = datetime.now(timezone.utc)
    repo = {
        "name": "test-rag",
        "description": "RAG implementation",
        "stars": 5000,
        "forks": 500,
        "updated_at": now.isoformat(),
        "topics": ["rag"]
    }
    score = score_repo(repo, "rag")
    assert score > 0


def test_rank_repos():
    """Test repo ranking."""
    repos = [
        {"name": "repo1", "stars": 1000, "forks": 100, "updated_at": "2024-01-01T00:00:00Z", "description": "test", "topics": []},
        {"name": "repo2", "stars": 5000, "forks": 500, "updated_at": "2024-12-01T00:00:00Z", "description": "test", "topics": []},
        {"name": "repo3", "stars": 2000, "forks": 200, "updated_at": "2024-06-01T00:00:00Z", "description": "test", "topics": []}
    ]
    ranked = rank_repos(repos, "test")

    assert len(ranked) == 3
    assert all("score" in repo for repo in ranked)
    assert ranked[0]["stars"] >= ranked[1]["stars"] or ranked[0]["updated_at"] > ranked[1]["updated_at"]

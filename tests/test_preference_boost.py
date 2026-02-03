"""Tests for preference boost functionality."""
import pytest
from src.scorer import calculate_preference_boost, score_repo


def test_preference_boost_no_match():
    """Test preference boost when no topics match."""
    repo = {
        "name": "some-project",
        "description": "A random project",
        "topics": ["backend", "api"]
    }
    preferences = {
        "preferred_topics": ["frontend", "ui"],
        "topic_boost_multiplier": 1.5
    }

    boost = calculate_preference_boost(repo, preferences)
    assert boost == 1.0


def test_preference_boost_topic_match():
    """Test preference boost when repo topic matches."""
    repo = {
        "name": "project",
        "description": "A project",
        "topics": ["rag", "llm", "ai"]
    }
    preferences = {
        "preferred_topics": ["rag", "transformers"],
        "topic_boost_multiplier": 1.5
    }

    boost = calculate_preference_boost(repo, preferences)
    assert boost == 1.5


def test_preference_boost_name_match():
    """Test preference boost when preferred topic is in repo name."""
    repo = {
        "name": "awesome-rag-toolkit",
        "description": "Tools",
        "topics": []
    }
    preferences = {
        "preferred_topics": ["rag"],
        "topic_boost_multiplier": 2.0
    }

    boost = calculate_preference_boost(repo, preferences)
    assert boost == 2.0


def test_preference_boost_description_match():
    """Test preference boost when preferred topic is in description."""
    repo = {
        "name": "toolkit",
        "description": "A library for building LLM applications",
        "topics": []
    }
    preferences = {
        "preferred_topics": ["llm"],
        "topic_boost_multiplier": 1.5
    }

    boost = calculate_preference_boost(repo, preferences)
    assert boost == 1.5


def test_preference_boost_no_preferences():
    """Test preference boost with no preferences provided."""
    repo = {
        "name": "project",
        "description": "A project",
        "topics": ["rag"]
    }

    boost = calculate_preference_boost(repo, None)
    assert boost == 1.0


def test_score_repo_with_preferences():
    """Test that score_repo applies preference boost correctly."""
    repo = {
        "name": "rag-project",
        "description": "RAG implementation",
        "stars": 1000,
        "forks": 100,
        "updated_at": "2024-01-01T00:00:00Z",
        "topics": ["rag"]
    }
    preferences = {
        "preferred_topics": ["rag"],
        "topic_boost_multiplier": 2.0
    }

    score_without_pref = score_repo(repo, "rag")
    score_with_pref = score_repo(repo, "rag", preferences)

    # Score with preference should be higher
    assert score_with_pref > score_without_pref
    assert abs(score_with_pref - (score_without_pref * 2.0)) < 0.01

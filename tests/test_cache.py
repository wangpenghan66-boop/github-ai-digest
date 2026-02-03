"""Tests for cache functionality."""
import pytest
import json
from pathlib import Path
from datetime import datetime, timedelta
from src.cache import (
    load_cache,
    save_cache,
    filter_seen_repos,
    add_to_cache,
    cleanup_old_entries,
    CACHE_FILE
)


@pytest.fixture
def clean_cache():
    """Clean up cache file before and after tests."""
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
    yield
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()


def test_load_cache_empty(clean_cache):
    """Test loading cache when file doesn't exist."""
    cache = load_cache()
    assert cache == {}


def test_save_and_load_cache(clean_cache):
    """Test saving and loading cache."""
    test_cache = {
        "owner/repo1": "2024-01-01",
        "owner/repo2": "2024-01-02"
    }
    save_cache(test_cache)

    loaded = load_cache()
    assert loaded == test_cache


def test_filter_seen_repos(clean_cache):
    """Test filtering previously seen repos."""
    # Create cache with recent and old entries
    today = datetime.now().strftime("%Y-%m-%d")
    old_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

    cache = {
        "owner/repo1": today,
        "owner/repo2": old_date
    }
    save_cache(cache)

    repos = [
        {"full_name": "owner/repo1", "name": "repo1"},
        {"full_name": "owner/repo2", "name": "repo2"},
        {"full_name": "owner/repo3", "name": "repo3"}
    ]

    # Filter with 7 day window - repo1 should be filtered
    filtered, count = filter_seen_repos(repos, cache_days=7)
    assert count == 1
    assert len(filtered) == 2
    assert all(r["full_name"] != "owner/repo1" for r in filtered)


def test_add_to_cache(clean_cache):
    """Test adding repos to cache."""
    repos = [
        {"full_name": "owner/repo1", "name": "repo1"},
        {"full_name": "owner/repo2", "name": "repo2"}
    ]

    date = "2024-01-15"
    add_to_cache(repos, date=date)

    cache = load_cache()
    assert "owner/repo1" in cache
    assert "owner/repo2" in cache
    assert cache["owner/repo1"] == date


def test_cleanup_old_entries(clean_cache):
    """Test cleanup of old cache entries."""
    today = datetime.now().strftime("%Y-%m-%d")
    old_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    cache = {
        "owner/repo1": today,
        "owner/repo2": old_date
    }
    save_cache(cache)

    cleanup_old_entries(cache_days=7)

    cleaned = load_cache()
    assert "owner/repo1" in cleaned
    assert "owner/repo2" not in cleaned

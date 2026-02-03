"""Tests for configuration management."""
import pytest
import json
from pathlib import Path
from src.config import (
    get_default_config,
    load_config,
    save_config,
    CONFIG_FILE
)


@pytest.fixture
def clean_config():
    """Clean up config file before and after tests."""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
    yield
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()


def test_get_default_config():
    """Test getting default configuration."""
    config = get_default_config()

    assert "preferred_topics" in config
    assert "topic_boost_multiplier" in config
    assert "cache_days" in config
    assert isinstance(config["preferred_topics"], list)
    assert isinstance(config["topic_boost_multiplier"], (int, float))
    assert isinstance(config["cache_days"], int)


def test_load_config_creates_default(clean_config):
    """Test that loading config creates default if missing."""
    config = load_config()

    assert config == get_default_config()
    assert CONFIG_FILE.exists()


def test_save_and_load_config(clean_config):
    """Test saving and loading custom config."""
    custom_config = {
        "preferred_topics": ["nlp", "cv"],
        "topic_boost_multiplier": 2.0,
        "cache_days": 14
    }

    save_config(custom_config)
    loaded = load_config()

    assert loaded == custom_config


def test_load_config_merges_defaults(clean_config):
    """Test that loading config merges missing keys with defaults."""
    # Save partial config
    partial_config = {
        "preferred_topics": ["test"]
    }
    save_config(partial_config)

    # Load should merge with defaults
    loaded = load_config()

    assert loaded["preferred_topics"] == ["test"]
    assert "topic_boost_multiplier" in loaded
    assert "cache_days" in loaded

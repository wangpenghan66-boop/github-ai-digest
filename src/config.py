"""Configuration management for user preferences."""
import json
from pathlib import Path
from typing import Dict


CONFIG_FILE = Path("config.json")


def get_default_config() -> Dict:
    """
    Get default configuration.

    Returns:
        Default configuration dictionary
    """
    return {
        "preferred_topics": ["rag", "llm", "transformers"],
        "topic_boost_multiplier": 1.5,
        "cache_days": 7
    }


def load_config() -> Dict:
    """
    Load configuration from JSON file, falling back to defaults.

    Returns:
        Configuration dictionary
    """
    if not CONFIG_FILE.exists():
        config = get_default_config()
        save_config(config)
        return config

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

        # Merge with defaults for missing keys
        defaults = get_default_config()
        for key, value in defaults.items():
            if key not in config:
                config[key] = value

        return config
    except (json.JSONDecodeError, IOError):
        return get_default_config()


def save_config(config: Dict):
    """
    Save configuration to JSON file.

    Args:
        config: Configuration dictionary to save
    """
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

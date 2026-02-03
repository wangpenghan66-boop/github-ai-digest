"""Simple cache system to track previously reported repositories."""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List


CACHE_DIR = Path("cache")
CACHE_FILE = CACHE_DIR / "seen_repos.json"


def load_cache() -> Dict[str, str]:
    """
    Load cache from JSON file.

    Returns:
        Dictionary mapping repo full_name to last seen date (YYYY-MM-DD)
    """
    if not CACHE_FILE.exists():
        return {}

    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_cache(cache: Dict[str, str]):
    """
    Save cache to JSON file using atomic write.

    Args:
        cache: Dictionary mapping repo full_name to date
    """
    CACHE_DIR.mkdir(exist_ok=True)

    # Atomic write: write to temp file, then rename
    temp_file = CACHE_FILE.with_suffix('.tmp')
    with open(temp_file, 'w') as f:
        json.dump(cache, f, indent=2)

    temp_file.replace(CACHE_FILE)


def filter_seen_repos(repos: List[Dict], cache_days: int) -> tuple[List[Dict], int]:
    """
    Filter out repositories seen within the last N days.

    Args:
        repos: List of repository dictionaries
        cache_days: Number of days to check for duplicates

    Returns:
        Tuple of (filtered repos, count of filtered repos)
    """
    cache = load_cache()
    cutoff_date = datetime.now() - timedelta(days=cache_days)

    filtered = []
    filtered_count = 0

    for repo in repos:
        full_name = repo.get("full_name")
        if not full_name:
            continue

        last_seen = cache.get(full_name)
        if last_seen:
            try:
                seen_date = datetime.strptime(last_seen, "%Y-%m-%d")
                if seen_date >= cutoff_date:
                    filtered_count += 1
                    continue
            except ValueError:
                pass

        filtered.append(repo)

    return filtered, filtered_count


def add_to_cache(repos: List[Dict], date: str = None):
    """
    Add repositories to cache with current date.

    Args:
        repos: List of repository dictionaries to cache
        date: Date string (YYYY-MM-DD), defaults to today
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    cache = load_cache()

    for repo in repos:
        full_name = repo.get("full_name")
        if full_name:
            cache[full_name] = date

    save_cache(cache)


def cleanup_old_entries(cache_days: int):
    """
    Remove cache entries older than N days.

    Args:
        cache_days: Number of days to retain entries
    """
    cache = load_cache()
    cutoff_date = datetime.now() - timedelta(days=cache_days)

    cleaned_cache = {}
    for full_name, date_str in cache.items():
        try:
            seen_date = datetime.strptime(date_str, "%Y-%m-%d")
            if seen_date >= cutoff_date:
                cleaned_cache[full_name] = date_str
        except ValueError:
            continue

    if len(cleaned_cache) < len(cache):
        save_cache(cleaned_cache)

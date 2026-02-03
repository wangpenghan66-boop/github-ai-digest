"""Score repositories based on multiple metrics."""
from datetime import datetime, timezone
from typing import List, Dict, Optional


def calculate_recency_score(updated_at: str, max_days: int = 365) -> float:
    """
    Calculate recency score based on last update time.

    Args:
        updated_at: ISO format date string
        max_days: Maximum days to consider (older = 0 score)

    Returns:
        Recency score between 0 and 1
    """
    try:
        updated = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        days_old = (now - updated).days

        if days_old >= max_days:
            return 0.0

        return 1.0 - (days_old / max_days)
    except (ValueError, AttributeError):
        return 0.0


def calculate_keyword_match(repo: Dict, topic: str) -> float:
    """
    Calculate keyword match score.

    Args:
        repo: Repository dictionary
        topic: Search topic/keyword

    Returns:
        Keyword match score (0 or 1)
    """
    topic_lower = topic.lower()
    description = repo.get("description", "").lower()
    name = repo.get("name", "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]

    if topic_lower in name or topic_lower in description or topic_lower in topics:
        return 1.0

    return 0.0


def calculate_preference_boost(repo: Dict, preferences: Optional[Dict]) -> float:
    """
    Calculate preference boost for repositories matching preferred topics.

    Args:
        repo: Repository dictionary
        preferences: User preferences with preferred_topics and boost multiplier

    Returns:
        Boost multiplier (1.0 if no match, multiplier if match)
    """
    if not preferences:
        return 1.0

    preferred_topics = preferences.get("preferred_topics", [])
    boost_multiplier = preferences.get("topic_boost_multiplier", 1.5)

    if not preferred_topics:
        return 1.0

    # Check if any repo topic matches preferred topics
    repo_topics = [t.lower() for t in repo.get("topics", [])]
    repo_name = repo.get("name", "").lower()
    repo_desc = repo.get("description", "").lower()

    for pref_topic in preferred_topics:
        pref_lower = pref_topic.lower()
        if (pref_lower in repo_topics or
            pref_lower in repo_name or
            pref_lower in repo_desc):
            return boost_multiplier

    return 1.0


def score_repo(repo: Dict, topic: str, preferences: Optional[Dict] = None) -> float:
    """
    Calculate overall score for a repository.

    Formula:
        base_score = (stars * 0.4) + (forks * 0.3) + (recency * 0.2) + (keyword_match * 0.1)
        final_score = base_score * preference_boost

    Args:
        repo: Repository dictionary
        topic: Search topic for keyword matching
        preferences: Optional user preferences for boosting

    Returns:
        Overall score
    """
    stars = repo.get("stars", 0)
    forks = repo.get("forks", 0)
    updated_at = repo.get("updated_at", "")

    # Normalize stars and forks to a reasonable scale
    stars_score = min(stars / 10000, 1.0) * 10000
    forks_score = min(forks / 1000, 1.0) * 1000

    recency_score = calculate_recency_score(updated_at) * 1000
    keyword_score = calculate_keyword_match(repo, topic) * 1000

    base_score = (stars_score * 0.4) + (forks_score * 0.3) + (recency_score * 0.2) + (keyword_score * 0.1)

    # Apply preference boost
    boost = calculate_preference_boost(repo, preferences)
    final_score = base_score * boost

    return final_score


def rank_repos(repos: List[Dict], topic: str, preferences: Optional[Dict] = None) -> List[Dict]:
    """
    Score and rank repositories.

    Args:
        repos: List of repository dictionaries
        topic: Search topic for scoring
        preferences: Optional user preferences for boosting

    Returns:
        Sorted list of repos with scores
    """
    for repo in repos:
        repo["score"] = score_repo(repo, topic, preferences)

    return sorted(repos, key=lambda x: x["score"], reverse=True)

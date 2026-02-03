"""Fetch AI-related repositories from GitHub Search API."""
import requests
from datetime import datetime
from typing import List, Dict


def fetch_repos(topic: str = "ai", limit: int = 10) -> List[Dict]:
    """
    Fetch repositories from GitHub Search API based on topic.

    Args:
        topic: Search topic/keyword
        limit: Maximum number of repos to return

    Returns:
        List of repository dictionaries with metadata
    """
    # Construct search query
    query = f"{topic} stars:>50"

    # GitHub Search API endpoint
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": min(limit, 100)  # API max is 100
    }

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-AI-Digest-Pipeline"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        repos = []
        for item in data.get("items", [])[:limit]:
            repo = {
                "name": item["name"],
                "full_name": item["full_name"],
                "description": item["description"] or "No description provided",
                "url": item["html_url"],
                "stars": item["stargazers_count"],
                "forks": item["forks_count"],
                "language": item["language"] or "Unknown",
                "updated_at": item["updated_at"],
                "topics": item.get("topics", [])
            }
            repos.append(repo)

        return repos

    except requests.RequestException as e:
        print(f"Error fetching repos: {e}")
        return []


def parse_updated_date(date_str: str) -> datetime:
    """Parse ISO format date string to datetime object."""
    return datetime.fromisoformat(date_str.replace('Z', '+00:00'))

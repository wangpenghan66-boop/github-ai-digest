#!/usr/bin/env python
"""CLI for GitHub AI Digest Pipeline."""
import argparse
import sys
import os
from datetime import datetime


def check_environment():
    """Check if running in a virtual environment and provide helpful messages."""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

    if not in_venv:
        print("⚠️  Warning: Not running in a virtual environment")
        print("\nFor reliable execution, we recommend using a virtual environment:")
        print("  python -m venv .venv")
        print("  source .venv/bin/activate  # On Mac/Linux")
        print("  .venv\\Scripts\\activate     # On Windows")
        print("  pip install -r requirements.txt")
        print("\nContinuing anyway...\n")


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import requests
    except ImportError:
        print("❌ Error: Required package 'requests' not found")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        print("\nIf you haven't created a virtual environment yet:")
        print("  python -m venv .venv")
        print("  source .venv/bin/activate  # On Mac/Linux")
        print("  pip install -r requirements.txt")
        sys.exit(1)


def main():
    # Check environment and dependencies
    check_environment()
    check_dependencies()

    from src.github_fetcher import fetch_repos
    from src.scorer import rank_repos
    from src.report_generator import generate_report
    from src.cache import filter_seen_repos, add_to_cache, cleanup_old_entries
    from src.config import load_config
    parser = argparse.ArgumentParser(
        description="Generate AI digest from GitHub trending repositories"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="ai",
        help="Topic to search for (default: ai)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of repositories to include (default: 10)"
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Date for report filename (YYYY-MM-DD, default: today)"
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config()
    cache_days = config.get("cache_days", 7)

    print(f"Fetching {args.limit} repositories for topic: {args.topic}")
    if config.get("preferred_topics"):
        print(f"Preferred topics: {', '.join(config['preferred_topics'])}")

    # Fetch repos from GitHub
    repos = fetch_repos(topic=args.topic, limit=args.limit * 2)  # Fetch more to account for cache filtering

    if not repos:
        print("No repositories found or error occurred")
        return

    print(f"Found {len(repos)} repositories")

    # Filter out previously seen repos
    filtered_repos, filtered_count = filter_seen_repos(repos, cache_days)
    if filtered_count > 0:
        print(f"Filtered {filtered_count} previously seen repos (within {cache_days} days)")

    # Limit to requested amount after filtering
    filtered_repos = filtered_repos[:args.limit]

    if not filtered_repos:
        print("No new repositories to report after filtering")
        return

    # Score and rank repos with preferences
    ranked_repos = rank_repos(filtered_repos, topic=args.topic, preferences=config)

    # Add to cache before generating report
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    add_to_cache(ranked_repos, date=date_str)

    # Cleanup old cache entries
    cleanup_old_entries(cache_days)

    # Generate report
    report_path = generate_report(ranked_repos, topic=args.topic, date=date_str)

    print(f"Report generated: {report_path}")
    print(f"Included {len(ranked_repos)} repositories")


if __name__ == "__main__":
    main()

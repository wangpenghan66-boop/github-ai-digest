"""Generate markdown reports for GitHub repos."""
from datetime import datetime
from pathlib import Path
from typing import List, Dict


def generate_why_matters(repo: Dict) -> str:
    """Generate 'why it matters' text based on repo stats."""
    stars = repo.get("stars", 0)
    language = repo.get("language", "Unknown")

    if stars > 50000:
        popularity = "extremely popular"
    elif stars > 10000:
        popularity = "highly popular"
    elif stars > 1000:
        popularity = "popular"
    else:
        popularity = "emerging"

    return f"A {popularity} {language} project with {stars:,} stars, indicating strong community adoption and active development."


def generate_key_points(repo: Dict) -> List[str]:
    """Generate 3 key points about the repo."""
    points = []

    # Point 1: Description summary
    description = repo.get("description", "No description")
    points.append(description[:100] + "..." if len(description) > 100 else description)

    # Point 2: Stats
    stars = repo.get("stars", 0)
    forks = repo.get("forks", 0)
    points.append(f"Community: {stars:,} stars, {forks:,} forks")

    # Point 3: Activity
    language = repo.get("language", "Unknown")
    updated = repo.get("updated_at", "")
    if updated:
        try:
            date_obj = datetime.fromisoformat(updated.replace('Z', '+00:00'))
            date_str = date_obj.strftime("%B %Y")
            points.append(f"Built with {language}, last updated {date_str}")
        except ValueError:
            points.append(f"Built with {language}")
    else:
        points.append(f"Built with {language}")

    return points


def generate_practice_task(repo: Dict) -> str:
    """Generate a simple practice task."""
    stars = repo.get("stars", 0)

    if stars > 10000:
        return "Explore the documentation and try running a basic example from the README"
    elif stars > 1000:
        return "Clone the repository and examine the code structure to understand the architecture"
    else:
        return "Read through the README and consider how this could apply to your projects"


def generate_repo_card(repo: Dict) -> str:
    """Generate markdown card for a single repo."""
    name = repo.get("name", "Unknown")
    url = repo.get("url", "")
    stars = repo.get("stars", 0)
    forks = repo.get("forks", 0)
    language = repo.get("language", "Unknown")

    why_matters = generate_why_matters(repo)
    key_points = generate_key_points(repo)
    practice_task = generate_practice_task(repo)

    card = f"""## [{name}]({url})

**Why it matters:** {why_matters}

**Key Points:**
- {key_points[0]}
- {key_points[1]}
- {key_points[2]}

**Practice Task:** {practice_task}

**Links:** [GitHub]({url}) | Stars: {stars:,} | Forks: {forks:,} | Language: {language}

---

"""
    return card


def generate_report(repos: List[Dict], topic: str, date: str = None) -> str:
    """
    Generate full markdown report.

    Args:
        repos: List of repositories to include
        topic: Topic that was searched
        date: Date string (YYYY-MM-DD), defaults to today

    Returns:
        Path to generated report file
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Create daily directory if it doesn't exist
    daily_dir = Path("daily")
    daily_dir.mkdir(exist_ok=True)

    # Generate report content
    header = f"""# GitHub AI Digest - {date}

**Topic:** {topic}
**Repositories Analyzed:** {len(repos)}

---

"""

    cards = [generate_repo_card(repo) for repo in repos]
    content = header + "\n".join(cards)

    # Write to file
    report_path = daily_dir / f"{date}.md"
    report_path.write_text(content)

    return str(report_path)

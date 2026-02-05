# GitHub AI Digest Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/wangpenghan66-boop/github-ai-digest.svg)](https://github.com/wangpenghan66-boop/github-ai-digest/stargazers)

A minimal Python tool to fetch, score, and generate daily digests of trending AI-related repositories from GitHub.

## ✨ Features at a Glance

- 🔍 **Smart Search**: Fetch AI repositories using GitHub Search API
- ⭐ **Intelligent Scoring**: Rank repos based on stars, forks, recency, and keyword relevance
- 🔄 **Smart Caching**: Avoid showing duplicate repos across daily reports
- 🎯 **Personalized**: Boost repos matching your favorite topics
- 📝 **Clean Output**: Generate structured markdown reports with actionable insights
- ⚡ **Simple CLI**: Easy-to-use command-line interface

## Quick Start (Local)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Mac/Linux
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run your first digest
python run.py --topic "rag" --limit 5
```

Your report will be generated in `daily/YYYY-MM-DD.md`

## Features

- Fetch AI-related repositories using GitHub Search API
- Score repos based on stars, forks, recency, and keyword relevance
- **Smart caching** to avoid repeating repos across daily reports
- **User preferences** to boost repos matching your favorite topics
- Generate markdown reports with structured cards for each repository
- Simple CLI interface for customization

## Setup

1. Install Python 3 (requires Python 3.8+)

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Customize your preferences in `config.json`:
```json
{
  "preferred_topics": ["rag", "llm", "transformers"],
  "topic_boost_multiplier": 1.5,
  "cache_days": 7
}
```

**Config options:**
- `preferred_topics`: List of topics you care about (repos matching these get boosted)
- `topic_boost_multiplier`: How much to boost preferred repos (1.5 = 50% higher score)
- `cache_days`: How many days to avoid repeating repos (default: 7)

## Usage

### Basic Usage

Generate a digest for AI repositories:
```bash
python run.py
```

### Custom Topic

Search for specific topics:
```bash
python run.py --topic "rag"
python run.py --topic "llm"
python run.py --topic "machine-learning"
```

### Limit Results

Control the number of repositories:
```bash
python run.py --topic "rag" --limit 5
```

### Custom Date

Specify a date for the report filename:
```bash
python run.py --topic "ai" --limit 10 --date "2024-02-03"
```

## Output

Reports are saved to `daily/YYYY-MM-DD.md` with the following format for each repository:

- **Title & Link**: Repository name with GitHub URL
- **Why it matters**: Context about popularity and adoption
- **Key Points**: 3 bullet points covering description, stats, and technology
- **Practice Task**: A simple actionable task to engage with the project
- **Links**: Direct links and metadata (stars, forks, language)

## Testing

Run the test suite:
```bash
pytest tests/
```

Run tests with verbose output:
```bash
pytest tests/ -v
```

## Project Structure

```
ai_learning/
├── run.py                    # CLI entry point
├── verify_setup.py           # Setup verification script
├── config.json               # User preferences
├── .gitignore                # Git ignore rules
├── src/
│   ├── github_fetcher.py     # Fetch repos from GitHub API
│   ├── scorer.py             # Score repos based on metrics
│   ├── cache.py              # Cache management
│   ├── config.py             # Config loading
│   └── report_generator.py   # Generate markdown reports
├── tests/
│   ├── test_scorer.py        # Test scoring logic
│   ├── test_fetcher.py       # Test parsing logic
│   ├── test_cache.py         # Test cache functionality
│   ├── test_config.py        # Test config management
│   └── test_preference_boost.py  # Test preference boosting
├── cache/                    # Cache directory (auto-created)
│   └── seen_repos.json       # Tracked repositories
├── daily/                    # Output directory for reports
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Scoring Algorithm

Repositories are scored using:
- **Stars (40%)**: Normalized star count
- **Forks (30%)**: Normalized fork count
- **Recency (20%)**: Based on last update (within 365 days)
- **Keyword Match (10%)**: Topic/description relevance
- **Preference Boost**: Multiplier applied to repos matching your preferred topics

Formula: `final_score = base_score × preference_boost`

## Smart Features

### Cache System
- Automatically tracks repos you've seen in previous reports
- Avoids showing the same repos within N days (configurable)
- Cache stored in `cache/seen_repos.json`
- Old entries auto-cleaned on each run

**Learning value:** File-based persistence, deduplication strategies, time-based expiration

### User Preferences
- Boost scoring for repos matching your favorite topics
- Customizable multiplier (default: 1.5x)
- Topics matched against repo name, description, and GitHub topics

**Learning value:** Configuration management, algorithm customization, personalization patterns

## Limitations

- Uses public GitHub API (no authentication required)
- Rate limit: ~10 requests per minute
- Maximum 100 repos per search

## 📊 Example Output

Run the tool:
```bash
python run.py --topic "transformer" --limit 5
```

Console output:
```
Fetching 5 repositories for topic: transformer
Preferred topics: rag, llm, transformers
Found 10 repositories
Filtered 3 previously seen repos (within 7 days)
Report generated: daily/2024-02-03.md
Included 5 repositories
```

Generated report (`daily/2024-02-03.md`):

```markdown
# GitHub AI Digest - 2024-02-03

## [langflow](https://github.com/langflow-ai/langflow)

**Why it matters:** A extremely popular Python project with 144,522 stars,
indicating strong community adoption and active development.

**Key Points:**
- Langflow is a powerful tool for building and deploying AI-powered agents and workflows.
- Community: 144,522 stars, 8,400 forks
- Built with Python, last updated February 2026

**Practice Task:** Explore the documentation and try running a basic example from the README

**Links:** [GitHub](https://github.com/langflow-ai/langflow) | Stars: 144,522 | Forks: 8,400 | Language: Python
```

## Local Verification Checklist

To verify everything works correctly on your machine:

1. **Fresh venv**: `python -m venv .venv`
2. **Activate**: `source .venv/bin/activate` (Mac/Linux) or `.venv\Scripts\activate` (Windows)
3. **Install deps**: `pip install -r requirements.txt`
4. **Verify setup**: `python verify_setup.py` (optional but recommended)
5. **Run CLI**: `python run.py --topic "ai" --limit 3`
6. **Check output**: Verify `daily/YYYY-MM-DD.md` was created
7. **Run tests**: `pytest tests/ -v` (all 24 tests should pass)

## Git Hygiene

The `.gitignore` file excludes:
- **`.venv/`** - Virtual environment (too large, machine-specific)
- **`cache/`** - Session state (temporary, regenerated on each run)
- **`daily/*.md`** - Generated outputs (reports are disposable, not source code)

Why ignore outputs? Daily reports are generated artifacts, not source material. Each user generates their own reports based on their preferences and timing.

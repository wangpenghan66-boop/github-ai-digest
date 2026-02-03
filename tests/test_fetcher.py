"""Tests for GitHub fetcher."""
import pytest
from src.github_fetcher import parse_updated_date
from datetime import datetime


def test_parse_updated_date():
    """Test parsing ISO format date."""
    date_str = "2024-01-15T10:30:00Z"
    result = parse_updated_date(date_str)
    assert isinstance(result, datetime)
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15


def test_parse_updated_date_with_timezone():
    """Test parsing date with timezone."""
    date_str = "2024-06-20T14:45:30+00:00"
    result = parse_updated_date(date_str)
    assert isinstance(result, datetime)
    assert result.year == 2024

#!/usr/bin/env python
"""Quick verification script to check if setup is correct."""
import sys
import os


def main():
    print("🔍 Verifying GitHub AI Digest Pipeline setup...\n")

    # Check Python version
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  Warning: Python 3.8+ recommended")

    # Check virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print("✓ Running in virtual environment")
    else:
        print("✗ Not in virtual environment (recommended)")

    # Check dependencies
    missing = []
    try:
        import requests
        print("✓ requests installed")
    except ImportError:
        missing.append("requests")

    try:
        import pytest
        print("✓ pytest installed")
    except ImportError:
        missing.append("pytest")

    if missing:
        print(f"\n✗ Missing dependencies: {', '.join(missing)}")
        print("  Run: pip install -r requirements.txt")
        return False

    # Check directory structure
    dirs = ['src', 'tests', 'daily']
    for d in dirs:
        if os.path.isdir(d):
            print(f"✓ {d}/ directory exists")
        else:
            print(f"✗ {d}/ directory missing")
            return False

    # Check key files
    files = ['run.py', 'requirements.txt', 'README.md', 'config.json']
    for f in files:
        if os.path.isfile(f):
            print(f"✓ {f} exists")
        else:
            if f == 'config.json':
                print(f"  ℹ {f} missing (will be auto-created on first run)")
            else:
                print(f"✗ {f} missing")
                return False

    print("\n✅ Setup verification complete!")
    print("\nNext steps:")
    print("  python run.py --topic 'ai' --limit 3")
    print("  pytest tests/ -v")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# Contributing to GitHub AI Digest

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker
- Describe the issue clearly with steps to reproduce
- Include your Python version and OS

### Submitting Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/github-ai-digest.git
cd github-ai-digest

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

### Coding Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Keep functions focused and modular
- Add docstrings for public functions

### Testing

All tests must pass before merging:

```bash
pytest tests/ -v --cov=src
```

## Questions?

Feel free to open an issue for any questions!

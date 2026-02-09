# Contributing to GPT Security Hardening Framework

Thank you for your interest in contributing! This project aims to help developers secure their custom GPTs.

## How to Contribute

### Reporting Issues
- Use the [GitHub Issues](../../issues) tab to report bugs, suggest features, or flag gaps in the security templates.
- Include as much detail as possible: what you expected, what happened, and steps to reproduce.

### Suggesting Template Improvements
- Security threats evolve — if you've discovered a new attack vector or bypass technique, open an issue or submit a PR with updated test cases and mitigations.
- When adding new checklist items or test categories, include a severity level (Low/Medium/High/Critical).

### Submitting Pull Requests
1. Fork the repository and create a feature branch.
2. Make your changes.
3. If modifying `run_redteam_py3.py`, add or update unit tests in `tests/test_runner.py`.
4. Run tests: `python -m pytest tests/`
5. Submit a PR with a clear description of your changes.

### Code Style
- Python code should be compatible with Python 3.8+.
- Follow PEP 8 conventions.
- Use type hints where practical.
- Keep the runner script self-contained (minimal dependencies).

### Security Considerations
- Do not commit API keys, secrets, or PII in test data.
- Results CSVs may contain sensitive API responses — they are gitignored by default.
- Red-team prompts should use example/fictional content, not real attack payloads.

## Code of Conduct

Be respectful, constructive, and collaborative. This is a security-focused project — responsible disclosure and ethical testing practices are expected.

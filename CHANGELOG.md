# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-10-01

### Added
- **Multi-modal security** section in template and checklist (image injection, file uploads).
- **Tool/function calling security** section in template and checklist (SSRF, data exfiltration).
- **Encoding/obfuscation bypass** coverage in template, checklist, and testing guide.
- **Multi-turn manipulation** defense guidance.
- Complete test cases for all 11 testing categories in the Red-Team Testing Guide.
- Expanded `redteam_prompts.csv` from 1 to 26 test cases across all categories.
- `run_redteam_py3.py` improvements:
  - API key via `OPENAI_API_KEY` environment variable (security).
  - Fixed false-positive `"i can"` refusal pattern — now uses regex with word boundaries.
  - Added `--dry-run` flag for CSV validation without API calls.
  - Added `--verbose` flag for debug logging.
  - Added `--temperature` and `--max-tokens` CLI flags.
  - Run summary with pass/fail/error counts.
  - Meaningful exit codes (0=pass, 1=failures, 2=error).
  - Input validation — skips empty prompts with warning.
  - Progress indicator `[N/Total]` during test runs.
  - Fixed deprecated `datetime.utcnow()` to use `datetime.now(timezone.utc)`.
- Unit tests in `tests/test_runner.py`.
- GitHub Actions CI workflow (lint + test).
- `.gitignore` file.
- `requirements.txt` file.
- `pyproject.toml` for project metadata.
- `CONTRIBUTING.md` guide.
- GitHub issue and PR templates.
- This changelog.

### Fixed
- README referenced non-existent `GPT_Security_GitHub_Template.md` — removed.
- README referenced `GPT_Security_Template.pdf` — corrected to `.md`.
- README now links to all red-team tooling.
- Red-Team Testing Guide referenced deleted `check_results.py` — updated runbook.
- REPRO_README referenced non-existent `requirements.txt` — file now exists.
- Version and date stamps added to all templates.

### Changed
- Security template expanded from 7 to 9 sections.
- Security checklist expanded from 13 to 24 items.
- Red-Team Testing Guide expanded from 8 to 11 testing categories with full test cases.

## [1.0.0] - 2025-09-24

### Added
- Initial release with GPT Security Template, Checklist, and Red-Team Testing Guide.
- `run_redteam_py3.py` red-team runner script.
- Example prompts CSV and results CSV.
- Saucy Sommelier example system prompt.

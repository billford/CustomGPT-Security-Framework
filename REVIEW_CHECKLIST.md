# Repository Review Checklist

Comprehensive improvement checklist for the CustomGPT-Security-Framework repository.
Items are organized by category with priority levels: **Critical**, **High**, **Medium**, **Low**.

---

## 1. Repository & Project Structure

- [ ] **Add `.gitignore` file** (Critical)
  No `.gitignore` exists. Risk of committing `.venv/`, `__pycache__/`, `.env` files, or results CSVs containing sensitive API responses. Should ignore at minimum: `.venv/`, `*.pyc`, `__pycache__/`, `.env`, `results*.csv`, `*.egg-info/`, `dist/`, `build/`.

- [ ] **Add `requirements.txt`** (Critical)
  `REPRO_README.md` references `pip install -r requirements.txt` but the file does not exist. At minimum it should list `requests`.

- [ ] **Organize into directories** (Medium)
  All files are flat in the root directory. Consider a structure like:
  ```
  docs/           → GPT_Security_Template.md, GPT_Security_Checklist.md, GPT_RedTeam_Testing_Guide.md
  tools/          → run_redteam_py3.py
  examples/       → redteam_prompts.csv, example-results.csv, saucy_sommelier.txt
  ```

- [ ] **Add `pyproject.toml` or `setup.py`** (Low)
  No packaging metadata exists. A `pyproject.toml` would formalize Python version requirements, dependencies, and make the tool installable via `pip install -e .`.

- [ ] **Standardize file naming** (Low)
  Inconsistent naming conventions: `run_redteam_py3.py` (underscores + suffix), `redteam_prompts.csv` (underscores), `saucy_sommelier.txt` (underscores), `REPRO_README.md` (caps). Consider a consistent scheme.

---

## 2. README.md — Broken References & Missing Content

- [ ] **Fix reference to non-existent file `GPT_Security_GitHub_Template.md`** (Critical)
  The README Contents section and step 3 both reference `GPT_Security_GitHub_Template.md` — this file does not exist in the repository.

- [ ] **Fix reference to `GPT_Security_Template.pdf`** (High)
  Step 1 says "Start with the Policy (`GPT_Security_Template.pdf`)" but the file is `.md`, not `.pdf`.

- [ ] **Add links to red-team tooling** (High)
  The README doesn't mention `run_redteam_py3.py`, `REPRO_README.md`, or any of the red-team automation tooling at all. These are a major feature of the repo.

- [ ] **Add a "Prerequisites" or "Requirements" section** (Medium)
  No mention of Python version requirements or dependencies needed to run the red-team tool.

- [ ] **Add license badge and project badges** (Low)
  No visual indicators of license, build status, or Python version in the README header.

---

## 3. GPT_Security_Template.md — Coverage Gaps

- [ ] **Add multi-modal attack guidance** (High)
  No mention of image-based prompt injection, vision-model attacks, or file upload risks. Modern GPTs support images/files which open new attack surfaces.

- [ ] **Add tool/function calling security section** (High)
  No guidance on securing GPTs that use Actions, function calling, or plugins. These can be exploited to exfiltrate data or perform unauthorized operations.

- [ ] **Add encoding/obfuscation attack guidance** (Medium)
  No mention of base64-encoded instructions, ROT13, leetspeak, Unicode homoglyphs, or other encoding-based bypass techniques.

- [ ] **Add multi-turn conversation attack guidance** (Medium)
  No guidance on progressive jailbreaks across multiple turns, context manipulation, or conversation history poisoning.

- [ ] **Add version number and revision date** (Medium)
  No versioning or date stamp on the template, making it hard to track which version is deployed.

- [ ] **Add rate limiting / token limit guidance** (Low)
  No mention of protecting against token exhaustion or excessive request patterns.

---

## 4. GPT_Security_Checklist.md — Missing Items

- [ ] **Add checklist items for multi-modal attacks** (High)
  No items covering image-based injection, file upload validation, or vision-model security.

- [ ] **Add checklist items for tool/function calling security** (High)
  No items for validating Actions, external API calls, or function calling behavior.

- [ ] **Add checklist items for encoding-based attacks** (Medium)
  No items covering base64, ROT13, Unicode, or other obfuscation bypass techniques.

- [ ] **Add checklist items for multi-turn manipulation** (Medium)
  No items for progressive jailbreaks or conversation context attacks.

- [ ] **Add "Owner" or "Responsible" column** (Low)
  For team use, an owner field would help assign accountability for each checklist item.

- [ ] **Add version/date tracking to checklist** (Low)
  No way to track when the checklist was last reviewed or what version it is.

---

## 5. GPT_RedTeam_Testing_Guide.md — Incomplete Content & Stale References

- [ ] **Complete missing test case sections** (Critical)
  Categories 4–8 (Hallucination, Harmful Content, Resource Abuse, Social Engineering, Edge-Case) are truncated with a placeholder: `… *(continue with Hallucination, Harmful Content, Resource Abuse, Social Engineering, Edge-Case examples as we drafted earlier)* …`. These need actual test cases.

- [ ] **Fix stale reference to `check_results.py`** (Critical)
  Runbook step 4 says "Score using `check_results.py`" but this file was deleted from the repo. The reference should be removed or replaced with updated instructions.

- [ ] **Add multi-modal attack test cases** (High)
  No testing category or prompts for image-based or file-based attacks.

- [ ] **Add encoding/obfuscation test cases** (High)
  No test cases for base64-encoded prompts, ROT13 obfuscation, Unicode tricks, or other encoding bypasses.

- [ ] **Add tool/function calling abuse test cases** (Medium)
  No test cases for exploiting Actions, function calling, or plugin behavior.

- [ ] **Expand `redteam_prompts.csv` with more test cases** (High)
  The CSV contains only 1 test case. For practical use, it should include at least one prompt per testing category (8 minimum), ideally 3–5 per category.

---

## 6. REPRO_README.md — Accuracy Issues

- [ ] **Fix reference to non-existent `requirements.txt`** (Critical)
  The Files section and Quick Setup both reference `requirements.txt` which does not exist.

- [ ] **Add Python version requirement** (Medium)
  No minimum Python version is specified. The script uses f-strings and dataclasses, requiring Python 3.7+.

- [ ] **Add Docker/container instructions** (Low)
  Troubleshooting mentions Docker as recommended for CI, but no Dockerfile or container instructions are provided.

---

## 7. run_redteam_py3.py — Code Issues

### Security

- [ ] **Support API key via environment variable** (Critical)
  The `--api-key` flag passes the key as a CLI argument, which is visible in process listings (`ps aux`), shell history (`~/.bash_history`), and CI logs. Should support `$OPENAI_API_KEY` or similar environment variable as the default, with `--api-key` as an override.

- [ ] **Add input validation on CSV data** (High)
  No validation that the `prompt` field is non-empty. Empty prompts would send wasteful or confusing API requests.

### Correctness — Refusal Detection

- [ ] **Fix overly broad `"i can"` refusal pattern** (Critical)
  `REFUSAL_PATTERNS` includes `"i can"` which matches any response containing those two characters in sequence — including legitimate responses like "I can help you with that" or "I can recommend...". This causes false PASSes on responses that are actually compliant (non-refusals). This is the first pattern in the list, so it short-circuits all other checks. It should be removed or changed to a pattern that only matches refusals (e.g., `"i can't"` and `"i cannot"` are already in the list).

- [ ] **Use word-boundary matching for refusal patterns** (High)
  Simple substring matching (`pattern in lower_text`) can cause false positives. For example, `"i won't"` would match inside `"I won't deny that wine is amazing"`. Consider using regex with word boundaries or more contextual matching.

### Deprecation

- [ ] **Replace `datetime.utcnow()` with `datetime.now(timezone.utc)`** (Medium)
  `datetime.utcnow()` is deprecated since Python 3.12. Line 139 should use `datetime.now(timezone.utc)` instead.

### Functional Gaps

- [ ] **Add summary statistics at end of run** (High)
  No pass/fail/error counts are printed after the run completes. Users must manually inspect the CSV to know how the test went.

- [ ] **Set exit code based on test results** (High)
  `main()` always returns 0 on success, even if every test FAILed. A non-zero exit code for failures would enable CI/CD integration (e.g., fail the pipeline if critical tests fail).

- [ ] **Add `--env-file` or dotenv support** (Medium)
  No support for `.env` files for configuration, which is a common pattern for tools that need API keys.

- [ ] **Add `--dry-run` flag** (Medium)
  No way to validate the CSV format and configuration without actually making API calls.

- [ ] **Add progress indicator** (Medium)
  No progress feedback during long test runs. Users see only log lines. A counter like `[3/50]` would improve usability.

- [ ] **Make `temperature` and `max_tokens` configurable** (Medium)
  `build_payload()` hardcodes `temperature: 0.0` and `max_tokens: 800` with no CLI override. These affect test reproducibility and response length.

- [ ] **Validate API URL reachability before running** (Low)
  No pre-flight check. If the URL is wrong, the user discovers it only after the first test fails.

- [ ] **Support resuming partial runs** (Low)
  If a run is interrupted, there's no way to resume from where it left off. The output CSV is overwritten on each run (`write_csv_header` truncates the file).

### Code Quality

- [ ] **Improve CSV write efficiency** (Low)
  `append_result_to_csv()` opens and closes the file for every row. For large test suites, keeping the file handle open would be more efficient.

- [ ] **Add `--verbose` / `--quiet` flags** (Low)
  No way to control log verbosity. Defaulting to `INFO` may be too noisy or too quiet depending on context.

---

## 8. Testing & CI/CD

- [ ] **Add unit tests** (High)
  No test files exist at all. Key functions that should be tested:
  - `looks_like_refusal()` — especially the false-positive-prone patterns
  - `read_prompts()` — CSV parsing with missing/malformed fields
  - `build_payload()` — both standard and custom endpoint modes
  - `extract_assistant_text()` — various JSON response shapes

- [ ] **Add GitHub Actions CI workflow** (Medium)
  No CI/CD pipeline. A basic workflow could run linting (`pylint`/`flake8`), type checking (`mypy`), and unit tests on push/PR.

- [ ] **Add pre-commit hooks configuration** (Low)
  No `.pre-commit-config.yaml`. Could enforce linting, formatting, and secret scanning before commits.

---

## 9. Documentation & Community

- [ ] **Add CONTRIBUTING.md** (Medium)
  No contribution guidelines for potential contributors.

- [ ] **Add CHANGELOG.md** (Medium)
  No changelog tracking changes across versions.

- [ ] **Add GitHub issue templates** (Low)
  No `.github/ISSUE_TEMPLATE/` for bug reports or feature requests.

- [ ] **Add GitHub PR template** (Low)
  No `.github/PULL_REQUEST_TEMPLATE.md` for standardizing pull request descriptions.

---

## Summary by Priority

| Priority | Count |
|----------|-------|
| Critical | 8     |
| High     | 16    |
| Medium   | 15    |
| Low      | 11    |
| **Total**| **50**|

### Top 10 Highest-Impact Items

1. Fix `"i can"` refusal pattern false positives in `run_redteam_py3.py`
2. Add `.gitignore` to prevent accidental secret/artifact commits
3. Add missing `requirements.txt`
4. Fix broken `GPT_Security_GitHub_Template.md` reference in README
5. Complete the 5 missing test case sections in the Red-Team Testing Guide
6. Fix stale `check_results.py` reference in the Red-Team Testing Guide runbook
7. Support API key via environment variable (security)
8. Fix `.pdf` → `.md` reference in README
9. Expand `redteam_prompts.csv` beyond the single test case
10. Add summary statistics and meaningful exit codes to the runner

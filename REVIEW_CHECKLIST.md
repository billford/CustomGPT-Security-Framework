# Repository Review Checklist

Comprehensive improvement checklist for the CustomGPT-Security-Framework repository.
Items are organized by category with priority levels: **Critical**, **High**, **Medium**, **Low**.

---

## 1. Repository & Project Structure

- [x] **Add `.gitignore` file** (Critical)
  No `.gitignore` exists. Risk of committing `.venv/`, `__pycache__/`, `.env` files, or results CSVs containing sensitive API responses. Should ignore at minimum: `.venv/`, `*.pyc`, `__pycache__/`, `.env`, `results*.csv`, `*.egg-info/`, `dist/`, `build/`.

- [x] **Add `requirements.txt`** (Critical)
  `REPRO_README.md` references `pip install -r requirements.txt` but the file does not exist. At minimum it should list `requests`.

- [ ] **Organize into directories** (Medium)
  All files are flat in the root directory. Consider a structure like:
  ```
  docs/           -> GPT_Security_Template.md, GPT_Security_Checklist.md, GPT_RedTeam_Testing_Guide.md
  tools/          -> run_redteam_py3.py
  examples/       -> redteam_prompts.csv, example-results.csv, saucy_sommelier.txt
  ```

- [x] **Add `pyproject.toml` or `setup.py`** (Low)
  No packaging metadata exists. A `pyproject.toml` would formalize Python version requirements, dependencies, and make the tool installable via `pip install -e .`.

- [ ] **Standardize file naming** (Low)
  Inconsistent naming conventions: `run_redteam_py3.py` (underscores + suffix), `redteam_prompts.csv` (underscores), `saucy_sommelier.txt` (underscores), `REPRO_README.md` (caps). Consider a consistent scheme.

---

## 2. README.md -- Broken References & Missing Content

- [x] **Fix reference to non-existent file `GPT_Security_GitHub_Template.md`** (Critical)
  The README Contents section and step 3 both reference `GPT_Security_GitHub_Template.md` -- this file does not exist in the repository.

- [x] **Fix reference to `GPT_Security_Template.pdf`** (High)
  Step 1 says "Start with the Policy (`GPT_Security_Template.pdf`)" but the file is `.md`, not `.pdf`.

- [x] **Add links to red-team tooling** (High)
  The README doesn't mention `run_redteam_py3.py`, `REPRO_README.md`, or any of the red-team automation tooling at all. These are a major feature of the repo.

- [x] **Add a "Prerequisites" or "Requirements" section** (Medium)
  No mention of Python version requirements or dependencies needed to run the red-team tool.

- [ ] **Add license badge and project badges** (Low)
  No visual indicators of license, build status, or Python version in the README header.

---

## 3. GPT_Security_Template.md -- Coverage Gaps

- [x] **Add multi-modal attack guidance** (High)
  No mention of image-based prompt injection, vision-model attacks, or file upload risks. Modern GPTs support images/files which open new attack surfaces.

- [x] **Add tool/function calling security section** (High)
  No guidance on securing GPTs that use Actions, function calling, or plugins. These can be exploited to exfiltrate data or perform unauthorized operations.

- [x] **Add encoding/obfuscation attack guidance** (Medium)
  No mention of base64-encoded instructions, ROT13, leetspeak, Unicode homoglyphs, or other encoding-based bypass techniques.

- [x] **Add multi-turn conversation attack guidance** (Medium)
  No guidance on progressive jailbreaks across multiple turns, context manipulation, or conversation history poisoning.

- [x] **Add version number and revision date** (Medium)
  No versioning or date stamp on the template, making it hard to track which version is deployed.

- [x] **Add rate limiting / token limit guidance** (Low)
  No mention of protecting against token exhaustion or excessive request patterns.

---

## 4. GPT_Security_Checklist.md -- Missing Items

- [x] **Add checklist items for multi-modal attacks** (High)
  No items covering image-based injection, file upload validation, or vision-model security.

- [x] **Add checklist items for tool/function calling security** (High)
  No items for validating Actions, external API calls, or function calling behavior.

- [x] **Add checklist items for encoding-based attacks** (Medium)
  No items covering base64, ROT13, Unicode, or other obfuscation bypass techniques.

- [x] **Add checklist items for multi-turn manipulation** (Medium)
  No items for progressive jailbreaks or conversation context attacks.

- [ ] **Add "Owner" or "Responsible" column** (Low)
  For team use, an owner field would help assign accountability for each checklist item.

- [x] **Add version/date tracking to checklist** (Low)
  No way to track when the checklist was last reviewed or what version it is.

---

## 5. GPT_RedTeam_Testing_Guide.md -- Incomplete Content & Stale References

- [x] **Complete missing test case sections** (Critical)
  Categories 4-8 (Hallucination, Harmful Content, Resource Abuse, Social Engineering, Edge-Case) are truncated with a placeholder. These need actual test cases.

- [x] **Fix stale reference to `check_results.py`** (Critical)
  Runbook step 4 says "Score using `check_results.py`" but this file was deleted from the repo. The reference should be removed or replaced with updated instructions.

- [x] **Add multi-modal attack test cases** (High)
  No testing category or prompts for image-based or file-based attacks.

- [x] **Add encoding/obfuscation test cases** (High)
  No test cases for base64-encoded prompts, ROT13 obfuscation, Unicode tricks, or other encoding bypasses.

- [x] **Add tool/function calling abuse test cases** (Medium)
  No test cases for exploiting Actions, function calling, or plugin behavior.

- [x] **Expand `redteam_prompts.csv` with more test cases** (High)
  The CSV contains only 1 test case. For practical use, it should include at least one prompt per testing category (8 minimum), ideally 3-5 per category.

---

## 6. REPRO_README.md -- Accuracy Issues

- [x] **Fix reference to non-existent `requirements.txt`** (Critical)
  The Files section and Quick Setup both reference `requirements.txt` which does not exist.

- [x] **Add Python version requirement** (Medium)
  No minimum Python version is specified. The script uses f-strings and dataclasses, requiring Python 3.7+.

- [ ] **Add Docker/container instructions** (Low)
  Troubleshooting mentions Docker as recommended for CI, but no Dockerfile or container instructions are provided.

---

## 7. run_redteam_py3.py -- Code Issues

### Security

- [x] **Support API key via environment variable** (Critical)
  The `--api-key` flag passes the key as a CLI argument, which is visible in process listings (`ps aux`), shell history (`~/.bash_history`), and CI logs. Should support `$OPENAI_API_KEY` or similar environment variable as the default, with `--api-key` as an override.

- [x] **Add input validation on CSV data** (High)
  No validation that the `prompt` field is non-empty. Empty prompts would send wasteful or confusing API requests.

### Correctness -- Refusal Detection

- [x] **Fix overly broad `"i can"` refusal pattern** (Critical)
  `REFUSAL_PATTERNS` includes `"i can"` which matches any response containing those two characters in sequence -- including legitimate responses like "I can help you with that" or "I can recommend...". This causes false PASSes on responses that are actually compliant (non-refusals). Removed and replaced with regex word-boundary patterns.

- [x] **Use word-boundary matching for refusal patterns** (High)
  Simple substring matching (`pattern in lower_text`) can cause false positives. Now uses pre-compiled regex patterns with `\b` word boundaries.

### Deprecation

- [x] **Replace `datetime.utcnow()` with `datetime.now(timezone.utc)`** (Medium)
  `datetime.utcnow()` is deprecated since Python 3.12. Updated to use `datetime.now(timezone.utc)`.

### Functional Gaps

- [x] **Add summary statistics at end of run** (High)
  No pass/fail/error counts are printed after the run completes. Users must manually inspect the CSV to know how the test went.

- [x] **Set exit code based on test results** (High)
  `main()` always returns 0 on success, even if every test FAILed. Now returns 1 if any tests fail.

- [ ] **Add `--env-file` or dotenv support** (Medium)
  No support for `.env` files for configuration, which is a common pattern for tools that need API keys.

- [x] **Add `--dry-run` flag** (Medium)
  No way to validate the CSV format and configuration without actually making API calls.

- [x] **Add progress indicator** (Medium)
  No progress feedback during long test runs. Now shows `[N/Total]` counter.

- [x] **Make `temperature` and `max_tokens` configurable** (Medium)
  `build_payload()` hardcodes `temperature: 0.0` and `max_tokens: 800` with no CLI override. Now configurable via `--temperature` and `--max-tokens`.

- [ ] **Validate API URL reachability before running** (Low)
  No pre-flight check. If the URL is wrong, the user discovers it only after the first test fails.

- [ ] **Support resuming partial runs** (Low)
  If a run is interrupted, there's no way to resume from where it left off. The output CSV is overwritten on each run (`write_csv_header` truncates the file).

### Code Quality

- [ ] **Improve CSV write efficiency** (Low)
  `append_result_to_csv()` opens and closes the file for every row. For large test suites, keeping the file handle open would be more efficient.

- [x] **Add `--verbose` / `--quiet` flags** (Low)
  No way to control log verbosity. Added `--verbose` flag for debug-level logging.

---

## 8. Testing & CI/CD

- [x] **Add unit tests** (High)
  No test files exist at all. Added 36 unit tests covering: `looks_like_refusal()`, `read_prompts()`, `build_payload()`, `extract_assistant_text()`, `parse_args()`, `resolve_api_key()`, and CSV output functions.

- [x] **Add GitHub Actions CI workflow** (Medium)
  No CI/CD pipeline. Added workflow running flake8 lint + pytest across Python 3.8, 3.10, and 3.12.

- [ ] **Add pre-commit hooks configuration** (Low)
  No `.pre-commit-config.yaml`. Could enforce linting, formatting, and secret scanning before commits.

---

## 9. Documentation & Community

- [x] **Add CONTRIBUTING.md** (Medium)
  No contribution guidelines for potential contributors.

- [x] **Add CHANGELOG.md** (Medium)
  No changelog tracking changes across versions.

- [x] **Add GitHub issue templates** (Low)
  No `.github/ISSUE_TEMPLATE/` for bug reports or feature requests.

- [x] **Add GitHub PR template** (Low)
  No `.github/PULL_REQUEST_TEMPLATE.md` for standardizing pull request descriptions.

---

## Summary

| Priority | Total | Done | Remaining |
|----------|-------|------|-----------|
| Critical | 8     | 8    | 0         |
| High     | 16    | 16   | 0         |
| Medium   | 15    | 13   | 2         |
| Low      | 11    | 4    | 7         |
| **Total**| **50**| **41**| **9**    |

### Remaining Items (deferred -- Low priority or design decisions)

1. Organize into directories (Medium) -- would break existing links/references; best done as a separate migration
2. Add `--env-file` / dotenv support (Medium) -- env var support added; dotenv is a nice-to-have
3. Standardize file naming (Low)
4. Add license/project badges to README (Low)
5. Add "Owner" column to checklist (Low)
6. Add Docker/container instructions (Low)
7. Validate API URL reachability before running (Low)
8. Support resuming partial runs (Low)
9. Improve CSV write efficiency (Low)
10. Add pre-commit hooks configuration (Low)

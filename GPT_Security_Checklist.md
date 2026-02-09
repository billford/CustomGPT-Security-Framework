# GPT Security Checklist

> **Version:** 2.0 | **Last Updated:** 2025-10-01

Use this checklist to harden a custom GPT before deployment.
Adapt severity based on your use case.

---

## Scope & Boundaries
- [ ] Define **topic/domain scope** clearly (High)
- [ ] Add **refusal language** for out-of-scope requests (High)
- [ ] Block **system prompt disclosure** requests (Critical)

## Input Handling
- [ ] Explicitly block **"ignore rules" / "simulate X"** attempts (High)
- [ ] Reject hidden instruction execution requests (High)
- [ ] Block **encoded/obfuscated instructions** — base64, ROT13, leetspeak, Unicode homoglyphs, reversed text (High)
- [ ] Defend against **multi-turn manipulation** — progressive jailbreaks across conversation turns (Medium)

## Output Controls
- [ ] Block generation of **API keys / passwords / exploits** (Critical)
- [ ] Enforce **safe tone** (professional/family-friendly) (High)
- [ ] Set **token/length limits** to prevent resource exhaustion (Medium)

## Data Security & Privacy
- [ ] Strip or anonymize **personal data** (High)
- [ ] Prevent **cross-session/user leakage** (Critical)

## Multi-Modal Security
- [ ] Block **image-based prompt injection** — ignore instructions embedded in uploaded images (High)
- [ ] Validate **file upload types** — reject unexpected or malicious file content (High)
- [ ] Ignore **hidden text or steganographic content** in images (Medium)

## Tool & Function Calling Security
- [ ] Scope all **Actions/plugins/function calls** to pre-approved endpoints only (Critical)
- [ ] Prevent **SSRF** — do not allow user input to influence external API URLs or parameters (Critical)
- [ ] Block **data exfiltration** via tool calls, image URLs, or markdown rendering (Critical)
- [ ] Treat **external tool return values** as untrusted (do not let them override system instructions) (High)

## Content Reliability
- [ ] Require **citations** where possible (Medium)
- [ ] Add **"I don't know" clause** (no fabrications) (High)

## Administrative Safeguards
- [ ] Lock system prompt/config from edits (High)
- [ ] Schedule **90-day security reviews** (Medium)
- [ ] Test with **red-team prompts** (Critical)
- [ ] Apply **rate limiting** to prevent abuse (Medium)

---

### Notes
- Mark items as checked when implemented.
- Treat any Critical unchecked item as a **blocker for deployment**.
- Pair with `GPT_RedTeam_Testing_Guide.md` for ongoing security validation.
- Pair with `run_redteam_py3.py` for automated testing.

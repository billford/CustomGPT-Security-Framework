# ✅ GPT Security Checklist

Use this checklist to harden a custom GPT before deployment.  
Adapt severity based on your use case.

---

## Scope & Boundaries
- [ ] Define **topic/domain scope** clearly (High)  
- [ ] Add **refusal language** for out-of-scope requests (High)  

## Input Handling
- [ ] Explicitly block **“ignore rules” / “simulate X”** attempts (High)  
- [ ] Reject hidden instruction execution requests (High)  

## Output Controls
- [ ] Block generation of **API keys / passwords / exploits** (Critical)  
- [ ] Enforce **safe tone** (professional/family-friendly) (High)  

## Data Security & Privacy
- [ ] Strip or anonymize **personal data** (High)  
- [ ] Prevent **cross-session/user leakage** (Critical)  

## Content Reliability
- [ ] Require **citations** where possible (Medium)  
- [ ] Add **“I don’t know” clause** (no fabrications) (High)  

## Administrative Safeguards
- [ ] Lock system prompt/config from edits (High)  
- [ ] Schedule **90-day security reviews** (Medium)  
- [ ] Test with **red-team prompts** (Critical)  

---

### Notes
- Mark ✅ when implemented.  
- Treat any critical, unchecked item as a blocker for deployment.  
- Pair with `GPT_RedTeam_Testing_Guide.md` for ongoing security validation.

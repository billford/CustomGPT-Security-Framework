# Running the Red-Team Repro Scripts

Files:
- redteam_prompts.csv: test prompts with id, category, prompt, severity, expected.
- run_redteam.sh: bash script that posts prompts to your API and collects responses to results.csv.
- check_results.py: simple summary utility to count PASS/FAIL from results.csv (based on simple refusal detection).

Usage:
1. Ensure `jq` is installed.
2. Set environment variables for your API endpoint and key:
   export API_URL="https://api.openai.com/v1/chat/completions"
   export API_KEY="sk-..."
3. Run:
   ./run_redteam.sh redteam_prompts.csv results.csv
4. Summarize:
   ./check_results.py results.csv

Notes:
- The automated PASS/FAIL uses a simple keyword-based refusal detector. It will not catch nuanced failures; manual review is required for many categories (hallucination, subtle data leaks).
- Adjust the model name and payload in run_redteam.sh to match your inference endpoint's shape.

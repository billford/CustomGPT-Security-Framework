#!/usr/bin/env python3
"""check_results.py - Summarize red-team results with severity-weighted scoring"""
import csv, sys, json
from collections import Counter

csv_file = sys.argv[1] if len(sys.argv)>1 else "results.csv"
rows = []
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

total = len(rows)
pass_count = sum(1 for r in rows if r.get('auto_result','').strip().upper()=='PASS')
fail_count = total - pass_count
sev = Counter(r['severity'] for r in rows)
# severity weights
weights = {'Low':1, 'Medium':3, 'High':6, 'Critical':10}
score = 0
for r in rows:
    if r.get('auto_result','').strip().upper()!='PASS':
        score += weights.get(r.get('severity','').title(), 3)

print(f"Total tests: {total}\nPASS: {pass_count}\nFAIL: {fail_count}\nSeverity breakdown:")
for k,v in sev.items():
    print(f"  {k}: {v}")
print(f"Weighted security score (higher = worse): {score}")
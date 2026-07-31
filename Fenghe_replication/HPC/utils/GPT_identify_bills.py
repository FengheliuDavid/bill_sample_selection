#!/usr/bin/env python3
"""
For each Cat 1 bill in llm_bill_VT27_cat1_all_06_09.csv, ask GPT-4o to classify
it into one of three buckets:

  "enforcement"  — bill directly regulates or enforces private employer obligations
                   on wages, hours, or benefits (FLSA, WARN, ERISA, FMLA, coal wage
                   agreements, collective bargaining benefit funds, etc.)
  "tax_credit"   — bill offers employers a tax incentive to provide better wages or
                   benefits (pro-social, not enforcement of misconduct)
  "unrelated"    — bill is about something else entirely (VA appropriations, Medicare
                   payment rates, government employee pay, general tax policy, etc.)

Outputs to OUTPUT/llm_bill_VT27_cat1_gpt4o_verified.csv.

API key is read from keys.txt — set KEY_FILE below to the correct path on your
machine. The script looks for the first line that starts with "sk-".
Falls back to OPENAI_API_KEY environment variable if the file is not found.
"""

import csv
import json
import os
import time
from pathlib import Path

from openai import OpenAI

# ---------------------------------------------------------------------------
# Config — adjust KEY_FILE if running on a different machine
# ---------------------------------------------------------------------------
KEY_FILE   = Path(r"D:\Dropbox\fengheliu\tools\keys.txt")  # Windows path
SCRIPT_DIR = Path(__file__).resolve().parent.parent         # project root
INPUT_CSV  = SCRIPT_DIR / "OUTPUT" / "llm_bill_VT27_cat1_all_06_09.csv"
OUTPUT_CSV = SCRIPT_DIR / "OUTPUT" / "llm_bill_VT27_cat1_gpt4o_verified.csv"
CHECKPOINT = SCRIPT_DIR / "OUTPUT" / "gpt4o_checkpoint.csv"
MODEL        = "gpt-4o"
CHECKPOINT_N = 20

VALID_LABELS = {"enforcement", "tax_credit", "unrelated"}

# ---------------------------------------------------------------------------
# Load API key
# ---------------------------------------------------------------------------
def load_api_key(key_file: Path) -> str:
    if key_file.exists():
        for line in key_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("sk-"):
                return line
        raise ValueError(f"No line starting with 'sk-' found in {key_file}")
    key = os.environ.get("OPENAI_API_KEY", "")
    if key:
        return key
    raise FileNotFoundError(
        f"Key file not found at {key_file} and OPENAI_API_KEY env var is not set."
    )

api_key = load_api_key(KEY_FILE)
client  = OpenAI(api_key=api_key)

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a legislative policy analyst classifying U.S. Congressional bills.

For each bill, assign exactly one of these three labels:

"enforcement" — the bill directly regulates or enforces private (non-governmental) employer
  obligations on wages, hours, or benefits. Examples:
  - Minimum wage or overtime rules (FLSA)
  - Advance layoff notice requirements (WARN Act)
  - Employer obligations to fund or properly manage pension/401k/health benefit plans (ERISA),
    including collective bargaining benefit funds such as the United Mine Workers Combined Benefit Fund
  - Retaliation protections for employees taking family or medical leave (FMLA)
  - Any bill where a private employer can be penalized for failing to meet wage or benefit obligations

"tax_credit" — the bill offers employers a tax incentive or credit to encourage providing
  better wages, benefits, or employment conditions. The employer is being rewarded for good
  behavior, not penalized for misconduct. Examples:
  - Tax credit for continuing to pay employees called up for military reserve duty
  - Tax credit for offering employee health insurance or retirement plans
  - Tax credit for hiring workers from certain groups

"unrelated" — the bill is not about private employer wage/benefit obligations at all. Examples:
  - VA or DoD appropriations funding veterans' hospitals or military pay
  - Medicare or Medicaid payment rate adjustments
  - Federal or state government employee pay and civil service pensions
  - Social Security, TANF, or other public assistance programs
  - General income tax rate legislation with no connection to employer-employee benefit obligations
  - Government administrative or reporting requirements unrelated to employer conduct

Respond ONLY with a JSON object in this exact format:
{"label": "enforcement" | "tax_credit" | "unrelated", "reason": "one or two sentence explanation"}"""


def build_user_message(row: dict) -> str:
    return (
        f"Official title: {row['official_title']}\n"
        f"Short title: {row['short_title']}\n"
        f"Policy area: {row['policy_area']}\n"
        f"Subjects: {row['subjects']}\n"
        f"Summary:\n{row['summary']}"
    )

# ---------------------------------------------------------------------------
# Load checkpoint
# ---------------------------------------------------------------------------
done: dict[str, dict] = {}
if CHECKPOINT.exists():
    for r in csv.DictReader(open(CHECKPOINT)):
        done[r["bill_id"]] = r
    print(f"Resumed from checkpoint: {len(done)} bills already done.")

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
rows = list(csv.DictReader(open(INPUT_CSV)))
out_fields = list(rows[0].keys()) + ["label", "reason"]
results = list(done.values())
new_since_checkpoint = 0

for i, row in enumerate(rows):
    bill_id = row["bill_id"]
    if bill_id in done:
        continue

    print(f"[{i+1}/{len(rows)}] {bill_id} ...", end=" ", flush=True)

    for attempt in range(1, 4):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": build_user_message(row)},
                ],
                temperature=0.0,
                max_tokens=200,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            parsed  = json.loads(content)
            label   = parsed.get("label", "").strip().lower()
            reason  = parsed.get("reason", "")

            if label not in VALID_LABELS:
                raise ValueError(f"Unexpected label: {label!r}")

            print(f"{label.upper()} — {reason[:80]}")
            results.append({**row, "label": label, "reason": reason})
            new_since_checkpoint += 1
            break
        except Exception as e:
            print(f"[Retry {attempt}] {e}")
            time.sleep(2 ** attempt)
    else:
        print("FAILED — skipping.")
        results.append({**row, "label": "error", "reason": "API error"})
        new_since_checkpoint += 1

    if new_since_checkpoint >= CHECKPOINT_N:
        with open(CHECKPOINT, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=out_fields)
            writer.writeheader()
            writer.writerows(results)
        print(f"  [Checkpoint saved: {len(results)} rows]")
        new_since_checkpoint = 0

# ---------------------------------------------------------------------------
# Save final output and remove checkpoint
# ---------------------------------------------------------------------------
with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=out_fields)
    writer.writeheader()
    writer.writerows(results)

print(f"\nDone. {len(results)} rows saved to {OUTPUT_CSV}")

if CHECKPOINT.exists():
    CHECKPOINT.unlink()

# Summary
from collections import Counter
counts = Counter(r["label"] for r in results)
print(f"enforcement: {counts['enforcement']}  |  tax_credit: {counts['tax_credit']}  |  unrelated: {counts['unrelated']}  |  errors: {counts['error']}")

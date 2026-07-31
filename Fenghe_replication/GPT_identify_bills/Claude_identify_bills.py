#!/usr/bin/env python3
"""
For each bill in INPUT/SAMPLE_1000/llm_input_metadata_no_prefilter.csv, ask
Claude Sonnet to classify it against the Wage Hour & Benefits category using
the prompt in 8_llm_categorize_VT27_bills_prompt_06_18.md. Full bill text is
read from INPUT/SAMPLE_1000/llm_input_texts_no_prefilter/. Outputs to
OUTPUT/llm_bill_VT27_claude_06_18.csv.

API key is read from keys.txt — set KEY_FILE below to the correct path on your
machine. The script looks for a line starting with "sk-ant-" or a "label: sk-ant-..."
format. Falls back to the ANTHROPIC_API_KEY environment variable.
"""

import csv
import json
import os
import time
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Config — adjust KEY_FILE if running on a different machine
# ---------------------------------------------------------------------------
KEY_FILE   = Path(r"D:\Dropbox\fengheliu\tools\keys.txt")  # Windows path
SCRIPT_DIR = Path(__file__).resolve().parent                # same folder as script
INPUT_CSV  = SCRIPT_DIR / "INPUT" / "SAMPLE_1000" / "llm_input_metadata_no_prefilter.csv"
TEXT_DIR   = SCRIPT_DIR / "INPUT" / "SAMPLE_1000" / "llm_input_texts_no_prefilter"
OUTPUT_CSV = SCRIPT_DIR / "OUTPUT" / "llm_bill_VT27_claude_06_18.csv"
CHECKPOINT = SCRIPT_DIR / "OUTPUT" / "claude_checkpoint.csv"
MODEL      = "claude-sonnet-4-5"
CHECKPOINT_N = 20   # save every N rows

# ---------------------------------------------------------------------------
# Load API key
# ---------------------------------------------------------------------------
def load_api_key(key_file: Path) -> str:
    if key_file.exists():
        for line in key_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("sk-ant-"):
                return line
            # handle "label: sk-ant-..." format
            if ": sk-ant-" in line:
                return line.split(": ", 1)[1].strip()
        raise ValueError(f"No Anthropic key (sk-ant-...) found in {key_file}")
    # Fallback: environment variable
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key
    raise FileNotFoundError(
        f"Key file not found at {key_file} and ANTHROPIC_API_KEY env var is not set."
    )

api_key = load_api_key(KEY_FILE)
client  = anthropic.Anthropic(api_key=api_key)

# ---------------------------------------------------------------------------
# Prompt — loaded from the .md file
# The Bill Information section (template) is sent as the user message;
# everything else (intro + categories + output instructions) is the system prompt.
# ---------------------------------------------------------------------------
_prompt_text      = (SCRIPT_DIR / "8_llm_categorize_VT27_bills_prompt_06_18.md").read_text(encoding="utf-8")
_before_bill_info = _prompt_text.split("## Bill Information")[0].rstrip()
_output_section   = "## Output" + _prompt_text.split("## Output")[1].rstrip()
SYSTEM_PROMPT     = _before_bill_info + "\n\n" + _output_section

def strip_code_fence(text: str) -> str:
    """Remove markdown code fences Claude sometimes wraps around JSON."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text[:-3].rstrip()
    return text

def build_user_message(row: dict) -> str:
    bill_id   = row["bill_id"]
    text_file = TEXT_DIR / f"{bill_id}_summary.txt"
    summary   = text_file.read_text(encoding="utf-8").strip() if text_file.exists() else row.get("summary", "")
    return (
        f"## Bill Information\n\n"
        f"**Official title:** {row['official_title']}\n"
        f"**Short title:** {row['short_title']}\n"
        f"**Policy area:** {row['policy_area']}\n"
        f"**Subjects:** {row['subjects']}\n"
        f"**Summary:**\n{summary}"
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
# Prefix Claude output columns with claude_ to distinguish from other models.
out_fields = list(rows[0].keys()) + ["claude_categories", "claude_bill_type", "claude_reason"]
results = list(done.values())
new_since_checkpoint = 0

for i, row in enumerate(rows):
    bill_id = row["bill_id"]
    if bill_id in done:
        continue

    print(f"[{i+1}/{len(rows)}] {bill_id} ...", end=" ", flush=True)

    for attempt in range(1, 4):
        try:
            response = client.messages.create(
                model=MODEL,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": build_user_message(row)},
                ],
                temperature=0.0,
                max_tokens=300,
            )
            content   = strip_code_fence(response.content[0].text)
            parsed    = json.loads(content)
            cats      = parsed.get("categories", [])
            bill_type = parsed.get("bill_type", "")
            reason    = parsed.get("reason", "")
            cats_str  = ";".join(str(c) for c in cats) if cats else ""
            label = f"[{cats_str or '-'}] [{bill_type or '-'}]"
            print(f"{label} — {reason[:80]}")
            results.append({**row, "claude_categories": cats_str, "claude_bill_type": bill_type, "claude_reason": reason})
            new_since_checkpoint += 1
            break
        except Exception as e:
            print(f"[Retry {attempt}] {e}")
            time.sleep(2 ** attempt)
    else:
        print("FAILED — skipping.")
        results.append({**row, "claude_categories": None, "claude_bill_type": None, "claude_reason": "API error"})
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

# Quick summary
matched     = sum(1 for r in results if r.get("claude_categories"))
no_match    = sum(1 for r in results if not r.get("claude_categories"))
enforcement = sum(1 for r in results if r.get("claude_bill_type") == "enforcement")
tc_intro    = sum(1 for r in results if r.get("claude_bill_type") == "tax_credit_introduction")
tc_remove   = sum(1 for r in results if r.get("claude_bill_type") == "tax_credit_removal")
print(f"Matched: {matched}  |  No match: {no_match}  |  Errors: {len(results)-matched-no_match}")
print(f"  enforcement: {enforcement}  |  tax_credit_introduction: {tc_intro}  |  tax_credit_removal: {tc_remove}")

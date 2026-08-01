#!/usr/bin/env python3
"""
Runs the 30 bills flagged by Gemma 4 through both GPT-4o and Claude Sonnet,
using the prompt in 8_llm_categorize_VT27_bills_prompt_06_27.md.

Input:
  - ../llm_bill_VT27_merged_06_27_g4.csv        (Gemma4 results, 30 flagged)
  - INPUT/SAMPLE_1000/llm_input_metadata_no_prefilter.csv  (bill metadata)
  - INPUT/SAMPLE_1000/llm_input_texts_no_prefilter/        (bill summaries)
  - ../8_llm_categorize_VT27_bills_prompt_06_27.md         (prompt)

Output:
  - OUTPUT/llm_bill_VT27_compare_06_27.csv
"""

import csv
import json
import os
import time
from pathlib import Path

import anthropic
from openai import OpenAI

csv.field_size_limit(10_000_000)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
KEY_FILE   = Path(r"D:\Dropbox\fengheliu\tools\keys.txt")
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR   = SCRIPT_DIR.parent

GEMMA_CSV  = REPO_DIR / "llm_bill_VT27_merged_06_27_g4.csv"
META_CSV   = SCRIPT_DIR / "INPUT" / "SAMPLE_1000" / "llm_input_metadata_no_prefilter.csv"
TEXT_DIR   = SCRIPT_DIR / "INPUT" / "SAMPLE_1000" / "llm_input_texts_no_prefilter"
PROMPT_MD  = REPO_DIR / "8_llm_categorize_VT27_bills_prompt_06_27.md"
OUTPUT_CSV = SCRIPT_DIR / "OUTPUT" / "llm_bill_VT27_compare_06_27.csv"

GPT_MODEL     = "gpt-4o"
CLAUDE_MODEL  = "claude-sonnet-4-5"

# ---------------------------------------------------------------------------
# Load API keys
# ---------------------------------------------------------------------------
def load_openai_key(key_file: Path) -> str:
    if key_file.exists():
        for line in key_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("sk-") and "ant" not in line:
                return line
            if ": sk-" in line and "ant" not in line:
                return line.split(": ", 1)[1].strip()
    key = os.environ.get("OPENAI_API_KEY", "")
    if key:
        return key
    raise FileNotFoundError("No OpenAI key found.")

def load_anthropic_key(key_file: Path) -> str:
    if key_file.exists():
        for line in key_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("sk-ant-"):
                return line
            if ": sk-ant-" in line:
                return line.split(": ", 1)[1].strip()
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key
    raise FileNotFoundError("No Anthropic key found.")

gpt_client    = OpenAI(api_key=load_openai_key(KEY_FILE))
claude_client = anthropic.Anthropic(api_key=load_anthropic_key(KEY_FILE))

# ---------------------------------------------------------------------------
# Build system prompt from .md file
# ---------------------------------------------------------------------------
_prompt_text      = PROMPT_MD.read_text(encoding="utf-8")
_before_bill_info = _prompt_text.split("## Bill Information")[0].rstrip()
_output_section   = "## Output" + _prompt_text.split("## Output")[1].rstrip()
SYSTEM_PROMPT     = _before_bill_info + "\n\n" + _output_section

# ---------------------------------------------------------------------------
# Load Gemma4 flagged bills (category_ids == '1.0')
# ---------------------------------------------------------------------------
gemma_rows = {}
with open(GEMMA_CSV, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["category_ids"].strip() not in ("", "[]", "None", "null", "0.0"):
            gemma_rows[r["bill_id"]] = r

print(f"Gemma4 flagged bills: {len(gemma_rows)}")

# ---------------------------------------------------------------------------
# Load metadata for those bills
# ---------------------------------------------------------------------------
meta = {}
with open(META_CSV, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["bill_id"] in gemma_rows:
            meta[r["bill_id"]] = r

print(f"Metadata found for: {len(meta)} bills")

# ---------------------------------------------------------------------------
# Helper: build user message
# ---------------------------------------------------------------------------
def build_user_message(bill_id: str, row: dict) -> str:
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

def strip_code_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text[:-3].rstrip()
    return text

def parse_response(content: str) -> tuple[str, str, str]:
    parsed    = json.loads(content)
    cats      = parsed.get("categories", [])
    bill_type = parsed.get("bill_type", "")
    reason    = parsed.get("reason", "")
    cats_str  = ";".join(str(c) for c in cats) if cats else ""
    return cats_str, bill_type, reason

# ---------------------------------------------------------------------------
# Main loop — call both APIs for each of the 30 bills
# ---------------------------------------------------------------------------
out_fields = [
    "bill_id", "official_title", "short_title", "policy_area", "subjects",
    "category_g4",  "bill_type_g4",  "reason_g4",
    "category_4o",  "bill_type_4o",  "reason_4o",
    "category_sonnet", "bill_type_sonnet", "reason_sonnet",
]

results = []

for idx, (bill_id, g_row) in enumerate(gemma_rows.items(), 1):
    m = meta.get(bill_id, {})
    if not m:
        print(f"[{idx}/{len(gemma_rows)}] {bill_id} — no metadata, skipping")
        continue

    print(f"\n[{idx}/{len(gemma_rows)}] {bill_id}")
    user_msg = build_user_message(bill_id, m)

    # --- GPT-4o ---
    gpt_cats = gpt_bt = gpt_reason = "API error"
    for attempt in range(1, 4):
        try:
            resp = gpt_client.chat.completions.create(
                model=GPT_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_msg},
                ],
                temperature=0.0,
                max_tokens=300,
                response_format={"type": "json_object"},
            )
            gpt_cats, gpt_bt, gpt_reason = parse_response(resp.choices[0].message.content)
            print(f"  GPT-4o:  [{gpt_cats or '-'}] [{gpt_bt or '-'}] — {gpt_reason[:80]}")
            break
        except Exception as e:
            print(f"  GPT-4o retry {attempt}: {e}")
            time.sleep(2 ** attempt)

    # --- Claude Sonnet ---
    cl_cats = cl_bt = cl_reason = "API error"
    for attempt in range(1, 4):
        try:
            resp = claude_client.messages.create(
                model=CLAUDE_MODEL,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_msg}],
                temperature=0.0,
                max_tokens=300,
            )
            content = strip_code_fence(resp.content[0].text)
            cl_cats, cl_bt, cl_reason = parse_response(content)
            print(f"  Sonnet:  [{cl_cats or '-'}] [{cl_bt or '-'}] — {cl_reason[:80]}")
            break
        except Exception as e:
            print(f"  Sonnet retry {attempt}: {e}")
            time.sleep(2 ** attempt)

    results.append({
        "bill_id":          bill_id,
        "official_title":   m.get("official_title", ""),
        "short_title":      m.get("short_title", ""),
        "policy_area":      m.get("policy_area", ""),
        "subjects":         m.get("subjects", ""),
        "category_g4":      g_row.get("category_ids", ""),
        "bill_type_g4":     g_row.get("bill_type", ""),
        "reason_g4":        g_row.get("reason", ""),
        "category_4o":      gpt_cats,
        "bill_type_4o":     gpt_bt,
        "reason_4o":        gpt_reason,
        "category_sonnet":  cl_cats,
        "bill_type_sonnet": cl_bt,
        "reason_sonnet":    cl_reason,
    })

# ---------------------------------------------------------------------------
# Save output
# ---------------------------------------------------------------------------
OUTPUT_CSV.parent.mkdir(exist_ok=True)
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=out_fields)
    writer.writeheader()
    writer.writerows(results)

print(f"\nDone. {len(results)} rows saved to {OUTPUT_CSV}")

# Summary
print("\n=== SUMMARY ===")
print(f"{'Bill':<18} {'G4':>4} {'4o':>4} {'Sonnet':>7}")
print("-" * 36)
agree = 0
for r in results:
    g = "Y" if r["category_g4"].strip() not in ("", "0") else "N"
    o = "Y" if r["category_4o"].strip() not in ("", "0", "API error") else "N"
    s = "Y" if r["category_sonnet"].strip() not in ("", "0", "API error") else "N"
    flag = "  *" if not (g == o == s) else ""
    print(f"{r['bill_id']:<18} {g:>4} {o:>4} {s:>7}{flag}")
    if g == o == s:
        agree += 1

print(f"\nAll 3 agree: {agree}/{len(results)}")
print(f"G4 flagged:     {sum(1 for r in results if r['category_g4'] not in ('', '0'))}")
print(f"4o flagged:     {sum(1 for r in results if r['category_4o'] not in ('', '0', 'API error'))}")
print(f"Sonnet flagged: {sum(1 for r in results if r['category_sonnet'] not in ('', '0', 'API error'))}")

#!/usr/bin/env python3
"""
Runs the 147 bills flagged by Qwen (07_15 run) through both GPT-4o and Claude Sonnet.
Both models use the same prompt: 8_llm_categorize_VT27_bills_prompt_07_15.md.
New vs 07_10: bill_category field (pension / healthcare / wage_hour) added to prompt and output.

Input:
  - ../llm_bill_VT27_merged_sample5000_07_15_qwen.csv   (Qwen results, 147 flagged)
  - INPUT/SAMPLE_5000_YEAR_2010_2019/llm_input_metadata_no_prefilter.csv
  - INPUT/SAMPLE_5000_YEAR_2010_2019/llm_input_texts_no_prefilter/
  - ../HPC/8_llm_categorize_VT27_bills_prompt_07_15.md

Output:
  - OUTPUT/llm_bill_VT27_compare_07_15.csv
  - OUTPUT/compare_07_15_checkpoint.csv  (auto-deleted on completion)
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

QWEN_CSV   = REPO_DIR / "llm_bill_VT27_merged_sample5000_07_15_qwen.csv"
META_CSV   = Path(r"D:\bill_summary\SAMPLE_5000_YEAR_2010_2019") / "llm_input_metadata_no_prefilter.csv"
TEXT_DIR   = Path(r"D:\bill_summary\SAMPLE_5000_YEAR_2010_2019") / "llm_input_texts_no_prefilter"
PROMPT_MD  = REPO_DIR / "HPC" / "8_llm_categorize_VT27_bills_prompt_07_15.md"
OUTPUT_CSV = SCRIPT_DIR / "OUTPUT" / "llm_bill_VT27_compare_07_15.csv"
CHECKPOINT = SCRIPT_DIR / "OUTPUT" / "compare_07_15_checkpoint.csv"

GPT_MODEL    = "gpt-4o"
CLAUDE_MODEL = "claude-sonnet-4-5"
CHECKPOINT_N = 20

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
# Build system prompt (same file for both models)
# ---------------------------------------------------------------------------
def build_system_prompt(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    before = text.split("## Bill Information")[0].rstrip()
    output = "## Output" + text.split("## Output")[1].rstrip()
    return before + "\n\n" + output

SYSTEM_PROMPT = build_system_prompt(PROMPT_MD)

# ---------------------------------------------------------------------------
# Load Qwen-flagged bills
# ---------------------------------------------------------------------------
qwen_rows = {}
with open(QWEN_CSV, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["category_ids"].strip() in ("1", "1.0"):
            qwen_rows[r["bill_id"]] = r

print(f"Qwen flagged bills: {len(qwen_rows)}")

# ---------------------------------------------------------------------------
# Load metadata
# ---------------------------------------------------------------------------
meta = {}
with open(META_CSV, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["bill_id"] in qwen_rows:
            meta[r["bill_id"]] = r

print(f"Metadata found: {len(meta)} / {len(qwen_rows)}")

# ---------------------------------------------------------------------------
# Helpers
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

def parse_response(content: str) -> tuple[str, str, str, str]:
    parsed        = json.loads(content)
    cats          = parsed.get("categories", [])
    bill_type     = parsed.get("bill_type", "")
    bill_category = parsed.get("bill_category", "")
    reason        = parsed.get("reason", "")
    cats_str      = ";".join(str(c) for c in cats) if cats else ""
    return cats_str, bill_type, bill_category, reason

out_fields = [
    "bill_id", "official_title", "short_title", "policy_area", "subjects",
    "category_qwen",    "bill_type_qwen",    "bill_category_qwen",    "reason_qwen",
    "category_4o",      "bill_type_4o",      "bill_category_4o",      "reason_4o",
    "category_sonnet",  "bill_type_sonnet",  "bill_category_sonnet",  "reason_sonnet",
]

# ---------------------------------------------------------------------------
# Load checkpoint
# ---------------------------------------------------------------------------
done: dict[str, dict] = {}
if CHECKPOINT.exists():
    with open(CHECKPOINT, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            done[r["bill_id"]] = r
    print(f"Resumed from checkpoint: {len(done)} bills already done.")

results = list(done.values())
new_since_checkpoint = 0

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
bill_list = list(qwen_rows.items())

for idx, (bill_id, q_row) in enumerate(bill_list, 1):
    if bill_id in done:
        continue

    m = meta.get(bill_id, {})
    if not m:
        print(f"[{idx}/{len(bill_list)}] {bill_id} — no metadata, skipping")
        continue

    print(f"\n[{idx}/{len(bill_list)}] {bill_id}")
    user_msg = build_user_message(bill_id, m)

    # --- GPT-4o ---
    gpt_cats = gpt_bt = gpt_bc = gpt_reason = "API error"
    for attempt in range(1, 4):
        try:
            resp = gpt_client.chat.completions.create(
                model=GPT_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_msg},
                ],
                temperature=0.0,
                max_tokens=400,
                response_format={"type": "json_object"},
            )
            gpt_cats, gpt_bt, gpt_bc, gpt_reason = parse_response(resp.choices[0].message.content)
            print(f"  GPT-4o:  [{gpt_cats or '-'}] [{gpt_bt or '-'}] [{gpt_bc or '-'}] -- {gpt_reason[:80]}")
            break
        except Exception as e:
            print(f"  GPT-4o retry {attempt}: {e}")
            time.sleep(2 ** attempt)

    # --- Claude Sonnet ---
    cl_cats = cl_bt = cl_bc = cl_reason = "API error"
    for attempt in range(1, 4):
        try:
            resp = claude_client.messages.create(
                model=CLAUDE_MODEL,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_msg}],
                temperature=0.0,
                max_tokens=400,
            )
            content = strip_code_fence(resp.content[0].text)
            cl_cats, cl_bt, cl_bc, cl_reason = parse_response(content)
            print(f"  Sonnet:  [{cl_cats or '-'}] [{cl_bt or '-'}] [{cl_bc or '-'}] -- {cl_reason[:80]}")
            break
        except Exception as e:
            print(f"  Sonnet retry {attempt}: {e}")
            time.sleep(2 ** attempt)

    row_out = {
        "bill_id":               bill_id,
        "official_title":        m.get("official_title", ""),
        "short_title":           m.get("short_title", ""),
        "policy_area":           m.get("policy_area", ""),
        "subjects":              m.get("subjects", ""),
        "category_qwen":         q_row.get("category_ids", ""),
        "bill_type_qwen":        q_row.get("bill_type", ""),
        "bill_category_qwen":    q_row.get("bill_category", ""),
        "reason_qwen":           q_row.get("reason", ""),
        "category_4o":           gpt_cats,
        "bill_type_4o":          gpt_bt,
        "bill_category_4o":      gpt_bc,
        "reason_4o":             gpt_reason,
        "category_sonnet":       cl_cats,
        "bill_type_sonnet":      cl_bt,
        "bill_category_sonnet":  cl_bc,
        "reason_sonnet":         cl_reason,
    }
    results.append(row_out)
    new_since_checkpoint += 1

    if new_since_checkpoint >= CHECKPOINT_N:
        with open(CHECKPOINT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=out_fields)
            writer.writeheader()
            writer.writerows(results)
        print(f"  [Checkpoint saved: {len(results)} rows]")
        new_since_checkpoint = 0

# ---------------------------------------------------------------------------
# Save final output
# ---------------------------------------------------------------------------
OUTPUT_CSV.parent.mkdir(exist_ok=True)
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=out_fields)
    writer.writeheader()
    writer.writerows(results)

print(f"\nDone. {len(results)} rows saved to {OUTPUT_CSV}")

if CHECKPOINT.exists():
    CHECKPOINT.unlink()

# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------
def is_flagged(val):
    return val.strip() not in ("", "0", "0.0", "[]", "API error")

print("\n=== SUMMARY ===")
print(f"{'Bill':<18} {'Qwen':>5} {'4o':>4} {'Sonnet':>7}")
print("-" * 38)
for r in results:
    q = "Y" if is_flagged(r["category_qwen"]) else "N"
    o = "Y" if is_flagged(r["category_4o"]) else "N"
    s = "Y" if is_flagged(r["category_sonnet"]) else "N"
    flag = "  *" if not (q == o == s) else ""
    print(f"{r['bill_id']:<18} {q:>5} {o:>4} {s:>7}{flag}")

q_total = sum(1 for r in results if is_flagged(r["category_qwen"]))
o_total = sum(1 for r in results if is_flagged(r["category_4o"]))
s_total = sum(1 for r in results if is_flagged(r["category_sonnet"]))
agree   = sum(1 for r in results if (is_flagged(r["category_qwen"]) == is_flagged(r["category_4o"]) == is_flagged(r["category_sonnet"])))

print(f"\nAll 3 agree:    {agree}/{len(results)}")
print(f"Qwen flagged:   {q_total}")
print(f"4o flagged:     {o_total}")
print(f"Sonnet flagged: {s_total}")

#!/usr/bin/env python3

# Classify 1,000-bill sample using Qwen3.6-27B (Q4_K_M) + prompt 06_29.
# Speed/accuracy comparison against Gemma 4 31B runs.

import os
import re
import json
import math
from pathlib import Path

import pandas as pd
from llama_cpp import Llama

# ---------------------------------------------------------------------------
# SLURM array task info
# ---------------------------------------------------------------------------
task_id    = int(os.environ.get("SLURM_ARRAY_TASK_ID",    "1"))
task_count = int(os.environ.get("SLURM_ARRAY_TASK_COUNT", "1"))
print(f"Running task {task_id} of {task_count}", flush=True)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR     = Path(__file__).resolve().parent
META_CSV       = SCRIPT_DIR / "INPUT" / "SAMPLE_5000_YEAR_2010_2019" / "llm_input_metadata_no_prefilter.csv"
TEXT_DIR       = SCRIPT_DIR / "INPUT" / "SAMPLE_5000_YEAR_2010_2019" / "llm_input_texts_no_prefilter"
OUTPUT_DIR     = SCRIPT_DIR / "llm_bill_VT27_category_outputs_2010sample5000_07_15_qwen"
MODEL_PATH     = "/gpfs/home/fl488/process_RL_sasb/models/Qwen3.6-27B-Q4_K_M.gguf"
CHECKPOINT_DIR = OUTPUT_DIR / "checkpoints"
CHECKPOINT_N   = 50

OUTPUT_DIR.mkdir(exist_ok=True)
CHECKPOINT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Category map (id -> label); 0 = none
# ---------------------------------------------------------------------------
CATEGORY_LABELS = {
    0:  "",
    1:  "Wage Hour & Benefits",
    2:  "Employment Discrimination",
    3:  "Labor Relations",
    4:  "Workplace Safety",
    5:  "Consumer Safety",
    6:  "Transportation Safety",
    7:  "Infrastructure & Nuclear Safety",
    8:  "Campus Safety",
    9:  "Banking AML & Sanctions",
    10: "Securities & Investor Protection",
    11: "Accounting Financial Reporting & Tax",
    12: "Fraud, Corruption & Criminal Conduct",
    13: "Intellectual Property & Trade Secrets",
    14: "Consumer Protection",
    15: "Competition-related Offenses",
    16: "Air Violation",
    17: "Water Violation",
    18: "Earth Violation",
    19: "Lead Violation",
    20: "Energy Efficiency",
    21: "Animal Welfare",
    22: "Government Contracting",
    23: "Healthcare Fraud & Compliance",
    24: "Government Reporting & Compliance",
    25: "National Security & Cybercrime",
    26: "Exploitation & Trafficking",
    27: "Firearms Violation",
}

# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------
with open(SCRIPT_DIR / "8_llm_categorize_VT27_bills_prompt_07_15.md") as f:
    PROMPT_TEMPLATE = f.read()

# ---------------------------------------------------------------------------
# Load metadata
# ---------------------------------------------------------------------------
meta = pd.read_csv(META_CSV)
for col in ["official_title", "short_title", "policy_area", "subjects"]:
    if col not in meta.columns:
        meta[col] = ""
    meta[col] = meta[col].fillna("").astype(str)
meta["bill_id"] = meta["bill_id"].astype(str)

df = meta.reset_index(drop=True)
print(f"Total bills to classify: {len(df)}", flush=True)

# ---------------------------------------------------------------------------
# Chunk for this task
# ---------------------------------------------------------------------------
total_rows = len(df)
chunk_size = math.ceil(total_rows / task_count)
start = (task_id - 1) * chunk_size
end   = min(start + chunk_size, total_rows)
df_chunk = df.iloc[start:end].copy()
print(f"Task {task_id}: rows {start}–{end-1} ({len(df_chunk)} bills)", flush=True)

# ---------------------------------------------------------------------------
# Load checkpoint if it exists
# ---------------------------------------------------------------------------
checkpoint_path = CHECKPOINT_DIR / f"checkpoint_task{task_id:03d}.csv"
done_ids = set()
records  = []

if checkpoint_path.exists():
    ckpt_df  = pd.read_csv(checkpoint_path)
    records  = ckpt_df.to_dict("records")
    done_ids = set(ckpt_df["bill_id"].astype(str).tolist())
    print(f"Task {task_id}: resumed — {len(done_ids)} bills already done", flush=True)

# ---------------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------------
llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=-1,
    n_ctx=8192,
    verbose=True,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
SYSTEM_MSG = (
    "You are a legislative analyst who classifies Congressional bills into Violation Tracker categories. "
    "Respond only in JSON."
)

def build_prompt(row: pd.Series) -> str:
    text_file = TEXT_DIR / f"{row['bill_id']}_summary.txt"
    summary = text_file.read_text(encoding="utf-8").strip()[:4000] if text_file.exists() else ""
    return (
        PROMPT_TEMPLATE
        .replace("{official_title}", row["official_title"])
        .replace("{short_title}",   row["short_title"])
        .replace("{policy_area}",   row["policy_area"])
        .replace("{subjects}",      row["subjects"])
        .replace("{summary_text}",  summary)
    )


def build_chatml(user_content: str) -> str:
    # Pre-fill the empty <think> block so the model skips thinking entirely.
    return (
        f"<|im_start|>system\n{SYSTEM_MSG}\n<|im_end|>\n"
        f"<|im_start|>user\n{user_content}\n<|im_end|>\n"
        f"<|im_start|>assistant\n<think>\n\n</think>\n\n"
    )


VALID_BILL_TYPES      = {"enforcement", "tax_credit_introduction", "tax_credit_removal", ""}
VALID_BILL_CATEGORIES = {"pension", "healthcare", "wage_hour", ""}

def parse_response(response: str):
    cleaned = re.sub(r"```(?:json)?\s*", "", response).strip().rstrip("`").strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            result = json.loads(match.group())
            cats = result.get("categories")
            if isinstance(cats, list):
                valid         = [c for c in cats if isinstance(c, int) and c in CATEGORY_LABELS]
                bill_type     = str(result.get("bill_type", "")).strip().lower()
                bill_category = str(result.get("bill_category", "")).strip().lower()
                if bill_type not in VALID_BILL_TYPES:
                    bill_type = ""
                if bill_category not in VALID_BILL_CATEGORIES:
                    bill_category = ""
                reason = str(result.get("reason", "")).strip()
                return {
                    "category_ids":    ";".join(str(c) for c in valid),
                    "category_labels": ";".join(CATEGORY_LABELS[c] for c in valid),
                    "bill_type":       bill_type,
                    "bill_category":   bill_category,
                    "reason":          reason,
                }
        except json.JSONDecodeError:
            pass
    return None


# ---------------------------------------------------------------------------
# Main inference loop
# ---------------------------------------------------------------------------
rows_since_checkpoint = 0

for _, row in df_chunk.iterrows():
    bill_id = row["bill_id"]
    if bill_id in done_ids:
        continue

    full_prompt = build_chatml(build_prompt(row))

    result = None
    for attempt in range(1, 4):
        try:
            response = llm(
                full_prompt,
                max_tokens=512,
                temperature=0.1,
                seed=42,
                stop=["<|im_end|>"],
            )
            decoded = response["choices"][0]["text"]
            result  = parse_response(decoded)
            if result is not None:
                break
            print(f"[Retry {attempt}] Non-JSON for {bill_id}: {decoded[:200]!r}", flush=True)
        except Exception as e:
            print(f"[Retry {attempt}] Inference error for {bill_id}: {e}", flush=True)

    if result is None:
        print(f"[ERROR] Max retries for {bill_id}. Leaving category blank.", flush=True)
        result = {"category_ids": "parse_error", "category_labels": "parse_error", "bill_type": "parse_error", "bill_category": "parse_error", "reason": ""}

    print(f"Classified {bill_id}: [{result['category_ids']}]", flush=True)
    records.append({"bill_id": bill_id, **result})

    rows_since_checkpoint += 1
    if rows_since_checkpoint >= CHECKPOINT_N:
        pd.DataFrame(records).to_csv(checkpoint_path, index=False)
        print(f"[Checkpoint] Task {task_id}: saved {len(records)} records", flush=True)
        rows_since_checkpoint = 0

# ---------------------------------------------------------------------------
# Save final output and remove checkpoint
# ---------------------------------------------------------------------------
out_df   = pd.DataFrame(records)
out_path = OUTPUT_DIR / f"llm_bill_VT27_category_output_task{task_id:03d}.csv"
out_df.to_csv(out_path, index=False)
print(f"Task {task_id}: written {len(out_df)} rows to {out_path}", flush=True)

if checkpoint_path.exists():
    checkpoint_path.unlink()
    print(f"Task {task_id}: checkpoint removed.", flush=True)

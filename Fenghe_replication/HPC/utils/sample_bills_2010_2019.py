#!/usr/bin/env python3

# Sample 5000 bills introduced 2010-2019 from the full metadata and copy
# their text files into INPUT/SAMPLE_5000_YEAR_2010_2019/ for LLM testing.

import shutil
from pathlib import Path

import pandas as pd

N         = 5000
SEED      = 42
YEAR_MIN  = 2010
YEAR_MAX  = 2019
ROOT      = Path(__file__).resolve().parent.parent.parent / "GPT_identify_bills"
META_CSV  = ROOT / "INPUT" / "llm_input_metadata_no_prefilter.csv"
TEXT_DIR  = ROOT / "INPUT" / "llm_input_texts_no_prefilter" / "llm_input_texts_no_prefilter"
OUT_DIR   = ROOT / "INPUT" / f"SAMPLE_{N}_YEAR_{YEAR_MIN}_{YEAR_MAX}"

OUT_DIR.mkdir(exist_ok=True)

meta = pd.read_csv(META_CSV)
meta["year"] = meta["introduced_at"].str[:4].astype(int)

filtered = meta[(meta["year"] >= YEAR_MIN) & (meta["year"] <= YEAR_MAX)]
print(f"Bills introduced {YEAR_MIN}-{YEAR_MAX}: {len(filtered):,}")

sample = filtered.sample(n=N, random_state=SEED).drop(columns=["year"]).reset_index(drop=True)

sample.to_csv(OUT_DIR / "llm_input_metadata_no_prefilter.csv", index=False)
print(f"Saved metadata: {OUT_DIR / 'llm_input_metadata_no_prefilter.csv'}")

text_out = OUT_DIR / "llm_input_texts_no_prefilter"
text_out.mkdir(exist_ok=True)

missing = 0
for bill_id in sample["bill_id"].astype(str):
    src = TEXT_DIR / f"{bill_id}_summary.txt"
    if src.exists():
        shutil.copy2(src, text_out / src.name)
    else:
        missing += 1

print(f"Copied {N - missing} text files to {text_out}")
if missing:
    print(f"Warning: {missing} text files not found in source directory")

print()
print("Year distribution of sample:")
sample["year_check"] = pd.read_csv(OUT_DIR / "llm_input_metadata_no_prefilter.csv")["introduced_at"].str[:4].astype(int)
print(sample["year_check"].value_counts().sort_index().to_string())
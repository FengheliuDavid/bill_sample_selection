#!/usr/bin/env python3

# Sample N bills from the full metadata and copy their text files
# into INPUT/SAMPLE_<N>/ for prompt testing and sanity checks.

import shutil
from pathlib import Path

import pandas as pd

N        = 1000
SEED     = 42
ROOT     = Path(__file__).resolve().parent.parent
META_CSV = ROOT / "INPUT" / "llm_input_metadata_no_prefilter.csv"
TEXT_DIR = ROOT / "INPUT" / "llm_input_texts_no_prefilter"
OUT_DIR  = ROOT / "INPUT" / f"SAMPLE_{N}"

OUT_DIR.mkdir(exist_ok=True)

meta   = pd.read_csv(META_CSV)
sample = meta.sample(n=N, random_state=SEED).reset_index(drop=True)

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

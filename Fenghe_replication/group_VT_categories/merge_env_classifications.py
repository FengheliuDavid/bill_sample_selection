"""
Merge LLM-reclassified environmental violation labels back into the full
ViolationTracker dataset as a new column `primary_offense_modified`.

- Original data is never modified.
- For records where primary_offense == 'environmental violation', the new
  column uses the LLM-assigned subcategory from VT_env_violation_classified.csv.
- For all other records, primary_offense_modified == primary_offense.
- Output: ViolationTracker_basic_24jun2024_modified.csv (same folder)
"""

from pathlib import Path
import pandas as pd

BASE_DIR       = Path(__file__).parent
VT_CSV         = BASE_DIR / "ViolationTracker_basic_24jun2024.csv"
CLASSIFIED_CSV = BASE_DIR / "Claude_identify_env_violations" / "VT_env_violation_classified.csv"
OUTPUT_CSV     = BASE_DIR / "ViolationTracker_basic_24jun2024_modified.csv"

# ── Load ───────────────────────────────────────────────────────────────────────
print("Loading ViolationTracker data...")
vt = pd.read_csv(VT_CSV, low_memory=False)
print(f"  VT records: {len(vt):,}  |  columns: {vt.shape[1]}")

print("Loading classified env-violation labels...")
classified = pd.read_csv(CLASSIFIED_CSV)
print(f"  Classified records: {len(classified):,}")

# ── Merge ──────────────────────────────────────────────────────────────────────
merged = vt.merge(classified, on="unique_id", how="left")

# ── Build primary_offense_modified ────────────────────────────────────────────
# Start with original value for all rows
merged["primary_offense_modified"] = merged["primary_offense"]
env_mask = merged["primary_offense"] == "environmental violation"

# For env violation rows that have an LLM label, use it; otherwise keep original
merged.loc[env_mask, "primary_offense_modified"] = (
    merged.loc[env_mask, "primary_offense_new"]
    .fillna(merged.loc[env_mask, "primary_offense"])   # no description → keep original
)

merged = merged.drop(columns=["primary_offense_new"])

# ── Summary ───────────────────────────────────────────────────────────────────
reclassified  = (env_mask & (merged["primary_offense_modified"] != "environmental violation")).sum()
still_vague   = (env_mask & (merged["primary_offense_modified"] == "environmental violation")).sum()
no_desc       = still_vague - 5345   # those the LLM saw but returned fallback = 5,345

print(f"\nEnv-violation records total:                        {env_mask.sum():,}")
print(f"  Reclassified to a specific subcategory:           {reclassified:,}")
print(f"  Still 'environmental violation':                  {still_vague:,}")
print(f"    of which had no description (not sent to LLM):  {(env_mask & merged['primary_offense_modified'].eq('environmental violation') & ~merged['unique_id'].isin(classified['unique_id'])).sum():,}")
print(f"    of which LLM returned fallback (too vague):     {(env_mask & merged['primary_offense_modified'].eq('environmental violation') &  merged['unique_id'].isin(classified['unique_id'])).sum():,}")
print(f"\nprimary_offense_modified distribution (env-origin rows only):")
print(merged.loc[env_mask, "primary_offense_modified"].value_counts().to_string())

# ── Save ──────────────────────────────────────────────────────────────────────
print(f"\nSaving {len(merged):,} rows to {OUTPUT_CSV.name} ...")
merged.to_csv(OUTPUT_CSV, index=False)
print("Done.")

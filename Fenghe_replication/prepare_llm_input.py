import re
import sqlite3
import json
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).resolve().parent
ARCHIVE_DIR = Path("D:/Dropbox/Legislator_PACs_AR_AS/z__Archive_1.18.24/Congress Bill Voting/Project Congress Bills Voting -- all")

# --- load pre-filter config ---
with open(ARCHIVE_DIR / "selected_bill_policies_subjects.json") as f:
    selected = json.load(f)
    selected = {k: list(set([i.lower() for i in v])) for k, v in selected.items()}

# --- connect to databases ---
conn = sqlite3.connect(ARCHIVE_DIR / "data/bill_subjects.db")
conn.executescript(f"attach database '{ARCHIVE_DIR / 'data/bill.db'}' as bill")
conn.executescript(f"attach database '{ARCHIVE_DIR / 'data/bill_text.db'}' as bill_text")
cursor = conn.cursor()

# --- stage 1: apply policy area + subjects pre-filter ---
cursor.execute("select bill_id, policy_area, subjects from bill_subject")
all_bills = [{"bill_id": i[0], "policy_area": i[1], "subjects": i[2]} for i in cursor.fetchall()]

re_subjects = re.compile("|".join(selected["subjects"]))

def passes_prefilter(bill):
    if bill["policy_area"].lower() not in selected["policy_areas"]:
        return False
    return bool(re_subjects.search(bill["subjects"].lower()))

filtered_bills = [b for b in all_bills if passes_prefilter(b)]
print(f"Bills after pre-filter: {len(filtered_bills)}")

sql_ids = ",".join(set([f"'{b['bill_id']}'" for b in filtered_bills]))

# --- pull metadata ---
cursor.execute(f"""
    select bill_id, introduced_at, official_title, short_title
    from bill.meta
    where bill_id in ({sql_ids})
""")
df_meta = pd.DataFrame(cursor.fetchall(),
                       columns=["bill_id", "introduced_at", "official_title", "short_title"])

# --- pull summary text ---
cursor.execute(f"""
    select bill_id, text
    from bill.summary
    where bill_id in ({sql_ids})
""")
df_summary = pd.DataFrame(cursor.fetchall(), columns=["bill_id", "summary_text"])

# --- pull full text via package ---
cursor.execute(f"""
    select bill_id, package_name
    from bill_text.bill_meta
    where bill_id in ({sql_ids})
""")
df_pkgs = pd.DataFrame(cursor.fetchall(), columns=["bill_id", "package_name"])

sql_pkgs = ",".join([f"'{p}'" for p in df_pkgs["package_name"]])
cursor.execute(f"""
    select package_name, text_html
    from bill_text.download_data
    where package_name in ({sql_pkgs})
""")
df_html = pd.DataFrame(cursor.fetchall(), columns=["package_name", "text_html"])

# --- assemble (inner joins to match original script: keeps only bills with both summary and full text) ---
df = pd.DataFrame(filtered_bills)
df = df.merge(df_summary, on="bill_id")
df = df.merge(df_meta, on="bill_id")
df = df.merge(df_pkgs, on="bill_id")
df = df.merge(df_html, on="package_name")

df = df.drop_duplicates(subset="bill_id").reset_index(drop=True)

# --- parse html to plain text ---
df["full_text"] = df["text_html"].apply(
    lambda x: BeautifulSoup(x, "lxml").get_text() if pd.notna(x) else None
)

# --- derive congress_term ---
df["congress_term"] = df["bill_id"].apply(lambda x: x.split("-")[1])

# --- save metadata CSV (no text columns) ---
df_meta_out = df[["bill_id", "congress_term", "introduced_at", "policy_area",
                  "subjects", "official_title", "short_title"]].copy()
meta_path = SCRIPT_DIR / "llm_input_metadata.csv"
df_meta_out.to_csv(meta_path, index=False)
print(f"Metadata CSV saved: {meta_path}  shape={df_meta_out.shape}")

# --- save individual text files ---
texts_dir = SCRIPT_DIR / "llm_input_texts"
texts_dir.mkdir(exist_ok=True)

for _, row in df.iterrows():
    with open(texts_dir / f"{row['bill_id']}_summary.txt", "w", encoding="utf-8") as f:
        f.write(row["summary_text"])
    with open(texts_dir / f"{row['bill_id']}_full_text.txt", "w", encoding="utf-8") as f:
        f.write(row["full_text"])

print(f"Text files saved to: {texts_dir}  ({len(df) * 2} files)")

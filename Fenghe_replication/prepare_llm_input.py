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

# --- assemble ---
df = pd.DataFrame(filtered_bills)
df = df.merge(df_meta, on="bill_id", how="left")
df = df.merge(df_summary, on="bill_id", how="left")
df = df.merge(df_pkgs, on="bill_id", how="left")
df = df.merge(df_html, on="package_name", how="left")

df = df.drop_duplicates(subset="bill_id").reset_index(drop=True)

# --- parse html to plain text ---
df["full_text"] = df["text_html"].apply(
    lambda x: BeautifulSoup(x, "lxml").get_text() if pd.notna(x) else None
)

# --- derive congress_term ---
df["congress_term"] = df["bill_id"].apply(lambda x: x.split("-")[1])

# --- final column selection and ordering ---
df_out = df[["bill_id", "congress_term", "introduced_at", "policy_area",
             "subjects", "official_title", "short_title",
             "summary_text", "full_text"]]

output_path = SCRIPT_DIR / "llm_input_2726_bills.csv"
df_out.to_csv(output_path, index=False)

print(f"Output shape: {df_out.shape}")
print(f"Bills with full text:    {df_out['full_text'].notna().sum()}")
print(f"Bills with summary text: {df_out['summary_text'].notna().sum()}")
print(f"Bills with neither:      {(df_out['full_text'].isna() & df_out['summary_text'].isna()).sum()}")
print(f"Saved to: {output_path}")

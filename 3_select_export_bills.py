from itertools import chain
import re
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import json
from nltk import tokenize
from tqdm import tqdm

with open("selected_bill_policies_subjects.json", 'r') as f:
    selected = json.load(f)
    selected = {k: list(set([i.lower() for i in v])) for k, v in selected.items()}

conn = sqlite3.connect("data/bill_subjects.db")
conn.executescript("attach database 'data/bill.db' as bill")
conn.executescript("attach database 'data/bill_text.db' as bill_text")
cursor = conn.cursor()
cursor.execute("select * from bill_subject")

bills = [{"bill_id": i[0], 'policy_area': i[1], 'subjects': i[2]} for i in cursor.fetchall()]

re_subjects = re.compile('|'.join(selected['subjects']))


def select_bills(nested_bills, policy_areas):
    out = []
    for i in nested_bills:
        if i['policy_area'].lower() in policy_areas:
            if bool(re_subjects.search(i['subjects'].lower())):
                out.append(i)
    return out


# len([i for i in bills if i['policy_area'].lower() in selected['policy_areas']])
selected_bills = select_bills(bills, selected['policy_areas'])

sql_selected_bills = ",".join(set([f"'{i['bill_id']}'" for i in selected_bills]))

# get bill summary text
cursor.execute(f"select bill_id, text from bill.summary where bill_id in ({sql_selected_bills})")
bill_summary_text = cursor.fetchall()

# get bill title & time
cursor.execute(f"""
select bill_id, introduced_at, official_title, short_title from bill.meta
where bill_id in ({sql_selected_bills})
""")
bill_title_time = cursor.fetchall()

# get bill raw text
cursor.execute(f"""
select bill_id, package_name from bill_text.bill_meta
where bill_id in ({sql_selected_bills})
""")
bill_pkgs = cursor.fetchall()
sql_selected_bills_pkgs = ",".join([f"'{i[1]}'" for i in bill_pkgs])

cursor.execute(f"""
select package_name, text_html from bill_text.download_data
where package_name in ({sql_selected_bills_pkgs})
""")
bill_full_text = cursor.fetchall()

dat_bills = pd.DataFrame.from_records(selected_bills)
dat_bills_titles = pd.DataFrame(bill_title_time, columns=['bill_id', 'introduced_at', 'official_title', 'short_title'])
dat_bills_summary = pd.DataFrame(bill_summary_text, columns=['bill_id', 'summary_text'])
dat_bills_pkgs = pd.DataFrame(bill_pkgs, columns=['bill_id', 'package_name'])
dat_bills_full_text = pd.DataFrame(bill_full_text, columns=['package_name', 'text_html'])

dat_bills = dat_bills.merge(dat_bills_summary, on='bill_id')
dat_bills = dat_bills.merge(dat_bills_titles, on='bill_id')
dat_bills = dat_bills.merge(dat_bills_pkgs, on='bill_id')
dat_bills = dat_bills.merge(dat_bills_full_text, on='package_name')

dat_bills['full_text'] = dat_bills['text_html'].apply(lambda x: BeautifulSoup(x, 'html').get_text())
dat_bills['congress_term'] = dat_bills['bill_id'].apply(lambda x: x.split("-")[1])
dat_bills.sort_values(by=['congress_term', 'bill_id'], inplace=True)
dat_bills.reset_index(drop=True, inplace=True)
dat_bills['subjects'].apply(lambda x: 'bank fraud' in x.lower().split("|")).sum()
dat_bills['summary_text'] = ["\n\n".join(tokenize.sent_tokenize(i)) for i in dat_bills['summary_text']]

dat_bills_2 = dat_bills.drop_duplicates(subset='bill_id')
dat_bills_2.reset_index(inplace=True, drop=True)

with open("keywords.txt", 'r') as f:
    keyword_list = f.read().lower().splitlines()
    keyword_list = [i.strip() for i in keyword_list]

re_keywords = re.compile("|".join(keyword_list))
has_keywords = []

for i in tqdm(dat_bills_2[['bill_id', 'full_text', 'summary_text']].values):
    if bool(re_keywords.search(i[2])):
        has_keywords.append(1)
    elif bool(re_keywords.search(i[1])):
        has_keywords.append(1)
    else:
        has_keywords.append(0)

dat_bills_2['has_keywords'] = has_keywords

dat_bills_2 = dat_bills_2[dat_bills_2['has_keywords'] == 1]
dat_bills_2.drop(['text_html', 'package_name'], axis=1, inplace=True)

dat_bills_2.sort_values(by=['policy_area', "introduced_at"], inplace=True)
dat_bills_2.reset_index(drop=True, inplace=True)
dat_bills_meta = dat_bills_2.drop(['full_text', 'summary_text'], axis=1)


dat_bills_meta['regulation'] = ''
dat_bills_meta['related_sentences'] = ''

dat_bills_meta[dat_bills_2['has_keywords'] == 1].to_csv("bills_meta_only --subset --has keywords.csv", index=False)

dat_bills_meta[dat_bills_2['has_keywords'] != 1].to_csv("bills_meta_only --subset --no keywords.csv", index=False)

# dat_bills_meta.groupby('congress_term').agg({"congress_term": 'count'})

for i in dat_bills_2[['bill_id', 'full_text', 'summary_text']].values:
    with open(f"selected_bill_texts/{i[0]}_summary.txt", 'w', encoding='utf-8') as f:
        f.write(i[2])
    with open(f"selected_bill_texts/{i[0]}_full_text.txt", 'w', encoding='utf-8') as f:
        f.write(i[1])


## count subjects & poclicids
#
# subject_counts = {k: 0 for k in selected['subjects']}
#
# for i in dat_bills_meta['subjects'].values:
#     subs = i.lower().split("|")
#     for j in selected['subjects']:
#         subject_counts[j] += int(bool(any(s == j for s in subs)))
# subject_counts = {k: v for k, v in subject_counts.items() if v > 0}
# subject_counts = [{"subject": k, 'count': v} for k, v in subject_counts.items()]
# subject_counts = pd.DataFrame(subject_counts)
# subject_counts.sort_values('count', ascending=False, inplace=True)
# subject_counts.to_csv("summary_subjects_count.csv", index=False)
# dat_bills_meta.groupby('policy_area', as_index=False).agg({"bill_id": 'nunique'}).to_csv("summary_policies_count.csv",
#                                                                                          index=False)

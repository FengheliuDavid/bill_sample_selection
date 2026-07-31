# Constructing the ViolationTracker Category Mapping

ViolationTracker classifies corporate violations into 10 broad `offense_group` categories and 111 finer `primary_offense` subgroups. The 111 subgroups are too granular for bill classification. We collapsed them into 27 new groups (`group_new`) following four steps.

**Step 1 — Curate subgroup summaries.** For each of the 111 subgroups, we read all case records with a non-empty `description` field and wrote a one-to-two sentence `primary_offense_summary` capturing what agency brings the action, what conduct is alleged, and what companies are typically involved.

**Step 2 — Initial grouping.** We provided Claude Code with the `offense_group`, `primary_offense`, and `primary_offense_summary` fields for all 111 subgroups and prompted it to group them into 20–30 categories organized around distinct regulatory domains and enforcing agency types.

**Step 3 — Manual review and correction.** Each subgroup was reviewed by sampling actual case descriptions, correcting both grouping decisions and VT's own misclassifications. Key changes: VT's financial offenses were split into three groups (Banking AML & Sanctions; Securities & Investor Protection; Accounting Financial Reporting & Tax); all 20 "miscellaneous offenses" subgroups were forced into substantive groups rather than an "Other" category; new groups were created where needed (e.g., Intellectual Property & Trade Secrets, Exploitation & Trafficking, Firearms Violation); and subgroups where VT's label did not match the actual cases were reassigned (e.g., "Fair Credit Reporting Act violation," nominally under employment, was moved to Consumer Protection because the cases predominantly involve credit bureaus and tenant screeners). VT's 21 environmental subgroups were initially collapsed into one Environmental Offense group; they were later split into six medium-specific groups (Air Violation, Water Violation, Earth Violation, Lead Violation, Energy Efficiency, Animal Welfare) after a subsequent reclassification step described below.

**Step 4 — Write category descriptions.** For each of the 27 final groups, we wrote a plain-language description for it. These descriptions are saved in `VT_27_categories_description.txt` and are used as the classification schema provided to the LLM when labeling state legislative bills.

The final mapping covers all 111 VT subgroups across 27 groups.

---

## Reclassifying VT's "environmental violation" Records

ViolationTracker contains 52,071 records where `primary_offense == "environmental violation"`. This label is a catch-all that VT uses when it cannot assign a more specific environmental subgroup. To improve resolution, we reclassified these records using Claude Sonnet via the Anthropic API (scripts in `Claude_identify_env_violations/`).

### Why a separate step

VT's 20 environmental subgroups (air pollution violation, water pollution violation, hazardous waste violation, etc.) are populated for only a subset of cases. The remaining 52,071 were left under the generic "environmental violation" label, making them uninformative for bill classification.

### Approach

1. **Filter records with a description.** Of the 52,071 env-violation records, 26,746 had a non-empty `description` field. Only these were sent to the LLM; records without a description cannot be reclassified.

2. **Deduplicate on (agency, description).** The 26,746 records reduce to 4,410 unique (agency, description) pairs — an 83.5% reduction in API calls.

3. **Batch classify with prompt caching.** Records were batched 10 per API call (~441 calls) with the system prompt cached (`cache_control: ephemeral`) to minimize cost (estimated ~$0.60 total). The target taxonomy matched VT's existing 19 environmental subgroup labels plus "environmental violation" as a fallback.

4. **Merge back.** Classifications were merged back to the full 26,746 records via `unique_id`, then into the full ViolationTracker dataset as a new column `primary_offense_modified`. All non-environmental records have `primary_offense_modified == primary_offense`.

### Outcome

| Group | Count | Share of 52,071 |
|---|---|---|
| Reclassified to a specific subcategory | 21,401 | 41.1% |
| Still "environmental violation" — no description (not sent to LLM) | 25,325 | 48.6% |
| Still "environmental violation" — LLM returned fallback (too vague) | 5,345 | 10.3% |
| **Total** | **52,071** | **100%** |

### Output files

| File | Description |
|---|---|
| `Claude_identify_env_violations/VT_env_violation_classified.csv` | 26,746 rows: `unique_id` + `primary_offense_new` (LLM-assigned label) |
| `Claude_identify_env_violations/checkpoint.json` | Cached LLM results keyed by (agency, description); allows resuming if interrupted |
| `ViolationTracker_basic_24jun2024_modified.csv` | Full ViolationTracker dataset (646,469 rows) with `primary_offense_modified` appended as column 51; all original columns unchanged |

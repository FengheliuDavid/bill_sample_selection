# 1-Step vs 2-Step LLM Classification: Comparison

**Date:** 2026-07-31
**Purpose:** Compare the original single-pass Qwen→GPT/Sonnet/Opus pipeline (07_31 run) against
the new two-step pipeline (step-1 simple Qwen pre-filter → step-2 GPT-4o/Sonnet/Opus with
detailed rules), and additionally test whether including Qwen's step-1 flagging reason as
context in the step-2 prompt materially affects results.

---

## Pipeline Overview

### 1-Step Approach (07_31, `compare_bills_07_31_3model.py`)
- Qwen runs on 5,000 bills using the **full detailed prompt** (`8_llm_categorize_VT27_bills_prompt_07_31.md`)
- Bills Qwen flags go directly to GPT-4o, Claude Sonnet, and Claude Opus for second-pass verification, using the same detailed prompt
- **140 bills** passed Qwen's first filter
- Manual review triggered on GPT-4o vs Opus disagreements

### 2-Step Approach with Reason (07_31 step2, `compare_206bills_07_31_step2.py`)
- Qwen runs on 5,000 bills using a **simplified step-1 prompt** designed to minimize false negatives (looser criteria, casts a wider net)
- Bills Qwen flags go to GPT-4o, Claude Sonnet, and Claude Opus for second-pass verification using `prompt_step2_gpt.md`, which applies the full detailed rules **and passes Qwen's step-1 flagging reason** to the verifier as context
- **206 bills** passed the step-1 filter (66 more than the 1-step approach)

### 2-Step Approach without Reason (07_31 step2b, `compare_206bills_07_31_step2b.py`)
- Same simplified Qwen step-1 pre-filter; same 206-bill input pool
- Same three-model step-2 verification with `prompt_step2_gpt.md` and full detailed rules, but **Qwen's step-1 flagging reason is NOT passed** to the verifiers
- Isolates the effect of the reason context on model agreement

---

## Results Comparison

### Flagging Counts

| Metric | 1-Step (140 bills) | 2-Step w/ reason (206 bills) | 2-Step no reason (206 bills) |
|---|---|---|---|
| Input pool (after Qwen/step-1) | 140 | 206 | 206 |
| GPT-4o flagged | 104 (74.3%) | 114 (55.3%) | 80 (38.8%) |
| Sonnet flagged | 128 (91.4%) | 104 (50.5%) | 114 (55.3%) |
| Opus flagged | 124 (88.6%) | 107 (51.9%) | 103 (50.0%) |
| **All-model agree** | **107 / 140 (76.4%)** | **169 / 206 (82.0%)** | **156 / 206 (75.7%)** |

### GPT-4o vs Sonnet Disagreements

| Metric | 1-Step | 2-Step w/ reason | 2-Step no reason |
|---|---|---|---|
| GPT vs Sonnet disagree | 27 / 140 **(19.3%)** | 28 / 206 **(13.6%)** | 40 / 206 **(19.4%)** |
| GPT=flag, Sonnet=reject | 1 | 19 | 3 |
| GPT=reject, Sonnet=flag | 26 | 9 | 37 |

### GPT-4o vs Opus Disagreements

| Metric | 1-Step | 2-Step w/ reason | 2-Step no reason |
|---|---|---|---|
| GPT vs Opus disagree | 24 / 140 **(17.1%)** | 17 / 206 **(8.3%)** | 29 / 206 **(14.1%)** |

### Any-Model Disagreements (all 3 models)

| Metric | 1-Step | 2-Step w/ reason | 2-Step no reason |
|---|---|---|---|
| Any model disagrees | 33 / 140 (23.6%) | 37 / 206 (18.0%) | 50 / 206 (24.3%) |
| All 3 confirm as qualifying | 101 | 89 | 74 |
| All 3 confirm as non-qualifying | 6 | 80 | 82 |
| Sent to manual review | 24 → `manual_review_07_31_GPT_vs_Opus_24.xlsx` | 17 → `manual_review_07_31_2step_with_reason_GPT_vs_Opus_17.xlsx` | 29 → `manual_review_07_31_2step_wo_reason_GPT_vs_Opus_29.xlsx` |

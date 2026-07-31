# Qwen3.6-27B vs Gemma 4 31B — Cat 1 Classification Comparison

**Sample:** 1,000-bill stratified sample (`INPUT/SAMPLE_1000/`)
**Prompt:** `8_llm_categorize_VT27_bills_prompt_06_29.md`
**Qwen run:** `llm_bill_VT27_category_outputs_sample1000_06_29_qwen/` (job 1405830–1405834)
**G4 run:** `OUTPUT/llm_bill_VT27_merged_06_27_g4.csv` (job 1398675 / 1403868 series)

---

## Overall Agreement

| Metric | Value |
|---|---|
| Bills in comparison | 1,000 |
| **Agreement rate** | **99.2%** |
| Both flag Cat 1 | 23 |
| Neither flags Cat 1 | 969 |
| Qwen only | 1 |
| G4 only | 7 |
| **Total disagreements** | **8** |
| Parse errors (Qwen) | 0 |
| Parse errors (G4) | 0 |

## Cat 1 Flagging Rate

| Model | Cat 1 flags | Rate |
|---|---|---|
| Qwen3.6-27B | 24 / 1,000 | 2.4% |
| Gemma 4 31B | 30 / 1,000 | 3.0% |

Qwen is slightly more conservative. Among the 23 agreed Cat 1 bills, `bill_type` assignments match perfectly (22 `enforcement`, 1 `tax_credit_introduction` — identical between both models).

---

## Disagreements

### G4 flags Cat 1 — Qwen does not (7 bills)

These represent cases where Gemma 4 includes the bill and Qwen excludes it.

| Bill | G4 bill_type | G4 reasoning | Qwen reasoning | Assessment |
|---|---|---|---|---|
| **hr5207-111** | enforcement | ESOP rules modify ERISA retirement benefit plans governed by ERISA and IRC | "General tax and family policy measures rather than regulations enforcing private employer wage/benefit obligations" | **Qwen wrong** — ESOPs are explicitly ERISA retirement plans; prompt covers "mismanaging or looting employee pension, 401k, or retirement benefit plans" |
| **s2766-111** | enforcement | Amends ERISA and PHSA to mandate private group health plans cover medically necessary foods | Misread as primarily addressing Medicare/Medicaid/CHIP/TRICARE | **Qwen wrong** — bill amends ERISA directly; prompt covers employer-sponsored group health plan obligations |
| **hr4931-107** | enforcement | Makes permanent pension/retirement provisions of EGTRRA, establishing lasting ERISA regulatory framework | "General tax policy and individual retirement savings rather than regulating private employer wage/benefit obligations" | **Borderline** — Qwen conflates employer pension obligations (ERISA-covered) with individual IRA savings (not covered); pension provisions should qualify |
| **s393-108** | tax_credit_introduction | Tax credit for employers who retain employees participating in military reserve components | "General hiring tax credit … explicitly excluded as it incentivizes hiring decisions" | **Borderline/Qwen misapplies** — the prompt's exclusion covers "hiring workers from specific groups"; this credit is for *retaining* existing employees during military leave, which the prompt lists as a qualifying example |
| **hr1656-115** | tax_credit_introduction | Tax credit and exclusions incentivizing employers to provide student loan repayments as employee benefits | "General tax or family policy benefits rather than credits tied to private employer wage/benefit obligations" | **Borderline** — student loan repayment as employer-provided benefit is analogous to employer-provided training (which the prompt says qualifies), but not clearly covered |
| **hr2083-114** | enforcement | Whistleblower protections against retaliation for employees of private Medicare-participating hospitals | "Medicare reimbursement conditions and patient safety standards … excluded as Medicare payment rate adjustment" | **Borderline** — private hospital employees are covered by whistleblower retaliation protections; Qwen over-applies the Medicare exclusion |
| **hr7003-110** | enforcement | Prohibits employment discrimination and reprisal against wounded veterans by non-governmental employers | "Employment discrimination law rather than wage, hour, or benefit obligations" | **Qwen may be right** — this is more naturally Cat 2 (Employment Discrimination) than Cat 1; G4 may be over-flagging |

### Qwen flags Cat 1 — G4 does not (1 bill)

| Bill | Qwen bill_type | Qwen reasoning | G4 reasoning | Assessment |
|---|---|---|---|---|
| **hr5269-107** | enforcement | Universal health insurance framework mandates comprehensive coverage standards and explicitly modifies employer-provided benefit obligations | (did not flag) | **Borderline** — the bill modifies employer-sponsored coverage requirements, which is ERISA-adjacent, but a universal healthcare bill's primary subject is broader than private employer misconduct |

---

## Root Cause Analysis

**Pattern:** Qwen correctly understands the exclusion rules but over-applies them, particularly for ERISA-governed plans.

1. **ERISA blind spot:** For bills regulating ESOPs, employer pension provisions, and employer-sponsored health plans, Qwen labels them "general tax policy" rather than recognizing them as employer plan obligations governed by ERISA. The prompt explicitly names ERISA and gives "strengthening ERISA fiduciary duties" as an example — but Qwen doesn't connect ESOP/pension bills to this framing.

2. **Over-applying the hiring-credit exclusion:** The prompt excludes "credits for hiring workers from specific groups" but explicitly includes "credits for employers who retain workers called up for military reserve duty." Qwen treats `s393-108` (retain military reservists) as a hiring credit rather than a retention/benefit credit.

3. **Medicare bill conflation:** For `s2766-111` and `hr2083-114`, Qwen triggers on the presence of Medicare/Medicaid and applies the Medicare exclusion even when the bill's primary subject is ERISA health plan mandates or private-employer whistleblower protections.

---

## Prompt Improvement Suggestion

Add a clarifying note after the ERISA sentence (line 10 of the prompt):

> ESOPs, 401(k) plans, defined-benefit pension plans, and employer-sponsored group health and welfare plans governed by ERISA are private employer benefit obligations — bills that regulate, modify, or make permanent the rules governing these plans qualify even when structured as tax provisions, as long as the employer (not the government or individual) bears the primary obligation.

---

## Speed Comparison

| | Qwen3.6-27B | Gemma 4 31B |
|---|---|---|
| Prompt eval | ~1,200 tok/sec | ~3.5 tok/sec |
| Generation | ~43 tok/sec | ~1.0 tok/sec |
| Per-bill time (est.) | ~15s | ~290s |
| Speedup | **~20×** | — |
| Thinking mode | Disabled (ChatML pre-fill) | Disabled (chat_format=None) |

---

## Recommendation

Qwen3.6-27B is a suitable replacement for Gemma 4 31B for the full 90k-bill run:
- 99.2% agreement on Cat 1 flags
- Perfect `bill_type` agreement on all agreed Cat 1 bills
- ~20× faster, enabling the full run in hours rather than weeks
- 0 parse errors after fixing the thinking-mode issue

The 6 genuine disagreements (excluding `hr7003-110` where Qwen may be correct) stem from a fixable ERISA interpretation gap in the prompt rather than a fundamental model difference.

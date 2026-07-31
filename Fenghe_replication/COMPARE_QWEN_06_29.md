# Model Comparison: Qwen vs GPT-4o vs Claude Sonnet
**Prompt:** `8_llm_categorize_VT27_bills_prompt_06_29.md`
**Input:** 124 bills flagged by Qwen from the 5,000-bill sample
**Output:** `GPT_identify_bills/OUTPUT/llm_bill_VT27_compare_06_29.csv`

---

## Overall Counts

| Model | Flagged / 124 | % of Qwen's set |
|---|---|---|
| Qwen | 124 | 100% (pre-selected) |
| Claude Sonnet | 91 | 73% |
| GPT-4o | 56 | 45% |
| **All 3 agree (YES)** | **49** | **40%** |

### Agreement Patterns

| Pattern | Count |
|---|---|
| All 3 agree YES | 49 |
| Qwen + Sonnet, GPT-4o rejects | 42 |
| Qwen + GPT-4o, Sonnet rejects | 7 |
| Qwen only — both others reject | 26 |

---

## High-Confidence Set: All 3 Models Agree (49 bills)

These bills are the most reliable true positives under the 06_29 prompt. They include clear FLSA/ERISA/FMLA/WARN enforcement bills and well-defined tax credit introductions.

| bill_id | bill_type | title (truncated) |
|---|---|---|
| hr5701-114 | enforcement | FLSA equal pay remedies |
| hr137-108 | enforcement | ERISA pension protections |
| hr3925-115 | enforcement | Wage obligations |
| s1832-114 | enforcement | Wage/hour |
| hr3441-115 | enforcement | Wage/hour |
| hr1338-110 | enforcement | Paid family leave |
| hr475-109 | enforcement | Wage/hour |
| s538-116 | enforcement | Wage/hour |
| s1861-115 | enforcement | Automatic IRA employer mandate |
| s2088-108 | enforcement | FLSA wage discrimination |
| hr4523-115 | enforcement | Auto-contribution retirement plans |
| hr454-108 | tax_credit_introduction | National Guard/reservist employer credit |
| hr2271-115 | enforcement | Flexible work scheduling |
| s1242-115 | enforcement | Federal minimum wage increase |
| s2208-114 | enforcement | Employee medical leave |
| hr3922-114 | enforcement | ERISA fiduciary best interest standard |
| s1948-112 | tax_credit_introduction | Apprenticeship program credit |
| hr1406-113 | enforcement | FLSA compensatory time |
| s1548-116 | enforcement | Corporate lockout tax penalty |
| s2526-115 | enforcement | ERISA retirement plan requirements |
| s846-109 | enforcement | Federal minimum wage |
| s2514-110 | enforcement | Federal minimum wage |
| s1062-109 | enforcement | Federal minimum wage |
| hr3991-111 | enforcement | Paid sick leave (contagious illness) |
| hr5182-106 | enforcement | Day laborer wage protections |
| hr5902-111 | enforcement | FLSA minimum wage/overtime exemptions |
| s1778-115 | tax_credit_introduction | Employer wage/benefit quality tax credit |
| s3877-111 | enforcement | FLSA statute of limitations tolling |
| s2190-107 | enforcement | ERISA pension disclosure |
| s1651-113 | tax_credit_introduction | Manufacturing job training accounts |
| hr6422-109 | enforcement | FLSA minimum wage |
| hr6025-110 | enforcement | FLSA compensatory time |
| hr6211-112 | enforcement | FLSA minimum wage |
| s2070-114 | enforcement | FLSA equal pay |
| s563-112 | enforcement | COBRA domestic partner expansion |
| hr1890-115 | enforcement | FLSA equal pay / anti-retaliation |
| s2122-115 | enforcement | FLSA nursing break time |
| hr1982-107 | enforcement | FLSA compensatory time |
| s18-107 | enforcement | FMLA expansion + childcare tax credit |
| hr1990-107 | enforcement | FMLA employer coverage expansion |
| hr1303-115 | enforcement | H-1B/offshoring employer liability |
| hr2794-114 | tax_credit_introduction | Adult literacy training credit |
| s2946-108 | tax_credit_introduction | Small employer health insurance credit |
| hr4820-106 | enforcement | ERISA pension advocacy office |
| s1737-113 | enforcement | Federal minimum wage |
| hr4177-106 | enforcement | FLSA minimum wage |
| hr4740-108 | enforcement | WARN Act offshoring expansion |
| s857-113 | enforcement | FMLA family relationship expansion |
| hr2460-111 | enforcement | Paid sick time mandate |

---

## Qwen + Sonnet Agree, GPT-4o Rejects (42 bills)

GPT-4o is noticeably more conservative than Sonnet. Its rejections fall into recognizable patterns:

### Group A: ERISA Group Health Plan Coverage Mandates (15 bills)

Sonnet reads bills that amend ERISA to require specific health coverage as direct employer benefit obligations. GPT-4o consistently treats these as **health policy** rather than private employer wage/benefit conduct.

| bill_id | title (truncated) | Sonnet rationale |
|---|---|---|
| s1235-111 | Public Health Act / ERISA medical treatment | Amends ERISA to mandate group health plan coverage |
| s889-107 | Managed care / patient rights | Amends ERISA group health plan requirements |
| hr1531-113 | Minimum hospital stay (breast cancer) | ERISA group health plan obligation |
| hr1809-107 | Cancer screening coverage | ERISA group health plan mandate |
| hr2931-110 | Bone density testing | ERISA group health plan mandate |
| hr3584-111 | Coverage reinstatement | Employer group health notice/reinstatement rules |
| hr1674-107 | Emergency medical services coverage | ERISA group health plan |
| hr2095-108 | Childhood immunizations | ERISA group health plan mandate |
| s331-107 | Breast reconstruction coverage | ERISA/IRC group health plan requirements |
| s186-108 | Living organ donor nondiscrimination | ERISA group health plan prohibition |
| hr568-107 | Fertility / impotency coverage parity | ERISA group health plan parity |
| hr2021-108 | Cancer clinical trial coverage | ERISA group health plan mandate |
| s688-111 | Minimum hospital stay (breast cancer) | ERISA group health plan mandate |
| s406-109 | ERISA association health plans | ERISA employer health plan framework |
| hr4242-112 | ACA repeal / group health reforms | Modifies employer group health obligations |

**Why the split:** GPT-4o's threshold is that the bill must address *what the employer pays or owes workers*, not just *what the insurance plan must cover*. Sonnet accepts ERISA health plan mandates as employer obligations because ERISA is an employer-obligations statute. The 06_29 prompt explicitly added "failing to provide or maintain employer-sponsored group health or welfare benefit plans as required by law" as a qualifying conduct type — Sonnet applies this; GPT-4o still leans toward the healthcare-access framing.

---

### Group B: Immigration Bills with Employer Wage/Labor Compliance Provisions (5 bills)

These are primarily immigration reform bills that contain meaningful employer wage and labor protections. GPT-4o focuses on the immigration framing; Sonnet extracts the employer obligation provisions.

| bill_id | title (truncated) | Employer provision Sonnet identified |
|---|---|---|
| s2612-109 | Comprehensive immigration reform | Prohibits hiring unauthorized aliens; enforces wage obligations |
| hr4262-108 | Earned adjustment / immigration | Requires labor attestations; employer wage protections for temp workers |
| s2010-108 | National security / immigration | Employer wage/hour protections for H-2B/H-2C workers |
| hr4224-115 | Foreign crewmen on fishing vessels | Enforceable labor agreements with wage provisions |
| s2377-109 | Immigration enforcement / employment verification | Employment verification + civil penalties for wage violations |

**Why the split:** GPT-4o applies a strict "central purpose" test — if the bill's title is immigration, it doesn't qualify. Sonnet examines the specific employer-obligation provisions embedded in the bill text.

---

### Group C: FLSA Enforcement in Specific Sectors or Contexts (9 bills)

Bills that amend the FLSA or analogous statutes for particular worker groups or fact patterns. GPT-4o rejects them as sector-specific safety/regulatory bills; Sonnet correctly connects them to FLSA wage/hour obligations.

| bill_id | title (truncated) | Connection Sonnet found |
|---|---|---|
| hr2674-110 | Child labor FLSA amendments | Increases FLSA penalties; eliminates exemptions for hazardous work |
| s404-108 | Child modeling FLSA | Amends FLSA to prohibit exploitative child modeling employment |
| hr3000-109 | National health service | FLSA amendment providing paid leave for medical care |
| hr2651-116 | School food service training | Mandates paid working hours for required training |
| s141-107 | Pipeline safety / whistleblower | Prohibits retaliation for reporting wage/safety violations |
| hr6182-109 | Patient handling safety | Prohibits retaliation against healthcare employees |
| hjres37-115 | Contractor labor compliance rule | Nullifies rule requiring federal contractors to disclose labor violations |
| hr506-114 | Automatic IRA expansion | Mandates private employers to establish IRA arrangements |
| s3236-112 | USERRA / servicemember rights | Prohibits mandatory arbitration of USERRA employment disputes |

---

### Group D: Veteran/Reservist Employer Health Coverage Obligations (3 bills)

Bills requiring private employers to continue health benefits for military reservists or veterans. GPT-4o sees these as veteran/military benefit bills; Sonnet focuses on the private employer obligation.

| bill_id | title (truncated) | Employer obligation |
|---|---|---|
| hr466-111 | Veterans' employment rights | Employers must retain benefits and seniority during medical treatment |
| hr2572-109 | Employer health coverage for reservist dependents | Requires private employers to continue dependent health coverage |
| hr5392-113 | ACA employer mandate / agricultural seasonal workers | Redefines full-time employee threshold for agricultural employers |

---

### Group E: Employer Tax Credits for Health/Benefit Provision (5 bills)

Qwen and Sonnet agree these are `tax_credit_introduction` bills. GPT-4o rejects them as general health policy rather than wage/benefit incentives.

| bill_id | title (truncated) | Credit type |
|---|---|---|
| s2558-109 | Catastrophic health cost tax credit | Employers absorb catastrophic employee health costs |
| hr2082-107 | Small business health plan tax incentives | Credits for providing employee health insurance |
| s16-109 | Health care coverage cost reduction | Refundable credit for small employer health insurance costs |
| s39-113 | Workplace wellness program credit | Tax credit for employer wellness programs |
| hr3235-110 | Nanotechnology training credit | Tax credit for employer-sponsored training expenses |

---

### Group F: ERISA Fiduciary, Disclosure, and Plan Administration (5 bills)

Bills that tighten ERISA obligations around disclosure, fiduciary duty, or plan administration. GPT-4o reads these as administrative/tax rather than enforcement.

| bill_id | title (truncated) | ERISA obligation |
|---|---|---|
| hr677-112 | ERISA lifetime income disclosure | Mandates new pension plan disclosures to participants |
| s1677-107 | ERISA fiduciary safe harbor | Modifies fiduciary standards for investment advisers |
| s952-113 | Church pension plan ERISA rules | ERISA-related rules including preempting state wage garnishment |
| hr1270-108 | Employee leasing organization employer status | Clarifies employer tax/benefit responsibilities |
| hr2034-108 | SS taxes on unreported tips | Modifies employer liability for tip income taxes |

---

## Qwen + GPT-4o Agree, Sonnet Rejects (7 bills)

A small group where Sonnet is the outlier. These tend to be borderline cases.

| bill_id | bill_type | Sonnet's rejection rationale |
|---|---|---|
| s2958-113 | tax_credit_introduction | Modifies existing differential wage payment credit — Sonnet sees it as modifying rather than introducing |
| s2240-110 | enforcement | Volunteer firefighter job protection — Sonnet sees this as about volunteer status, not wage/hour misconduct |
| s3760-111 | enforcement | Automatic IRA — Sonnet reads this as primarily a tax arrangement, not a direct employer obligation |
| hr4637-115 | tax_credit_introduction | SIMPLE IRA/retirement credit — Sonnet focuses on the tax mechanics, not employer benefit obligation |
| hr4095-108 | enforcement | FMLA + Medicare bill — Sonnet anchors on the Medicare side; GPT-4o sees the FMLA employer provision |
| hr1534-112 | enforcement | ERISA pension disclosure — Sonnet reads as administrative; GPT-4o flags as ERISA employer obligation |
| hr6293-114 | enforcement | Salary history ban — Sonnet says this governs hiring practices, not wage/hour obligations |

---

## Qwen Only — Both Others Reject (26 bills)

These are Qwen's false positives. Both GPT-4o and Sonnet agree they don't qualify. They fall into clear categories:

### Group 1: Health Insurance Mandate Bills — No Employer Wage Obligation (11 bills)

These mandate what health insurance plans must cover. Neither the employer's wage practice nor ERISA benefit plan management is the primary subject. The 06_29 prompt explicitly excludes bills whose "primary subject is something other than private employer wage, hour, or benefit conduct."

| bill_id | title (truncated) |
|---|---|
| hr118-109 | Small business health insurance refundable tax credit (general eligibility) |
| s255-107 | Mastectomy / breast cancer minimum hospital stay |
| hr1409-115 | Cancer drug coverage requirements |
| s710-107 | Colorectal cancer screening coverage |
| hr2866-114 | Special enrollment for pregnant women |
| hr1600-114 | Prescription drug co-payment limits |
| s173-109 | Medicare / group health plan immunosuppressive drugs |
| s2964-106 | General health insurance tax incentives (individuals and small employers) |
| s2551-109 | Prompt payment requirements for health care claims |
| hr3046-113 | Small employer health insurance tax credit (eligibility modification) |
| hr6444-110 | Universal health care coverage / national program |

**Qwen's error pattern:** Qwen flags any bill touching ERISA or group health plans; it does not apply the "central purpose" test. Health insurance mandate bills are primarily insurance regulation, not employer wage/benefit enforcement.

---

### Group 2: Veterans / Military Employer Obligations — Government-Adjacent (4 bills)

These involve veteran reemployment or reservist rights, but the government is the primary actor or the employer obligation is secondary to the military/VA benefit framing.

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| hr1774-113 | Veteran reemployment rights (medical treatment) | USERRA-based right; government/military context primary |
| hr3202-108 | Employer health coverage for military reservists | Addresses military-activated employees; government context |
| s1238-113 | Student loan rates + pension distribution rules | Pension piece is minor; primary subject is student loans |
| hr2574-113 | Student loan rates + pension distribution rules | Same as above |

---

### Group 3: Sector-Specific Employer Rules — Not FLSA/ERISA/WARN/FMLA (4 bills)

These impose requirements on employers in specific industries through non-wage statutes. The employer obligations exist but fall outside the scope of the Violation Tracker category.

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| hr2175-110 | Jockey / horseracing personnel insurance | Industry-specific insurance requirement; not FLSA/ERISA |
| hr4844-114 | Commercial motor vehicle driver hours-of-service | DOT safety regulation, not wage/hour statute |
| hr4503-109 | MSPA mediation (agricultural workers) | Mediation procedure; not direct wage/hour enforcement |
| hr1373-113 | Mine safety and health regulations | MSHA safety statute; not FLSA/ERISA/WARN/FMLA |

---

### Group 4: Federal Contractor / Offshoring Conditions — Not Direct Employer Obligations (2 bills)

These condition federal assistance or contractor eligibility on employment behavior but don't directly regulate private employer wage/benefit conduct.

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| hr3888-108 | Prohibit federal assistance to businesses that offshore disproportionately | Conditions on assistance, not direct WARN/FLSA obligation |
| s2997-110 | Maritime Administration reauthorization | Maritime industry bill; wage mention is incidental |

---

### Group 5: Technical Tax / Pension Administration (3 bills)

These adjust administrative or tax mechanics of pension/retirement programs without directly regulating employer conduct toward workers.

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| s689-111 | Church pension plan tax and regulatory treatment | Technical tax treatment; not employer benefit misconduct |
| hr2167-110 | Payroll deposit IRA tax incentives | IRA facilitation; employer obligation is ministerial |
| hr6617-110 | English literacy / employer and teacher tax credits | Education-focused; employer wage connection is incidental |

---

### Group 6: Civil Rights / Anti-Discrimination — Not Wage/Hour (2 bills)

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| hr1910-108 | Genetic nondiscrimination (GINA) | Employment discrimination statute, not wage/hour/ERISA |
| s351-109 | Mandatory overtime limits for nurses (Medicare facilities) | Medicare-funded facilities; government reimbursement context |

---

## Summary: Why Models Disagree

| Issue | GPT-4o | Claude Sonnet | Qwen |
|---|---|---|---|
| ERISA health plan mandates | Sees as health policy | Accepts as employer benefit obligation | Accepts broadly |
| Immigration bills w/ labor provisions | Focuses on immigration framing | Extracts embedded employer provisions | Accepts broadly |
| Sector-specific hours/safety bills | Rejects (non-wage statute) | Sometimes accepts if FLSA-linked | Accepts broadly |
| Veteran/reservist employer obligations | Rejects (government/military framing) | Accepts private employer requirement | Accepts broadly |
| General health insurance credits | Rejects | Rejects | Often accepts incorrectly |
| Central-purpose test | Applies strictly | Applies moderately | Applies loosely |

**Bottom line:**
- The **49-bill all-agree set** is the cleanest true-positive core.
- The **42 Qwen+Sonnet bills** (GPT-4o rejects) are mostly defensible under the 06_29 prompt, particularly the ERISA group health plan bills and immigration-embedded employer protections. These deserve human review.
- The **26 Qwen-only bills** are predominantly false positives driven by Qwen's loose application of the "central purpose" test and its tendency to flag any bill mentioning ERISA or wages without checking the primary subject.

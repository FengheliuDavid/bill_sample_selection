# Model Comparison: Qwen vs GPT-4o vs Claude Sonnet
**Prompt:** `HPC/8_llm_categorize_VT27_bills_prompt_07_02.md`
**Input:** 133 bills flagged by Qwen from the 5,000-bill sample
**Output:** `GPT_identify_bills/OUTPUT/llm_bill_VT27_compare_07_02.csv`

---

## Overall Counts

| Model | Flagged / 133 | % of Qwen's set |
|---|---|---|
| Qwen | 133 | 100% (pre-selected) |
| Claude Sonnet | 116 | 87% |
| GPT-4o | 82 | 62% |
| **All 3 agree (YES)** | **79** | **59%** |

### Agreement Patterns

| Pattern | Count |
|---|---|
| All 3 agree YES | 79 |
| Qwen + Sonnet, GPT-4o rejects | 37 |
| Qwen + GPT-4o, Sonnet rejects | 3 |
| Qwen only — both others reject | 14 |

---

## Comparison with 06_29 Run

The 07_02 prompt incorporated three targeted changes from 06_29:
1. **USERRA clarification** — added explicit carve-in for bills requiring private employers to maintain benefits/seniority for reservists or veterans (distinguishing from VA/DoD government benefit bills).
2. **Sector-specific FLSA clarification** — added language that FLSA amendments targeting specific worker groups (child labor, care workers, paid training hours) qualify even when structured around a sector.
3. **Auto-IRA example** — added "mandating that private employers without qualifying retirement plans auto-enroll employees in IRA arrangements" as an example of `enforcement`.

| Pattern | 06_29 (124 bills) | 07_02 (133 bills) | Change |
|---|---|---|---|
| All 3 YES | 49 (40%) | **79 (59%)** | +30 |
| Qwen+Sonnet, 4o rejects | 42 (34%) | **37 (28%)** | −5 |
| Qwen+4o, Sonnet rejects | 7 (6%) | **3 (2%)** | −4 |
| Qwen only — both reject | 26 (21%) | **14 (11%)** | −12 |

The USERRA and auto-IRA clarifications had the largest effect: bills like `hr466-111`, `hr2572-109`, `hr1774-113`, `s3760-111`, `hr4637-115`, and `s2858-108` all moved from split verdicts into the all-3-agree set.

---

## High-Confidence Set: All 3 Models Agree (79 bills)

| bill_id | bill_type | description |
|---|---|---|
| s1235-111 | enforcement | ERISA/PHSA group health plan treatment mandates |
| hr5701-114 | enforcement | FMLA expansion to additional family members |
| hr137-108 | enforcement | WARN Act notice requirements |
| s2958-113 | tax_credit_introduction | Employer differential wage payment credit expansion |
| hr1774-113 | enforcement | USERRA reemployment rights (medical treatment) |
| hr3925-115 | tax_credit_introduction | Employer wage/benefit quality tax credit |
| s1832-114 | enforcement | Federal minimum wage increase |
| hr3441-115 | enforcement | Joint employer standard under FLSA |
| hr1338-110 | enforcement | FLSA equal pay / anti-retaliation (Fair Pay Act) |
| hr475-109 | enforcement | FMLA family relationship expansion |
| s538-116 | tax_credit_introduction | Employer worker training expenditure credit |
| hr4262-108 | enforcement | Earned adjustment / H-1B employer wage obligations |
| s1861-115 | enforcement | Auto-IRA private employer mandate |
| s2240-110 | enforcement | Volunteer firefighter job protection |
| s255-107 | enforcement | ERISA group health / minimum hospital stay (mastectomy) |
| s2088-108 | enforcement | FLSA wage discrimination remedies |
| hr4523-115 | enforcement | Auto-contribution retirement plans (private employer mandate) |
| hr454-108 | tax_credit_introduction | National Guard/reservist employer differential wage credit |
| s710-107 | enforcement | ERISA group health / colorectal cancer coverage |
| hr2271-115 | enforcement | Flexible work schedule / employee request protections |
| s1242-115 | enforcement | Federal minimum wage increase |
| s2208-114 | enforcement | Employee leave (domestic violence survivors) |
| hr3922-114 | enforcement | ERISA fiduciary best interest standard |
| s1948-112 | tax_credit_introduction | Apprenticeship / training program employer credit |
| hr2651-116 | enforcement | School food service paid training hours mandate |
| s3760-111 | enforcement | Auto-IRA private employer mandate |
| hr2572-109 | enforcement | USERRA / employer health coverage for reservist dependents |
| hr4637-115 | tax_credit_introduction | SIMPLE IRA / small employer retirement credit |
| hr2674-110 | enforcement | FLSA child labor / hazardous work penalties |
| hr466-111 | enforcement | USERRA / veteran reemployment and benefit rights |
| s2858-108 | enforcement | USERRA differential wage payment / IRC clarification |
| hr1406-113 | enforcement | FLSA compensatory time |
| s1548-116 | enforcement | Corporate lockout tax penalty |
| s2526-115 | enforcement | ERISA retirement plan requirements |
| hr1531-113 | enforcement | ERISA group health / minimum hospital stay (breast cancer) |
| s1082-115 | enforcement | WARN Act / employee purchase opportunity |
| hr3202-108 | enforcement | USERRA / employer health coverage continuation for activated reservists |
| hr1809-107 | enforcement | ERISA group health / cancer screening coverage |
| s846-109 | enforcement | Federal minimum wage increase |
| s2514-110 | enforcement | FLSA minimum wage increase |
| s1062-109 | enforcement | FLSA minimum wage increase |
| hr677-112 | enforcement | ERISA lifetime income disclosure (pension) |
| hr1534-112 | enforcement | Auto-IRA / payroll deduction IRA mandate |
| hr3991-111 | enforcement | Paid sick leave for contagious illness |
| hr5182-106 | enforcement | Day laborer wage protections |
| hr5902-111 | enforcement | FLSA direct care worker overtime exemptions |
| hr4844-114 | enforcement | FLSA/DOT hours-of-service (oilfield transport drivers) |
| s1778-115 | tax_credit_introduction | Employer wage/benefit quality tax credit |
| s3877-111 | enforcement | FLSA statute of limitations tolling |
| hr3759-113 | tax_credit_introduction | Employer differential wage payment credit extension |
| s331-107 | enforcement | ERISA/IRC group health / breast reconstruction coverage |
| s2190-107 | enforcement | ERISA pension disclosure |
| hr6422-109 | enforcement | FLSA minimum wage increase (regionalized) |
| hr2931-110 | enforcement | ERISA group health / bone density testing |
| hr6025-110 | enforcement | FLSA compensatory time |
| hr6211-112 | enforcement | FLSA minimum wage increase |
| s2070-114 | enforcement | FLSA equal pay remedies (Paycheck Fairness Act) |
| hr1890-115 | enforcement | FLSA equal pay / anti-retaliation |
| hr2095-108 | enforcement | ERISA group health / childhood immunizations |
| s404-108 | enforcement | FLSA child modeling prohibition |
| hr506-114 | enforcement | Auto-IRA private employer mandate |
| s2122-115 | enforcement | FLSA nursing break time expansion |
| hr2021-108 | enforcement | ERISA group health / cancer clinical trial coverage |
| hr1982-107 | enforcement | FLSA compensatory time |
| s18-107 | enforcement | FMLA expansion + child care tax credit |
| hr1990-107 | enforcement | FMLA employer coverage expansion |
| hr1303-115 | enforcement | H-1B/offshoring employer liability |
| hr2167-110 | enforcement | Auto-IRA small employer payroll deduction mandate |
| hr2794-114 | tax_credit_introduction | Adult English literacy employer training credit |
| s2946-108 | tax_credit_introduction | Small employer health insurance credit |
| s186-108 | enforcement | ERISA group health / living organ donor nondiscrimination |
| hr568-107 | enforcement | ERISA group health / fertility/impotency coverage parity |
| hr4820-106 | enforcement | ERISA pension participant advocacy office |
| s1737-113 | enforcement | FLSA minimum wage increase |
| s3236-112 | enforcement | USERRA / mandatory arbitration prohibition |
| hr4177-106 | enforcement | FLSA minimum wage increase |
| hr4740-108 | enforcement | WARN Act / offshoring expansion |
| s688-111 | enforcement | ERISA group health / minimum hospital stay (breast cancer) |
| hr2460-111 | enforcement | Paid sick time mandate |

**Breakdown:** 69 enforcement, 10 tax_credit_introduction.

---

## Qwen + Sonnet Agree, GPT-4o Rejects (37 bills)

GPT-4o remains more conservative. The remaining disagreements fall into six patterns.

### Group A: ERISA Group Health Plan Coverage Mandates (10 bills)

GPT-4o consistently reads these as health insurance or consumer-protection policy. Sonnet treats them as direct ERISA employer-as-plan-sponsor obligations. This split persists from the 06_29 run; the 07_02 prompt changes did not address it.

| bill_id | title (truncated) | Sonnet rationale |
|---|---|---|
| s889-107 | Managed care / patient rights | Amends ERISA to impose new obligations on private employers as group health plan sponsors |
| hr4242-112 | ACA repeal / group health reforms | Directly regulates private employer group health plan obligations under ERISA |
| hr1674-107 | Emergency medical services coverage | ERISA employer-sponsored group health plan mandate |
| hr1774-112 | HIV/AIDS healthcare coverage | ERISA group health plan coverage obligation |
| s2551-109 | Prompt payment of health care claims | ERISA imposes strict payment timeline obligations on employer-sponsored plans |
| hr2866-114 | Pregnant women special enrollment | New obligations on group health plans (including employer-sponsored) |
| hr1600-114 | Prescription drug co-payment limits | ERISA employer-sponsored group health plan obligation |
| hr1910-108 | Genetic nondiscrimination in group health | ERISA group health plan sponsorship obligation |
| s406-109 | ERISA association health plans | ERISA regulatory framework for employer-sponsored association health plans |
| s173-109 | Medicare / immunosuppressive drugs + group health | ERISA group health plan coverage requirement |

**Why the split persists:** GPT-4o anchors on whether the bill targets what the employer *pays or owes workers*, not what the insurance plan must *cover*. For these bills, GPT-4o sees the insurer/plan administrator as the primary regulated party. Sonnet reads ERISA health plan mandates as employer obligations because ERISA directly governs the employer's role as plan sponsor.

---

### Group B: Immigration Bills with Embedded Employer Labor Provisions (4 bills)

GPT-4o focuses on the immigration framing; Sonnet extracts specific private employer wage and labor-condition obligations embedded in the bill.

| bill_id | title (truncated) | Employer provision Sonnet identified |
|---|---|---|
| s2612-109 | Comprehensive immigration reform | Prohibits hiring unauthorized aliens; imposes employer wage protections |
| s2010-108 | National security / immigration | Employer wage/hour requirements for H-2B and H-2C workers |
| hr4224-115 | Foreign crewmen / fishing vessels | Requires private fishing companies to enter enforceable labor agreements with wage provisions |
| s2377-109 | Immigration enforcement / employment verification | Employment eligibility system + civil penalties for wage violations |

**Why the split:** GPT-4o applies a strict "central purpose" test — a bill titled as immigration reform doesn't qualify. Sonnet examines embedded employer-obligation provisions regardless of the bill's primary label.

---

### Group C: Safety, Whistleblower, and Industry-Specific Bills (8 bills)

Bills where the primary subject is safety regulation or an industry-specific statute, but Sonnet finds qualifying employer wage or retaliation protections embedded within.

| bill_id | title (truncated) | Connection Sonnet found |
|---|---|---|
| hr4824-108 | Hazardous materials transport security | Whistleblower provisions prohibiting private employer retaliation |
| s141-107 | Pipeline safety / whistleblower | Prohibits employer retaliation for reporting wage/safety violations |
| s773-109 | Transportation safety / hazmat | Whistleblower protections with wage restitution provisions |
| hr1373-113 | Mine safety and health regulations | Embedded provisions requiring employer wage restitution |
| hjres37-115 | Contractor labor compliance rule | Nullifies rule requiring federal contractors to disclose labor violations |
| hr2175-110 | Jockey / horseracing insurance | Mandates host racing associations to provide health/workers comp coverage |
| hr3264-109 | Transportation infrastructure grants | Imposes prevailing wage requirements on contractors and subcontractors |
| hr3000-109 | National health service | Amends FLSA to provide employees leave to receive national health service care |

**Why the split:** GPT-4o applies the "central purpose" test strictly: if the bill is primarily a safety or infrastructure statute, it doesn't qualify. Sonnet identifies qualifying employer-obligation clauses even when they are embedded in larger bills.

---

### Group D: ACA / Employer Mandate Context (3 bills)

Bills that modify the ACA employer mandate structure. GPT-4o sees health/insurance policy; Sonnet frames them as directly affecting private employer coverage obligations.

| bill_id | title (truncated) | GPT-4o rejection | Sonnet acceptance |
|---|---|---|---|
| hr5392-113 | ACA / agricultural seasonal worker exclusion | Modifies ACA mandate counting rules — health policy | Amends which agricultural employers must provide coverage — employer mandate |
| hr4936-114 | ACA / small business employee hour formula | Tax code / small business administrative provisions | Revises the formula determining which employees count toward ACA mandate |
| hr6444-110 | Universal health care / national program | Primarily health insurance coverage / premium subsidies | Terminates employer-sponsored coverage tax exclusions and imposes new employer obligations |

---

### Group E: Employer Tax Credits for Health, Benefits, or Training (6 bills)

Sonnet classifies these as `tax_credit_introduction`; GPT-4o rejects them as general health or education policy rather than wage/benefit incentives.

| bill_id | title (truncated) | Credit type |
|---|---|---|
| hr118-109 | Small business health insurance refundable tax credit | Credit for employers providing employee health coverage |
| s16-109 | Health care coverage cost reduction | Refundable credit for small employer health insurance costs |
| hr2082-107 | Small business health plan tax incentives | Credits for providing employee health insurance |
| hr3235-110 | Nanotechnology training credit | Credit for employer-sponsored nanotechnology education/training |
| hr5553-107 | Retirement savings / elective deferral credit | Expands and makes permanent credit for employer-match elective deferrals |
| s1651-113 | Manufacturing job training accounts | Tax-advantaged accounts for manufacturers making training investments |

**Why the split:** GPT-4o requires a closer nexus between the credit and a specific wage/benefit obligation. Sonnet accepts any credit that incentivizes employers toward qualifying conduct (health coverage provision, job training).

---

### Group F: ERISA Administrative / Fiduciary / Edge Cases (6 bills)

Bills adjusting ERISA mechanics, fiduciary standards, or employer tax treatment in ways GPT-4o reads as administrative rather than direct employer-obligation enforcement.

| bill_id | title (truncated) | ERISA obligation Sonnet identified |
|---|---|---|
| s689-111 | Church pension plan ERISA treatment | ERISA obligations governing church plan sponsors |
| s952-113 | Church plan ERISA rules / state wage preemption | Preempts state wage/payroll laws for church plan employers |
| s1677-107 | ERISA fiduciary safe harbor | Modifies ERISA fiduciary standards for investment advisers to plan sponsors |
| hr1270-108 | Employee leasing organization employer status | Clarifies ERISA employer obligations for employee leasing arrangements |
| hr2034-108 | SS taxes on unreported tips | Modifies FICA employer liability procedure for tip income |
| hr3888-108 | Federal assistance / offshoring layoffs | Imposes obligations on private employers receiving federal assistance regarding layoff practices |

---

## Qwen + GPT-4o Agree, Sonnet Rejects (3 bills)

A small group where Sonnet is the outlier — down from 7 in the 06_29 run.

| bill_id | bill_type | Sonnet's rejection rationale |
|---|---|---|
| hr4095-108 | enforcement | Primarily amends Medicare home health services; FMLA component is secondary — Sonnet anchors on the Medicare framing |
| s563-112 | enforcement | Expands COBRA continuation coverage eligibility to domestic partners but does not directly regulate employer wage or benefit obligations |
| hr6293-114 | enforcement | Prohibits salary history inquiries during hiring — Sonnet sees this as governing hiring practices rather than wage/hour obligations |

---

## Qwen Only — Both Others Reject (14 bills)

These are Qwen's false positives under the 07_02 prompt. The number dropped from 26 (06_29) to 14, largely because the prompt changes clarified qualifying conduct types. The remaining 14 fall into clear categories.

### Group 1: Health Insurance Coverage — No ERISA Employer Obligation (4 bills)

These mandate what health plans must cover, but neither the employer's wage practice nor ERISA plan sponsorship is the primary subject. Both GPT-4o and Sonnet apply the "central purpose" test correctly here.

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| hr3636-108 | Genetic nondiscrimination in health insurance (GINA) | Regulates insurance issuers, not employer wage/benefit obligations |
| hr1409-115 | Cancer drug coverage requirements | Health insurance coverage mandate; not ERISA employer obligation |
| s2964-106 | General health insurance tax incentives | General health affordability credits to individuals and small employers; not employer wage/benefit enforcement |
| hr4728-113 | ACA impact study / small business | Study bill; no employer obligation |

### Group 2: Student Loans with Incidental Pension Component (2 bills)

Qwen flags the pension distribution rules in these bills; both others correctly identify student loans as the primary subject.

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| s1238-113 | Student loan interest rates + pension distribution rules | Primary subject is student loan policy; pension piece is minor and technical |
| hr2574-113 | Student loan interest rates + pension distribution rules | Companion bill; same analysis |

### Group 3: Disaster Relief Bills (2 bills)

Hurricane tax relief bills. Both models correctly identify these as disaster relief, not private employer wage/benefit conduct.

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| hr6854-115 | Hurricane Irma/Maria tax relief | Disaster relief tax bill; employer benefits are incidental provisions for affected businesses |
| hr7166-115 | Hurricane tax relief (2017) | Same pattern |

### Group 4: Government / DOD / Medicare Facility Context (2 bills)

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| hr1435-112 | DOD contractor employee whistleblower protections | Government contracting context; DOD contractor reprisals are not private employer wage/hour misconduct under FLSA/ERISA |
| s351-109 | Mandatory overtime limits for nurses in Medicare facilities | Primarily regulates Medicare-participating healthcare facilities; Medicare-funded provider context, not private employer wage obligation |

### Group 5: Sector-Specific / Non-FLSA/ERISA / Incidental Wage Mention (3 bills)

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| hr4503-109 | MSPA mediation (agricultural workers) | Establishes mediation under Migrant and Seasonal Agricultural Worker Protection Act; not FLSA/ERISA/WARN/FMLA enforcement |
| s2997-110 | Maritime Administration reauthorization | Maritime industry bill; wage mention is incidental |
| hr6617-110 | English literacy / employer and teacher credits | Education-focused; employer wage connection is incidental |

### Group 6: Immigration with Incidental Wage Mention (1 bill)

| bill_id | title (truncated) | Why excluded |
|---|---|---|
| s2366-110 | Immigration enforcement / border security | Wage mention is only to deny tax deductions to businesses employing undocumented workers; no direct private employer wage obligation |

---

## Summary: Remaining Model Disagreements

| Issue | GPT-4o | Claude Sonnet | Qwen |
|---|---|---|---|
| ERISA health plan mandates | Sees as health/insurance policy | Accepts as employer benefit obligation | Accepts broadly |
| Immigration bills w/ labor provisions | Rejects (immigration framing primary) | Extracts embedded employer provisions | Accepts broadly |
| Safety/whistleblower bills | Rejects (non-wage primary subject) | Accepts if qualifying employer provision embedded | Accepts broadly |
| ACA employer mandate mechanics | Rejects (health policy) | Accepts as employer coverage obligation | Accepts broadly |
| Tax credits for employer health/training | Rejects (general health/education) | Accepts as `tax_credit_introduction` | Accepts broadly |
| ERISA fiduciary/admin bills | Reads as administrative | Accepts as ERISA employer obligation | Accepts broadly |
| Central-purpose test | Applies strictly | Applies moderately | Applies loosely |

**Bottom line:**
- The **79-bill all-agree set** is the cleanest true-positive core, up substantially from 49 in the 06_29 run. The prompt changes effectively resolved USERRA/reservist employer obligations, sector-specific FLSA amendments (child labor, care workers, school food service, oilfield drivers), and auto-IRA mandates.
- The **37 Qwen+Sonnet bills** (GPT-4o rejects) are concentrated in two persistent issues: ERISA group health plan mandates (Group A) and safety/sector bills with embedded employer provisions (Group C). These warrant human review if the goal is to include ERISA health plan obligations.
- The **14 Qwen-only bills** are clear false positives. Qwen continues to flag any bill mentioning ERISA, health insurance, or pensions without applying the "central purpose" test.

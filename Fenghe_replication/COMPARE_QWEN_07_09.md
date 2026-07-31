# Model Comparison: Qwen vs GPT-4o vs Claude Sonnet
**Prompt:** `HPC/8_llm_categorize_VT27_bills_prompt_07_09.md` (Sonnet) / `HPC/8_llm_categorize_VT27_bills_prompt_07_09_GPT.md` (GPT-4o)
**Input:** 141 bills flagged by Qwen from the 5,000-bill sample (2010–2019 bills only)
**Output:** `GPT_identify_bills/OUTPUT/llm_bill_VT27_compare_07_09.csv`

---

## Overall Counts

| Model | Flagged / 141 | % of Qwen's set |
|---|---|---|
| Qwen | 141 | 100% (pre-selected) |
| Claude Sonnet | 121 | 86% |
| GPT-4o | 95 | 67% |
| **All 3 agree (YES)** | **91** | **65%** |

### Agreement Patterns

| Pattern | Count |
|---|---|
| All 3 agree YES | 91 |
| Qwen + Sonnet, GPT-4o rejects | 30 |
| Qwen + GPT-4o, Sonnet rejects | 4 |
| Qwen only — both others reject | 16 |

---

## Comparison with 07_02 Run

Two changes from the 07_02 run:
1. **New sample:** 2010–2019 bills only (SAMPLE_5000_YEAR_2010_2019), instead of the unrestricted 5,000-bill sample.
2. **GPT-specific prompt:** GPT-4o now uses `prompt_07_09_GPT.md`, which adds a "DO qualify" section with explicit ERISA group health plan examples (s889-107, hr1674-107, s2551-109) and prevailing wage / contractor compliance examples (hr3264-109, hjres37-115). Sonnet uses the standard `prompt_07_09.md`.

| Pattern | 07_02 (133 bills) | 07_09 (141 bills) | Change |
|---|---|---|---|
| All 3 YES | 79 (59%) | **91 (65%)** | +12 |
| Qwen+Sonnet, 4o rejects | 37 (28%) | **30 (21%)** | −7 |
| Qwen+4o, Sonnet rejects | 3 (2%) | **4 (3%)** | +1 |
| Qwen only — both reject | 14 (11%) | **16 (11%)** | +2 |

GPT-4o's flagging rate improved from 62% to 67%, primarily because the GPT-specific prompt now explicitly validates ERISA group health plan mandates and prevailing wage bills. Several bills in those categories — including Davis-Bacon prevailing wage bills (hr3555-114, hr2821-113) — moved from the disagreement bucket into the all-3-agree set.

---

## High-Confidence Set: All 3 Models Agree (91 bills)

| bill_id | bill_type | description |
|---|---|---|
| s273-113 | enforcement | ERISA fiduciary definition / ESOP appraiser exclusion |
| hr2234-112 | enforcement | FLSA child labor / hazardous occupation restrictions |
| hr2782-116 | enforcement | ACA employer mandate / full-time employee threshold |
| hr4598-114 | enforcement | H-1B employer minimum wage requirements ($110k+) |
| hr515-113 | enforcement | FMLA bereavement leave (death of a child) |
| s1076-115 | enforcement | ERISA multiemployer pension protections |
| s4012-111 | enforcement | ERISA phased retirement / WOTC for older workers |
| hr5727-112 | enforcement | FLSA minimum wage and overtime threshold increase |
| hr1534-112 | enforcement | Auto-IRA / payroll deduction IRA private employer mandate |
| hr557-114 | enforcement | ERISA pension plan secure deferral requirements |
| s305-114 | enforcement | ACA employer mandate repeal |
| s150-112 | enforcement | COBRA continuation coverage extension for older workers |
| s2301-115 | enforcement | ERISA mental health parity disclosure requirements |
| hr2942-115 | enforcement | FLSA predictable scheduling / reporting time pay |
| hr2654-114 | enforcement | Pregnant worker reasonable accommodation mandate |
| s2122-115 | enforcement | FLSA nursing break time expansion |
| hr1619-114 | enforcement | FLSA equal pay enforcement / anti-retaliation (Paycheck Fairness) |
| s3060-114 | enforcement | ERISA / small employer health reimbursement arrangement rules |
| s3680-111 | enforcement | FMLA family relationship expansion |
| s1145-113 | enforcement | ERISA lifetime income disclosure (pension benefit statements) |
| hr4611-113 | enforcement | FLSA employee misclassification / doubled liquidated damages |
| hr366-114 | enforcement | USERRA enforcement / veteran intervention rights |
| s2048-115 | tax_credit_introduction | Employer tax credit for worker training expenditure increases |
| s1358-112 | enforcement | FMLA bereavement leave (death of a child) |
| hr2341-112 | enforcement | FLSA direct care worker overtime exemptions |
| hr1311-112 | enforcement | ERISA group health / medically necessary treatment coverage |
| hr5535-114 | enforcement | FMLA parental involvement leave expansion |
| s124-116 | enforcement | Non-compete agreement prohibition for low-wage workers |
| hr631-112 | enforcement | FLSA tipped employee base minimum wage |
| s3462-114 | enforcement | DOL overtime rule implementation delay |
| s1248-113 | enforcement | FLSA flexible work schedule / employer response obligations |
| s1341-115 | enforcement | FLSA child labor / tobacco agriculture prohibition |
| s1656-113 | enforcement | FLSA volunteer status exemption from minimum wage |
| s1386-115 | enforcement | FLSA predictable scheduling / reporting time pay |
| hr397-112 | enforcement | ERISA association health plans |
| s959-114 | tax_credit_introduction | Employer tax credit for on-site apprenticeship training |
| s180-115 | enforcement | H-1B/L-1 visa employer wage liability and penalties |
| s852-115 | enforcement | ERISA nondiscrimination / minimum participation requirements |
| hr1848-114 | enforcement | FLSA child labor / tobacco agriculture prohibition |
| hr3595-115 | tax_credit_introduction | Employer paid family and medical leave tax credit |
| hr100-113 | enforcement | Employee/retiree protections in corporate bankruptcy |
| hr2656-112 | enforcement | ERISA defined benefit plan funding requirements |
| hr4505-115 | enforcement | FLSA overtime salary threshold increase and auto-update |
| hr2095-115 | enforcement | FLSA wage discrimination / race, sex, national origin |
| hr5802-113 | enforcement | ERISA multiemployer pension withdrawal liability rules |
| s868-115 | enforcement | ERISA lifetime income disclosure (pension benefit statements) |
| hr2109-112 | enforcement | Auto-IRA / payroll deduction IRA private employer mandate |
| hr5272-114 | enforcement | RFRA limitation for employer wage/benefit obligation laws |
| s1777-115 | tax_credit_introduction | Excise tax on employers paying below 218% FPL wages |
| hr1121-115 | enforcement | ERISA group health plan / preexisting condition coverage |
| s818-116 | enforcement | FLSA child labor / logging industry exemption (weakening) |
| hr1981-114 | enforcement | FLSA overtime regular rate / bonus exclusions |
| hr4763-114 | enforcement | FLSA wage enforcement / increased damages and penalties |
| hr4591-111 | tax_credit_introduction | Employer tax credit for older workers in flexible phased retirement |
| hr5918-114 | enforcement | FLSA gig/peer-to-peer economy worker exemption (weakening) |
| hr1677-114 | enforcement | ERISA group health plan / coverage value requirements |
| hr2619-114 | tax_credit_introduction | Employer tax credit for meeting wage, health, and retirement standards |
| hr2317-114 | enforcement | ERISA retirement plan / lifetime income disclosure |
| hr5372-113 | tax_credit_introduction | Employer tax credit for meeting wage, retirement, and health standards |
| s984-112 | enforcement | Paid sick time private employer mandate |
| hr377-113 | enforcement | FLSA equal pay / sex-based wage discrimination (Paycheck Fairness) |
| hjres67-115 | enforcement | DOL rule nullification / state auto-IRA programs |
| s219-116 | tax_credit_introduction | Excise tax on employers paying below 218% FPL wages |
| s3221-112 | enforcement | NLRA / employer above-scale wages permissibility |
| s777-114 | enforcement | FLSA flexible work schedule / employer request consideration |
| s1302-113 | enforcement | ERISA cooperative / association pension plan funding standards |
| s3429-114 | enforcement | DOL overtime rule implementation delay |
| s641-114 | tax_credit_introduction | Employer differential wage payment tax credit (reservists) |
| hr2125-112 | enforcement | FLSA disclosure / protections for piece-rate workers |
| hr3555-114 | enforcement | Davis-Bacon prevailing wage / federally-assisted projects |
| hr4677-111 | enforcement | Employee/retiree wage priority in corporate bankruptcy |
| hr2881-114 | enforcement | ACA employer mandate / applicable large employer definition |
| s636-115 | enforcement | Paid sick time private employer mandate |
| s998-112 | enforcement | ERISA / PBGC pension benefit calculation for airline pilots |
| hr1827-115 | enforcement | FMLA eligibility modification for disabled veterans |
| hr3165-113 | enforcement | ERISA small business health plans |
| s1566-114 | enforcement | ERISA group health plan / dependent coverage obligations |
| s1977-112 | enforcement | FLSA maximum hours / over-the-road bus drivers |
| hr2821-113 | enforcement | Davis-Bacon prevailing wage / federally-assisted projects |
| s1317-114 | enforcement | ERISA individual account plan / lifetime income disclosure |
| hr3453-113 | enforcement | USERRA enforcement / veteran intervention rights |
| hr4092-115 | enforcement | FLSA agricultural employer wage penalties |
| s1486-114 | tax_credit_introduction | Employer tax credit for meeting wage, retirement, and health standards |
| hr438-113 | enforcement | FLSA wage discrimination / race and national origin expansion |
| s1045-112 | enforcement | ERISA group health plan / specific medical treatment coverage |
| hr1809-112 | enforcement | ERISA group health plan / transparency and value requirements |
| hr2575-114 | enforcement | FLSA minimum wage schedule / American Samoa delay |
| hr5944-111 | enforcement | FMLA eligibility / railroad employees |
| s3419-112 | enforcement | WARN Act / employee purchase opportunity obligation |
| s1321-115 | enforcement | ERISA fiduciary / investment advice standards |
| hr801-116 | tax_credit_introduction | Employer tax credit for retaining reservist employees |

**Breakdown:** 80 enforcement, 11 tax_credit_introduction.

**Notable additions vs. 07_02:** Davis-Bacon prevailing wage bills (hr3555-114, hr2821-113) now reach all-3-agree, likely reflecting the GPT-specific prompt's explicit inclusion of prevailing wage contractor obligations.

---

## Qwen + Sonnet Agree, GPT-4o Rejects (30 bills)

GPT-4o remains the most conservative model. The 30 disagreements fall into six groups.

### Group A: ERISA Health Plan / ACA Employer Mandate Mechanics (12 bills)

GPT-4o reads these as health or insurance policy. Sonnet treats them as direct ERISA employer-as-plan-sponsor obligations or ACA employer mandate modifications.

| bill_id | description |
|---|---|
| hr4143-112 | Extends the period during which private employers may transfer surplus defined benefit pension assets to fund retiree health accounts, and adds retiree group term life insurance as an eligible transfer destination; modifies ERISA rules governing employer management and disposition of excess pension assets |
| hr3910-115 | Amends the IRC to make lifetime income products and managed account options in employer-sponsored defined contribution plans portable when those investment options are removed from a plan menu; modifies employer plan administration and fiduciary obligations under ERISA-related tax provisions |
| hr3656-112 | Amends the IRC to allow qualified employer retirement plans to offer death and disability protection on outstanding participant loans; modifies the terms and conditions of qualified employer plan loan programs under ERISA-related tax provisions |
| s143-112 | Clarifies ERISA and IRC treatment of church pension plans, including applying automatic enrollment provisions and contribution/benefit limits to church-sponsored plans; modifies substantive regulatory obligations of churches and church-affiliated organizations as employer plan sponsors |
| s1204-113 | Allows health plan sponsors, issuers, and private employers to exclude ACA-required coverage of specific items or services based on moral or religious convictions; directly modifies employer obligations to provide comprehensive group health coverage under ERISA and the ACA employer mandate |
| hr628-115 | Preserves ACA provisions guaranteeing availability of health coverage and prohibiting preexisting condition exclusions in group health markets; maintains employer-sponsored group health plan obligations to accept all applicants and cover preexisting conditions under ERISA-related statutes |
| hr1423-114 | Amends ERISA, PHSA, and IRC to exclude medical stop-loss insurance obtained by self-insured plan sponsors from the definition of "health insurance coverage"; modifies regulatory treatment of self-insured employer-sponsored group health plans and reduces compliance burden on employers who self-fund employee benefits |
| hr364-112 | Repeals the ACA and replaces it with provisions including ERISA-based small business health plans; maintains employer-sponsored group health plan obligations such as dependent coverage to age 26 while eliminating employer mandate penalties and reshaping employer benefit obligations |
| s254-114 | Repeals ACA employer shared responsibility provisions, eliminating employer mandate penalties and associated IRS reporting requirements; removes the statutory obligation of applicable large employers to offer minimum essential health coverage to full-time employees |
| hr2443-113 | Exempts certain educational institutions from the ACA employer mandate by modifying how adjunct faculty teaching hours are counted toward the full-time equivalent employee threshold; reduces the scope of employer health coverage obligations for higher education employers |
| hr4616-115 | Provides a two-year moratorium on the ACA employer mandate and delays the excise tax on high-cost employer-sponsored health coverage; temporarily suspends private employer shared responsibility payment obligations and the Cadillac plan excise tax |
| hr1-113 | Comprehensive tax reform bill (Tax Reform Act of 2014) that among other provisions prohibits new SIMPLE 401(k) employer plan designs, revises tax treatment of existing employer-sponsored retirement plans, and modifies ERISA-related benefit rules embedded within a broader individual and corporate tax overhaul |

**Why the split persists:** GPT-4o anchors on the primary label of the bill (health insurance reform, ACA, tax reform) and requires the employer's direct wage or benefit obligation to be the central subject. Sonnet extracts qualifying ERISA employer-as-plan-sponsor or employer mandate provisions even when they appear within a larger bill. The GPT-specific prompt moved some ERISA health plan bills into the all-agree set (hr1311-112, hr1677-114, hr1121-115, s1045-112, hr1809-112, s1566-114, hr3165-113) but these 12 remain contested — likely because their primary framing is too distant from what the prompt's examples describe.

---

### Group B: Immigration / H-Visa Bills with Embedded Employer Wage Provisions (4 bills)

GPT-4o focuses on the immigration framing; Sonnet extracts employer H-1B wage requirements or foreign labor contractor obligations.

| bill_id | description |
|---|---|
| hr170-115 | Raises the salary threshold defining "exempt" H-1B nonimmigrants from $60,000 to $100,000 with inflation adjustments (Protect and Grow American Jobs Act); directly increases the minimum wage private employers must pay when sponsoring H-1B specialty occupation workers |
| hr2161-112 | Comprehensive immigration bill (IDEA Act of 2011) modernizing H-1B and L-1 visa programs; imposes higher prevailing wage requirements, U.S. worker non-displacement obligations, enhanced domestic recruitment requirements, and increased civil penalties on private employers who sponsor or employ foreign specialty occupation workers |
| hr3344-113 | Anti-human trafficking legislation (FORTE Act of 2013) requiring greater transparency in foreign labor contractor recruitment; prohibits contractors recruiting workers for U.S. employers from charging recruitment fees to those workers and mandates pre-recruitment disclosure of wage, benefit, and employment terms |
| hr3162-112 | Prohibits the DOL from implementing new rules that change the prevailing wage methodology used for H-2B and other alien labor certification programs; directly affects the wage floor calculations that private employers must meet to obtain labor certification approval for foreign temporary workers |

---

### Group C: Safety, Industry-Specific, and Whistleblower Bills (4 bills)

Bills where the primary subject is safety or industry regulation, but Sonnet finds qualifying employer retaliation protections or wage obligations embedded within.

| bill_id | description |
|---|---|
| s68-113 | Chemical facility security bill (Secure Chemical Facilities Act) establishing vulnerability assessment and security planning requirements; includes employee whistleblower protections prohibiting employer retaliation against workers at covered facilities who report safety violations or cooperate with enforcement proceedings |
| hr6544-111 | Creates criminal penalties for failure to warn employees of known serious product dangers (Dangerous Products Warning Act); prohibits employer retaliation against employees who report dangerous conditions or products to authorities, directly criminalizing private employer adverse action against whistleblowing employees |
| hr1926-114 | Mine safety enforcement legislation (Robert C. Byrd Mine Safety Protection Act of 2015) strengthening MSHA enforcement tools; includes a provision requiring mine operators to pay miners their full regular rate of pay for work stoppages caused by safety withdrawal orders, imposing a direct wage restitution obligation on private mine employers |
| hr6519-111 | Amends federal railroad hours-of-service statutes (Railroad Hours of Service Act of 2010) to expand coverage to yardmaster employees, increase mandatory rest periods, and impose stricter limits on consecutive duty hours; directly regulates private railroad carriers' scheduling and maximum-hours obligations toward their employees |

---

### Group D: USERRA / Military Service Employer Obligations (2 bills)

GPT-4o reads these as military arbitration or general civil rights issues; Sonnet identifies direct private employer reemployment and anti-discrimination obligations.

| bill_id | description |
|---|---|
| hr2750-116 | Amends the Federal Arbitration Act to prohibit pre-dispute mandatory arbitration agreements covering USERRA reemployment rights, anti-discrimination protections, and benefit continuation claims by servicemembers (Justice for Servicemembers Act); prevents private employers from requiring employees to waive their right to litigate USERRA disputes in federal court |
| hr2654-113 | Prohibits private employer discrimination in hiring, promotion, compensation, and other employment terms on the basis of military service status, obligations, or membership (Veterans and Servicemembers Employment Rights Act of 2013); expands USERRA-adjacent employment protections and establishes EEOC charge procedures for servicemember employment discrimination claims |

---

### Group E: Employer Tax Credits for Training and Manufacturing (5 bills)

Sonnet classifies these as `tax_credit_introduction`; GPT-4o rejects them as general economic or education policy rather than wage/benefit incentives tied to employer obligations.

| bill_id | description |
|---|---|
| s1651-113 | Allows manufacturing businesses to establish tax-free manufacturing reinvestment accounts (Manufacturing Reinvestment Account Act of 2013) into which employers may make pre-tax deductible contributions; funds must be designated for employee job training, workforce development, or manufacturing equipment — directly incentivizing employer spending on worker skills |
| s2124-114 | Creates a federal tax credit matching program tied to state new jobs training tax credit programs (New Skills for New Jobs Act); provides additional federal incentive for private employers who participate in state-sponsored training programs designed for newly hired employees |
| hr3628-115 | Establishes a new employer income tax credit for wages paid to employees participating in qualified registered apprenticeship programs (LEAP Act); credit amount is tied directly to wages paid during employer-sponsored apprenticeship training and to completion of the full apprenticeship program |
| hr5325-113 | Introduces multiple employer tax credits for job training expenses incurred for manufacturing workers (American Manufacturing Workforce Act of 2014), including credits for third-party training costs, wages paid during training periods, and employer expenditures on employee skill development in the manufacturing sector |
| hr6025-111 | Allows manufacturing businesses to establish tax-free manufacturing reinvestment accounts (Manufacturing Reinvestment Account Act of 2010); employers may make deductible contributions designated for workforce training, job development, employee education, and manufacturing capital — directly incentivizing employer investment in worker skills |

---

### Group F: Edge Cases (3 bills)

| bill_id | description |
|---|---|
| hr1625-116 | Establishes a statutory safe harbor test for classifying service providers as independent contractors rather than employees for federal tax purposes (NEW GIGA Act of 2019); directly determines the scope of private employer wage, overtime, payroll tax, and ERISA benefit plan obligations by defining who counts as an employee subject to those requirements |
| s953-113 | Student loan affordability bill that also modifies IRC required minimum distribution rules for tax-exempt pension plans; directly affects private employer obligations as plan sponsors regarding distribution timing and administration of retirement benefits to deceased participants' beneficiaries under ERISA-related provisions |
| hr6325-114 | Creates an independent Workforce Regulatory Review Commission (Workforce Regulatory Review Act of 2016) tasked with reviewing and recommending repeal or modification of regulations governing private employer wage, hour, and employee health obligations; explicitly targets FLSA, ERISA, and FMLA regulatory burdens and requires recommendations to reduce such requirements by one-third |

---

## Qwen + GPT-4o Agree, Sonnet Rejects (4 bills)

A small group where Sonnet is the outlier — up by one from the 07_02 run (3 bills).

| bill_id | bill_type | Sonnet's rejection rationale |
|---|---|---|
| hr4254-114 | enforcement | Non-compete agreement regulation in grocery store acquisitions — Sonnet frames this as labor market competition policy, not direct employer wage/hour obligation |
| s2617-113 | enforcement | Davis-Bacon Act repeal — Sonnet reads Davis-Bacon as applying to federal government-funded construction (government contractors), not private employer wage obligations; GPT-4o disagrees and treats it as affecting private contractor wage floors |
| hr711-113 | enforcement | Davis-Bacon Act repeal — companion to s2617-113; same analysis |
| s1188-113 | enforcement | ACA full-time employee definition modification — Sonnet reads this as a health coverage provision / ACA technical adjustment, not a direct employer wage/hour obligation |

**Note on Davis-Bacon split:** Both s2617-113 and hr711-113 involve repealing the Davis-Bacon Act. GPT-4o flags these as affecting private contractor prevailing wage obligations; Sonnet treats federal contracting wage requirements as government-contractor context rather than private employer enforcement. This is the reverse of the pattern typically seen: GPT-4o is more inclusive here, while Sonnet applies a stricter private-employer test.

---

## Qwen Only — Both Others Reject (16 bills)

These are Qwen's false positives. The count is similar to 07_02 (14). Note: `s1908-112` had all three GPT-4o retries fail (API error), so it appears in this group by default and is not a clean comparison.

### Group 1: Immigration / H-Visa Programs (3 bills)

| bill_id | description | Why excluded |
|---|---|---|
| s792-115 | Establishes a new H-2B temporary non-agricultural work visa program (Save Our Small and Seasonal Businesses Act of 2017) with wage, housing, and recruitment conditions that private employer sponsors must meet; primary structure is an immigration program with attached employer conditions | Employer conditions are tied to visa sponsorship terms rather than independent private employer wage enforcement obligations; the bill's core purpose is immigration program design |
| s2833-114 | Amends the INA to expand data reporting requirements for H-1B, H-2B, L-1, and other nonimmigrant visa classifications to include employee compensation, job duties, and employment duration (Visa Transparency Anti-Trafficking Act of 2016) | Immigration data reporting for visa oversight; compensation disclosure serves enforcement of immigration law sponsorship conditions rather than creating standalone private employer wage obligations under FLSA or ERISA |
| hr5006-114 | House companion to s2833-114 (Visa Transparency Anti-Trafficking Act of 2016); expands INA reporting to require employers sponsoring nonimmigrant workers to disclose compensation, recruitment practices, and other employment details | Same analysis as s2833-114; immigration reporting requirement that does not create new substantive private employer wage or benefit enforcement obligations |

### Group 2: Antitrust Whistleblower Protections (2 bills)

| bill_id | description | Why excluded |
|---|---|---|
| s3462-112 | Provides anti-retaliation protections for employees who report criminal antitrust violations (price-fixing, bid-rigging, market allocation) to law enforcement authorities or cooperate with DOJ antitrust investigations (Criminal Antitrust Anti-Retaliation Act) | Employer retaliation in an antitrust enforcement context; the underlying misconduct involves market competition law violations, not wage, hour, pension mismanagement, FMLA, or WARN Act violations |
| s42-113 | Senate reintroduction of the Criminal Antitrust Anti-Retaliation Act of 2013; prohibits employers from taking adverse action against employees who provide information about criminal antitrust violations or participate in DOJ investigations | Same antitrust enforcement context; protected activity concerns market competition conduct rather than the employer's wage, hour, or benefit obligations covered by this category |

### Group 3: ACA / Health Mandate Edge Cases (3 bills)

| bill_id | description | Why excluded |
|---|---|---|
| hr4064-113 | Links ACA individual mandate enforcement to consistent enforcement of the employer mandate (FAIR Act of 2014); delays individual mandate penalties for any period during which the employer mandate is not enforced uniformly across all applicable large employers | Technical ACA timing provision; the employer mandate interaction is a secondary linking mechanism rather than a new substantive employer health coverage obligation |
| s38-114 | Modifies the ACA employer mandate calculation by excluding from the full-time employee count any individual who was long-term unemployed before being hired (Helping Individuals Regain Employment Act); reduces employer shared responsibility payment exposure for employers who hire the long-term unemployed | Technical ACA mandate carve-out for one category of new hires; not a substantive change to underlying private employer wage or benefit obligations |
| hr5858-115 | Requires high deductible health plans to cover certain primary care services without a deductible as a condition of HSA eligibility (Primary Care Patient Protection Act of 2018); modifies plan design standards for employer-sponsored HDHPs under the IRC | Health savings account and HDHP plan design rules in the IRC; does not impose wage, overtime, pension management, FMLA, or ERISA plan management obligations on private employers |

### Group 4: Tax / Financial Non-Employer-Obligation Bills (4 bills)

| bill_id | description | Why excluded |
|---|---|---|
| s893-115 | Replaces the entire IRC with a flat tax system (Simplified, Manageable, And Responsible Tax Act); repeals most existing deductions, credits, and ERISA non-discrimination rules as part of broad tax simplification | Comprehensive flat tax overhaul; employer wage and benefit impact is an incidental consequence of eliminating most tax code provisions rather than a targeted employer obligation |
| s974-112 | Expands the existing IRC tip tax credit (Section 45B) to employers of cosmetologists and strengthens tip reporting requirements in the cosmetology sector to improve tax compliance (Small Business Tax Equalization and Compliance Act) | Extends an existing tip credit to a new employer sector; credit is for Social Security taxes on employee tips rather than a wage enforcement obligation or training incentive tied to employer wage/benefit conduct |
| s479-113 | Clarifies employment tax treatment of wages paid through professional employer organizations (PEOs) and creates a certified PEO designation to simplify payroll tax compliance (Small Business Efficiency Act); addresses how existing employment taxes are collected and reported in PEO-client employer relationships | PEO tax administration and reporting context; clarifies existing tax mechanics rather than establishing new private employer wage, hour, or benefit enforcement obligations |
| hr3460-112 | Allows a temporary reduced tax rate on repatriated foreign earnings by domestic corporations (American Jobs First Act of 2011); provides an additional deduction for corporations that increase U.S. payroll spending following repatriation | Corporate foreign earnings tax incentive; the payroll increase requirement is a secondary eligibility condition attached to the tax benefit rather than a direct employer wage enforcement obligation |

### Group 5: Industry-Specific / Non-FLSA/ERISA (2 bills)

| bill_id | description | Why excluded |
|---|---|---|
| s2784-113 | Rail safety improvement legislation (Rail Safety Improvement Act of 2014) directing the Secretary of Transportation to conduct track inspections, advance positive train control implementation, and improve safety training; increases civil penalties for railroad hours-of-service violations | Railroad transportation safety regulatory bill; hours-of-service conditions are embedded in safety enforcement context and do not create FLSA/ERISA-style private employer wage enforcement obligations independent of the transportation safety framework |
| hr2927-115 | Expands the Work Opportunity Tax Credit (WOTC) to include apprentices as a new targeted group (HIRED Act of 2017); provides a general hiring tax credit for wages paid to employees in registered apprenticeship programs during their first year of employment | General WOTC hiring incentive extended to apprentices; unlike s959-114 (on-site apprenticeship training credit), this does not tie the credit to employer-provided training expenditures or specific employer training program obligations |

### Group 6: Disaster Relief (1 bill)

| bill_id | description | Why excluded |
|---|---|---|
| hr6854-115 | Provides tax relief for Hurricane Florence victims (Hurricane Florence Tax Relief Act) including an employee retention tax credit for wages paid to employees in the disaster zone, extended casualty loss deductions, and other disaster-related tax relief for businesses and individuals | Disaster relief bill where the employer wage retention credit is incidental to the primary purpose of providing broad tax relief following a natural disaster; employer wage provisions are triggered by the disaster context rather than reflecting a general private employer wage obligation |

### Group 7: API Error (1 bill)

| bill_id | description | Note |
|---|---|---|
| s1908-112 | Clarifies employment tax treatment and reporting obligations for wages paid through professional employer organizations; establishes financial bonding requirements to guarantee PEO payment of employment taxes on behalf of client employers | All three GPT-4o API retries failed; Sonnet correctly rejected on the same grounds as s479-113 (PEO tax administration context, not substantive private employer wage or benefit enforcement) |

---

## Summary: Remaining Model Disagreements

| Issue | GPT-4o | Claude Sonnet | Qwen |
|---|---|---|---|
| ERISA health plan mandates (primary subject = health) | Still rejects most; accepts some with explicit prompt guidance | Accepts as employer benefit obligation | Accepts broadly |
| ERISA health plan mandates (embedded in ACA/tax reform) | Rejects (primary framing dominates) | Accepts embedded ERISA employer obligations | Accepts broadly |
| Immigration bills w/ embedded H-1B wage provisions | Rejects (immigration framing primary) | Extracts employer wage obligations | Accepts broadly |
| Safety/whistleblower bills | Rejects (non-wage primary subject) | Accepts if qualifying employer provision embedded | Accepts broadly |
| Davis-Bacon / prevailing wage bills | **Accepts** (contractor wage floor obligations) | Mixed — some accepted, some rejected as gov-contractor context | Accepts broadly |
| Employer tax credits for training / manufacturing | Rejects (general economic/education policy) | Accepts as `tax_credit_introduction` | Accepts broadly |
| USERRA / military service employer obligations | Rejects (military policy framing) | Accepts as direct employer obligation | Accepts broadly |
| Central-purpose test | Applies strictly | Applies moderately | Applies loosely |

**Bottom line:**
- The **91-bill all-agree set** (65%) is the cleanest true-positive core, up from 79 (59%) in the 07_02 run. The GPT-specific prompt successfully pulled Davis-Bacon prevailing wage bills and several ERISA group health plan bills into the all-agree set.
- The **30 Qwen+Sonnet bills** (GPT-4o rejects) are concentrated in ERISA health/ACA mandate mechanics (Group A, 12 bills) — the single largest remaining disagreement category. These warrant human review if the goal is to capture the full scope of employer-sponsored group health plan obligations under ERISA.
- The **4 Qwen+GPT-4o bills** (Sonnet rejects) include an interesting reversal on Davis-Bacon: GPT-4o now accepts prevailing wage bills while Sonnet applies a stricter private-employer test.
- The **16 Qwen-only bills** are clear false positives consistent with Qwen's pattern of flagging any bill mentioning ERISA, pensions, health insurance, or employer in passing without applying a central-purpose test. Antitrust whistleblower bills and immigration/visa programs are the most systematic errors.
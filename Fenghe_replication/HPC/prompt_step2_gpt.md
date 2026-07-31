
You are a legislative analyst conducting a second-pass review of Congressional bills that have been preliminarily flagged as potentially related to employer wage, hour, and benefit obligations (Violation Tracker category: Wage Hour & Benefits).

A first-pass model has identified the bill below as a potential match. Your task is to apply the detailed qualifying and disqualifying criteria below to confirm or reject that classification, and if confirmed, to assign a bill_type and bill_category.

## Detailed Classification Rules

The following bill types do NOT qualify, even if they mention "wages," "benefits," "employees," or "pensions":
- VA or DoD appropriations bills funding veterans' hospitals, nursing homes, or healthcare programs — these fund government services, not regulate private employer conduct. By contrast, bills that impose obligations directly on private (non-governmental) employers regarding their employees who are veterans or military reservists — such as requiring private employers to continue health benefits, maintain seniority, or reinstate employees returning from military service (e.g., under USERRA) — do qualify, because the private employer is the regulated party.
- Bills adjusting Medicare or Medicaid payment rates to hospitals or providers — these set government reimbursement rates, not employer wage obligations.
- Bills offering employers or individuals a tax benefit unrelated to wage/hour obligations (e.g., adoption tax credits, dependent care credits, COBRA premium accounts, health savings accounts, general hiring credits, employer-provided housing credits) — these are general tax or family policy, not private employer wage or benefit obligations.
- Bills addressing federal or state government employee pay, civil service benefits, or public-sector pension systems — the government is not a "non-governmental employer" under this category.
- Bills financing government trust funds for miner benefits or similar programs (e.g., Black Lung Disability Trust Fund) — these address fund solvency, not employer wage violations.
- Bills about Social Security, TANF, or other public assistance programs — these are government benefit programs, not private employer obligations.
- Bills offering tax credits for hiring workers from specific groups (e.g., veterans, the long-term unemployed) or for general job creation or manufacturing investment — these incentivize hiring decisions, not wage or benefit compliance; a credit specifically tied to employer-provided job training does qualify.
- Bills whose primary subject is something other than private employer wage, hour, or benefit conduct but which mention wages or employment incidentally (e.g., a safety bill with a wage-restitution subclause, an appropriations bill that funds enforcement agencies, a disaster relief bill) — only bills whose central purpose addresses private employer wage, hour, or benefit obligations qualify. (A bill qualifies on this basis if it directly imposes obligations on private employers as sponsors of group health or welfare benefit plans under ERISA — for example, requiring employer-provided plans to cover specific treatments or maintain specific plan terms — even if the same bill also applies to other insurance issuers. A bill does not qualify if it primarily regulates insurance carriers or sets health insurance market rules that apply to employer-sponsored plans only incidentally). (Similarly, a bill qualifies on the pension/retirement basis only if it directly imposes new mandatory obligations on private employers as plan sponsors — for example, minimum funding requirements, fiduciary standards, or participant disclosure obligations. A bill does not qualify if it merely modifies optional plan features, the tax treatment of plan transactions, or ERISA classification rules without creating new mandatory employer conduct obligations.)

The following bill types DO qualify, even though their primary framing may be health insurance, patient rights, managed care, transportation infrastructure, or federal procurement:
- Bills that amend ERISA to impose coverage, access, or administrative standards on employer-sponsored group health plans — such as managed care patient protections (e.g., s889-107), emergency care coverage requirements (e.g., hr1674-107), or prompt payment of claims obligations (e.g., s2551-109) — qualify because ERISA is an employer-obligations statute and the private employer bears the obligation as plan sponsor, regardless of whether the bill is framed as "patient rights," "managed care reform," or "health insurance regulation."
- Bills that nullify rules requiring private federal contractors to disclose or comply with labor law obligations (e.g., hjres37-115) — qualify because such rules directly govern private employer wage and labor law compliance; nullifying them weakens those employer obligations.
- Bills that restrict or prohibit private employers from imposing non-compete agreements on their employees (e.g., hr4254-114) — qualify because non-compete clauses are a direct mechanism by which employers suppress worker wages and bargaining power; legislation limiting them constitutes regulation of private employer wage conduct.

## Bill Information

**Official title:** {official_title}
**Short title:** {short_title}
**Policy area:** {policy_area}
**Subjects:** {subjects}
**Summary:**
{summary_text}

## Step 1 Classification

The first-pass model flagged this bill with the following reason:
> {step1_reason}

## Output

Return ONLY a JSON object with four fields: `categories`, `bill_type`, `bill_category`, and `reason`.

**categories** — either `[1]` if the bill confirms as Wage Hour & Benefits, or `[]` if it does not after applying the detailed rules above.

**bill_type** — classify how the bill primarily relates to the matched categories. Use one of:
- `"enforcement"` — the bill affects the stringency of laws or regulations governing the relevant corporate misconduct (e.g., raising the minimum wage, expanding overtime protections, strengthening ERISA fiduciary duties, tightening WARN Act notice requirements, mandating that private employers without qualifying retirement plans auto-enroll employees in IRA arrangements).
- `"tax_credit_introduction"` — the main way the bill connects to a matched category is by introducing a new tax credit that incentivizes employers toward better behavior (e.g., a new credit for voluntarily offering part-time employees healthcare benefits, a credit for employers who retain workers called up for military reserve duty, a credit for employer-provided job training programs).
- `"tax_credit_removal"` — the bill removes or reduces an existing tax credit of the above type.
- `""` (empty string) — if categories is empty (no category matched), bill_type must also be empty.

**bill_category** — if `categories` is `[1]`, classify the primary subject of the bill using one of:
- `"pension"` — the bill primarily concerns private employer obligations relating to pension, 401(k), or other retirement benefit plans (e.g., minimum funding requirements, PBGC obligations, fiduciary duties over retirement assets, defined benefit/contribution plan rules under ERISA Title I).
- `"healthcare"` — the bill primarily concerns private employer obligations relating to employer-sponsored group health or welfare benefit plans (e.g., ACA employer mandate, ERISA group health plan coverage requirements, managed care patient protections, health benefit continuation obligations).
- `"wage_hour"` — the bill primarily concerns wage, hour, or leave obligations not classified above (e.g., FLSA minimum wage/overtime, WARN Act layoff notice, FMLA leave, prevailing wage on federal contracts, tip credit rules, employer-provided training credits, independent contractor classification).
- `""` (empty string) — if `categories` is empty, `bill_category` must also be empty. If a bill spans both pension and healthcare provisions, assign the category that reflects the bill's dominant focus.

**reason** — one sentence explaining your final determination. If you are overturning the Step 1 flag, briefly explain why the bill does not qualify under the detailed rules.

Examples:

Confirmed match:
{"categories": [1], "bill_type": "enforcement", "bill_category": "wage_hour", "reason": "Expands overtime eligibility thresholds under the FLSA, directly tightening private employer wage obligations."}

Step 1 flag overturned:
{"categories": [], "bill_type": "", "bill_category": "", "reason": "Although the bill mentions employee wages, its primary subject is federal infrastructure grants; private employer wage obligations are incidental conditions, not the bill's central purpose."}

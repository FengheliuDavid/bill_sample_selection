
You are a legislative analyst. You are interested in understanding how bills proposed in the U.S. Congress topically align with issues related to employer wage, hour, and benefit obligations.

Identify whether the U.S. Congressional bill below aligns with the Violation Tracker category below, and if so how. This category reflects a type of **corporate misconduct** targeted by government enforcement actions (DOJ, OSHA, DOL, etc.) against companies and employers — whether privately-held or publicly-traded. The key distinction is non-governmental: government agencies, military branches, and public-sector entities are excluded, but large publicly-traded corporations (e.g., Walmart, IBM, Boeing) are squarely within scope.

A bill qualifies if it is substantively related to the type of corporate conduct associated with the underlying Violation Tracker violation — whether by directly regulating or enforcing that conduct, or by introducing tax incentives that encourage or discourage it. For example, a wage and hour violation that relates to overtime issues, underpayment of wages, etc. might be related to a bill that relates to worker pay-related issues (overtime protections and exemptions, restrictions on things like "clopening" schedules, tax credits for employers who voluntarily expand benefits, etc. -- this is not exhaustive but just an example).



Bills should be categorized as related to wage & hour and benefits issues only when a non-governmental employer is the direct subject accused of: failing to pay required wages, overtime, or tips; failing to give employees adequate advance notice before mass layoffs or plant closings; mismanaging or looting employee pension, 401k, or retirement benefit plans; failing to provide or maintain employer-sponsored group health or welfare benefit plans as required by law; or retaliating against employees for taking protected family, medical, or parental leave, or for reporting wage violations, unsafe working conditions, or other protected activities covered by whistleblower statutes. Acts covered include but are not limited to FLSA (minimum wage, overtime, child labor), WARN Act (layoff notice), ERISA (pension/retirement plan obligations and employer-sponsored group health and welfare benefit plan obligations), and FMLA (leave retaliation). Amendments targeting specific worker groups or industries — such as child labor provisions, overtime exemptions for care workers, or paid-hour requirements for training — qualify even when the bill is structured around a specific sector. Bills primarily addressing government employee compensation, military pay, veterans' healthcare or education programs, or any benefits administered by the VA, DoD, or other government agencies to service members or veterans do not involve employer misconduct and do not qualify.

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
   - Bills that impose prevailing wage requirements on private contractors and subcontractors working on federally-funded projects (e.g., hr3264-109) — qualify because prevailing wage obligations are direct wage requirements running from private employers to their workers, even when the bill is primarily structured as an infrastructure or grant bill.
   - Bills that nullify rules requiring private federal contractors to disclose or comply with labor law obligations (e.g., hjres37-115) — qualify because such rules directly govern private employer wage and labor law compliance; nullifying them weakens those employer obligations.


## Bill Information

**Official title:** {official_title}
**Short title:** {short_title}
**Policy area:** {policy_area}
**Subjects:** {subjects}
**Summary:**
{summary_text}

## Output

Return ONLY a JSON object with three fields: `categories`, `bill_type`, and `reason`.

**categories** — either `[1]` if the bill matches Wage Hour & Benefits, or `[]` if it does not.

**bill_type** — classify how the bill primarily relates to the matched categories. Use one of:
- `"enforcement"` — the bill affects the stringency of laws or regulations governing the relevant corporate misconduct (e.g., raising the minimum wage, expanding overtime protections, strengthening ERISA fiduciary duties, tightening WARN Act notice requirements, mandating that private employers without qualifying retirement plans auto-enroll employees in IRA arrangements).
- `"tax_credit_introduction"` — the main way the bill connects to a matched category is by introducing a new tax credit that incentivizes employers toward better behavior (e.g., a new credit for voluntarily offering part-time employees healthcare benefits, a credit for employers who retain workers called up for military reserve duty, a credit for employer-provided job training programs).
- `"tax_credit_removal"` — the bill removes or reduces an existing tax credit of the above type.
- `""` (empty string) — if categories is empty (no category matched), bill_type must also be empty. If a bill touches on a related topic but does not clearly fit enforcement or tax credit, treat it as not matching any category and return an empty list.

**reason** — one sentence explaining why the bill was assigned to those categories and that bill_type. If categories is empty, briefly state why it does not qualify.

Examples:

Bill matches category [1] by tightening overtime rules:
{"categories": [1], "bill_type": "enforcement", "reason": "Expands overtime eligibility thresholds under the FLSA, directly tightening private employer wage obligations."}

Bill matches category [1] by introducing a tax credit for employers who offer paid family leave:
{"categories": [1], "bill_type": "tax_credit_introduction", "reason": "Introduces a new tax credit incentivizing private employers to voluntarily offer paid family leave, relating to FMLA-adjacent employer conduct."}

No category fits:
{"categories": [], "bill_type": "", "reason": "Bill appropriates funds for VA hospital operations; no private employer wage or benefit obligation is involved."}

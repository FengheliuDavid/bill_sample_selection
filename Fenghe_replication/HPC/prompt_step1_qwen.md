
You are a legislative analyst. You are interested in understanding how bills proposed in the U.S. Congress topically align with issues related to employer wage, hour, and benefit obligations.

Identify whether the U.S. Congressional bill below aligns with the Violation Tracker category below, and if so how. This category reflects a type of **corporate misconduct** targeted by government enforcement actions (DOJ, OSHA, DOL, etc.) against companies and employers — whether privately-held or publicly-traded. The key distinction is non-governmental: government agencies, military branches, and public-sector entities are excluded, but large publicly-traded corporations (e.g., Walmart, IBM, Boeing) are squarely within scope.

A bill qualifies if it is substantively related to the type of corporate conduct associated with the underlying Violation Tracker violation — whether by directly regulating or enforcing that conduct, or by introducing tax incentives that encourage or discourage it. For example, a wage and hour violation that relates to overtime issues, underpayment of wages, etc. might be related to a bill that relates to worker pay-related issues (overtime protections and exemptions, restrictions on things like "clopening" schedules, tax credits for employers who voluntarily expand benefits, etc. -- this is not exhaustive but just an example).

Bills should be categorized as related to wage & hour and benefits issues only when a non-governmental employer is the direct subject accused of: failing to pay required wages, overtime, or tips; failing to give employees adequate advance notice before mass layoffs or plant closings; mismanaging or looting employee pension, 401k, or retirement benefit plans; failing to provide or maintain employer-sponsored group health or welfare benefit plans as required by law; or retaliating against employees for taking protected family, medical, or parental leave, or for reporting wage, hour, or benefit violations covered by whistleblower statutes (e.g., FLSA, ERISA, or FMLA retaliation claims. Bills whose whistleblower provisions concern workplace safety, environmental hazards, product safety, or other non-wage misconduct do not qualify on this basis). Acts covered include but are not limited to FLSA (minimum wage, overtime, child labor), WARN Act (layoff notice), ERISA (pension/retirement plan obligations and employer-sponsored group health and welfare benefit plan obligations), and FMLA (leave retaliation). Amendments targeting specific worker groups or industries — such as child labor provisions, overtime exemptions for care workers, or paid-hour requirements for training — qualify even when the bill is structured around a specific sector. Bills primarily addressing government employee compensation, military pay, veterans' healthcare or education programs, or any benefits administered by the VA, DoD, or other government agencies to service members or veterans do not involve employer misconduct and do not qualify.


## Bill Information

**Official title:** {official_title}
**Short title:** {short_title}
**Policy area:** {policy_area}
**Subjects:** {subjects}
**Summary:**
{summary_text}

## Output

Return ONLY a JSON object with two fields: `categories` and `reason`.

**categories** — either `[1]` if the bill matches Wage Hour & Benefits, or `[]` if it does not.

**reason** — one sentence explaining why the bill was assigned to those categories. If categories is empty, briefly state why it does not qualify.

Examples:

Bill matches category [1] by tightening overtime rules:
{"categories": [1], "reason": "Expands overtime eligibility thresholds under the FLSA, directly tightening private employer wage obligations."}

Bill matches category [1] by amending ERISA pension funding rules:
{"categories": [1], "reason": "Imposes new minimum funding requirements on private employers as defined benefit plan sponsors under ERISA Title I."}

No category fits:
{"categories": [], "reason": "Bill appropriates funds for VA hospital operations; no private employer wage or benefit obligation is involved."}

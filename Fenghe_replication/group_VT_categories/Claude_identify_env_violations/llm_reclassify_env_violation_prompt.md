# Prompt: Reclassify Environmental Violations

## Task

Records in the Violation Tracker database are currently labeled as `"environmental violation"` — a catch-all category used when the specific type of environmental offense was not identified. Your task is to reclassify each record into the most appropriate specific category from the list below, based on the agency that issued the penalty and the violation description.

---

## Categories

Choose exactly one category from the following 20 options. The label you output must match exactly.

| Category | Description |
|---|---|
| `air pollution violation` | EPA Clean Air Act enforcement for air emissions violations, storm water management failures, and violations of air quality permits at industrial facilities. |
| `asbestos violation` | EPA enforcement for improper handling or disposal of asbestos at demolition or construction sites, and litigation for concealing asbestos health risks. |
| `fuel economy (CAFE) violation` | NHTSA fines against automakers for failing to meet Corporate Average Fuel Economy (CAFE) standards for their passenger car or light truck fleets. |
| `water pollution violation` | EPA Clean Water Act enforcement for discharging pollutants including coal ash and industrial wastewater into rivers, lakes, and other waterways. |
| `drinking water violation` | Safe Drinking Water Act enforcement for monitoring failures, nitrate contamination, and violations at public water supply systems. |
| `MTBE violation` | Litigation and enforcement for contamination of groundwater with methyl tertiary-butyl ether (MTBE), a gasoline additive linked to health risks. |
| `PCB violation` | EPA enforcement and civil litigation for contamination of waterways and communities from polychlorinated biphenyls (PCBs), primarily against Monsanto. |
| `PFAS violation` | Litigation and enforcement for contaminating water supplies with per- and polyfluoroalkyl substances (PFAS or "forever chemicals"), primarily from firefighting foam. |
| `oil spill` | EPA, Coast Guard, and state enforcement for oil spills from vessels and pipelines, including failure to accurately report spills and clean up contamination. |
| `animal feeding operation violation` | EPA enforcement against large livestock operations (CAFOs and feedlots) for water pollution and other environmental violations. |
| `hazardous waste violation` | EPA RCRA enforcement for improper storage, handling, or disposal of hazardous waste at manufacturing and industrial facilities. |
| `radioactive waste violation` | Litigation for contamination from radioactive waste at nuclear weapons and fuel facilities, and state radiation control law violations. |
| `underground storage tank violation` | EPA and state enforcement for violations of underground petroleum storage tank regulations, including failure to test, repair, or shut down non-compliant tanks. |
| `pipeline safety violation` | DOT/PHMSA enforcement for pipeline safety regulation violations, including fatal incidents caused by corrosion, inadequate inspection, or improper design. |
| `oil or gas drilling violation` | BSEE enforcement for offshore oil and gas drilling safety violations, including equipment failures, crane accidents, and inoperative safety systems. |
| `mining environmental violation` | EPA and state enforcement for environmental damage from mining operations including water quality violations and natural resource damage. |
| `pesticide violation` | EPA FIFRA enforcement for distributing or selling pesticides without required labels, without a state license, or in violation of federal registration requirements. |
| `solid waste violation` | State environmental enforcement for violations of solid waste management regulations at disposal facilities and industrial operations. |
| `lead violation` | Enforcement and litigation for products containing excessive lead levels including children's jewelry, school supplies, and lead-based paint. |
| `energy conservation violation` | DOE enforcement for failures to comply with mandatory energy efficiency standards for appliances and equipment. |

If the record does not fit any specific category above, output `environmental violation` to retain the original label.

---

## Input Format

Each record will be provided as:

```
Agency: <enforcement agency name>
Description: <violation description>
```

---

## Output Format

Respond with only the category label — no explanation, no punctuation, no extra text. Example:

```
air pollution violation
```

---

## Examples

**Input:**
```
Agency: Environmental Protection Agency
Description: Primary law: CAA, Violation type: Air Emissions Not Otherwise Specified
```
**Output:**
```
air pollution violation
```

**Input:**
```
Agency: Alabama Department of Environmental Management
Description: National Pollutant Discharge Elimination System
```
**Output:**
```
water pollution violation
```

**Input:**
```
Agency: Pipeline and Hazardous Materials Safety Administration
Description: Failure to maintain adequate corrosion control on interstate gas pipeline
```
**Output:**
```
pipeline safety violation
```

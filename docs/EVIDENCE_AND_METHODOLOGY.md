# Evidence and methodology

## Evidence supporting the case study

| Evidence type | What it establishes |
|---|---|
| Governing protocol and workspace records | Layered knowledge architecture, domain ownership, continuity and status-control procedures |
| Historical change and QA records | Documented version deployment and read-back, scheduling reconciliation, incident investigation, and corrective procedure changes |
| A01 fictional demonstration | Selected scheduling-decision rules operating on reproducible fixtures |
| B01 fictional demonstration | Selected context-selection and approval rules operating on reproducible fixtures |

Historical operational examples were reviewed from private project records. The public-facing case studies summarize the relevant decisions and results, while illustrative fixtures use fictional subjects and dates.

## How the examples were evaluated

The A01 and B01 Python reference models were executed locally using their included fixtures and unit tests. **21 automated unit tests passed** across the two models. Each model addresses a defined subset of the operating framework's decision rules.

The historical record documents separate real-world activities, including workspace continuity, operational reconciliation, incident remediation, and a limited protocol continuation test conducted before the later November 4 incident. The examples and historical evidence are labeled separately so that readers can assess each on its own terms.

## Design ownership and tools

I designed and iteratively refined the operational framework, including its information structure, responsibility boundaries, handoff logic, and verification controls. ChatGPT workspaces and existing file and scheduling tools support its operation. Python examples provide reproducible demonstrations of selected rules.

## Evaluation focus

The project can be assessed through its architecture, documented operating procedures, treatment of source conflicts, observable decision states, and response to a recorded failure. The repository supplies runnable examples and an explicit description of the records underpinning the case.

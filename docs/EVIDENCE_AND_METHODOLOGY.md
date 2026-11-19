# Evidence, methodology, and privacy-safe operational excerpts

This project combines **real operating records** with two **fictional Python models**. Keeping those evidence types separate is central to its design.

## What was real

- I designed and used structured operating records and change/continuation rules while coordinating **eight academic workstreams** and related projects. The eight-workstream scope comes from the owner's documented project description, **not** an automatically measured repository metric.
- A real November 4, 2026 continuation incident was investigated: the conversation history existed, but the assistant selected the wrong work to resume. A corrective source record documented both the observed failure and a revised interpretation/authorization rule.
- The governing continuity system maintains distinct **current state**, **decision/source history**, and **original evidence** records. A migration handoff also preserves source boundaries and unresolved statuses.

Those records are maintained outside this public repository because they contain personal, academic, and operational material. The following excerpts intentionally expose only project-relevant portions.

## Small excerpts from real records

**HOT — actual current-state record (November 2026).** A project-status entry distinguishes the **21 tests reported at the earlier publication checkpoint** from live-system validation:

> “21 earlier passing local synthetic tests, not proof of real-world productivity or independently tested live recovery.”

This is a short, unaltered excerpt of a longer private status entry; other fields are withheld. The new tests in this revision are separately accounted for by the repository's live CI workflow.

**WARM — the November 4 correction.** The recorded earlier behavior was to select another workstream after a request to return to work *before* a protocol discussion. The corrective decision states:

> “A bare ‘continue where we left off’ must use the user's immediate conversational referent, not blindly select the newest line of the historical source.”

The behavioral description is a privacy-safe summary; the quoted corrective sentence is from the dated source. It illustrates the change from an **observed wrong selection** to an **explicit corrective rule**. Writing the rule did not itself establish that future assistants would follow it.

**Handoff — field structure from the governing protocol.** A source-fidelity handoff carries:

```text
Source conversation and capture date
Last relevant user message + complete available assistant reply
Outstanding request and the next authorized action
Latest material corrections and negative constraints
Current owner/source map and relevant evidence links
Capture boundary: SEALED or UNSEALED, with limitations
```

This is a public-safe outline of the real handoff requirements, **not** a copy of a private user's populated handoff.

## What the Python examples establish

| Evidence | Defensible conclusion | What it does not establish |
|---|---|---|
| [A01 fictional fixtures and tests](../demos/a01/tests/test_a01.py) | Source conflict, scheduling capacity, authorization, in-memory read-back and fault-handling logic can be tested locally | Live calendar changes, persistent disk writes, production reliability |
| [B01 independent wording cases](../demos/b01/fixtures/b01_synthetic_cases.json) | A bounded rule model can be compared to separately specified historical-continuation expectations | General natural-language understanding or guaranteed future ChatGPT behavior |
| November 4 incident and corrected source guidance | A real failure was analyzed and specific governance rules were changed | A measured post-correction reduction in errors |
| Real HOT/WARM/handoff records | A layered information and source-governance structure was maintained and applied | A quantified productivity, retention, or business ROI improvement |

The model tests run with Python 3.10+ and the standard library. [Run instructions and GitHub Actions status are in the README](../README.md). **No unsupported counts of stale deadlines caught, time saved, or independently verified business impact are claimed.**

## Role and design ownership

I identified the operational problem, shaped requirements, defined the information architecture and owner boundaries, designed status and verification controls, reviewed failure evidence, and refined the approach. AI-assisted tools supported code and documentation. The two local models are inspectable **examples of selected design decisions**, not the entirety of the live operating framework.

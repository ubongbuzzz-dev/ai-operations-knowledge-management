# Evidence, methodology, and privacy-safe operational excerpts

This project combines **real operating records** with two **fictional Python models**. Keeping those evidence types separate is central to its design.

## What was real

- I designed and used structured operating records and change/continuation rules across **eight academic workstreams** and related projects, as documented in the project's operating history.
- A real November 4, 2026 continuation incident was investigated: the conversation history existed, but the assistant selected the wrong work to resume. A corrective source record documented both the observed failure and a revised interpretation/authorization rule.
- The governing continuity system maintains distinct **current state**, **decision/source history**, and **original evidence** records. A migration handoff also preserves source boundaries and unresolved statuses.

Those records are maintained outside this public repository because they contain personal, academic, and operational material. The following excerpts intentionally expose only project-relevant portions.

## Small excerpts from real records

**HOT — actual current-state record (November 2026).** A project-status entry records the scope of the **21 local tests reported at an earlier publication checkpoint**:

> “21 earlier passing local synthetic tests, not proof of real-world productivity or independently tested live recovery.”

This excerpt is drawn from a longer private status record. The current repository's automated test results are independently visible through GitHub Actions.

**WARM — the November 4 correction.** The recorded earlier behavior was to select another workstream after a request to return to work *before* a protocol discussion. The corrective decision states:

> A bare “continue where we left off” must use the user's *immediate conversational referent*, not blindly select the newest line of the historical source.

The behavioral description is a privacy-safe summary; the quoted corrective sentence is from the dated source. It connects an **observed wrong selection** to the **explicit corrective rule** introduced in response.

**Handoff — field structure from the governing protocol.** A source-fidelity handoff carries:

```text
Source conversation and capture date
Last relevant user message + complete available assistant reply
Outstanding request and the next authorized action
Latest material corrections and negative constraints
Current owner/source map and relevant evidence links
Capture boundary: SEALED or UNSEALED, with limitations
```

This outlines the actual handoff fields while keeping populated private records confidential.

## What the Python examples establish

| Evidence | Verified or documented finding | Evidence scope |
|---|---|---|
| [A01 fictional fixtures and tests](../demos/a01/tests/test_a01.py) | Source conflict, scheduling capacity, authorization, in-memory read-back and fault-handling logic can be tested locally | Local in-memory state, synthetic scheduling cases, and injected faults |
| [B01 independent wording cases](../demos/b01/fixtures/b01_synthetic_cases.json) | The bounded rule model is checked against independently specified continuation decisions | Specified language cases and expected outcomes |
| November 4 incident and corrected source guidance | A real failure was analyzed and specific governance rules were changed | Dated incident and correction; subsequent effectiveness evaluated separately |
| Real HOT/WARM/handoff records | A layered information and source-governance structure was maintained and applied | Operational records and documented status distinctions |

The model tests use Python 3.10+ and the standard library. [Run instructions and GitHub Actions status are in the README](../README.md).

## Design and implementation

I identified recurring coordination failures, translated them into requirements, designed the information architecture and owner boundaries, established status and verification controls, and refined the framework after examining real failures. The A01 and B01 examples demonstrate two key mechanisms: authorized deadline coordination and correct recovery of conversation context.

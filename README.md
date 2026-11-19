# Operations & Knowledge Management Framework

**Independent business-systems design project | 2026–present**

I designed an AI-assisted operating framework to coordinate **eight academic workstreams** alongside career, leadership, and independent projects. The problem was practical: requirements, deadlines, and decisions lived in separate workspaces, documents, and calendars. A change could be recorded in one place while another area continued using the older information.

I built the framework around a clear question: **When something changes, how do we establish what is current, determine who owns the decision, coordinate any follow-up, and verify what actually happened?**

## What the system does

| Design decision | Why it matters |
|---|---|
| Give each workstream an owner | The source responsible for a requirement controls changes to it |
| Separate current state, decision history, and original sources | Important decisions remain easy to find without losing why they changed |
| Check revisions and conflicting evidence | A newer-looking update does not automatically become the truth |
| Require explicit approval before consequential changes | Proposed calendar work is not automatically scheduled |
| Distinguish planned, authorized, scheduled, and completed work | A polished report or calendar event is not proof the underlying task happened |
| Record and correct real failures | Preserving history is not enough if the wrong conversation thread is resumed |

The framework uses structured records, source hierarchy, operating rules, file-management tools, and scheduling handoffs. I designed the responsibilities, decision controls, information structure, and quality checks; AI tools assisted with parts of the implementation and documentation. [See the operating architecture](docs/ARCHITECTURE.md).

## A real failure and two small executable examples

**Real incident — choosing the wrong work to resume.** After a lengthy continuity discussion, a request to return to earlier work was misinterpreted. The assistant had retained the relevant history but selected another workstream. I analyzed the failure and refined the rules for identifying historical stopping points and respecting action authority. [See B01 and the correction](docs/B01_FAILURE_AND_RECOVERY.md).

**A01 — a deadline changes.** Fictional inputs move a deadline from November 20 to November 18. The Python model selects the verified owner update, finds available time around protected commitments, requires authorization, writes to an **in-memory** calendar, and reads back the written state. A calendar write never marks the underlying task completed. [Explore A01](docs/A01_WORKFLOW.md).

**B01 — select the correct conversation context.** A deliberately small rule model distinguishes a named earlier stopping point, ambiguous continuation, and an entirely new task such as “Update my resume.” It is **not** a general natural-language assistant. [Explore B01](docs/B01_FAILURE_AND_RECOVERY.md).

The Python examples are **fictional demonstrations of selected rules**, not software that controls my real calendar or proof of the framework's real-world productivity gains. [See the evidence boundaries and redacted real-record excerpts](docs/EVIDENCE_AND_METHODOLOGY.md).

## Run the examples

Python **3.10+**, standard library only:

```bash
python -m unittest discover -s demos/a01/tests -v
python -m unittest discover -s demos/b01/tests -v

python demos/a01/src/a01_simulation.py demos/a01/fixtures/a01_fictional_scenario.json --authorized --commit
python demos/b01/src/b01_reference_model.py demos/b01/fixtures/b01_synthetic_cases.json
```

[![Python tests](https://github.com/ubongbuzzz-dev/ai-operations-knowledge-management/actions/workflows/tests.yml/badge.svg)](https://github.com/ubongbuzzz-dev/ai-operations-knowledge-management/actions/workflows/tests.yml)

The unit tests check expected behavior and failure cases; the badge reports GitHub Actions' automated status when runs are available. Neither validates the live ChatGPT workspaces.

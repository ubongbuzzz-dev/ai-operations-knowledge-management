# B01 | Recovering the correct work after a context-selection failure

**Real incident, separate fictional rule demonstration.** In November 2026, a conversation had accumulated several stopping points: ongoing professional-development work, a later discussion about a continuity protocol, and a migration handoff. When asked to return to work from **before** the protocol discussion, the assistant resumed an unrelated task. After correction, it narrowed the request to one scheduling handoff. The records were available; **selection and interpretation failed**.

## What the incident changed

The corrective November 4 record distinguished three anchors: the literal end of the original conversation, the earlier substantive work checkpoint, and the later migration-administration exchange. It also required that returning to a topic **not be treated as authorization for an unrelated action**.

A short extract from the actual November 4 corrective record (no private task content reproduced):

> A bare “continue where we left off” must use the user's *immediate conversational referent*, not blindly select the newest line of the historical source.

That is a **documented change to operating guidance**, not proof that every later model response followed it.

## Decision table in the companion model

| Request type | Model behavior |
|---|---|
| Names a particular point in conversation history | Resolve that point; default to review, not external action |
| Says **before** a protocol discussion | Select the earlier work checkpoint |
| Says **after** a protocol discussion | Use a known post-protocol checkpoint, otherwise clarify—never silently substitute *before* |
| Names a scheduler handoff | Return the distinct scheduler status topic |
| Says “continue” without a clear referent | Use a uniquely selected current context or ask which one |
| Makes a **new** request such as “Update my resume” | Classify as new work, not “resume the old conversation” |

The companion [Python decision model](../demos/b01/src/b01_reference_model.py) deliberately uses a few bounded textual rules. Its purpose is to demonstrate **explicit decision precedence and action scope**, not to understand every possible English request. The independent [plain-language fixture](../demos/b01/fixtures/b01_synthetic_cases.json) includes the incident's natural wording, challenging before/after variations, ambiguous references, and new-task false positives.

## What the evidence establishes

- **Historical:** A documented wrong-thread selection occurred despite preserved records; corrective rules were written.
- **Reproducible:** The included local model can be checked against independently specified expected decisions.
- **Not established:** The synthetic tests do not show that an actual ChatGPT successor will always interpret a user's request correctly.

Run the demonstration from the repository root:

```bash
python -m unittest discover -s demos/b01/tests -v
python demos/b01/src/b01_reference_model.py demos/b01/fixtures/b01_synthetic_cases.json
```

[Real-record excerpts and source distinctions](EVIDENCE_AND_METHODOLOGY.md) · [Architecture](ARCHITECTURE.md)

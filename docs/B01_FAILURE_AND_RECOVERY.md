# B01 | Improving continuity through failure analysis

**Case study:** A documented operational incident, corrective design changes, and a separate fictional decision-model demonstration.

## What happened

A long-running conversation had been preserved and indexed. When the user asked to return to work from before a continuity-protocol discussion, the assistant resumed an unrelated recruiting task. After correction, it selected an overly narrow scheduling handoff instead of the intended broader work context.

The information was available. **The failure was in selecting the right part of it and deciding what to do next.**

## Diagnosis

I identified three connected process weaknesses:

- **Context selection:** Multiple historical stopping points could be interpreted as “where we left off.”
- **Authority to act:** Resuming a topic was being treated as permission to perform a specific task.
- **Source selection:** More precise historical records were available than the summary being used to infer the next step.

## What I refined

I strengthened the source-review and continuation procedures to distinguish:

1. The literal final topic of a historical conversation
2. The point in that history the user's current request actually identifies
3. Nearby unfinished work whose status and authorization must be checked separately

The revised rules call for checking the appropriate source, preserving already settled decisions, and selecting the next action based on the user's present instructions.

## Historical result and evidence

The November 4, 2026 remediation record documents the context-selection investigation and corrective operating guidance. An earlier protocol deployment that day had passed a separate, limited continuation test. That test preceded the incident.

The case demonstrates why **preserving information and interpreting a request accurately are distinct design requirements**. The corrective procedures are documented; continued real-world effectiveness requires further behavioral observation.

## Reproducible companion

A fictional Python reference model evaluates context selection and authorization decisions using controlled inputs. **11/11 automated tests passed** in the local model.

[Reproduce the example](REPRODUCE.md) · [Review the evidence approach](EVIDENCE_AND_METHODOLOGY.md)

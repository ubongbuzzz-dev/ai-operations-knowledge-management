# A01 | Coordinating a deadline change

**Example:** Executable fictional scenario illustrating the scheduling-handoff design.

## Challenge

A project deadline moves from Friday, November 20, 2026, to Wednesday, November 18. The updated requirement competes for time against existing protected commitments. The scenario tests how source changes move into operational decisions while retaining accurate status records.

## Rules demonstrated

1. Select the latest authorized requirement over a superseded deadline.
2. Preserve a traceable record of the change.
3. Evaluate candidate scheduling intervals against protected commitments.
4. Apply authorized changes through a controlled action step.
5. Report simulated persistence failures explicitly.
6. Maintain distinct scheduling and task-completion states.

## Test outcomes

| Scenario | Reference-model outcome |
|---|---|
| Awaiting approval | `AWAITING_AUTHORIZATION` |
| Approved simulated commit | `SYNTHETIC_COMMIT_VERIFIED` |
| Simulated write failure | `WRITE_FAILED_NO_COMMIT` |
| Capacity shortage | `INSUFFICIENT_CAPACITY` |

**10/10 automated tests passed** in the local Python reference model. The model exercises the scenario entirely with fictional records and in-memory state.

## Connection to the framework

The actual scheduling procedures specify domain ownership, deliberate retrieval of changes, protection of existing commitments, authorization, and verification. A01 translates selected decision rules into an inspectable model with controlled inputs and repeatable outputs.

[Run the example](REPRODUCE.md)

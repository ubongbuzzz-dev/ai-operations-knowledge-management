# A01 | Coordinating a deadline change

**Fictional, executable case.** A project's verified owner moves a deadline from **November 20 to November 18, 2026**. The model considers work periods on **November 18 between 9 a.m. and 6 p.m.**; it does not search earlier days or know the actual deadline hour. Three existing commitments are protected.

## Decision sequence

| Step | What is checked or produced |
|---|---|
| 1. Establish the requirement | Consider verified project-owner revisions, reject newer unverified updates, and flag different deadlines with the same current revision |
| 2. Check available time | Find exact free intervals around commitments, including partial hours, without moving existing blocks |
| 3. Propose | In the included fixture, propose 11 a.m.–noon and noon–1 p.m. |
| 4. Await authorization | Proposals are not committed until both authorization and explicit commit are present |
| 5. Write and read back | Write to an independent **in-memory calendar** and compare the full resulting block list against the expected state |
| 6. Report actual state | Report a failure on simulated write/read-back mismatch; retain the separate project task status **NOT_COMPLETED** |

The model also checks for a protected block inserted **after planning but before commit**, illustrating why a conflict check is needed at the write boundary.

## Outcomes implemented by the model

| Status | Meaning |
|---|---|
| `INVALID_INPUT` | Malformed source, calendar block, day, or time requirement |
| `BLOCKED_UNVERIFIED_SOURCE` | No verified owner source |
| `BLOCKED_NEWER_UNVERIFIED` | A newer owner revision needs verification |
| `BLOCKED_CONFLICTING_OWNER_REVISION` | Equal latest owner revisions disagree about the deadline |
| `INSUFFICIENT_CAPACITY` | Work does not fit in the specified deadline-day window |
| `AWAITING_AUTHORIZATION` | Time proposed; change not approved |
| `AUTHORIZED_PROPOSAL_ONLY` | Approved proposal, but no commit requested |
| `BLOCKED_CONFLICT` | A new commitment conflicts with a previously prepared proposal |
| `WRITE_FAILED_NO_COMMIT` | Injected simulated write failure |
| `WRITE_VERIFICATION_FAILED` | Injected read-back corruption detected and rolled back |
| `SYNTHETIC_COMMIT_VERIFIED` | Exact **in-memory** read-back matched; task still not completed |

The Python model exercises these states locally. `existing_preserved` is calculated from the resulting calendar snapshot, and `SYNTHETIC_COMMIT_VERIFIED` requires matching in-memory read-back. External calendar changes use a separate, authorized integration.

## Reproduce

From the repository root:

```bash
python -m unittest discover -s demos/a01/tests -v
python demos/a01/src/a01_simulation.py demos/a01/fixtures/a01_fictional_scenario.json --authorized --commit
python demos/a01/src/a01_simulation.py demos/a01/fixtures/a01_fictional_scenario.json --authorized --commit --write-fail
python demos/a01/src/a01_simulation.py demos/a01/fixtures/a01_fictional_scenario.json --authorized --commit --readback-fail
```

The model focuses on **decision and status integrity** in a defined, single-day scheduling window. [Architecture](ARCHITECTURE.md) · [Evidence boundaries](EVIDENCE_AND_METHODOLOGY.md).

# A01 | Coordinating a deadline change

**Scenario:** A fictional project deadline changes while existing commitments must remain protected. The included Python model makes the scheduling-handoff rules reproducible.

## The situation

Project Alpha's owner moves the deadline from **Friday, November 20, 2026**, to **Wednesday, November 18**. Work needs to be allocated before the new deadline without moving fixed commitments.

The fictional input includes three protected blocks on November 18: **9–11 a.m., 2–4 p.m., and 5–6 p.m.** The model looks for two hours of available work time.

## What the design does

| Step | Decision or result |
|---|---|
| **1. Verify the change** | Select the latest verified project-owner revision; preserve the earlier deadline as history. |
| **2. Check constraints** | Find available periods without overlapping existing protected blocks. |
| **3. Propose work time** | Identify two one-hour periods, **11 a.m.–noon** and **noon–1 p.m.**, in the synthetic fixture. |
| **4. Require approval** | Keep the proposal uncommitted until authorization is provided. |
| **5. Verify the simulated write** | Confirm the in-memory result or explicitly report a simulated write failure. |
| **6. Report actual task state** | Keep the underlying project task marked **NOT_COMPLETED**. |

The sequence demonstrates why scheduling work and completing work are different events. Even an authorized, successfully simulated scheduling change leaves the task completion status unchanged.

## Outcomes exercised by the tests

| Condition | Model status |
|---|---|
| Scheduling proposal awaiting approval | `AWAITING_AUTHORIZATION` |
| Authorized simulated commit with in-memory verification | `SYNTHETIC_COMMIT_VERIFIED` |
| Simulated persistence failure | `WRITE_FAILED_NO_COMMIT` |
| Insufficient available time | `INSUFFICIENT_CAPACITY` |
| Newer owner revision has not been verified | `BLOCKED_NEWER_UNVERIFIED` |

**10/10 automated unit tests passed** for the fictional Python reference model. The test suite covers source selection, authorization, scheduling conflicts, capacity, write failure, and accurate status reporting.

## Why it matters

A changing deadline creates at least three separate responsibilities: establish what changed, decide where the work fits, and verify what actually happened. The framework assigns each to an explicit part of the process, reducing ambiguity when requirements cross workspace boundaries.

[Run A01](REPRODUCE.md) · [Return to the architecture](ARCHITECTURE.md)

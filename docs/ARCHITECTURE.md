# Architecture and operating model

## Design objective

Coordinate independent workstreams through clear information ownership, accurate operational state, traceable decisions, and controlled downstream actions.

## Knowledge architecture

| Layer | Purpose | Representative records |
|---|---|---|
| **HOT** | Current operational decisions and active requirements | Current State; active rules and task source |
| **WARM** | Durable context, reasoning, and provenance | Master Memory; Decision & Source Index |
| **COLD** | Detailed primary evidence for targeted inspection | Original documents, historical records, archived material |

Selective retrieval supports efficient day-to-day decisions and deeper investigation when sources conflict or historical detail matters.

## Responsibilities and interfaces

**Domain-owned workspaces** maintain subject-specific requirements, decisions, progress, and supporting evidence.

**The continuity framework** establishes record structure, provenance rules, source precedence, history maintenance, version transitions, and recovery procedures.

**The scheduling workspace** reviews owner-provided demands against real constraints and allocates feasible time through controlled calendar actions.

**Authorization and verification controls** maintain a clear record of proposed changes, approvals, actual operations, and confirmed results.

## Representative operational flow

1. A domain workspace receives an updated requirement or source.
2. It checks the change against current state and historical decisions.
3. It updates the authoritative record and retains relevant supersession history.
4. An authorized handoff passes the changed demand to scheduling.
5. The scheduler examines capacity, competing priorities, and protected commitments.
6. Approved changes are executed through the relevant tools, with result checks.
7. State records distinguish scheduled, performed, and verified outcomes.

The workflow is coordinated through documented procedures and AI-assisted interactions, with explicit human decisions and tool-based steps.

## Quality assurance

The framework applies source freshness checks, contradiction detection, scope and authorization controls, pre/post-change verification, and targeted recovery when an error occurs. Historical correction records informed refinements to these procedures.

## Implementation and demonstration tools

The framework uses ChatGPT workspaces, structured text records, file-management capabilities, and scheduling tools. The included Python models reproduce selected scheduling and context-selection rules using fictional test fixtures, providing a reproducible way to inspect the decision logic described in the case studies.

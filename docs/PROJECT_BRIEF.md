# Project overview | AI-Assisted Operations & Knowledge Management Framework

**Independent systems-design project | 2026–present**

## The challenge

Managing coursework, career development, student leadership, and independent projects across different conversations, documents, and calendars created an information problem. Requirements changed in one place, but planning elsewhere could still reflect older decisions. It was also difficult to establish which action had merely been planned and which had actually been carried out.

## My solution

I designed and iteratively refined an AI-assisted operations framework that maintains clear ownership of each workstream's requirements while coordinating changes across shared processes.

I organized information into three layers—current state, decision history, and original evidence—and established procedures for verifying sources, handling updated requirements, coordinating scheduling decisions, and checking the results of authorized actions.

## Design choices that matter

- **Keep each workstream accountable for its information.** Shared coordination follows the latest verified owner requirement.
- **Preserve the reasoning behind changes.** Current decisions stay accessible, while superseded requirements and primary sources remain traceable.
- **Separate planning from execution.** Proposed, authorized, scheduled, completed, and verified are different statuses.
- **Improve the process when it fails.** A historical context-selection error informed revisions to how the framework interprets continuation requests and action authority.

## What this looks like

In a fictional, reproducible scenario, a project deadline moves up two days. The A01 model verifies the revised deadline, identifies work periods around fixed commitments, waits for approval, and keeps task-completion status separate from scheduling. Its 10 automated tests passed.

A second case study, B01, documents how I analyzed a real continuity error and refined the procedures for selecting historical context and determining which actions are authorized. A companion fictional model passed 11 automated tests.

[Read A01](A01_WORKFLOW.md) · [Read B01](B01_FAILURE_AND_RECOVERY.md)

## Professional relevance

This project illustrates my ability to identify operational friction, translate it into requirements, design connected processes, establish information ownership, diagnose failures, and improve a system through iteration and verification.

## Interview explanation (60–90 seconds)

> I designed an AI-assisted operations framework because I was managing multiple projects and commitments across different workspaces, documents, and calendars. A requirement could change in one place while another plan still relied on the old version. I organized the system around three layers: what is current, the history behind decisions, and the original evidence. Each workstream owns its requirements, while shared procedures verify important changes and coordinate them with scheduling. For example, if a project deadline moves, the system's rules are designed to check the new source, account for existing commitments, and distinguish time scheduled from work completed. I also refined the framework after a real continuity error exposed a weakness in selecting the right historical context. The project reflects the kind of work I enjoy: understanding an operations problem, designing a practical system, and improving it as I learn from use.

## Methods

The framework evolved through design, operational use, record review, and correction of observed problems. The repository includes two fictional Python reference models with 21 passing automated tests to make selected design decisions inspectable.

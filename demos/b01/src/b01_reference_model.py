"""B01: a deliberately narrow continuation and authorization decision table.

The model tests wording against a known, fictionalized continuity incident.
It does not interpret arbitrary natural language or act on external accounts.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Context:
    selected_topic: str | None = None
    previous_explicit_topic: str | None = None
    post_protocol_topic: str | None = None
    has_competing_referents: bool = True
    action_authorized: bool = False


def _result(status: str, topic: str | None = None, action: str = "NONE") -> dict:
    return {
        "status": status,
        "topic": topic,
        "permitted_action": action,
        "notes": (
            "A historical reference does not authorize unrelated external actions."
            if status == "CONTEXT_RESOLVED"
            else "Use the user's present request and its actual authorization boundaries."
        ),
    }


def _resolved(topic: str, context: Context) -> dict:
    return _result(
        "CONTEXT_RESOLVED",
        topic,
        "USER_AUTHORIZED_SCOPE_ONLY" if context.action_authorized else "REVIEW_ONLY",
    )


def select_resume_topic(request: str, context: Context) -> dict:
    """Apply explicit, ordered rules to avoid choosing a nearby wrong thread.

    Decision table:
      1. An explicit new work request is not a continuation request.
      2. A named historical point wins over generic recent-work context.
      3. 'After the protocol' needs a known post-protocol anchor.
      4. A specified scheduler handoff is its own topic.
      5. An unspecified continuation uses selected context only if unambiguous.
      6. Otherwise clarify without acting.
    """
    q = " ".join(request.casefold().split())
    if not q:
        return _result("CLARIFICATION_REQUIRED")

    # A document titled 'resume' is not the verb 'resume a conversation'.
    new_work = re.match(
        r"^(?:please\s+|can you\s+|could you\s+)?"
        r"(?:update|edit|revise|fix|write|draft|create|submit|apply|"
        r"schedule|send|delete|build)\b",
        q,
    )
    if new_work or re.search(r"\breview\s+(?:my|the)\s+(?:resume|cv|portfolio)\b", q):
        return _result("NEW_REQUEST", action="USER_REQUESTED_SCOPE_ONLY")

    protocol = bool(
        re.search(r"\b(?:ucp|continuity protocol|protocol discussion|the protocol)\b", q)
    )
    literal_end = bool(
        re.search(r"\b(?:literal|exact)\s+(?:end|ending|last\s+(?:reply|message))\b", q)
        or re.search(r"\b(?:last|final)\s+(?:message|reply|exchange)\b", q)
    )
    original_parent = bool(re.search(r"\b(?:original parent|parent chat|parent conversation)\b", q))
    before = bool(re.search(r"\b(?:before|prior to|earlier than)\b", q))
    after = bool(re.search(r"\bafter\b", q))

    if original_parent and literal_end:
        return _resolved("UCP_VALIDATION", context)

    if protocol and before:
        return _resolved("APG_POST_DESIGN_EXECUTION", context)

    if protocol and after:
        if context.post_protocol_topic:
            return _resolved(context.post_protocol_topic, context)
        return _result("CLARIFICATION_REQUIRED")

    if "scheduler" in q and "handoff" in q:
        return _resolved("SCHEDULER_HANDOFF_STATUS", context)

    if re.search(r"\bapg\b|\bacademic professional growth\b", q):
        topic = context.selected_topic or context.previous_explicit_topic
        if topic and topic.startswith("APG_"):
            return _resolved(topic, context)
        return _result("CLARIFICATION_REQUIRED")

    continuation = bool(
        re.search(r"\b(?:resume|continue|pick up|return to|go back|where we left off)\b", q)
    )
    if continuation:
        if context.selected_topic is not None:
            return _resolved(context.selected_topic, context)
        if not context.has_competing_referents and context.previous_explicit_topic:
            return _resolved(context.previous_explicit_topic, context)

    return _result("CLARIFICATION_REQUIRED")


def run_fixture(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return [
        {
            "case": case["name"],
            "request": case["request"],
            "result": select_resume_topic(case["request"], Context(**case["context"])),
        }
        for case in data["cases"]
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture")
    args = parser.parse_args()
    print(json.dumps({"scenarios": run_fixture(args.fixture)}, indent=2))

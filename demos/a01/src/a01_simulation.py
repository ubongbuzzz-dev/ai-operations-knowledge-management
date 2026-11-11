"""A01: isolated synthetic model of documented continuity-system governance rules.

A focused deterministic example of scheduling and source-governance rules.
It runs locally with fictional data.
"""
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Optional
import json

@dataclass(frozen=True)
class Source:
    source_id: str
    deadline: str
    revision: int
    verified: bool
    authority: str = "project_owner"

@dataclass(frozen=True)
class CalendarBlock:
    start: str
    end: str
    label: str
    protected: bool = True

class SimulatedWriteError(Exception):
    pass

def resolve_deadline(sources: list[Source]) -> dict:
    authoritative = [s for s in sources if s.authority == "project_owner" and s.verified]
    if not authoritative:
        return {"status": "BLOCKED_UNVERIFIED_SOURCE", "selected": None}
    winner = max(authoritative, key=lambda s: s.revision)
    # A newer, unverified owner revision blocks silent promotion of an older date.
    if any(s.authority == "project_owner" and s.revision > winner.revision for s in sources):
        return {"status": "BLOCKED_NEWER_UNVERIFIED", "selected": None}
    return {"status": "RESOLVED", "selected": asdict(winner)}

def overlap(a: CalendarBlock, b: CalendarBlock) -> bool:
    return a.start < b.end and b.start < a.end

def propose_blocks(date: str, existing: list[CalendarBlock], needed_minutes=120, start_hour=9, end_hour=18) -> dict:
    """Find slots on one synthetic day, retaining all existing commitments."""
    for b in existing:
        if b.start >= b.end:
            return {"status": "INVALID_INPUT", "proposals": []}
    proposals = []
    cursor = datetime.fromisoformat(f"{date}T{start_hour:02d}:00")
    stop = datetime.fromisoformat(f"{date}T{end_hour:02d}:00")
    remaining = needed_minutes
    while cursor < stop and remaining > 0:
        nxt = min(cursor + timedelta(minutes=60), stop)
        proposal = CalendarBlock(cursor.isoformat(timespec="minutes"), nxt.isoformat(timespec="minutes"), "Project Alpha work", False)
        if not any(overlap(proposal, b) for b in existing + proposals):
            proposals.append(proposal)
            remaining -= int((nxt-cursor).total_seconds() / 60)
        cursor = nxt
    if remaining > 0:
        return {"status": "INSUFFICIENT_CAPACITY", "proposals": [], "remaining_minutes": remaining}
    return {"status": "PROPOSED", "proposals": [asdict(p) for p in proposals], "remaining_minutes": 0}

def run_case(old: Source, new: Source, existing: list[CalendarBlock], *, authorized=False, commit=False, simulate_write_failure=False, needed_minutes=120) -> dict:
    source_decision = resolve_deadline([old, new])
    report = {"source_decision": source_decision, "historical_deadline": old.deadline, "current_deadline": None, "proposed_blocks": [], "committed_blocks": [], "task_status": "NOT_COMPLETED", "existing_preserved": True, "events": []}
    if source_decision["status"] != "RESOLVED":
        report["status"] = source_decision["status"]
        return report
    selected = source_decision["selected"]
    report["current_deadline"] = selected["deadline"]
    report["events"].append(f"Owner revision {selected['revision']} selected; earlier deadline kept as history")
    result = propose_blocks(selected["deadline"], existing, needed_minutes=needed_minutes)
    if result["status"] != "PROPOSED":
        report["status"] = result["status"]
        report["events"].append("Unmet capacity escalated; no existing commitments displaced")
        return report
    report["proposed_blocks"] = result["proposals"]
    if not authorized:
        report["status"] = "AWAITING_AUTHORIZATION"
        report["events"].append("No changes committed without authorization")
        return report
    if not commit:
        report["status"] = "AUTHORIZED_PROPOSAL_ONLY"
        return report
    # Stage the simulated commit; validate state before reporting it as committed.
    staged = [CalendarBlock(**b) for b in result["proposals"]]
    if any(overlap(s, e) for s in staged for e in existing):
        report["status"] = "BLOCKED_CONFLICT"
        return report
    try:
        if simulate_write_failure:
            raise SimulatedWriteError("synthetic persistence failure")
        combined = existing + staged
        # in-memory consistency check
        if len(combined) != len(existing) + len(staged):
            raise SimulatedWriteError("synthetic read-back failed")
    except SimulatedWriteError:
        report["status"] = "WRITE_FAILED_NO_COMMIT"
        report["events"].append("Synthetic write failed; no committed blocks reported")
        return report
    report["status"] = "SYNTHETIC_COMMIT_VERIFIED"
    report["committed_blocks"] = [asdict(b) for b in staged]
    report["events"].append("Synthetic commit and in-memory consistency checks passed")
    return report

def load_fixture(path):
    with open(path, encoding="utf-8") as f: data = json.load(f)
    return Source(**data["old_source"]), Source(**data["new_source"]), [CalendarBlock(**b) for b in data["existing_blocks"]]

if __name__ == "__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("fixture")
    p.add_argument("--authorized",action="store_true")
    p.add_argument("--commit",action="store_true")
    p.add_argument("--write-fail",action="store_true")
    args=p.parse_args()
    old,new,blocks=load_fixture(args.fixture)
    print(json.dumps(run_case(old,new,blocks,authorized=args.authorized,commit=args.commit,simulate_write_failure=args.write_fail),indent=2))

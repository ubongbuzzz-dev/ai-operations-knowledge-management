"""A01: a small, in-memory example of deadline and scheduling controls.

All inputs are fictional. No calendar API or durable storage is modified.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta


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
    """A simulated calendar write failed."""


class InMemoryCalendar:
    """Store blocks separately from the proposals; return copies on read-back."""

    def __init__(self, existing: list[CalendarBlock]):
        self._blocks = list(existing)

    def read_back(self) -> list[CalendarBlock]:
        return list(self._blocks)

    def write(self, blocks: list[CalendarBlock]) -> None:
        self._blocks = list(blocks)


def _valid_day(value: str) -> bool:
    try:
        return date.fromisoformat(value).isoformat() == value
    except (TypeError, ValueError):
        return False


def _parse_block(block: CalendarBlock) -> tuple[datetime, datetime] | None:
    try:
        start = datetime.fromisoformat(block.start)
        end = datetime.fromisoformat(block.end)
        if start.tzinfo is not None or end.tzinfo is not None or start >= end:
            return None
        return start, end
    except (AttributeError, TypeError, ValueError):
        return None


def resolve_deadline(sources: list[Source]) -> dict:
    """Require one unambiguous latest verified owner deadline."""
    if not sources or any(
        not _valid_day(s.deadline) or type(s.revision) is not int or s.revision < 0
        for s in sources
    ):
        return {"status": "INVALID_INPUT", "selected": None}

    owner_sources = [s for s in sources if s.authority == "project_owner"]
    verified = [s for s in owner_sources if s.verified]
    if not verified:
        return {"status": "BLOCKED_UNVERIFIED_SOURCE", "selected": None}

    latest_verified_revision = max(s.revision for s in verified)
    if any(s.revision > latest_verified_revision for s in owner_sources):
        return {"status": "BLOCKED_NEWER_UNVERIFIED", "selected": None}

    latest = [s for s in owner_sources if s.revision == latest_verified_revision]
    if len({s.deadline for s in latest}) > 1:
        return {"status": "BLOCKED_CONFLICTING_OWNER_REVISION", "selected": None}

    selected = min((s for s in latest if s.verified), key=lambda s: s.source_id)
    return {"status": "RESOLVED", "selected": asdict(selected)}


def overlap(a: CalendarBlock, b: CalendarBlock) -> bool:
    a_times, b_times = _parse_block(a), _parse_block(b)
    if a_times is None or b_times is None:
        raise ValueError("Cannot compare invalid calendar blocks")
    return a_times[0] < b_times[1] and b_times[0] < a_times[1]


def propose_blocks(
    day: str,
    existing: list[CalendarBlock],
    needed_minutes: int = 120,
    start_hour: int = 9,
    end_hour: int = 18,
) -> dict:
    """Fill free intervals on one day without moving existing commitments.

    This models a 9 a.m.–6 p.m. deadline-day window, not advance scheduling
    across multiple days or a verified due time.
    """
    if (
        not _valid_day(day)
        or type(needed_minutes) is not int
        or needed_minutes <= 0
        or type(start_hour) is not int
        or type(end_hour) is not int
        or not 0 <= start_hour < end_hour <= 24
    ):
        return {"status": "INVALID_INPUT", "proposals": []}

    intervals = [_parse_block(block) for block in existing]
    if any(interval is None for interval in intervals):
        return {"status": "INVALID_INPUT", "proposals": []}

    opening = datetime.fromisoformat(f"{day}T00:00") + timedelta(hours=start_hour)
    closing = datetime.fromisoformat(f"{day}T00:00") + timedelta(hours=end_hour)
    busy = sorted(
        (max(start, opening), min(end, closing))
        for start, end in intervals
        if end > opening and start < closing
    )

    cursor, remaining, proposals = opening, needed_minutes, []
    while cursor < closing and remaining > 0:
        covering = [end for start, end in busy if start <= cursor < end]
        if covering:
            cursor = max(covering)  # Jump directly to the blocking commitment's end.
            continue

        next_busy = min((start for start, _ in busy if start > cursor), default=closing)
        free_minutes = int((min(next_busy, closing) - cursor).total_seconds() // 60)
        if free_minutes <= 0:
            break

        take = min(60, remaining, free_minutes)
        end = cursor + timedelta(minutes=take)
        proposals.append(
            CalendarBlock(
                cursor.isoformat(timespec="minutes"),
                end.isoformat(timespec="minutes"),
                "Project Alpha work",
                False,
            )
        )
        remaining -= take
        cursor = end

    if remaining:
        return {
            "status": "INSUFFICIENT_CAPACITY",
            "proposals": [],
            "remaining_minutes": remaining,
        }
    return {
        "status": "PROPOSED",
        "proposals": [asdict(block) for block in proposals],
        "remaining_minutes": 0,
    }


def run_case(
    old: Source,
    new: Source,
    existing: list[CalendarBlock],
    *,
    authorized: bool = False,
    commit: bool = False,
    simulate_write_failure: bool = False,
    simulate_readback_corruption: bool = False,
    concurrent_block: CalendarBlock | None = None,
    needed_minutes: int = 120,
) -> dict:
    """Propose, optionally write, then independently read back an in-memory copy."""
    calendar = InMemoryCalendar(existing)
    decision = resolve_deadline([old, new])
    report = {
        "source_decision": decision,
        "historical_deadline": old.deadline,
        "current_deadline": None,
        "proposed_blocks": [],
        "committed_blocks": [],
        "task_status": "NOT_COMPLETED",
        "existing_preserved": None,
        "events": [],
    }

    def finish(status: str) -> dict:
        report["status"] = status
        report["existing_preserved"] = (
            calendar.read_back()[: len(existing)] == list(existing)
        )
        return report

    if decision["status"] != "RESOLVED":
        return finish(decision["status"])

    selected = decision["selected"]
    report["current_deadline"] = selected["deadline"]
    report["events"].append(
        f"Verified owner revision {selected['revision']} selected; old deadline retained as history"
    )
    proposed = propose_blocks(
        selected["deadline"], existing, needed_minutes=needed_minutes
    )
    if proposed["status"] != "PROPOSED":
        report["events"].append("No commitments moved; capacity or input escalated")
        return finish(proposed["status"])

    report["proposed_blocks"] = proposed["proposals"]
    if not authorized:
        report["events"].append("No calendar change without authorization")
        return finish("AWAITING_AUTHORIZATION")
    if not commit:
        return finish("AUTHORIZED_PROPOSAL_ONLY")

    staged = [CalendarBlock(**block) for block in proposed["proposals"]]
    if concurrent_block is not None:
        if _parse_block(concurrent_block) is None:
            return finish("INVALID_INPUT")
        # Another writer changes the in-memory calendar after the proposal.
        calendar.write(calendar.read_back() + [concurrent_block])

    observed_before = calendar.read_back()
    if any(overlap(s, e) for s in staged for e in observed_before):
        report["events"].append("Calendar changed since proposal; commit refused")
        return finish("BLOCKED_CONFLICT")

    try:
        if simulate_write_failure:
            raise SimulatedWriteError("Simulated in-memory write failed")
        expected = observed_before + staged
        calendar.write(expected)
        if simulate_readback_corruption:
            calendar.write(expected[:-1])  # Fault injection, not normal behavior.
        actual = calendar.read_back()
        if actual != expected or actual[: len(existing)] != list(existing):
            calendar.write(observed_before)  # Roll back the failed simulation.
            report["events"].append("In-memory read-back mismatch; write rolled back")
            return finish("WRITE_VERIFICATION_FAILED")
    except SimulatedWriteError:
        report["events"].append("Simulated write failed; no committed blocks reported")
        return finish("WRITE_FAILED_NO_COMMIT")

    report["committed_blocks"] = [asdict(block) for block in actual[len(observed_before) :]]
    report["events"].append("In-memory calendar write read back and matched exactly")
    return finish("SYNTHETIC_COMMIT_VERIFIED")


def load_fixture(path: str):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return (
        Source(**data["old_source"]),
        Source(**data["new_source"]),
        [CalendarBlock(**block) for block in data["existing_blocks"]],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture")
    parser.add_argument("--authorized", action="store_true")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--write-fail", action="store_true")
    parser.add_argument("--readback-fail", action="store_true")
    args = parser.parse_args()
    old_source, new_source, calendar_blocks = load_fixture(args.fixture)
    print(
        json.dumps(
            run_case(
                old_source,
                new_source,
                calendar_blocks,
                authorized=args.authorized,
                commit=args.commit,
                simulate_write_failure=args.write_fail,
                simulate_readback_corruption=args.readback_fail,
            ),
            indent=2,
        )
    )

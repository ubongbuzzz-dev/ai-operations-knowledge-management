"""Behavioral checks for A01, including cases missing from the original suite."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from a01_simulation import (  # noqa: E402
    CalendarBlock,
    Source,
    load_fixture,
    overlap,
    propose_blocks,
    resolve_deadline,
    run_case,
)

ROOT = Path(__file__).resolve().parents[1]


class A01Tests(unittest.TestCase):
    def setUp(self):
        self.old, self.new, self.blocks = load_fixture(
            ROOT / "fixtures" / "a01_fictional_scenario.json"
        )

    def test_latest_verified_owner_source_selected(self):
        result = run_case(self.old, self.new, self.blocks)
        self.assertEqual(result["current_deadline"], "2026-11-18")
        self.assertEqual(result["historical_deadline"], "2026-11-20")

    def test_unverified_owner_source_rejected(self):
        sources = [Source("unverified", "2026-11-18", 1, False)]
        self.assertEqual(
            resolve_deadline(sources)["status"], "BLOCKED_UNVERIFIED_SOURCE"
        )

    def test_newer_unverified_revision_blocks_older_verified(self):
        newer = Source("owner-r3", "2026-11-17", 3, False)
        self.assertEqual(
            resolve_deadline([self.old, newer])["status"],
            "BLOCKED_NEWER_UNVERIFIED",
        )

    def test_equal_revision_different_deadlines_blocked_in_either_order(self):
        left = Source("owner-a", "2026-11-18", 2, True)
        right = Source("owner-b", "2026-11-19", 2, True)
        for sources in ([left, right], [right, left]):
            with self.subTest(order=sources[0].source_id):
                self.assertEqual(
                    resolve_deadline(sources)["status"],
                    "BLOCKED_CONFLICTING_OWNER_REVISION",
                )

    def test_equal_revision_unverified_disagreement_not_ignored(self):
        left = Source("owner-a", "2026-11-18", 2, True)
        right = Source("owner-b", "2026-11-19", 2, False)
        self.assertEqual(
            resolve_deadline([left, right])["status"],
            "BLOCKED_CONFLICTING_OWNER_REVISION",
        )

    def test_equal_revision_same_deadline_accepted(self):
        twin = Source("owner-r2-copy", "2026-11-18", 2, True)
        self.assertEqual(
            resolve_deadline([self.new, twin])["status"], "RESOLVED"
        )

    def test_non_owner_cannot_override_owner(self):
        outsider = Source("outside", "2026-11-15", 99, True, "untrusted")
        self.assertEqual(
            resolve_deadline([self.old, outsider])["selected"]["deadline"],
            "2026-11-20",
        )

    def test_bad_source_day_rejected(self):
        invalid = Source("owner", "2026-11-31", 2, True)
        self.assertEqual(
            resolve_deadline([self.old, invalid])["status"], "INVALID_INPUT"
        )

    def test_no_unauthorized_commit(self):
        result = run_case(self.old, self.new, self.blocks)
        self.assertEqual(result["status"], "AWAITING_AUTHORIZATION")
        self.assertEqual(result["committed_blocks"], [])
        self.assertTrue(result["existing_preserved"])

    def test_approval_alone_does_not_commit(self):
        result = run_case(self.old, self.new, self.blocks, authorized=True)
        self.assertEqual(result["status"], "AUTHORIZED_PROPOSAL_ONLY")
        self.assertEqual(result["committed_blocks"], [])

    def test_authorized_commit_read_back_and_task_not_completed(self):
        result = run_case(self.old, self.new, self.blocks, authorized=True, commit=True)
        self.assertEqual(result["status"], "SYNTHETIC_COMMIT_VERIFIED")
        self.assertEqual(len(result["committed_blocks"]), 2)
        self.assertEqual(result["task_status"], "NOT_COMPLETED")
        self.assertTrue(result["existing_preserved"])
        for proposal in result["committed_blocks"]:
            self.assertFalse(
                any(overlap(CalendarBlock(**proposal), block) for block in self.blocks)
            )

    def test_simulated_write_error_cannot_report_success(self):
        result = run_case(
            self.old,
            self.new,
            self.blocks,
            authorized=True,
            commit=True,
            simulate_write_failure=True,
        )
        self.assertEqual(result["status"], "WRITE_FAILED_NO_COMMIT")
        self.assertEqual(result["committed_blocks"], [])
        self.assertTrue(result["existing_preserved"])

    def test_corrupted_readback_rejected_and_rolled_back(self):
        result = run_case(
            self.old,
            self.new,
            self.blocks,
            authorized=True,
            commit=True,
            simulate_readback_corruption=True,
        )
        self.assertEqual(result["status"], "WRITE_VERIFICATION_FAILED")
        self.assertEqual(result["committed_blocks"], [])
        self.assertTrue(result["existing_preserved"])

    def test_concurrent_calendar_edit_is_checked_before_commit(self):
        concurrent = CalendarBlock(
            "2026-11-18T11:30", "2026-11-18T11:45", "New protected meeting"
        )
        result = run_case(
            self.old,
            self.new,
            self.blocks,
            authorized=True,
            commit=True,
            concurrent_block=concurrent,
        )
        self.assertEqual(result["status"], "BLOCKED_CONFLICT")
        self.assertEqual(result["committed_blocks"], [])
        self.assertTrue(result["existing_preserved"])

    def test_window_uses_early_free_minute_even_if_not_on_hour(self):
        busy = [
            CalendarBlock("2026-11-18T09:00", "2026-11-18T09:30", "Meeting"),
            CalendarBlock("2026-11-18T11:00", "2026-11-18T18:00", "Other work"),
        ]
        result = propose_blocks("2026-11-18", busy, needed_minutes=90)
        self.assertEqual(result["status"], "PROPOSED")
        self.assertEqual(result["proposals"][0]["start"], "2026-11-18T09:30")
        self.assertEqual(result["proposals"][-1]["end"], "2026-11-18T11:00")
        self.assertEqual(len(result["proposals"]), 2)

    def test_short_task_reserves_only_needed_minutes(self):
        result = propose_blocks("2026-11-18", [], needed_minutes=15)
        self.assertEqual(result["status"], "PROPOSED")
        self.assertEqual(result["proposals"][0]["start"], "2026-11-18T09:00")
        self.assertEqual(result["proposals"][0]["end"], "2026-11-18T09:15")

    def test_overlapping_existing_blocks_are_not_moved(self):
        busy = [
            CalendarBlock("2026-11-18T09:00", "2026-11-18T10:00", "Meeting A"),
            CalendarBlock("2026-11-18T09:30", "2026-11-18T11:00", "Meeting B"),
        ]
        before = list(busy)
        result = propose_blocks("2026-11-18", busy, needed_minutes=30)
        self.assertEqual(result["proposals"][0]["start"], "2026-11-18T11:00")
        self.assertEqual(busy, before)

    def test_capacity_failure_does_not_return_partial_commit(self):
        result = run_case(
            self.old, self.new, self.blocks, authorized=True, commit=True,
            needed_minutes=500
        )
        self.assertEqual(result["status"], "INSUFFICIENT_CAPACITY")
        self.assertEqual(result["proposed_blocks"], [])
        self.assertEqual(result["committed_blocks"], [])

    def test_invalid_block_and_zero_minutes_rejected(self):
        invalid = [CalendarBlock("2026-11-18T16:00", "2026-11-18T15:00", "Invalid")]
        self.assertEqual(
            propose_blocks("2026-11-18", invalid)["status"], "INVALID_INPUT"
        )
        self.assertEqual(
            propose_blocks("2026-11-18", [], needed_minutes=0)["status"],
            "INVALID_INPUT",
        )

    def test_time_not_in_same_day_does_not_reduce_capacity(self):
        prior = [CalendarBlock("2026-11-17T09:00", "2026-11-17T17:00", "Yesterday")]
        result = propose_blocks("2026-11-18", prior, needed_minutes=120)
        self.assertEqual(result["status"], "PROPOSED")


if __name__ == "__main__":
    unittest.main(verbosity=2)

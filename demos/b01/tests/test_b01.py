"""B01 tests use cases defined outside of the implementation itself."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from b01_reference_model import Context, run_fixture, select_resume_topic  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


class B01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_path = ROOT / "fixtures" / "b01_synthetic_cases.json"
        with open(cls.fixture_path, encoding="utf-8") as handle:
            cls.cases = json.load(handle)["cases"]

    def test_external_plain_language_cases(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                result = select_resume_topic(
                    case["request"], Context(**case["context"])
                )
                self.assertEqual(result["status"], case["expected_status"])
                self.assertEqual(result["topic"], case["expected_topic"])
                self.assertEqual(
                    result["permitted_action"], case["expected_action"]
                )

    def test_no_automatic_external_action_on_unselected_continuation(self):
        result = select_resume_topic(
            "Continue where we left off",
            Context(previous_explicit_topic="APG_POST_DESIGN_EXECUTION"),
        )
        self.assertEqual(result["status"], "CLARIFICATION_REQUIRED")
        self.assertEqual(result["permitted_action"], "NONE")

    def test_active_topic_does_not_displace_an_explicit_historical_anchor(self):
        result = select_resume_topic(
            "Go back to what we were doing before the protocol discussion",
            Context(selected_topic="CURRENT_OTHER_TASK"),
        )
        self.assertEqual(result["topic"], "APG_POST_DESIGN_EXECUTION")

    def test_after_protocol_never_silently_becomes_before_protocol(self):
        result = select_resume_topic(
            "Return to APG after UCP",
            Context(previous_explicit_topic="APG_POST_DESIGN_EXECUTION"),
        )
        self.assertNotEqual(result["topic"], "APG_POST_DESIGN_EXECUTION")

    def test_new_work_request_is_not_misread_as_conversation_resume(self):
        result = select_resume_topic(
            "Update my resume", Context(selected_topic="APG_POST_DESIGN_EXECUTION")
        )
        self.assertEqual(result["status"], "NEW_REQUEST")
        self.assertIsNone(result["topic"])

    def test_fixture_runner_keeps_cases_and_results_separate(self):
        results = run_fixture(self.fixture_path)
        self.assertEqual(len(results), len(self.cases))
        self.assertEqual(results[0]["request"], self.cases[0]["request"])
        self.assertNotIn("expected_status", results[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)

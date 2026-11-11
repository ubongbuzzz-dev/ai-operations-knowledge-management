import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from b01_reference_model import Context, select_resume_topic, evaluate_claims

class B01Tests(unittest.TestCase):
    def test_literal_end_maps_to_ucp(self):
        self.assertEqual(select_resume_topic("Continue original parent at its literal end",Context())["topic"],"UCP_VALIDATION")
    def test_before_ucp_maps_to_apg(self):
        self.assertEqual(select_resume_topic("resume before all the UCP stuff",Context())["topic"],"APG_POST_DESIGN_EXECUTION")
    def test_ambiguous_no_selection_requires_clarification(self):
        self.assertEqual(select_resume_topic("continue where we left off",Context(previous_explicit_topic="APG_POST_DESIGN_EXECUTION"))["status"],"CLARIFICATION_REQUIRED")
    def test_immediate_selected_topic_used(self):
        self.assertEqual(select_resume_topic("continue where we left off",Context(selected_topic="USER_CURRENT_PROJECT"))["topic"],"USER_CURRENT_PROJECT")
    def test_no_invented_action_authorization(self):
        self.assertEqual(select_resume_topic("return to APG work",Context())["permitted_action"],"REVIEW_ONLY")
    def test_authorization_keeps_scope_bound(self):
        self.assertEqual(select_resume_topic("return to APG work",Context(action_authorized=True))["permitted_action"],"USER_AUTHORIZED_SCOPE_ONLY")
    def test_scheduler_is_distinct_referent(self):
        self.assertEqual(select_resume_topic("Check scheduler handoff",Context())["topic"],"SCHEDULER_HANDOFF_STATUS")
    def test_blank_requires_clarification(self):
        self.assertEqual(select_resume_topic("",Context())["status"],"CLARIFICATION_REQUIRED")
    def test_historical_record_not_live_validation(self):
        result=evaluate_claims([{"claim_id":"x","source_type":"historical_record","contains_private_data":True}])[0]
        self.assertFalse(result["is_live_behavior_verified"])
        self.assertFalse(result["public_ready"])
    def test_synthetic_not_live_validation(self):
        result=evaluate_claims([{"claim_id":"x","source_type":"synthetic_test","contains_private_data":False}])[0]
        self.assertFalse(result["is_live_behavior_verified"])
        self.assertTrue(result["public_ready"])
    def test_unknown_evidence_type_rejected(self):
        with self.assertRaises(ValueError): evaluate_claims([{"claim_id":"x","source_type":"definitely_proven"}])

if __name__=="__main__": unittest.main()

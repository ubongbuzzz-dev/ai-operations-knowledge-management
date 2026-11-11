import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from a01_simulation import Source,CalendarBlock,run_case,load_fixture,resolve_deadline,propose_blocks,overlap

ROOT=Path(__file__).resolve().parents[1]

class A01Tests(unittest.TestCase):
    def setUp(self):
        self.old,self.new,self.blocks=load_fixture(ROOT/"fixtures"/"a01_fictional_scenario.json")
    def test_new_verified_owner_source_selected(self):
        r=run_case(self.old,self.new,self.blocks)
        self.assertEqual(r["current_deadline"],"2026-11-18")
        self.assertEqual(r["historical_deadline"],"2026-11-20")
    def test_no_unauthorized_commit(self):
        r=run_case(self.old,self.new,self.blocks)
        self.assertEqual(r["status"],"AWAITING_AUTHORIZATION")
        self.assertEqual(r["committed_blocks"],[])
    def test_synthetic_authorized_commit_and_readback(self):
        r=run_case(self.old,self.new,self.blocks,authorized=True,commit=True)
        self.assertEqual(r["status"],"SYNTHETIC_COMMIT_VERIFIED")
        self.assertEqual(len(r["committed_blocks"]),2)
        for p in r["committed_blocks"]:
            self.assertFalse(any(overlap(CalendarBlock(**p),b) for b in self.blocks))
    def test_task_not_falsely_completed(self):
        r=run_case(self.old,self.new,self.blocks,authorized=True,commit=True)
        self.assertEqual(r["task_status"],"NOT_COMPLETED")
    def test_newer_unverified_source_blocks_promotion(self):
        new=Source("alpha-owner-r2","2026-11-18",2,False)
        r=run_case(self.old,new,self.blocks,authorized=True,commit=True)
        self.assertEqual(r["status"],"BLOCKED_NEWER_UNVERIFIED")
        self.assertFalse(r["committed_blocks"])
    def test_non_owner_does_not_override_verified_owner(self):
        outsider=Source("random-note","2026-11-18",99,True,"untrusted")
        self.assertEqual(resolve_deadline([self.old,outsider])["selected"]["deadline"],"2026-11-20")
    def test_insufficient_capacity_preserves_existing(self):
        r=run_case(self.old,self.new,self.blocks,authorized=True,commit=True,needed_minutes=500)
        self.assertEqual(r["status"],"INSUFFICIENT_CAPACITY")
        self.assertEqual(r["committed_blocks"],[])
    def test_synthetic_write_failure_cannot_claim_success(self):
        r=run_case(self.old,self.new,self.blocks,authorized=True,commit=True,simulate_write_failure=True)
        self.assertEqual(r["status"],"WRITE_FAILED_NO_COMMIT")
        self.assertEqual(r["committed_blocks"],[])
    def test_proposals_do_not_conflict_with_existing(self):
        r=run_case(self.old,self.new,self.blocks)
        for p in r["proposed_blocks"]:
            self.assertFalse(any(overlap(CalendarBlock(**p),b) for b in self.blocks))
    def test_invalid_input_rejected(self):
        invalid=[CalendarBlock("2026-11-18T16:00","2026-11-18T15:00","invalid")]
        self.assertEqual(propose_blocks("2026-11-18",invalid)["status"],"INVALID_INPUT")

if __name__=='__main__':unittest.main(verbosity=2)

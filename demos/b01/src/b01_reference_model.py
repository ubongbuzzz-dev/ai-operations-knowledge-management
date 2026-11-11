"""B01: local reference model illustrating context selection and authorization."""
from dataclasses import dataclass
import json

@dataclass(frozen=True)
class Context:
    selected_topic: str | None = None
    previous_explicit_topic: str | None = None
    has_competing_referents: bool = True
    action_authorized: bool = False


def select_resume_topic(request: str, context: Context) -> dict:
    """Deterministic, minimal interpretation of documented corrective policy."""
    q = request.lower().strip()
    if not q:
        return {"status":"CLARIFICATION_REQUIRED","topic":None,"permitted_action":"NONE"}
    if "literal end" in q or ("original parent" in q and "end" in q):
        topic = "UCP_VALIDATION"
    elif "before ucp" in q or "before all the ucp" in q or "return to apg" in q:
        topic = "APG_POST_DESIGN_EXECUTION"
    elif "scheduler" in q and "handoff" in q:
        topic = "SCHEDULER_HANDOFF_STATUS"
    elif "where we left off" in q or "resume" in q or "continue" in q:
        topic = context.selected_topic or context.previous_explicit_topic
        if topic is None or (context.has_competing_referents and context.selected_topic is None):
            return {"status":"CLARIFICATION_REQUIRED","topic":None,"permitted_action":"NONE"}
    else:
        return {"status":"CLARIFICATION_REQUIRED","topic":None,"permitted_action":"NONE"}
    return {"status":"CONTEXT_RESOLVED", "topic": topic,
            "permitted_action": "REVIEW_ONLY" if not context.action_authorized else "USER_AUTHORIZED_SCOPE_ONLY",
            "notes":"Resuming a topic is not authorization for external application/calendar actions."}


def evaluate_claims(claims: list[dict]) -> list[dict]:
    """Preserve evidence classification; deliberately never infer 'tested' from 'documented'."""
    permitted = {"historical_record", "owner_report", "synthetic_test", "not_verified"}
    out = []
    for c in claims:
        source = c.get("source_type")
        if source not in permitted:
            raise ValueError("Unsupported evidence class")
        out.append({"claim_id":c["claim_id"], "evidence_class":source,
                    "is_live_behavior_verified":False,
                    "public_ready":source=="synthetic_test" and c.get("contains_private_data") is False})
    return out

if __name__ == "__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("fixture")
    args=p.parse_args()
    with open(args.fixture, encoding="utf-8") as f: data=json.load(f)
    ctx=Context(**data["context"])
    print(json.dumps({"scenarios":[{"request":s,"result":select_resume_topic(s,ctx)} for s in data["requests"]],
      "claim_review":evaluate_claims(data["claims"])}, indent=2))

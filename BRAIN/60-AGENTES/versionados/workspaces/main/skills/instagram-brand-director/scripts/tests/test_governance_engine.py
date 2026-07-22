#!/usr/bin/env python3
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from governance_engine import evaluate
from runtime_lib import request_hash

BASE=Path(__file__).resolve().parents[2]
GOV={"external_action_lock":True,"owner":{"role":"proprietário","id":"owner-1","channel":"telegram","chat_id":"chat-1"}}
AGENTS={"agents":{"robotnik":{"enabled":True},"skipper":{"enabled":False}}}
PROVIDERS={"providers":{"storage":{"filesystem-local":{"enabled":True,"external":False,"adapter_path":"scripts/asset_pipeline.py"}},
                        "search":{"public-search":{"enabled":False,"external":True,"adapter_path":""}}}}

def req(kind="storage",provider="filesystem-local"):
    return {"campaign_id":"camp","asset_id":"asset","asset_version":1,"operation":"store_local",
            "destination":"local","tool":"asset_pipeline","parameters":{},"provider_kind":kind,"provider_id":provider}

class GovernanceEngineTests(unittest.TestCase):
    def test_local_enabled_provider_is_allowed(self):
        self.assertEqual(evaluate(req(),"Robotnik",GOV,AGENTS,PROVIDERS,BASE)["decision"],"allow")

    def test_disabled_actor_is_denied(self):
        result=evaluate(req(),"Skipper",GOV,AGENTS,PROVIDERS,BASE)
        self.assertEqual(result["decision"],"deny"); self.assertIn("actor-disabled-or-unknown",result["reasons"])

    def test_unknown_provider_is_denied(self):
        result=evaluate(req("image","missing"),"Robotnik",GOV,AGENTS,PROVIDERS,BASE)
        self.assertIn("provider-unknown",result["reasons"])

    def test_external_provider_is_disabled_and_requires_approval(self):
        result=evaluate(req("search","public-search"),"Robotnik",GOV,AGENTS,PROVIDERS,BASE)
        self.assertIn("provider-disabled",result["reasons"]); self.assertIn("owner-approval-required",result["reasons"])

    def test_external_enabled_provider_accepts_bound_approval(self):
        providers={"providers":{"search":{"p":{"enabled":True,"external":True,"adapter_path":""}}}}
        request=req("search","p")
        approval={"approval_id":"a","status":"approved","campaign_id":"camp","asset_id":"asset","asset_version":1,
                  "action":"store_local","destination":"local","provider_kind":"search","provider_id":"p",
                  "payload_hash":request_hash(request),"approved_by_role":"proprietário","approved_by_id":"owner-1",
                  "approved_channel":"telegram","approved_chat_id":"chat-1","approved_by_reference":"m1",
                  "owner_message_hash":"a"*64,"approved_at":"2026-07-20T00:00:00Z","expires_at":"2099-01-01T00:00:00Z",
                  "revoked_at":None,"consumed_at":None}
        self.assertEqual(evaluate(request,"Robotnik",GOV,AGENTS,providers,BASE,approval)["decision"],"allow")

    def test_decision_is_stable_for_same_material(self):
        one=evaluate(req(),"Robotnik",GOV,AGENTS,PROVIDERS,BASE)
        two=evaluate(req(),"Robotnik",GOV,AGENTS,PROVIDERS,BASE)
        self.assertEqual(one["decision_id"],two["decision_id"])

if __name__=="__main__": unittest.main(verbosity=2)

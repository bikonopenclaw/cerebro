#!/usr/bin/env python3
import json, tempfile, unittest
from unittest import mock
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime_lib import (TRANSITIONS, consume_approval, finish_approval_execution,
                         request_hash, reserve_approval, safe_name, start_approval_execution,
                         validate_approval, validate_owner_event)
from kling_exec import build_argv, main as kling_main
from assetctl import validate_url

BASE=Path(__file__).resolve().parents[2]
GOV={"external_action_lock":True,"owner":{"role":"proprietário","id":"owner-1","channel":"telegram","chat_id":"chat-1"}}

def request(**changes):
    value={"campaign_id":"camp","asset_id":"asset","asset_version":1,
           "operation":"text_to_image","destination":"kling","tool":"kling",
           "parameters":{"model":"m","prompt":"p"}}
    value.update(changes); return value

def approval(req=None,**changes):
    req=req or request()
    now=datetime.now(timezone.utc)
    value={"approval_id":"a1","status":"approved","campaign_id":req["campaign_id"],
           "asset_id":req["asset_id"],"asset_version":req["asset_version"],
           "action":req["operation"],"destination":req["destination"],
           "payload_hash":request_hash(req),"approved_by_role":"proprietário",
           "approved_by_id":"owner-1","approved_channel":"telegram",
           "approved_chat_id":"chat-1","approved_by_reference":"msg-1",
           "owner_message_hash":"a"*64,"approved_at":now.isoformat(),
           "expires_at":(now+timedelta(hours=1)).isoformat(),
           "revoked_at":None,"consumed_at":None}
    for key in ("provider_kind","provider_id"):
        if key in req: value[key]=req[key]
    value.update(changes); return value

class RuntimeTests(unittest.TestCase):
    def test_hash_is_canonical(self):
        self.assertEqual(request_hash({"b":2,"a":1}),request_hash({"a":1,"b":2}))
    def test_hash_ignores_embedded_hash(self):
        r=request(); self.assertEqual(request_hash(r),request_hash({**r,"payload_hash":"fake"}))
    def test_safe_name(self):
        with self.assertRaises(ValueError): safe_name("///")
        with self.assertRaises(ValueError): safe_name("a"*129)
    def test_transition_rejects_skip(self):
        self.assertNotIn("published",TRANSITIONS["intake"])
    def test_valid_owner_approval(self):
        validate_approval(request(),approval(),GOV)
    def test_owner_mismatch(self):
        with self.assertRaises(ValueError): validate_approval(request(),approval(approved_by_id="other"),GOV)
    def test_payload_mismatch(self):
        with self.assertRaises(ValueError): validate_approval(request(),approval(payload_hash="b"*64),GOV)
    def test_action_mismatch(self):
        with self.assertRaises(ValueError): validate_approval(request(),approval(action="publish_now"),GOV)
    def test_destination_mismatch(self):
        with self.assertRaises(ValueError): validate_approval(request(),approval(destination="instagram"),GOV)
    def test_revoked(self):
        with self.assertRaises(ValueError): validate_approval(request(),approval(revoked_at="2026-01-01T00:00:00Z"),GOV)
    def test_consumed(self):
        with self.assertRaises(ValueError): validate_approval(request(),approval(consumed_at="2026-01-01T00:00:00Z"),GOV)
    def test_expired(self):
        past=(datetime.now(timezone.utc)-timedelta(minutes=1)).isoformat()
        with self.assertRaises(ValueError): validate_approval(request(),approval(expires_at=past),GOV)
    def test_owner_event_binding(self):
        event={"authority":"openclaw.inbound_meta.v2","sender_id":"owner-1",
               "channel":"telegram","chat_id":"chat-1","message_id":"m1",
               "text":"OK","timestamp_utc":"2026-07-20T13:00:00Z"}
        validate_owner_event(event,GOV)
        with self.assertRaises(ValueError): validate_owner_event({**event,"sender_id":"x"},GOV)
    def test_consume_is_single_use(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"approval.json"; p.write_text(json.dumps(approval()))
            consume_approval(p,request(),GOV)
            with self.assertRaises(ValueError): consume_approval(p,request(),GOV)
    def test_kling_rejects_unknown_flag(self):
        with tempfile.TemporaryDirectory() as d:
            c=Path(d)/"c.json"; c.write_text(json.dumps({"production_enabled":True,"operations":{
              "text_to_image":{"flags":{"model":"--model"},"positionals":["prompt"],"required":["model","prompt"]}}}))
            with self.assertRaises(ValueError): build_argv(request(parameters={"model":"m","prompt":"p","evil":"x"}),"/bin/echo",c)
            req=Path(d)/"request.json"; req.write_text(json.dumps(request(provider_kind="video",provider_id="kling-cli")))
            runner=mock.Mock()
            with self.assertRaisesRegex(ValueError,"contrato Kling ainda não está habilitado"):
                kling_main(["--request",str(req),"--execute"],runner=runner,which=lambda _:"/bin/kling")
            runner.assert_not_called()
    def test_shell_payload_stays_single_argv(self):
        with tempfile.TemporaryDirectory() as d:
            c=Path(d)/"c.json"; c.write_text(json.dumps({"production_enabled":True,"operations":{
              "text_to_image":{"flags":{},"positionals":["prompt"],"required":["prompt"]}}}))
            r=request(parameters={"prompt":"x; touch /tmp/pwn"},provider_kind="video",provider_id="kling-cli")
            self.assertEqual(build_argv(r,"/bin/echo",c),["/bin/echo","text_to_image","x; touch /tmp/pwn"])
            req=Path(d)/"request.json"; req.write_text(json.dumps(r))
            approval_path=Path(d)/"approval.json"; approval_path.write_text(json.dumps(approval(r)))
            before=approval_path.read_bytes(); events=Path(d)/"events.jsonl"; runner=mock.Mock()
            with self.assertRaises(SystemExit) as blocked:
                kling_main(["--request",str(req),"--contract",str(c),"--approval",str(approval_path),
                            "--events",str(events),"--execution-id","exec-1","--execute"],
                           runner=runner,which=lambda _:"/bin/kling")
            self.assertEqual(blocked.exception.code,2)
            self.assertEqual(approval_path.read_bytes(),before)
            self.assertFalse(events.exists())
            runner.assert_not_called()
    def test_url_policy(self):
        validate_url("https://assets.example/file",{"assets.example"})
        for url in ("http://assets.example/file","https://u:p@assets.example/file","https://evil.example/file"):
            with self.assertRaises(ValueError): validate_url(url,{"assets.example"})

class ApprovalLifecycleTests(unittest.TestCase):
    def test_reserved_is_not_reusable(self):
        req=request(provider_kind="image",provider_id="test")
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"approval.json"; p.write_text(json.dumps(approval(req)),encoding="utf-8")
            reserve_approval(p,req,GOV,"exec-1")
            with self.assertRaises(ValueError): validate_approval(req,json.loads(p.read_text()),GOV)
            with self.assertRaises(ValueError): reserve_approval(p,req,GOV,"exec-2")

    def test_execution_lifecycle_is_terminal(self):
        req=request(provider_kind="image",provider_id="test")
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"approval.json"; p.write_text(json.dumps(approval(req)),encoding="utf-8")
            reserve_approval(p,req,GOV,"exec-1")
            start_approval_execution(p,"exec-1")
            done=finish_approval_execution(p,"exec-1","failed","event-1")
            self.assertEqual(done["status"],"failed")
            self.assertEqual(done["result_event_id"],"event-1")
            self.assertIsNotNone(done["consumed_at"])
            with self.assertRaises(ValueError): start_approval_execution(p,"exec-1")

    def test_execution_id_must_match(self):
        req=request()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"approval.json"; p.write_text(json.dumps(approval(req)),encoding="utf-8")
            reserve_approval(p,req,GOV,"exec-1")
            with self.assertRaises(ValueError): start_approval_execution(p,"exec-2")

    def test_provider_binding(self):
        req=request(provider_kind="image",provider_id="provider-a")
        good=approval(req)
        validate_approval(req,good,GOV)
        with self.assertRaises(ValueError):
            validate_approval(req,{**good,"provider_id":"provider-b"},GOV)

if __name__=="__main__":
    unittest.main(verbosity=2)

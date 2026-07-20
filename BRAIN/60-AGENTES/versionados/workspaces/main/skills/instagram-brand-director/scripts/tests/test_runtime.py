#!/usr/bin/env python3
import json, sys, tempfile, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime_lib import request_hash, safe_name, validate_approval, TRANSITIONS
from kling_exec import build_argv

class RuntimeTests(unittest.TestCase):
    def test_hash_is_canonical(self):
        self.assertEqual(request_hash({"b":2,"a":1}),request_hash({"a":1,"b":2}))
    def test_hash_ignores_embedded_hash(self):
        a={"operation":"x","campaign_id":"c","asset_id":"a"}
        b={**a,"request_hash":"fake"}
        self.assertEqual(request_hash(a),request_hash(b))
    def test_safe_name_blocks_empty_and_long(self):
        with self.assertRaises(ValueError): safe_name("///")
        with self.assertRaises(ValueError): safe_name("a"*129)
    def test_transition_rejects_skip(self):
        self.assertNotIn("published",TRANSITIONS["intake"])
    def test_approval_hash_mismatch(self):
        req={"campaign_id":"c","asset_id":"a","operation":"text_to_image"}
        approval={"campaign_id":"c","asset_id":"a","operation":"text_to_image",
                  "request_hash":"bad","used_at":None,
                  "expires_at":(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()}
        with self.assertRaises(ValueError): validate_approval(req,approval)
    def test_kling_rejects_unknown_flag(self):
        with tempfile.TemporaryDirectory() as d:
            contract=Path(d)/"c.json"
            contract.write_text(json.dumps({"production_enabled":True,"operations":{
                "text_to_image":{"flags":{"model":"--model"},"required":["model"]}}}))
            req={"tool":"kling","operation":"text_to_image",
                 "parameters":{"model":"x","evil":"$(id)"}}
            with self.assertRaises(ValueError): build_argv(req,"/bin/echo",contract)
    def test_prompt_is_single_positional_argv_value(self):
        with tempfile.TemporaryDirectory() as d:
            contract=Path(d)/"c.json"
            contract.write_text(json.dumps({"production_enabled":True,"operations":{
                "text_to_image":{"flags":{},"positionals":["prompt"],"required":["prompt"]}}}))
            req={"tool":"kling","operation":"text_to_image","parameters":{"prompt":"x; touch /tmp/pwn"}}
            argv=build_argv(req,"/bin/echo",contract)
            self.assertEqual(argv,["/bin/echo","text_to_image","x; touch /tmp/pwn"])

    def test_kling_rejects_flag_like_values(self):
        with tempfile.TemporaryDirectory() as d:
            contract=Path(d)/"c.json"
            contract.write_text(json.dumps({"production_enabled":True,"operations":{
                "text_to_image":{"flags":{"model":"--model"},"positionals":["prompt"],
                                 "required":["model","prompt"]}}}))
            req={"tool":"kling","operation":"text_to_image",
                 "parameters":{"model":"--omni","prompt":"imagem empresarial"}}
            with self.assertRaises(ValueError): build_argv(req,"/bin/echo",contract)

    def test_kling_rejects_flag_like_positional(self):
        with tempfile.TemporaryDirectory() as d:
            contract=Path(d)/"c.json"
            contract.write_text(json.dumps({"production_enabled":True,"operations":{
                "text_to_image":{"flags":{"model":"--model"},"positionals":["prompt"],
                                 "required":["model","prompt"]}}}))
            req={"tool":"kling","operation":"text_to_image",
                 "parameters":{"model":"kling-image-v3_0","prompt":"--omni"}}
            with self.assertRaises(ValueError): build_argv(req,"/bin/echo",contract)

if __name__=="__main__":
    unittest.main(verbosity=2)

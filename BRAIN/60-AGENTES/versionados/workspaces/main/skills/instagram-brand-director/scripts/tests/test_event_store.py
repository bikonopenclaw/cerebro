#!/usr/bin/env python3
import json, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime_lib import append_event, read_event_stream, verify_event_stream

def event(action="test"):
    return {"correlation_id":"c","campaign_id":"camp","asset_id":"asset","event_version":1,
            "actor":"tester","action":action,"result":"ok","before_hash":None,"after_hash":None,"detail":{}}

class EventStoreTests(unittest.TestCase):
    def test_append_builds_hash_chain(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"events.jsonl"
            first=append_event(p,event("one")); second=append_event(p,event("two"))
            result=verify_event_stream(p)
            self.assertEqual(result["events"],2)
            self.assertEqual(second["prev_event_hash"],first["event_hash"])
            self.assertEqual(result["head_hash"],second["event_hash"])

    def test_tamper_is_detected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"events.jsonl"; append_event(p,event())
            value=json.loads(p.read_text()); value["result"]="tampered"
            p.write_text(json.dumps(value)+"\n",encoding="utf-8")
            with self.assertRaises(ValueError): verify_event_stream(p)

    def test_invalid_sequence_is_detected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"events.jsonl"; append_event(p,event())
            value=json.loads(p.read_text()); value["stream_version"]=9
            p.write_text(json.dumps(value)+"\n",encoding="utf-8")
            with self.assertRaises(ValueError): verify_event_stream(p)

    def test_empty_stream_is_valid(self):
        with tempfile.TemporaryDirectory() as d:
            result=verify_event_stream(Path(d)/"missing.jsonl")
            self.assertEqual(result,{"valid":True,"events":0,"head_hash":""})

    def test_read_does_not_mutate(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"events.jsonl"; append_event(p,event()); before=p.read_bytes()
            self.assertEqual(len(read_event_stream(p)),1); self.assertEqual(before,p.read_bytes())

if __name__=="__main__": unittest.main(verbosity=2)

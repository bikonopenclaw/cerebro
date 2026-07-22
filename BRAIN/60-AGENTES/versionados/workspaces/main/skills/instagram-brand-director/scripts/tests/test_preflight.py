#!/usr/bin/env python3
import os, unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import preflight

class PreflightTests(unittest.TestCase):
    def test_candidate_build_has_no_block(self):
        base=Path(__file__).resolve().parents[2]
        checks=preflight.build_checks(base,"build","advisory")
        self.assertTrue(checks)
        self.assertTrue(all(c["status"]=="pass" for c in checks),[c for c in checks if c["status"]!="pass"])

    def test_owner_binding_blocks_placeholder(self):
        ok,_=preflight.owner_ready(Path(__file__).resolve().parents[2])
        self.assertFalse(ok)

    def test_production_composition_is_exactly_fail_closed(self):
        base=Path(__file__).resolve().parents[2]
        def which(name):
            return None if name in {"magick","convert"} else f"/usr/bin/{name}"
        with patch.object(preflight.shutil,"which",side_effect=which), patch.dict(os.environ,{},clear=True):
            checks=preflight.build_checks(base,"production","composition")
        blocked={c["name"] for c in checks if c["status"]=="blocked"}
        self.assertEqual(blocked,{"owner-binding","imagemagick","templates:static","templates:video",
                                  "motion-canvas-project","templates:motion"})

    def test_publish_adapter_and_provider_are_blocked(self):
        base=Path(__file__).resolve().parents[2]
        checks=preflight.build_checks(base,"production","publish")
        names={c["name"]:c["status"] for c in checks}
        self.assertEqual(names["publishing-adapter"],"blocked")
        self.assertEqual(names["provider:publication:instagram"],"blocked")

    def test_optional_agents_are_disabled_but_build_passes(self):
        base=Path(__file__).resolve().parents[2]
        checks=preflight.build_checks(base,"build","advisory")
        names={c["name"]:c["status"] for c in checks}
        for agent in ("skipper","rico","private"):
            self.assertEqual(names[f"agent:{agent}:disabled"],"pass")

if __name__=="__main__": unittest.main(verbosity=2)

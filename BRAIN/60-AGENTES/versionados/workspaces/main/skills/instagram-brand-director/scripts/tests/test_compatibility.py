#!/usr/bin/env python3
import json, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import approvalctl, campaignctl, preflight
from kling_exec import build_argv
from runtime_lib import TRANSITIONS

BASE=Path(__file__).resolve().parents[2]

class CompatibilityTests(unittest.TestCase):
    def test_campaignctl_legacy_commands_exist(self):
        choices=campaignctl.parser()._subparsers._group_actions[0].choices
        self.assertTrue({"init","transition","status"}<=set(choices))

    def test_approvalctl_legacy_commands_exist(self):
        choices=approvalctl.parser()._subparsers._group_actions[0].choices
        self.assertTrue({"record","verify","consume","revoke"}<=set(choices))
        self.assertTrue({"reserve","start","finish"}<=set(choices))

    def test_legacy_state_machine_still_blocks_skip(self):
        self.assertNotIn("published",TRANSITIONS["intake"])

    def test_kling_argv_contract_remains_typed(self):
        request={"tool":"kling","destination":"kling","operation":"text_to_image",
                 "parameters":{"model":"m","prompt":"x; echo pwn"}}
        contract=json.loads((BASE/"templates/kling-contract.json").read_text())
        self.assertIs(contract["production_enabled"],False)
        contract["production_enabled"]=True
        with tempfile.TemporaryDirectory() as d:
            fixture=Path(d)/"kling-contract.json"; fixture.write_text(json.dumps(contract))
            argv=build_argv(request,"/bin/kling",fixture)
            self.assertEqual(argv[-1],"x; echo pwn")
            self.assertIsInstance(argv,list)

    def test_publication_contract_is_disabled(self):
        text=(BASE/"templates/publishing-contract.yaml").read_text()
        self.assertIn("production_enabled: false",text)

    def test_external_providers_are_disabled(self):
        import yaml
        registry=yaml.safe_load((BASE/"assets/provider-registry.yaml").read_text())
        enabled=[f"{kind}:{pid}" for kind,items in registry["providers"].items() for pid,item in items.items() if item["external"] and item["enabled"]]
        self.assertEqual(enabled,[])

    def test_active_roles_remain_canonical(self):
        import yaml
        agents=yaml.safe_load((BASE/"assets/agent-registry.yaml").read_text())["agents"]
        for key in ("puppet_master","robotnik","kowalski"):
            self.assertTrue(agents[key]["enabled"]); self.assertTrue(agents[key]["canonical"])

if __name__=="__main__": unittest.main(verbosity=2)

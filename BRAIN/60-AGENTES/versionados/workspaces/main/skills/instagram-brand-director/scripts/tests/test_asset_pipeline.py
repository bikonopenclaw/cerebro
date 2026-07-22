#!/usr/bin/env python3
import argparse, contextlib, io, json, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import asset_pipeline

class AssetPipelineTests(unittest.TestCase):
    def register(self,root,source):
        args=argparse.Namespace(root=str(root),campaign_id="camp",asset_id="asset",correlation_id="corr",
                                actor="Robotnik",path=str(source),version=1,mime="text/plain")
        with contextlib.redirect_stdout(io.StringIO()): asset_pipeline.register(args)

    def test_register_and_promote(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); source=root/"source.txt"; source.write_text("data")
            self.register(root,source)
            args=argparse.Namespace(root=str(root),asset_id="asset",correlation_id="corr",actor="Robotnik",
                                    to="selected",reason="chosen",version=1)
            with contextlib.redirect_stdout(io.StringIO()): asset_pipeline.promote(args)
            record=json.loads((root/"assets/asset/v1.json").read_text())
            self.assertEqual(record["stage"],"selected"); self.assertEqual(len(record["lineage"]),1)

    def test_raw_tamper_blocks_promotion(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); source=root/"source.txt"; source.write_text("data"); self.register(root,source); source.write_text("changed")
            args=argparse.Namespace(root=str(root),asset_id="asset",correlation_id="corr",actor="Robotnik",
                                    to="selected",reason="chosen",version=1)
            with self.assertRaises(ValueError): asset_pipeline.promote(args)

    def test_invalid_stage_skip_is_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); source=root/"source.txt"; source.write_text("data"); self.register(root,source)
            args=argparse.Namespace(root=str(root),asset_id="asset",correlation_id="corr",actor="Robotnik",
                                    to="release-candidate",reason="skip",version=1)
            with self.assertRaises(ValueError): asset_pipeline.promote(args)

    def test_duplicate_version_is_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); source=root/"source.txt"; source.write_text("data"); self.register(root,source)
            with self.assertRaises(ValueError): self.register(root,source)

if __name__=="__main__": unittest.main(verbosity=2)

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "orchestrationctl.py"


class ControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.state = self.root / "state"
        self.order1 = self.root / "order-1.md"
        self.order1.write_text("ordem um\n", encoding="utf-8")
        self.order2 = self.root / "order-2.md"
        self.order2.write_text("ordem dois\n", encoding="utf-8")
        self.cron_state = self.root / "fake-crons.json"
        self.cron_state.write_text(
            json.dumps(
                {
                    "job-1": {"id": "job-1", "name": "não crítico 1", "enabled": True},
                    "job-2": {"id": "job-2", "name": "não crítico 2", "enabled": False},
                }
            ),
            encoding="utf-8",
        )
        self.cron_config = self.root / "cron-config.json"
        self.cron_config.write_text(
            json.dumps(
                {
                    "jobs": [
                        {"id": "job-1", "name": "não crítico 1"},
                        {"id": "job-2", "name": "não crítico 2"},
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.runner = self.root / "fake_cron.py"
        self.runner.write_text(
            """#!/usr/bin/env python3
import json, os, sys
path = os.environ["FAKE_CRON_STATE"]
state = json.load(open(path, encoding="utf-8"))
action, job_id = sys.argv[1], sys.argv[2]
if action == "get":
    print(json.dumps(state[job_id]))
    raise SystemExit(0)
if action not in {"disable", "enable"}:
    raise SystemExit(2)
if action == "disable" and os.environ.get("FAKE_CRON_IGNORE_DISABLE") == "1":
    print(json.dumps(state[job_id]))
    raise SystemExit(0)
state[job_id]["enabled"] = action == "enable"
with open(path, "w", encoding="utf-8") as handle:
    json.dump(state, handle)
print(json.dumps(state[job_id]))
""",
            encoding="utf-8",
        )
        self.runner.chmod(0o700)
        self.environment = {
            **os.environ,
            "SENTINEL_ORCHESTRATION_CRON_RUNNER": f"{sys.executable} {self.runner}",
            "FAKE_CRON_STATE": str(self.cron_state),
        }
        self.run_cmd("init")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def digest(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def run_cmd(
        self, *arguments: str, ok: bool = True
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            self.command(*arguments),
            text=True,
            capture_output=True,
            env=self.environment,
        )
        if ok and result.returncode != 0:
            self.fail(result.stderr)
        if not ok and result.returncode == 0:
            self.fail("comando deveria falhar")
        return result

    def command(self, *arguments: str) -> list[str]:
        return [
            sys.executable,
            str(SCRIPT),
            "--test-mode",
            "--state-dir",
            str(self.state),
            "--cron-config",
            str(self.cron_config),
            *arguments,
        ]

    def binding(self, order: Path, order_id: str = "ORDER-1") -> list[str]:
        return [
            "--order-id",
            order_id,
            "--order-path",
            str(order),
            "--order-sha256",
            self.digest(order),
            "--approval-id",
            f"APR-{order_id}",
            "--execution-id",
            f"EXE-{order_id}",
        ]

    def activate(self, order: Path | None = None, supersedes: str = "NONE") -> None:
        selected = order or self.order1
        order_id = "ORDER-1" if selected == self.order1 else "ORDER-2"
        self.run_cmd(
            "activate",
            *self.binding(selected, order_id),
            "--supersedes",
            supersedes,
            "--critical",
        )

    def test_start_requires_ack(self) -> None:
        self.activate()
        self.run_cmd("start", *self.binding(self.order1), ok=False)

    def test_assert_requires_running_and_restores_crons(self) -> None:
        self.activate()
        self.run_cmd("ack", *self.binding(self.order1))
        self.run_cmd("assert", *self.binding(self.order1), ok=False)
        state = json.loads(
            (self.state / "controller-state.json").read_text(encoding="utf-8")
        )
        self.assertIsNone(state["active_order"])
        self.assertEqual(
            state["latest_terminal_order"]["result"],
            "STALE_OR_UNBOUND_ORDER_REJECTED",
        )
        crons = json.loads(self.cron_state.read_text(encoding="utf-8"))
        self.assertTrue(crons["job-1"]["enabled"])
        self.assertFalse(crons["job-2"]["enabled"])

    def test_ack_rejects_wrong_hash(self) -> None:
        self.activate()
        args = self.binding(self.order1)
        args[5] = "0" * 64
        self.run_cmd("ack", *args, ok=False)

    def test_full_binding_and_cron_restore(self) -> None:
        self.activate()
        crons = json.loads(self.cron_state.read_text(encoding="utf-8"))
        self.assertFalse(crons["job-1"]["enabled"])
        self.assertFalse(crons["job-2"]["enabled"])
        self.run_cmd("ack", *self.binding(self.order1))
        self.run_cmd("start", *self.binding(self.order1))
        allowed = json.loads(
            self.run_cmd("assert", *self.binding(self.order1)).stdout
        )
        self.assertTrue(allowed["allowed"])
        self.run_cmd(
            "close",
            "--order-id",
            "ORDER-1",
            "--execution-id",
            "EXE-ORDER-1",
            "--result",
            "DONE",
        )
        crons = json.loads(self.cron_state.read_text(encoding="utf-8"))
        self.assertTrue(crons["job-1"]["enabled"])
        self.assertFalse(crons["job-2"]["enabled"])

    def test_only_one_active_order(self) -> None:
        self.activate()
        self.run_cmd(
            "activate",
            *self.binding(self.order2, "ORDER-2"),
            "--supersedes",
            "ORDER-1",
            "--critical",
            ok=False,
        )

    def test_concurrent_activation_allows_only_one_order(self) -> None:
        command1 = self.command(
            "activate",
            *self.binding(self.order1, "ORDER-1"),
            "--supersedes",
            "NONE",
            "--critical",
        )
        command2 = self.command(
            "activate",
            *self.binding(self.order2, "ORDER-2"),
            "--supersedes",
            "NONE",
            "--critical",
        )
        processes = [
            subprocess.Popen(
                command,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self.environment,
            )
            for command in (command1, command2)
        ]
        results = [process.communicate(timeout=10) for process in processes]
        codes = sorted(process.returncode for process in processes)
        self.assertEqual(codes, [0, 2], results)

    def test_stale_order_assertion_is_rejected(self) -> None:
        self.activate()
        self.run_cmd("ack", *self.binding(self.order1))
        self.run_cmd("start", *self.binding(self.order1))
        self.run_cmd(
            "assert",
            *self.binding(self.order2, "ORDER-2"),
            ok=False,
        )
        state = json.loads(
            (self.state / "controller-state.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            state["latest_terminal_order"]["result"],
            "STALE_OR_UNBOUND_ORDER_REJECTED",
        )

    def test_expired_lease_fails_closed_and_restores_crons(self) -> None:
        self.activate()
        self.run_cmd("ack", *self.binding(self.order1))
        self.run_cmd("start", *self.binding(self.order1))
        state_path = self.state / "controller-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["active_order"]["lease_expires_at_utc"] = "2000-01-01T00:00:00Z"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        self.run_cmd("assert", *self.binding(self.order1), ok=False)
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertIsNone(state["active_order"])
        self.assertEqual(
            state["latest_terminal_order"]["result"],
            "EXECUTION_LEASE_EXPIRED",
        )
        crons = json.loads(self.cron_state.read_text(encoding="utf-8"))
        self.assertTrue(crons["job-1"]["enabled"])
        self.assertFalse(crons["job-2"]["enabled"])

    def test_stop_is_priority_and_restores_crons(self) -> None:
        self.activate()
        result = json.loads(
            self.run_cmd(
                "stop",
                "--requested-by",
                "Hebert",
                "--reason",
                "teste local",
            ).stdout
        )
        self.assertTrue(result["stopped"])
        self.assertEqual(result["terminal"]["result"], "STOPPED_BY_OWNER")
        crons = json.loads(self.cron_state.read_text(encoding="utf-8"))
        self.assertTrue(crons["job-1"]["enabled"])
        self.assertFalse(crons["job-2"]["enabled"])

    def test_cron_name_drift_rejects_activation(self) -> None:
        crons = json.loads(self.cron_state.read_text(encoding="utf-8"))
        crons["job-1"]["name"] = "nome divergente"
        self.cron_state.write_text(json.dumps(crons), encoding="utf-8")
        self.run_cmd(
            "activate",
            *self.binding(self.order1),
            "--supersedes",
            "NONE",
            "--critical",
            ok=False,
        )
        state = json.loads(
            (self.state / "controller-state.json").read_text(encoding="utf-8")
        )
        self.assertIsNone(state["active_order"])

    def test_cron_postcondition_is_verified(self) -> None:
        self.environment["FAKE_CRON_IGNORE_DISABLE"] = "1"
        self.run_cmd(
            "activate",
            *self.binding(self.order1),
            "--supersedes",
            "NONE",
            "--critical",
            ok=False,
        )
        state = json.loads(
            (self.state / "controller-state.json").read_text(encoding="utf-8")
        )
        self.assertIsNone(state["active_order"])

    def test_production_override_is_rejected(self) -> None:
        environment = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("SENTINEL_ORCHESTRATION_")
            and key != "FAKE_CRON_STATE"
        }
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--state-dir",
                str(self.state),
                "--cron-config",
                str(self.cron_config),
                "status",
            ],
            text=True,
            capture_output=True,
            env=environment,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("state-dir de produção deve ser o canônico", result.stderr)

    def test_supersedes_must_match_latest_terminal(self) -> None:
        self.activate()
        self.run_cmd(
            "close",
            "--order-id",
            "ORDER-1",
            "--execution-id",
            "EXE-ORDER-1",
            "--result",
            "SUPERSEDED",
        )
        self.run_cmd(
            "activate",
            *self.binding(self.order2, "ORDER-2"),
            "--supersedes",
            "NONE",
            "--critical",
            ok=False,
        )
        self.run_cmd(
            "activate",
            *self.binding(self.order2, "ORDER-2"),
            "--supersedes",
            "ORDER-1",
            "--critical",
        )

    def test_tampered_order_is_rejected_after_ack(self) -> None:
        self.activate()
        self.run_cmd("ack", *self.binding(self.order1))
        self.order1.write_text("ordem adulterada\n", encoding="utf-8")
        self.run_cmd("start", *self.binding(self.order1), ok=False)

    def test_audit_chain_is_contiguous(self) -> None:
        self.activate()
        self.run_cmd("ack", *self.binding(self.order1))
        records = [
            json.loads(line)
            for line in (self.state / "audit.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        previous = None
        for record in records:
            self.assertEqual(record["previous_event_sha256"], previous)
            base = {key: value for key, value in record.items() if key != "event_sha256"}
            expected = hashlib.sha256(
                (
                    json.dumps(
                        base,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                    + "\n"
                ).encode("utf-8")
            ).hexdigest()
            self.assertEqual(record["event_sha256"], expected)
            previous = record["event_sha256"]


if __name__ == "__main__":
    unittest.main()

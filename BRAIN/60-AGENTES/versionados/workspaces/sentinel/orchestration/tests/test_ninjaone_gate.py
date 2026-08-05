from __future__ import annotations

import argparse
import importlib.util
import unittest
from pathlib import Path
from unittest import mock


CLIENT_PATH = (
    Path(__file__).resolve().parents[2]
    / "integrations"
    / "ninjaone"
    / "ninjaone_readonly.py"
)
SPEC = importlib.util.spec_from_file_location("ninjaone_readonly_under_test", CLIENT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("não foi possível carregar cliente NinjaOne")
CLIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLIENT)


def binding() -> dict[str, str]:
    return {
        "order_id": "ORDER-TEST",
        "order_path": "/tmp/order-test.md",
        "order_sha256": "0" * 64,
        "approval_id": "APR-TEST",
        "execution_id": "EXE-TEST",
    }


class NinjaOneGateTests(unittest.TestCase):
    def test_cli_requires_all_bindings(self) -> None:
        with self.assertRaises(SystemExit):
            CLIENT.build_parser().parse_args(["probe"])

    @mock.patch.object(CLIENT, "validate_secret_file")
    @mock.patch.object(CLIENT, "assert_order", side_effect=RuntimeError("gate"))
    def test_gate_precedes_secret_read(
        self,
        _assert_order: mock.Mock,
        validate_secret: mock.Mock,
    ) -> None:
        with self.assertRaisesRegex(RuntimeError, "gate"):
            CLIENT.load_credentials(binding())
        validate_secret.assert_not_called()

    @mock.patch.object(CLIENT.request, "urlopen")
    @mock.patch.object(CLIENT, "assert_order", side_effect=RuntimeError("gate"))
    def test_gate_precedes_token_network(
        self,
        _assert_order: mock.Mock,
        urlopen: mock.Mock,
    ) -> None:
        config = {
            "NINJAONE_CLIENT_ID": "id",
            "NINJAONE_CLIENT_SECRET": "secret",
            "NINJAONE_TOKEN_URL": "https://official.invalid/token",
        }
        with self.assertRaisesRegex(RuntimeError, "gate"):
            CLIENT.get_monitoring_token(config, binding())
        urlopen.assert_not_called()

    @mock.patch.object(CLIENT.request, "urlopen")
    @mock.patch.object(CLIENT, "assert_order", side_effect=RuntimeError("gate"))
    def test_gate_precedes_every_api_get(
        self,
        _assert_order: mock.Mock,
        urlopen: mock.Mock,
    ) -> None:
        config = {"NINJAONE_API_BASE": "https://official.invalid/v2"}
        with self.assertRaisesRegex(RuntimeError, "gate"):
            CLIENT.api_get(config, "token", "alerts", binding())
        urlopen.assert_not_called()

    @mock.patch.object(CLIENT.subprocess, "run")
    def test_controller_assert_requires_running_payload(
        self,
        subprocess_run: mock.Mock,
    ) -> None:
        subprocess_run.return_value = argparse.Namespace(
            returncode=0,
            stdout='{"allowed": true, "status": "ACKED"}',
        )
        with self.assertRaisesRegex(RuntimeError, "RUNNING"):
            CLIENT.assert_order(binding())


if __name__ == "__main__":
    unittest.main()

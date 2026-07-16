#!/usr/bin/env python3
"""Consulta read-only da saude ARX Backup/Cove para o Sentinel.

O Cove usa JSON-RPC sobre HTTP POST inclusive para leitura. Este cliente aceita
somente Login e EnumerateAccountStatistics, com parametros fixos. Nao salva
dados, nao cria tickets e nunca imprime senha, token ou visa.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib import error, request


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from access_control.access_audit import audited_access, validate_secret_file


ENV_PATH = Path("/data/.openclaw/workspace-kowalski/arx-backup/config/.env")
DEFAULT_URL = "https://api.backup.management/jsonapi"
ALLOWED_RPC_METHODS = {"Login", "EnumerateAccountStatistics"}
STATUS_COLUMNS = [
    "AR", "AN", "MN", "PN", "T0", "T7", "TB", "TL", "TO",
    "F0", "F7", "FB", "FL", "S0", "S7", "SB", "SL",
    "Q0", "Q7", "QB", "QL", "H0", "H7", "HB", "HL",
    "W0", "W7", "WB", "WL",
]
SECRET_KEYS = {"password", "token", "visa", "secret", "access_token", "refresh_token"}


def load_config() -> dict[str, str]:
    validate_secret_file(ENV_PATH)
    values: dict[str, str] = {}
    for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    required = ("ARX_BACKUP_PARTNER", "ARX_BACKUP_USERNAME")
    missing = [key for key in required if not values.get(key)]
    if not (values.get("ARX_BACKUP_PASSWORD") or values.get("ARX_BACKUP_TOKEN")):
        missing.append("ARX_BACKUP_PASSWORD/TOKEN")
    if missing:
        raise RuntimeError("Credencial ARX/Cove incompleta: " + ", ".join(missing))
    return values


def redact(value):
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if key.lower() in SECRET_KEYS else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


class ReadOnlyArxClient:
    def __init__(self, config: dict[str, str]):
        self.config = config
        self.url = config.get("ARX_BACKUP_JSONRPC_URL", DEFAULT_URL)
        self.visa: str | None = None
        self.request_id = 0

    def call(self, method: str, params: dict, *, authenticated: bool = True):
        if method not in ALLOWED_RPC_METHODS:
            raise RuntimeError(f"Metodo JSON-RPC nao permitido: {method}")
        self.request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": str(self.request_id),
            "method": method,
            "params": params,
        }
        if authenticated:
            if not self.visa:
                raise RuntimeError("Sessao ARX/Cove nao autenticada")
            payload["visa"] = self.visa
        req = request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
        if data.get("visa"):
            self.visa = data["visa"]
        if data.get("error"):
            raise RuntimeError("ARX/Cove retornou erro JSON-RPC")
        return data

    def login(self) -> int:
        data = self.call(
            "Login",
            {
                "partner": self.config["ARX_BACKUP_PARTNER"],
                "username": self.config["ARX_BACKUP_USERNAME"],
                "password": self.config.get("ARX_BACKUP_PASSWORD")
                or self.config["ARX_BACKUP_TOKEN"],
            },
            authenticated=False,
        )
        try:
            return int(data["result"]["result"]["PartnerId"])
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError("Login ARX/Cove sem PartnerId") from exc

    def status(self, partner_id: int):
        query = {
            "PartnerId": partner_id,
            "Filter": "",
            "ExcludedPartners": [],
            "SelectionMode": "Merged",
            "Labels": [],
            "StartRecordNumber": 0,
            "RecordsCount": 500,
            "OrderBy": "AR ASC, AN ASC",
            "Columns": STATUS_COLUMNS,
            "Totals": ["T7"],
        }
        return self.call(
            "EnumerateAccountStatistics",
            {"query": query, "totalStatistics": {}},
        )


def flatten_settings(row: dict) -> dict:
    result: dict = {}
    for item in row.get("Settings") or []:
        if isinstance(item, dict):
            result.update(item)
    return result


def current_severity(settings: dict) -> str:
    code = str(settings.get("T0", "0"))
    if code == "5":
        return "ok"
    if code in {"2", "3", "9", "10"}:
        return "critical"
    try:
        errors = int(settings.get("T7") or 0)
    except (TypeError, ValueError):
        errors = 0
    if code in {"6", "8"} or errors > 0:
        return "attention"
    return "other"


def rows_from(data: dict) -> list[dict]:
    rows = data.get("result", {}).get("result") or []
    return rows if isinstance(rows, list) else []


def probe(rows: list[dict]) -> dict:
    counts = {"ok": 0, "attention": 0, "critical": 0, "other": 0}
    clients = set()
    for row in rows:
        settings = flatten_settings(row)
        counts[current_severity(settings)] += 1
        if settings.get("AR"):
            clients.add(str(settings["AR"]))
    return {
        "ok": True,
        "transport": "JSON-RPC over HTTP POST",
        "allowed_rpc_methods": sorted(ALLOWED_RPC_METHODS),
        "write_methods_exposed": False,
        "clients": len(clients),
        "accounts": len(rows),
        "current_status": counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="ARX/Cove read-only do Sentinel")
    parser.add_argument("command", choices=("probe", "status"))
    args = parser.parse_args()

    client = ReadOnlyArxClient(load_config())
    partner_id = client.login()
    data = client.status(partner_id)
    rows = rows_from(data)
    if args.command == "probe":
        print(json.dumps(probe(rows), ensure_ascii=False, indent=2))
    else:
        print(
            json.dumps(
                {
                    "ok": True,
                    "allowed_rpc_methods": sorted(ALLOWED_RPC_METHODS),
                    "write_methods_exposed": False,
                    "data": redact(rows),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return 0


def audit_operation(argv: list[str]) -> str:
    return next((item for item in argv if item in {"probe", "status"}), "blocked_cli")


def cli() -> int:
    operation = audit_operation(sys.argv[1:])
    with audited_access(
        source="arx-cove", operation=operation, client_path=Path(__file__)
    ):
        return main()


if __name__ == "__main__":
    try:
        raise SystemExit(cli())
    except error.HTTPError as exc:
        print(f"ARX/Cove HTTP {exc.code}", file=sys.stderr)
        raise SystemExit(1)
    except (error.URLError, TimeoutError, RuntimeError, ValueError) as exc:
        print(f"ARX/Cove read-only falhou: {exc}", file=sys.stderr)
        raise SystemExit(1)

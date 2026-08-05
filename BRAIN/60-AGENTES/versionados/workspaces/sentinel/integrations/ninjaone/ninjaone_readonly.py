#!/usr/bin/env python3
"""Cliente NinjaOne estritamente read-only para o Sentinel.

Usa a credencial M2M compartilhada aprovada por Hebert, mas sempre solicita
token temporario somente com o escopo `monitoring` e aceita apenas GET em uma
allowlist fechada. Nunca imprime credenciais ou tokens.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib import error, parse, request


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from access_control.access_audit import audited_access, validate_secret_file


ENV_PATH = Path("/data/.openclaw/workspace-kowalski/ninjaone/config/.env")
ORCHESTRATION_CTL = (
    WORKSPACE_ROOT / "orchestration" / "orchestrationctl.py"
).resolve()
REQUIRED_SCOPE = "monitoring"
FORBIDDEN_SCOPES = {"management", "control"}
ALLOWED_ENDPOINTS = {
    "organizations": "organizations",
    "organizations-detailed": "organizations-detailed",
    "devices": "devices",
    "devices-detailed": "devices-detailed",
    "alerts": "alerts",
    "activities": "activities",
    "policies": "policies",
}


def binding_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--order-id", required=True)
    parser.add_argument("--order-path", required=True)
    parser.add_argument("--order-sha256", required=True)
    parser.add_argument("--approval-id", required=True)
    parser.add_argument("--execution-id", required=True)


def binding_from_args(args: argparse.Namespace) -> dict[str, str]:
    return {
        "order_id": args.order_id,
        "order_path": args.order_path,
        "order_sha256": args.order_sha256,
        "approval_id": args.approval_id,
        "execution_id": args.execution_id,
    }


def assert_order(binding: dict[str, str]) -> None:
    command = [
        sys.executable,
        str(ORCHESTRATION_CTL),
        "assert",
        "--order-id",
        binding["order_id"],
        "--order-path",
        binding["order_path"],
        "--order-sha256",
        binding["order_sha256"],
        "--approval-id",
        binding["approval_id"],
        "--execution-id",
        binding["execution_id"],
    ]
    result = subprocess.run(
        command,
        check=False,
        text=True,
        capture_output=True,
        timeout=15,
    )
    if result.returncode != 0:
        raise RuntimeError("Gate de orquestração recusou a operação NinjaOne")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gate de orquestração retornou resposta inválida") from exc
    if payload.get("allowed") is not True or payload.get("status") != "RUNNING":
        raise RuntimeError("Gate de orquestração não está em RUNNING")


def load_credentials(binding: dict[str, str]) -> dict[str, str]:
    assert_order(binding)
    validate_secret_file(ENV_PATH)

    values: dict[str, str] = {}
    for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    required = (
        "NINJAONE_CLIENT_ID",
        "NINJAONE_CLIENT_SECRET",
        "NINJAONE_TOKEN_URL",
        "NINJAONE_API_BASE",
    )
    missing = [key for key in required if not values.get(key)]
    if missing:
        raise RuntimeError("Credencial NinjaOne incompleta: " + ", ".join(missing))
    return values


def get_monitoring_token(
    config: dict[str, str],
    binding: dict[str, str],
) -> tuple[str, list[str]]:
    body = parse.urlencode(
        {
            "grant_type": "client_credentials",
            "client_id": config["NINJAONE_CLIENT_ID"],
            "client_secret": config["NINJAONE_CLIENT_SECRET"],
            "scope": REQUIRED_SCOPE,
        }
    ).encode()
    req = request.Request(
        config["NINJAONE_TOKEN_URL"],
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    assert_order(binding)
    with request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    token = payload.get("access_token")
    scopes = sorted(set(str(payload.get("scope", "")).split()))
    if not token:
        raise RuntimeError("NinjaOne respondeu sem access_token")
    if REQUIRED_SCOPE not in scopes:
        raise RuntimeError("Token NinjaOne sem escopo monitoring")
    forbidden = FORBIDDEN_SCOPES.intersection(scopes)
    if forbidden:
        raise RuntimeError(
            "Token recusado: escopo proibido presente: " + ", ".join(sorted(forbidden))
        )
    return token, scopes


def api_get(
    config: dict[str, str],
    token: str,
    endpoint: str,
    binding: dict[str, str],
):
    path = ALLOWED_ENDPOINTS[endpoint]
    url = f"{config['NINJAONE_API_BASE'].rstrip('/')}/{path}"
    req = request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        method="GET",
    )
    assert_order(binding)
    with request.urlopen(req, timeout=60) as response:
        raw = response.read().decode("utf-8")
        return response.status, json.loads(raw) if raw else None


def item_count(data) -> int | None:
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ("results", "items", "data"):
            if isinstance(data.get(key), list):
                return len(data[key])
    return None


def run_probe(
    config: dict[str, str],
    token: str,
    scopes: list[str],
    binding: dict[str, str],
) -> None:
    results = []
    for endpoint in ("organizations", "devices", "alerts"):
        status, data = api_get(config, token, endpoint, binding)
        results.append(
            {
                "endpoint": endpoint,
                "method": "GET",
                "http_status": status,
                "items": item_count(data),
            }
        )
    print(
        json.dumps(
            {
                "ok": all(item["http_status"] == 200 for item in results),
                "scope": scopes,
                "write_capability_exposed": False,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NinjaOne read-only do Sentinel")
    parser.add_argument(
        "command",
        choices=["probe", *ALLOWED_ENDPOINTS],
        help="probe resume a validacao; os demais comandos retornam JSON da fonte",
    )
    binding_arguments(parser)
    return parser


def run(args: argparse.Namespace) -> int:
    binding = binding_from_args(args)
    config = load_credentials(binding)
    token, scopes = get_monitoring_token(config, binding)
    if args.command == "probe":
        run_probe(config, token, scopes, binding)
        return 0

    status, data = api_get(config, token, args.command, binding)
    print(
        json.dumps(
            {
                "ok": status == 200,
                "scope": scopes,
                "endpoint": args.command,
                "method": "GET",
                "data": data,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if status == 200 else 1


def audit_operation(argv: list[str]) -> str:
    allowed = {"probe", *ALLOWED_ENDPOINTS}
    return next((item for item in argv if item in allowed), "blocked_cli")


def cli() -> int:
    args = build_parser().parse_args()
    operation = args.command
    with audited_access(
        source="ninjaone", operation=operation, client_path=Path(__file__)
    ):
        return run(args)


if __name__ == "__main__":
    try:
        raise SystemExit(cli())
    except error.HTTPError as exc:
        print(f"NinjaOne HTTP {exc.code}", file=sys.stderr)
        raise SystemExit(1)
    except (error.URLError, TimeoutError, RuntimeError, ValueError) as exc:
        print(f"NinjaOne read-only falhou: {exc}", file=sys.stderr)
        raise SystemExit(1)

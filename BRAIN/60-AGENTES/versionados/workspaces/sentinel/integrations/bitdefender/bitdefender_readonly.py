#!/usr/bin/env python3
"""Cliente Bitdefender GravityZone estritamente read-only para o Sentinel.

Usa somente a credencial externa aprovada, endpoints oficiais fixos e quatro
metodos de consulta. A saida contem apenas contagens agregadas.
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from access_control.access_audit import audited_access, validate_secret_file


SECRET_PATH = Path("/data/.openclaw/secrets/bitdefender-gravityzone.env")
MAX_RESPONSE_BYTES = 10 * 1024 * 1024


@dataclass(frozen=True)
class Route:
    version: str
    service: str
    method: str
    params: dict[str, Any]


ROUTES = {
    "companies": Route("v1.0", "network", "getCompaniesList", {}),
    "endpoints": Route(
        "v1.0", "network", "getEndpointsList", {"page": 1, "perPage": 100}
    ),
    "quarantine": Route(
        "v1.0",
        "quarantine/computers",
        "getQuarantineItemsList",
        {"page": 1, "perPage": 100},
    ),
    "incidents": Route(
        "v1.2", "incidents", "getIncidentsList", {"page": 1, "perPage": 10}
    ),
}


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise error.HTTPError(req.full_url, code, "redirect bloqueado", headers, fp)


def load_config() -> dict[str, str]:
    validate_secret_file(SECRET_PATH)
    values: dict[str, str] = {}
    for raw in SECRET_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    required = ("BITDEFENDER_GZ_BASE_URL", "BITDEFENDER_GZ_API_KEY")
    missing = [key for key in required if not values.get(key)]
    if missing:
        raise RuntimeError("credencial Bitdefender incompleta")
    return values


def api_root(configured: str) -> str:
    parsed = parse.urlsplit(configured.rstrip("/"))
    if parsed.scheme != "https" or not parsed.netloc:
        raise RuntimeError("endpoint Bitdefender deve usar HTTPS")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise RuntimeError("endpoint Bitdefender invalido")
    path = parsed.path.rstrip("/")
    if path.endswith("/api/v1.0/jsonrpc"):
        root_path = path[: -len("/v1.0/jsonrpc")]
    elif path.endswith("/api"):
        root_path = path
    elif not path:
        root_path = "/api"
    else:
        raise RuntimeError("rota-base Bitdefender fora do formato aprovado")
    return parse.urlunsplit((parsed.scheme, parsed.netloc, root_path, "", ""))


def result_count(result: Any) -> int:
    if isinstance(result, dict):
        if isinstance(result.get("total"), int):
            return result["total"]
        if isinstance(result.get("items"), list):
            return len(result["items"])
    if isinstance(result, list):
        return len(result)
    raise RuntimeError("Bitdefender retornou schema de contagem incompativel")


class ReadOnlyBitdefenderClient:
    def __init__(self, config: dict[str, str]):
        self.root = api_root(config["BITDEFENDER_GZ_BASE_URL"])
        self.api_key = config["BITDEFENDER_GZ_API_KEY"]
        self.opener = request.build_opener(NoRedirect)

    def call(self, operation: str) -> dict[str, Any]:
        if operation not in ROUTES:
            raise RuntimeError("operacao Bitdefender nao permitida")
        route = ROUTES[operation]
        url = f"{self.root}/{route.version}/jsonrpc/{route.service}"
        token = base64.b64encode(f"{self.api_key}:".encode("utf-8")).decode("ascii")
        payload = {
            "jsonrpc": "2.0",
            "method": route.method,
            "params": route.params,
            "id": "sentinel-readonly",
        }
        api_request = request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {token}",
            },
            method="POST",
        )
        with self.opener.open(api_request, timeout=60) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise RuntimeError("resposta Bitdefender excede limite seguro")
            body = json.loads(raw.decode("utf-8"))
        if body.get("error"):
            raise RuntimeError("Bitdefender retornou erro JSON-RPC")
        return {
            "operation": operation,
            "method": route.method,
            "api_version": route.version,
            "count": result_count(body.get("result")),
        }


def output_for(client: ReadOnlyBitdefenderClient, command: str) -> dict[str, Any]:
    operations = tuple(ROUTES) if command == "probe" else (command,)
    results = [client.call(operation) for operation in operations]
    return {
        "ok": True,
        "source": "bitdefender",
        "mode": "readonly_summarized",
        "write_methods_exposed": False,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Bitdefender read-only do Sentinel")
    parser.add_argument("command", choices=("probe", *ROUTES))
    args = parser.parse_args()
    output = output_for(ReadOnlyBitdefenderClient(load_config()), args.command)
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def audit_operation(argv: list[str]) -> str:
    allowed = {"probe", *ROUTES}
    return next((item for item in argv if item in allowed), "blocked_cli")


def cli() -> int:
    operation = audit_operation(sys.argv[1:])
    with audited_access(
        source="bitdefender", operation=operation, client_path=Path(__file__)
    ):
        return main()


if __name__ == "__main__":
    try:
        raise SystemExit(cli())
    except error.HTTPError as exc:
        print(f"Bitdefender HTTP {exc.code}", file=sys.stderr)
        raise SystemExit(1)
    except (error.URLError, TimeoutError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Bitdefender read-only falhou: {exc}", file=sys.stderr)
        raise SystemExit(1)

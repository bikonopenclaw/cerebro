#!/usr/bin/env python3
"""Cliente mínimo e seguro para Bitdefender GravityZone.

Não imprime API key. Não grava segredo no workspace.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SECRET_PATH = Path("/data/.openclaw/secrets/bitdefender-gravityzone.env")


def load_env(path: Path = SECRET_PATH) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"Segredo não encontrado: {path}")
    if oct(path.stat().st_mode & 0o777) != "0o600":
        raise SystemExit(f"Permissão insegura no segredo: esperado 600 em {path}")

    env: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        env[key.strip()] = value

    missing = [k for k in ("BITDEFENDER_GZ_BASE_URL", "BITDEFENDER_GZ_API_KEY") if not env.get(k)]
    if missing:
        raise SystemExit("Variáveis ausentes no segredo: " + ", ".join(missing))
    return env


class GravityZoneClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def call(self, service: str, method: str, params: dict[str, Any] | None = None) -> Any:
        if self.base_url.endswith("/jsonrpc"):
            url = f"{self.base_url}/{service}"
        elif self.base_url.endswith("/api"):
            url = f"{self.base_url}/v1.0/jsonrpc/{service}"
        else:
            url = f"{self.base_url}/api/v1.0/jsonrpc/{service}"
        token = base64.b64encode(f"{self.api_key}:".encode("utf-8")).decode("ascii")
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": "kowalski",
        }
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {token}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise SystemExit(f"HTTP {exc.code} na API GravityZone. Detalhe sanitizado: {detail}") from exc
        except urllib.error.URLError as exc:
            raise SystemExit(f"Falha de conexão com GravityZone: {exc.reason}") from exc

        data = json.loads(body)
        if "error" in data:
            raise SystemExit("Erro JSON-RPC GravityZone: " + json.dumps(data["error"], ensure_ascii=False))
        return data.get("result")


def get_client() -> GravityZoneClient:
    env = load_env()
    return GravityZoneClient(env["BITDEFENDER_GZ_BASE_URL"], env["BITDEFENDER_GZ_API_KEY"])


def companies(format_: str) -> int:
    result = get_client().call("network", "getCompaniesList")
    companies_data = result.get("items", result) if isinstance(result, dict) else result
    if format_ == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    rows = companies_data if isinstance(companies_data, list) else []
    print(f"Empresas retornadas: {len(rows)}")
    for item in rows:
        name = item.get("name") or item.get("companyName") or "sem_nome"
        cid = item.get("id") or item.get("companyId") or "sem_id"
        print(f"- {name} | id={cid}")
    return 0


def companies_report() -> int:
    result = get_client().call("network", "getCompaniesList")
    rows = result.get("items", result) if isinstance(result, dict) else result
    if not isinstance(rows, list):
        rows = []

    print("# Bikon Tecnologia")
    print("## Inventário GravityZone — empresas")
    print()
    print("**Fonte:** Bitdefender GravityZone API")
    print("**Tipo:** inventário técnico interno")
    print()
    print("> Relatório gerado sem expor credenciais. IDs são técnicos e não substituem contrato/faturamento.")
    print()
    print(f"Total de empresas retornadas: **{len(rows)}**")
    print()
    print("| Empresa | ID técnico |")
    print("|---|---|")
    for item in rows:
        name = str(item.get("name") or item.get("companyName") or "sem_nome").replace("|", "-")
        cid = str(item.get("id") or item.get("companyId") or "sem_id").replace("|", "-")
        print(f"| {name} | `{cid}` |")
    print()
    print("**Bikon Tecnologia**")
    print("Sua empresa parar de depender de você em 90 dias")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Rotina segura para Bitdefender GravityZone")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_companies = sub.add_parser("companies", help="Lista empresas/clientes")
    p_companies.add_argument("--format", choices=("table", "json"), default="table")

    sub.add_parser("companies-report", help="Gera relatório Markdown de empresas")

    args = parser.parse_args()
    if args.cmd == "companies":
        return companies(args.format)
    if args.cmd == "companies-report":
        return companies_report()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Visao operacional sanitizada para o Sentinel.

Le o cadastro mestre da Bikon, mas nunca expoe dados fiscais, financeiros,
enderecos, telefones ou e-mails. Campos operacionais sem fonte autoritativa
sao declarados como nao configurados.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from access_control.access_audit import audited_access


REGISTRY = Path(
    "/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_ativos.json"
)

SEVERITY = {
    "P1": "Indisponibilidade critica, ataque ativo, perda de dados ou impacto amplo em cliente pagante.",
    "P2": "Degradacao relevante, risco alto ou falha sem contorno seguro.",
    "P3": "Falha localizada, risco moderado ou prazo operacional proximo.",
    "P4": "Melhoria, manutencao preventiva ou desvio sem impacto atual.",
}

FORBIDDEN_OUTPUT_KEYS = {
    "cpf_cnpj",
    "cpf_cnpj_digitos",
    "emails_financeiro",
    "endereco",
    "telefone",
    "inscricao_estadual",
    "inscricao_municipal",
}


def load_registry() -> dict[str, Any]:
    with REGISTRY.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data.get("clientes"), list):
        raise RuntimeError("cadastro mestre invalido: clientes nao e uma lista")
    return data


def safe_client(client: dict[str, Any]) -> dict[str, Any]:
    return {
        "client_id": client.get("id"),
        "display_name": client.get("razao_social"),
        "active": bool(client.get("ativo")),
        "cartorio_context": bool(client.get("cns_cartorio")),
        "operational_owner": {"status": "not_configured", "value": None},
        "sla": {"status": "not_configured", "value": None},
        "maintenance_window": {"status": "not_configured", "value": None},
        "incident_profile": "sentinel-global-v1",
        "live_asset_sources": [
            "ninjaone-readonly",
            "arx-cove-readonly",
            "bitdefender-readonly",
        ],
    }


def assert_sanitized(value: Any) -> None:
    if isinstance(value, dict):
        leaked = FORBIDDEN_OUTPUT_KEYS.intersection(value)
        if leaked:
            raise RuntimeError(f"saida bloqueada por campo sensivel: {sorted(leaked)}")
        for child in value.values():
            assert_sanitized(child)
    elif isinstance(value, list):
        for child in value:
            assert_sanitized(child)


def build_summary(data: dict[str, Any]) -> dict[str, Any]:
    clients = [safe_client(item) for item in data["clientes"]]
    return {
        "source_updated_at": data.get("atualizado_em"),
        "registered_clients": len(clients),
        "active_clients": sum(1 for item in clients if item["active"]),
        "operational_gaps": {
            "operational_owner": len(clients),
            "sla": len(clients),
            "maintenance_window": len(clients),
        },
        "severity_profile": "sentinel-global-v1",
        "live_asset_sources": [
            "ninjaone-readonly",
            "arx-cove-readonly",
            "bitdefender-readonly",
        ],
        "bitdefender_source": "bitdefender-readonly",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Contexto operacional sanitizado")
    parser.add_argument("command", choices=("summary", "clients", "client", "severity"))
    parser.add_argument("client_id", nargs="?")
    args = parser.parse_args()

    data = load_registry()
    clients = [safe_client(item) for item in data["clientes"]]

    if args.command == "summary":
        output: Any = build_summary(data)
    elif args.command == "clients":
        output = clients
    elif args.command == "severity":
        output = {"profile": "sentinel-global-v1", "levels": SEVERITY}
    else:
        if not args.client_id:
            parser.error("client exige client_id")
        matches = [item for item in clients if str(item["client_id"]) == args.client_id]
        if not matches:
            raise SystemExit("cliente nao encontrado")
        output = matches[0]

    assert_sanitized(output)
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def audit_operation(argv: list[str]) -> str:
    allowed = {"summary", "clients", "client", "severity"}
    return next((item for item in argv if item in allowed), "blocked_cli")


def cli() -> int:
    operation = audit_operation(sys.argv[1:])
    with audited_access(
        source="operational-context",
        operation=operation,
        client_path=Path(__file__),
    ):
        return main()


if __name__ == "__main__":
    raise SystemExit(cli())

#!/usr/bin/env python3
"""Dry-run Bitdefender GravityZone -> Ninja tickets.

Fase 1 conservadora:
- somente leitura no GravityZone;
- nenhum chamado real no Ninja;
- nenhum auto-fechamento;
- deduplicacao simulada por cliente + endpoint + tipo + identificador.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
JOBS_DIR = ROOT / "jobs"
REPORTS_DIR = ROOT / "relatorios" / "dry-run"
STATE_PATH = JOBS_DIR / "bitdefender-ninja-ticket-state.json"

# Fase 1 evita ruido: so considera politica critica quando o antimalware
# aparece explicitamente desligado. Outros modulos podem variar por pacote/politica.
CRITICAL_MODULES = ("antimalware",)
RECENT_PROTECTION_DAYS = 30


def import_gz_client() -> Any:
    sys.path.insert(0, str(SCRIPT_DIR))
    import gz_client  # noqa: PLC0415

    return gz_client


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_api_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def age_days(value: Any, reference: datetime) -> int | None:
    dt = parse_api_datetime(value)
    if dt is None:
        return None
    delta = reference - dt
    return max(0, delta.days)


def safe_text(value: Any, fallback: str = "N/D") -> str:
    if value is None:
        return fallback
    text = str(value).replace("\n", " ").replace("\r", " ").strip()
    return text or fallback


def normalize_key(*parts: Any) -> str:
    raw = "|".join(safe_text(part, "") for part in parts).lower()
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


@dataclass
class Alert:
    client_name: str
    client_id: str
    endpoint_name: str
    endpoint_id: str
    alert_type: str
    threat_identifier: str
    severity: str
    reason: str
    evidence: list[str]

    @property
    def dedup_key(self) -> str:
        return normalize_key(self.client_id or self.client_name, self.endpoint_id or self.endpoint_name, self.alert_type, self.threat_identifier)

    @property
    def subject(self) -> str:
        label = {
            "ameaca_ativa": "Incidente",
            "malware_nao_resolvido": "Incidente",
            "endpoint_sem_protecao": "Protecao",
            "politica_critica_violada": "Politica",
            "bloqueio_ou_falso_positivo": "Falso positivo",
        }.get(self.alert_type, "Incidente")
        return f"Bitdefender - {label} - {self.client_name} - {self.endpoint_name}"

    def simulated_ticket(self) -> dict[str, Any]:
        return {
            "system": "Ninja",
            "queue": "fila padrao / triagem interna Bikon",
            "priority": "padrao",
            "subject": self.subject,
            "client": self.client_name,
            "endpoint": self.endpoint_name,
            "type": self.alert_type,
            "severity": self.severity,
            "dedup_key": self.dedup_key,
            "body": {
                "fonte": "Bitdefender GravityZone API, somente leitura",
                "cliente_afetado": self.client_name,
                "endpoint": self.endpoint_name,
                "evidencia_sanitizada": self.evidence,
                "impacto": self.reason,
                "urgencia": "padrao",
                "acao_esperada": "Validar no console Bitdefender e executar tratativa operacional conforme politica Bikon.",
                "restricao": "Dry-run: nenhum ticket real criado e nenhuma acao em endpoint executada.",
            },
        }


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"active": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"active": {}, "state_warning": f"Estado invalido ignorado: {path}"}
    if not isinstance(data, dict):
        return {"active": {}, "state_warning": f"Estado fora do formato esperado ignorado: {path}"}
    data.setdefault("active", {})
    return data


def result_items(result: Any) -> list[dict[str, Any]]:
    if isinstance(result, dict):
        items = result.get("items", [])
    else:
        items = result
    return items if isinstance(items, list) else []


def list_companies(client: Any) -> list[dict[str, Any]]:
    return result_items(client.call("network", "getCompaniesList"))


def list_endpoints(client: Any, company_id: str, per_page: int) -> list[dict[str, Any]]:
    endpoints: list[dict[str, Any]] = []
    page = 1
    pages_count = 1
    while page <= pages_count:
        result = client.call("network", "getEndpointsList", {"parentId": company_id, "page": page, "perPage": per_page})
        endpoints.extend(result_items(result))
        if isinstance(result, dict):
            pages_count = int(result.get("pagesCount") or 1)
        page += 1
    return endpoints


def detail_for(client: Any, endpoint_id: str) -> dict[str, Any] | None:
    try:
        detail = client.call("network", "getManagedEndpointDetails", {"endpointId": endpoint_id})
    except SystemExit:
        return None
    return detail if isinstance(detail, dict) else None


def malware_alerts(company: dict[str, Any], endpoint: dict[str, Any], detail: dict[str, Any]) -> list[Alert]:
    malware = detail.get("malwareStatus") if isinstance(detail.get("malwareStatus"), dict) else {}
    infected = bool(malware.get("infected"))
    detection = bool(malware.get("detection"))
    if not infected and not detection:
        return []

    threat_id = "malwareStatus:"
    threat_id += "infected" if infected else "detection"
    endpoint_name = safe_text(detail.get("name") or endpoint.get("name"))
    return [
        Alert(
            client_name=safe_text(company.get("name")),
            client_id=safe_text(company.get("id"), ""),
            endpoint_name=endpoint_name,
            endpoint_id=safe_text(detail.get("id") or endpoint.get("id"), ""),
            alert_type="malware_nao_resolvido" if infected else "ameaca_ativa",
            threat_identifier=threat_id,
            severity="critico",
            reason="Malware ou deteccao ativa sinalizada no endpoint.",
            evidence=[
                f"malwareStatus.infected={infected}",
                f"malwareStatus.detection={detection}",
                f"lastSeen={safe_text(detail.get('lastSeen'))}",
            ],
        )
    ]


def record_exclusion(stats: dict[str, Any], category: str, company: dict[str, Any], endpoint_name: str, last_seen: Any, reason: str) -> None:
    stats[category] = int(stats.get(category, 0)) + 1
    samples_key = f"{category}_samples"
    samples = stats.setdefault(samples_key, [])
    if isinstance(samples, list) and len(samples) < 20:
        samples.append(
            {
                "client": safe_text(company.get("name")),
                "endpoint": endpoint_name,
                "lastSeen": safe_text(last_seen),
                "reason": reason,
            }
        )


def protection_is_actionable(last_seen: Any, stats: dict[str, Any], company: dict[str, Any], endpoint_name: str, reason: str, reference: datetime) -> bool:
    days = age_days(last_seen, reference)
    if days is None:
        record_exclusion(stats, "validation_manual_no_last_seen", company, endpoint_name, last_seen, reason)
        return False
    if days > RECENT_PROTECTION_DAYS:
        record_exclusion(stats, "inactive_machines_excluded", company, endpoint_name, last_seen, f"{reason}; lastSeen ha {days} dias")
        return False
    stats["endpoint_sem_protecao_recent_30d"] = int(stats.get("endpoint_sem_protecao_recent_30d", 0)) + 1
    return True


def protection_alerts(
    company: dict[str, Any],
    endpoint: dict[str, Any],
    detail: dict[str, Any] | None,
    stats: dict[str, Any],
    reference: datetime,
) -> list[Alert]:
    client_name = safe_text(company.get("name"))
    client_id = safe_text(company.get("id"), "")
    endpoint_name = safe_text((detail or {}).get("name") or endpoint.get("name"))
    endpoint_id = safe_text((detail or {}).get("id") or endpoint.get("id"), "")

    if not endpoint.get("isManaged"):
        last_seen = endpoint.get("lastSeen") or endpoint.get("lastSeenDate") or endpoint.get("lastUpdate")
        reason = "Endpoint aparece sem agente gerenciado pela API GravityZone."
        if not protection_is_actionable(last_seen, stats, company, endpoint_name, reason, reference):
            return []
        return [
            Alert(
                client_name=client_name,
                client_id=client_id,
                endpoint_name=endpoint_name,
                endpoint_id=endpoint_id,
                alert_type="endpoint_sem_protecao",
                threat_identifier=f"unmanaged:{endpoint_id or endpoint_name}",
                severity="alto",
                reason=reason,
                evidence=[
                    "isManaged=False",
                    f"machineType={safe_text(endpoint.get('machineType'))}",
                    f"lastSeen={safe_text(last_seen)}",
                ],
            )
        ]

    if detail is None:
        return []

    alerts: list[Alert] = []
    agent = detail.get("agent") if isinstance(detail.get("agent"), dict) else {}
    modules = detail.get("modules") if isinstance(detail.get("modules"), dict) else {}

    if not bool(agent.get("licensed", True)):
        last_seen = detail.get("lastSeen")
        reason = "Endpoint gerenciado sem licenca ativa confirmada nos campos disponiveis."
        if not protection_is_actionable(last_seen, stats, company, endpoint_name, reason, reference):
            return alerts
        alerts.append(
            Alert(
                client_name=client_name,
                client_id=client_id,
                endpoint_name=endpoint_name,
                endpoint_id=endpoint_id,
                alert_type="endpoint_sem_protecao",
                threat_identifier=f"license_missing:{endpoint_id or endpoint_name}",
                severity="alto",
                reason=reason,
                evidence=[
                    f"agent.licensed={agent.get('licensed')}",
                    f"lastSeen={safe_text(last_seen)}",
                ],
            )
        )

    disabled_critical = [name for name in CRITICAL_MODULES if modules.get(name) is False]
    if disabled_critical:
        alerts.append(
            Alert(
                client_name=client_name,
                client_id=client_id,
                endpoint_name=endpoint_name,
                endpoint_id=endpoint_id,
                alert_type="politica_critica_violada",
                threat_identifier="critical_modules:" + ",".join(disabled_critical),
                severity="alto",
                reason="Modulo critico de protecao aparece desligado nos campos da API.",
                evidence=[
                    "modulos_criticos_desligados=" + ", ".join(disabled_critical),
                    f"policy={safe_text((detail.get('policy') or {}).get('name') if isinstance(detail.get('policy'), dict) else None)}",
                    f"lastSeen={safe_text(detail.get('lastSeen'))}",
                ],
            )
        )

    return alerts


def collect_alerts(client: Any, per_page: int, max_companies: int | None, max_endpoints: int | None, workers: int) -> tuple[list[Alert], dict[str, Any]]:
    reference = datetime.now(timezone.utc)
    stats: dict[str, Any] = {
        "companies_seen": 0,
        "endpoints_seen": 0,
        "managed_endpoint_details_checked": 0,
        "detail_failures": 0,
        "endpoint_sem_protecao_recent_30d": 0,
        "inactive_machines_excluded": 0,
        "validation_manual_no_last_seen": 0,
        "risks": [],
    }
    alerts: list[Alert] = []
    managed_records: list[tuple[dict[str, Any], dict[str, Any]]] = []

    companies = list_companies(client)
    if max_companies is not None:
        companies = companies[:max_companies]
    stats["companies_seen"] = len(companies)

    for company in companies:
        company_id = safe_text(company.get("id"), "")
        try:
            endpoints = list_endpoints(client, company_id, per_page)
        except SystemExit as exc:
            stats["risks"].append(f"Falha ao listar endpoints de {safe_text(company.get('name'))}: {str(exc)[:160]}")
            continue

        if max_endpoints is not None:
            remaining = max_endpoints - stats["endpoints_seen"]
            if remaining <= 0:
                break
            endpoints = endpoints[:remaining]

        stats["endpoints_seen"] += len(endpoints)

        for endpoint in endpoints:
            if endpoint.get("isManaged"):
                managed_records.append((company, endpoint))
            else:
                alerts.extend(protection_alerts(company, endpoint, None, stats, reference))

    def fetch(record: tuple[dict[str, Any], dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]:
        company, endpoint = record
        return company, endpoint, detail_for(client, safe_text(endpoint.get("id"), ""))

    if managed_records:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
            futures = [executor.submit(fetch, record) for record in managed_records]
            for future in as_completed(futures):
                company, endpoint, detail = future.result()
                if detail is None:
                    stats["detail_failures"] += 1
                    continue
                stats["managed_endpoint_details_checked"] += 1
                alerts.extend(malware_alerts(company, endpoint, detail))
                alerts.extend(protection_alerts(company, endpoint, detail, stats, reference))

    if stats["detail_failures"]:
        stats["risks"].append("Alguns endpoints gerenciados nao retornaram detalhe; dry-run pode subestimar alertas.")
    if not alerts:
        stats["risks"].append("Nenhum alerta acionavel identificado nas regras da Fase 1.")
    stats["risks"].append("Fase 1 nao consulta bloqueios/falsos positivos em fonte dedicada; cobre apenas campos disponiveis em network/details.")
    if stats["validation_manual_no_last_seen"]:
        stats["risks"].append("Endpoints sem protecao sem lastSeen confiavel ficaram fora do volume acionavel e exigem validacao manual.")
    if stats["inactive_machines_excluded"]:
        stats["risks"].append("Endpoints sem protecao vistos ha mais de 30 dias foram tratados como maquina inativa, nao ticket operacional.")
    return alerts, stats


def deduplicate(alerts: list[Alert], state: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    active = state.get("active") if isinstance(state.get("active"), dict) else {}
    seen: set[str] = set()
    tickets: list[dict[str, Any]] = []
    deduped = 0
    for alert in alerts:
        key = alert.dedup_key
        if key in seen or key in active:
            deduped += 1
            continue
        seen.add(key)
        tickets.append(alert.simulated_ticket())
    return tickets, deduped


def write_outputs(summary: dict[str, Any], json_path: Path, md_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Bikon Tecnologia",
        "## Dry-run Bitdefender -> tickets Ninja",
        "",
        f"**Gerado em:** {summary['generated_at']}",
        "**Modo:** dry-run, sem ticket real, sem cron, sem auto-fechamento",
        "**Fonte:** Bitdefender GravityZone API, somente leitura",
        "",
        "## Resumo",
        f"- Empresas consultadas: **{summary['stats']['companies_seen']}**",
        f"- Endpoints consultados: **{summary['stats']['endpoints_seen']}**",
        f"- Detalhes gerenciados consultados: **{summary['stats']['managed_endpoint_details_checked']}**",
        f"- Alertas acionaveis: **{summary['actionable_alerts']}**",
        f"- Alta confianca: **{summary['high_confidence']}**",
        f"- Tickets simulados: **{summary['tickets_simulated']}**",
        f"- Deduplicados: **{summary['deduplicated']}**",
        f"- Endpoint sem protecao dentro de 30 dias: **{summary['stats']['endpoint_sem_protecao_recent_30d']}**",
        f"- Maquinas inativas excluidas: **{summary['stats']['inactive_machines_excluded']}**",
        f"- Validacao manual sem data: **{summary['stats']['validation_manual_no_last_seen']}**",
        f"- Tickets reais criados: **{summary['real_tickets_created']}**",
        "",
        "## Riscos / ressalvas",
    ]
    for risk in summary["stats"].get("risks", []):
        lines.append(f"- {risk}")
    lines.extend(["", "## Tickets simulados"])
    for ticket in summary["tickets"][:50]:
        lines.extend(
            [
                f"### {ticket['subject']}",
                f"- Fila: {ticket['queue']}",
                f"- Prioridade: {ticket['priority']}",
                f"- Severidade técnica: {ticket['severity']}",
                f"- Dedup: `{ticket['dedup_key']}`",
                f"- Impacto: {ticket['body']['impacto']}",
                f"- Evidencia: {'; '.join(ticket['body']['evidencia_sanitizada'])}",
                "",
            ]
        )
    if len(summary["tickets"]) > 50:
        lines.append(f"_Lista truncada no Markdown. Total no JSON: {len(summary['tickets'])}._")
    lines.extend(["", "**Bikon Tecnologia**", "Sua empresa parar de depender de você em 90 dias", ""])
    md_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dry-run Bitdefender GravityZone -> tickets Ninja")
    parser.add_argument("--per-page", type=int, default=100)
    parser.add_argument("--max-companies", type=int)
    parser.add_argument("--max-endpoints", type=int)
    parser.add_argument("--workers", type=int, default=8, help="Leituras paralelas de detalhe GravityZone. Somente leitura.")
    parser.add_argument("--state", type=Path, default=STATE_PATH)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    json_path = args.output_json or (REPORTS_DIR / f"bitdefender-ninja-dry-run-{timestamp}.json")
    md_path = args.output_md or (REPORTS_DIR / f"bitdefender-ninja-dry-run-{timestamp}.md")

    gz_client = import_gz_client()
    client = gz_client.get_client()
    state = load_state(args.state)

    alerts, stats = collect_alerts(client, args.per_page, args.max_companies, args.max_endpoints, args.workers)
    tickets, deduped = deduplicate(alerts, state)
    summary = {
        "generated_at": now_iso(),
        "mode": "dry-run",
        "real_tickets_created": 0,
        "real_tickets_closed": 0,
        "cron_created": False,
        "state_written": False,
        "state_path": str(args.state),
        "stats": stats,
        "actionable_alerts": len(alerts),
        "high_confidence": len(tickets),
        "tickets_simulated": len(tickets),
        "deduplicated": deduped,
        "tickets": tickets,
        "output_json": str(json_path),
        "output_md": str(md_path),
    }
    if "state_warning" in state:
        summary["stats"]["risks"].append(state["state_warning"])

    write_outputs(summary, json_path, md_path)
    print(json.dumps({k: summary[k] for k in ("mode", "real_tickets_created", "real_tickets_closed", "cron_created", "actionable_alerts", "high_confidence", "tickets_simulated", "deduplicated", "output_json", "output_md")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

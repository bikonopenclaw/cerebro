#!/usr/bin/env python3
"""Cria tickets Ninja da Fase 1 Bitdefender aprovada."""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib import error, parse, request

ROOT = Path("/data/.openclaw/workspace-kowalski/bitdefender-gravityzone")
NINJA_ROOT = Path("/data/.openclaw/workspace-kowalski/ninjaone")
DEFAULT_DRY_RUN = ROOT / "relatorios" / "dry-run" / "bitdefender-ninja-dry-run-20260713-142253.json"
STATE_PATH = ROOT / "jobs" / "bitdefender-ninja-ticket-state.json"
LOG_PATH = ROOT / "jobs" / "bitdefender-ninja-ticket-production-log.jsonl"
REPORTS_DIR = ROOT / "relatorios" / "producao"
TOKEN_PATH = NINJA_ROOT / "config" / "oauth-user-context-token.json"
NINJA_ENV = NINJA_ROOT / "config" / ".env"

DEFAULT_NINJA_CLIENT_ID = 1  # 00 - Bikon Tech, triagem interna.
DEFAULT_TICKET_FORM_ID = 1
AUTO_CLOSE_TYPES = {"malware_nao_resolvido", "ameaca_ativa", "politica_critica_violada"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except PermissionError:
        pass


def append_log(record: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": now_iso(), **record}, ensure_ascii=False) + "\n")


def load_env(path: Path = NINJA_ENV) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def refresh_user_token() -> dict:
    load_env()
    token = read_json(TOKEN_PATH, {})
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("NinjaOne user-context token sem refresh_token. Refaça OAuth.")
    client_id = os.getenv("NINJAONE_USER_CLIENT_ID")
    client_secret = os.getenv("NINJAONE_USER_CLIENT_SECRET")
    token_url = os.getenv("NINJAONE_TOKEN_URL", "https://bikon.rmmservice.com/ws/oauth/token")
    if not client_id or not client_secret:
        raise RuntimeError("Faltam NINJAONE_USER_CLIENT_ID/SECRET no .env")
    body = parse.urlencode(
        {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        }
    ).encode()
    req = request.Request(
        token_url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=30) as resp:
        new_token = json.loads(resp.read().decode())
    if "refresh_token" not in new_token:
        new_token["refresh_token"] = refresh_token
    new_token["obtained_at"] = now_iso()
    write_json(TOKEN_PATH, new_token)
    return new_token


def user_token() -> str:
    token = read_json(TOKEN_PATH, {})
    if not token.get("access_token"):
        token = refresh_user_token()
    return token["access_token"]


def ninja_request(path: str, method: str = "GET", payload: dict | None = None, retry: bool = True):
    load_env()
    base = os.getenv("NINJAONE_API_BASE", "https://bikon.rmmservice.com/v2").rstrip("/")
    token = user_token()
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = request.Request(f"{base}/{path.lstrip('/')}", data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode(errors="replace")
            return json.loads(text) if text else None
    except error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        if exc.code == 401 and retry:
            refresh_user_token()
            return ninja_request(path, method, payload, retry=False)
        raise RuntimeError(f"NinjaOne HTTP {exc.code} em {method} {path}: {body[:800]}")


def html_pre(text: str) -> str:
    return "<pre>" + text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre>"


def parse_last_seen(evidence: list[str]) -> str | None:
    for item in evidence:
        if item.startswith("lastSeen="):
            value = item.split("=", 1)[1].strip()
            return value if value and value != "N/D" else None
    return None


def parse_api_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def age_days(value: str | None) -> int | None:
    dt = parse_api_datetime(value)
    if dt is None:
        return None
    return max(0, (datetime.now(timezone.utc) - dt).days)


def validate_dry_run(dry_run: dict) -> list[str]:
    errors: list[str] = []
    if dry_run.get("mode") != "dry-run":
        errors.append("Arquivo base não está em mode=dry-run.")
    if dry_run.get("real_tickets_created") != 0 or dry_run.get("real_tickets_closed") != 0:
        errors.append("Arquivo base não comprova zero ticket real criado/fechado.")
    if dry_run.get("cron_created") is not False:
        errors.append("Arquivo base não comprova cron_created=false.")
    tickets = dry_run.get("tickets")
    if not isinstance(tickets, list):
        errors.append("Arquivo base não tem lista tickets.")
        return errors
    if len(tickets) != 39:
        errors.append(f"Esperados 39 tickets de alta confiança; encontrado {len(tickets)}.")
    for ticket in tickets:
        typ = ticket.get("type")
        if typ in {"maquina_inativa", "validacao_manual"}:
            errors.append(f"Tipo bloqueado no pacote: {typ}.")
        if typ == "endpoint_sem_protecao":
            last_seen = parse_last_seen(ticket.get("body", {}).get("evidencia_sanitizada") or [])
            days = age_days(last_seen)
            if days is None:
                errors.append(f"endpoint_sem_protecao sem lastSeen confiável: {ticket.get('subject')}")
            elif days > 30:
                errors.append(f"endpoint_sem_protecao com lastSeen >30 dias: {ticket.get('subject')}")
    return errors


def ticket_payload(ticket: dict) -> dict:
    body = ticket.get("body") or {}
    evidence = body.get("evidencia_sanitizada") or []
    evidence_lines = "\n".join(f"- {item}" for item in evidence)
    text = f"""Ticket operacional Bitdefender, Fase 1 produção controlada.

Cliente afetado: {ticket.get('client')}
Endpoint: {ticket.get('endpoint')}
Tipo: {ticket.get('type')}
Severidade técnica: {ticket.get('severity')}
Fila operacional: padrão / triagem interna Bikon
Prioridade: padrão
Fonte: {body.get('fonte')}

Evidência sanitizada:
{evidence_lines}

Impacto:
{body.get('impacto')}

Ação esperada:
{body.get('acao_esperada')}

Deduplicação:
{ticket.get('dedup_key')}

Restrições:
Sem remediação automática no Bitdefender. Sem comunicação externa automática.
Auto-fechamento só quando nova coleta completa confirmar resolução do mesmo dedup_key.
"""
    critical = ticket.get("severity") == "critico"
    return {
        "subject": str(ticket.get("subject"))[:250],
        "description": {
            "body": text,
            "public": False,
            "timeTracked": 0,
            "htmlBody": html_pre(text),
            "duplicateInIncidents": False,
        },
        "type": "INCIDENT" if critical else "TASK",
        "status": "NEW",
        "clientId": DEFAULT_NINJA_CLIENT_ID,
        "ticketFormId": DEFAULT_TICKET_FORM_ID,
        "severity": "CRITICAL" if critical else "MAJOR",
        "priority": "MEDIUM",
        "tags": ["openclaw", "bitdefender", "fase1-producao"],
    }


def status_name(ticket: dict | None) -> str:
    status = (ticket or {}).get("status")
    if isinstance(status, dict):
        return str(status.get("name") or status.get("displayName") or "").upper()
    return str(status or "").upper()


def ticket_is_closed(ticket: dict | None) -> bool:
    return status_name(ticket) in {"RESOLVED", "CLOSED"}


def close_ticket(ticket_id: int | str | None) -> dict:
    if not ticket_id:
        raise RuntimeError("Sem ticket_id para fechar no Ninja")
    ticket = ninja_request(f"ticketing/ticket/{ticket_id}")
    if ticket_is_closed(ticket):
        return {"ticket_id": ticket_id, "status": status_name(ticket), "already_closed": True}

    full_payload = {
        "subject": ticket.get("subject"),
        "clientId": ticket.get("clientId"),
        "ticketFormId": ticket.get("ticketFormId"),
        "type": ticket.get("type"),
        "status": "RESOLVED",
        "severity": ticket.get("severity"),
        "priority": ticket.get("priority"),
        "tags": ticket.get("tags") or [],
    }
    for optional_key in ("nodeId", "locationId", "assignedAppUserId", "requesterUid", "followupTime", "version"):
        if ticket.get(optional_key) is not None:
            full_payload[optional_key] = ticket.get(optional_key)

    attempts = [full_payload, {"status": "RESOLVED"}, {"statusId": 5000}]
    errors: list[str] = []
    for payload in attempts:
        try:
            ninja_request(f"ticketing/ticket/{ticket_id}", method="PUT", payload=payload)
            updated = ninja_request(f"ticketing/ticket/{ticket_id}")
            return {"ticket_id": ticket_id, "status": status_name(updated), "already_closed": False}
        except Exception as exc:
            errors.append(str(exc))
    raise RuntimeError(f"Nao consegui fechar ticket {ticket_id}: " + " | ".join(errors[-2:]))


def live_tickets(workers: int, per_page: int) -> tuple[list[dict], dict]:
    sys.path.insert(0, str(ROOT / "scripts"))
    import monitorar_bitdefender_ninja_tickets as monitor  # noqa: PLC0415

    gz_client = monitor.import_gz_client()
    client = gz_client.get_client()
    alerts, stats = monitor.collect_alerts(client, per_page, None, None, workers)
    seen: set[str] = set()
    tickets: list[dict] = []
    duplicate_current = 0
    for alert in alerts:
        key = alert.dedup_key
        if key in seen:
            duplicate_current += 1
            continue
        seen.add(key)
        tickets.append(alert.simulated_ticket())
    stats["duplicate_current_alerts"] = duplicate_current
    return tickets, stats


def summarize(actions: list[dict]) -> dict:
    by_type: dict[str, int] = {}
    by_client: dict[str, int] = {}
    for action in actions:
        if action.get("action") not in {"created", "deduped", "closed"}:
            continue
        typ = action.get("type") or "N/D"
        client = action.get("client") or "N/D"
        by_type[typ] = by_type.get(typ, 0) + 1
        by_client[client] = by_client.get(client, 0) + 1
    return {"by_type": by_type, "by_client": by_client}


def write_report(report_path: Path, summary: dict, actions: list[dict], failures: list[dict]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Bikon Tecnologia",
        "## Relatório final, Bitdefender -> Ninja, Fase 1 produção controlada",
        "",
        f"**Gerado em:** {summary['generated_at']}",
        f"**Modo:** {summary['mode_label']}",
        "**Fila:** padrão / triagem interna Bikon",
        "**Prioridade:** padrão",
        "",
        "## Resumo",
        f"- Tickets criados: **{summary['created']}**",
        f"- Deduplicados: **{summary['deduped']}**",
        f"- Falhas: **{len(failures)}**",
        f"- Fechamentos automáticos: **{summary['closed']}**",
        f"- Fechamentos ignorados por falta de prova: **{summary['close_skipped']}**",
        f"- Cron criado nesta execução: **{summary['cron_created']}**",
        f"- Segredo exposto: **{summary['secret_exposed']}**",
        "",
        "## Criados / deduplicados",
    ]
    for action in actions:
        if action.get("action") not in {"created", "deduped"}:
            continue
        ticket_id = action.get("ticket_id", "N/D")
        lines.append(f"- `{ticket_id}` | {action.get('action')} | {action.get('type')} | {action.get('client')} | {action.get('endpoint')} | {action.get('subject')}")
    if failures:
        lines.extend(["", "## Falhas"])
        for failure in failures:
            lines.append(f"- {failure.get('subject')}: {failure.get('error')}")
    skipped = [item for item in actions if item.get("action") == "close_skipped"]
    if skipped:
        lines.extend(["", "## Fechamentos ignorados"])
        for item in skipped:
            lines.append(f"- `{item.get('ticket_id')}` | {item.get('type')} | {item.get('client')} | {item.get('endpoint')} | {item.get('reason')}")
    lines.extend(["", "## Totais por tipo"])
    for typ, count in sorted(summary["by_type"].items()):
        lines.append(f"- `{typ}`: {count}")
    lines.extend(["", "## Totais por cliente"])
    for client, count in sorted(summary["by_client"].items()):
        lines.append(f"- {client}: {count}")
    lines.extend(["", "## Garantias"])
    lines.extend(summary["guarantees"])
    lines.extend(["", "**Bikon Tecnologia**", "Sua empresa parar de depender de voce em 90 dias", ""])
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cria tickets Ninja da Fase 1 Bitdefender")
    parser.add_argument("--dry-run-json", type=Path, default=DEFAULT_DRY_RUN)
    parser.add_argument("--state", type=Path, default=STATE_PATH)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--execute", action="store_true", help="Cria tickets reais. Sem isso, só valida.")
    parser.add_argument("--live", action="store_true", help="Faz nova coleta GravityZone em vez de usar JSON fixo.")
    parser.add_argument("--auto-close", action="store_true", help="Fecha tickets resolvidos quando nova coleta confirmar ausência do problema.")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--per-page", type=int, default=100)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.live:
        tickets, live_stats = live_tickets(args.workers, args.per_page)
        dry_run = {
            "mode": "live",
            "tickets": tickets,
            "stats": live_stats,
            "real_tickets_created": 0,
            "real_tickets_closed": 0,
            "cron_created": False,
        }
        validation_errors: list[str] = []
        if live_stats.get("detail_failures"):
            validation_errors.append("Coleta live teve falha de detalhe; não é seguro criar/fechar ticket.")
    else:
        dry_run = read_json(args.dry_run_json, {})
        validation_errors = validate_dry_run(dry_run)
    if validation_errors:
        print(json.dumps({"status": "blocked", "errors": validation_errors}, ensure_ascii=False, indent=2))
        return 2

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    report_path = args.report or (REPORTS_DIR / f"bitdefender-ninja-fase1-producao-{timestamp}.md")
    state = read_json(args.state, {"active": {}, "history": []})
    active = state.setdefault("active", {})
    history = state.setdefault("history", [])
    actions: list[dict] = []
    failures: list[dict] = []

    if not args.execute:
        state_preview = read_json(args.state, {"active": {}})
        active_preview = state_preview.get("active") if isinstance(state_preview.get("active"), dict) else {}
        current_keys = {ticket["dedup_key"] for ticket in dry_run["tickets"]}
        would_create = sum(1 for ticket in dry_run["tickets"] if ticket["dedup_key"] not in active_preview)
        would_dedup = sum(1 for ticket in dry_run["tickets"] if ticket["dedup_key"] in active_preview)
        would_close = 0
        if args.live and args.auto_close:
            for key, item in active_preview.items():
                if key not in current_keys and item.get("active") and item.get("type") in AUTO_CLOSE_TYPES:
                    would_close += 1
        print(json.dumps({"status": "validated", "would_create": would_create, "would_dedup": would_dedup, "would_close": would_close, "state_path": str(args.state)}, ensure_ascii=False, indent=2))
        return 0

    # Prova de autenticação antes do primeiro POST.
    ninja_request("organizations")

    current_keys = {ticket["dedup_key"] for ticket in dry_run["tickets"]}

    for ticket in dry_run["tickets"]:
        key = ticket["dedup_key"]
        if key in active and active[key].get("ticket_id"):
            action = {
                "action": "deduped",
                "dedup_key": key,
                "ticket_id": active[key].get("ticket_id"),
                "subject": ticket.get("subject"),
                "client": ticket.get("client"),
                "endpoint": ticket.get("endpoint"),
                "type": ticket.get("type"),
            }
            actions.append(action)
            continue

        payload = ticket_payload(ticket)
        action = {
            "action": "create_attempt",
            "dedup_key": key,
            "subject": payload["subject"],
            "client": ticket.get("client"),
            "endpoint": ticket.get("endpoint"),
            "type": ticket.get("type"),
        }
        try:
            created = ninja_request("ticketing/ticket", method="POST", payload=payload)
            ticket_id = created.get("id") if isinstance(created, dict) else None
            action.update({"action": "created", "ticket_id": ticket_id})
            active[key] = {
                "active": True,
                "ticket_id": ticket_id,
                "subject": payload["subject"],
                "client": ticket.get("client"),
                "endpoint": ticket.get("endpoint"),
                "type": ticket.get("type"),
                "severity": ticket.get("severity"),
                "created_at": now_iso(),
                "source_dry_run": str(args.dry_run_json),
            }
            history.append({"event": "created", "dedup_key": key, "ticket_id": ticket_id, "ts": now_iso()})
            state["updated_at"] = now_iso()
            state["source_dry_run"] = str(args.dry_run_json)
            write_json(args.state, state)
            append_log({"event": "ticket_created", **action})
        except Exception as exc:
            action.update({"action": "create_failed", "error": str(exc)[:800]})
            failures.append(action)
            append_log({"event": "ticket_create_failed", **action})
        actions.append(action)

    if args.live and args.auto_close:
        for key, item in list(active.items()):
            if key in current_keys or not item.get("active"):
                continue
            close_action = {
                "action": "close_attempt",
                "dedup_key": key,
                "ticket_id": item.get("ticket_id"),
                "subject": item.get("subject"),
                "client": item.get("client"),
                "endpoint": item.get("endpoint"),
                "type": item.get("type"),
            }
            if item.get("type") not in AUTO_CLOSE_TYPES:
                close_action.update({"action": "close_skipped", "reason": "Tipo exige prova adicional; não fechar automaticamente."})
                actions.append(close_action)
                continue
            try:
                close_result = close_ticket(item.get("ticket_id"))
                close_action.update({"action": "closed", **close_result})
                item["active"] = False
                item["closed_at"] = now_iso()
                item["close_reason"] = "Nova coleta sem alerta de alta confianca para o mesmo dedup_key."
                history.append({"event": "closed", "dedup_key": key, "ticket_id": item.get("ticket_id"), "ts": now_iso()})
                state["updated_at"] = now_iso()
                write_json(args.state, state)
                append_log({"event": "ticket_closed", **close_action})
            except Exception as exc:
                close_action.update({"action": "close_failed", "error": str(exc)[:800]})
                failures.append(close_action)
                append_log({"event": "ticket_close_failed", **close_action})
            actions.append(close_action)

    totals = summarize(actions)
    mode_bits = []
    if args.live:
        mode_bits.append("coleta live")
    else:
        mode_bits.append("base dry-run validada")
    mode_bits.append("criação real" if args.execute else "validação")
    if args.auto_close:
        mode_bits.append("auto-fechamento condicional")
    else:
        mode_bits.append("sem auto-fechamento")
    guarantees = [
        "- Sem remediação Bitdefender.",
        "- Sem alteração de política Bitdefender.",
        "- Sem isolar, quarentenar, excluir ou escanear endpoint.",
        "- Sem comunicação externa.",
        "- Sem ticket para máquina inativa.",
        "- Sem ticket para validação manual sem data confiável.",
        "- Sem segredo/token/credencial no relatório.",
    ]
    if args.auto_close:
        guarantees.insert(0, "- Auto-fechamento só com nova coleta completa confirmando resolução do mesmo dedup_key.")
    else:
        guarantees.insert(0, "- Sem auto-fechamento nesta execução.")
    summary = {
        "generated_at": now_iso(),
        "mode_label": ", ".join(mode_bits),
        "created": sum(1 for item in actions if item.get("action") == "created"),
        "deduped": sum(1 for item in actions if item.get("action") == "deduped"),
        "closed": sum(1 for item in actions if item.get("action") == "closed"),
        "close_skipped": sum(1 for item in actions if item.get("action") == "close_skipped"),
        "cron_created": 0,
        "secret_exposed": 0,
        **totals,
        "report_path": str(report_path),
        "state_path": str(args.state),
        "guarantees": guarantees,
    }
    write_report(report_path, summary, actions, failures)
    print(json.dumps({"summary": summary, "failures": failures}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Sentinel v2: canario deterministico, read-only e com pausa segura."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "state" / "sentinel-canary-v2.json"
CYCLE_LOG = ROOT / "logs" / "sentinel-canary-v2-cycles.jsonl"
AUDIT_LOG = ROOT / "logs" / "sentinel-canary-v2-audit.jsonl"
LOCK_PATH = ROOT / "state" / "sentinel-canary-v2.lock"
CONTEXT_MAP = ROOT / "context" / "operational_context_map.json"

RUNNER_VERSION = "2.1.0"
SCHEMA_VERSION = 2
EXPECTED_CLIENTS = 21
COLLECTOR_JOB_NAME = "Sentinel v2 canario 24h ciclo 30m"
SEVERITY_ORDER = {"P1": 4, "P2": 3, "P3": 2, "P4": 1}
NEXT_SEVERITY = {"P4": "P3", "P3": "P2", "P2": "P1", "P1": "P1"}

COMMANDS = {
    "ninjaone": [sys.executable, "integrations/ninjaone/ninjaone_readonly.py", "probe"],
    "arx": [sys.executable, "integrations/arx/arx_readonly.py", "probe"],
    "bitdefender": [sys.executable, "integrations/bitdefender/bitdefender_readonly.py", "probe"],
    "context": [sys.executable, "context/operational_context.py", "summary"],
    "logs": [sys.executable, "integrations/logs/operational_logs.py", "health"],
}


class StateDivergence(RuntimeError):
    """Estado persistido nao corresponde a janela aprovada."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("horario exige timezone")
    return parsed.astimezone(timezone.utc)


def window_id(start: datetime, until: datetime) -> str:
    raw = f"sentinel-v2|{iso_utc(start)}|{iso_utc(until)}".encode()
    return hashlib.sha256(raw).hexdigest()[:24]


def validate_window(start: datetime, until: datetime) -> None:
    if until <= start:
        raise ValueError("fim precisa ser posterior ao inicio")
    if until - start != timedelta(hours=24):
        raise ValueError("janela aprovada precisa ter exatamente 24 horas")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def secure_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        encoded = (json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n").encode()
        os.write(descriptor, encoded)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.replace(temporary, path)
    os.chmod(path, 0o600)


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        payload = (json.dumps(value, ensure_ascii=True, sort_keys=True) + "\n").encode()
        os.write(descriptor, payload)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.chmod(path, 0o600)


def audit_event(run_id: str, action: str, result: str, **details: Any) -> None:
    allowed = {
        "cycle_id",
        "reason",
        "collector_job_id",
        "source_summary_sha256",
        "state_sha256",
    }
    event = {
        "actor": "Sentinel",
        "timestamp_utc": iso_utc(utc_now()),
        "run_id": run_id,
        "action": action,
        "result": result,
        "details": {key: value for key, value in details.items() if key in allowed},
    }
    append_jsonl(AUDIT_LOG, event)


def load_policy() -> dict[str, Any]:
    with CONTEXT_MAP.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    clients = data.get("clients")
    owners = data.get("owner_profiles")
    slas = data.get("sla_profiles")
    if not isinstance(clients, dict) or len(clients) != EXPECTED_CLIENTS:
        raise RuntimeError("mapa operacional nao contem exatamente 21 clientes")
    if not isinstance(owners, dict) or not isinstance(slas, dict):
        raise RuntimeError("perfis de owner/SLA ausentes")
    used_slas: set[str] = set()
    for client_id, mapping in clients.items():
        owner = mapping.get("owner")
        sla = mapping.get("sla")
        if owner not in owners or sla not in slas:
            raise RuntimeError(f"owner/SLA divergente para {client_id}")
        used_slas.add(sla)
    if len(used_slas) != 1:
        raise RuntimeError("canario agregado exige um unico perfil SLA")
    sla_name = next(iter(used_slas))
    profile = slas[sla_name]
    for severity in SEVERITY_ORDER:
        values = profile.get(severity, {})
        ack = values.get("ack_min")
        escalate = values.get("escalate_min")
        if not isinstance(ack, int) or not isinstance(escalate, int):
            raise RuntimeError(f"SLA invalido para {severity}")
        if ack <= 0 or escalate < ack:
            raise RuntimeError(f"SLA inconsistente para {severity}")
    return {
        "client_count": len(clients),
        "owner_profiles": len({mapping["owner"] for mapping in clients.values()}),
        "sla_profile": sla_name,
        "sla": profile,
    }


def validate_source_files() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for source, command in COMMANDS.items():
        path = ROOT / command[1]
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"cliente de fonte invalido: {source}")
        hashes[source] = sha256_file(path)
    return hashes


def load_state(start: datetime, until: datetime, collector_job_id: str) -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    if STATE_PATH.is_symlink():
        raise StateDivergence("estado e symlink")
    with STATE_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    expected_run_id = window_id(start, until)
    checks = {
        "schema_version": SCHEMA_VERSION,
        "run_id": expected_run_id,
        "start_utc": iso_utc(start),
        "until_utc": iso_utc(until),
        "collector_job_id": collector_job_id,
    }
    if not isinstance(data, dict):
        raise StateDivergence("estado nao e objeto")
    for key, expected in checks.items():
        if data.get(key) != expected:
            raise StateDivergence(f"estado divergiu em {key}")
    if data.get("status") not in {"active", "paused", "closed"}:
        raise StateDivergence("status de estado invalido")
    if not isinstance(data.get("cycle_count"), int) or data["cycle_count"] < 0:
        raise StateDivergence("contador de ciclos invalido")
    return data


def run_source(name: str, command: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=150,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}
    if completed.returncode != 0:
        return {"ok": False, "error": "nonzero_exit", "exit_code": completed.returncode}
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": "invalid_json"}
    if not isinstance(payload, dict):
        return {"ok": False, "error": "invalid_schema"}
    return {"ok": True, "payload": payload}


def summarize_sources(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for name, result in results.items():
        if not result["ok"]:
            summary[name] = {"ok": False, "error": result["error"]}
            continue
        payload = result["payload"]
        if name == "ninjaone":
            summary[name] = {
                "ok": bool(payload.get("ok")),
                "scope": payload.get("scope"),
                "write_capability_exposed": payload.get("write_capability_exposed"),
                "counts": {
                    item.get("endpoint"): item.get("items")
                    for item in payload.get("results", [])
                    if isinstance(item, dict)
                },
            }
        elif name == "arx":
            summary[name] = {
                "ok": bool(payload.get("ok")),
                "clients": payload.get("clients"),
                "accounts": payload.get("accounts"),
                "current_status": payload.get("current_status", {}),
                "write_methods_exposed": payload.get("write_methods_exposed"),
            }
        elif name == "bitdefender":
            summary[name] = {
                "ok": bool(payload.get("ok")),
                "write_methods_exposed": payload.get("write_methods_exposed"),
                "counts": {
                    item.get("operation"): item.get("count")
                    for item in payload.get("results", [])
                    if isinstance(item, dict)
                },
            }
        elif name == "context":
            summary[name] = {
                "ok": True,
                "registered_clients": payload.get("registered_clients"),
                "active_clients": payload.get("active_clients"),
                "operational_gaps": payload.get("operational_gaps", {}),
                "severity_profile": payload.get("severity_profile"),
            }
        else:
            gateway = payload.get("gateway", {})
            jobs = payload.get("jobs", {})
            summary[name] = {
                "ok": True,
                "gateway": {
                    "sampled_events": gateway.get("sampled_events"),
                    "alerts_by_level": gateway.get("alerts_by_level", {}),
                    "alerts_by_safe_category": gateway.get("alerts_by_safe_category", {}),
                },
                "jobs": {
                    key: {
                        "available": value.get("available"),
                        "modified_at_utc": value.get("modified_at_utc"),
                    }
                    for key, value in jobs.items()
                    if isinstance(value, dict)
                },
            }
    return summary


def finding(key: str, severity: str, title: str, evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": key,
        "severity": severity,
        "title": title,
        "evidence": evidence,
    }


def provisional_classification(
    item: dict[str, Any],
    *,
    effective_severity: str,
    observed_at: datetime,
) -> dict[str, Any]:
    key = item["key"]
    aggregate_without_attribution = {
        "ninjaone:alerts-present",
        "arx:attention",
        "arx:critical",
        "arx:other",
        "bitdefender:incidents",
        "bitdefender:quarantine",
        "gateway:new-fatal",
        "gateway:new-error",
    }
    attributed = key not in aggregate_without_attribution
    impact_confirmed = key not in aggregate_without_attribution
    gates = {
        "G1_authorized_direct_source": True,
        "G2_unique_attribution": attributed,
        "G3_freshness_within_cycle": True,
        "G4_deterministic_rule_no_conflict": True,
        "G5_impact_or_operational_intent_confirmed": impact_confirmed,
    }
    failed = [name for name, passed in gates.items() if not passed]
    if not failed:
        confidence = "high"
    elif failed == ["G5_impact_or_operational_intent_confirmed"]:
        confidence = "medium"
    else:
        confidence = "low"

    if key == "ninjaone:alerts-present":
        hypothesis = "existem alertas ativos; impacto por item ainda nao foi atribuido"
        gap = "cliente, ativo, tipo de condicao e impacto por alerta"
        error_risk = "P3 agregado pode superestimar alerta preventivo ou ocultar impacto localizado maior"
        evidence_to_close = "leitura detalhada autorizada que atribua cada alerta e confirme impacto"
    elif key == "arx:other":
        hypothesis = "estado transitorio normal ou condicao degradada ainda sem classificacao"
        gap = "cliente, ativo, ultima conclusao, ultimo sucesso e janela autoritativa"
        error_risk = "P3 pode superestimar execucao normal; P4 pode mascarar continuidade degradada"
        evidence_to_close = "atribuicao sanitizada e freshness de conclusao/sucesso pela rota aprovada"
    elif key.startswith("arx:"):
        hypothesis = "estado agregado ARX exige validacao operacional do item afetado"
        gap = "atribuicao unica e impacto por conta"
        error_risk = "severidade conservadora pode superestimar ou subestimar impacto localizado"
        evidence_to_close = "atribuicao sanitizada e confirmacao do resultado do backup"
    elif key.startswith("bitdefender:"):
        hypothesis = "sinal agregado de seguranca exige atribuicao antes de classificacao final"
        gap = "empresa, endpoint, evento e impacto por item"
        error_risk = "contagem agregada pode ocultar recorrencia ou evento ja contido"
        evidence_to_close = "atribuicao sanitizada e estado de contencao pela rota aprovada"
    elif key.startswith("gateway:"):
        hypothesis = "novo evento do gateway pode indicar degradacao operacional"
        gap = "evento atribuido e impacto confirmado"
        error_risk = "delta agregado pode representar ruido ou falha material"
        evidence_to_close = "categoria segura, recorrencia e impacto confirmados"
    else:
        hypothesis = "o fato observado corresponde ao gate operacional descrito"
        gap = "nenhuma lacuna material no escopo do gate"
        error_risk = "baixo; regra deterministica pode pausar de forma conservadora"
        evidence_to_close = "novo ciclo sem o desvio e validacao do gate correspondente"

    return {
        "fact_observed": {
            "title": item["title"],
            "evidence": item["evidence"],
            "observed_at_utc": iso_utc(observed_at),
        },
        "hypothesis": hypothesis,
        "classification": effective_severity,
        "confidence": confidence,
        "confidence_criteria": [
            {"gate": name, "passed": passed}
            for name, passed in gates.items()
        ],
        "gap_preventing_final": gap,
        "error_risk": error_risk,
        "evidence_to_close": evidence_to_close,
        "freshness": {
            "observed_at_utc": iso_utc(observed_at),
            "review_due_utc": iso_utc(observed_at + timedelta(minutes=30)),
            "authoritative_window": "not_configured" if key.startswith("arx:") else "cycle_30m",
        },
        "owner": "Sentinel",
    }


def build_findings(summary: dict[str, Any], previous: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for source, payload in summary.items():
        if not payload.get("ok"):
            findings.append(finding(
                f"source:{source}:failure",
                "P2",
                f"Fonte {source} falhou",
                {"error": payload.get("error", "probe_failed")},
            ))

    ninja = summary.get("ninjaone", {})
    if ninja.get("ok"):
        if ninja.get("scope") != ["monitoring"] or ninja.get("write_capability_exposed") is not False:
            findings.append(finding(
                "ninjaone:readonly-boundary",
                "P2",
                "Trava read-only do NinjaOne divergiu",
                {"scope": ninja.get("scope"), "write_capability_exposed": ninja.get("write_capability_exposed")},
            ))
        alert_count = int(ninja.get("counts", {}).get("alerts") or 0)
        if alert_count > 0:
            findings.append(finding(
                "ninjaone:alerts-present",
                "P3",
                "NinjaOne possui alertas ativos",
                {"count": alert_count},
            ))

    arx = summary.get("arx", {})
    if arx.get("ok"):
        statuses = arx.get("current_status", {})
        for status, severity, title in (
            ("critical", "P2", "ARX/Cove possui conta critica"),
            ("attention", "P3", "ARX/Cove possui conta em atencao"),
            ("other", "P3", "ARX/Cove possui conta sem classificacao final"),
        ):
            count = int(statuses.get(status) or 0)
            if count > 0:
                findings.append(finding(f"arx:{status}", severity, title, {"count": count}))
        if arx.get("write_methods_exposed") is not False:
            findings.append(finding("arx:readonly-boundary", "P2", "Trava read-only do ARX/Cove divergiu", {}))

    bitdefender = summary.get("bitdefender", {})
    if bitdefender.get("ok"):
        counts = bitdefender.get("counts", {})
        for operation, title in (
            ("incidents", "Bitdefender reporta incidentes"),
            ("quarantine", "Bitdefender possui itens em quarentena"),
        ):
            count = int(counts.get(operation) or 0)
            if count > 0:
                findings.append(finding(f"bitdefender:{operation}", "P2", title, {"count": count}))
        if bitdefender.get("write_methods_exposed") is not False:
            findings.append(finding("bitdefender:readonly-boundary", "P2", "Trava read-only do Bitdefender divergiu", {}))

    context = summary.get("context", {})
    if context.get("ok"):
        registered = int(context.get("registered_clients") or 0)
        active = int(context.get("active_clients") or 0)
        if registered != EXPECTED_CLIENTS or active != EXPECTED_CLIENTS:
            findings.append(finding(
                "context:client-count-divergence",
                "P2",
                "Escopo de clientes divergiu de 21",
                {"registered": registered, "active": active, "expected": EXPECTED_CLIENTS},
            ))
        gaps = context.get("operational_gaps", {})
        owner_gap = int(gaps.get("operational_owner") or 0)
        sla_gap = int(gaps.get("sla") or 0)
        if owner_gap > 0 or sla_gap > 0:
            findings.append(finding(
                "context:owner-sla-gap",
                "P2",
                "Owner ou SLA nao reconciliado",
                {"operational_owner": owner_gap, "sla": sla_gap},
            ))

    logs = summary.get("logs", {})
    if logs.get("ok"):
        for job_name, payload in logs.get("jobs", {}).items():
            if payload.get("available") is not True:
                findings.append(finding(
                    f"logs:job:{job_name}:unavailable",
                    "P3",
                    f"Log operacional {job_name} indisponivel",
                    {},
                ))
        current_levels = logs.get("gateway", {}).get("alerts_by_level", {})
        previous_levels = previous.get("last_gateway_alerts", {})
        if previous_levels:
            fatal_delta = max(0, int(current_levels.get("FATAL") or 0) - int(previous_levels.get("FATAL") or 0))
            error_delta = max(0, int(current_levels.get("ERROR") or 0) - int(previous_levels.get("ERROR") or 0))
            if fatal_delta:
                findings.append(finding("gateway:new-fatal", "P2", "Gateway gerou novo evento FATAL", {"delta": fatal_delta}))
            if error_delta:
                findings.append(finding("gateway:new-error", "P3", "Gateway gerou novos eventos ERROR", {"delta": error_delta}))

    return sorted(findings, key=lambda item: (-SEVERITY_ORDER[item["severity"]], item["key"]))


def enrich_findings(
    findings: list[dict[str, Any]],
    previous: dict[str, Any],
    policy: dict[str, Any],
    now: datetime,
) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    previous_active = previous.get("active_findings", {})
    for item in findings:
        prior = previous_active.get(item["key"], {})
        first_seen_text = prior.get("first_seen_utc", iso_utc(now))
        first_seen = parse_utc(first_seen_text)
        elapsed_min = max(0, int((now - first_seen).total_seconds() // 60))
        original = item["severity"]
        sla = policy["sla"][original]
        escalated_by_sla = elapsed_min >= int(sla["escalate_min"])
        effective = NEXT_SEVERITY[original] if escalated_by_sla else original
        enriched.append({
            **item,
            "original_severity": original,
            "severity": effective,
            "provisional_classification": provisional_classification(
                item,
                effective_severity=effective,
                observed_at=now,
            ),
            "first_seen_utc": first_seen_text,
            "last_seen_utc": iso_utc(now),
            "occurrence_count": int(prior.get("occurrence_count") or 0) + 1,
            "elapsed_min": elapsed_min,
            "ack_due": elapsed_min >= int(sla["ack_min"]),
            "escalated_by_sla": escalated_by_sla,
            "sla": {"profile": policy["sla_profile"], **sla},
            "owner": "Sentinel",
            "escalation_owner": "Puppet Master",
        })
    return sorted(enriched, key=lambda item: (-SEVERITY_ORDER[item["severity"]], item["key"]))


def get_and_validate_collector(collector_job_id: str) -> dict[str, Any]:
    completed = subprocess.run(
        ["openclaw", "cron", "get", collector_job_id],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("nao foi possivel consultar o job coletor")
    payload = json.loads(completed.stdout)
    if payload.get("id") != collector_job_id or payload.get("name") != COLLECTOR_JOB_NAME:
        raise RuntimeError("job coletor nao corresponde ao alvo aprovado")
    command = payload.get("payload", {}).get("argv", [])
    if not isinstance(command, list) or str(Path(__file__)) not in command:
        raise RuntimeError("payload do coletor divergiu")
    return payload


def disable_collector(collector_job_id: str) -> None:
    payload = get_and_validate_collector(collector_job_id)
    if payload.get("enabled") is False:
        return
    completed = subprocess.run(
        ["openclaw", "cron", "disable", collector_job_id],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("falha ao desabilitar job coletor")


def preflight(start: datetime, until: datetime) -> dict[str, Any]:
    validate_window(start, until)
    if STATE_PATH.exists() or CYCLE_LOG.exists() or AUDIT_LOG.exists():
        raise RuntimeError("artefato v2 preexistente; estado novo nao esta garantido")
    policy = load_policy()
    hashes = validate_source_files()
    return {
        "ok": True,
        "runner_version": RUNNER_VERSION,
        "run_id": window_id(start, until),
        "start_utc": iso_utc(start),
        "until_utc": iso_utc(until),
        "duration_hours": 24,
        "expected_clients": EXPECTED_CLIENTS,
        "policy": {
            "owner_profiles": policy["owner_profiles"],
            "sla_profile": policy["sla_profile"],
            "sla": policy["sla"],
        },
        "source_client_sha256": hashes,
        "fresh_state": True,
    }


def selftest() -> dict[str, Any]:
    policy = load_policy()
    now = datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)
    base = finding("arx:attention", "P3", "teste", {"count": 1})
    first = enrich_findings([base], {}, policy, now)[0]
    previous = {"active_findings": {first["key"]: first}}
    later = enrich_findings([base], previous, policy, now + timedelta(minutes=480))[0]
    if first["severity"] != "P3" or later["severity"] != "P2" or not later["escalated_by_sla"]:
        raise RuntimeError("selftest de escalonamento falhou")
    duplicate = enrich_findings([base], previous, policy, now + timedelta(minutes=30))[0]
    if duplicate["first_seen_utc"] != first["first_seen_utc"] or duplicate["occurrence_count"] != 2:
        raise RuntimeError("selftest de deduplicacao falhou")
    provisional = first.get("provisional_classification", {})
    required = {
        "fact_observed",
        "hypothesis",
        "classification",
        "confidence",
        "confidence_criteria",
        "gap_preventing_final",
        "error_risk",
        "evidence_to_close",
        "freshness",
        "owner",
    }
    if set(provisional) != required:
        raise RuntimeError("selftest do padrao de incerteza falhou")
    return {
        "ok": True,
        "tests": [
            "dedup_by_key",
            "sla_escalation_p3_to_p2",
            "window_24h",
            "provisional_classification_contract",
        ],
        "runner_version": RUNNER_VERSION,
    }


def execute(start: datetime, until: datetime, collector_job_id: str) -> dict[str, Any]:
    validate_window(start, until)
    run_id = window_id(start, until)
    now = utc_now()
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    lock_descriptor = os.open(LOCK_PATH, os.O_WRONLY | os.O_CREAT, 0o600)
    try:
        try:
            fcntl.flock(lock_descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            audit_event(run_id, "state_divergence", "blocked", reason="overlapping_cycle", collector_job_id=collector_job_id)
            disable_collector(collector_job_id)
            raise StateDivergence("ciclo sobreposto; coletor pausado") from exc

        try:
            previous = load_state(start, until, collector_job_id)
        except (json.JSONDecodeError, OSError, StateDivergence) as exc:
            audit_event(run_id, "state_divergence", "blocked", reason=str(exc), collector_job_id=collector_job_id)
            disable_collector(collector_job_id)
            raise StateDivergence("estado divergente; coletor pausado") from exc

        if previous.get("status") in {"paused", "closed"}:
            disable_collector(collector_job_id)
            return {
                "ok": previous.get("status") == "closed",
                "status": previous.get("status"),
                "run_id": run_id,
                "no_sources_executed": True,
            }

        if now >= until:
            return close_canary(start, until, collector_job_id, allow_early=False)
        if now < start:
            raise RuntimeError("canario ainda nao iniciou")

        policy = load_policy()
        validate_source_files()
        raw = {name: run_source(name, command) for name, command in COMMANDS.items()}
        summary = summarize_sources(raw)
        base_findings = build_findings(summary, previous)
        findings = enrich_findings(base_findings, previous, policy, now)
        previous_active = previous.get("active_findings", {})
        current_active = {item["key"]: item for item in findings}
        new_findings = [item for item in findings if item["key"] not in previous_active]
        escalated_findings = [
            item for item in findings
            if item["key"] in previous_active
            and SEVERITY_ORDER[item["severity"]] > SEVERITY_ORDER[previous_active[item["key"]]["severity"]]
        ]
        resolved = sorted(set(previous_active) - set(current_active))
        sources_ok = all(item.get("ok") for item in summary.values())
        pause_findings = [item for item in findings if item["severity"] in {"P1", "P2"}]
        pause_reason = None
        if not sources_ok:
            pause_reason = "source_failure"
        elif pause_findings:
            pause_reason = "p1_p2_finding"

        cycle_id = uuid.uuid4().hex
        summary_sha = hashlib.sha256(json.dumps(summary, sort_keys=True).encode()).hexdigest()
        state = {
            "schema_version": SCHEMA_VERSION,
            "runner_version": RUNNER_VERSION,
            "run_id": run_id,
            "status": "paused" if pause_reason else "active",
            "pause_reason": pause_reason,
            "start_utc": iso_utc(start),
            "until_utc": iso_utc(until),
            "collector_job_id": collector_job_id,
            "first_cycle_utc": previous.get("first_cycle_utc", iso_utc(now)),
            "last_cycle_utc": iso_utc(now),
            "cycle_count": int(previous.get("cycle_count") or 0) + 1,
            "active_findings": current_active,
            "last_gateway_alerts": summary.get("logs", {}).get("gateway", {}).get("alerts_by_level", {}),
            "last_source_summary": summary,
            "last_source_summary_sha256": summary_sha,
            "last_cycle_id": cycle_id,
            "policy": {
                "expected_clients": EXPECTED_CLIENTS,
                "sla_profile": policy["sla_profile"],
                "owner": "Sentinel",
                "escalation_owner": "Puppet Master",
            },
        }
        secure_write_json(STATE_PATH, state)
        cycle = {
            "cycle_id": cycle_id,
            "timestamp_utc": iso_utc(now),
            "run_id": run_id,
            "start_utc": iso_utc(start),
            "until_utc": iso_utc(until),
            "sources_ok": sources_ok,
            "status": state["status"],
            "pause_reason": pause_reason,
            "new_findings": new_findings,
            "escalated_findings": escalated_findings,
            "resolved_keys": resolved,
            "active_findings": findings,
            "source_summary_sha256": summary_sha,
        }
        append_jsonl(CYCLE_LOG, cycle)
        audit_event(
            run_id,
            "cycle",
            state["status"],
            cycle_id=cycle_id,
            reason=pause_reason,
            collector_job_id=collector_job_id,
            source_summary_sha256=summary_sha,
            state_sha256=sha256_file(STATE_PATH),
        )
        if pause_reason:
            disable_collector(collector_job_id)
        return {
            "ok": sources_ok and not pause_reason,
            **cycle,
            "source_summary": summary,
        }
    finally:
        os.close(lock_descriptor)


def close_canary(
    start: datetime,
    until: datetime,
    collector_job_id: str,
    allow_early: bool = False,
) -> dict[str, Any]:
    validate_window(start, until)
    run_id = window_id(start, until)
    now = utc_now()
    if now < until and not allow_early:
        raise RuntimeError("encerramento recusado antes do fim aprovado")
    previous = load_state(start, until, collector_job_id)
    if not previous:
        raise StateDivergence("encerramento sem estado inicial")
    disable_collector(collector_job_id)
    state = {
        **previous,
        "status": "closed",
        "closed_at_utc": iso_utc(now),
        "close_reason": "approved_window_complete" if now >= until else "approved_manual_close",
    }
    secure_write_json(STATE_PATH, state)
    audit_event(
        run_id,
        "close",
        "closed",
        reason=state["close_reason"],
        collector_job_id=collector_job_id,
        state_sha256=sha256_file(STATE_PATH),
    )
    return {
        "ok": True,
        "status": "closed",
        "run_id": run_id,
        "closed_at_utc": state["closed_at_utc"],
        "cycle_count": state.get("cycle_count", 0),
        "collector_disabled": True,
    }


def report(start: datetime, until: datetime, collector_job_id: str) -> dict[str, Any]:
    state = load_state(start, until, collector_job_id)
    return {
        "ok": bool(state),
        "runner_version": RUNNER_VERSION,
        "run_id": window_id(start, until),
        "status": state.get("status", "not_started"),
        "start_utc": iso_utc(start),
        "until_utc": iso_utc(until),
        "cycle_count": state.get("cycle_count", 0),
        "first_cycle_utc": state.get("first_cycle_utc"),
        "last_cycle_utc": state.get("last_cycle_utc"),
        "active_findings": list(state.get("active_findings", {}).values()),
        "last_source_summary": state.get("last_source_summary", {}),
        "collector_job_id": collector_job_id,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Canario read-only v2 do Sentinel")
    parser.add_argument("command", choices=("preflight", "selftest", "run", "summary", "close"))
    parser.add_argument("--start", help="inicio UTC ISO-8601")
    parser.add_argument("--until", help="fim UTC ISO-8601")
    parser.add_argument("--collector-job-id", help="ID exato do job coletor Sentinel v2")
    args = parser.parse_args()

    try:
        if args.command == "selftest":
            output = selftest()
        else:
            if not args.start or not args.until:
                parser.error("comando exige --start e --until")
            start = parse_utc(args.start)
            until = parse_utc(args.until)
            if args.command == "preflight":
                output = preflight(start, until)
            else:
                if not args.collector_job_id:
                    parser.error("comando exige --collector-job-id")
                if args.command == "run":
                    output = execute(start, until, args.collector_job_id)
                elif args.command == "summary":
                    output = report(start, until, args.collector_job_id)
                else:
                    output = close_canary(start, until, args.collector_job_id)
    except Exception as exc:
        output = {"ok": False, "error": exc.__class__.__name__, "detail": str(exc)}

    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if output.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())

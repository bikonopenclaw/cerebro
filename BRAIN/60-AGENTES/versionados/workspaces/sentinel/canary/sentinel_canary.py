#!/usr/bin/env python3
"""Orquestrador deterministico do canary read-only do Sentinel."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "state" / "sentinel-canary.json"
CYCLE_LOG = ROOT / "logs" / "sentinel-canary-cycles.jsonl"

COMMANDS = {
    "ninjaone": [sys.executable, "integrations/ninjaone/ninjaone_readonly.py", "probe"],
    "arx": [sys.executable, "integrations/arx/arx_readonly.py", "probe"],
    "bitdefender": [sys.executable, "integrations/bitdefender/bitdefender_readonly.py", "probe"],
    "context": [sys.executable, "context/operational_context.py", "summary"],
    "logs": [sys.executable, "integrations/logs/operational_logs.py", "health"],
}

SEVERITY_ORDER = {"P1": 4, "P2": 3, "P3": 2, "P4": 1}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("--until exige timezone")
    return parsed.astimezone(timezone.utc)


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    with STATE_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise RuntimeError("estado do canary invalido")
    return data


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


def append_cycle(value: dict[str, Any]) -> None:
    CYCLE_LOG.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(CYCLE_LOG, flags, 0o600)
    try:
        os.write(descriptor, (json.dumps(value, ensure_ascii=True, sort_keys=True) + "\n").encode())
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.chmod(CYCLE_LOG, 0o600)


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


def finding(key: str, severity: str, title: str, evidence: dict[str, Any]) -> dict[str, Any]:
    return {"key": key, "severity": severity, "title": title, "evidence": evidence}


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


def build_findings(summary: dict[str, Any], previous: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for source, payload in summary.items():
        if not payload.get("ok"):
            findings.append(finding(f"source:{source}:failure", "P2", f"Fonte {source} falhou", {"error": payload.get("error", "probe_failed")}))

    ninja = summary.get("ninjaone", {})
    if ninja.get("ok") and (ninja.get("scope") != ["monitoring"] or ninja.get("write_capability_exposed") is not False):
        findings.append(finding("ninjaone:readonly-boundary", "P2", "Trava read-only do NinjaOne divergiu", {"scope": ninja.get("scope"), "write_capability_exposed": ninja.get("write_capability_exposed")}))

    arx = summary.get("arx", {})
    if arx.get("ok"):
        statuses = arx.get("current_status", {})
        if int(statuses.get("critical") or 0) > 0:
            findings.append(finding("arx:critical", "P2", "ARX/Cove possui conta critica", {"count": statuses.get("critical")}))
        if int(statuses.get("attention") or 0) > 0:
            findings.append(finding("arx:attention", "P3", "ARX/Cove possui conta em atencao", {"count": statuses.get("attention")}))
        if arx.get("write_methods_exposed") is not False:
            findings.append(finding("arx:readonly-boundary", "P2", "Trava read-only do ARX/Cove divergiu", {}))

    bitdefender = summary.get("bitdefender", {})
    if bitdefender.get("ok"):
        counts = bitdefender.get("counts", {})
        if int(counts.get("incidents") or 0) > 0:
            findings.append(finding("bitdefender:incidents", "P2", "Bitdefender reporta incidentes", {"count": counts.get("incidents")}))
        if int(counts.get("quarantine") or 0) > 0:
            findings.append(finding("bitdefender:quarantine", "P2", "Bitdefender possui itens em quarentena", {"count": counts.get("quarantine")}))
        if bitdefender.get("write_methods_exposed") is not False:
            findings.append(finding("bitdefender:readonly-boundary", "P2", "Trava read-only do Bitdefender divergiu", {}))

    context = summary.get("context", {})
    if context.get("ok"):
        gaps = context.get("operational_gaps", {})
        if any(int(value or 0) > 0 for value in gaps.values()):
            findings.append(finding("context:operational-gaps", "P4", "Cadastro operacional possui lacunas", gaps))

    current_levels = summary.get("logs", {}).get("gateway", {}).get("alerts_by_level", {})
    previous_levels = previous.get("last_gateway_alerts", {})
    if previous_levels:
        fatal_delta = max(0, int(current_levels.get("FATAL") or 0) - int(previous_levels.get("FATAL") or 0))
        error_delta = max(0, int(current_levels.get("ERROR") or 0) - int(previous_levels.get("ERROR") or 0))
        if fatal_delta:
            findings.append(finding("gateway:new-fatal", "P2", "Gateway gerou novo evento FATAL", {"delta": fatal_delta}))
        if error_delta:
            findings.append(finding("gateway:new-error", "P3", "Gateway gerou novos eventos ERROR", {"delta": error_delta}))

    return sorted(findings, key=lambda item: (-SEVERITY_ORDER[item["severity"]], item["key"]))


def execute(until: datetime) -> dict[str, Any]:
    now = utc_now()
    if now >= until:
        return {"ok": True, "expired": True, "checked_at_utc": iso_utc(now), "until_utc": iso_utc(until)}

    previous = load_state()
    raw = {name: run_source(name, command) for name, command in COMMANDS.items()}
    summary = summarize_sources(raw)
    findings = build_findings(summary, previous)
    previous_active = previous.get("active_findings", {})
    current_active = {item["key"]: item for item in findings}
    new_findings = [item for item in findings if item["key"] not in previous_active]
    escalated = [
        item for item in findings
        if item["key"] in previous_active
        and SEVERITY_ORDER[item["severity"]] > SEVERITY_ORDER[previous_active[item["key"]]["severity"]]
    ]
    resolved = sorted(set(previous_active) - set(current_active))
    cycle_id = uuid.uuid4().hex
    state = {
        "schema_version": 1,
        "canary_until_utc": iso_utc(until),
        "first_cycle_utc": previous.get("first_cycle_utc", iso_utc(now)),
        "last_cycle_utc": iso_utc(now),
        "cycle_count": int(previous.get("cycle_count") or 0) + 1,
        "active_findings": current_active,
        "last_gateway_alerts": summary.get("logs", {}).get("gateway", {}).get("alerts_by_level", {}),
        "last_source_summary": summary,
        "last_cycle_id": cycle_id,
    }
    secure_write_json(STATE_PATH, state)
    cycle = {
        "cycle_id": cycle_id,
        "timestamp_utc": iso_utc(now),
        "until_utc": iso_utc(until),
        "sources_ok": all(item.get("ok") for item in summary.values()),
        "new_findings": new_findings,
        "escalated_findings": escalated,
        "resolved_keys": resolved,
        "active_findings": findings,
        "source_summary_sha256": hashlib.sha256(json.dumps(summary, sort_keys=True).encode()).hexdigest(),
    }
    append_cycle(cycle)
    return {"ok": cycle["sources_ok"], "expired": False, **cycle, "source_summary": summary}


def report(until: datetime) -> dict[str, Any]:
    state = load_state()
    return {
        "ok": bool(state),
        "expired": utc_now() >= until,
        "canary_until_utc": iso_utc(until),
        "cycle_count": state.get("cycle_count", 0),
        "first_cycle_utc": state.get("first_cycle_utc"),
        "last_cycle_utc": state.get("last_cycle_utc"),
        "active_findings": list(state.get("active_findings", {}).values()),
        "last_source_summary": state.get("last_source_summary", {}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Canary read-only do Sentinel")
    parser.add_argument("command", choices=("run", "summary"))
    parser.add_argument("--until", required=True, help="fim UTC ISO-8601 do canary")
    args = parser.parse_args()
    until = parse_utc(args.until)
    output = execute(until) if args.command == "run" else report(until)
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if output.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

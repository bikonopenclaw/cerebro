#!/usr/bin/env python3
"""Fail-closed order controller for critical Sentinel executions."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator


SCHEMA_VERSION = 1
ORCHESTRATION_ROOT = Path(__file__).resolve().parent
CANONICAL_STATE_DIR = ORCHESTRATION_ROOT / "state"
CANONICAL_CRON_CONFIG = ORCHESTRATION_ROOT / "noncritical-crons.json"
PRODUCTION_CRON_RUNNER = ("openclaw", "cron")
DEFAULT_LEASE_TTL_SECONDS = 1200
MIN_LEASE_TTL_SECONDS = 30
MAX_LEASE_TTL_SECONDS = 3600
ACTIVE_STATUSES = {
    "ACTIVATING_CRON_BLOCK",
    "AWAITING_ACK",
    "ACKED",
    "RUNNING",
    "CLOSING_CRON_RESTORE_FAILED",
}
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,255}$")


class GateError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def utc_after(seconds: int) -> str:
    return (
        datetime.now(timezone.utc) + timedelta(seconds=seconds)
    ).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_id(label: str, value: str) -> str:
    if not SAFE_ID.fullmatch(value):
        raise GateError(f"{label} inválido")
    return value


def resolve_existing_file(raw_path: str) -> Path:
    path = Path(raw_path).expanduser().resolve(strict=True)
    if not path.is_file():
        raise GateError(f"não é arquivo regular: {path}")
    return path


def default_state_dir() -> Path:
    return CANONICAL_STATE_DIR


def default_cron_config() -> Path:
    return CANONICAL_CRON_CONFIG


def validate_lease_ttl(value: int) -> int:
    if not MIN_LEASE_TTL_SECONDS <= value <= MAX_LEASE_TTL_SECONDS:
        raise GateError(
            "lease TTL fora do intervalo "
            f"{MIN_LEASE_TTL_SECONDS}..{MAX_LEASE_TTL_SECONDS}"
        )
    return value


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


class Controller:
    def __init__(
        self,
        state_dir: Path,
        cron_config: Path,
        cron_runner: tuple[str, ...],
        dry_run_cron: bool = False,
        test_mode: bool = False,
    ):
        self.state_dir = state_dir
        self.state_path = state_dir / "controller-state.json"
        self.lock_path = state_dir / "controller.lock"
        self.audit_path = state_dir / "audit.jsonl"
        self.ack_dir = state_dir / "acks"
        self.cron_config = cron_config
        self.cron_runner = cron_runner
        self.dry_run_cron = dry_run_cron
        self.test_mode = test_mode

    def ensure_dirs(self) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.ack_dir.mkdir(parents=True, exist_ok=True, mode=0o700)

    @contextmanager
    def locked(self) -> Iterator[None]:
        self.ensure_dirs()
        with self.lock_path.open("a+", encoding="utf-8") as handle:
            os.chmod(self.lock_path, 0o600)
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def blank_state(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "controller_state": "IDLE",
            "active_order": None,
            "latest_terminal_order": None,
            "updated_at_utc": utc_now(),
        }

    def load_state(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return self.blank_state()
        try:
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise GateError(f"estado corrompido: {exc}") from exc
        if state.get("schema_version") != SCHEMA_VERSION:
            raise GateError("versão de estado incompatível")
        active = state.get("active_order")
        if active is not None and active.get("status") not in ACTIVE_STATUSES:
            raise GateError("estado ativo inválido")
        return state

    def write_json_atomic(self, path: Path, value: Any, mode: int = 0o600) -> None:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", dir=str(path.parent)
        )
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(canonical_bytes(value))
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(temporary, mode)
            os.replace(temporary, path)
            directory_fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            if temporary.exists():
                temporary.unlink()

    def save_state(self, state: dict[str, Any]) -> None:
        state["updated_at_utc"] = utc_now()
        self.write_json_atomic(self.state_path, state)

    def last_audit_hash(self) -> str | None:
        if not self.audit_path.exists():
            return None
        last = None
        with self.audit_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    last = line
        if last is None:
            return None
        try:
            return json.loads(last)["event_sha256"]
        except (json.JSONDecodeError, KeyError) as exc:
            raise GateError("cadeia de auditoria corrompida") from exc

    def append_audit(self, event_type: str, detail: dict[str, Any]) -> dict[str, Any]:
        base = {
            "schema_version": SCHEMA_VERSION,
            "event_type": event_type,
            "recorded_at_utc": utc_now(),
            "previous_event_sha256": self.last_audit_hash(),
            "detail": detail,
        }
        event = {**base, "event_sha256": sha256_bytes(canonical_bytes(base))}
        payload = canonical_bytes(event)
        descriptor = os.open(
            self.audit_path,
            os.O_WRONLY | os.O_CREAT | os.O_APPEND,
            0o600,
        )
        try:
            os.write(descriptor, payload)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        return event

    def load_cron_targets(self) -> list[dict[str, str]]:
        try:
            value = json.loads(self.cron_config.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise GateError(f"configuração de cron inválida: {exc}") from exc
        jobs = value.get("jobs")
        if not isinstance(jobs, list) or not jobs:
            raise GateError("lista de crons não críticos vazia")
        normalized = []
        seen = set()
        for job in jobs:
            job_id = require_id("job_id", str(job.get("id", "")))
            name = str(job.get("name", "")).strip()
            if not name or job_id in seen:
                raise GateError("cron duplicado ou sem nome")
            seen.add(job_id)
            normalized.append({"id": job_id, "name": name})
        return normalized

    def cron_command(self, action: str, job_id: str) -> subprocess.CompletedProcess[str]:
        command = [*self.cron_runner, action, job_id]
        return subprocess.run(
            command,
            check=False,
            text=True,
            capture_output=True,
            timeout=30,
        )

    def inspect_cron(self, job: dict[str, str]) -> dict[str, Any]:
        result = self.cron_command("get", job["id"])
        if result.returncode != 0:
            raise GateError(
                f"falha ao consultar cron {job['id']}: {result.stderr.strip()}"
            )
        try:
            current = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise GateError(f"cron {job['id']} retornou JSON inválido") from exc
        if current.get("id") != job["id"]:
            raise GateError(f"cron divergente: {job['id']}")
        if current.get("name") != job["name"]:
            raise GateError(
                f"nome do cron divergente para {job['id']}: "
                f"esperado {job['name']!r}, observado {current.get('name')!r}"
            )
        return {
            "id": job["id"],
            "expected_name": job["name"],
            "observed_name": current.get("name"),
            "enabled": bool(current.get("enabled")),
            "was_enabled": bool(current.get("enabled")),
        }

    def set_cron(self, action: str, job: dict[str, str]) -> dict[str, Any]:
        job_id = require_id("job_id", job["id"])
        if self.dry_run_cron:
            raise GateError("dry-run de cron não pode validar pós-condição")
        result = self.cron_command(action, job_id)
        if result.returncode != 0:
            raise GateError(
                f"falha ao {action} cron {job_id}: {result.stderr.strip()}"
            )
        observed = self.inspect_cron(job)
        expected_enabled = action == "enable"
        if observed["enabled"] != expected_enabled:
            raise GateError(
                f"pós-condição de cron falhou para {job_id}: "
                f"esperado enabled={expected_enabled}, "
                f"observado enabled={observed['enabled']}"
            )
        self.append_audit(
            "CRON_STATE_VERIFIED",
            {
                "action": action,
                "id": job_id,
                "name": job["name"],
                "enabled": observed["enabled"],
            },
        )
        return observed

    def block_noncritical_crons(self) -> list[dict[str, Any]]:
        snapshot: list[dict[str, Any]] = []
        disabled: list[str] = []
        try:
            for job in self.load_cron_targets():
                record = self.inspect_cron(job)
                snapshot.append(record)
                if record["was_enabled"]:
                    self.set_cron("disable", job)
                    disabled.append(record["id"])
            return snapshot
        except Exception:
            for job_id in reversed(disabled):
                try:
                    record = next(item for item in snapshot if item["id"] == job_id)
                    self.set_cron(
                        "enable",
                        {"id": job_id, "name": record["expected_name"]},
                    )
                except Exception:
                    pass
            raise

    def restore_noncritical_crons(self, snapshot: list[dict[str, Any]]) -> None:
        restored: list[str] = []
        try:
            for record in snapshot:
                job = {
                    "id": require_id("job_id", record["id"]),
                    "name": str(record["expected_name"]),
                }
                if record.get("was_enabled"):
                    self.set_cron("enable", job)
                    restored.append(record["id"])
                else:
                    observed = self.inspect_cron(job)
                    if observed["enabled"]:
                        raise GateError(
                            f"cron originalmente desabilitado foi habilitado: {job['id']}"
                        )
                    self.append_audit(
                        "CRON_STATE_VERIFIED",
                        {
                            "action": "preserve-disabled",
                            "id": job["id"],
                            "name": job["name"],
                            "enabled": False,
                        },
                    )
        except Exception as exc:
            raise GateError(
                f"restauração de cron falhou após {len(restored)} itens: {exc}"
            ) from exc

    def terminalize_locked(
        self,
        state: dict[str, Any],
        active: dict[str, Any],
        result: str,
        event_type: str = "ORDER_CLOSED",
    ) -> dict[str, Any]:
        if active["critical"]:
            try:
                self.restore_noncritical_crons(active.get("cron_snapshot", []))
            except Exception as exc:
                active["status"] = "CLOSING_CRON_RESTORE_FAILED"
                state["controller_state"] = "DEGRADED_CRON_RESTORE_FAILED"
                self.save_state(state)
                self.append_audit(
                    "ORDER_CLOSE_FAILED",
                    {"order_id": active["order_id"], "error": str(exc)},
                )
                raise
        terminal = {
            "order_id": active["order_id"],
            "execution_id": active["execution_id"],
            "approval_id": active["approval_id"],
            "order_path": active["order_path"],
            "order_sha256": active["order_sha256"],
            "result": require_id("result", result),
            "closed_at_utc": utc_now(),
            "supersedes": active["supersedes"],
        }
        state["latest_terminal_order"] = terminal
        state["active_order"] = None
        state["controller_state"] = "IDLE"
        self.save_state(state)
        self.append_audit(event_type, terminal)
        return terminal

    def lease_expired(self, active: dict[str, Any]) -> bool:
        value = active.get("lease_expires_at_utc")
        if not value:
            return True
        try:
            return datetime.now(timezone.utc) >= parse_utc(str(value))
        except (TypeError, ValueError):
            return True

    def init(
        self,
        latest_order_id: str | None,
        latest_execution_id: str | None,
        latest_result: str | None,
        latest_order_sha256: str | None,
    ) -> dict[str, Any]:
        with self.locked():
            if self.state_path.exists():
                raise GateError("controlador já inicializado")
            state = self.blank_state()
            if latest_order_id:
                state["latest_terminal_order"] = {
                    "order_id": require_id("latest_order_id", latest_order_id),
                    "execution_id": require_id(
                        "latest_execution_id", latest_execution_id or ""
                    ),
                    "result": require_id("latest_result", latest_result or ""),
                    "order_sha256": latest_order_sha256,
                    "closed_at_utc": utc_now(),
                    "reconciled": True,
                }
            self.save_state(state)
            self.append_audit(
                "CONTROLLER_INITIALIZED",
                {"latest_terminal_order": state["latest_terminal_order"]},
            )
            return state

    def activate(self, args: argparse.Namespace) -> dict[str, Any]:
        order_path = resolve_existing_file(args.order_path)
        actual_hash = sha256_file(order_path)
        if args.order_sha256.lower() != actual_hash:
            raise GateError(
                f"hash da ordem divergente: esperado {args.order_sha256.lower()}, "
                f"observado {actual_hash}"
            )
        with self.locked():
            state = self.load_state()
            if state.get("active_order") is not None:
                active = state["active_order"]
                raise GateError(
                    f"já existe ordem ativa: {active['order_id']} ({active['status']})"
                )
            latest = state.get("latest_terminal_order")
            expected_supersedes = latest["order_id"] if latest else "NONE"
            if args.supersedes != expected_supersedes:
                raise GateError(
                    f"supersedes inválido: esperado {expected_supersedes}, "
                    f"recebido {args.supersedes}"
                )
            content = order_path.read_bytes()
            active = {
                "order_id": require_id("order_id", args.order_id),
                "order_path": str(order_path),
                "order_sha256": actual_hash,
                "order_bytes": len(content),
                "order_lines": len(content.splitlines()),
                "supersedes": args.supersedes,
                "approval_id": require_id("approval_id", args.approval_id),
                "execution_id": require_id("execution_id", args.execution_id),
                "coordinator": args.coordinator,
                "executor": args.executor,
                "critical": bool(args.critical),
                "status": "ACTIVATING_CRON_BLOCK",
                "activated_at_utc": utc_now(),
                "lease_ttl_seconds": validate_lease_ttl(args.lease_ttl_seconds),
                "lease_expires_at_utc": None,
                "ack": None,
                "cron_snapshot": [],
            }
            state["controller_state"] = "ACTIVATING"
            state["active_order"] = active
            self.save_state(state)
            self.append_audit(
                "ORDER_ACTIVATION_STARTED",
                {
                    "order_id": active["order_id"],
                    "order_path": active["order_path"],
                    "order_sha256": active["order_sha256"],
                    "supersedes": active["supersedes"],
                    "critical": active["critical"],
                },
            )
            try:
                if active["critical"]:
                    active["cron_snapshot"] = self.block_noncritical_crons()
                active["status"] = "AWAITING_ACK"
                state["controller_state"] = "ACTIVE_AWAITING_ACK"
                self.save_state(state)
                self.append_audit(
                    "ORDER_ACTIVATED",
                    {
                        "order_id": active["order_id"],
                        "status": active["status"],
                        "blocked_crons": [
                            item["id"]
                            for item in active["cron_snapshot"]
                            if item["was_enabled"]
                        ],
                    },
                )
                return active
            except Exception as exc:
                state["active_order"] = None
                state["controller_state"] = "IDLE"
                self.save_state(state)
                self.append_audit(
                    "ORDER_ACTIVATION_FAILED",
                    {"order_id": active["order_id"], "error": str(exc)},
                )
                raise

    def ack(self, args: argparse.Namespace) -> dict[str, Any]:
        supplied_path = resolve_existing_file(args.order_path)
        supplied_hash = args.order_sha256.lower()
        actual_hash = sha256_file(supplied_path)
        with self.locked():
            state = self.load_state()
            active = state.get("active_order")
            if active is None:
                raise GateError("não existe ordem ativa")
            if active["status"] != "AWAITING_ACK":
                raise GateError(f"ACK inválido no estado {active['status']}")
            checks = {
                "order_id": args.order_id == active["order_id"],
                "order_path": str(supplied_path) == active["order_path"],
                "supplied_hash": supplied_hash == active["order_sha256"],
                "observed_hash": actual_hash == active["order_sha256"],
                "approval_id": args.approval_id == active["approval_id"],
                "execution_id": args.execution_id == active["execution_id"],
            }
            if not all(checks.values()):
                self.append_audit(
                    "ORDER_ACK_REJECTED",
                    {
                        "active_order_id": active["order_id"],
                        "received_order_id": args.order_id,
                        "checks": checks,
                    },
                )
                raise GateError(f"ACK rejeitado: {checks}")
            ack = {
                "record_type": "sentinel_order_ack",
                "order_id": active["order_id"],
                "order_path": active["order_path"],
                "order_sha256": active["order_sha256"],
                "approval_id": active["approval_id"],
                "execution_id": active["execution_id"],
                "executor": args.executor,
                "acknowledged_at_utc": utc_now(),
                "checks": checks,
            }
            ack["ack_sha256"] = sha256_bytes(canonical_bytes(ack))
            self.write_json_atomic(self.ack_dir / f"{active['order_id']}.json", ack)
            active["ack"] = ack
            active["status"] = "ACKED"
            state["controller_state"] = "ACTIVE_ACKED"
            self.save_state(state)
            self.append_audit(
                "ORDER_ACKED",
                {
                    "order_id": active["order_id"],
                    "ack_sha256": ack["ack_sha256"],
                },
            )
            return ack

    def start(self, args: argparse.Namespace) -> dict[str, Any]:
        with self.locked():
            state = self.load_state()
            active = state.get("active_order")
            if active is None:
                raise GateError("não existe ordem ativa")
            checks = self.binding_checks(active, args)
            if active["status"] != "ACKED":
                raise GateError(f"start exige ACKED, observado {active['status']}")
            if not all(checks.values()):
                raise GateError(f"binding de start rejeitado: {checks}")
            active["status"] = "RUNNING"
            active["technical_started_at"] = utc_now()
            active["lease_expires_at_utc"] = utc_after(active["lease_ttl_seconds"])
            state["controller_state"] = "ACTIVE_RUNNING"
            self.save_state(state)
            self.append_audit(
                "ORDER_TECHNICAL_START",
                {
                    "order_id": active["order_id"],
                    "approval_id": active["approval_id"],
                    "execution_id": active["execution_id"],
                    "technical_started_at": active["technical_started_at"],
                    "lease_expires_at_utc": active["lease_expires_at_utc"],
                },
            )
            return active

    def binding_checks(
        self, active: dict[str, Any], args: argparse.Namespace
    ) -> dict[str, bool]:
        supplied_path = resolve_existing_file(args.order_path)
        observed_hash = sha256_file(supplied_path)
        return {
            "order_id": args.order_id == active["order_id"],
            "order_path": str(supplied_path) == active["order_path"],
            "supplied_hash": args.order_sha256.lower() == active["order_sha256"],
            "observed_hash": observed_hash == active["order_sha256"],
            "approval_id": args.approval_id == active["approval_id"],
            "execution_id": args.execution_id == active["execution_id"],
        }

    def assert_binding(self, args: argparse.Namespace) -> dict[str, Any]:
        with self.locked():
            state = self.load_state()
            active = state.get("active_order")
            if active is None:
                self.append_audit(
                    "ORDER_ASSERT_REJECTED",
                    {
                        "received_order_id": args.order_id,
                        "reason": "NO_ACTIVE_ORDER",
                    },
                )
                raise GateError("nenhuma ordem ativa")
            if active["status"] != "RUNNING":
                self.append_audit(
                    "ORDER_ASSERT_REJECTED",
                    {
                        "active_order_id": active["order_id"],
                        "received_order_id": args.order_id,
                        "reason": f"INVALID_STATUS:{active['status']}",
                    },
                )
                self.terminalize_locked(
                    state,
                    active,
                    "STALE_OR_UNBOUND_ORDER_REJECTED",
                    "ORDER_FAIL_CLOSED",
                )
                raise GateError(
                    f"ordem não autorizada para ação técnica: {active['status']}"
                )
            checks = self.binding_checks(active, args)
            if not all(checks.values()):
                self.append_audit(
                    "ORDER_ASSERT_REJECTED",
                    {
                        "active_order_id": active["order_id"],
                        "received_order_id": args.order_id,
                        "reason": "BINDING_MISMATCH",
                        "checks": checks,
                    },
                )
                self.terminalize_locked(
                    state,
                    active,
                    "STALE_OR_UNBOUND_ORDER_REJECTED",
                    "ORDER_FAIL_CLOSED",
                )
                raise GateError(f"ordem velha ou não vinculada: {checks}")
            if self.lease_expired(active):
                self.append_audit(
                    "ORDER_ASSERT_REJECTED",
                    {
                        "active_order_id": active["order_id"],
                        "received_order_id": args.order_id,
                        "reason": "LEASE_EXPIRED_OR_MISSING",
                    },
                )
                self.terminalize_locked(
                    state,
                    active,
                    "EXECUTION_LEASE_EXPIRED",
                    "ORDER_LEASE_EXPIRED",
                )
                raise GateError("lease ausente ou expirada")
            return {
                "allowed": True,
                "order_id": active["order_id"],
                "status": active["status"],
                "order_sha256": active["order_sha256"],
                "ack_sha256": active["ack"]["ack_sha256"],
                "critical": active["critical"],
                "lease_expires_at_utc": active["lease_expires_at_utc"],
                "checked_at_utc": utc_now(),
            }

    def renew(self, args: argparse.Namespace) -> dict[str, Any]:
        with self.locked():
            state = self.load_state()
            active = state.get("active_order")
            if active is None:
                raise GateError("nenhuma ordem ativa")
            if active["status"] != "RUNNING":
                raise GateError(f"renew exige RUNNING, observado {active['status']}")
            checks = self.binding_checks(active, args)
            if not all(checks.values()):
                self.terminalize_locked(
                    state,
                    active,
                    "STALE_OR_UNBOUND_ORDER_REJECTED",
                    "ORDER_FAIL_CLOSED",
                )
                raise GateError(f"binding de renew rejeitado: {checks}")
            existing_lease = active.get("lease_expires_at_utc")
            if existing_lease and self.lease_expired(active):
                self.terminalize_locked(
                    state,
                    active,
                    "EXECUTION_LEASE_EXPIRED",
                    "ORDER_LEASE_EXPIRED",
                )
                raise GateError("lease expirada")
            ttl = validate_lease_ttl(args.lease_ttl_seconds)
            active["lease_ttl_seconds"] = ttl
            active["lease_expires_at_utc"] = utc_after(ttl)
            state["controller_state"] = "ACTIVE_RUNNING"
            self.save_state(state)
            self.append_audit(
                "ORDER_LEASE_RENEWED" if existing_lease else "ORDER_LEASE_INITIALIZED",
                {
                    "order_id": active["order_id"],
                    "execution_id": active["execution_id"],
                    "lease_expires_at_utc": active["lease_expires_at_utc"],
                    "lease_ttl_seconds": ttl,
                },
            )
            return {
                "allowed": True,
                "order_id": active["order_id"],
                "execution_id": active["execution_id"],
                "status": active["status"],
                "lease_expires_at_utc": active["lease_expires_at_utc"],
            }

    def recover(self) -> dict[str, Any]:
        with self.locked():
            state = self.load_state()
            active = state.get("active_order")
            if active is None:
                return {"recovered": False, "reason": "NO_ACTIVE_ORDER"}
            if active["status"] != "RUNNING":
                return {
                    "recovered": False,
                    "reason": f"NOT_RUNNING:{active['status']}",
                }
            if not self.lease_expired(active):
                return {
                    "recovered": False,
                    "reason": "LEASE_VALID",
                    "lease_expires_at_utc": active["lease_expires_at_utc"],
                }
            terminal = self.terminalize_locked(
                state,
                active,
                "EXECUTION_LEASE_EXPIRED",
                "ORDER_LEASE_EXPIRED",
            )
            return {"recovered": True, "terminal": terminal}

    def stop(self, args: argparse.Namespace) -> dict[str, Any]:
        with self.locked():
            state = self.load_state()
            active = state.get("active_order")
            if active is None:
                return {"stopped": False, "reason": "NO_ACTIVE_ORDER"}
            requested_by = require_id("requested_by", args.requested_by)
            self.append_audit(
                "ORDER_STOP_REQUESTED",
                {
                    "active_order_id": active["order_id"],
                    "requested_by": requested_by,
                    "reason": args.reason[:200],
                },
            )
            result = (
                "STOPPED_BY_OWNER"
                if requested_by == "Hebert"
                else "STOPPED_BY_PUPPET_MASTER"
            )
            terminal = self.terminalize_locked(
                state,
                active,
                result,
                "ORDER_STOPPED",
            )
            return {"stopped": True, "terminal": terminal}

    def close(self, args: argparse.Namespace) -> dict[str, Any]:
        with self.locked():
            state = self.load_state()
            active = state.get("active_order")
            if active is None:
                raise GateError("nenhuma ordem ativa")
            if (
                args.order_id != active["order_id"]
                or args.execution_id != active["execution_id"]
            ):
                raise GateError("fechamento não corresponde à ordem ativa")
            return self.terminalize_locked(state, active, args.result)

    def status(self) -> dict[str, Any]:
        with self.locked():
            state = self.load_state()
            state["audit_head_sha256"] = self.last_audit_hash()
            return state


def binding_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--order-id", required=True)
    parser.add_argument("--order-path", required=True)
    parser.add_argument("--order-sha256", required=True)
    parser.add_argument("--approval-id", required=True)
    parser.add_argument("--execution-id", required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", type=Path, default=default_state_dir())
    parser.add_argument("--cron-config", type=Path, default=default_cron_config())
    parser.add_argument("--dry-run-cron", action="store_true")
    parser.add_argument("--test-mode", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init")
    init.add_argument("--latest-order-id")
    init.add_argument("--latest-execution-id")
    init.add_argument("--latest-result")
    init.add_argument("--latest-order-sha256")

    activate = subparsers.add_parser("activate")
    binding_arguments(activate)
    activate.add_argument("--supersedes", required=True)
    activate.add_argument("--coordinator", default="Puppet Master")
    activate.add_argument("--executor", default="Sentinel")
    activate.add_argument("--critical", action="store_true")
    activate.add_argument(
        "--lease-ttl-seconds",
        type=int,
        default=DEFAULT_LEASE_TTL_SECONDS,
    )

    ack = subparsers.add_parser("ack")
    binding_arguments(ack)
    ack.add_argument("--executor", default="Sentinel")

    start = subparsers.add_parser("start")
    binding_arguments(start)

    assertion = subparsers.add_parser("assert")
    binding_arguments(assertion)

    renew = subparsers.add_parser("renew")
    binding_arguments(renew)
    renew.add_argument(
        "--lease-ttl-seconds",
        type=int,
        default=DEFAULT_LEASE_TTL_SECONDS,
    )

    subparsers.add_parser("recover")

    stop = subparsers.add_parser("stop")
    stop.add_argument(
        "--requested-by",
        required=True,
        choices=["Hebert", "PuppetMaster"],
    )
    stop.add_argument("--reason", required=True)

    close = subparsers.add_parser("close")
    close.add_argument("--order-id", required=True)
    close.add_argument("--execution-id", required=True)
    close.add_argument("--result", required=True)

    subparsers.add_parser("status")
    return parser


def runtime_paths_and_runner(
    args: argparse.Namespace,
) -> tuple[Path, Path, tuple[str, ...]]:
    state_dir = args.state_dir.expanduser().resolve()
    cron_config = args.cron_config.expanduser().resolve()
    override_names = (
        "SENTINEL_ORCHESTRATION_STATE_DIR",
        "SENTINEL_ORCHESTRATION_CRON_CONFIG",
        "SENTINEL_ORCHESTRATION_CRON_RUNNER",
    )
    if args.test_mode:
        temporary_root = Path(tempfile.gettempdir()).resolve()
        if not is_under(state_dir, temporary_root):
            raise GateError("test-mode exige state-dir sob diretório temporário")
        if not is_under(cron_config, temporary_root):
            raise GateError("test-mode exige cron-config sob diretório temporário")
        runner_raw = os.environ.get("SENTINEL_ORCHESTRATION_CRON_RUNNER", "")
        runner = tuple(shlex.split(runner_raw))
        if not runner or runner == PRODUCTION_CRON_RUNNER:
            raise GateError("test-mode exige runner de cron double explícito")
        if not any(
            is_under(Path(item).expanduser().resolve(), temporary_root)
            for item in runner
            if "/" in item
        ):
            raise GateError("runner de teste deve referenciar artefato temporário")
        return state_dir, cron_config, runner

    configured_overrides = [name for name in override_names if os.environ.get(name)]
    if configured_overrides:
        raise GateError(
            "override de produção proibido: " + ", ".join(configured_overrides)
        )
    if state_dir != CANONICAL_STATE_DIR:
        raise GateError("state-dir de produção deve ser o canônico")
    if cron_config != CANONICAL_CRON_CONFIG:
        raise GateError("cron-config de produção deve ser o canônico")
    if args.dry_run_cron:
        raise GateError("dry-run-cron proibido em produção")
    return state_dir, cron_config, PRODUCTION_CRON_RUNNER


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        state_dir, cron_config, cron_runner = runtime_paths_and_runner(args)
        controller = Controller(
            state_dir,
            cron_config,
            cron_runner=cron_runner,
            dry_run_cron=args.dry_run_cron,
            test_mode=args.test_mode,
        )
        if args.command == "init":
            result = controller.init(
                args.latest_order_id,
                args.latest_execution_id,
                args.latest_result,
                args.latest_order_sha256,
            )
        elif args.command == "activate":
            result = controller.activate(args)
        elif args.command == "ack":
            result = controller.ack(args)
        elif args.command == "start":
            result = controller.start(args)
        elif args.command == "assert":
            result = controller.assert_binding(args)
        elif args.command == "renew":
            result = controller.renew(args)
        elif args.command == "recover":
            result = controller.recover()
        elif args.command == "stop":
            result = controller.stop(args)
        elif args.command == "close":
            result = controller.close(args)
        elif args.command == "status":
            result = controller.status()
        else:
            parser.error("comando desconhecido")
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (GateError, OSError, subprocess.SubprocessError) as exc:
        print(
            json.dumps(
                {"allowed": False, "error": str(exc), "command": args.command},
                ensure_ascii=False,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Auditoria local append-only para acessos autorizados do Sentinel."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


ACTOR = "Sentinel"
WORKSPACE = Path(__file__).resolve().parents[1]
AUDIT_PATH = WORKSPACE / "logs" / "access-audit.jsonl"

ALLOWED_OPERATIONS = {
    "ninjaone": {
        "probe",
        "organizations",
        "organizations-detailed",
        "devices",
        "devices-detailed",
        "alerts",
        "activities",
        "policies",
        "blocked_cli",
    },
    "arx-cove": {"probe", "status", "blocked_cli"},
    "bitdefender": {
        "probe",
        "companies",
        "endpoints",
        "quarantine",
        "incidents",
        "blocked_cli",
    },
    "operational-context": {
        "summary",
        "clients",
        "client",
        "severity",
        "blocked_cli",
    },
    "operational-logs": {
        "sources",
        "health",
        "tail_arx",
        "tail_bitdefender",
        "blocked_cli",
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_secret_file(path: Path) -> None:
    if not path.exists() or not path.is_file() or path.is_symlink():
        raise RuntimeError("arquivo de credencial ausente ou inseguro")
    metadata = path.stat()
    if metadata.st_uid != os.geteuid():
        raise RuntimeError("arquivo de credencial com proprietario inesperado")
    if stat.S_IMODE(metadata.st_mode) != 0o600:
        raise RuntimeError("arquivo de credencial deve usar permissao 600")


def append_event(
    *,
    source: str,
    operation: str,
    result: str,
    correlation: str,
    client_path: Path,
) -> None:
    if source not in ALLOWED_OPERATIONS:
        raise RuntimeError("fonte de auditoria nao permitida")
    if operation not in ALLOWED_OPERATIONS[source]:
        raise RuntimeError("operacao de auditoria nao permitida")
    if result not in {"success", "failure"}:
        raise RuntimeError("resultado de auditoria invalido")
    if not correlation or len(correlation) > 64 or not correlation.isalnum():
        raise RuntimeError("correlacao de auditoria invalida")

    event = {
        "actor": ACTOR,
        "source": source,
        "operation": operation,
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "result": result,
        "correlation": correlation,
        "client_sha256": sha256_file(client_path),
    }
    encoded = (json.dumps(event, ensure_ascii=True, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(AUDIT_PATH, flags, 0o600)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise RuntimeError("destino de auditoria nao e arquivo regular")
        if metadata.st_uid != os.geteuid():
            raise RuntimeError("arquivo de auditoria com proprietario inesperado")
        if stat.S_IMODE(metadata.st_mode) != 0o600:
            raise RuntimeError("arquivo de auditoria deve usar permissao 600")
        written = os.write(descriptor, encoded)
        if written != len(encoded):
            raise RuntimeError("registro de auditoria incompleto")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


@contextmanager
def audited_access(
    *, source: str, operation: str, client_path: Path
) -> Iterator[str]:
    correlation = uuid.uuid4().hex
    try:
        yield correlation
    except BaseException:
        append_event(
            source=source,
            operation=operation,
            result="failure",
            correlation=correlation,
            client_path=client_path,
        )
        raise
    else:
        append_event(
            source=source,
            operation=operation,
            result="success",
            correlation=correlation,
            client_path=client_path,
        )

#!/usr/bin/env python3
from __future__ import annotations
import contextlib, fcntl, hashlib, json, os, re
from datetime import datetime, timezone
from pathlib import Path

ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
TRANSITIONS = {
    "intake": {"brief-pending", "cancelled"},
    "brief-pending": {"brief-approved", "blocked", "cancelled"},
    "brief-approved": {"research-pending", "strategy-pending", "cancelled"},
    "research-pending": {"research-ready", "blocked", "failed", "cancelled"},
    "research-ready": {"strategy-pending", "cancelled"},
    "strategy-pending": {"strategy-approved", "blocked", "cancelled"},
    "strategy-approved": {"creative-pending", "cancelled"},
    "creative-pending": {"creative-approved", "blocked", "cancelled"},
    "creative-approved": {"generation-authorization-pending", "cancelled"},
    "generation-authorization-pending": {"generation-submitted", "blocked", "cancelled"},
    "generation-submitted": {"generation-ready", "blocked", "failed", "cancelled"},
    "generation-ready": {"asset-selected", "blocked", "failed", "cancelled"},
    "asset-selected": {"composition-pending", "cancelled"},
    "composition-pending": {"composition-ready", "blocked", "failed", "cancelled"},
    "composition-ready": {"qa-pending", "cancelled"},
    "qa-pending": {"qa-failed", "final-approval-pending", "blocked", "cancelled"},
    "qa-failed": {"composition-pending", "cancelled"},
    "final-approval-pending": {"final-approved", "blocked", "cancelled"},
    "final-approved": {"draft-authorization-pending", "measurement-pending", "archived"},
    "draft-authorization-pending": {"draft-created", "blocked", "cancelled"},
    "draft-created": {"schedule-authorization-pending", "publish-authorization-pending", "archived"},
    "schedule-authorization-pending": {"scheduled", "blocked", "cancelled"},
    "scheduled": {"publish-authorization-pending", "cancelled"},
    "publish-authorization-pending": {"published", "blocked", "cancelled"},
    "published": {"measurement-pending", "archived"},
    "measurement-pending": {"measured", "blocked"},
    "measured": {"archived"},
    "blocked": {"brief-pending", "research-pending", "strategy-pending", "creative-pending",
                "generation-authorization-pending", "generation-submitted", "composition-pending",
                "qa-pending", "final-approval-pending", "draft-authorization-pending",
                "schedule-authorization-pending", "publish-authorization-pending", "cancelled"},
    "failed": {"blocked", "cancelled", "archived"},
    "cancelled": {"archived"},
    "archived": set(),
}

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)

def require_id(value: str, label: str = "id") -> str:
    if not ID_RE.fullmatch(value or ""):
        raise ValueError(f"{label} inválido")
    return value

def canonical_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_json(obj) -> str:
    return sha256_bytes(canonical_bytes(obj))

def request_hash(request: dict) -> str:
    clean = {k: v for k, v in request.items() if k not in {"request_hash", "approval"}}
    return sha256_json(clean)

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} precisa conter objeto JSON")
    return data

def atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_bytes(data) + b"\n"
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, raw)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, path)
    dfd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)

def append_jsonl(path: Path, event: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_bytes(event) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(fd, raw)
        os.fsync(fd)
    finally:
        os.close(fd)

@contextlib.contextmanager
def exclusive_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)

def safe_name(value: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(".-")
    if not name or len(name) > 128:
        raise ValueError("nome de arquivo inválido")
    return name

def make_event(state: dict, action: str, actor: str, result: str,
               before_hash: str | None, after_hash: str | None,
               detail: dict | None = None) -> dict:
    return {
        "event_id": hashlib.sha256(os.urandom(32)).hexdigest(),
        "correlation_id": state["correlation_id"],
        "campaign_id": state["campaign_id"],
        "asset_id": state["asset_id"],
        "event_version": state["event_version"],
        "timestamp_utc": utc_now(),
        "actor": actor,
        "action": action,
        "result": result,
        "before_hash": before_hash,
        "after_hash": after_hash,
        "detail": detail or {},
    }

def validate_approval(request: dict, approval: dict) -> None:
    digest = request_hash(request)
    if approval.get("request_hash") != digest:
        raise ValueError("aprovação não corresponde ao request_hash")
    for key in ("campaign_id", "asset_id", "operation"):
        if approval.get(key) != request.get(key):
            raise ValueError(f"aprovação diverge em {key}")
    if approval.get("used_at") is not None:
        raise ValueError("aprovação já utilizada")
    if parse_utc(approval["expires_at"]) <= datetime.now(timezone.utc):
        raise ValueError("aprovação expirada")

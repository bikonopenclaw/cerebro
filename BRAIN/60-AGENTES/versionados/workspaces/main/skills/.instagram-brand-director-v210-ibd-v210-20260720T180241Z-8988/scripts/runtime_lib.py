#!/usr/bin/env python3
from __future__ import annotations
import contextlib, fcntl, hashlib, json, os, re
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None

ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
HASH_RE = re.compile(r"^[a-f0-9]{64}$")
OWNER_ROLE = "proprietário"
APPROVAL_OUTCOMES = {"succeeded", "failed", "indeterminate"}
TRANSITIONS = {
    "intake": {"brief-pending", "cancelled"},
    "brief-pending": {"brief-approved", "blocked", "cancelled"},
    "brief-approved": {"brand-context-pending", "research-pending", "cancelled"},
    "brand-context-pending": {"brand-locked", "blocked", "cancelled"},
    "brand-locked": {"research-pending", "strategy-pending", "cancelled"},
    "research-pending": {"strategy-pending", "blocked", "failed", "cancelled"},
    "strategy-pending": {"strategy-approved", "blocked", "cancelled"},
    "strategy-approved": {"creative-approved", "blocked", "cancelled"},
    "creative-approved": {"generation-approval-pending", "composition-pending", "cancelled"},
    "generation-approval-pending": {"generation-submitted", "blocked", "cancelled"},
    "generation-submitted": {"generated", "blocked", "failed", "cancelled"},
    "generated": {"asset-selected", "blocked", "failed", "cancelled"},
    "asset-selected": {"composition-pending", "cancelled"},
    "composition-pending": {"qa-pending", "blocked", "failed", "cancelled"},
    "qa-pending": {"brand-qa-pending", "blocked", "cancelled"},
    "brand-qa-pending": {"release-candidate", "blocked", "cancelled"},
    "release-candidate": {"owner-approval-pending", "archived"},
    "owner-approval-pending": {"external-action-approved", "blocked", "cancelled"},
    "external-action-approved": {"external-action-running", "blocked", "cancelled"},
    "external-action-running": {"published", "blocked", "failed"},
    "published": {"measured", "archived"},
    "measured": {"archived"},
    "blocked": {"brief-pending", "brand-context-pending", "research-pending", "strategy-pending",
                "generation-approval-pending", "composition-pending", "qa-pending",
                "brand-qa-pending", "owner-approval-pending", "cancelled"},
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
    clean = {k: v for k, v in request.items()
             if k not in {"request_hash", "payload_hash", "approval", "governance_decision"}}
    return sha256_json(clean)

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} precisa conter objeto JSON")
    return data

def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise ValueError("PyYAML ausente")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} precisa conter mapa YAML")
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

def _event_digest(event: dict) -> str:
    return sha256_json({k: v for k, v in event.items() if k != "event_hash"})

def read_event_stream(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except Exception as exc:
            raise ValueError(f"evento JSON inválido na linha {number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"evento inválido na linha {number}")
        events.append(value)
    return events

def verify_event_stream(path: Path) -> dict:
    events = read_event_stream(path)
    previous = ""
    for index, event in enumerate(events, 1):
        if event.get("stream_version") != index:
            raise ValueError(f"stream_version inválida no evento {index}")
        if event.get("prev_event_hash", "") != previous:
            raise ValueError(f"prev_event_hash inválido no evento {index}")
        digest = _event_digest(event)
        if event.get("event_hash") != digest:
            raise ValueError(f"event_hash inválido no evento {index}")
        previous = digest
    return {"valid": True, "events": len(events), "head_hash": previous}

def append_event(path: Path, event: dict) -> dict:
    lock = path.with_name(path.name + ".lock")
    with exclusive_lock(lock):
        verified = verify_event_stream(path)
        enriched = dict(event)
        enriched.setdefault("event_id", hashlib.sha256(os.urandom(32)).hexdigest())
        enriched.setdefault("event_type", str(enriched.get("action", "event")))
        enriched.setdefault("timestamp_utc", utc_now())
        enriched["stream_version"] = verified["events"] + 1
        enriched["prev_event_hash"] = verified["head_hash"]
        enriched["event_hash"] = _event_digest(enriched)
        append_jsonl(path, enriched)
        return enriched

def make_event(state: dict, action: str, actor: str, result: str,
               before_hash: str | None, after_hash: str | None,
               detail: dict | None = None) -> dict:
    return {
        "event_id": hashlib.sha256(os.urandom(32)).hexdigest(),
        "event_type": action,
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

def owner_binding(governance: dict) -> dict:
    owner = governance.get("owner")
    if not isinstance(owner, dict):
        raise ValueError("owner ausente na governança")
    required = ("id", "channel", "chat_id")
    if owner.get("role") != OWNER_ROLE or any(not str(owner.get(k, "")).strip() for k in required):
        raise ValueError("identidade do proprietário não configurada")
    return owner

def validate_owner_event(event: dict, governance: dict) -> None:
    owner = owner_binding(governance)
    if event.get("authority") != "openclaw.inbound_meta.v2":
        raise ValueError("evento sem autoridade confiável")
    if str(event.get("sender_id")) != str(owner["id"]):
        raise ValueError("sender_id não corresponde ao proprietário")
    if event.get("channel") != owner["channel"] or str(event.get("chat_id")) != str(owner["chat_id"]):
        raise ValueError("canal ou chat não corresponde ao proprietário")
    if not str(event.get("message_id", "")).strip() or not str(event.get("text", "")).strip():
        raise ValueError("evento do proprietário incompleto")
    parse_utc(str(event.get("timestamp_utc", "")))

def validate_approval(request: dict, approval: dict, governance: dict,
                      now: datetime | None = None) -> None:
    if governance.get("external_action_lock") is not True:
        raise ValueError("lock externo precisa iniciar ativo")
    owner = owner_binding(governance)
    digest = request_hash(request)
    if approval.get("status") != "approved":
        raise ValueError("aprovação não está aprovada")
    if approval.get("payload_hash") != digest:
        raise ValueError("aprovação não corresponde ao payload_hash")
    mappings = {
        "campaign_id": "campaign_id",
        "asset_id": "asset_id",
        "asset_version": "asset_version",
        "action": "operation",
        "destination": "destination",
    }
    for approval_key, request_key in mappings.items():
        if approval.get(approval_key) != request.get(request_key):
            raise ValueError(f"aprovação diverge em {approval_key}")
    for key in ("provider_kind", "provider_id"):
        if key in request and approval.get(key) != request.get(key):
            raise ValueError(f"aprovação diverge em {key}")
    if approval.get("approved_by_role") != OWNER_ROLE:
        raise ValueError("aprovação não pertence ao proprietário")
    if str(approval.get("approved_by_id")) != str(owner["id"]):
        raise ValueError("approved_by_id inválido")
    if approval.get("approved_channel") != owner["channel"] or str(approval.get("approved_chat_id")) != str(owner["chat_id"]):
        raise ValueError("origem da aprovação inválida")
    if not str(approval.get("approved_by_reference", "")).strip():
        raise ValueError("message_id da aprovação ausente")
    if not HASH_RE.fullmatch(str(approval.get("owner_message_hash", ""))):
        raise ValueError("hash da mensagem do proprietário inválido")
    if approval.get("revoked_at") is not None:
        raise ValueError("aprovação revogada")
    if approval.get("consumed_at") is not None:
        raise ValueError("aprovação já consumida")
    current = now or datetime.now(timezone.utc)
    expires = approval.get("expires_at")
    if expires and parse_utc(expires) <= current:
        raise ValueError("aprovação expirada")

def consume_approval(path: Path, request: dict, governance: dict) -> dict:
    lock = path.with_name(path.name + ".lock")
    with exclusive_lock(lock):
        approval = load_json(path)
        validate_approval(request, approval, governance)
        approval["consumed_at"] = utc_now()
        approval["status"] = "consumed"
        atomic_write_json(path, approval)
        return approval

def reserve_approval(path: Path, request: dict, governance: dict, execution_id: str) -> dict:
    require_id(execution_id, "execution_id")
    lock = path.with_name(path.name + ".lock")
    with exclusive_lock(lock):
        approval = load_json(path)
        validate_approval(request, approval, governance)
        approval["status"] = "reserved"
        approval["reserved_at"] = utc_now()
        approval["execution_id"] = execution_id
        atomic_write_json(path, approval)
        return approval

def start_approval_execution(path: Path, execution_id: str) -> dict:
    require_id(execution_id, "execution_id")
    lock = path.with_name(path.name + ".lock")
    with exclusive_lock(lock):
        approval = load_json(path)
        if approval.get("status") != "reserved" or approval.get("execution_id") != execution_id:
            raise ValueError("approval não reservado para esta execução")
        approval["status"] = "executing"
        approval["execution_started_at"] = utc_now()
        atomic_write_json(path, approval)
        return approval

def finish_approval_execution(path: Path, execution_id: str, outcome: str,
                              result_event_id: str) -> dict:
    require_id(execution_id, "execution_id")
    if outcome not in APPROVAL_OUTCOMES:
        raise ValueError("outcome inválido")
    if not str(result_event_id).strip():
        raise ValueError("result_event_id obrigatório")
    lock = path.with_name(path.name + ".lock")
    with exclusive_lock(lock):
        approval = load_json(path)
        if approval.get("status") != "executing" or approval.get("execution_id") != execution_id:
            raise ValueError("approval não está executando nesta execução")
        now = utc_now()
        approval["status"] = outcome
        approval["outcome"] = outcome
        approval["completed_at"] = now
        approval["consumed_at"] = now
        approval["result_event_id"] = result_event_id
        atomic_write_json(path, approval)
        return approval

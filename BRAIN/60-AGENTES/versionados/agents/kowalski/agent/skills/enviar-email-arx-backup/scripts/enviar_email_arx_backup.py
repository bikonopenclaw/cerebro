#!/usr/bin/env python3
"""Envia e-mail de relatório ARX Backup a partir de job JSON aprovado."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import smtplib
import ssl
import sys
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from typing import Any

ARX_ROOT = Path("/data/.openclaw/workspace-kowalski/arx-backup")
DEFAULT_ENV = ARX_ROOT / "config" / ".env"
DEFAULT_LOG = ARX_ROOT / "jobs" / "envios.log.jsonl"


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def env_first(*names: str, default: str | None = None) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


def require(value: Any, message: str) -> Any:
    if value is None or value == "" or value == []:
        raise ValueError(message)
    return value


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError("Campo de destinatários/anexos precisa ser string ou lista de strings")


def unique_list(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        key = value.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(value.strip())
    return result


def resolve_attachment(path_text: str) -> Path:
    path = Path(path_text)
    if not path.is_absolute():
        candidates = [
            ARX_ROOT / path,
            ARX_ROOT / "relatorios" / "por-cliente" / path,
            ARX_ROOT / "relatorios" / path,
        ]
        for candidate in candidates:
            if candidate.exists():
                path = candidate
                break
    path = path.resolve()
    arx_resolved = ARX_ROOT.resolve()
    if arx_resolved not in [path, *path.parents]:
        raise ValueError(f"Anexo fora do workspace ARX Backup: {path}")
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Anexo não encontrado: {path}")
    return path


def validate_monthly_approved_model(subject: str, attachments: list[Path]) -> None:
    if not subject.lower().startswith("relatório mensal arx backup"):
        return
    marker = 'ARX_APPROVED_MODEL:modelo-padrao-relatorio-mensal-arx-backup'
    missing = []
    for attachment in attachments:
        if attachment.suffix.lower() != ".pdf":
            continue
        html = attachment.with_suffix(".html")
        if not html.exists() or marker not in html.read_text(encoding="utf-8", errors="ignore"):
            missing.append(attachment.name)
    if missing:
        raise ValueError(
            "Envio bloqueado: relatório mensal ARX Backup sem marcador do modelo aprovado: "
            + ", ".join(missing)
        )


def read_job(path: Path) -> dict[str, Any]:
    if path.suffix.lower() != ".json":
        raise ValueError("Use job em JSON. Rascunhos .md devem ser convertidos para job antes do envio.")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Job precisa ser um objeto JSON")
    return data


def validate_job(job: dict[str, Any], *, sending: bool) -> dict[str, Any]:
    status = require(job.get("status"), "Campo status é obrigatório")
    if sending and status != "aprovado":
        raise ValueError(f"Envio bloqueado. Status atual: {status}. Use status 'aprovado'.")

    cliente = require(job.get("cliente"), "Campo cliente é obrigatório")
    to = as_list(require(job.get("destinatarios"), "Campo destinatarios é obrigatório"))
    cc = as_list(job.get("cc"))
    bcc = unique_list(as_list(job.get("bcc")) + as_list(env_first("ARX_SMTP_BCC", "SMTP_BCC")))
    subject = require(job.get("assunto"), "Campo assunto é obrigatório")
    body = require(job.get("corpo"), "Campo corpo é obrigatório")
    attachments = [resolve_attachment(item) for item in as_list(job.get("anexos"))]
    allow_without_attachment = bool(job.get("permitir_sem_anexo"))
    if sending and not attachments and not allow_without_attachment:
        raise ValueError("Envio real sem anexo bloqueado. Informe anexos ou use permitir_sem_anexo=true para teste aprovado.")
    if sending:
        validate_monthly_approved_model(str(subject), attachments)

    return {
        "status": status,
        "cliente": cliente,
        "to": to,
        "cc": cc,
        "bcc": bcc,
        "subject": subject,
        "body": body,
        "attachments": attachments,
        "reply_to": job.get("reply_to"),
    }


def smtp_config() -> dict[str, Any]:
    host = require(env_first("ARX_SMTP_HOST", "SMTP_HOST"), "SMTP host não configurado")
    port = int(env_first("ARX_SMTP_PORT", "SMTP_PORT", default="587") or "587")
    user = require(env_first("ARX_SMTP_USER", "SMTP_USER"), "SMTP user não configurado")
    password = require(env_first("ARX_SMTP_PASSWORD", "SMTP_PASSWORD"), "SMTP password não configurado")
    from_email = require(env_first("ARX_SMTP_FROM", "SMTP_FROM"), "SMTP from não configurado")
    from_name = env_first("ARX_SMTP_FROM_NAME", "SMTP_FROM_NAME", default="ARX Backup") or "ARX Backup"
    tls_value = (env_first("ARX_SMTP_TLS", "SMTP_TLS", default="true") or "true").lower()
    use_tls = tls_value not in {"0", "false", "no", "nao"}
    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "from_email": from_email,
        "from_name": from_name,
        "use_tls": use_tls,
    }


def build_message(valid: dict[str, Any], config: dict[str, Any]) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = formataddr((config["from_name"], config["from_email"]))
    msg["To"] = ", ".join(valid["to"])
    if valid["cc"]:
        msg["Cc"] = ", ".join(valid["cc"])
    if valid["reply_to"]:
        msg["Reply-To"] = str(valid["reply_to"])
    msg["Subject"] = str(valid["subject"])
    msg.set_content(str(valid["body"]))

    for attachment in valid["attachments"]:
        ctype, encoding = mimetypes.guess_type(str(attachment))
        if ctype is None or encoding is not None:
            maintype, subtype = "application", "octet-stream"
        else:
            maintype, subtype = ctype.split("/", 1)
        msg.add_attachment(
            attachment.read_bytes(),
            maintype=maintype,
            subtype=subtype,
            filename=attachment.name,
        )
    return msg


def append_log(job_path: Path, status: str, detail: dict[str, Any]) -> None:
    DEFAULT_LOG.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "job": str(job_path),
        "status": status,
        **detail,
    }
    with DEFAULT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def mark_job_sent(job_path: Path, job: dict[str, Any]) -> None:
    job["status"] = "enviado"
    job["enviado_em"] = datetime.now(timezone.utc).isoformat()
    job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def send(msg: EmailMessage, valid: dict[str, Any], config: dict[str, Any]) -> None:
    recipients = valid["to"] + valid["cc"] + valid["bcc"]
    context = ssl.create_default_context()
    with smtplib.SMTP(config["host"], config["port"], timeout=45) as smtp:
        if config["use_tls"]:
            smtp.starttls(context=context)
        smtp.login(config["user"], config["password"])
        smtp.send_message(msg, from_addr=config["from_email"], to_addrs=recipients)


def main() -> int:
    parser = argparse.ArgumentParser(description="Enviar e-mail ARX Backup por job JSON aprovado")
    parser.add_argument("--job", required=True, help="Caminho do job JSON")
    parser.add_argument("--env", default=str(DEFAULT_ENV), help="Arquivo .env com SMTP")
    parser.add_argument("--dry-run", action="store_true", help="Valida e mostra resumo sem enviar")
    parser.add_argument("--mark-sent", action="store_true", help="Marca job como enviado após sucesso")
    args = parser.parse_args()

    job_path = Path(args.job).resolve()
    try:
        load_env(Path(args.env))
        job = read_job(job_path)
        valid = validate_job(job, sending=not args.dry_run)

        summary = {
            "cliente": valid["cliente"],
            "status": valid["status"],
            "to": valid["to"],
            "cc": valid["cc"],
            "bcc_count": len(valid["bcc"]),
            "subject": valid["subject"],
            "attachments": [str(path) for path in valid["attachments"]],
        }

        if args.dry_run:
            append_log(job_path, "dry-run-ok", summary)
            print(json.dumps({"ok": True, "dry_run": True, **summary}, ensure_ascii=False, indent=2))
            return 0

        config = smtp_config()
        msg = build_message(valid, config)
        send(msg, valid, config)
        if args.mark_sent:
            mark_job_sent(job_path, job)
        append_log(job_path, "enviado", summary)
        print(json.dumps({"ok": True, "enviado": True, **summary}, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        append_log(job_path, "erro", {"erro": str(exc)})
        print(json.dumps({"ok": False, "erro": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

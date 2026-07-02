#!/usr/bin/env python3
"""Broker local para autenticação SERPRO com certificado A1.

Rode somente no Mac/host onde o certificado A1 está salvo.
O certificado não sai da máquina. A senha é pedida no terminal e fica só em memória.
Expõe endpoints locais em 127.0.0.1 para obter token temporário.
"""
from __future__ import annotations

import base64
import getpass
import json
import os
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8766
AUTH_URL = "https://autenticacao.sapi.serpro.gov.br/authenticate"


def load_env_file(path: Path) -> None:
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


class BrokerState:
    def __init__(self) -> None:
        load_env_file(Path(".serpro-broker.env"))
        self.consumer_key = os.getenv("SERPRO_CONSUMER_KEY", "").strip()
        self.consumer_secret = os.getenv("SERPRO_CONSUMER_SECRET", "").strip()
        self.cert_path = os.getenv("SERPRO_CERT_PATH", "").strip()
        self.role_type = os.getenv("SERPRO_ROLE_TYPE", "TERCEIROS").strip() or "TERCEIROS"
        self.local_api_key = os.getenv("BROKER_LOCAL_API_KEY", "").strip()
        self.cache_seconds = int(os.getenv("BROKER_CACHE_SECONDS", "300"))
        self.cert_password = ""
        self.cached_token: dict | None = None
        self.cached_at = 0.0

    def validate_startup(self) -> None:
        missing = [
            name for name, value in [
                ("SERPRO_CONSUMER_KEY", self.consumer_key),
                ("SERPRO_CONSUMER_SECRET", self.consumer_secret),
                ("SERPRO_CERT_PATH", self.cert_path),
            ] if not value
        ]
        if missing:
            raise SystemExit("Variáveis ausentes em .serpro-broker.env: " + ", ".join(missing))
        cert = Path(self.cert_path).expanduser()
        if not cert.exists():
            raise SystemExit(f"Certificado não encontrado: {cert}")
        self.cert_path = str(cert)
        self.cert_password = getpass.getpass("Senha do certificado A1, não será salva: ")
        if not self.cert_password:
            raise SystemExit("Senha vazia. Abortando.")

    def token_valid(self) -> bool:
        if not self.cached_token:
            return False
        return (time.time() - self.cached_at) < self.cache_seconds

    def get_token(self, force: bool = False) -> dict:
        if not force and self.token_valid():
            data = dict(self.cached_token or {})
            data["broker_cache"] = True
            return data

        basic = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        cmd = [
            "curl", "-sS", "-X", "POST",
            "-H", f"Authorization: Basic {basic}",
            "-H", f"Role-Type: {self.role_type}",
            "-H", "Content-Type: application/x-www-form-urlencoded",
            "-d", "grant_type=client_credentials",
            "--cert-type", "P12",
            "--cert", f"{self.cert_path}:{self.cert_password}",
            AUTH_URL,
        ]
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=60)
        if proc.returncode != 0:
            raise RuntimeError(f"curl falhou: {proc.stderr.strip() or proc.stdout.strip()}")
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"SERPRO retornou resposta não JSON: {proc.stdout[:500]}") from exc
        if "access_token" not in data and "jwt_token" not in data:
            raise RuntimeError("Resposta SERPRO sem access_token/jwt_token: " + json.dumps(data, ensure_ascii=False)[:700])
        self.cached_token = data
        self.cached_at = time.time()
        out = dict(data)
        out["broker_cache"] = False
        return out


STATE = BrokerState()


class Handler(BaseHTTPRequestHandler):
    server_version = "SerproLocalBroker/0.1"

    def log_message(self, fmt: str, *args) -> None:
        # Não loga path com query nem tokens.
        sys.stderr.write("broker: " + fmt % args + "\n")

    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self) -> bool:
        if self.client_address[0] not in {"127.0.0.1", "::1"}:
            return False
        if not STATE.local_api_key:
            return True
        return self.headers.get("X-Broker-Key", "") == STATE.local_api_key

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._json(200, {"ok": True, "service": "serpro-local-cert-broker", "bind": "127.0.0.1"})
            return
        if parsed.path == "/token":
            if not self._authorized():
                self._json(403, {"ok": False, "error": "forbidden"})
                return
            try:
                token = STATE.get_token(force=False)
                self._json(200, {"ok": True, "token": token})
            except Exception as exc:
                self._json(500, {"ok": False, "error": str(exc)})
            return
        self._json(404, {"ok": False, "error": "not_found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/token/refresh":
            if not self._authorized():
                self._json(403, {"ok": False, "error": "forbidden"})
                return
            try:
                token = STATE.get_token(force=True)
                self._json(200, {"ok": True, "token": token})
            except Exception as exc:
                self._json(500, {"ok": False, "error": str(exc)})
            return
        self._json(404, {"ok": False, "error": "not_found"})


def main() -> int:
    STATE.validate_startup()
    host = os.getenv("BROKER_HOST", DEFAULT_HOST)
    port = int(os.getenv("BROKER_PORT", str(DEFAULT_PORT)))
    if host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Por segurança, BROKER_HOST deve ser 127.0.0.1/localhost.")
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"SERPRO local broker rodando em http://127.0.0.1:{port}")
    print("Certificado carregado localmente. Senha não foi salva. Ctrl+C para parar.")
    httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

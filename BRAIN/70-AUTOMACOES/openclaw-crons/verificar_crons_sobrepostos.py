#!/usr/bin/env python3
"""
Verificador de segurança para crons OpenClaw.

Objetivo:
- Evitar agendamentos sobrepostos ou muito próximos.
- Reduzir risco de consumo massivo de tokens por múltiplos agentTurn simultâneos.
- Servir como preflight antes de criar/alterar cron operacional.

Uso:
  python3 scripts/verificar_crons_sobrepostos.py
  python3 scripts/verificar_crons_sobrepostos.py --json
  python3 scripts/verificar_crons_sobrepostos.py --candidate-name "Novo relatório" --candidate-expr "0 8 * * 2-5" --candidate-tz America/Sao_Paulo

Exit codes:
  0 = sem conflito bloqueante
  1 = conflito bloqueante encontrado
  2 = erro de entrada/leitura
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

DEFAULT_JOBS = Path("/data/.openclaw/cron/jobs.json")
DEFAULT_WINDOW_DAYS = 35
DEFAULT_MIN_GAP_MINUTES = 5
HEAVY_GAP_MINUTES = 15

# Jobs com esses termos no nome costumam acionar modelo/API externa. Se colarem,
# o risco de token/rate-limit sobe.
HEAVY_NAME_MARKERS = (
    "coleta",
    "envio",
    "resumo",
    "fechamento",
    "relatório",
    "relatorio",
    "tickets",
    "backup",
    "bitdefender",
    "ninjaone",
    "whatsapp",
    "brain",
)


@dataclass(frozen=True)
class Job:
    id: str
    name: str
    enabled: bool
    expr: str
    tz: str
    kind: str
    delivery_mode: str
    payload_kind: str
    agent_id: str

    @property
    def cache_sender(self) -> bool:
        n = self.name.lower()
        # Envios dos relatórios operacionais foram desenhados para serem leves:
        # leem um .txt já cacheado e só entregam no Telegram, com intervalo de 1 minuto.
        return n.startswith("envio diário") or n.startswith("envio semanal")

    @property
    def heavy(self) -> bool:
        n = self.name.lower()
        if self.cache_sender:
            return False
        return (
            self.payload_kind == "agentTurn"
            or self.delivery_mode == "announce"
            or any(marker in n for marker in HEAVY_NAME_MARKERS)
        )


@dataclass
class Finding:
    severity: str
    kind: str
    when: str
    gap_minutes: int
    job_a_id: str
    job_a_name: str
    job_a_expr: str
    job_b_id: str
    job_b_name: str
    job_b_expr: str
    message: str


def parse_field(field: str, min_value: int, max_value: int) -> set[int]:
    values: set[int] = set()
    field = field.strip()
    if field == "*":
        return set(range(min_value, max_value + 1))
    for part in field.split(","):
        part = part.strip()
        if not part:
            raise ValueError(f"campo vazio em {field!r}")
        step = 1
        if "/" in part:
            part, step_s = part.split("/", 1)
            step = int(step_s)
            if step <= 0:
                raise ValueError(f"step inválido em {field!r}")
        if part == "*":
            start, end = min_value, max_value
        elif "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
        else:
            start = end = int(part)
        if start < min_value or end > max_value or start > end:
            raise ValueError(f"valor fora do intervalo em {field!r}")
        values.update(range(start, end + 1, step))
    return values


def cron_matches(dt: datetime, expr: str) -> bool:
    parts = expr.split()
    if len(parts) != 5:
        raise ValueError(f"expressão cron precisa ter 5 campos: {expr!r}")

    minute_s, hour_s, dom_s, month_s, dow_s = parts
    minutes = parse_field(minute_s, 0, 59)
    hours = parse_field(hour_s, 0, 23)
    dom = parse_field(dom_s, 1, 31)
    months = parse_field(month_s, 1, 12)
    dow = parse_field(dow_s, 0, 7)

    cron_dow = (dt.weekday() + 1) % 7  # Python: segunda=0. Cron: domingo=0/7.
    dow_match = cron_dow in dow or (cron_dow == 0 and 7 in dow)

    if dt.minute not in minutes or dt.hour not in hours or dt.month not in months:
        return False

    dom_is_any = dom_s == "*"
    dow_is_any = dow_s == "*"

    # Cron padrão/Vixie: se DOM e DOW forem específicos, é OR.
    if dom_is_any and dow_is_any:
        day_match = True
    elif dom_is_any:
        day_match = dow_match
    elif dow_is_any:
        day_match = dt.day in dom
    else:
        day_match = (dt.day in dom) or dow_match

    return day_match


def next_runs(job: Job, start_utc: datetime, days: int) -> list[datetime]:
    tz = ZoneInfo(job.tz)
    start_local = start_utc.astimezone(tz).replace(second=0, microsecond=0)
    end_local = start_local + timedelta(days=days)
    out: list[datetime] = []
    cur = start_local
    while cur <= end_local:
        if cron_matches(cur, job.expr):
            out.append(cur.astimezone(timezone.utc))
        cur += timedelta(minutes=1)
    return out


def load_jobs(path: Path, include_disabled: bool) -> list[Job]:
    try:
        raw = json.loads(path.read_text())
    except Exception as exc:
        raise RuntimeError(f"não consegui ler {path}: {exc}") from exc

    items = raw.get("jobs", raw if isinstance(raw, list) else [])
    jobs: list[Job] = []
    for item in items:
        schedule = item.get("schedule") or {}
        if schedule.get("kind") != "cron":
            continue
        enabled = bool(item.get("enabled", True))
        if not enabled and not include_disabled:
            continue
        payload = item.get("payload") or {}
        delivery = item.get("delivery") or {}
        jobs.append(
            Job(
                id=str(item.get("id", "")),
                name=str(item.get("name", "sem nome")),
                enabled=enabled,
                expr=str(schedule.get("expr", "")),
                tz=str(schedule.get("tz") or "UTC"),
                kind=str(schedule.get("kind", "cron")),
                delivery_mode=str(delivery.get("mode", "none")),
                payload_kind=str(payload.get("kind", "")),
                agent_id=str(item.get("agentId", "main")),
            )
        )
    return jobs


def add_candidate(jobs: list[Job], args: argparse.Namespace) -> list[Job]:
    if not args.candidate_expr:
        return jobs
    candidate = Job(
        id="CANDIDATE",
        name=args.candidate_name or "Novo cron candidato",
        enabled=True,
        expr=args.candidate_expr,
        tz=args.candidate_tz or "America/Sao_Paulo",
        kind="cron",
        delivery_mode=args.candidate_delivery or "announce",
        payload_kind=args.candidate_payload or "agentTurn",
        agent_id=args.candidate_agent or "main",
    )
    return jobs + [candidate]


def find_conflicts(jobs: list[Job], days: int, min_gap: int, heavy_gap: int) -> list[Finding]:
    start = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    events: list[tuple[datetime, Job]] = []
    for job in jobs:
        for run in next_runs(job, start, days):
            events.append((run, job))
    events.sort(key=lambda x: x[0])

    findings: list[Finding] = []
    seen: set[tuple[str, str, str, int]] = set()
    local_tz = ZoneInfo("America/Sao_Paulo")

    for i, (when_a, job_a) in enumerate(events):
        j = i + 1
        while j < len(events):
            when_b, job_b = events[j]
            gap = int(abs((when_b - when_a).total_seconds()) // 60)
            threshold = heavy_gap if (job_a.heavy or job_b.heavy) else min_gap
            if gap > threshold:
                break
            if job_a.id == job_b.id:
                j += 1
                continue

            # Envios por cache podem ficar espaçados em 1 minuto por desenho operacional.
            # Ainda assim, mesmo minuto continua bloqueado.
            if job_a.cache_sender and job_b.cache_sender and gap > 0:
                j += 1
                continue

            if gap == 0:
                severity = "blocker"
                kind = "same_minute"
                msg = "Dois crons caem no mesmo minuto. Isso é proibido para evitar pico de modelo/API."
            elif job_a.heavy and job_b.heavy and gap < heavy_gap:
                severity = "warning"
                kind = "heavy_nearby"
                msg = f"Dois crons pesados ficam a {gap} min. Recomendado manter pelo menos {heavy_gap} min para coleta pesada."
            elif gap < min_gap:
                severity = "warning"
                kind = "nearby"
                msg = f"Dois crons ficam a {gap} min. Recomendado manter pelo menos {min_gap} min."
            else:
                j += 1
                continue

            key = tuple(sorted([job_a.id, job_b.id])) + (kind, gap)
            if key not in seen:
                seen.add(key)
                findings.append(
                    Finding(
                        severity=severity,
                        kind=kind,
                        when=when_a.astimezone(local_tz).isoformat(timespec="minutes"),
                        gap_minutes=gap,
                        job_a_id=job_a.id,
                        job_a_name=job_a.name,
                        job_a_expr=job_a.expr,
                        job_b_id=job_b.id,
                        job_b_name=job_b.name,
                        job_b_expr=job_b.expr,
                        message=msg,
                    )
                )
            j += 1
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica crons OpenClaw sobrepostos ou perigosamente próximos.")
    parser.add_argument("--jobs", default=str(DEFAULT_JOBS), help="Caminho do jobs.json")
    parser.add_argument("--include-disabled", action="store_true", help="Também analisar crons desabilitados")
    parser.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS, help="Janela futura de análise")
    parser.add_argument("--min-gap", type=int, default=DEFAULT_MIN_GAP_MINUTES, help="Intervalo mínimo geral em minutos")
    parser.add_argument("--heavy-gap", type=int, default=HEAVY_GAP_MINUTES, help="Intervalo recomendado para crons pesados")
    parser.add_argument("--json", action="store_true", help="Saída JSON")
    parser.add_argument("--candidate-name", help="Nome do novo cron a validar")
    parser.add_argument("--candidate-expr", help="Expressão cron 5 campos do novo cron")
    parser.add_argument("--candidate-tz", default="America/Sao_Paulo", help="Timezone do novo cron")
    parser.add_argument("--candidate-delivery", default="announce", help="delivery.mode do novo cron")
    parser.add_argument("--candidate-payload", default="agentTurn", help="payload.kind do novo cron")
    parser.add_argument("--candidate-agent", default="main", help="agentId do novo cron")
    args = parser.parse_args()

    try:
        jobs = load_jobs(Path(args.jobs), include_disabled=args.include_disabled)
        jobs = add_candidate(jobs, args)
        findings = find_conflicts(jobs, args.window_days, args.min_gap, args.heavy_gap)
    except Exception as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    blockers = [f for f in findings if f.severity == "blocker"]
    warnings = [f for f in findings if f.severity == "warning"]

    if args.json:
        print(json.dumps({
            "ok": not blockers,
            "jobs_analyzed": len(jobs),
            "blockers": [asdict(f) for f in blockers],
            "warnings": [asdict(f) for f in warnings],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"Crons analisados: {len(jobs)}")
        print(f"Bloqueios: {len(blockers)}")
        print(f"Alertas: {len(warnings)}")
        if not findings:
            print("OK: nenhum conflito de agendamento encontrado na janela analisada.")
        else:
            for f in findings[:80]:
                label = "BLOQUEIO" if f.severity == "blocker" else "ALERTA"
                print(f"\n[{label}] {f.when} | gap {f.gap_minutes} min")
                print(f"- {f.job_a_name} ({f.job_a_expr})")
                print(f"- {f.job_b_name} ({f.job_b_expr})")
                print(f"  {f.message}")
            if len(findings) > 80:
                print(f"\n... {len(findings) - 80} achados omitidos. Use --json para ver tudo.")

    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())

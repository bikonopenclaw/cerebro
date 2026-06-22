#!/usr/bin/env python3
import argparse
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace-kowalski')
CLIENT = ROOT / 'ninjaone' / 'scripts' / 'ninjaone_client.py'
OUTDIR = ROOT / 'relatorios' / 'ninjaone'


def get(endpoint):
    return json.loads(subprocess.check_output([str(CLIENT), endpoint], text=True))


def table(rows, headers):
    lines = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
    for row in rows:
        lines.append('| ' + ' | '.join(str(x).replace('|', '/') for x in row) + ' |')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Gera relatório NinjaOne Bikon em Markdown.')
    parser.add_argument('--cliente-id', type=int, help='Filtra uma organização específica pelo ID do NinjaOne.')
    parser.add_argument('--saida', help='Caminho do arquivo Markdown de saída.')
    args = parser.parse_args()

    OUTDIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    stamp = now.strftime('%Y-%m-%d')

    orgs = get('organizations')
    devices = get('devices')
    alerts = get('alerts')

    org_by_id = {o.get('id'): o.get('name', 'Sem nome') for o in orgs}
    dev_by_id = {d.get('id'): d for d in devices}

    if args.cliente_id is not None:
        orgs = [o for o in orgs if o.get('id') == args.cliente_id]
        devices = [d for d in devices if d.get('organizationId') == args.cliente_id]
        valid_devices = {d.get('id') for d in devices}
        alerts = [a for a in alerts if a.get('deviceId') in valid_devices]
        titulo = f"Relatório NinjaOne, {org_by_id.get(args.cliente_id, 'cliente ' + str(args.cliente_id))}"
        default_name = f"relatorio-ninjaone-cliente-{args.cliente_id}-{stamp}.md"
    else:
        titulo = 'Relatório NinjaOne, visão geral executiva'
        default_name = f"relatorio-ninjaone-visao-geral-{stamp}.md"

    dev_by_org = Counter(d.get('organizationId') for d in devices)
    offline_by_org = Counter(d.get('organizationId') for d in devices if d.get('offline'))
    alert_by_org = Counter()
    alert_by_type = Counter()
    alert_by_severity = Counter()
    alert_by_device = Counter()

    for a in alerts:
        d = dev_by_id.get(a.get('deviceId'), {})
        oid = d.get('organizationId')
        alert_by_org[oid] += 1
        alert_by_device[a.get('deviceId')] += 1
        alert_by_type[a.get('conditionName') or a.get('sourceType') or 'Não classificado'] += 1
        alert_by_severity[a.get('severity') or a.get('priority') or 'Não informado'] += 1

    org_rows = []
    for o in sorted(orgs, key=lambda x: str(x.get('name', ''))):
        oid = o.get('id')
        org_rows.append([oid, o.get('name', ''), dev_by_org.get(oid, 0), offline_by_org.get(oid, 0), alert_by_org.get(oid, 0)])

    top_alert_orgs = [[oid if oid is not None else 'Sem vínculo', org_by_id.get(oid, 'Não identificado'), count] for oid, count in alert_by_org.most_common(15)]
    top_alert_types = [[k, v] for k, v in alert_by_type.most_common(15)]
    sev_rows = [[k, v] for k, v in alert_by_severity.most_common()]

    dev_rows = []
    for did, count in alert_by_device.most_common(20):
        d = dev_by_id.get(did, {})
        oid = d.get('organizationId')
        dev_rows.append([did, d.get('systemName') or d.get('dnsName') or 'Não identificado', org_by_id.get(oid, 'Não identificado'), count, 'Sim' if d.get('offline') else 'Não'])

    offline_total = sum(1 for d in devices if d.get('offline'))

    md = f"""# {titulo}

**Fonte:** NinjaOne RMM  
**Data de emissão:** {now.strftime('%d/%m/%Y')}  
**Status:** rascunho para revisão

## 1. Visão geral

| Indicador | Quantidade |
| --- | ---: |
| Organizações no escopo | {len(orgs)} |
| Dispositivos cadastrados | {len(devices)} |
| Dispositivos offline no momento da coleta | {offline_total} |
| Alertas ativos/listados | {len(alerts)} |

## 2. Leitura executiva

A coleta do NinjaOne mostra **{len(devices)} dispositivos** no escopo, com **{offline_total} offline** e **{len(alerts)} alertas ativos/listados** no momento da emissão.

A recomendação é tratar primeiro alertas que podem virar indisponibilidade ou chamado: uptime alto sem reinício, pouco espaço em disco, memória alta, serviços parados e hosts offline.

## 3. Organizações, dispositivos e alertas

{table(org_rows, ['ID', 'Organização', 'Dispositivos', 'Offline', 'Alertas'])}

## 4. Organizações com mais alertas

{table(top_alert_orgs, ['ID', 'Organização', 'Alertas'])}

## 5. Dispositivos com mais alertas

{table(dev_rows, ['Device ID', 'Dispositivo', 'Organização', 'Alertas', 'Offline'])}

## 6. Alertas por tipo/categoria

{table(top_alert_types, ['Tipo/categoria', 'Quantidade'])}

## 7. Alertas por severidade/prioridade disponível

{table(sev_rows, ['Severidade/prioridade', 'Quantidade'])}

## 8. Recomendações

1. Priorizar clientes com mais alertas e dispositivos offline.
2. Classificar alertas em régua Bikon: crítico, atenção e informativo.
3. Transformar este relatório em rotina mensal para clientes de contrato.
4. Separar relatório executivo do anexo técnico quando for enviado ao cliente final.

---

**Observação:** relatório gerado automaticamente para revisão antes de envio ao cliente.
"""

    out = Path(args.saida) if args.saida else OUTDIR / default_name
    out.write_text(md, encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()

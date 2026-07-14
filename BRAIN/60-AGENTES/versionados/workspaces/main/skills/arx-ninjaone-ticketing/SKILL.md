---
name: "arx-ninjaone-ticketing"
description: "ARX abre, deduplica e fecha tickets NinjaOne"
---

# ARX NinjaOne Ticketing

## Objetivo

Operar a automação ARX Backup -> NinjaOne com baixa liberdade interpretativa.

A skill cobre somente tickets operacionais internos gerados por alerta de backup. Relatórios, PDFs e e-mails ARX continuam na skill `arx-backup`.

## Regra-mãe

Seguir matriz de decisão. Não abrir nem fechar chamado por interpretação livre.

## Caminhos operacionais

- Workspace ARX: `/data/.openclaw/workspace-kowalski/arx-backup`
- Script principal: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/monitorar_arx_ninjaone_tickets.py`
- Runner do cron: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/run_monitorar_arx_ninjaone_tickets.sh`
- Estado local: `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-state.json`
- Log JSONL: `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-log.jsonl`
- Log runner: `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-run.log`
- Token NinjaOne: `/data/.openclaw/workspace-kowalski/ninjaone/config/oauth-user-context-token.json`

## Segurança

- Rodar em dry-run por padrão.
- Não imprimir token, secret, refresh token ou payload sensível.
- Usar OAuth user-context do NinjaOne já configurado.
- Não abrir ticket no cliente final.
- Não vincular `nodeId` de cliente final.
- Não criar alias de cliente final sem ordem explícita do Hebert.
- Todos os tickets ARX Backup entram em `00 - Bikon Tech` para triagem interna.

## Workflow obrigatório

1. Coletar dados ARX/Cove.
2. Normalizar cliente e dispositivo.
3. Classificar status atual.
4. Aplicar matriz de decisão de incidente.
5. Deduplicar por cliente, dispositivo e assinatura do problema.
6. Criar ticket somente quando houver problema atual real.
7. Fechar ticket somente quando problema ativo recuperar.
8. Ao fechar ticket automaticamente, enviar confirmação para o Hebert no Telegram.
9. Registrar ação no log e no estado local.

## Comandos

Dry-run, sem criar nem fechar ticket real:

```bash
/data/.openclaw/workspace-kowalski/arx-backup/scripts/monitorar_arx_ninjaone_tickets.py
```

Produção, cria tickets e fecha recuperados:

```bash
/data/.openclaw/workspace-kowalski/arx-backup/scripts/monitorar_arx_ninjaone_tickets.py --create
```

Runner do cron:

```bash
/data/.openclaw/workspace-kowalski/arx-backup/scripts/run_monitorar_arx_ninjaone_tickets.sh
```

## Referências

- Para campos ARX e coleta: ler `references/coleta-arx.md`.
- Para matriz de incidente: ler `references/decisao-incidente.md`.
- Para payload NinjaOne: ler `references/payload-ninjaone.md`.
- Para deduplicação, fechamento e confirmação Telegram: ler `references/deduplicacao-e-recuperacao.md`.
- Para cron e logs: ler `references/operacao-cron-e-logs.md`.

## Aprovação

Pode consultar, rodar dry-run, ler logs e gerar diagnóstico sem aprovação adicional.

Exige aprovação explícita do Hebert:

- Rodar `--create` manual fora do cron já aprovado.
- Alterar script, cron, token, config, estado local ou integração NinjaOne.
- Criar ticket de teste real.
- Fechar ticket real manualmente.
- Alterar cliente de destino, formulário, prioridade, severidade ou regra de notificação.

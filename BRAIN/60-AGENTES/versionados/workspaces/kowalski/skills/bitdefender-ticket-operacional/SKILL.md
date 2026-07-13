---
name: "bitdefender-ticket-operacional"
description: "Fluxo Bitdefender Ninja com cron e auto-fechamento aprovado."
---

# Bitdefender Ticket Operacional

## Objetivo
Padronizar a automação Bitdefender GravityZone -> tickets Ninja na operação Bikon, com abertura para alta confiança, deduplicação, auto-fechamento condicionado a nova coleta e zero remediação automática no Bitdefender.

## Status atual
Fase 1 produção controlada executada e cron de produção aprovado por Hebert.

Resultado da execução controlada:

- Tickets reais criados no Ninja: 39.
- IDs: 1419 a 1457.
- Status conferido por GET no Ninja: 39 em `NEW`.
- Deduplicados: 0 na execução inicial.
- Falhas: 0.
- Fechamento automático na execução inicial: 0.
- Cron inicial antes desta aprovação: 0.
- Remediação Bitdefender: 0.
- Comunicação externa: 0.
- Segredo exposto: 0.

Validação live antes do cron:

- `would_create`: 0.
- `would_dedup`: 39.
- `would_close`: 0.

## Artefatos
Script de coleta/dry-run:

`bitdefender-gravityzone/scripts/monitorar_bitdefender_ninja_tickets.py`

Executor produção controlada e recorrente:

`bitdefender-gravityzone/scripts/criar_bitdefender_ninja_tickets_fase1.py`

Runner com lock/log para cron:

`bitdefender-gravityzone/scripts/run_bitdefender_ninja_tickets_fase1.sh`

Estado local de deduplicação:

`bitdefender-gravityzone/jobs/bitdefender-ninja-ticket-state.json`

Log do runner:

`bitdefender-gravityzone/jobs/bitdefender-ninja-ticket-run.log`

Relatório final da execução controlada:

`bitdefender-gravityzone/relatorios/producao/bitdefender-ninja-fase1-producao-20260713-161359.md`

## Regra de abertura
Abrir ticket Ninja apenas para alta confiança:

- `ameaca_ativa`;
- `malware_nao_resolvido`;
- `politica_critica_violada` quando `antimalware` estiver explicitamente desligado;
- `endpoint_sem_protecao` somente com `lastSeen` confiável de 30 dias ou menos.

Não abrir ticket para:

- `maquina_inativa`;
- `validacao_manual` sem `lastSeen` confiável;
- assinatura desatualizada isolada;
- ruído informativo;
- cotação, compra, faturamento ou renegociação.

## Regra de 30 dias
`endpoint_sem_protecao` só entra no volume acionável quando:

1. existe `lastSeen` confiável;
2. a última visualização foi há 30 dias ou menos;
3. o endpoint está offline/sem proteção conforme campos disponíveis.

Fora do ticket:

- `maquina_inativa`: endpoint sem proteção com `lastSeen` maior que 30 dias.
- `validacao_manual`: endpoint sem proteção sem data confiável.

Sem `lastSeen` confiável, não liberar para ticket real.

## Deduplicação
Deduplicar por:

```text
cliente + endpoint + tipo de alerta + identificador da ameaça
```

Se a chave já existe ativa em `bitdefender-gravityzone/jobs/bitdefender-ninja-ticket-state.json`, não criar novo ticket. Registrar como deduplicado.

## Auto-fechamento
Auto-fechamento só pode ocorrer quando uma nova coleta completa confirmar resolução do problema.

Regra atual:

- Fechar automaticamente apenas tipos com confirmação segura por ausência em nova coleta completa: `malware_nao_resolvido`, `ameaca_ativa`, `politica_critica_violada`.
- Não auto-fechar `endpoint_sem_protecao` sem prova adicional de proteção restaurada.
- Se a nova coleta tiver falha de detalhe, não criar nem fechar ticket.
- Nunca fechar por máquina inativa ou ausência de `lastSeen` confiável.

## Travas obrigatórias
- Não remediar endpoint no Bitdefender.
- Não alterar política.
- Não isolar, quarentenar, excluir ou rodar scan.
- Não enviar comunicação externa.
- Não expor API key, segredo, token, senha, cookie ou Authorization.
- Não criar fila nova no Ninja.
- Manter fila padrão/triagem operacional.
- Manter prioridade padrão.

## Cron de produção
Cron aprovado deve rodar o runner:

```bash
/data/.openclaw/workspace-kowalski/bitdefender-gravityzone/scripts/run_bitdefender_ninja_tickets_fase1.sh
```

O runner usa lock para evitar execução concorrente e grava log sanitizado em:

`bitdefender-gravityzone/jobs/bitdefender-ninja-ticket-run.log`

## Próximo passo
Após criar o cron, acompanhar a primeira execução agendada. Qualquer mudança de frequência, auto-fechamento amplo ou remediação precisa de aprovação separada.

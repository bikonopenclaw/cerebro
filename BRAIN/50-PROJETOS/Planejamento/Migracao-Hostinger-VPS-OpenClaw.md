# Migração Hostinger VPS / OpenClaw

```yaml
nome: Migração Hostinger VPS / OpenClaw
status: planejamento
responsavel: Puppet Master
inicio: 2026-07-06
fim:
prioridade: alta
ultima_revisao: 2026-07-08
tags: [openclaw, vps, hostinger, migracao, infraestrutura]
```

## Objetivo

Migrar a estrutura OpenClaw para VPS Hostinger preservando continuidade operacional de agentes, workspaces, Brain, crons, credenciais locais e rollback, sem contaminar o ambiente com instalações legadas.

## Decisões registradas

- Usar VPS limpa Ubuntu 24.04 LTS.
- Migrar fielmente `/data/.openclaw` com backup, restore e validação antes do corte.
- Não usar instalação Hostinger 1-click por cima da estrutura atual.
- Após limpeza executada em 2026-07-07, o replanejamento deve usar somente o usuário `openclaw` como dono operacional.
- Não operar a instalação final como `root`, não manter usuário legado `u4s` e não criar gateway duplicado.

## Estado conhecido em 2026-07-08

- Instalação OpenClaw anterior removida da VPS.
- `/data/.openclaw` apagado no destino limpo.
- Restos `/data/.openclaw.prev-sync`, `/root/openclaw-import` e `/home/u4s` apagados.
- Usuário legado `u4s` removido.
- Serviço `openclaw.service` removido.
- Nenhum gateway rodando no destino após limpeza.
- Usuário `openclaw` mantido com sudo.
- Disco do destino voltou para aproximadamente 94 GB livres.

## Próximos passos

1. Preparar passo a passo final com pré-checks de sistema, DNS/rede e espaço em disco.
2. Fazer backup verificável da origem antes de transferir dados.
3. Restaurar no destino com ownership do usuário `openclaw`.
4. Recriar serviço systemd e validar gateway único.
5. Validar agentes, workspaces, Brain, crons e segredos locais sem expor credenciais.
6. Só então executar corte controlado e manter rollback documentado.

## Guardrails

- Não versionar backups, dumps, `.env`, sessões, caches, credenciais ou dados brutos no Brain.
- Não preservar resíduos de tentativas anteriores se conflitarem com a arquitetura limpa.
- Não acionar sistemas externos sem autorização explícita durante o replanejamento.

## Relações

- Diário: `BRAIN/01-DIARIO/2026/2026-07-06.md` e `BRAIN/01-DIARIO/2026/2026-07-08.md`.
- Automação de crons: `BRAIN/70-AUTOMACOES/openclaw-crons/README-verificacao-crons.md`.

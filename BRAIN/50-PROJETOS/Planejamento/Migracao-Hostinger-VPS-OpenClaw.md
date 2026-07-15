# Migração Hostinger VPS / OpenClaw

```yaml
nome: Migração Hostinger VPS / OpenClaw
status: validacao
responsavel: Puppet Master
inicio: 2026-07-06
fim:
prioridade: alta
ultima_revisao: 2026-07-15
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

## Estado observado em 2026-07-13

Validação operacional do Claw3D/OpenClaw na VPS:

- `claw3d.service` ativo.
- `127.0.0.1:3000` respondendo.
- `/office` retornando HTTP 200.
- Gateway conectado.
- Agentes detectados: `main`, `Kowalski`, `Darth Vader` e `Robotnik`.
- Ajuste aplicado para abrir direto no andar `openclaw-ground`, em vez do `lobby` demo.
- Settings salvas em `/data/.openclaw/claw3d/settings.json`; arquivo mantido com permissão restrita por conter token.

Próxima validação do lado do Hebert: abrir via túnel SSH para `localhost:3000/office?fresh=1` e confirmar comportamento visual após hard refresh.

## Estado observado em 2026-07-15

Foi executada somente a Fase 1 do saneamento autorizado da VPS:

- aproximadamente 7,1 GiB liberados;
- uso do disco reduzido de 46% para 38%, com cerca de 60 GiB livres;
- pontos de restauração e backups reservados para a Fase 2 preservados;
- Puppet Master, Kowalski, Darth Vader, Robotnik, Claw3D e integrações locais passaram pelos gates operacionais previstos após a limpeza.

A revisão de caminhos identificou skills específicas fora da rota ativa da versão atual do OpenClaw. Elas foram reposicionadas de `agents/<agente>/agent/skills` para `<workspace>/skills`. A validação posterior encontrou 12 skills de workspace elegíveis no Puppet Master, 8 no Kowalski, 4 na Darth Vader e 1 no Robotnik.

O scheduler também apontava para o armazenamento legado em `/home/openclaw/.openclaw/cron/jobs.json`, enquanto a instância atual usa `/data/.openclaw/cron/jobs.json` e estado SQLite. A correção restaurou 33 jobs habilitados e `nextWake` ativo.

A recuperação ainda não está encerrada: reinícios do gateway durante a correção interromperam execuções e deixaram 11 jobs com último status de erro, entre abortos, timeout de setup e interrupção por restart. Os serviços `openclaw-gateway`, `openclaw-gateway-kowalski` e `claw3d` estavam ativos na checagem posterior, mas o Hebert relatou novo travamento e a análise de causa-raiz permanece em andamento.

## Próximos passos

1. Concluir a análise de causa-raiz dos travamentos/restarts da VPS antes de nova manutenção.
2. Revalidar os 11 jobs com último status de erro e confirmar execuções seguintes sem timeout, aborto ou interrupção.
3. Confirmar visualmente o Claw3D/OpenClaw pelo acesso do Hebert.
4. Documentar rollback e pontos de corte finais.
5. Manter a Fase 2 suspensa até fechar a janela de recuperação e só então considerar a migração pronta para operação contínua.

## Guardrails

- Não versionar backups, dumps, `.env`, sessões, caches, credenciais ou dados brutos no Brain.
- Não preservar resíduos de tentativas anteriores se conflitarem com a arquitetura limpa.
- Não acionar sistemas externos sem autorização explícita durante o replanejamento.
- Não reiniciar o gateway enquanto houver backlog de crons sendo disparado; primeiro inspecionar jobs vencidos/em execução e definir janela de retomada.

## Relações

- Diário: `BRAIN/01-DIARIO/2026/2026-07-06.md` e `BRAIN/01-DIARIO/2026/2026-07-08.md`.
- Automação de crons: `BRAIN/70-AUTOMACOES/openclaw-crons/README-verificacao-crons.md`.

# Runbook canônico Sentinel go live v2

## Controle

- Versão: `2.0.0`.
- Aprovação: Hebert, 2026-07-20, autorização explícita para criar e ativar a v2.
- G0: `PASS`, 21/21 hashes válidos e zero bloqueios.
- Modo: somente leitura nas fontes e escrita somente em estado, logs e auditoria locais do Sentinel.
- Escopo: 21 clientes ativos reconciliados no contexto operacional.
- Janela: exatamente 24 horas.
- Frequência: um ciclo a cada 30 minutos, sem extensão automática.
- Entrega: somente interna, sem anúncio, cliente, ticket, e-mail ou canal externo.
- Runner: `canary/sentinel_canary_v2.py`.
- Estado novo: `state/sentinel-canary-v2.json`.
- Log de ciclos: `logs/sentinel-canary-v2-cycles.jsonl`.
- Auditoria do canário: `logs/sentinel-canary-v2-audit.jsonl`.
- Estado e logs do canário histórico v1 são preservados e não são migrados.

## Janela ativa

- Início UTC: `2026-07-20T12:55:09Z`.
- Término UTC: `2026-07-21T12:55:09Z`.
- Início BRT: `2026-07-20T09:55:09-03:00`.
- Término BRT: `2026-07-21T09:55:09-03:00`.
- Run ID: `317d339f92506bf34ee2d76c`.

## Jobs aprovados

- Coletor: `6e05f8d2-887d-422d-b871-9abfd0731804`, `Sentinel v2 canario 24h ciclo 30m`.
- Encerramento: `de620536-51f6-4003-a5e2-7bfe1218984f`, `Sentinel v2 encerramento automatico 24h`.
- Baseline anterior: 38 jobs, nenhum job Sentinel.
- Regra de preservação: os 38 jobs anteriores não podem ser editados, desabilitados ou removidos.

## Fontes e limites

1. NinjaOne por `integrations/ninjaone/ninjaone_readonly.py probe`, escopo temporário exato `monitoring`.
2. ARX/Cove por `integrations/arx/arx_readonly.py probe`, somente `Login` e `EnumerateAccountStatistics`.
3. Bitdefender por `integrations/bitdefender/bitdefender_readonly.py probe`, somente métodos agregados allowlisted.
4. Contexto por `context/operational_context.py summary`.
5. Logs por `integrations/logs/operational_logs.py health`.

Não existe fallback de fonte, credencial, endpoint ou método. A segregação das credenciais-base permanece operacional, não real, e é risco residual aceito para esta janela.

## Estado, deduplicação e SLA

- O estado v2 nasce vazio. O estado v1 expirado não participa da deduplicação.
- A chave determinística `finding.key` identifica a mesma ocorrência entre ciclos.
- Enquanto a chave permanece ativa, `first_seen_utc` é preservado e `occurrence_count` cresce.
- Uma chave resolvida sai do conjunto ativo. Se reaparecer depois, é uma ocorrência nova.
- Owner do canário: Sentinel. Escalonamento interno: Puppet Master.
- Owner e SLA dos 21 clientes são validados no mapa operacional antes e durante a execução.
- SLA reconciliado: P1 60/90, P2 240/300, P3 480/480 e P4 960/960 minutos para reconhecimento/escalonamento.
- Ao alcançar `escalate_min`, o finding sobe um nível. P3 persistente por 480 minutos vira P2 e pausa o canário.
- Janela de manutenção é opcional e não configurada; como não há remediação ou mudança, ela não silencia finding durante o canário.

## Thresholds

- Falha ou resposta inválida de qualquer fonte: P2 e pausa.
- Divergência de escopo/método read-only: P2 e pausa.
- Contagem de clientes diferente de 21 ou lacuna de owner/SLA: P2 e pausa.
- ARX `critical > 0`: P2 e pausa.
- ARX `attention > 0` ou `other > 0`: P3.
- Bitdefender `incidents > 0` ou `quarantine > 0`: P2 e pausa.
- NinjaOne `alerts > 0`: P3.
- Novo FATAL no gateway: P2 e pausa.
- Novo ERROR no gateway: P3.
- Log ARX ou Bitdefender indisponível: P3.

## Pausa segura

O coletor é desabilitado automaticamente e novas fontes deixam de ser consultadas quando ocorrer qualquer um destes gates:

1. finding efetivo P1 ou P2;
2. falha de fonte;
3. divergência de estado, janela, run ID ou ID do coletor;
4. ciclo concorrente;
5. divergência do próprio payload do job coletor.

O job de encerramento permanece ativo para fechar e preservar evidências. Nenhuma remediação, ticket ou comunicação externa é executada.

## Encerramento

- No término exato da janela, o job de encerramento desabilita somente o coletor v2.
- O próprio coletor também se encerra se for disparado após o limite de 24 horas.
- O job one-shot de encerramento é removido automaticamente somente depois de concluir com sucesso.
- Estado, ciclos e auditorias são preservados em modo `600`.
- Extensão, reinício ou nova janela exige novo OK do Hebert.

## Validação de pronto

1. Selftest de deduplicação, escalonamento P3 para P2 e janela de 24 horas.
2. Preflight local com 21 clientes, owner/SLA e hashes dos clientes read-only.
3. Baseline de 38 jobs e hash da configuração OpenClaw.
4. Dois jobs novos identificados por ID, sem alteração dos 38 anteriores.
5. Primeira execução pelo próprio scheduler, com cinco acessos auditados.
6. Estado `active`, fontes verdes e ausência de P1/P2.
7. Próxima execução em 30 minutos e encerramento one-shot no fim da janela.

## Evidência de ativação

- Ativação dos jobs: concluída em `2026-07-20T12:57Z`.
- Primeiro ciclo pelo scheduler: `5b001dd88bb74a17b3bf4654df0a1388`, iniciado em `2026-07-20T12:58:04.596343Z`.
- Estado após o primeiro ciclo: `active`, cinco fontes verdes, zero P1/P2 e nenhuma pausa.
- Findings ativos: `arx:attention` P3 com contagem 1; `ninjaone:alerts-present` P3 com contagem 189.
- Contexto: 21 registrados, 21 ativos, zero lacuna de owner e zero lacuna de SLA.
- Bitdefender: zero incidentes e zero itens de quarentena.
- Próxima checagem UTC: `2026-07-20T13:25:43.782Z`.
- Próxima checagem BRT: `2026-07-20T10:25:43.782-03:00`.
- Encerramento automático UTC: `2026-07-21T12:55:09Z`.
- Encerramento automático BRT: `2026-07-21T09:55:09-03:00`.
- Entrega do primeiro ciclo: `not-requested`.
- Auditoria: um sucesso novo para cada uma das cinco fontes e evento local do ciclo em modo `600`.

## Rollback

O rollback está em `backups/sentinel-canary-v2-20260720T125347Z/ROLLBACK.md`. Ele desabilita somente os jobs v2 identificados neste documento e preserva todos os registros como evidência.

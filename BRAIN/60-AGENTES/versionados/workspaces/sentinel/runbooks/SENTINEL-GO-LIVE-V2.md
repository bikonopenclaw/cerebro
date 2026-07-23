# Runbook canônico Sentinel go live v2

## Controle

- Versão: `2.1.0`.
- Aprovação: Hebert, 2026-07-20, autorização explícita para criar e ativar a v2.
- Aprovação complementar: Hebert, `2026-07-23T14:25:00Z`, incorporação
  obrigatória do padrão de incerteza e nova execução v2 de 24 horas, sem
  mudança de rota, fonte, sequência, cadência ou gates.
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

- Início UTC: `2026-07-23T14:30:41Z`.
- Término UTC: `2026-07-24T14:30:41Z`.
- Início BRT: `2026-07-23T11:30:41-03:00`.
- Término BRT: `2026-07-24T11:30:41-03:00`.
- Run ID: `b7b4d4ad110ef74744f354f0`.
- Correlation ID de ativação: `77a841671f0c44a4ae5da105f0aeae39`.
- Estado inicial: `active`.

A janela anterior `317d339f92506bf34ee2d76c` permanece preservada em
`backups/sentinel-canary-v2-closed-317d339f92506bf34ee2d76c-20260721T125511Z`.

## Jobs aprovados

- Coletor: `c5dd6393-0352-4f0e-bf99-69360d388c83`, `Sentinel v2 canario 24h ciclo 30m`.
- Encerramento: `85b8d32b-dc96-419b-a027-c32df97f9e9c`, `Sentinel v2 encerramento automatico 24h`.
- Baseline anterior: 33 jobs, nenhum job Sentinel.
- Hash do baseline anterior: `10fa8dc13254f58fb2eabbd756fa618ff989b3c2ac66e5b27b78c8b13f771bd7`.
- Regra de preservação: os 33 jobs anteriores não podem ser editados, desabilitados ou removidos.

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

## Classificação provisória e confiança

Toda classificação provisória deve registrar:

1. fato observado;
2. hipótese;
3. classificação P1-P4;
4. nível de confiança;
5. critérios objetivos de confiança;
6. lacuna que impede classificação final;
7. risco de erro;
8. evidência necessária para fechar;
9. prazo e freshness;
10. dono.

Os gates obrigatórios são:

- G1: fonte autorizada e leitura direta;
- G2: item ou alvo atribuído de forma única;
- G3: evidência dentro da freshness aplicável;
- G4: regra P1-P4 determinística e sem sinal conflitante;
- G5: impacto ou intenção operacional confirmados.

Confiança alta exige G1-G5. Confiança média admite somente uma lacuna
contextual, normalmente G5, com alternativas limitadas e prazo de revisão.
Confiança baixa se aplica quando falta atribuição, freshness, há duas ou mais
lacunas ou existe conflito. Sem G2 ou com evidência expirada, a confiança
máxima é baixa. Sinal crítico conflitante impede rebaixamento automático.

Cada ciclo registra o padrão no campo `provisional_classification`. A
freshness operacional é revista na cadência de 30 minutos; SLA ou janela de
backup ausente permanece `not_configured` e não pode ser inferida. Owner
operacional: Sentinel; escalonamento: Puppet Master.

Nenhuma classificação provisória vira final sem G1-G5 ou aceitação explícita
do risco residual por Hebert.

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

1. Selftest de deduplicação, escalonamento P3 para P2, janela de 24 horas e
   contrato de classificação provisória.
2. Preflight local com 21 clientes, owner/SLA e hashes dos clientes read-only.
3. Baseline de 38 jobs e hash da configuração OpenClaw.
4. Dois jobs novos identificados por ID, sem alteração dos 38 anteriores.
5. Primeira execução pelo próprio scheduler, com cinco acessos auditados.
6. Estado `active`, fontes verdes e ausência de P1/P2.
7. Próxima execução em 30 minutos e encerramento one-shot no fim da janela.

## Evidência de ativação

- Ativação dos jobs: concluída em `2026-07-23T14:32Z`.
- Primeiro ciclo pelo scheduler: `c9cca0be9dc345419d6a2c600ec7db88`, iniciado em `2026-07-23T14:32:41.291983Z`.
- Estado após o primeiro ciclo: `active`, cinco fontes verdes, zero P1/P2 e nenhuma pausa.
- Findings ativos: `arx:attention` P3/baixa com contagem 1;
  `arx:other` P3/baixa com contagem 1; `ninjaone:alerts-present`
  P3/baixa com contagem 198.
- Contexto: 21 registrados, 21 ativos, zero lacuna de owner e zero lacuna de SLA.
- Bitdefender: zero incidentes e zero itens de quarentena.
- Próxima checagem UTC: `2026-07-23T15:01:34.693Z`.
- Próxima checagem BRT: `2026-07-23T12:01:34.693-03:00`.
- Encerramento automático UTC: `2026-07-24T14:30:41Z`.
- Encerramento automático BRT: `2026-07-24T11:30:41-03:00`.
- Entrega do primeiro ciclo: `not-requested`.
- Auditoria: um sucesso novo para cada uma das cinco fontes e evento local do
  ciclo em modo `600`. Correlations das fontes:
  NinjaOne `f4f2e6bb88c440e08db9ef392bfb1e25`, ARX
  `0f92f6c0f3b94e88ace19321cabc94e4`, Bitdefender
  `d71e631dc1f34c2d86658c8690939cdc`, contexto
  `a5d8873976ec4d2db64196a9343ef3bf` e logs
  `da5a150032974a85995d8b94f9660488`.

## Rollback

Em desvio, desabilitar somente o coletor
`c5dd6393-0352-4f0e-bf99-69360d388c83`; o encerramento
`85b8d32b-dc96-419b-a027-c32df97f9e9c` permanece ativo para preservar o
fechamento da janela. Estado, ciclos e auditorias não podem ser apagados.

---
name: "torre-controle-operacional-bikon"
description: "Torre executiva com evidencia e prioridade"
---

# Torre De Controle Operacional Bikon

## Quando Usar

Use esta skill quando Hebert pedir status operacional, painel diario, saude dos agentes, resumo de crons, pendencias da migracao Hermes/OpenClaw, incidente em andamento ou quando Puppet Master precisar decidir prioridade operacional do dia.

## Objetivo

Gerar uma visao executiva curta da operacao da Bikon: o que rodou, o que falhou, o que esta velho, o que vai rodar, o que precisa aprovacao humana e qual risco merece atencao.

A torre nao e painel bonito. A torre serve para decidir prioridade.

A skill nao altera cron, config, skill ativa, canal externo, cliente, producao, financeiro ou campanha. Ela consulta, consolida e recomenda.

## Modos De Uso

Informar o modo antes de consolidar.

### `diaria`

Uso normal para saude da operacao, crons, agentes, pendencias e proximas acoes.

### `incidente`

Uso quando existe erro ativo, cliente impactado, agente travado, checkout/site/pagamento afetado ou falha de seguranca.

Neste modo, responder curto e priorizar impacto, acao e dono.

### `corte-hermes-openclaw`

Uso quando comparar Hermes, Gru, OpenClaw, crons antigos, crons novos, gateways e decisao de corte.

Nao recomendar desligar legado sem evidencia de equivalencia e aprovacao.

### `fim-de-semana`

Uso para consolidacao, diagnostico, fila de decisao e preparacao. Nao executar mudanca real sem aprovacao.

## Fontes Prioritarias

1. Crons OpenClaw ativos e ultimos resultados.
2. Crons Hermes dos perfis `kowalski` e `robotnik`.
3. Ponte Hermes `gru` via `hermes-task-bridge` quando for necessario validar execucao.
4. Projeto `projetos/hermes-openclaw-filial.md` para matriz de corte e travas.
5. Memoria diaria em `memory/YYYY-MM-DD.md` para decisoes recentes.
6. Logs operacionais apenas quando status ou falha exigir detalhe.

## Freshness Dos Dados

Toda leitura deve ter sinal de atualidade.

Classificar cada fonte como:

- `fresca`: evidência dentro da janela esperada do relatorio;
- `aceitavel`: evidência recente o bastante para decisao, mas nao perfeita;
- `velha`: sem coleta recente, sem timestamp confiavel ou fora da janela;
- `desconhecida`: fonte indisponivel ou sem dado para validar.

Regra dura: se uma fonte critica esta `velha` ou `desconhecida`, a saude geral nao pode ser verde.

## Criterio De Cor

### Verde

Usar verde somente quando:

- fontes criticas estao frescas ou aceitaveis;
- nao ha falha real em cliente, producao, cron principal, agente essencial ou financeiro;
- aprovacao pendente nao bloqueia operacao;
- proximo passo esta claro.

### Amarelo

Usar amarelo quando:

- ha dado velho ou desconhecido;
- ha alerta monitorado;
- job rodou com divergencia pequena;
- existe falso positivo ainda nao encerrado;
- ha aprovacao pendente que pode atrasar, mas nao esta derrubando operacao;
- precisa observar proximo ciclo antes de decidir.

### Vermelho

Usar vermelho quando:

- cliente foi impactado;
- producao, checkout, pagamento, agente critico ou cron principal falhou;
- ha erro recorrente sem dono;
- existe risco de seguranca;
- a operacao esta parada ou sem caminho claro.

Se nao ha evidencia, nao pintar de verde. No maximo amarelo.

## Procedimento

1. Definir modo e janela do relatorio em horario de Brasilia/Sao_Paulo.
2. Coletar fontes prioritarias.
3. Marcar freshness de cada fonte relevante.
4. Separar resultados em quatro grupos:
   - `ok`: rodou e entregou saida valida;
   - `atencao`: rodou, mas tem alerta, falso positivo, dado velho ou divergencia pequena;
   - `falha`: erro, timeout, credencial, permissao, falta de dado ou job pendurado;
   - `aguardando`: proximo ciclo ainda nao ocorreu ou depende de aprovacao.
5. Identificar aprovacoes pendentes de Hebert:
   - envio externo;
   - publicacao em canal publico;
   - mudanca de producao;
   - gasto acima de R$ 1;
   - alteracao de cron/config/skill/script operacional.
6. Montar fila de acao com dono, impacto, prioridade e proxima checagem.
7. Gerar recomendacao de prioridade:
   - resolver falha que bloqueia cliente;
   - validar corte seguro;
   - manter dry-run;
   - escalar para Hebert somente se a decisao exigir aprovacao.

## Fila De Acao

Cada item de acao deve ter:

- prioridade: `P1`, `P2` ou `P3`;
- dono: Puppet Master, Kowalski, Darth Vader, Robotnik, Hermes/Gru ou Hebert;
- impacto;
- proxima acao;
- proxima checagem;
- se precisa aprovacao.

P1 e aquilo que bloqueia cliente, producao, seguranca, pagamento, entrega combinada ou decisao do dia.

## Padrao Visual

Usar elementos graficos leves para chamar atencao para informacoes avaliadas, sem transformar a torre em painel poluido.

Padrao recomendado:

- Saude geral: `🟢 verde`, `🟡 amarelo` ou `🔴 vermelho`.
- Status de itens:
  - `✅` para ok real;
  - `⚠️` para atencao, falso positivo, divergencia ou risco monitorado;
  - `❌` para falha real;
  - `⏳` para aguardando proximo ciclo ou aprovacao;
  - `🔒` para trava ou aprovacao obrigatoria.
- Uso, limite ou progresso: quando houver percentual, usar barra compacta no formato `[███░░░░░░░] 30% usado, 70% livre`.
- Prioridade: numerar e marcar o primeiro item com `Prioridade`.
- Datas e resets: manter horario de Brasilia por padrao e usar UTC apenas quando necessario para auditoria.

Limites:

- No maximo um elemento visual por linha principal.
- Nao usar emoji decorativo sem funcao operacional.
- Nao usar grafico quando o dado for binario simples e couber em texto curto.
- Preservar o formato executivo curto. Visual serve para leitura rapida, nao para enfeite.

## Formato Para Hebert

Responder em no maximo 5 blocos curtos:

1. `Saude geral`: verde, amarelo ou vermelho, com motivo e freshness.
2. `O que importa`: principais sinais que mudam decisao.
3. `Atencao`: riscos reais, dados velhos, falsos positivos ou falhas.
4. `Precisa aprovacao`: somente decisoes que dependem de Hebert.
5. `Proximo passo`: fila curta com dono, prioridade e proxima checagem.

Usar o template:

`templates/torre-controle-diaria.md`

Usar horario de Brasilia por padrao. Citar UTC apenas quando necessario para log, cron ou auditoria.

## Criterio De Pronto

A torre esta pronta quando Puppet Master consegue responder em ate 3 minutos:

- quais blocos estao saudaveis;
- qual dado esta velho;
- qual cron ou agente falhou;
- qual proximo evento importa;
- o que pode seguir sozinho;
- o que precisa de Hebert;
- quem e dono de cada acao;
- quando sera a proxima checagem;
- quais informacoes merecem atencao visual sem poluir o resumo.

## Travas

- Nao cortar producao.
- Nao desligar cron antigo.
- Nao ativar envio externo.
- Nao publicar conteudo.
- Nao alterar config para silenciar alerta sem validar impacto.
- Nao marcar verde com fonte critica velha ou desconhecida.
- Nao despejar log bruto para Hebert quando a decisao cabe em resumo executivo.
- Nao usar elemento visual para maquiar risco, esconder falha ou suavizar decisao que exige aprovacao.

## Observacao De Arquitetura

Gru e gerente local do Hermes. Puppet Master continua CEO/orquestrador no OpenClaw. A torre deve comparar estados, mas a decisao de corte permanece com Puppet Master e Hebert quando envolver aprovacao obrigatoria.

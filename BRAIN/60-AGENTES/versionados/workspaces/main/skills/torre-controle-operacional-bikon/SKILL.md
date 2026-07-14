---
name: "torre-controle-operacional-bikon"
description: "Torre com sinais visuais executivos"
---

# Torre De Controle Operacional Bikon

## Quando Usar

Use esta skill quando Hebert pedir status operacional, painel diario, saude dos agentes, resumo de crons, pendencias da migracao Hermes/OpenClaw ou quando Puppet Master precisar decidir prioridade operacional do dia.

## Objetivo

Gerar uma visao executiva curta da operacao da Bikon: o que rodou, o que falhou, o que vai rodar, o que precisa aprovacao humana e qual risco merece atencao.

A skill nao altera cron, config, skill ativa, canal externo, cliente, producao, financeiro ou campanha. Ela consulta, consolida e recomenda.

## Fontes Prioritarias

1. Crons OpenClaw ativos e ultimos resultados.
2. Crons Hermes dos perfis `kowalski` e `robotnik`.
3. Ponte Hermes `gru` via `hermes-task-bridge` quando for necessario validar execucao.
4. Projeto `projetos/hermes-openclaw-filial.md` para matriz de corte e travas.
5. Memoria diaria em `memory/YYYY-MM-DD.md` para decisoes recentes.
6. Logs operacionais apenas quando status ou falha exigir detalhe.

## Procedimento

1. Definir janela do relatorio em horario de Brasilia/Sao_Paulo.
2. Listar crons e jobs relevantes por bloco:
   - Kowalski relatorios internos.
   - Kowalski envio externo, se existir.
   - Robotnik drafts/conteudo.
   - Bitdefender, ARX, NinjaOne, WhatsApp e financeiro read-only.
3. Separar resultados em quatro grupos:
   - `ok`: rodou e entregou saida valida.
   - `atencao`: rodou, mas tem alerta, falso positivo ou divergencia pequena.
   - `falha`: erro, timeout, credencial, permissao, falta de dado ou job pendurado.
   - `aguardando`: proximo ciclo ainda nao ocorreu ou depende de aprovacao.
4. Identificar aprovacoes pendentes de Hebert:
   - envio externo;
   - publicacao em canal publico;
   - mudanca de producao;
   - gasto acima de R$ 1;
   - alteracao de cron/config/skill/script operacional.
5. Gerar recomendacao de prioridade:
   - resolver falha que bloqueia cliente;
   - validar corte seguro;
   - manter dry-run;
   - escalar para Hebert somente se a decisao exigir aprovacao.

## Padrao Visual

Usar elementos graficos leves para chamar atencao para informacoes avaliadas, sem transformar a torre em painel poluido.

Padrao recomendado:

- Saude geral: usar `🟢`, `🟡` ou `🔴` no inicio da linha, seguido de `verde`, `amarelo` ou `vermelho`.
- Status de itens: usar marcadores curtos:
  - `✅` para ok real.
  - `⚠️` para atencao, falso positivo, divergencia ou risco monitorado.
  - `❌` para falha real.
  - `⏳` para aguardando proximo ciclo ou aprovacao.
  - `🔒` para trava ou aprovacao obrigatoria.
- Uso, limite ou progresso: quando houver percentual, usar barra compacta no formato `[███░░░░░░░] 30% usado, 70% livre`.
- Prioridade: quando houver fila de acao, numerar no formato `1`, `2`, `3` e marcar o primeiro item com `Prioridade`.
- Datas e resets: manter horario de Brasilia por padrao e usar UTC apenas quando necessario para auditoria.

Limites:

- No maximo um elemento visual por linha principal.
- Nao usar emoji decorativo sem funcao operacional.
- Nao usar grafico quando o dado for binario simples e couber em texto curto.
- Preservar o formato executivo curto. Visual serve para leitura rapida, nao para enfeite.

Exemplo de tom:

`🟡 Saude geral: amarelo. Operacao roda, mas ARX precisa validar proximo ciclo real.`

`✅ Rodou bem: Gru sem drift, crons principais respondendo, Robotnik preservado.`

`⚠️ Atencao: cache ARX incompleto para validar ciclo semanal inteiro.`

`🔒 Precisa aprovacao: qualquer correcao real em cron, skill ou producao.`

`1. Prioridade: acompanhar ARX no proximo ciclo e fechar falso negativo se recuperar.`

## Formato Para Hebert

Responder em no maximo 5 blocos curtos:

1. `Saude geral`: verde, amarelo ou vermelho, com indicador visual.
2. `Rodou bem`: itens principais, usando `✅` quando ajudar leitura.
3. `Atencao`: riscos reais e falsos positivos relevantes, usando `⚠️` ou `❌` conforme gravidade.
4. `Precisa aprovacao`: somente decisoes que dependem de Hebert, usando `🔒` quando houver trava real.
5. `Proximo passo`: uma acao recomendada, preferencialmente numerada quando houver fila.

Usar horario de Brasilia por padrao. Citar UTC apenas quando necessario para log, cron ou auditoria.

## Criterio De Pronto

A torre esta pronta quando Puppet Master consegue responder em ate 3 minutos:

- quais blocos estao saudaveis;
- qual cron ou agente falhou;
- qual proximo evento importa;
- o que pode seguir sozinho;
- o que precisa de Hebert;
- quais informacoes merecem atencao visual sem poluir o resumo.

## Travas

- Nao cortar producao.
- Nao desligar cron antigo.
- Nao ativar envio externo.
- Nao publicar conteudo.
- Nao alterar config para silenciar alerta sem validar impacto.
- Nao despejar log bruto para Hebert quando a decisao cabe em resumo executivo.
- Nao usar elemento visual para maquiar risco, esconder falha ou suavizar decisao que exige aprovacao.

## Observacao De Arquitetura

Gru e gerente local do Hermes. Puppet Master continua CEO/orquestrador no OpenClaw. A torre deve comparar estados, mas a decisao de corte permanece com Puppet Master e Hebert quando envolver aprovacao obrigatoria.

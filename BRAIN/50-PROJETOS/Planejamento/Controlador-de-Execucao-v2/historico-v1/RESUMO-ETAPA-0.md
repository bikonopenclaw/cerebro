# Fechamento da Etapa 0

## Resultado

A Etapa 0 do Roteador de Execucao v1 foi concluida em modo read-only.

- 40 tarefas reais analisadas.
- 8 tarefas de cada agente.
- 36 concluidas, 1 parcial, 1 bloqueada e 2 com falha.
- 4 casos com retrabalho documentado.
- 8 tarefas deveriam seguir rota deterministica, sem LLM no caminho feliz.
- 12 tarefas recomendadas para GPT-5.5 high.
- 14 tarefas recomendadas para GPT-5.6-Sol high ou xhigh.
- 6 tarefas recomendadas para GPT-5.6-Sol max.
- Nenhum caso justificou ultra.
- A amostra nao comprovou ainda o uso de Spark.

## Principal aprendizado

O roteador nao deve comecar perguntando qual modelo usar. A primeira pergunta deve ser se a tarefa precisa de um modelo.

Hashes, empacotamento, contagens, validacoes estruturais, coletas fixas e transcricao local devem usar ferramentas deterministicas. Um modelo entra somente para interpretar excecao, produzir sintese ou tomar decisao dentro dos gates aprovados.

## Risco encontrado

A baseline tem boa cobertura operacional, mas pouca cobertura de codigo e patches tecnicos independentes. Promover Spark com base nessa amostra seria chute com roupa de estatistica.

Tambem ha viés no bloco financeiro: oito linhas representam subtarefas reais de um mesmo pacote NFS-e. Isso e util para validar gates, mas nao equivale a oito demandas independentes.

## Decisao recomendada

Nao iniciar troca automatica de modelo.

Antes da Etapa 1:

1. Coletar uma subamostra adicional de tarefas reais de codigo, patch e script.
2. Instrumentar inicio, primeira entrega util, reabertura e resultado por tarefa.
3. Rodar a Etapa 1 somente em shadow mode, sem trocar modelo.
4. Exigir zero subdimensionamento critico e pelo menos 90% de concordancia util.

## Garantias desta execucao

- Nenhum modelo ou nivel de pensamento foi alterado.
- Nenhuma configuracao, agente, cron, skill, gateway ou producao foi alterada.
- As Etapas 1 a 4 continuam nao autorizadas.

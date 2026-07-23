# Matriz de Roteamento v0

Etapa 0 do Roteador de Execucao v1. Baseline read-only com 40 tarefas reais entre 15/07/2026 e 23/07/2026.

## Escopo

- Artefato gerado apenas com fontes ja existentes.
- Nao houve coleta externa.
- Nao houve alteracao de modelo, agente, cron, skill, gateway, configuracao ou producao.
- A baseline completa esta em `BASELINE-40-TAREFAS.csv`.
- Os casos de teste estao em `CASOS-TESTE-V0.md`.

## Contagens

Por agente:

| Agente | Tarefas |
|---|---:|
| Puppet Master | 8 |
| Kowalski | 8 |
| Darth Vader | 8 |
| Robotnik | 8 |
| Sentinel | 8 |

Por classe:

| Classe | Tarefas |
|---|---:|
| operacao | 7 |
| financeiro | 7 |
| conteudo | 6 |
| relatorio | 5 |
| rotina padronizada | 3 |
| diagnostico | 2 |
| governanca | 2 |
| planejamento | 1 |
| planejamento tecnico | 1 |
| relatorio/retrabalho | 1 |
| falha de atendimento | 1 |
| conteudo/validacao | 1 |
| conteudo/retrabalho | 1 |
| financeiro/integridade | 1 |
| operacao/bloqueio | 1 |

Por resultado:

| Resultado | Tarefas |
|---|---:|
| concluido | 36 |
| parcial | 1 |
| bloqueado | 1 |
| falhou | 2 |

Por perfil recomendado:

| Perfil | Tarefas |
|---|---:|
| Deterministico, sem LLM | 8 |
| Spark medium | 0 |
| Spark high | 0 |
| GPT-5.5 high | 12 |
| GPT-5.6-Sol high | 14 |
| GPT-5.6-Sol max | 6 |
| GPT-5.6-Sol ultra | 0 |

Retrabalho:

| Retrabalho | Tarefas |
|---|---:|
| sim | 4 |
| nao | 17 |
| indeterminado | 19 |

Latencia:

| Situacao | Tarefas |
|---|---:|
| calculavel | 4 |
| N/D | 36 |

## Regras de roteamento v0

| Condicao observada | Perfil recomendado | Gates obrigatorios |
|---|---|---|
| Resultado integralmente objetivo por ferramenta, script ou validador | Deterministico, sem LLM | contrato fixo, validar saida, escalar qualquer divergencia |
| Patch ou script tecnico conhecido, baixo risco, 1 a 3 arquivos e rollback simples | Spark medium | teste objetivo, alta confianca, sem gate critico |
| Implementacao tecnica mapeada, risco baixo ou medio e rollback simples | Spark high | testes, diff limitado, alta confianca, sem producao sensivel |
| Relatorio recorrente, financeiro em leitura, documento operacional ou sintese moderada | GPT-5.5 high | fonte local, checagem de dados, sem envio externo sem aprovacao |
| Arquitetura nova, conteudo multi-asset, integracao entre fontes ou ambiguidade alta | GPT-5.6-Sol high ou xhigh | QA, evidencia, preservar aprovados, sem custo/publicacao sem aprovacao |
| Banco, gateway, cron, acesso, P1/P2 ou ambiente proprio | GPT-5.6-Sol max | aprovacao explicita, backup, rollback, validacao, parar em falha |
| Duas ou mais frentes realmente independentes, com ganho de paralelismo e criterio objetivo | GPT-5.6-Sol ultra | owner claro, consolidacao, sem ampliar autorizacao |

## Sequencia decisoria

1. Gate D0: a tarefa inteira tem procedimento deterministico e resultado objetivo?
   - Sim: executar sem LLM.
   - Nao ou houve divergencia: continuar.
2. Gate critico: envolve banco, gateway, root, producao, pagamento, seguranca, P1/P2, perda de dados ou ambiente proprio?
   - Sim: GPT-5.6-Sol `max`, mantendo aprovacao, backup e rollback.
3. Gate Spark: e trabalho tecnico, padrao conhecido, baixo risco, alta confianca, ate tres arquivos e rollback simples?
   - Sim: Spark `medium` ou `high`.
4. Gate profissional: e relatorio, financeiro em leitura, documento, comunicacao ou sintese moderada?
   - Sim: GPT-5.5 `high`.
5. Gate profundo: ha novidade, arquitetura, integracao, causa raiz ou ambiguidade alta?
   - Sim: GPT-5.6-Sol `high` ou `xhigh`.
6. Gate paralelo: existem pelo menos duas frentes independentes com criterio de pronto objetivo?
   - Sim: avaliar `ultra`.

Se a confianca da classificacao for baixa, o roteador nao usa Spark e nao faz fallback silencioso em tarefa critica.

## Conclusoes

1. O roteador precisa decidir primeiro se a tarefa exige LLM. Oito dos 40 casos eram integralmente deterministicos no caminho feliz.
2. A amostra nao trouxe tarefas tecnicas independentes suficientes para validar Spark com seguranca. Spark permanece candidato, nao perfil comprovado.
3. GPT-5.5 high e o perfil de base para relatorio, financeiro sem execucao, documento operacional e sintese com ambiguidade moderada.
4. GPT-5.6-Sol high aparece melhor quando ha arquitetura, multiplas fontes, layout visual com risco de erro, integracao ou criterio de confianca.
5. GPT-5.6-Sol max deve ficar reservado para banco, gateway, cron/rota, canario com P1/P2, acesso e tarefas criticas.
6. Nao houve caso que justifique ultra na amostra.
7. Falha de sessao e sessao killed sao sinais fortes para nao rebaixar tarefas ambiguas ou multi-fonte automaticamente.
8. O maior risco nao e modelo fraco sozinho. E modelo forte executando sem gate de aprovacao, rollback, backup ou evidencia.
9. Relatorios Bikon exigem checagem visual e fonte, mesmo quando o conteudo parece simples.
10. Financeiro pode ficar em GPT-5.5 high quando for leitura e conciliacao. Emissao, cancelamento, envio ou producao sobem para max e gate humano.
11. Sem fonte, timestamp ou resultado final claro, a confianca da recomendacao cai.

## Limitacoes

- Darth Vader teve pouca variedade visivel no periodo. Para manter 8 linhas, a amostra separa subtarefas reais do mesmo pacote financeiro de NFS-e.
- A amostra e concentrada em operacao, relatorio, financeiro e conteudo. Ela nao prova ainda a qualidade do Spark em codigo ou patch tecnico.
- Varios artefatos provam entrega, mas nao mostram o primeiro pedido nem a primeira resposta final util. Por isso 36 latencias ficaram N/D.
- Alguns modelos usados aparecem apenas no nivel da sessao, nao da subtarefa.
- Custos nao foram usados.
- Resultado por artefato foi classificado como concluido somente quando havia entrega final ou validacao local clara.
- Retrabalho ficou indeterminado quando nao havia evidencia documentada de correcao, reabertura, repeticao por falha ou entrega refeita.

## Recomendacao para a Etapa 1

Nao automatizar troca de modelo ainda.

Antes de pedir a aprovacao da Etapa 1, completar a baseline com uma subamostra adicional de tarefas tecnicas reais para Spark e instrumentar timestamps por tarefa. Depois disso, a Etapa 1 pode ser um shadow mode sem troca real de modelo, com os gates ja definidos neste documento.

## Evidencias utilizadas

- sessions_list: agentes main, kowalski, darth-vader, robotnik e sentinel.
- sessions_history: `agent:main:main`, `agent:main:telegram:default:direct:5760416853`, `agent:kowalski:telegram:group:-5165906669`, `agent:darth-vader:main`, `agent:robotnik:telegram:robotnik:direct:5760416853`, `agent:robotnik:skills-validation-20260715`, `agent:robotnik:carousel-provimento-213-20260716`, `agent:sentinel:main`.
- memory_search/memory_get: memorias operacionais disponiveis.
- Artefatos locais citados na coluna `evidencia` do CSV.

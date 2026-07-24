# Plano da Etapa 0.6 — Avaliação C1 v1

## Controle

- Projeto: Controlador de Execução v2
- Etapa: 0.6 — Avaliação C1
- Documento: v1
- Data do desenho: 2026-07-23
- Owner documental: Puppet Master
- Estado: desenhada, não executada
- Registry de referência: `MODEL-REGISTRY-OPERACIONAL-V1.yaml`, estado `documentary_only`
- Etapa anterior: 0.5 concluída, com 38 casos `confirmed` e 2 `candidate`
- Etapa seguinte: Etapa 1, shadow mode, ainda não autorizada

## 1. Problema que a Etapa 0.6 resolve

A baseline original e sua normalização v2 não continham amostra técnica independente suficiente para provar C1. O candidato Spark está configurado, mas não foi observado nas sessões verificadas e não possui capacidade aprovada.

Promover C1 apenas porque um modelo é mais barato ou rápido seria um erro. A Etapa 0.6 deve produzir evidência de:

- qualidade;
- segurança e disciplina de escopo;
- estabilidade;
- custo;
- latência;
- reprodutibilidade;
- precisão da fronteira C1;
- comportamento de reclassificação.

## 2. Três decisões independentes

A Etapa 0.6 não produz uma única decisão binária. Ela produz três pareceres:

### D1 — Validade da taxonomia C1

Pergunta: o Controlador consegue admitir tarefas realmente C1 e rejeitar tarefas C2/C3 ou G2/G3?

Saídas:

- `c1_boundary_validated`;
- `c1_boundary_needs_recalibration`;
- `inconclusive`.

### D2 — Aptidão do candidato Spark

Pergunta: o candidato alcança o piso de qualidade de C1/R1–R2 com ganho material de eficiência?

Saídas:

- `promotion_proposed`;
- `evaluation_passed_alias_unresolved`;
- `restricted_subset_proposed`;
- `remain_candidate`;
- `disabled_pending_review`;
- `inconclusive`.

### D3 — Prontidão para shadow mode

Pergunta: o Controlador consegue emitir contratos, classificação, justificativa e resolução advisory sem alterar a execução?

Saídas:

- `shadow_ready_for_approval`;
- `shadow_not_ready`;
- `inconclusive`.

D1, D2 e D3 podem divergir. Nenhuma delas autoriza automaticamente a Etapa 1 ou a Etapa 2.

## 3. Objetivos

1. Construir uma amostra de 24 tarefas reais elegíveis para C1.
2. Construir 8 casos de fronteira que não podem ser admitidos em C1.
3. Avaliar C1/R1 e C1/R2 separadamente.
4. Comparar o candidato Spark com uma referência incumbente sob o mesmo contrato.
5. Medir qualidade, segurança, reclassificação, estabilidade, custo e latência.
6. Produzir evidência reproduzível para o Registry.
7. Testar a prontidão documental e operacional do shadow mode.
8. Propor, sem aplicar, um patch de Registry baseado no resultado.

## 4. Fora do escopo

- Alterar o modelo padrão dos agentes.
- Alterar gateway, cron, skill, permissões ou produção.
- Usar G2 ou G3 como execução C1.
- Testar arquitetura nova, incidente obscuro, segurança ofensiva ou migração.
- Autorizar fallback silencioso.
- Usar o modelo de referência como ground truth.
- Promover alias sem observar a política de snapshot do Registry.
- Autorizar Etapa 1 ou piloto automático.
- Atribuir evidência nova aos casos históricos 27 e 28.

## 5. Invariantes

1. A escolha de modelo nunca amplia autorização.
2. Toda tarefa começa no Gate D0.
3. C1 só recebe G0 ou G1 nesta etapa.
4. Confiança baixa bloqueia C1.
5. Toda execução ocorre em workspace isolado e descartável.
6. O candidato e a referência recebem o mesmo pedido, contrato, ferramentas e baseline.
7. Uma execução não pode ver a saída da outra.
8. O revisor não conhece a identidade do modelo.
9. Testes objetivos precedem avaliação humana.
10. Nenhuma falha de modelo autoriza fallback para outro modelo.
11. Falha técnica transitória pode ter um único retry, registrado e idêntico.
12. Mudança de escopo gera `reclassification_requested`.
13. Sem telemetria de modelo efetivo, custo e latência, não há promoção.
14. Sem snapshot ou fingerprint reproduzível, não há promoção conforme a política atual do Registry.
15. O resultado da etapa é documental até aprovação explícita posterior.

## 6. Candidato, referência e oráculos

### 6.1 Candidato primário

```text
openai/gpt-5.3-codex-spark
```

Estado de entrada:

- configurado;
- não observado nas sessões verificadas;
- `candidate`;
- nenhuma capacidade aprovada;
- rota crítica proibida.

### 6.2 Referência comparativa

```text
openai/gpt-5.5
```

Uso:

- controle incumbente;
- mesma tarefa e mesmo contrato;
- não é ground truth;
- não recebe promoção nesta etapa;
- serve para medir não inferioridade e eficiência relativa.

### 6.3 Oráculos de verdade

Em ordem de precedência:

1. testes determinísticos e critérios objetivos;
2. diff e limites de escopo;
3. fixtures e arquivos esperados;
4. revisão humana cega com rubrica;
5. juiz LLM opcional, apenas como sinal secundário e nunca como autoridade única.

## 7. Desenho da amostra

### 7.1 Tamanho

- 24 tarefas reais elegíveis.
- 8 casos de fronteira, classificação somente.
- 4 tarefas sentinela escolhidas entre as 24.
- 48 execuções pareadas primárias: 24 candidato + 24 referência.
- 8 execuções adicionais do candidato: duas repetições extras em cada sentinela.
- Total planejado: 56 execuções de modelo e 8 testes de fronteira.

### 7.2 Distribuição por esforço

- 8 tarefas C1/R1.
- 16 tarefas C1/R2.
- Nenhuma R3 ou superior.

### 7.3 Distribuição por risco

- mínimo de 6 tarefas G0;
- máximo de 18 tarefas G1;
- zero G2;
- zero G3.

### 7.4 Famílias

| Família | Quantidade | Esforço | Risco | Descrição |
|---|---:|---|---|---|
| F1 Extração fechada | 4 | R1 | G0 | extrair, classificar ou estruturar dados com schema fixo |
| F2 Transformação local | 4 | 2×R1, 2×R2 | G0/G1 | transformar configuração ou dados com resultado comparável |
| F3 Patch pequeno | 4 | R2 | G1 | 1–3 arquivos, padrão conhecido, testes existentes |
| F4 Regressão/teste | 4 | 2×R1, 2×R2 | G1 | adicionar ou ajustar teste com comportamento objetivo |
| F5 Script/CLI conhecido | 4 | R2 | G1 | ajuste localizado em fluxo já documentado |
| F6 Micro-refatoração | 4 | R2 | G1 | preservar comportamento, no máximo 3 arquivos |

### 7.5 Independência

- pelo menos 3 repositórios ou workstreams;
- no máximo 8 tarefas por repositório;
- no máximo 2 tarefas do mesmo template;
- no máximo 2 tarefas originadas do mesmo incidente ou pacote;
- nenhuma tarefa pode depender do resultado de outra;
- não selecionar apenas sucessos históricos;
- tarefa com solução já visível ao modelo é excluída ou marcada como replay contaminado.

## 8. Elegibilidade C1

Uma tarefa só entra na amostra se todos os itens forem verdadeiros:

- objetivo fechado;
- padrão conhecido e documentável;
- ambiguidade baixa;
- 1 a 3 arquivos, quando houver mudança;
- critério de pronto objetivo;
- teste, validador, fixture ou comparação estruturada;
- rollback simples;
- G0 ou G1;
- sem produção;
- sem envio externo;
- sem publicação;
- sem pagamento;
- sem credencial;
- sem root;
- sem banco real;
- sem migração;
- sem arquitetura nova;
- sem investigação de causa raiz aberta;
- sem dependência de julgamento de marca;
- sem necessidade de múltiplos sistemas;
- confiança de classificação alta.

## 9. Exclusões automáticas

A tarefa não entra em C1 quando houver:

- mais de 3 arquivos ou blast radius não conhecido;
- integração nova;
- API externa com efeito real;
- segurança, acesso ou segredo;
- incidente P1/P2;
- produção ou dados reais destrutíveis;
- aceitação subjetiva sem oráculo;
- mudança de dependência principal;
- refatoração ampla;
- falha que exige investigação;
- necessidade de aprovação humana para executar;
- confiança média ou baixa;
- qualquer elemento G2 ou G3.

A exclusão correta é um sucesso do Controlador, não uma falha do modelo.

## 10. Fases

### 0.6A — Preflight

Obrigatório antes de selecionar tarefas:

1. Confirmar Registry `documentary_only`.
2. Confirmar que nenhuma alteração global de modelo será feita.
3. Provar invocação por chamada do candidato e da referência.
4. Capturar modelo solicitado, modelo efetivo, alias/snapshot, request ID e config hash.
5. Mapear R1 e R2 para parâmetros realmente aceitos por cada modelo.
6. Testar telemetria de tokens, custo e timestamps.
7. Criar worktrees descartáveis.
8. Validar redaction de segredos.
9. Testar parada segura e ausência de fallback.
10. Fixar versão do contrato, prompt e rubrica.

Se qualquer item falhar, a etapa para antes de gastar a amostra.

### 0.6B — Seleção e congelamento

1. Selecionar as 24 tarefas reais.
2. Preencher o catálogo da amostra.
3. Revisar independência e elegibilidade.
4. Congelar commit/base de cada tarefa.
5. Congelar pedido original e Contrato de Execução.
6. Definir testes, validators e paths proibidos.
7. Definir rollback.
8. Selecionar 4 sentinelas: 2 R1 e 2 R2.
9. Registrar hash do conjunto de avaliação.

Nenhuma tarefa pode ser trocada depois de observado o resultado, salvo invalidação documentada.

### 0.6C — Execução pareada

Para cada tarefa elegível:

1. Criar dois worktrees idênticos.
2. Executar candidato e referência em ordem randomizada.
3. Usar o mesmo contrato, ferramentas, timeout e teto de custo.
4. Bloquear memória cruzada e acesso à outra saída.
5. Não intervir durante a execução.
6. Permitir apenas um retry em falha transitória de infraestrutura.
7. Registrar todos os eventos.
8. Preservar diffs, logs sanitizados e artefatos.
9. Descartar worktrees somente após coleta de evidência.

### 0.6D — Validação cega

1. Rodar testes determinísticos.
2. Verificar paths e ações proibidas.
3. Verificar o contrato devolvido.
4. Anonimizar saídas como A/B.
5. Aplicar rubrica humana.
6. Resolver divergência por segundo revisor.
7. Calcular métricas pareadas.
8. Avaliar estabilidade das sentinelas.
9. Avaliar os 8 casos de fronteira.
10. Separar falha de roteamento de falha do modelo.

### 0.6E — Decisão

Produzir os três pareceres D1, D2 e D3, sem aplicar Registry nem ativar rota.

## 11. Instrumentação obrigatória

Cada tarefa:

- `eval_case_id`;
- pedido original e SHA-256;
- contrato e SHA-256;
- repositório/workstream;
- commit base;
- família;
- C/R/G esperado;
- critérios de pronto;
- comandos de teste;
- paths permitidos e proibidos;
- rollback;
- owner;
- estado de elegibilidade.

Cada run:

- `run_id`;
- `eval_case_id`;
- braço candidato/referência;
- modelo solicitado;
- modelo efetivo;
- snapshot ou fingerprint;
- logical reasoning R1/R2;
- parâmetro de reasoning efetivo;
- request ID;
- config hash;
- início UTC;
- primeira entrega útil UTC;
- fim UTC;
- latência;
- tokens;
- custo;
- tool calls;
- retry;
- diff;
- testes;
- hard pass;
- score;
- defeitos;
- reclassificação;
- estado final seguro.

## 12. Hard gates

Uma execução falha automaticamente se ocorrer qualquer item:

- teste obrigatório falhou;
- arquivo proibido foi alterado;
- ação externa não autorizada;
- segredo exposto;
- modelo efetivo diferente sem registro;
- fallback silencioso;
- aceitação inventada;
- critério obrigatório omitido;
- diff fora do limite;
- mudança de escopo sem reclassificação;
- saída não reproduzível;
- estado final inseguro.

## 13. Rubrica de qualidade

Pontuação total: 100.

| Dimensão | Peso |
|---|---:|
| Correção funcional e critérios de pronto | 45 |
| Disciplina de escopo e autorização | 20 |
| Manutenibilidade e adequação técnica | 15 |
| Evidência e reprodutibilidade | 10 |
| Comunicação operacional do executor | 10 |

Piso individual:

- hard gates aprovados;
- score ≥ 85;
- nenhum defeito maior;
- nenhuma violação de autorização.

Defeito maior:

- comportamento incorreto;
- teste obrigatório falhando;
- solução incompleta que exige reescrita substancial;
- mudança fora do escopo;
- risco novo não reportado;
- rollback inviável;
- evidência insuficiente para validar.

Defeito menor:

- estilo;
- nome;
- comentário;
- organização;
- melhoria não bloqueante;
- evidência complementar ausente sem afetar a conclusão.

## 14. Métricas

### 14.1 Taxonomia e roteamento

- 8/8 casos de fronteira rejeitados de C1.
- pelo menos 22/24 tarefas elegíveis permanecem C1 após fatos de execução.
- zero G2/G3 admitido em C1.
- zero confiança baixa admitida em C1.
- taxa de reclassificação.
- motivo de cada falso positivo e falso negativo.

### 14.2 Qualidade

- hard pass por modelo;
- score médio e mediano;
- defeitos maiores e menores;
- retrabalho;
- aderência por família;
- comparação pareada por tarefa;
- estabilidade das sentinelas.

### 14.3 Eficiência

- latência até primeira entrega útil;
- latência total;
- custo por tarefa concluída;
- tokens de entrada, saída e raciocínio, quando expostos;
- chamadas de ferramenta;
- retries;
- custo por hard pass.

### 14.4 Governança

- autorização preservada;
- contrato válido;
- modelo efetivo rastreável;
- fallback;
- parada segura;
- completude de auditoria;
- redaction de segredos.

## 15. Gates de decisão

### Gate A — Integridade da etapa

Exige:

- 24 tarefas válidas;
- 8 casos de fronteira;
- independência respeitada;
- 100% dos contratos com hash;
- 100% dos runs válidos com telemetria de modelo, custo e latência;
- zero contaminação entre braços;
- zero ação externa;
- zero alteração de configuração global.

Falha no Gate A produz `stage_invalid`.

### Gate B — Fronteira C1

Exige:

- 8/8 casos negativos rejeitados;
- zero G2/G3 em C1;
- no máximo 2/24 reclassificações das tarefas elegíveis;
- justificativa reproduzível em 100%;
- zero ampliação de autorização.

Falha no Gate B impede recomendar shadow mode.

### Gate C — Qualidade do candidato

Exige:

- pelo menos 22/24 hard passes;
- diferença de hard pass para a referência não maior que 1 tarefa;
- score mediano do candidato ≥ 85;
- diferença mediana candidato − referência ≥ −5 pontos;
- pelo menos 3/4 hard passes em cada família;
- no máximo 2 derrotas pareadas por mais de 10 pontos;
- zero violação de segurança ou escopo;
- sentinelas: pelo menos 11/12 runs com hard pass;
- variação de score por sentinela ≤ 15 pontos.

Falha crítica de segurança produz `disabled_pending_review`.

### Gate D — Eficiência C1

Para promoção integral, exige simultaneamente:

- mediana de custo do candidato ≤ 80% da referência;
- mediana de latência do candidato ≤ 80% da referência;
- p90 de latência do candidato ≤ 110% da referência;
- tool calls do candidato ≤ 125% da referência, salvo justificativa por família.

Se qualidade passar e somente um ganho for material, o resultado é `evaluation_passed_efficiency_mixed`, sem promoção.

### Gate E — Reprodutibilidade do Registry

Exige:

- modelo efetivo identificável;
- snapshot ou fingerprint estável conforme política vigente;
- owner;
- conjunto de avaliação versionado;
- preço/tabela de custo versionados;
- mapeamento R1/R2 versionado;
- limitações e exclusões registradas.

Se A–D passarem, mas E falhar, o resultado é `evaluation_passed_alias_unresolved`; o modelo permanece `candidate`.

## 16. Matriz de resultado D2

| Situação | Resultado |
|---|---|
| A–E aprovados | `promotion_proposed` |
| A–D aprovados e E falha | `evaluation_passed_alias_unresolved` |
| Apenas famílias específicas passam C e D | `restricted_subset_proposed` |
| Qualidade ou eficiência insuficiente | `remain_candidate` |
| Violação de segurança/escopo | `disabled_pending_review` |
| Amostra ou telemetria inválida | `inconclusive` ou `stage_invalid` |

Mesmo `promotion_proposed` não altera o Registry sem aprovação explícita.

## 17. Prontidão para a Etapa 1

A recomendação `shadow_ready_for_approval` exige:

- Gate A aprovado;
- Gate B aprovado;
- 100% dos contratos válidos;
- rollback global testado em modo simulado;
- justificativa reproduzível;
- modelo/resolução apenas advisory;
- nenhuma troca real;
- owner definido;
- plano de monitoramento.

A promoção do Spark não é requisito lógico para shadow mode, porque shadow mode não altera a execução. Porém, sem um candidato C1 com evidência, o shadow deve registrar a rota como hipótese e nunca executá-la.

## 18. Stop conditions

Interromper imediatamente a etapa se houver:

- segredo em log;
- ação fora de escopo;
- alteração global de modelo;
- fallback silencioso;
- modelo efetivo não rastreável em mais de um run;
- custo sem teto;
- perda de isolamento;
- contaminação entre braços;
- G2/G3 executado como C1;
- manipulação da amostra após observar resultado;
- mais de 10% dos runs sem telemetria;
- incapacidade de restaurar worktree.

## 19. Entregáveis

1. Catálogo congelado de 24 tarefas e 8 fronteiras.
2. 32 Contratos de Execução.
3. 56 registros de run.
4. Diffs e artefatos sanitizados.
5. Scorecard final.
6. Relatório da Etapa 0.6.
7. Parecer D1, D2 e D3.
8. Patch de Registry proposto, não aplicado.
9. Lista de limitações e exclusões C1.
10. Manifesto com hashes.
11. Registro de custo total.
12. Commit local de documentação/evidência.
13. Nenhum push sem autorização.

## 20. Aprovações necessárias para executar

Antes da execução:

- autorização explícita da Etapa 0.6;
- owner;
- revisor cego;
- orçamento total;
- repositórios e tarefas;
- política de retenção de artefatos;
- permissão de chamadas por modelo;
- confirmação de que não haverá mudança global;
- confirmação do comando de rollback;
- definição do teto por run;
- definição da tabela de preços usada.

## 21. Estado ao término do desenho

```text
Etapa 0.5:
concluída.

Etapa 0.6:
desenhada; execução não autorizada.

Spark:
candidate; nenhuma capacidade aprovada.

Registry:
documentary_only.

Etapa 1:
não autorizada.

Alterações operacionais:
nenhuma.
```

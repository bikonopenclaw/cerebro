# Protocolo Experimental C1 v1

## 1. Princípio

A avaliação deve comparar saídas sob condições equivalentes e separar:

- erro de roteamento;
- erro do modelo;
- falha de infraestrutura;
- falha do validador;
- inadequação da própria tarefa.

## 2. Preparação

### 2.1 Congelar versões

Registrar:

```text
controller_version
policy_version
contract_schema_version
registry_version
prompt_version
rubric_version
price_table_version
toolchain_versions
repository_commit
evaluation_set_sha256
```

### 2.2 Provar seleção por chamada

A execução só pode começar se o harness permitir:

- informar modelo por run;
- informar esforço por run;
- capturar modelo efetivo;
- não alterar configuração global;
- não modificar o agente padrão;
- impedir fallback silencioso.

Se a plataforma só permitir trocar configuração global, a Etapa 0.6 fica bloqueada.

### 2.3 Workspaces

Para cada tarefa:

```text
eval/<case_id>/candidate/
eval/<case_id>/reference/
```

Ambos partem do mesmo commit. Cada workspace tem:

- lista de paths permitidos;
- lista de paths proibidos;
- comando de teste;
- estado inicial hash;
- rollback testado.

## 3. Contrato

O pedido original é imutável. O Controlador gera um contrato contendo:

- objetivo normalizado;
- C1;
- R1 ou R2;
- G0 ou G1;
- confiança alta;
- ações permitidas;
- ações proibidas;
- arquivos autorizados;
- critérios de pronto;
- evidências;
- política de falha;
- stop conditions.

A referência e o candidato recebem o mesmo contrato. Somente a resolução de modelo muda.

## 4. Randomização e cegamento

1. Gerar uma seed única e registrá-la.
2. Randomizar qual braço executa primeiro.
3. Gerar aliases de revisão `A` e `B`.
4. Manter o mapa de identidade fora do alcance do revisor.
5. Não permitir que um braço leia logs, diffs ou respostas do outro.
6. Revelar identidades apenas após o score estar congelado.

## 5. Execução

### 5.1 Run válido

Um run é válido quando:

- começa do baseline correto;
- usa o contrato correto;
- modelo efetivo é confirmado;
- reasoning efetivo é registrado;
- telemetria é completa;
- não houve intervenção humana;
- não houve mudança de prompt;
- o fim está claramente registrado.

### 5.2 Retry

Um único retry é permitido somente para:

- timeout de infraestrutura;
- indisponibilidade transitória do provider;
- falha técnica sem saída de modelo utilizável.

Não é permitido retry para:

- teste falhando;
- resposta incompleta;
- decisão errada;
- diff ruim;
- alucinação;
- violação de escopo.

O retry usa exatamente o mesmo contrato e entra na métrica de confiabilidade.

## 6. Validação automática

Executar, nesta ordem:

1. verificar hash do baseline;
2. verificar modelo e contrato;
3. verificar paths proibidos;
4. verificar diff;
5. rodar formatter/linter quando aplicável;
6. rodar testes obrigatórios;
7. validar schema de saída;
8. buscar segredos/canários;
9. validar rollback;
10. gerar pacote de evidência.

Falha em hard gate encerra a validação técnica, mas a evidência é preservada.

## 7. Revisão humana cega

O revisor recebe:

- pedido;
- contrato;
- saída A ou B;
- diff;
- testes;
- evidência sanitizada.

Não recebe:

- modelo;
- custo;
- latência;
- ordem de execução;
- comentário do executor sobre concorrentes.

O score é congelado antes da revelação.

## 8. Reclassificação

Quando fatos novos mostram que a tarefa não era C1:

```yaml
status: reclassification_requested
reason: "..."
new_facts: []
current_safe_state: "..."
proposed_classification:
  capability: "C2|C3"
  reasoning: "R2|R3|R4"
  risk: "G0|G1|G2|G3"
```

Consequências:

- não continuar com o candidato;
- contar como erro de fronteira se a evidência era previsível na entrada;
- contar como descoberta legítima se o fato era oculto e não inferível;
- não incluir o run na qualidade do modelo;
- incluir o evento nas métricas de roteamento.

## 9. Sentinelas

Selecionar:

- 2 tarefas R1;
- 2 tarefas R2;
- pelo menos 2 famílias;
- pelo menos 2 repositórios.

Cada sentinela recebe três runs do candidato. O objetivo é medir:

- estabilidade de hard pass;
- variação de score;
- variação de latência;
- variação de custo;
- inconsistência de escopo;
- sensibilidade a reasoning.

## 10. Evidência por run

Diretório recomendado:

```text
evidence/<run_id>/
  contract.yaml
  request.sha256
  environment.json
  model-resolution.json
  timestamps.json
  usage.json
  stdout.sanitized.log
  stderr.sanitized.log
  diff.patch
  tests.txt
  validation.json
  reviewer-score.yaml
  artifact-manifest.json
```

## 11. Cálculo

### Qualidade

```text
hard_pass_rate = hard_passes / valid_runs
score_delta = candidate_score - reference_score
family_pass_rate = passes_in_family / runs_in_family
```

### Eficiência

```text
cost_ratio = median(candidate_cost) / median(reference_cost)
latency_ratio = median(candidate_latency) / median(reference_latency)
p90_ratio = p90(candidate_latency) / p90(reference_latency)
cost_per_pass = total_cost / hard_passes
```

### Roteamento

```text
false_positive_c1 = casos não C1 admitidos em C1
false_negative_c1 = casos C1 rejeitados
reclassification_rate = reclassifications / eligible_cases
```

## 12. Segurança e retenção

- logs sempre sanitizados;
- nenhum segredo em prompt;
- artefatos reais sensíveis substituídos por fixtures;
- hashes preservados;
- outputs do modelo não executados automaticamente fora do workspace;
- retenção definida antes da execução;
- remoção somente após manifesto e aprovação.

## 13. Fechamento

Ao encerrar:

1. congelar scorecard;
2. revelar mapa A/B;
3. calcular métricas;
4. produzir D1, D2 e D3;
5. gerar patch proposto;
6. verificar que Registry real não mudou;
7. verificar que configuração global não mudou;
8. criar commit local;
9. não fazer push;
10. solicitar decisão humana.

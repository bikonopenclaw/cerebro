# Relatório da Etapa 0.6 — Avaliação C1

> Template normativo. Não preencher antes de congelar a amostra e concluir a execução.

## 1. Controle

- Evaluation set:
- SHA-256:
- Controller version:
- Registry version:
- Contract version:
- Rubric version:
- Price table version:
- Data de início UTC:
- Data de fim UTC:
- Owner:
- Revisor(es):
- Commit local:
- Push: não realizado

## 2. Escopo executado

- Tarefas elegíveis:
- Casos de fronteira:
- Runs candidato:
- Runs referência:
- Repetições sentinela:
- Runs inválidos:
- Motivos de invalidação:

## 3. Integridade

| Verificação | Resultado | Evidência |
|---|---|---|
| 24 tarefas reais | | |
| 8 fronteiras | | |
| independência | | |
| contratos com hash | | |
| telemetria completa | | |
| modelo efetivo confirmado | | |
| zero mudança global | | |
| zero ação externa | | |
| zero segredo | | |
| cegamento preservado | | |

## 4. Parecer D1 — Taxonomia C1

- B01–B08 rejeitados:
- Falsos positivos C1:
- Falsos negativos C1:
- Reclassificações:
- G2/G3 admitidos:
- Ampliações de autorização:
- Resultado D1:
- Justificativa:

## 5. Parecer D2 — Candidato Spark

### 5.1 Qualidade

| Métrica | Candidato | Referência | Gate |
|---|---:|---:|---|
| Hard passes | | | candidato ≥22/24 |
| Hard pass rate | | | |
| Score mediano | | | candidato ≥85 |
| Delta mediano | | | ≥−5 |
| Defeitos maiores | | | |
| Defeitos menores | | | |
| Famílias ≥3/4 | | | 6/6 |
| Sentinelas hard pass | | N/A | ≥11/12 |

### 5.2 Eficiência

| Métrica | Candidato | Referência | Razão | Gate |
|---|---:|---:|---:|---|
| Custo mediano | | | | ≤0,80 |
| Latência mediana | | | | ≤0,80 |
| Latência p90 | | | | ≤1,10 |
| Tool calls | | | | ≤1,25 |
| Custo por hard pass | | | | informativo |

### 5.3 Reprodutibilidade

- Modelo solicitado:
- Modelo efetivo:
- Snapshot/fingerprint:
- Mapeamento R1:
- Mapeamento R2:
- Owner:
- Eval set versionado:
- Limitações:

### 5.4 Resultado D2

- Resultado:
- Capacidade proposta:
- Reasoning permitido:
- Riscos permitidos:
- Famílias permitidas:
- Exclusões:
- Promoção aplicada: não
- Aprovação pendente:

## 6. Parecer D3 — Shadow mode

| Critério | Resultado |
|---|---|
| Gate A | |
| Gate B | |
| contratos válidos | |
| rollback simulado | |
| resolução advisory | |
| justificativa reproduzível | |
| owner e monitoramento | |

- Resultado D3:
- Limitações:
- Recomendação:

## 7. Falhas e reclassificações

| Case ID | Arm | Tipo | Causa | Contagem | Impacto |
|---|---|---|---|---:|---|

## 8. Resultado por família

| Família | R | G | Candidate pass | Reference pass | Score delta | Cost ratio | Latency ratio | Decisão |
|---|---|---|---:|---:|---:|---:|---:|---|

## 9. Decisão final

Marcar uma opção:

- [ ] `promotion_proposed`
- [ ] `evaluation_passed_alias_unresolved`
- [ ] `restricted_subset_proposed`
- [ ] `remain_candidate`
- [ ] `disabled_pending_review`
- [ ] `inconclusive`
- [ ] `stage_invalid`

## 10. Registry

- Registry real alterado: não
- Patch proposto:
- Snapshot confirmado:
- Activation authorized: false
- Critical route allowed: false

## 11. Etapa 1

- Etapa 1 autorizada: não
- Shadow readiness:
- Condições pendentes:
- Aprovação solicitada:

## 12. Garantias

- Nenhum modelo padrão alterado.
- Nenhum gateway, cron, agente ou produção alterado.
- Nenhuma rota automática ativada.
- Nenhum fallback silencioso.
- Nenhum push sem autorização.

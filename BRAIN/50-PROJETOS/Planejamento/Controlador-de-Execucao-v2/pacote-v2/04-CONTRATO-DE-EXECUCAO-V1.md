# Contrato de Execução v1

## Objetivo

Definir a interface formal entre Controlador, Executor e Validador.

## Schema canônico

```yaml
schema_version: "1.0"
task_id: "tsk_<utc>_<id>"
parent_task_id: null
created_at_utc: "YYYY-MM-DDTHH:MM:SSZ"
request:
  original: "texto imutável"
  original_sha256: "..."
  normalized_objective: "resultado a alcançar"
  context: "contexto relevante"
  inputs: []
  expected_outputs: []
classification:
  execution_type: "deterministic|llm"
  capability: "C0|C1|C2|C3|C4|C5"
  reasoning: "R0|R1|R2|R3|R4|R5"
  risk: "G0|G1|G2|G3"
  confidence: "high|medium|low"
  rationale: []
model_resolution:
  registry_version: "1"
  model_id: null
  model_snapshot: null
  reasoning_effort: null
  reasoning_mode: "standard"
  execution_mode: "single|parallel"
  fallback_policy: "stop_and_escalate"
authorization:
  allowed_actions: []
  forbidden_actions: []
  conditional_actions: []
  approval_required: false
  approval_reference: null
execution:
  executor: "agent-or-tool"
  tools_allowed: []
  files_or_systems_allowed: []
  max_parallel_workstreams: 1
  cost_ceiling: null
  latency_target: null
  timeout_policy: "bounded"
validation:
  done_criteria: []
  evidence_required: []
  validators: []
  rollback_required: false
  rollback_plan: null
failure_policy:
  on_missing_input: "partial_and_report|stop"
  on_tool_failure: "retry_bounded|escalate|stop"
  on_scope_change: "request_reclassification"
  on_gate_failure: "stop_safe_state"
  on_model_failure: "stop_and_escalate"
executor_brief: |
  Texto amigável e operacional para o agente.
audit:
  controller_version: "..."
  policy_version: "..."
  decision_trace_id: "..."
```

## Regras de preenchimento

- `original` é imutável.
- `normalized_objective` descreve resultado, não método inventado.
- C0 exige `model_id: null` e R0.
- G3 exige aprovação explícita quando houver efeito real, além de rollback e evidência.
- `allowed_actions` é uma lista fechada.
- Ações não listadas não são automaticamente permitidas.
- `executor_brief` não pode contradizer campos estruturados; em conflito, o schema prevalece.

## Template do brief amigável

```text
OBJETIVO
[resultado final]

CONTEXTO
[por que e para quem]

ENTRADAS AUTORIZADAS
[fontes, arquivos e sistemas]

ESCOPO
[ações permitidas]

FORA DO ESCOPO
[ações proibidas e condicionais]

CRITÉRIOS DE PRONTO
[checks objetivos]

EVIDÊNCIAS OBRIGATÓRIAS
[logs, hashes, fontes, testes]

POLÍTICA DE FALHA
[o que fazer em erro, lacuna ou divergência]

SAÍDA ESPERADA
[formato e localização]
```

## Resposta do executor

O executor deve devolver:

```yaml
status: "completed|partial|blocked|failed|reclassification_requested"
summary: "..."
outputs: []
evidence: []
changes_made: []
changes_not_made: []
validation_results: []
new_facts: []
current_safe_state: "..."
reclassification_request: null
```

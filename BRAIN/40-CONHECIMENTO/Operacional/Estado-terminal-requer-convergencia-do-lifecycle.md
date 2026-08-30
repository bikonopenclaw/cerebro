# Estado terminal requer convergencia do lifecycle

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W35
confiabilidade: alta
ultima_revisao: 2026-08-30
tags: [lifecycle, execucao, registry, cgroup, terminalidade, reconciliacao]
```

## Principio

Uma execucao so e terminal quando fila, admissao, registry, child, processo fisico e evidencias persistidas convergem para a mesma identidade e para um unico resultado. Estado terminal em apenas uma camada nao prova encerramento do workload.

## Aplicacao pratica

- Criar a identidade duravel antes do child ou do processo fisico.
- Registrar transicoes `accepted -> admitted/deferred -> spawned -> bootstrapped -> workload_started -> output_committed -> terminal`.
- Vincular fila, registry, PID, unit/tmux, cgroup e checkpoint ao mesmo execution ID.
- Considerar terminalidade invalida quando o cgroup canonico ainda possui processo vivo, os bytes continuam mudando ou falta reconciliacao do output.
- Preservar historico factual: lease expirada ou admissao stale nao deve ser reescrita como cancelamento que nao ocorreu.
- Depois de perda de sessao ou gateway, reconciliar a mesma execucao; nao criar retry concorrente por ausencia de observador.

## Exemplo conectado

Em 2026-W35, RSE, ODP/B1 e o P1 de Relatorios Operacionais mostraram o mesmo defeito: child criado antes da admissao, caller bloqueado em espera e perda da sessao sem convergencia com registry e processo fisico. A retomada ficou bloqueada ate existir lifecycle canonico e prova terminal compartilhada.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|Ausencia de evidencia nao e status operacional]]
- [[40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel|Contrato de runtime reprodutivel]]
- [[40-CONHECIMENTO/Operacional/Governanca-de-capacidade-nao-e-roteamento-semantico|Governanca de capacidade nao e roteamento semantico]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-RSE|OpenClaw RSE]]
- [[01-DIARIO/Semanal/2026-W35|Semana 2026-W35]]

# Controlador de Execução v2

```yaml
status: etapa_0_6_desenhada_nao_executada
implementacao: nao_autorizada
roteamento_automatico: desativado
ultima_revisao: 2026-07-24
responsavel: Puppet Master
```

## Escopo

Este diretório é o equivalente versionado de `docs/workflows/controller/`.

A v2 substitui documentalmente o Roteador de Execução v1, sem apagar a evidência histórica. Nenhum modelo, nível de pensamento, agente, cron, skill, gateway, configuração ou produção foi alterado.

## Estrutura

### Histórico v1 preservado

- [Plano v1](historico-v1/PLANO-ROTEADOR-EXECUCAO-V1.md)
- [Baseline v1](historico-v1/BASELINE-40-TAREFAS.csv)
- [Matriz v0](historico-v1/MATRIZ-ROTEAMENTO-V0.md)
- [Casos de teste v0](historico-v1/CASOS-TESTE-V0.md)
- [Resumo da Etapa 0](historico-v1/RESUMO-ETAPA-0.md)

Os cinco arquivos foram copiados antes da marcação de supersession no artefato operacional e mantêm os hashes originais.

### Pacote v2 recebido

- [Instruções](pacote-v2/00-LEIA-ME-PARA-O-AGENTE.md)
- [Plano v2](pacote-v2/01-PLANO-CONTROLADOR-EXECUCAO-V2.md)
- [Especificação](pacote-v2/02-SPEC-CONTROLADOR-EXECUCAO-V1.md)
- [Registry proposto](pacote-v2/03-MODEL-REGISTRY-V1.md)
- [Contrato de execução](pacote-v2/04-CONTRATO-DE-EXECUCAO-V1.md)
- [Matriz de capacidades](pacote-v2/05-MATRIZ-CAPACIDADES-V1.md)
- [Casos de teste](pacote-v2/06-CASOS-TESTE-CONTROLADOR-V1.md)
- [Baseline v2](pacote-v2/07-BASELINE-40-TAREFAS-V2.csv)
- [Relatório proposto da Etapa 0.5](pacote-v2/08-RELATORIO-ETAPA-0.5.md)
- [Changelog v2](pacote-v2/09-CHANGELOG-V2.md)
- [Manifesto do pacote](pacote-v2/MANIFEST.json)

### Resultado operacional read-only

- [Registry confirmado do ambiente](operacional/MODEL-REGISTRY-OPERACIONAL-V1.yaml)
- [Baseline operacional corrigida](operacional/BASELINE-40-TAREFAS-V2.csv)
- [Casos de teste operacionais corrigidos](operacional/CASOS-TESTE-CONTROLADOR-V1.md)
- [Relatório pré-aprovação, superseded](operacional/RELATORIO-ETAPA-0.5-PRE-APROVACAO.md)
- [Relatório validado vigente](operacional/RELATORIO-ETAPA-0.5-VALIDADO.md)

O conteúdo de `pacote-v2/` permanece imutável como evidência recebida. As cópias em `operacional/` são a referência vigente para a Etapa 0.5.

### Desenho documental da Etapa 0.6

- [Instruções do pacote](etapa-0.6/00-LEIA-ME-PARA-O-AGENTE.md)
- [Plano da avaliação C1](etapa-0.6/10-PLANO-ETAPA-0.6-AVALIACAO-C1-V1.md)
- [Protocolo experimental](etapa-0.6/11-PROTOCOLO-EXPERIMENTAL-C1-V1.md)
- [Casos de fronteira](etapa-0.6/12-CASOS-FRONTEIRA-C1-V1.md)
- [Template do relatório](etapa-0.6/13-RELATORIO-ETAPA-0.6-TEMPLATE.md)
- [Patch de Registry proposto e não aplicado](etapa-0.6/14-PATCH-MODEL-REGISTRY-PROPOSTO.yaml)
- [Instrução de execução bloqueada](etapa-0.6/15-INSTRUCAO-DE-EXECUCAO-PARA-O-AGENTE.md)
- [Scorecard C1](etapa-0.6/ETAPA-0.6-SCORECARD-C1-V1.xlsx)
- [Manifesto da Etapa 0.6](etapa-0.6/MANIFEST.json)

Os nove arquivos foram incorporados sem modificação. Os oito artefatos relacionados no manifesto mantêm seus hashes SHA-256 originais.

## Estado decisório

- Etapa 0.5 documental executada.
- Nove correções C/R/G foram aprovadas por Hebert em `2026-07-23T22:07:42Z` e aplicadas às cópias operacionais.
- A baseline separa estado de validação, origem da classificação e horário de aprovação.
- Há 38 casos `confirmed` e 2 `candidate`, IDs 27 e 28, por ausência de evidência histórica local.
- Registry criado somente com modelos configurados ou observados no ambiente.
- Etapa 0.6 desenhada, mas não executada.
- Avaliação C1 bloqueada até nova autorização explícita.
- Spark permanece `candidate`, sem capacidades aprovadas.
- Patch de Registry permanece `not_applied`, com `activation_authorized: false`.
- Nenhuma das 24 tarefas elegíveis, 8 fronteiras ou 56 runs planejados foi executada.
- Etapa 1 e roteamento automático continuam não autorizados.

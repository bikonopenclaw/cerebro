# Relatório da Etapa 0.5 — Proposta de Reclassificação

## Estado

Documento preenchido a partir da baseline histórica de 40 tarefas. A reclassificação é uma proposta read-only e ainda precisa ser revisada pelo agente com as evidências originais antes de servir como ground truth.

## Resultado proposto

| Capacidade | Quantidade |
|---|---:|
| C0 | 8 |
| C2 | 14 |
| C3 | 18 |

## Distribuição de risco

| Risco | Quantidade |
|---|---:|
| G0 | 27 |
| G1 | 2 |
| G2 | 5 |
| G3 | 6 |

## Aprendizados

1. Oito tarefas permanecem C0: a maior economia vem de não chamar LLM, não de escolher um modelo menor.
2. Casos anteriormente rotulados como “max” foram separados entre dificuldade e risco. Exemplo: remover crons pendentes é G3, mas não exige automaticamente R5.
3. Nenhum dos 40 casos fornece evidência suficiente para C4 ou C5.
4. C1 continua sem amostra técnica independente suficiente; não foi atribuído na baseline proposta.
5. O modelo concreto ficou como N/D até o Registry passar pelas avaliações.

## Pendências antes do shadow mode

- revisar cada linha contra a evidência original;
- coletar subamostra de código, patch e script para C1;
- instrumentar timestamps, custo e reabertura;
- executar EVAL-C1-TECH, EVAL-C2-PRO, EVAL-C3-DEEP e EVAL-G3-SAFETY;
- aprovar snapshots concretos no Registry;
- definir owner e rollback global;
- atualizar os casos quando houver divergência confirmada.

## Recomendação

Não automatizar a troca de modelo. Autorizar apenas shadow mode depois da revisão da Etapa 0.5. O controlador deve registrar a recomendação, mas o executor continua usando a rota vigente até aprovação explícita.

# Instrução de Execução da Etapa 0.6 para o Agente

> Estado: bloqueada até autorização explícita. Este texto é uma ordem pronta para uso futuro; não execute por estar presente no repositório.

## Objetivo

Executar a Etapa 0.6 — Avaliação C1 exatamente conforme:

- `10-PLANO-ETAPA-0.6-AVALIACAO-C1-V1.md`;
- `11-PROTOCOLO-EXPERIMENTAL-C1-V1.md`;
- `12-CASOS-FRONTEIRA-C1-V1.md`;
- `ETAPA-0.6-SCORECARD-C1-V1.xlsx`.

## Autorização necessária

Antes de iniciar, registrar:

```text
approved_by
approved_at_utc
budget_ceiling
owner
blind_reviewer
repositories_allowed
retention_policy
per_call_model_override_confirmed
rollback_command
```

Na ausência de qualquer campo, parar.

## Restrições

- Não alterar configuração global de modelo.
- Não alterar agentes, gateway, cron, skills ou produção.
- Não usar G2 ou G3.
- Não usar segredos reais.
- Não publicar ou enviar.
- Não fazer fallback silencioso.
- Não trocar tarefas após observar resultados.
- Não aplicar patch do Registry.
- Não ativar Etapa 1.
- Não fazer push.

## Sequência

1. Executar preflight.
2. Congelar 24 tarefas e 8 fronteiras.
3. Gerar hashes do evaluation set.
4. Gerar contratos.
5. Criar worktrees isolados.
6. Executar 48 runs pareados.
7. Executar 8 repetições sentinela.
8. Validar e cegar resultados.
9. Calcular métricas.
10. Emitir D1, D2 e D3.
11. Gerar relatório e patch proposto.
12. Confirmar que Registry e configuração global permaneceram intactos.
13. Criar commit local:

```text
eval: complete etapa 0.6 c1 assessment
```

14. Não fazer push.
15. Solicitar aprovação humana.

## Stop conditions

Parar imediatamente em qualquer condição listada no plano, inclusive segredo, ação externa, perda de isolamento, mudança global, fallback silencioso, G2/G3 ou telemetria insuficiente.

## Saída final

Informar:

- commit local;
- hash do evaluation set;
- total de runs;
- hard passes;
- custo e latência;
- D1, D2 e D3;
- Registry alterado: não;
- Etapa 1 ativada: não;
- push: não.

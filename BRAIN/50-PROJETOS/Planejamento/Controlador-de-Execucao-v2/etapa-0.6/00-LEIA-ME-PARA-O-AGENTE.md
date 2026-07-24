# Etapa 0.6 — Avaliação C1

## Finalidade deste pacote

Este pacote desenha a Etapa 0.6 do Controlador de Execução v2. Ele não executa a avaliação, não altera o Registry, não troca modelos e não autoriza a Etapa 1.

A Etapa 0.6 existe para responder, de forma separada, a três perguntas:

1. A fronteira da capacidade C1 está suficientemente bem definida para ser aplicada de forma segura?
2. O candidato `openai/gpt-5.3-codex-spark` entrega qualidade adequada em C1/R1–R2, com ganho material de custo e latência?
3. O Controlador está pronto para entrar em shadow mode sem mudar a execução real?

As respostas podem ser diferentes. Um modelo pode passar em qualidade e continuar sem promoção por falta de snapshot reproduzível. Da mesma forma, o Controlador pode estar pronto para shadow mode mesmo que nenhum modelo C1 seja promovido.

## Estado

- Desenho documental: concluído.
- Execução: não autorizada.
- Chamadas de modelo: não autorizadas por este pacote.
- Gasto: não autorizado por este pacote.
- Alteração de modelo, agente, gateway, cron ou produção: proibida.
- Etapa 1: não autorizada.
- Registry: permanece `documentary_only`.
- Candidato primário: `openai/gpt-5.3-codex-spark`, ainda `candidate`.
- Referência comparativa: `openai/gpt-5.5`, apenas como rota incumbente observada; não é ground truth nem modelo validado.

## Arquivos

1. `10-PLANO-ETAPA-0.6-AVALIACAO-C1-V1.md` — desenho executivo, gates e decisão.
2. `11-PROTOCOLO-EXPERIMENTAL-C1-V1.md` — procedimento operacional reproduzível.
3. `12-CASOS-FRONTEIRA-C1-V1.md` — casos negativos que nunca devem entrar em C1.
4. `13-RELATORIO-ETAPA-0.6-TEMPLATE.md` — estrutura do relatório final.
5. `14-PATCH-MODEL-REGISTRY-PROPOSTO.yaml` — patch condicional, não aplicável sem aprovação.
6. `15-INSTRUCAO-DE-EXECUCAO-PARA-O-AGENTE.md` — ordem operacional pronta, ainda bloqueada.
7. `ETAPA-0.6-SCORECARD-C1-V1.xlsx` — catálogo da amostra, plano de runs, scorecard e rubrica.
8. `MANIFEST.json` — hashes SHA-256 do pacote.

## Incorporação documental recomendada

Salvar em:

```text
docs/controller/etapa-0.6/
```

Preservar:

- artefatos v1;
- pacote original do Controlador v2;
- baseline 40×28 validada;
- casos 27 e 28 como `candidate`;
- Registry operacional atual;
- commits locais já existentes.

Commit documental recomendado:

```text
docs: design etapa 0.6 c1 evaluation
```

Não fazer push sem autorização.

## Regra crítica

Este pacote não autoriza executar a avaliação. Para executar, ainda são necessários:

- aprovação explícita da Etapa 0.6;
- orçamento total;
- owner da avaliação;
- revisor cego;
- repositórios e tarefas reais elegíveis;
- mecanismo por chamada para escolher modelo e esforço sem alterar configuração global;
- telemetria de custo, latência e modelo efetivo;
- worktrees isolados e rollback testado.

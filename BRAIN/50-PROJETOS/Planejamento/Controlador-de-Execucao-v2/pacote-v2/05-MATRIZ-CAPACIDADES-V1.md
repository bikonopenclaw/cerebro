# Matriz de Capacidades v1

## Matriz principal

| Condição | Capacidade | Esforço inicial | Risco típico | Observação |
|---|---|---|---|---|
| Procedimento fixo e resultado objetivo | C0 | R0 | G0–G3 | risco define gates, não uso de LLM |
| Extração, triagem, transformação simples | C1 | R1–R2 | G0–G1 | exige alta confiança e avaliação aprovada |
| Relatório, documento, síntese moderada | C2 | R2–R3 | G0–G2 | porto seguro profissional |
| Arquitetura, integração, diagnóstico difícil | C3 | R3–R4 | G0–G3 | gates independentes |
| Problema intelectual de fronteira | C4 | R4–R5 | qualquer | somente com ganho medido sobre C3 |
| Duas ou mais frentes independentes | C5 | conforme frente | qualquer | modo paralelo, não escala de inteligência |

## Esforço lógico

| Nível | Uso |
|---|---|
| R0 | sem LLM ou resposta direta determinística |
| R1 | classificação e transformação simples |
| R2 | tarefa profissional conhecida e balanceada |
| R3 | análise aprofundada, múltiplas fontes ou ferramentas |
| R4 | alta ambiguidade, arquitetura ou verificação intensiva |
| R5 | casos mais difíceis, qualidade acima de custo/latência, com avaliação que justifique |

## Risco operacional

| Nível | Definição | Gates mínimos |
|---|---|---|
| G0 | leitura ou produção de artefato sem efeito externo | validação e evidência |
| G1 | mudança reversível e localizada | diff/teste/rollback simples |
| G2 | impacto moderado, múltiplos sistemas ou comunicação externa controlada | aprovação conforme política, rollback e revisão |
| G3 | produção, root, banco, pagamento, emissão fiscal, credencial, segurança, P1/P2 ou perda de dados | aprovação explícita, backup, rollback, owner, parada segura e validação pós-ação |

## Árvore decisória

1. A tarefa inteira é determinística? C0/R0.
2. Há efeito externo ou risco? Classificar G0–G3 e gates.
3. A tarefa é fechada, conhecida e simples? C1.
4. É trabalho profissional com julgamento moderado? C2.
5. Há novidade, integração, causa raiz ou ambiguidade alta? C3.
6. Avaliações mostram ganho material de fronteira? C4.
7. Existem frentes independentes e ganho comprovável? C5.
8. Resolver modelo no Registry.

## Regras contra erros comuns

- G3 não implica R5.
- R5 não implica G3.
- C5 não implica modelo mais caro em todas as frentes.
- modelo forte não substitui aprovação, backup ou rollback.
- latência baixa não autoriza C1 sem evidência.
- confiança baixa bloqueia rebaixamento automático.

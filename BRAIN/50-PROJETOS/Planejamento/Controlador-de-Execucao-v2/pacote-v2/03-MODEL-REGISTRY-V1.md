# Registro de Modelos v1

## Controle

- Data da fotografia: 2026-07-23
- Estado: inicial, candidato à validação na Etapa 0.5
- Fonte de verdade permanente: este arquivo para resolução operacional; documentação oficial do fornecedor para capacidades declaradas
- Regra: nomes concretos nunca aparecem nas regras permanentes do controlador

## Estados

- `candidate`: disponível, mas ainda não aprovado para produção;
- `validated`: aprovado em avaliações internas definidas;
- `restricted`: uso limitado a classes ou gates específicos;
- `disabled`: indisponível ou reprovado;
- `deprecated`: mantido apenas por compatibilidade e migração.

## Registro inicial

| model_id | fornecedor | status inicial | capacidades candidatas | esforços declarados | uso preferencial | rota crítica |
|---|---|---|---|---|---|---|
| gpt-5.6-luna | OpenAI | candidate | C1, C2 limitado | none, low, medium, high, xhigh, max* | alto volume, baixa latência, rotinas estruturadas | não, até validação |
| gpt-5.6-terra | OpenAI | candidate | C2, C3 | none, low, medium, high, xhigh, max* | equilíbrio qualidade/custo | somente após avaliação G2/G3 |
| gpt-5.6-sol | OpenAI | candidate | C2, C3, C4, C5 | none, low, medium, high, xhigh, max | fronteira, arquitetura, diagnóstico e coordenação | candidato, nunca substitui gates |
| gpt-5.6 | OpenAI | restricted | alias para Sol na fotografia atual | conforme resolução | conveniência; evitar em auditoria reprodutível | não usar sem snapshot |
| gpt-5.3-codex | OpenAI | candidate | C1, C2, C3 técnico | conforme documentação do snapshot | código e tarefas agentic | somente após suíte técnica |
| gpt-5.3-codex-spark | OpenAI | candidate | C1 técnico | medium, high conforme ambiente observado | patches fechados e scripts conhecidos | não |

`*` O suporte exato deve ser confirmado por chamada de capabilities ou documentação do snapshot antes da ativação. O controlador não deve assumir uniformidade entre variantes.

## Requisitos mínimos por capacidade

| Capacidade | Requisitos mínimos do modelo |
|---|---|
| C1 | saída estruturada confiável, baixa latência, tool use básico, avaliações de rotina |
| C2 | síntese multi-fonte, boa aderência a instruções, ferramentas, documentos profissionais |
| C3 | raciocínio complexo, código/arquitetura, integração, contexto amplo, ferramentas robustas |
| C4 | melhor desempenho validado em avaliações difíceis, verificação intensiva e confiabilidade superior |
| C5 | coordenação de subagentes ou suporte de orquestração, consolidação e isolamento de frentes |

## Política de resolução

1. Preferir snapshots fixos em produção e aliases somente em experimentos controlados.
2. Filtrar por capacidade e gates antes de custo.
3. Entre candidatos equivalentes, escolher menor custo total esperado, não menor preço por token isolado.
4. `reasoning.effort` é escolhido pelo controlador e traduzido pelo adapter do modelo.
5. `reasoning.mode=pro` é um modo separado, permitido apenas quando avaliações demonstrarem ganho.
6. Multiagente é um modo separado e só pode ser acionado para C5.
7. Fast mode ou prioridade de processamento não altera capacidade nem autorização.

## Avaliações necessárias

| eval_set | objetivo | promoção permitida |
|---|---|---|
| EVAL-C1-TECH | patches, scripts, testes e rollback simples | candidate → validated para C1 técnico |
| EVAL-C2-PRO | relatórios, financeiro em leitura, documentos e comunicação | candidate → validated para C2 |
| EVAL-C3-DEEP | arquitetura, integração, diagnóstico e causa raiz | candidate → validated para C3 |
| EVAL-C4-FRONTIER | casos onde C3 falha ou perde qualidade | candidate → validated para C4 |
| EVAL-G3-SAFETY | preservação de gates, parada e rollback | permissão restrita em G3 |
| EVAL-C5-PARALLEL | decomposição, owners e consolidação | permissão para C5 |

## Registro de decisão por modelo

Cada ativação deve registrar: snapshot, data, owner, capacidades aprovadas, esforços testados, preço de referência, latência p50/p95, taxa de sucesso, falhas conhecidas, classes proibidas e data da próxima revisão.

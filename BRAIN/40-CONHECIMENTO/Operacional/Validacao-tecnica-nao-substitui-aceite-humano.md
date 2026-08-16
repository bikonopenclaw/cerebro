# Validacao tecnica nao substitui aceite humano

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W33
confiabilidade: alta
ultima_revisao: 2026-08-16
tags: [aceite, validacao, fail-closed, provimento-213, fip, kowalski]
```

## Principio

Teste automatizado, hash, manifesto, rota `200`, Kowalski `PASS` ou suite completa provam somente a dimensao tecnica que foi exercitada. Quando o gate definido e visual, humano, semantico, financeiro ou de verdade canonica, a aceitacao continua bloqueada ate a evidencia propria desse gate existir.

Validacao tecnica reduz risco, mas nao muda o criterio de aceite.

## Aplicacao pratica

- Declarar qual dimensao cada gate valida: tecnica, visual, semantica, financeira, canonica ou humana.
- Manter `FAIL_CLOSED` quando a suite passa, mas o gate humano/visual ainda nao foi executado.
- Separar "pronto tecnicamente" de "aceito operacionalmente".
- Registrar quem ou qual evidencia autoriza a promocao final.
- Nao substituir reteste em dispositivo real, revisao de PDF, reconciliacao de corpus ou aceite de Project Owner por resumo tecnico.

## Exemplo conectado

Na semana 2026-W33, o Mini App e a composicao visual do Provimento 213 passaram em testes, rotas, Kowalski e pureza read-only, mas permaneceram bloqueados ate reteste real do iPhone do Project Owner. O PDF Alzira tambem exigiu aceite semantico apos corrigir o falso `100%`.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Commit-de-estado-nao-e-aceitacao-operacional|Commit de estado nao e aceitacao operacional]]
- [[40-CONHECIMENTO/Operacional/Contagem-nao-e-percentual-de-conclusao|Contagem nao e percentual de conclusao]]
- [[01-DIARIO/Semanal/2026-W33|Semana 2026-W33]]

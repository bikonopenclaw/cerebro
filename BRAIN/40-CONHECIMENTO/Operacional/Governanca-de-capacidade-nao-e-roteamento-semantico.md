# Governanca de capacidade nao e roteamento semantico

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W34
confiabilidade: alta
ultima_revisao: 2026-08-23
tags: [capacidade, roteamento, rse, puppet, admissao, governanca]
```

## Principio

Governanca de capacidade decide se uma execucao cabe agora, deve esperar ou deve ser rejeitada por pressao operacional. Ela nao decide a intencao da tarefa nem reclassifica seu significado.

A autoridade de classificacao semantica deve permanecer separada da autoridade de admissao por recursos.

## Aplicacao pratica

- Puppet ou owner equivalente classifica intencao, risco, foreground/background e escopo.
- RSE ou camada de capacidade consome perfil de recurso e decide admissao, deferral, fila, pressao e reserva atomica.
- Pressao operacional pode bloquear trabalho caro, mas nao deve transformar tarefa, dominio ou autorizacao.
- Uma decisao de capacidade `PASS` nao amplia permissoes mutativas nem substitui approval de superficie.
- Logs devem registrar classificacao recebida, decisao de capacidade e razao de deferral/rejeicao sem reinterpretar o pedido.

## Exemplo conectado

Em 2026-W34, [[50-PROJETOS/Em-Andamento/OpenClaw-RSE|OpenClaw RSE]] fechou Capacity-Aware Execution Governance v1 como `PASS`. O contrato canonico preservou Puppet como dono de intencao/classificacao e RSE como autoridade de admissao, fila, pressao, headroom e reserva atomica.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Producao-parcial-por-dominio-nao-herda-autorizacao|Producao parcial por dominio nao herda autorizacao]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-RSE|OpenClaw RSE]]
- [[01-DIARIO/Semanal/2026-W34|Semana 2026-W34]]

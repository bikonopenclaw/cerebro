# Inventario de capacidades nao autoriza uso operacional

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W35
confiabilidade: alta
ultima_revisao: 2026-08-30
tags: [capacidades, registry, provider, autorizacao, read-only, mutacao]
```

## Principio

Descobrir e autenticar capacidades de um provider melhora o mapa de decisao, mas nao autoriza executar essas capacidades. Suporte tecnico, implementacao existente, permissao de credencial e autoridade operacional sao dimensoes separadas.

## Aplicacao pratica

- Separar capacidades de leitura, mutativas, implementadas, parciais e nao implementadas.
- Marcar mutacoes owner-gated mesmo quando o provider e a credencial as suportam.
- Priorizar backlog read-only com prova de nao mutacao.
- Exigir alvo seguro, approval proprio, idempotencia, limite, rollback e evidencia terminal para cada canario mutativo.
- Nao converter contagem total de capacidades em percentual de prontidao ou permissao herdada.

## Exemplo conectado

Em 2026-W35, o Sentinel autenticou `374` capacidades em cinco providers, incluindo `189` mutativas, e terminou Phase D com zero mutacao. O registry passou a servir como mapa de backlog; Phase E e uso real permaneceram bloqueados por approvals proprios.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[40-CONHECIMENTO/Operacional/Capacidade-tecnica-nao-substitui-evidencia-de-ambiente|Capacidade tecnica nao substitui evidencia de ambiente]]
- [[40-CONHECIMENTO/Operacional/Contagem-nao-e-percentual-de-conclusao|Contagem nao e percentual de conclusao]]
- [[60-AGENTES/SENTINEL|Sentinel]]
- [[01-DIARIO/Semanal/2026-W35|Semana 2026-W35]]

# Menor privilégio em monitoramento

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W29
confiabilidade: alta
ultima_revisao: 2026-07-17
tags: [monitoramento, menor-privilegio, read-only, allowlist, auditoria, revogacao]
```

## Princípio

Monitorar não exige poder de remediar. Agentes de observabilidade devem receber somente a leitura necessária, por clientes tipados e allowlists verificáveis, com saída sanitizada e revogação testável.

## Requisitos

- Fonte e operação explicitamente autorizadas.
- Cliente read-only sem URL, método, comando ou caminho arbitrário.
- Segredo fora do Brain/Git e permissão local restrita.
- Saída mínima, sem resposta bruta, credencial ou dado pessoal desnecessário.
- Auditoria append-only com ator, fonte, operação, horário UTC, resultado, correlação e hash do cliente.
- Falha de auditoria bloqueia a consulta.
- Revogação no provedor seguida de prova pela mesma rota aprovada.

## Limite de credencial compartilhada

Um wrapper read-only reduz risco operacional, mas não transforma uma credencial ampla em credencial de privilégio mínimo. Quando o provedor permitir, a solução correta é criar identidade exclusiva com escopo somente leitura. Até lá, a limitação deve permanecer documentada e revisada.

## Relações

- `BRAIN/60-AGENTES/SENTINEL.md`
- `BRAIN/60-AGENTES/versionados/workspaces/sentinel/access_control/REVOGACAO.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional.md`

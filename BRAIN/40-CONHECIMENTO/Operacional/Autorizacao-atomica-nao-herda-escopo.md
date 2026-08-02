# Autorizacao atomica nao herda escopo

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W31
confiabilidade: alta
ultima_revisao: 2026-08-02
tags: [approval, checkpoints, escopo, governanca, fail-closed, provimento-213]
```

## Principio

Autorizacao operacional deve ser atomica. Um approval, checkpoint, commit, hash, validacao independente ou publicacao comprova somente o escopo exato que foi autorizado e executado.

Nenhuma evidencia tecnica herda permissao para a proxima etapa.

## Aplicacao pratica

- Separar documento, implementacao, commit, push/publicacao, homologacao, deploy, recorrencia e rollback.
- Usar cada `approval_id` e `execution_id` apenas para a unidade autorizada.
- Tratar ordem terminal como encerrada; falha, timeout ou sucesso parcial nao autorizam reuso.
- Antes de continuar, declarar o novo impacto, os limites e o rollback da proxima unidade.
- Quando faltar evidencia completa, manter bloqueado em vez de reconstruir estado por resumo, memoria ou hash isolado.

## Exemplo conectado

Na semana 2026-W31, o OpenClaw - Provimento 213 teve EPs documentais, commits, hashes, validacoes independentes e publicacao canonica. Esses marcos nao autorizaram provider, target, preflight, restore, contato externo, envio de PDF, deploy ou recorrencia.

## Relacoes

- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
- `BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md`
- `BRAIN/01-DIARIO/Semanal/2026-W31.md`

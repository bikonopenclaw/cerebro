# Boundary de escrita em delegacao de engenharia

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao diaria 2026-08-07; reforco semanal 2026-W32
confiabilidade: alta
ultima_revisao: 2026-08-09
tags: [edc, codex, sandbox, writable-roots, fail-closed, validacao]
```

## Principio

Delegacao de engenharia com permissao de escrita so e aceitavel quando os writable roots autorizados forem explicitamente declarados e a persistencia real pos-execucao provar que nada foi criado, alterado ou mantido fora desses roots.

Sandbox preflight, schema valido e exit code `0` nao bastam para aceitar a tarefa.

## Aplicacao pratica

- Congelar os writable roots por tarefa, nao por projeto inteiro.
- Validar antes e depois: hashes de targets, lista de arquivos, diretorios novos, caches, artefatos de teste e estado persistido.
- Tratar qualquer arquivo fora do boundary como `FAIL_CLOSED`, mesmo que a mudanca funcional principal pareca correta.
- Nao aceitar baseline, pacote ou resultado tecnico quando houver side effect fora do boundary.
- Preservar evidencia de violacao ate haver autorizacao explicita para limpeza ou retry.
- Revalidar o estado persistido depois de cada rodada, porque alinhamento de schema e piloto read-only nao provam enforcement de escrita.

## Exemplo conectado

Em 2026-08-07, a primeira delegacao EDC para implementar o CPIW V4 Production Apply Adapter executou Codex e produziu mudancas preliminares dentro dos roots autorizados, mas tambem persistiu artefatos fora do boundary. A rodada foi invalidada como `CODEX_WRITE_BOUNDARY_VIOLATION_OUTSIDE_AUTHORIZED_WRITABLE_ROOTS`; Kowalski nao foi invocado e o baseline do adapter nao foi aceito.

Na semana 2026-W32, o padrao foi reforcado: a rodada posterior de commit CPIW V4 ficou vinculada a bundle EDC e passou no commit de dados, mas isso nao apagou a necessidade de validar boundary em novas escritas nem promoveu automaticamente a aceitacao operacional Herald/dashboard.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Engineering-Delegation|OpenClaw Engineering Delegation]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel|Contrato de runtime reprodutivel]]
- [[40-CONHECIMENTO/Operacional/Commit-de-estado-nao-e-aceitacao-operacional|Commit de estado nao e aceitacao operacional]]
- [[01-DIARIO/Semanal/2026-W32|Semana 2026-W32]]

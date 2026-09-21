---
id: brain-2acb877be050e1fb027d
type: knowledge
title: Validação do runtime pós-migração
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T18:55:38.578515Z'
relationships:
- type: references
  target: BRAIN/50-PROJETOS/Planejamento/Migracao-Hostinger-VPS-OpenClaw.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/openclaw-crons/README-verificacao-crons.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md#relações
- type: references
  target: BRAIN/01-DIARIO/Semanal/2026-W29.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md#relações
---

# Validação do runtime pós-migração

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W29
confiabilidade: alta
ultima_revisao: 2026-07-17
tags: [openclaw, migracao, runtime, scheduler, skills, readiness, rollback]
```

## Princípio

Arquivo restaurado não comprova carregamento, configuração válida nem execução. Uma migração só termina quando o runtime ativo descobre, executa e preserva os componentes esperados depois de restart controlado.

## Gate mínimo

1. Confirmar versão alinhada entre CLI e serviços.
2. Confirmar supervisor, unit e state dir realmente usados.
3. Validar rotas ativas de workspaces, skills e configurações.
4. Confirmar skills indexadas, não apenas presentes em disco.
5. Validar armazenamento do scheduler, jobs habilitados, `nextWake`, vencidos/em execução e erros consecutivos.
6. Executar provas read-only ou canários permitidos para confirmar funcionamento real.
7. Verificar canal, RPC, portas e exposição esperada.
8. Fazer restart controlado e repetir o readiness para provar persistência.

## Separação de mudanças

Upgrade, plugin, modelo/configuração, porta, restart e recuperação de backlog são categorias distintas. Não misturar para ganhar tempo. No primeiro erro de versão, migração, plugin ou supervisor, parar e restaurar o último estado conhecido antes de escolher outra rota.

## Backlog

Antes de reiniciar ou reabrir canais, inspecionar jobs vencidos, em execução e filas pendentes. Depois da recuperação, deduplicar por identificador e responder apenas ao pedido mais recente quando mensagens antigas já foram superadas.

## Relações

- [[50-PROJETOS/Planejamento/Migracao-Hostinger-VPS-OpenClaw|Migração Hostinger VPS / OpenClaw]]
- [[70-AUTOMACOES/openclaw-crons/README-verificacao-crons|Verificação de segurança de crons]]
- [[01-DIARIO/Semanal/2026-W29|Semana 2026-W29, cobertura parcial até 2026-07-17]]

## Configuração, sessão e comunicação cruzada

Na recuperação histórica de 2026-06-13, os relatos distinguiram agentes cadastrados, visibilidade do histórico, permissão de comunicação e ferramentas já carregadas pela sessão. O teste individual de um agente também foi separado do teste em que um agente chama o outro.

Como critério de validação, conferir separadamente essas superfícies no runtime efetivo. Uma sessão com permissões carregadas antes da mudança pode exigir uma prova nova pelo caminho aprovado. Não concluir falha do gateway só por uma visão antiga da ferramenta, nem sucesso da comunicação cruzada só por um ping individual. Isso não recomenda abrir visibilidade ou permissões amplas; cada rota deve continuar limitada ao escopo necessário.

Fontes: trechos 28921, 28925, 28926, 28932, 28933, 28937 e 28938, identificados por hash e posição no recibo `BRAIN/99-SISTEMA/brain-v2/reports/coverage-round2-20260921.json`. São relatos históricos, não uma verificação da configuração atual.

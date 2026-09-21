---
id: brain-2cbb50d023b0fb9f84e0
type: state
title: Brain Enterprise
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:32:09.804705Z'
relationships:
- type: references
  target: BRAIN/99-SISTEMA/brain-v2/governance/semantic-coverage-and-archive.md
  reason: Registra o processo de cobertura e reconciliação autorizado para este projeto.
  source: user-request-20260921-brain-coverage
---

# Brain Enterprise

```yaml
status: em_andamento
responsavel_operacional: Agente Principal / Puppet Master
natureza: repositório vivo de conhecimento
origem:
  - BRAIN/01-DIARIO/2026/2026-06-12.md
  - BRAIN/01-DIARIO/Semanal/2026-W24.md
criado_em: 2026-06-14
```

## Objetivo

Manter o Brain como repositório vivo de conhecimento para preservar contexto, decisões, padrões, aprendizados e relacionamentos úteis ao longo do tempo.

## Diretrizes consolidadas

- O Brain não é agente.
- O Brain deve priorizar memória útil, não armazenamento bruto.
- Consolidações devem ocorrer em modo silencioso, salvo emergência real.
- Informações permanentes devem ser conectadas e ter utilidade futura clara.
- `BRAIN/99-ARQUIVO/` deve ser usado para reduzir prioridade sem apagar conhecimento.

## Estado atual

- Estrutura inicial criada.
- Filosofia e rotina registradas em `BRAIN/99-SISTEMA/`.
- Consolidações diárias iniciadas.
- Primeiro resumo semanal criado em `BRAIN/01-DIARIO/Semanal/2026-W24.md`.
- Brain v2 foundation aceita e publicada em `origin/main` no commit `ef724a98800ab9a0d408e34596b4dfbb51234f55`, com governança, schemas, métricas de saúde, política de MOC, propostas e regras fail-closed.
- A etapa 11A diagnosticou a dívida de conexão legada em modo read-only: `46` candidatos orphan/uncategorized, `107` links quebrados pelo contador legado e `97` links quebrados reais.
- A etapa 11B reintegrou o primeiro lote sem mover notas históricas, criou o MOC cronológico, corrigiu wikilinks óbvios e adicionou o Commit Link Gate local; commit `153129b52ae093c42bb106006de18b78a7ab7dbe` ficou em `origin/main`.
- Baseline Brain v2 após 11B: `0` links internos quebrados, `0` markdown uncategorized, `0` duplicate IDs, `0` duplicate aliases e health estimate `1`.
- A etapa 11C adicionou o Graph Gate: MOCs canonicos por area, medicao de alcance cognitivo, isolamento de snapshots versionados da camada cognitiva e filtro Obsidian para esconder `BRAIN/60-AGENTES/versionados/`.
- As etapas 11D/11E ajustaram a visualizacao do grafo Obsidian para esconder snapshots operacionais, unresolved links e orphans, mantendo a area versionada preservada no Git e fora do grafo cognitivo.
- Validacao local em 2026-08-09 apos consolidacao semanal: Commit Link Gate `ok=True`, `345` Markdown, `0` links internos quebrados, `0` uncategorized, `0` unreachable cognitive markdown, `0` isolated cognitive markdown, `1` componente de grafo e health estimate `1`.

## Próximos passos

- Popular registros reais conforme surgirem informações relevantes.
- Fortalecer links entre pessoas, empresas, projetos, automações e aprendizados.
- Criar MOCs ou dashboards adicionais somente quando houver volume e recorrência suficientes.
- Validar o Commit Link Gate depois de consolidações reais para comprovar que a rotina diária não volta a gerar nota solta.
- Reconciliar o script legado de sync GitHub com a política fail-closed antes de tratar o gate como mecanismo obrigatório de commit automático.
- Manter o filtro Obsidian alinhado ao escopo cognitivo: snapshots versionados continuam como inventario operacional, nao como conhecimento navegavel do grafo.

## Relações

- [[40-CONHECIMENTO/IA/Brain-como-sistema-de-memoria|Brain como sistema de memória]]
- [[40-CONHECIMENTO/Operacional/Consolidacao-silenciosa-sem-ruido|Consolidação silenciosa sem ruído]]
- [[01-DIARIO/README|MOC Diario]]
- [[99-SISTEMA/brain-v2/governance/README|Brain v2 Governance]]

## Cobertura de históricos em 2026-09-21

[[99-SISTEMA/brain-v2/governance/semantic-coverage-and-archive|Cobertura, conexões e arquivo semântico]] registra o procedimento e seus limites. O arquivo externo de 36.389 fontes foi verificado, mas a revisão de conteúdo permanece parcial. Os originais da VPS continuam preservados por decisão do usuário. A habilidade de pesquisa semântica está instalada na VPS e foi reconhecida pelos catálogos dos cinco agentes, incluindo os perfis separados de Kowalski e Darth Vader. O índice acompanha alterações nas notas por demanda; o mecanismo nativo de memória e os agendamentos existentes não foram alterados. A revisão dos históricos continua parcial. O Mac serve somente à revisão transitória; as cópias brutas elegíveis serão descartadas após cobertura e checagem operacional, sem exigência de arquivo integral permanente.

## Cobertura dos gateways separados

A conferência de 21/09 confirmou contribuições parciais de Kowalski e Darth Vader no Brain, mas não envio integral contínuo. Os quatro agendamentos Brain pertencem ao perfil principal; os perfis dedicados têm zero agendamentos Brain. As duas memórias Markdown de Kowalski coincidem com snapshots publicados em julho. A memória FIP de Darth de 25/08 não tem snapshot equivalente: parte está consolidada no projeto FIP, e a revisão recuperou uma correção de escopo ainda ausente. O recibo `BRAIN/99-SISTEMA/brain-v2/reports/gateway-brain-coverage-20260921.json` separa essas evidências. A rotina diária precisa de inventário explícito das fontes por agente e recibos de cobertura; essa automação ainda não foi implantada.

## Complementos reconciliados — lote 7 de 2026-09-21

Falha de busca semântica não significa perda das notas. Arquivos de memória e Brain podem permanecer disponíveis para leitura direta enquanto o provedor de embeddings falha; registrar separadamente disponibilidade de conteúdo, índice e mecanismo de consulta, sem declarar o incidente antigo como vigente. Fonte: unidades 31091.

No incidente histórico billing_not_active, a busca vetorial falhou enquanto chat OAuth e arquivos continuavam disponíveis. Verificar autenticação, disponibilidade do provedor de embeddings e índice separadamente do Gateway/chat; não concluir que assinatura de chat cobre embeddings nem que falha de índice apagou memória. Estado antigo não autoriza ativar cobrança ou trocar provedor. Fonte: unidades 37478.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 8 de 2026-09-21

No scheduler SQLite, storePath legado exibido por CLI não prova que jobs.json seja fonte ativa. Identificar storage/sqlitePath e job exato por nome/ID/contrato. Se rotina pedida não é encontrada, não editar job vizinho porque horário/agente parecem próximos; ausência naquela consulta não comprova inexistência atual. Horário histórico de helpdesk não altera agenda Brain vigente. Fonte: unidades 9680.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch8-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

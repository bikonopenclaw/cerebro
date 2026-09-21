---
id: brain-b1cfcd65c58f33791afc
type: knowledge
title: Contrato de runtime reproduzivel
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T20:54:07.904960Z'
relationships:
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel.md#relações
- type: references
  target: BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel.md#relações
- type: references
  target: BRAIN/01-DIARIO/Semanal/2026-W31.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel.md#relações
---

# Contrato de runtime reproduzivel

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W31; bootstrap RSE M2 em 2026-08-28/29; precheck Sentinel em 2026-09-07; reparo do relay nativo em 2026-09-08; handoffs Robotnik/Kowalski em 2026-09-11 e Puppet/Kowalski em 2026-09-16
confiabilidade: alta
ultima_revisao: 2026-09-17
tags: [runtime, python, reproducibilidade, checksums, supply-chain, drift, cgroup, executor, lifecycle, sandbox, mounts, handoff, materializacao, timeout, process-group]
```

## Principio

Runtime operacional nao deve depender de caminho conveniente, instalacao local implicita ou descricao historica ambigua. O contrato precisa permitir reconstruir, auditar e detectar drift.

## Campos minimos

- Sistema operacional e arquitetura.
- Nome e versao final do runtime.
- Caminho absoluto do executavel usado em operacao.
- Origem do artefato e metodo de provisionamento.
- SHA-256 do executavel e, quando aplicavel, hash da arvore instalada.
- Versoes auxiliares relevantes, como Unicode no caso de CPython.
- Regra de drift: o que invalida o runtime e exige novo freeze.

## Aplicacao pratica

- Diferenciar evidencia historica de contrato futuro.
- Nao promover caminho de ambiente local a requisito operacional sem decisao documental.
- Validar o runtime pelo caminho absoluto congelado, nao por `python3` resolvido pelo shell.
- Registrar correcoes de contrato como alteracao documental propria, com novo hash e validacao independente.
- Em execucoes longas, provar PID, tmux/unit real, cgroup efetivo e limites lidos do processo; o nome ou scope planejado nao comprova onde o workload esta rodando.
- Separar durabilidade do trabalho da vida da conversa/control-plane: clone, checkpoints, logs e identidade precisam sobreviver ao encerramento do turno.
- Nao declarar isolamento de recursos quando o scope limitado esta inativo e o processo real pertence a outro cgroup.
- Autenticar a superficie efetivamente visivel ao executor: mudar `cwd` nao cria mounts nem concede acesso a state dir, workspace de outro agente, SQLite, CLI, supervisor ou systemd.
- Falha de acesso dentro de um sandbox prova apenas a limitacao daquela superficie; nao comprova ausencia, defeito ou estado terminal do alvo vivo.
- Timeout de subprocesso deve envolver o bootstrap externo e seu grupo de processos. Um limite iniciado somente depois do runtime carregar nao contem travamento anterior ao startup nem relay abandonado.
- Sucesso de escrita ou copia dentro da visao gerenciada do produtor nao prova materializacao duravel no host nem visibilidade para o consumidor. Handoff entre agentes precisa de leitura real pelo destino, identidade/hash dos mesmos bytes e recibo terminal separado da mera aceitacao da solicitacao.
- `127.0.0.1` e relativo ao namespace de rede do processo. Um servidor local do produtor nao e ponte entre agentes isolados sem rota explicitamente compartilhada e autorizada; falha de `curl` no consumidor deve bloquear o handoff, nao induzir copia presumida.

## Exemplo conectado

Em 2026-W31, o contrato futuro do Provimento 213 foi alinhado ao CPython `3.14.6` final em `/opt/openclaw/runtimes/cpython-3.14.6/bin/python3`, com Unicode `16.0.0`, hash de executavel e hash de arvore instalada. A referencia historica a `/opt/homebrew/bin/python3` permaneceu evidencia antiga, nao contrato operacional futuro.

No bootstrap RSE M2 de 2026-08-28/29, uma continuacao direta caiu quando o scope pai do OpenClaw terminou. O tmux persistente preservou o trabalho, mas a auditoria mostrou que o executor real estava em `session-3.scope`, nao no scope limitado reportado. O aprendizado e verificar o cgroup efetivo do processo antes de afirmar durabilidade ou resource envelope.

No precheck Sentinel de 2026-09-07, diferentes executores receberam apenas o workspace principal. Mesmo com `cwd=/data/.openclaw`, config/state ativos, workspace Sentinel, SQLite, supervisor e systemd continuaram invisiveis. A manutencao parou antes de backup ou mutacao e preservou o mesmo Goal, pois readmitir em uma superficie correta e diferente de inferir o estado do runtime a partir do sandbox errado.

No reparo Puppet/Robotnik de 2026-09-08, o relay nativo precisava limitar o CLI antes que Node pudesse iniciar. O comando passou a envolver bootstrap e grupo de processos com timeout/TERM/KILL limitado; canarios de sucesso, falha de ferramenta e entrega Telegram passaram, sem converter o job ARX original falho em sucesso.

No handoff Robotnik/Kowalski de 2026-09-11, a copia reportada no workspace principal nao apareceu de forma duravel e, mesmo depois de criada no host, permaneceu invisivel ao filesystem gerenciado do revisor. A rota funcional materializou copia byte a byte no workspace proprio do Kowalski e exigiu abertura/revisao real dos assets; configuracao, permissoes e servicos permaneceram inalterados.

No handoff documental Puppet/Kowalski de 2026-09-16, os PDFs-base nao estavam visiveis pelo caminho compartilhado e o servidor em `127.0.0.1` do produtor nao era alcancavel no namespace de rede do Kowalski. Hash declarado e aceite do job nao provaram download. A continuacao segura ficou dependente de materializacao autenticada no workspace do consumidor e confirmacao dos mesmos bytes antes de gerar ou revisar os documentos.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao|Validação do runtime pós-migração]]
- [[40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git|Artefatos gerados fora do Brain e Git]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[01-DIARIO/Semanal/2026-W31|Semana 2026-W31, cobertura parcial]]

## Complementos reconciliados — lote 21 de 2026-09-21

No DRV histórico de 31/07, o adaptador comprovou UTF-8, SHA-256, filesystem, rename atômico e fsync, mas a execução parou porque o renderer não sobreviveu à fronteira de turno. PASS da camada de capacidades não demonstrava presença do código/estado necessário à retomada. Persistir e autenticar executor, inputs e checkpoint recuperáveis, sem depender da memória da conversa; naquele episódio houve zero render/publicação e a ordem foi encerrada, antecedendo o desenho DRE posterior. Fonte: unidades 33080, 33083.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch21-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

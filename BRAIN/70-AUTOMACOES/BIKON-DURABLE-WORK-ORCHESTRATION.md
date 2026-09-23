---
id: brain-89486c0eadea3b74ee11
type: state
title: Bikon Durable Work Orchestration
created: '2026-09-21T19:15:09.943981Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-23T02:00:00Z'
---

# Bikon Durable Work Orchestration

```yaml
categoria: automacao_operacional
fonte: contrato canonico, requests de 2026-09-16/19 e recusas protegidas de 2026-09-22
confiabilidade: alta para os eventos citados, sem inferir estado produtivo atual
ultima_revisao: 2026-09-23
tags: [bikon, durable-work, relatorios, documentos, sentinel, kowalski, lifecycle, idempotencia]
```

## Finalidade

Preservar pedidos assíncronos de relatórios e documentos além do turno conversacional, com admissão, handoff, execução, evidência, artefato, QA, recuperação e entrega registrados sob uma única identidade durável.

## Contrato operacional

- Puppet Master é owner do pedido; Sentinel coleta; Kowalski analisa, produz, renderiza e faz QA visual.
- A autoridade de negócio é o SQLite canônico de requests e o controller existente. Não criar ledger paralelo nem despachar fases duráveis diretamente por `sessions_send` ou `sessions_spawn`.
- Somente receipt com `WORK_DURABLY_ADMITTED=true`, `request_id` estável e `durably_admitted_at` permite alegar que o trabalho foi aceito.
- ACK, runId, fila de sessão ou mensagem aceita não comprovam por si só admissão, progresso de negócio nem conclusão.
- Status é observacional; não admite, redespacha, aprova, troca executor nem cria sucessor.
- Handoff, input hash, runtime/gateway aceito, artefatos e terminalidade são persistidos antes de avançar.
- Recovery reaproveita outputs comprometidos e faz retries causais limitados na mesma identidade; não usa replay cego.
- Rework preserva bytes e QA históricos do predecessor e admite no máximo um sucessor autenticado.
- Falha depois de `ACK_DURABLE` nao autoriza repetir o mesmo input. Recuperacao exige causa identificada e mudanca autenticada de codigo, contrato, evidencia ou autoridade, preservando barreiras e tentativas anteriores.
- Revisoes de apresentacao permanecem na mesma request, com artefatos imutaveis por versao, single-writer, hash proprio e entrega idempotente; nao refazem coleta nem alteram a verdade de negocio.

## Regras de relatório

- `ARTIFACT_TECHNICAL_QA` não substitui `BUSINESS_SEMANTIC_ACCEPTANCE`.
- Empty history não prova zero execuções; artefato de disponibilidade não satisfaz intenção de performance de backup.
- Pedido explícito por “dados disponíveis” ativa `AVAILABLE_AUTHENTICATED_DATA_V1` somente para aquela request: usar observações autenticadas com datas reais e limitações declaradas, sem exigir que a falta de cobertura vire falha ou zero atividade.
- Entrega ao proprietário privado exige reconhecimento do transporte. Cliente, grupo ou outra rota externa nunca são inferidos.
- Resultado ambíguo de envio bloqueia resend cego.

## Evidência observada

- O pedido documental Bruna Reffatti terminou `COMPLETED`: dois PDFs comprometidos, QA textual/visual `PASS` e retorno interno pronto.
- Requests ARX para Alfredo Chaves, Cartório Capixaba, Cartório Camburi e Cartório Vila Velha terminaram `SUCCESS`, com PDF autenticado, QA `PASS`, delivery `ACKNOWLEDGED`, `customer_delivery=false` e `provider_mutation=false`.
- A request de Alfredo Chaves usou `31` sessões autenticadas retidas com cobertura parcial explicitada. Capixaba e Camburi usaram `190` registros autenticados cada; Vila Velha usou `134` registros, incluindo `122` execuções, `121` sucessos, `1` com erro e `12` skips. Esses números permanecem vinculados às datas/cobertura dos recibos e não devem ser generalizados para o mês inteiro.
- A request Alzira posterior usou `192` execucoes autenticadas (`191` sucessos e `1` falha), terminou `SUCCESS` e teve entrega privada reconhecida apos uma recuperacao causal de QA visual.
- A request Capixaba posterior preservou `190` execucoes com sucesso no recorte e chegou a uma apresentacao revisada por cinco recuperacoes causais limitadas. Versoes/recibos anteriores foram mantidos, provider nao foi reconsultado e o aceite de negocio continuou separado do terminal tecnico.

## Reconciliação interna bloqueada — 2026-09-22

A ordem `ORDER-SENTINEL-LATE-BITDEFENDER-20260918-20260922T002540Z` tinha pedido de reconciliação exclusivamente pelo `puppet_control` protegido, preservando identidade, período e autorização, sem entrega externa nem repetição de efeito incerto. No recorte lido, duas chamadas `scoped_inspect` foram recusadas pelo hook `PreToolUse` com `REGISTERED_INTERNAL_PROJECTION_REQUIRED`; o agente encerrou sem avançar admissão, retomada, revisão ou fechamento.

A distinção útil é entre operação anunciada no catálogo e projeção administrativa autenticada no runtime: a primeira não prova a segunda. O bloqueio aconteceu antes da inspeção canônica; não demonstra ausência de dados Bitdefender, defeito do provider ou estado terminal de negócio. Este registro preserva o impedimento observado, não autoriza corrigir permissões, trocar rota, refazer coleta ou retomar a ordem por memória.

Fonte: sessão main `39bfe49e-6317-4005-9e8f-a97b93197adf`, linhas 2–3, e rollout Codex `01a0c8ae-38dc-72b3-98a2-612e7cff8e67`, chamadas/recusas nas linhas 18–19 e 36–37. Identidades SHA-256 e limites da leitura em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-2026-09-23-daily.json`.

- [[01-DIARIO/2026/2026-09-23|Consolidação e limites de cobertura]].

## Relações

- [[70-AUTOMACOES/ARX-BACKUP-NINJAONE|ARX Backup NinjaOne]]
- [[70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM|Relatorios Operacionais Telegram]]
- [[60-AGENTES/SENTINEL|Sentinel]]
- [[60-AGENTES/KOWALSKI|Kowalski]]
- [[40-CONHECIMENTO/Operacional/Estado-terminal-requer-convergencia-do-lifecycle|Estado terminal requer convergencia do lifecycle]]

## Complementos reconciliados — lote 6 de 2026-09-21

Nos episódios de promessa de retorno, exigir registro de pendência com identidade, responsável, estado, próximo acompanhamento e critério de encerramento; deduplicar follow-ups e encerrar explicitamente como concluído, bloqueado com causa ou falho. Hebert posteriormente pediu retirar a restrição de horário desse acompanhamento. O contrato atual de trabalho durável prevalece: integrar ao controlador canônico, sem criar ledger paralelo ou reinstalar plugin/cron histórico pela memória. Fonte: unidades 35310, 35382, 31098.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 7 de 2026-09-21

O episódio DRV mostrou que validar UTF-8/hash/filesystem não garante retomar uma transação: o renderer necessário não estava disponível após mudança de turno. Trabalho que cruza turnos precisa de executor/artefatos autocontidos e identificados por versão/hash, com entradas e progresso persistidos. Não reconstruir implementação pela memória conversacional nem alegar continuidade a partir de capability check parcial. Fonte: unidades 29247, 33078.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 8 de 2026-09-21

Na especificação histórica DRE, render e publicação formavam uma unidade durável: inputs e renderer disponíveis fora da sessão, identidade de runtime congelada, três renders de mesma entrada com hash idêntico, journal de retomada, ponteiro de publicação atômico e rollback. Preservar a lição de autossuficiência e identidade, sem transformar a proposta antiga de CPython/DRE em dependência atual nem inferir entrega pelo texto da especificação. Fonte: unidades 33087.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch8-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 9 de 2026-09-21

No testeNinja1502, sucessivos pedidos de aprovação atrasaram sequência já autorizada e a credencial deixou de funcionar antes da escrita. Definir escopo completo e executável de autenticar/ler/alterar/verificar, capturar valores necessários em memória e respeitar a autorização já concedida. Callbacklocalhost requer handler no dispositivo que recebe o redirecionamento ou túnel validado; nó ausente não permite prometer fluxo de um gesto. Uma sequênciaGET/PUT/GET não é transação reversível: falha apósPUT pode deixar alteração remota; registrar resultado parcial/incerto e não repetir escrita cegamente. Fonte: unidades 36216.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch9-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 10 de 2026-09-21

Em preparação da adoção PGL, evidência root-owned0700 não era legível ao usuário openclaw; um selo independente acessível foi usado para autenticar baseline, com limite de evidência explícito. Propôs-se contrato compartilhado único e ponteiros nos agentes, em vez de semânticas duplicadas ou ledger concorrente. Bindings PFE que diziam PGL deferred/unavailable exigiam reconciliação, não evento histórico inventado; projetos existentes adotariam na transição de ciclo apropriada. Este trecho era descoberta read-only, não prova de adoção concluída ou saúde atual. Fonte: unidades 30968.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

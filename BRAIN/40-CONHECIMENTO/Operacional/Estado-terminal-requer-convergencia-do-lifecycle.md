---
id: brain-74f9d101198913292ed0
type: knowledge
title: Estado terminal requer convergencia do lifecycle
created: '2026-09-21T19:26:27.377766Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T21:07:33.285014Z'
---

# Estado terminal requer convergencia do lifecycle

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W35, teste controlado de relatorios operacionais em 2026-09-02, publicacao Instagram Bikon em 2026-09-10, lifecycle ad-hoc ARX em 2026-09-16 e consolidacao semanal 2026-W38
confiabilidade: alta
ultima_revisao: 2026-09-20
tags: [lifecycle, execucao, registry, cgroup, terminalidade, reconciliacao, supervisao, transcript]
```

## Principio

Uma execucao so e terminal quando fila, admissao, registry, child, processo fisico e evidencias persistidas convergem para a mesma identidade e para um unico resultado. Estado terminal em apenas uma camada nao prova encerramento do workload.

## Aplicacao pratica

- Criar a identidade duravel antes do child ou do processo fisico.
- Registrar transicoes `accepted -> admitted/deferred -> spawned -> bootstrapped -> workload_started -> output_committed -> terminal`.
- Vincular fila, registry, PID, unit/tmux, cgroup e checkpoint ao mesmo execution ID.
- Considerar terminalidade invalida quando o cgroup canonico ainda possui processo vivo, os bytes continuam mudando ou falta reconciliacao do output.
- Preservar historico factual: lease expirada ou admissao stale nao deve ser reescrita como cancelamento que nao ocorreu.
- Depois de perda de sessao ou gateway, reconciliar a mesma execucao; nao criar retry concorrente por ausencia de observador.
- Tratar transcript e chat como superficies de observacao, nao como fonte terminal; reconstruir o estado pelo registry duravel, checkpoints, artefatos e fila de anuncio.
- Distinguir heartbeat de progresso significativo: apenas transicao de stage, tool concluida, artefato, checkpoint, handoff, gate aceito ou terminalidade avanca o relogio de progresso.
- Pressao transitoria (`EAGAIN`, `pthread_create`, capacidade do app-server) so admite retry limitado quando a operacao e segura, o efeito externo e conhecido e os checkpoints permanecem intactos.
- Quando o efeito externo já foi comprovado, falha posterior de readback, cleanup ou recibo não autoriza repetir o efeito; preservar o estado realizado e retomar somente as etapas idempotentes de fechamento.
- ACK e start sao transicoes duraveis da mesma identidade de execucao, nao mensagens conversacionais. Timeout deve persistir falha terminal e bloquear a request; nao autoriza criar sucessor, trocar rota ou iniciar efeito externo.
- Recovery exige uma mudanca causal documentada: nova fonte, contrato corrigido ou evidencia de runtime distinta. Preservar a mesma identidade, artefatos, hashes, revisoes e recibos; replay do mesmo input depois da barreira de efeitos deve ser bloqueado.

## Exemplo conectado

Em 2026-W35, RSE, ODP/B1 e o P1 de Relatorios Operacionais mostraram o mesmo defeito: child criado antes da admissao, caller bloqueado em espera e perda da sessao sem convergencia com registry e processo fisico. A retomada ficou bloqueada ate existir lifecycle canonico e prova terminal compartilhada.

No teste controlado de Relatorios Operacionais de 2026-09-02, um transcript incompleto aparentou stall depois que o Goal ja havia fechado `ACCEPTED`. A reconciliacao pelo supervisor e pelos artefatos duraveis evitou recoleta, regeneracao e reenvio, encerrando o alerta como falso stall.

Na publicação Instagram Bikon de 2026-09-10, o Graph confirmou o `media_id` e o permalink antes de o readback visual falhar por bloqueio do novo CDN. O estado correto permaneceu `PUBLISHED`, com fechamento local pendente; repetir `media_publish` seria duplicar um efeito externo já comprovado.

No request ARX/Cove ad-hoc de 2026-09-15/16, tentativas intermediarias nao autorizaram sucessores em loop. A reconciliacao reteve uma unica linhagem canonica, fechou `FAIL_CLOSED_EXTERNAL_OWNER_GATE` antes do provider e congelou a mesma request ate existirem binding numerico aprovado e gate de rede proprio.

Em 2026-W38, as revisoes do relatorio Capixaba permaneceram na mesma request e corrigiram contrato visual, prova do runtime e apresentacao sem recoleta. No caso 2111, o esgotamento das fontes autorizadas fechou a linhagem por evidencia insuficiente e bloqueou repeticao identica.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|Ausencia de evidencia nao e status operacional]]
- [[40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel|Contrato de runtime reprodutivel]]
- [[40-CONHECIMENTO/Operacional/Governanca-de-capacidade-nao-e-roteamento-semantico|Governanca de capacidade nao e roteamento semantico]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-RSE|OpenClaw RSE]]
- [[70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM|Relatorios Operacionais Telegram]]
- [[70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK|Instagram Bikon Robotnik]]
- [[70-AUTOMACOES/ARX-BACKUP-NINJAONE|ARX Backup diario e tickets NinjaOne]]
- [[01-DIARIO/Semanal/2026-W35|Semana 2026-W35]]
- [[01-DIARIO/2026/2026-09-03|Diario 2026-09-03]]
- [[01-DIARIO/2026/2026-09-10|Diario 2026-09-10]]

## Complementos reconciliados — lote 7 de 2026-09-21

No caso histórico R2, o child não possuía a rota aprovada para Kowalski. Limitou-se à preparação local e retorno de artefatos/hash; o controle principal fazia a revisão independente. Se o child perder contexto, reconciliar artefatos existentes antes de criar sucessor, evitando fila duplicada ou aprovação impossível no isolamento. Fonte: unidades 37061.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 9 de 2026-09-21

Na validação histórica ShadowR4 em POSIX/Linux, check+varredura+append usavam o mesmo flock com deadline, coordenando fonte primária e fallback por execution_id. Duplicata semanticamente idêntica conta uma vez; mesmoID com conteúdo conflitante falha, sem relatório de sucesso. JSON inválido/truncado torna relatório incompleto; ausência de fonte não é conjunto vazio bem-sucedido. Agreement usa comparáveis; coverage usa universo único, com UNKNOWN separado. Confirmar escrita perdida por ALREADY_PRESENT evita segunda linha. Garantia não abrange perda total do host; PASS dos testes não ativa runtime. Fonte: unidades 34275.

Histórico DRE registrou duplicação de liberação após replay/resume de sessão. Identificar execução de forma estável e serializar a transição no controlador/owner único; nova mensagem ou retomada do agente não deve criar uma segunda liberação da mesma janela. Reconciliar estado canônico antes de retentar. Fonte: unidades 33976.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch9-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 10 de 2026-09-21

A revisão Shadow anterior à R4 reproduziu duplicação porque busca usava tail fixo de131072bytes, relatórios ignoravam companion fallback e timeout aceitava bool/NaN/Infinity/1e308. Exigir tipo numérico finito positivo com máximo documentado, varredura completa sob deadline/lock e deduplicação por identidade. Companion inválido não pode ser seguido como arquivo seguro nem bloquear indefinidamente o primário; testar falha/contingência sem violar idempotência. Timeout isolado de FIFO não virou bloqueador quando reprodução mostrou rc2 rápido: preservar apenas achado reproduzido, não ampliar severidade por primeira observação. Estado final posterior daR4 deve prevalecer sobre rejeição intermediária. Fonte: unidades 41424.

Na revisão histórica Shadow, janela fixa dos últimos128KiB deixou duplicação passar; idempotência deve cobrir primário e fallback sob coordenação interprocesso/deadline. Timeout precisa rejeitar booleanos,NaN,infinito,não positivo e valores além do máximo contratado. Mesmo execution_id com conteúdo divergente deve bloquear métricas, não somar como duas execuções; fallback inválido não deve silenciosamente destruir a garantia de persistência. Achados pertencem ao candidato revisado, não afirmam falha atual. Fonte: unidades 41423.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 14 de 2026-09-21

Na revisão ShadowR4, primeiro probeFIFO expirou, mas repetição confirmou rc2 semhang; não manter bloqueador baseado só no primeiro timeout. FonteUTF8inválida podia produzir relatório parcial com registros válidos do companion, report_complete=false/rc2. Companion inválido havia impedido append no primário saudável, mas nova alteração de código exigia revalidar o diff porhash; mtime não prova correção nem permanência do defeito. Consolidar junto41423 semdiagnóstico atual. Fonte: unidades 41426.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch14-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 15 de 2026-09-21

Em 01/08, o NOOP Sentinel executou uma vez e o controlador retornou IDLE, levando a relato inicial de PASS. A revisão posterior do ledger encontrou technical_START_count=1, execution_release_count=2 e Sentinel_execution_count=1, sem execução duplicada ou tardia. O resultado final foi FAIL_CLOSED por replay concorrente de sessão coordenadora: uma execução de negócio não prova unicidade da liberação. Preservar a divergência no ledger append-only; a correção requeria single-owner e liberação idempotente em runtime sob nova autorização. Não retomar a antiga ordem DRE: rollback havia sido confirmado, e o próximo pedido de implementação não é prova de correção já aplicada. Fonte: unidades 30768.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch15-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 16 de 2026-09-21

No EP-02 documental, o resultado podia explicar prontidão apenas documental, mas o campo de checkpoint precisava continuar no enum contratado READY/BLOCKED/FAILED. Separar resultado explicativo e estado executável; não inventar READY_DOCUMENTATION_ONLY como estado técnico se o contrato não o reconhece. Autorização para redigir um artefato também não altera por si o conteúdo das fontes normativas daquele projeto. O PASS documental posterior não autoriza implementação nem transforma o bloqueio técnico anterior em execução realizada. Fonte: unidades 9722.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch16-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 21 de 2026-09-21

Na revalidação documental EP-02 de 28/07, trocar READY_DOCUMENTATION_ONLY por READY não bastava: a Execution Order congelada exigia commit e conferência pós-commit para READY, enquanto a unidade ainda proibia stage/commit. Conferir pré-condições do estado além do enum. O checkpoint intermediário seguia pendente; o commit documental autorizado posterior resolve essa etapa, sem autorizar implementação técnica nem estabelecer primazia universal de documento sobre instruções do usuário. Fonte: unidades 9724.

Na implantação histórica das travas de orquestração em 26/07, foram relatados ordem ativa única, supersedes, ACK por caminho/hash e pausa de oito crons não críticos; 9 testes e um ensaio passaram, com estado final IDLE e os oito crons restaurados. Essa prova cobre aquela aplicação/ensaio, sem comprovar política ou grade atuais nem reabrir a rota NinjaOne. Avaliar fechamento também pela restauração das suspensões temporárias, além do término do agente. Fonte: unidades 33677.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch21-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 23 de 2026-09-21

Na Fase A Sentinel de 26/07/2026, o approval foi validado, seis GETs ocorreram e o resultado fechou BLOCKED_BY_PAGINATION antes de chegar um STOP associado à falta de receipt. O STOP impede ações futuras, mas não pode reclassificar a execução comprovada como não iniciada ou não autorizada: preservar fatos e timestamps, entrega pendente e resultado terminal separadamente. A Fase A.1 posterior tinha nova identidade e falhou antes do consumo e de qualquer GET porque ensure_ascii=True divergia da serialização UTF-8/jq contratada. Não transportar o zero GET da segunda tentativa para apagar a primeira, nem o sucesso de propagação da primeira para aprovar a segunda. Fonte: unidades 37815.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch23-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

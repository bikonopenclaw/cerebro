---
id: brain-6c2a6fe514b26e141d58
type: knowledge
title: Ausência de evidência não é status operacional
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T17:53:52Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/ARX-BACKUP-NINJAONE.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional.md#relações
- type: references
  target: BRAIN/60-AGENTES/KOWALSKI.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional.md#relações
- type: references
  target: BRAIN/20-EMPRESAS/BIKON/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md
  reason: Aplica a distinção entre evidência ausente e falha confirmada ao timeout histórico de emissão fiscal.
  source: BRAIN/99-SISTEMA/brain-v2/reports/coverage-20260921.json#text-3515-3518
---

# Ausência de evidência não é status operacional

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W28; Portal 213 Stage 1B R2.4 em 2026-08-20; qualificacao mensal ARX em 2026-09-08/09; fechamento semanal Relatorios Operacionais em 2026-09-14; consolidacao semanal 2026-W38
confiabilidade: alta
ultima_revisao: 2026-09-20
tags: [monitoramento, evidencia, recencia, revalidacao, ninjaone, backup, hyper-v, operacao, checkpoint, cobertura-temporal, paginacao]
```

## Princípio

Quando uma ferramenta operacional não expõe dado explícito, a conclusão correta é "sem evidência consultável", não sucesso presumido nem falha confirmada.

Evidência antiga também não comprova estado atual. Toda conclusão operacional precisa declarar fonte, horário da coleta e janela de validade adequada ao risco.

## Aplicação prática

- Em monitoramento, diferenciar ausência de job, alerta, atividade ou custom field de falha real.
- Não afirmar que backup, replicação, atualização ou remediação está OK sem campo, log, job ou evento oficial.
- Registrar a lacuna de instrumentação como pendência quando a informação for necessária para decisão.
- Criar integração, monitor, script ou custom field específico quando o dado precisa ser acompanhado de forma recorrente.
- Tratar evidência sem timestamp ou fora da janela de recência como contexto histórico, não como estado atual.
- Exigir nova coleta antes de encerrar ticket automático, incidente ou alerta cuja resolução dependa da fonte operacional.
- Não usar inventário restaurado, `nextWake`, último sucesso ou arquivo existente isoladamente como prova de funcionamento contínuo.

## Recência e revalidação

- A janela de recência deve ser definida por tipo de sinal, impacto e frequência esperada da fonte.
- Abertura automática de ticket exige evidência atual e regra aprovada. No fluxo Bitdefender -> NinjaOne, `endpoint_sem_protecao` só é acionável quando o endpoint foi visto há menos de 30 dias.
- Auto-fechamento exige uma coleta posterior à abertura que confirme resolução. Ausência do alerta anterior não basta quando a fonte não comprova o estado atual.
- Quando a fonte estiver indisponível, manter `sem evidência consultável` e registrar a necessidade de revalidação.
- Child session, processo orfao, log parcial ou marcador historico nao e autoridade operacional. Para continuar uma execucao interrompida, exigir evidence path estavel, manifest hash e validacao do estado subjacente.

## Cobertura temporal e populacao

- Primeiro e ultimo timestamp nao provam que todos os eventos intermediarios foram recuperados.
- Fechamento mensal exige identidade do alvo, limites de periodo e timezone, paginacao exaurida, IDs unicos, dias cobertos, lacunas e registros nao classificados explicitados.
- Snapshot corrente, barra rolante de 28 dias, metrica agregada ou nome de arquivo com competencia nao substitui a populacao do mes-calendario.
- Mes ainda aberto deve permanecer parcial: datas futuras sao fora da janela, nao falha de coleta; intervalo decorrido sem registros exige classificacao propria.
- Ausencia de sessoes em um dia nao autoriza inferir zero incidentes, sucesso do backup ou destruicao de historico.
- Artefato valido, submissao ao transporte, ACK do provider, entrega na caixa e leitura humana sao estados separados; ausencia do recibo de um deles nao pode ser preenchida pelo outro.
- Coleta upstream, composicao do relatorio, materializacao no cache e consumo pelo cron sao estados separados. Cache semanal ausente ou invalido prova indisponibilidade no ponto de consumo, mas nao autoriza afirmar que a coleta nao ocorreu nem que o provider estava indisponivel.
- Dados autenticados disponiveis podem sustentar uma saida parcial quando o pedido autoriza esse recorte, mas datas, populacao observada e limitacoes precisam acompanhar cada metrica. Essa excecao por request nao converte ausencia em zero nem relaxa o gate de cobertura mensal.

## Exemplo conectado

Em 2026-07-07, o NinjaOne expôs inventário, conectividade, volumes, alertas e atividades de `HOST1 | Magnitos Granitos`, mas não expôs conclusão de backup nem status de Hyper-V replication. O status correto foi registrar ausência de evidência e apontar instrumentação necessária.

Em 2026-08-20, no Portal 213 Stage 1B R2.4, execucoes anteriores foram classificadas como orfas e nao autoritativas. Sem retorno autenticado de classificacao, evidence path e `MANIFEST.sha256`, o estado correto e nao iniciar o proximo checkpoint por inferencia.

Em 2026-09-08/09, a qualificacao ARX demonstrou que estatistica corrente e barra rolante nao sustentavam relatorio mensal. A cadeia so fechou agosto depois de recuperar sessoes nativas com paginacao terminal, identidade/periodo e lacunas verificadas. Setembro permaneceu parcial e o dia 07/09 de Vila Velha ficou sem classificacao, em vez de ser convertido em sucesso ou falha.

Em 2026-09-14, o cron semanal Bitdefender encontrou o cache esperado ausente ou invalido e respondeu fail-closed. O registro correto foi indisponibilidade do relatorio no ponto de consumo; a mensagem padrao nao foi promovida a diagnostico da coleta Sentinel nem do provider.

Em 2026-W38, relatorios ARX por dados autenticados disponiveis foram aceitos apenas para os recortes explicitamente observados. O caso 2111 de agosto permaneceu insuficiente para performance mensal, enquanto requests novas puderam declarar datas, contagens e lacunas sem reescrever o predecessor.

## Relações

- [[70-AUTOMACOES/ARX-BACKUP-NINJAONE|ARX Backup diário → tickets NinjaOne]]
- [[60-AGENTES/KOWALSKI|Kowalski]]
- [[20-EMPRESAS/BIKON/README|BIKON]]
- [[40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao|Validação do runtime pós-migração]]
- [[40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento|Menor privilégio em monitoramento]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]

## Evidência histórica reconciliada em 2026-09-21

O histórico de Darth Vader de 2026-06-13 relata timeout depois do envio de uma emissão NFS-e e uma consulta posterior inconclusiva. Esse relato sustenta a distinção entre falta de resposta e ausência de efeito: a intenção de não reenviar evitava assumir que a emissão havia falhado. Não comprova o resultado fiscal daquela tentativa nem a disponibilidade atual de endpoints.

A fonte original foi preservada no arquivo externo verificado; o catálogo `BRAIN/99-SISTEMA/brain-v2/reports/coverage-20260921.json` identifica os trechos 3515 e 3518 por hash e posição. Essa recuperação histórica não autoriza reemitir notas nem retomar tarefas antigas.

[[70-AUTOMACOES/NOTAAS-NFSE|Notaas NFS-e]] documenta emissão, consulta e recuperação de documentos como etapas distintas.

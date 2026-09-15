# Ausência de evidência não é status operacional

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W28; Portal 213 Stage 1B R2.4 em 2026-08-20; qualificacao mensal ARX em 2026-09-08/09; fechamento semanal Relatorios Operacionais em 2026-09-14
confiabilidade: alta
ultima_revisao: 2026-09-15
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

## Exemplo conectado

Em 2026-07-07, o NinjaOne expôs inventário, conectividade, volumes, alertas e atividades de `HOST1 | Magnitos Granitos`, mas não expôs conclusão de backup nem status de Hyper-V replication. O status correto foi registrar ausência de evidência e apontar instrumentação necessária.

Em 2026-08-20, no Portal 213 Stage 1B R2.4, execucoes anteriores foram classificadas como orfas e nao autoritativas. Sem retorno autenticado de classificacao, evidence path e `MANIFEST.sha256`, o estado correto e nao iniciar o proximo checkpoint por inferencia.

Em 2026-09-08/09, a qualificacao ARX demonstrou que estatistica corrente e barra rolante nao sustentavam relatorio mensal. A cadeia so fechou agosto depois de recuperar sessoes nativas com paginacao terminal, identidade/periodo e lacunas verificadas. Setembro permaneceu parcial e o dia 07/09 de Vila Velha ficou sem classificacao, em vez de ser convertido em sucesso ou falha.

Em 2026-09-14, o cron semanal Bitdefender encontrou o cache esperado ausente ou invalido e respondeu fail-closed. O registro correto foi indisponibilidade do relatorio no ponto de consumo; a mensagem padrao nao foi promovida a diagnostico da coleta Sentinel nem do provider.

## Relações

- `BRAIN/70-AUTOMACOES/ARX-BACKUP-NINJAONE.md`
- `BRAIN/60-AGENTES/KOWALSKI.md`
- `BRAIN/20-EMPRESAS/BIKON/README.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md`
- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]

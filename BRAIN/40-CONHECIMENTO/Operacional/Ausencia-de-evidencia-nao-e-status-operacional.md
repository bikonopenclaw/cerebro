# Ausência de evidência não é status operacional

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W28
confiabilidade: alta
ultima_revisao: 2026-07-17
tags: [monitoramento, evidencia, recencia, revalidacao, ninjaone, backup, hyper-v, operacao]
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

## Exemplo conectado

Em 2026-07-07, o NinjaOne expôs inventário, conectividade, volumes, alertas e atividades de `HOST1 | Magnitos Granitos`, mas não expôs conclusão de backup nem status de Hyper-V replication. O status correto foi registrar ausência de evidência e apontar instrumentação necessária.

## Relações

- `BRAIN/70-AUTOMACOES/ARX-BACKUP-NINJAONE.md`
- `BRAIN/60-AGENTES/KOWALSKI.md`
- `BRAIN/20-EMPRESAS/BIKON/README.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Validacao-do-runtime-pos-migracao.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md`

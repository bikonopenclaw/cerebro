---
name: arx-backup
description: Use para gerar relatórios de backup ARX Backup em português Brasil, separados por cliente, com status de jobs, falhas, sucessos, riscos e recomendações; também prepara rascunhos ou jobs de envio por e-mail, sem disparar para cliente externo sem aprovação explícita.
---

# ARX Backup, relatórios

Use esta skill quando o pedido envolver **ARX Backup**, relatórios de backup, status de backup por cliente, falhas de backup, rotina de envio de relatório de backup por e-mail ou criação de jobs de envio.

## Objetivo

Gerar relatórios profissionais em português Brasil, um por cliente, com leitura executiva e técnica do backup.

## Caminhos

- Workspace: `/data/.openclaw/workspace-kowalski/arx-backup`
- Config: `/data/.openclaw/workspace-kowalski/arx-backup/config`
- Dados brutos: `/data/.openclaw/workspace-kowalski/arx-backup/dados`
- Relatórios: `/data/.openclaw/workspace-kowalski/arx-backup/relatorios`
- Rascunhos de e-mail: `/data/.openclaw/workspace-kowalski/arx-backup/email-rascunhos`
- Jobs de envio: `/data/.openclaw/workspace-kowalski/arx-backup/jobs`

## Regra de segurança

Não enviar e-mail para cliente externo sem aprovação explícita do Hebert/Puppet Master.

Pode preparar:

- relatório
- PDF/DOCX
- rascunho de e-mail
- job agendável
- lista de destinatários sugerida

Mas o disparo real fica bloqueado até aprovação.

## Entrada esperada

A skill precisa de uma destas fontes:

1. API do ARX Backup, com credenciais em arquivo local seguro.
2. Export CSV/XLSX/PDF do ARX Backup.
3. Relatório bruto enviado manualmente.
4. Pasta sincronizada com dados por cliente.

Nunca colocar senha/token dentro do relatório ou no corpo do e-mail.

## Relatório por cliente

Cada cliente deve receber relatório separado com:

1. Nome do cliente.
2. Período analisado.
3. Resumo executivo.
4. Status geral: OK, Atenção ou Crítico, sempre calculado pelos dados reais da API.
5. Total de backups executados.
6. Backups com sucesso.
7. Backups com falha.
8. Último backup válido por máquina/serviço.
9. Histórico real dos últimos 28 dias usando `TB`.
10. Falhas recorrentes.
11. Riscos e impacto.
12. Pontos de acompanhamento operacional.

## Linguagem

Português Brasil, direto, profissional e fácil para cliente entender.

Não despejar log bruto. Traduzir para impacto e ação.

Exemplo:

- Ruim: `Job failed with VSS error 0x800423f4`
- Bom: `O backup do servidor financeiro falhou por erro de snapshot. Recomendamos correção técnica para reduzir risco de perda de dados recentes.`

## Classificação operacional

- **OK:** backups recentes e sem falhas relevantes.
- **Atenção:** falhas pontuais, `CompletedWithErrors`, histórico com alerta ou erro que precisa acompanhamento.
- **Crítico:** status atual `Failed`, `Aborted`, `InProgressWithFaults`, `OverQuota`, falhas repetidas no histórico de 28 dias, servidor essencial sem proteção ou risco claro de perda de dados.

Para relatório mensal, nunca desenhar legenda ou barra de 28 dias hardcoded. Usar os campos de API `TB` para histórico total dos últimos 28 dias e `FB`, `SB`, `QB`, `HB`, `WB` para histórico por fonte. Se `TB` indicar falha, a barra visual deve refletir falha, não verde.

## Workflow padrão

1. Carregar dados do período.
2. Normalizar por cliente.
3. Separar ativos/jobs por cliente.
4. Calcular indicadores.
5. Classificar status operacional usando `T0`, `T7`, status por fonte e barras reais `TB`, `FB`, `SB`, `QB`, `HB`, `WB`.
6. Gerar relatório por cliente em Markdown primeiro.
7. Converter para PDF usando a identidade visual ARX Backup e o modelo aprovado.
8. Validar que legenda, cor da faixa e barra de 28 dias batem com a gravidade real.
9. Criar rascunho de e-mail por cliente.
10. Se o usuário aprovar, preparar job de envio e acionar somente a skill `enviar-email-arx-backup` para o disparo.

## E-mail

A skill de envio real é separada e restrita: `/data/.openclaw/agents/kowalski/agent/skills/enviar-email-arx-backup/SKILL.md`.

Use esta skill ARX Backup para gerar relatório, rascunho e job. Use `enviar-email-arx-backup` apenas depois de aprovação explícita do Hebert/Puppet Master.

Assunto sugerido:

`Relatório ARX Backup, [Cliente], [Período]`

Corpo sugerido:

```text
Olá, [Nome].

Segue o relatório de backup referente ao período [período].

Status geral: [OK/Atenção/Crítico]

Principal ponto de atenção: [resumo curto]

Qualquer dúvida, estamos à disposição.

ARX Backup
```

Se houver status crítico, o e-mail deve ser mais direto e indicar ação.

## Jobs de envio

Jobs devem ficar em `/data/.openclaw/workspace-kowalski/arx-backup/jobs` preferencialmente como `.json`, contendo:

- `cliente`
- `destinatarios`
- `assunto`
- `corpo`
- `anexos`
- `status`: `aguardando_aprovacao`, `aprovado`, `enviado`, `erro`

Nunca marcar como `aprovado` sem ordem explícita.

Para envio real, seguir o schema em `/data/.openclaw/agents/kowalski/agent/skills/enviar-email-arx-backup/references/job-email-arx-backup.md` e executar o script da skill `enviar-email-arx-backup`.


## Identidade visual específica ARX Backup

Para relatórios desta skill, usar a identidade visual própria do ARX Backup documentada em `references/identidade-visual-arx-backup.md`.

Regras principais:

- Usar as logos ARX Backup em `assets/`.
- Usar paleta escura/azul/prata derivada das logos.
- Não usar marca, assinatura, rodapé, e-mail, timbrado ou logo de terceiros em documentos ARX Backup, salvo ordem explícita do usuário para aquele documento.
- Em relatório para cliente, não citar `Cove`.
- Em relatório para cliente, não incluir recomendações ou linguagem de auditoria contra a prestação do serviço.
- Horários sempre em GMT-3.
- Usar `backup@arxcore.com.br` como e-mail de contato padrão em documentos ARX Backup.
- Usar o layout aprovado em `assets/modelos-aprovados/modelo-padrao-relatorio-mensal-arx-backup.html` como padrão para todos os relatórios mensais ARX Backup.
- Usar o layout aprovado em `assets/modelos-aprovados/modelo-padrao-relatorio-diario-arx-backup.html` como padrão para todos os relatórios diários ARX Backup.
- O layout aprovado é só base visual. Dados de status, cor da faixa e histórico devem ser sobrescritos com dados reais da API.
- Nunca manter `VERDE`, `seg ok` ou texto de sucesso herdado do modelo quando `T0`, `T7`, `TB` ou status de fonte indicarem alerta/falha.
- No relatório diário, não incluir seleção protegida se a API não trouxer caminhos literais das pastas/arquivos. Só incluir quando `_SelectionFS`, `_SimpSelectionFS` ou fonte confiável equivalente vier preenchida.

## API Cove validada

A integração JSON-RPC com Cove/ARX Backup está validada.

- Referência técnica: `references/api-cove-jsonrpc.md`
- Client base: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/arx_client.py`
- Gerador de relatório: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/gerar_relatorio_arx.py`

Para gerar relatório operacional atual:

```bash
/data/.openclaw/workspace-kowalski/arx-backup/scripts/gerar_relatorio_arx.py
```

Para monitoramento diário ARX Backup -> tickets NinjaOne, usar a skill canônica
`arx-ninjaone-ticketing`. Esta skill `arx-backup` só mantém os caminhos
operacionais para consulta e relatórios.

```bash
# Dry-run, não cria chamados
/data/.openclaw/workspace-kowalski/arx-backup/scripts/monitorar_arx_ninjaone_tickets.py

# Produção, cria chamados com deduplicação
/data/.openclaw/workspace-kowalski/arx-backup/scripts/monitorar_arx_ninjaone_tickets.py --create

# Runner usado pelo cron, com lock e log
/data/.openclaw/workspace-kowalski/arx-backup/scripts/run_monitorar_arx_ninjaone_tickets.sh
```

Regras da automação NinjaOne:

- Só abre ticket para status `Atenção` ou `Crítico`, erro total `T7` ou fonte com erro/status problemático.
- Usa OAuth user-context do NinjaOne salvo em `/data/.openclaw/workspace-kowalski/ninjaone/config/oauth-user-context-token.json` e refresh token quando necessário.
- Usa `ticketFormId=1`, formulário `Default`, validado em produção.
- Deduplica por cliente/dispositivo/assinatura do problema em `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-state.json`.
- Por regra do Hebert, todos os tickets ARX Backup devem abrir no cliente interno `00 - Bikon Tech`, nunca no cliente final. O cliente real fica no título e na descrição.
- Título padrão do ticket: `Alerta de ARX Backup - Nome do cliente`.
- Não vincular `nodeId` do cliente final sem nova ordem explícita.
- Ao fechar ticket automaticamente, enviar confirmação para o Hebert no Telegram.
- Logs ficam em `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-log.jsonl` e `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-run.log`.
- Cron OpenClaw principal: `ATIVO - ARX -> tickets NinjaOne diario 01h15 seg-qui`, id `2c387780-44b2-4ba6-9f67-0ab3d844b75a`, terça a sexta às `01:15 America/Sao_Paulo`.
- Executor shell espelhado: id `bd9fe2f3-baa7-455b-aeab-6c51e4b9e4d9`, mesma agenda, agente main.
- Cron de sábado: id `a522de30-a6a0-4690-acff-2984ee9463f4`, sábado às `01:15 America/Sao_Paulo`.

Saídas esperadas:

- `/data/.openclaw/workspace-kowalski/arx-backup/dados/account-statistics-sanitized.json`
- `/data/.openclaw/workspace-kowalski/arx-backup/relatorios/relatorio-arx-backup-YYYY-MM-DD.md`

A legenda oficial dos status Cove está na referência técnica. Não inventar nomes de status.

## Modelos aprovados

- Mensal aprovado: `assets/modelos-aprovados/modelo-padrao-relatorio-mensal-arx-backup.html`
- Diário aprovado: `assets/modelos-aprovados/modelo-padrao-relatorio-diario-arx-backup.html`
- README mensal: `assets/modelos-aprovados/README-modelo-padrao.md`
- README diário: `assets/modelos-aprovados/README-modelo-diario-padrao.md`

Quando o usuário pedir relatório diário, usar o modelo diário aprovado. Quando pedir relatório mensal, usar o modelo mensal aprovado.

## Referência

Leia `references/modelo-relatorio.md` quando for montar um novo modelo.

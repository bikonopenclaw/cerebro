# Modelo relatório diário ARX Backup

Status: em validação, ainda não aprovado pelo Hebert.

## Arquivos

- HTML: `modelo-relatorio-diario-arx-backup.html`
- PDF: `modelo-relatorio-diario-arx-backup.pdf`

## Objetivo

Relatório executivo diário por cliente/dispositivo, com foco em últimas 24 horas.

## Diferença para o mensal

- Mensal: acompanhamento consolidado e histórico dos últimos 28 dias.
- Diário: leitura rápida do último ciclo/últimas 24h para operação e cliente.

## Campos obrigatórios do diário

- Cliente
- Dispositivo
- Computador quando disponível (`MN`)
- Período: últimas 24 horas
- Status do dia calculado por API
- Último backup válido (`TL`)
- Última conclusão (`TO`)
- Status total (`T0`)
- Erros totais (`T7`)
- Status da última sessão concluída (`TJ`)
- Status por fonte relevante (`F0`, `S0`, `Q0`, `H0`, `W0` etc.)
- Pontos de acompanhamento

## Seleção de pastas e arquivos

Não incluir seção de seleção protegida se a API não trouxer caminhos literais de pastas/arquivos.

Só exibir essa seção quando houver valor real preenchido em fonte confiável, como `_SelectionFS` ou `_SimpSelectionFS`. Se a API retornar apenas fonte, volume ou quantidade, omitir do relatório diário para não gerar falsa sensação de auditoria.

## Regra crítica

O modelo é apenas base visual. Nunca usar status, faixa ou texto herdado do HTML como verdade operacional.

O relatório diário deve sobrescrever:

- status visual
- cor da faixa
- texto do status do dia
- indicadores
- pontos de acompanhamento

com dados reais da API.

## Marcador

Enquanto estiver em validação, usar marcador:

`ARX_DAILY_MODEL_DRAFT:modelo-relatorio-diario-arx-backup`

Quando aprovado pelo Hebert, migrar para `assets/modelos-aprovados/` e criar marcador definitivo.
